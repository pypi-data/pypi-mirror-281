import time
from threading import Thread
from typing import List

import click
import yaml
from kubernetes import client, config, utils, watch
from kubernetes.client import ApiTypeError, ApiException
from pkg_resources import resource_filename
from tensorkube.constants import get_cluster_name

from tensorkube.constants import NAMESPACE, REGION, PodStatus, BUILD_TOOL


def create_namespace(namespace_name):
    config.load_kube_config()
    namespace = client.V1Namespace()
    namespace.metadata = client.V1ObjectMeta(name=namespace_name)
    v1 = client.CoreV1Api()
    v1.create_namespace(body=namespace)


def create_docker_registry_secret(secret_name: str, namespace: str, base64_encoded_dockerconfigjson: str):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    secret = client.V1Secret()
    secret.api_version = "v1"
    secret.kind = "Secret"
    secret.metadata = client.V1ObjectMeta(name=secret_name, namespace=namespace)
    secret.type = "kubernetes.io/dockerconfigjson"
    secret.data = {".dockerconfigjson": base64_encoded_dockerconfigjson}

    v1.create_namespaced_secret(namespace=namespace, body=secret)


def create_aws_secret(credentials, namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    secret_name = "aws-secret"

    secret = client.V1Secret()
    secret.metadata = client.V1ObjectMeta(name=secret_name)
    secret.string_data = {"AWS_ACCESS_KEY_ID": credentials.access_key, "AWS_SECRET_ACCESS_KEY": credentials.secret_key,
                          "AWS_SESSION_TOKEN": credentials.token}

    try:
        # Check if the secret already exists
        existing_secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
        # If the secret exists, update it
        v1.replace_namespaced_secret(name=secret_name, namespace=namespace, body=secret)
        print(f"Secret {secret_name} updated successfully in namespace {namespace}.")
    except ApiException as e:
        if e.status == 404:
            # Secret does not exist, create it
            v1.create_namespaced_secret(namespace=namespace, body=secret)
            print(f"Secret {secret_name} created successfully in namespace {namespace}.")
        else:
            print(f"An error occurred: {e}")
            raise e


def delete_aws_secret(namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    try:
        v1.read_namespaced_secret(name="aws-secret", namespace=namespace)
    except client.ApiException as e:
        if e.status == 404:
            return
        else:
            raise
    v1.delete_namespaced_secret(name="aws-secret", namespace=namespace)


def create_build_pv_and_pvc(bucket_name: str, namespace: str = NAMESPACE, region: str = REGION):
    config.load_kube_config()

    pv_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/pv.yaml')
    pvc_config_file_path = resource_filename('tensorkube', 'configurations/build_configs/pvc.yaml')
    with open(pv_config_file_path) as f:
        pv = yaml.safe_load(f)
    with open(pvc_config_file_path) as f:
        pvc = yaml.safe_load(f)

    pv['spec']['mountOptions'] = ["allow-delete", "region {}".format(region)]
    pv['spec']['csi']['volumeAttributes']['bucketName'] = bucket_name
    pv['metadata']['namespace'] = namespace

    pvc['metadata']['namespace'] = namespace

    k8s_client = client.ApiClient()
    v1 = client.CoreV1Api()

    pv_name = pv['metadata']['name']
    pvc_name = pvc['metadata']['name']

    try:
        # Check if the PV already exists
        v1.read_persistent_volume(name=pv_name)
        print(f"PersistentVolume {pv_name} already exists. Skipping creation.")
    except ApiException as e:
        if e.status == 404:
            utils.create_from_dict(k8s_client, pv)
            print(f"PersistentVolume {pv_name} created successfully.")
        else:
            print(f"An error occurred while checking PersistentVolume: {e}")
            raise e

    try:
        # Check if the PVC already exists
        v1.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
        print(f"PersistentVolumeClaim {pvc_name} already exists in namespace {namespace}. Skipping creation.")
    except ApiException as e:
        if e.status == 404:
            # PVC does not exist, proceed to create
            k8s_client = client.ApiClient()
            utils.create_from_dict(k8s_client, pvc)
            print(f"PersistentVolumeClaim {pvc_name} created successfully in namespace {namespace}.")
        else:
            print(f"An error occurred while checking PersistentVolumeClaim: {e}")
            raise e


def apply_k8s_buildkit_config(project_name: str, sanitised_project_name: str, bucket_name: str,
                              aws_account_number: str, ecr_repo_url: str,
                              namespace: str = NAMESPACE, region: str = REGION):
    config.load_kube_config()

    buildkit_config_file_path = resource_filename('tensorkube',
                                                    'configurations/build_configs/buildkit.yaml')
    with open(buildkit_config_file_path) as f:
        buildkit_config = yaml.safe_load(f)
    
    buildkit_config['metadata']['name'] = 'buildkit-{}'.format(sanitised_project_name)
    buildkit_config['metadata']['namespace'] = namespace
    buildkit_config['spec']['template']['spec']['containers'][0]['env'][0]['value'] = region
    buildkit_config['spec']['template']['spec']['containers'][0]['command'] = [ "/bin/sh", "-c",
        f"""
        apk add --no-cache curl unzip aws-cli docker
        chmod 777 /data/images
        mkdir -p /data/cache
        chmod 777 /data/cache
        ls -l /data/images
        aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {aws_account_number}.dkr.ecr.{region}.amazonaws.com
        buildctl-daemonless.sh build\
            --frontend dockerfile.v0\
            --local context=/data/build/{project_name}\
            --local dockerfile=/data/build/{project_name}\
            --output type=image,name={ecr_repo_url},push=true\
            --export-cache type=s3,region={region},bucket={bucket_name},name={get_cluster_name()}-cache,mode=max\
            --import-cache type=s3,region={region},bucket={bucket_name},name={get_cluster_name()}-cache"""
    ]

    k8s_client = client.ApiClient()
    utils.create_from_dict(k8s_client, buildkit_config)
    click.echo('Deployed a Buildkit image')


def get_build_job_pod_name(sanitised_project_name: str, namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace)
    for pod in pods.items:
        if pod.metadata.name.startswith("{}-{}".format(BUILD_TOOL, sanitised_project_name)):
            return pod.metadata.name
    return None


def check_pod_status(pod_name, namespace):
    # Load kube config
    config.load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Get the status of the pod
    pod_status = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)

    # Return the status of the pod
    return pod_status.status.phase


def find_and_delete_old_build_job(job_name: str, namespace: str = NAMESPACE):
    config.load_kube_config()
    v1 = client.BatchV1Api()
    jobs = v1.list_namespaced_job(namespace=namespace)
    for job in jobs.items:
        if job.metadata.name == job_name:
            if any(condition.type in ['Complete', 'Failed'] for condition in job.status.conditions):
                v1.delete_namespaced_job(name=job.metadata.name, namespace=namespace)
                return True
            else:
                return False

    return True


def start_streaming_pod(pod_name, namespace, status=None, container_name=None):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    # Create a stream to the pod
    # Initialize the Watch class
    watch_client = watch.Watch()
    # Stream events until the pod is ready
    print(f"Streaming events for pod {pod_name} in namespace {namespace}")
    for event in watch_client.stream(v1.list_namespaced_event, namespace=namespace):
        pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        if event['object'].involved_object.kind == 'Pod' and event['object'].involved_object.name == pod_name:
            print("Event: %s %s" % (event['type'], event['object'].message))
        if pod.status.phase != 'Pending':
            break

    print(f"Streaming logs for pod {pod_name} in namespace {namespace}")

    try:
        for event in watch_client.stream(v1.read_namespaced_pod_log, name=pod_name, namespace=namespace, follow=True,
                                         container=container_name):
            click.echo(event)
            if status:
                pod = v1.read_namespaced_pod_status(name=pod_name, namespace=namespace)
                if status.value == pod.status.phase:
                    print(f"Pod {pod_name} has reached {status.value} state")
                    return
    except client.ApiException as e:
        if e.status == 404:
            print(f"Pod {pod_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Log streaming stopped by user")
        return
    except ApiTypeError as e:
        print(f"An error occurred while streaming logs for pod {pod_name} in namespace {namespace}")
        print(e)
        return
    except Exception as e:
        print(f"An unexpected error occurred for pod {pod_name} in namespace {namespace}")
        print(e)
        raise


def start_streaming_service(service_name, namespace):
    # Load kube config
    config.load_kube_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    # Stream the service status
    try:
        while True:
            pods = v1.list_namespaced_pod(namespace, label_selector=f'serving.knative.dev/service={service_name}')
            if pods.items:
                print(f"Pods scheduled for service {service_name}: {[pod.metadata.name for pod in pods.items]}")
                break
            time.sleep(5)
        # Start streaming the logs from the pod
        for pod in pods.items:
            thread = Thread(target=start_streaming_pod,
                            args=(pod.metadata.name, namespace, PodStatus.RUNNING, 'user-container'))
            thread.start()
    except client.ApiException as e:
        if e.status == 404:
            print(f"Service {service_name} not found in namespace {namespace}")
        else:
            raise
    except KeyboardInterrupt:
        print("Service status streaming stopped by user")
        return
    except Exception as e:
        print("An unexpected error occurred for service status streaming")
        raise
