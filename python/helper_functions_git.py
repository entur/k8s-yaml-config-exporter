import os
import datetime

from git import Repo, Git 


# Print repo info
def print_repository(repo):
    print('Repo description: {}'.format(repo.description))
    print('Repo active branch is {}'.format(repo.active_branch))
    for remote in repo.remotes:
        print('Remote named \'{}\' with URL \'{}\''.format(remote, remote.url))
    print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))


# Print Commit Info
def print_commit(commit):
    print('----')
    print(str(commit.hexsha))
    print('\'{}\' by {} ({})'.format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str(commit.authored_datetime))
    print(str('count: {} and size: {}'.format(commit.count(),
                                              commit.size)))



# Clone or pull repo
def clone_repo(repo_path, remote_url, remote_branch, commits_to_print):
    # create Repo object and clone remote repo
    git_ssh_identity_file = os.path.expanduser('~/.ssh/id_rsa')
    git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
    with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
        if not os.path.exists(repo_path):
            repo = Repo.clone_from(remote_url, repo_path, branch=remote_branch, recursive=True)
        else:
            repo = Repo(repo_path)
            print('Project exist locally, try pulling')
            repo.remotes.origin.pull()

    # check that the repository loaded correctly
    if not repo.bare:
        print('Repo at {} successfully loaded.'.format(repo_path))
        print_repository(repo)

        # create list of commits then print some of them to stdout
        commits = list(repo.iter_commits(remote_branch))[:commits_to_print]
        for commit in commits:
            print_commit(commit)
            pass
    else:
        print('Could not load repository at {} :('.format(repo_path))
    
    return repo


def commit_and_push_changes(repo):
    
    # get time
    now = str(datetime.datetime.now()).split('.')[0]

    # Commit changes
    diffs = repo.git.diff('HEAD', name_only=True)
    if diffs:
        for file in diffs.split('\n'):
            print('----')
            repo.git.add(file)
            print('Added: ',file)


    # Take care of untraceked files
    untracked_files = repo.untracked_files
    if untracked_files:
        for untracked_file in untracked_files:
            repo.git.add(untracked_file)
            print('Added untracked file: ',untracked_file)
    
    # Bulk commit and push
    if diffs or untracked_files:

        git_username = os.environ.get('GIT_USERNAME')
        git_user_email = os.environ.get('GIT_USER_EMAIL')
        if git_username and git_user_email:
            repo.config_writer().set_value("user", "name", git_username).release()
            repo.config_writer().set_value("user", "email", git_user_email).release()

        repo.git.commit('-m', 'Automatic backup at ' + now)
        print('Comitted above files at ', now)
        print('---- \n')
        # Push changes
        print('Pushing changes...')
        repo.git.push()
        return True
    else:
        print('----')
        return False
        