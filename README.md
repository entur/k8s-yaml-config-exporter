# Kubernetes yaml config exporter

A simple script for exporting current kubernetes files.
Intended destination: git
Supports multiple projects for destination paths.

## Run
`./k8s_yaml_exporter.sh`

## Specifying types to export
`TYPES="deployment" ./k8s_yaml_exporter.sh`

## Specifying destination folder
`BASEPATH=../devsetup/roles/cloud/files/ ./k8s_yaml_exporter.sh`


## Licence
Licensed under the EUPL, Version 1.2. See LICENSE.txt