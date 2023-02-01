import subprocess

def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, git_repo, "../ClonedRepo"])

def install_requirements(command):
    subprocess.run([command])

def build_repo(command):
    subprocess.run([command])

def test_repo(command):
    subprocess.run([command])