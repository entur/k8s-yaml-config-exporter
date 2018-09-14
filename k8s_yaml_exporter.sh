#!/bin/bash

# Export yaml files from current kubernetes cluster

# Licensed under the EUPL, Version 1.2 or – as soon they will be approved by
# the European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
#   https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence.


if which python3
then
    echo "Detected python3 installed"
else
    echo "requires python3 to be installed with json and yaml imports";
    echo "pip install yaml/pyyaml"
    echo "pip install json"
    exit 1
fi

# Where to find kubernetes yaml files
: ${BASEPATH="../roles/cloud/files"}

# What kuberentes types to export. SINGULARITY

# export of clusterrolebinding is not supported
: ${TYPES="configmap daemonset persistentvolume deployment statefulset service persistentvolumeclaim cronjob horizontalpodautoscaler ingress replicationcontroller podtemplate"}
project=$(kubectl config current-context |  sed 's/.*_//' |  sed 's/-.*//');

# Tip: export all projects:
# for project in carbon neon radon; do echo $project; gcp_context.sh $project; ./k8s_yaml_exporter.sh; done

read -p "Hello $USER. Do you want to export yaml files for gcp k8s ${project} to base path ${BASEPATH}?" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then


    for type in ${TYPES}
    do
        echo "---------- $type -----------------"

        kubectl get ${type} --all-namespaces  | tr -s ' ' | cut -d' ' -f1-2 | grep -v NAME | while read line
        do
            if [ "${type}" == "persistentvolume" ]
            then
                read name size <<< ${line};
                namespaceArgument=""
            else
                read namespace name <<< ${line};
                namespaceArgument="--namespace ${namespace}"
            fi

            if [[ "${namespace}" = *"kube"* && "$name" != "traefik" ]]
            then
                echo "Detected kube in namespace ${namespace} for type ${type}. Ignoring."
                continue;
            fi

            echo "Exporting ${name} of type $type in namespace $namespace"

            if [[ "${name}" = *"$type" ]]
            then
                echo "omiting type ${type} as it is already present in name: ${name}"
                destinationFile="${BASEPATH}/${project}/${type}/${name}.yaml"
            else
                destinationFile="${BASEPATH}/${project}/${type}/${name}-${type}.yaml"
            fi

            tmpFile="/tmp/tmpfileforme"


            kubectl  ${namespaceArgument} get --export -o=json ${type} ${name} | jq --sort-keys \
            'del(
                .metadata.annotations."autoscaling.alpha.kubernetes.io/conditions",
                .metadata.annotations."autoscaling.alpha.kubernetes.io/current-metrics",
                .metadata.annotations."pv.kubernetes.io/bound-by-controller",
                .metadata.annotations."deployment.kubernetes.io/revision",
                .metadata.annotations."kubectl.kubernetes.io/last-applied-configuration",
                .metadata.annotations.finalizers,
                .metadata.annotations."pv.kubernetes.io/bind-completed",
                .metadata.annotations."pv.kubernetes.io/bound-by-controller",
                .metadata.creationTimestamp,
                .metadata.generation,
                .metadata.resourceVersion,
                .metadata.selfLink,
                .metadata.uid,
                .metadata.finalizers,
                .spec.clusterIP,
                .spec.claimRef,
                .status
            )' | python3 -c 'import sys, yaml, json; yaml.safe_dump(json.load(sys.stdin), sys.stdout, default_flow_style=False)' > ${tmpFile}

            length=$(cat ${tmpFile} | wc -l)
            if [ $length == 0 ]
            then
                echo "File $tmpFile was empty. Will not move to destination ${destinationFile}"
            else
                mkdir -p ${BASEPATH}/${project}/${type}
                mv ${tmpFile} ${destinationFile}
            fi
        done;

        echo "Done: ---- $type -----------------"
    done

    echo "Done"

else
    echo "Run the script like this, making sure your BASEPATH is correct!"
    echo "BASEPATH=${BASEPATH} $0"
fi