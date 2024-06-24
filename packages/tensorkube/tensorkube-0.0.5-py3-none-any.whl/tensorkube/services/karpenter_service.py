import click
import yaml
from kubernetes import client, config
from pkg_resources import resource_filename

from tensorkube.constants import get_cluster_name


def apply_ec2nodeclass():
    file_name = resource_filename('tensorkube', 'configurations/karpenter_ec2nodeclass.yaml')
    with open(file_name, 'r') as file:
        yaml_doc = yaml.safe_load(file)

    # initialise the kubernetes client
    config.load_kube_config()
    api_instance = client.CustomObjectsApi()

    group = "karpenter.k8s.aws"
    version = "v1beta1"
    namespace = "default"
    plural = "ec2nodeclasses"
    name = "default"

    yaml_doc['spec']['role'] = f"KarpenterNodeRole-{get_cluster_name()}"
    yaml_doc['spec']['subnetSelectorTerms'][0]['tags']['karpenter.sh/discovery'] = get_cluster_name()
    yaml_doc['spec']['securityGroupSelectorTerms'][0]['tags']['karpenter.sh/discovery'] = get_cluster_name()

    try:
        # Check if the resource already exists
        existing_resource = api_instance.get_cluster_custom_object(
            group=group, version=version, plural=plural, name=name
        )
        print(f"Resource {name} already exists. Skipping creation.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            # Resource does not exist, proceed to create
            api_instance.create_cluster_custom_object(
                group=group, version=version, plural=plural, body=yaml_doc
            )
            print(f"Resource {name} created successfully.")
        else:
            print(f"An error occurred: {e}")
            raise e


def apply_nodepools():
    file_name = resource_filename('tensorkube', 'configurations/karpenter_nodepool.yaml')
    with open(file_name, 'r') as file:
        yaml_doc = yaml.safe_load(file)

    # initialise the kubernetes client
    config.load_kube_config()
    api_instance = client.CustomObjectsApi()

    group = "karpenter.sh"
    version = "v1beta1"
    namespace = "default"
    plural = "nodepools"
    name = "default"
    try:
        # Check if the resource already exists
        existing_resource = api_instance.get_cluster_custom_object(
            group=group, version=version, plural=plural, name=name
        )
        print(f"Resource {name} already exists. Skipping creation.")
    except client.exceptions.ApiException as e:
        if e.status == 404:
            # Resource does not exist, proceed to create
            api_instance.create_cluster_custom_object(
                group=group, version=version, plural=plural, body=yaml_doc
            )
            print(f"Resource {name} created successfully.")
        else:
            print(f"An error occurred: {e}")
            raise e


def apply_karpenter_configuration():
    apply_ec2nodeclass()
    apply_nodepools()


def delete_ec2nodeclasses():
    config.load_kube_config()
    api_instance = client.CustomObjectsApi()

    group = "karpenter.k8s.aws"
    version = "v1beta1"
    plural = "ec2nodeclasses"

    ec2nodeclasses = api_instance.list_cluster_custom_object(group, version, plural)

    for ec2nodeclass in ec2nodeclasses:
        api_instance.delete_cluster_custom_object(group=group, version=version, plural=plural,
                                                  name=ec2nodeclass['metadata']['name'])
        click.echo(f'Deleted ec2nodeclass: {ec2nodeclass["metadata"]["name"]}')
    click.echo(f'Deleted all ec2nodeclasses.')


def delete_nodepools():
    config.load_kube_config()
    api_instance = client.CustomObjectsApi()

    group = "karpenter.sh"
    version = "v1beta1"
    plural = "nodepools"

    nodepools = api_instance.list_cluster_custom_object(group=group, version=version, plural=plural)

    for nodepool in nodepools:
        api_instance.delete_cluster_custom_object(group=group, version=version, plural=plural,
                                                  name=nodepool['metadata']['name'])
        click.echo(f'Deleted nodepool: {nodepool["metadata"]["name"]}')
    click.echo(f'Deleted all nodepools.')


def delete_karpenter_resources():
    delete_ec2nodeclasses()
    delete_nodepools()
