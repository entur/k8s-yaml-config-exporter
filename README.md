# Kubernetes yaml config exporter

A simple project for exporting current Kubernetes resource files.
Intended destination: git, bitbucket
Supports multiple projects for destination paths.

## Install requirements
Assuming python3 is installed.

`pip3 install -r requirements.txt`

## Setup config
check out the `config.yaml` file for possible configurations. 

Add or remove namespaces by modifying `namespaces`

Filter the `kube-system` namespace if wanted: add kube-system to the list of `namespaces`, and add apps to backup in the list of `kube_system_filter`, or leave it blank `[]`

define path to backup dir by modifying: `repo_path`

Add or remove apis by modifying `resource_types`.
Note that the resource_types must have been defined in the `k8s_client_apis.yaml`. 
Define new resource types when necessary at `k8s_client_apis.yaml`. Find the list of available APIS here: https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md

## Run
Run:
- `k8s_yaml_exporter.py` -> exports resources from current cluster to `repo_path`, assuming the cluster name is defined in the local cluster config in the format `SOMEIDENTIFIER_CLUSTERNAME` or `CLUSTERNAME`. Iterates through `resource_types`.

```
python3 k8s_yaml_exporter.py
```

or run:
- `main.py` -> pulls `remote_repo` to `repo_path` assuming `~/.ssh` exist locally. Exports resources from current cluster to `repo_path` and overwrites any files with same name, commits changes, and pushes it to `remote_repo` on `remote_branch`.

```
python3 main.py
```

## Run as k8s job in cluster.
Run as cronjob in local kubernetes cluster.

### Docker build
Build docker image: `docker build -t k8s-resources-backup:TAG .`

### Github/Bitbucket SSH setup
You need to add id_rsa and known_hosts files as secret to the cluster.

Either run:
```
kubectl create secret generic k8s-resources-backup-ssh --from-file=id_rsa=id_rsa --from-file=known_hosts=known_hosts
```

or 

```
apiVersion: v1
data:
  id_rsa: <base64 encoded private-key>
  known_hosts: <base64 encoded known_hosts>
kind: Secret
metadata:
  name: k8s-resources-backup-ssh
  namespace: default
type: Opaque

```

### Kubernetes
Deploying using HELM.
Add the following variables to helm deploy;

CLUSTER_NAME (kubernetes api has no way to know the cluster name, therefore need this variable on kubernetes)

TODO!: ADD NEW FILES ALSO! NOT ONLY CHANGES!
        HELM CHART
---

