import subprocess

import click
import yaml
from kubernetes import config, client

from tensorkube.constants import KNATIVE_SERVING_NAMESPACE, CONFIG_FEATURES


def get_instance_family_from_gpu_type(gpu_type):
    gpu_type = gpu_type.lower()
    if gpu_type == 'v100':
        return 'p3'
    elif gpu_type == 'a10g':
        return 'g5'
    else:
        raise ValueError(f"Unsupported GPU type: {gpu_type}")


def apply_knative_service(service_name: str, image_url: str, yaml_file_path: str, gpus: int, gpu_type: str,
                          cpu: float = 100, memory: int = 200):
    # Load kube config
    config.load_kube_config()

    # Read the YAML file
    with open(yaml_file_path, 'r') as f:
        yaml_content = f.read()

    click.echo(f"Applying Knative service {service_name} with image {image_url} and {gpus} GPUs.")
    # Replace the placeholders with the actual values
    yaml_content = yaml_content.replace('${SERVICE_NAME}', service_name)
    yaml_content = yaml_content.replace('${IMAGE_URL}', image_url)
    yaml_content = yaml_content.replace('${GPUS}', str(gpus))

    # Load the YAML content
    yaml_dict = yaml.safe_load(yaml_content)
    if gpus > 0:
        yaml_dict['spec']['template']['spec']['nodeSelector'] = {
            'karpenter.k8s.aws/instance-family': get_instance_family_from_gpu_type(gpu_type)}
    else:
        yaml_dict['spec']['template']['spec']['containers'][0]['resources']['requests'][
            'memory'] = f'{str(int(memory))}M'
        yaml_dict['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = f'{str(int(cpu))}m'

    # Create a Kubernetes API client
    k8s_client = client.CustomObjectsApi()

    # Apply the configuration
    group = "serving.knative.dev"
    version = "v1"
    namespace = "default"
    plural = "services"

    # check if the custom object exists if yes then update else create
    try:
        existing_service = k8s_client.get_namespaced_custom_object(group, version, namespace, plural, service_name)
        resource_version = existing_service['metadata']['resourceVersion']
        # add the resource_version to the yaml dict
        yaml_dict['metadata']['resourceVersion'] = resource_version
        click.echo(f'Resource version is {resource_version}')
        # Remove immutable fields
        if 'metadata' in yaml_dict:
            if 'annotations' in yaml_dict['metadata']:
                if 'serving.knative.dev/creator' in yaml_dict['metadata']['annotations']:
                    del yaml_dict['metadata']['annotations']['serving.knative.dev/creator']
            if 'annotations' in yaml_dict['metadata']:
                if 'serving.knative.dev/lastModifier' in yaml_dict['metadata']['annotations']:
                    del yaml_dict['metadata']['annotations']['serving.knative.dev/lastModifier']
        k8s_client.patch_namespaced_custom_object(group, version, namespace, plural, service_name, yaml_dict)
        click.echo(f"Updated Knative service {service_name}.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            k8s_client.create_namespaced_custom_object(group, version, namespace, plural, yaml_dict)
            click.echo(f"Created Knative service {service_name}.")
        else:
            click.echo(f"Error applying Knative service: {e}")
            raise e


def enable_knative_selectors(namespace=KNATIVE_SERVING_NAMESPACE):
    """
    Enable the nodeSelector feature in the config-features ConfigMap.

    Args:
        namespace (str): The namespace where the ConfigMap is located. Defaults to 'knative-serving'.
    """
    # Load the kubeconfig
    config.load_kube_config()

    # Create an instance of the API class
    v1 = client.CoreV1Api()

    try:
        # Get the existing config-features ConfigMap
        config_map = v1.read_namespaced_config_map(name=CONFIG_FEATURES, namespace=namespace)

        # Update the ConfigMap data
        if config_map.data is None:
            config_map.data = {}
        config_map.data['kubernetes.podspec-nodeselector'] = 'enabled'
        config_map.data['kubernetes.podspec-affinity'] = 'enabled'

        # Update the ConfigMap
        v1.patch_namespaced_config_map(name=CONFIG_FEATURES, namespace=namespace, body=config_map)
        print(f"Successfully enabled node selector and affinity features in {CONFIG_FEATURES} ConfigMap.")
    except client.exceptions.ApiException as e:
        print(f"Exception when updating ConfigMap: {e}")
        raise


def list_deployed_services():
    # kubectl get ksvc
    command = ["kubectl", "get", "ksvc"]
    subprocess.run(command, check=True)


def delete_knative_services():
    # kubectl delete ksvc --all -n <your-namespace>
    command = ["kubectl", "delete", "ksvc", "--all", "-n", "default"]
    subprocess.run(command, check=True)  # TODO maybe wait for pods to scale down before returning


def cleanup_knative_resources():
    try:
        # kubectl delete gateway --all -n istio-system
        command = ["kubectl", "delete", "gateway", "--all", "-n", "istio-system"]
        subprocess.run(command, check=True)
        #  kubectl delete gateway --all -n knative-serving
        command = ["kubectl", "delete", "gateway", "--all", "-n", "knative-serving"]
        subprocess.run(command, check=True)
    except Exception as e:
        click.echo(f"Error while cleaning up Istio gateways: {e}")
