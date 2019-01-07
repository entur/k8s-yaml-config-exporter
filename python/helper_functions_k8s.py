import os

from kubernetes import client, config

def k8s_load_config():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()


def k8s_current_cluster_name():
    # kubernetes api have no idea of the cluster name, 
    # hence assuming name from local cluster config
    # assuming the cluster name is in this format SOMEIDENTIFIER_CLUSTERNAME
    try:
        contexts, active_context = config.list_kube_config_contexts()
        if active_context:
            try:
                cluster_name = active_context['context']['cluster'].rsplit('_',1)[1]
            except IndexError:
                cluster_name = active_context['context']['cluster']
        else:
            print('could not find kurrent context')
    except FileNotFoundError:
        cluster_name = ""
    return cluster_name


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def k8s_stip_lines(dict):

    try:
        del dict['metadata']['annotations']['deployment.kubernetes.io/revision']
    except KeyError:
        pass

    try:
        del dict['metadata']['annotations']['autoscaling.alpha.kubernetes.io/conditions']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['annotations']['autoscaling.alpha.kubernetes.io/current-metrics']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['annotations']['pv.kubernetes.io/bound-by-controller']
    except KeyError:
        pass

    try:
        del dict['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['annotations']['finalizers']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['annotations']['pv.kubernetes.io/bind-completed']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['annotations']['pv.kubernetes.io/bound-by-controller']
    except KeyError:
        pass

    try:
        del dict['metadata']['creationTimestamp']
    except KeyError:
        pass

    try:
        del dict['metadata']['generation']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['resourceVersion']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['selfLink']
    except KeyError:
        pass

    try:
        del dict['spec']['template']['metadata']['creationTimestamp']
    except KeyError:
        pass
    
    try:
        del dict['metadata']['uid']
    except KeyError:
        pass

    try:
        del dict['metadata']['finalizers']
    except KeyError:
        pass

    try:
        del dict['spec']['clusterIP']
    except KeyError:
        pass

    try:
        del dict['spec']['claimRef']
    except KeyError:
        pass

    try:
        del dict['status']
    except KeyError:
        pass
        
    return dict
