import os
import yaml
import sys

from pathlib import Path

from helper_functions_git import (
    clone_repo,
    commit_and_push_changes
)
from k8s_yaml_exporter import k8s_yaml_exporter


def main():
    # read config from configuration file; config.yaml
    with open("config.yaml", 'r') as ymlfile:
        app_config = yaml.load(ymlfile)

    # Set variables
    repo_path = Path(app_config['git']['repo_path'])
    remote_repo = app_config['git']['remote_repo']
    remote_branch = app_config['git']['remote_branch']
    commits_to_print = int(app_config['git']['commits_to_print'])

    # Clone repo
    repo = clone_repo(repo_path, remote_repo, remote_branch, commits_to_print)

    # Run backup Script
    k8s_yaml_exporter()

    # Commit and push changes, 
    # or terminate program if no changes to comit
    if not commit_and_push_changes(repo):
        print('No changes, quit program')
        quit()
        

if __name__ == '__main__':
    main()