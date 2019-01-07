import json
import yaml
import os

from itertools import product
from kubernetes import client,config
from pathlib import Path

from helper_functions_k8s import (
    k8s_load_config,
    k8s_current_cluster_name,
    create_dir,
    k8s_stip_lines
)


def k8s_yaml_exporter():
    # Load cluster config
    k8s_load_config()

    # Retrieve cluster name
    # Quit if cluster name is unkown
    cluster_name = k8s_current_cluster_name()
    if not cluster_name:
        print('Could not find Cluster name. Checking for ENV Variable "CLUSTER_NAME"')
        cluster_name = os.environ.get('CLUSTER_NAME')
        if not cluster_name:
            print('Could not find ENV variable either...quitting')
            quit()
        print("found CLUSTER_NAME, CLUSTER_NAME=", cluster_name)


    # Get k8s_client apis
    with open("k8s_client_apis.yaml", 'r') as ymlfile:
        api_mapping = yaml.load(ymlfile)
    api_list_resources = api_mapping['k8s_client_apis']['list_apis']
    api_read_resource = api_mapping['k8s_client_apis']['read_apis']


    # Get config
    with open("config.yaml", 'r') as ymlfile:
        app_config = yaml.load(ymlfile)
    # Get list of namespaces and resources_types to backup
    backup_dir = app_config['git']['repo_path']
    namespaces = app_config['kubernetes']['namespaces']
    resource_types = app_config['kubernetes']['resource_types']
    kube_system_apps = app_config['kubernetes']['kube_system_filter']


    # Loop through each resourcetype in each namespace
    for namespace,resource_type in product(namespaces,resource_types):

        # Check if the current resourcetype is to be backed
        if resource_type in api_list_resources:

            # check if it is namespace specific;
            if "namespaced" in api_list_resources[resource_type]:
                list_func = eval(api_list_resources[resource_type])(namespace,watch=False)
            else:
                namespace = "no_namespace"
                list_func = eval(api_list_resources[resource_type])(watch=False)

            # Loop through each resource and return data
            for resource in list_func.items:
                
                if any(kube_system_apps):
                    if namespace == 'kube-system' and not any(resource.metadata.name in s for s in kube_system_apps): # resource.metadata.name in str(kube_system_apps):
                        continue

                # Check if the current resourcetype is to be backed
                if resource_type in api_read_resource:
                    # check if it is namespace specific
                    if "namespaced" in api_read_resource[resource_type]:
                        read_func = eval(api_read_resource[resource_type])(resource.metadata.name,namespace,export=True,exact=True,_preload_content=False)
                    else:
                        namespace = "no_namespace"
                        read_func = eval(api_read_resource[resource_type])(resource.metadata.name,_preload_content=False)
                else:
                     continue
                
                # deserialize json to python object, prepare fo yaml conversion
                resource_read = json.loads(read_func.data)

                # Strip the object for some predefined parameters
                resource_read = k8s_stip_lines(resource_read)


                # Save yaml file
                dir_path = Path(backup_dir +  '/' + cluster_name + '/' + namespace + '/' + resource_type)
                create_dir(dir_path)
                file_path = Path(str(dir_path) + '/' + resource.metadata.name + '-' + resource_type + '.yaml')
                with open(file_path, 'w') as outfile:
                    yaml.dump(resource_read, outfile, default_flow_style=False)
                
                print(file_path)
        else:
            continue



if __name__ == '__main__':
    k8s_yaml_exporter()

