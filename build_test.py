import subprocess

def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, git_repo, "../ClonedRepo"])

def install_requirements():
    pass

def build_repo():
    pass

def test_repo():
    pass