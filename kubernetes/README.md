# k8s-resources-backup

The required manifest to deploy k8s-resources-backup

## Secrets

Pull and push to git repo requires ssh-key setup.

The secrets are made from two files: known_hostse and private key id_rsa. This command creates the correct secret:

`kubectl create secret generic k8s-resources-backup-ssh --from-file=known_hosts=[[PATH TO known_hosts]] --from-file=id_rsa=[[PATH TO PRIVATE KEY]]`
