import subprocess
import os
import pdb

def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, "https://github.com/" + git_repo + ".git"])

def install_requirements(command):
    subprocess.run([command])

def build_repo(command):
    subprocess.run([command])

def repo_test(command):
    subprocess.run([command])

def delete_repo(repo_name):
    subprocess.run(["rm","-rf", repo_name])