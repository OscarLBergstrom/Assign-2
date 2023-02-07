import subprocess
import os
import pdb
from pathlib import Path
import yaml
from yaml.loader import SafeLoader


def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, "https://github.com/" + git_repo + ".git"])

def install_requirements(command, repo):
    code = subprocess.run(command + [repo + "/requirements.txt"]).returncode
    return code
def run_command(command, repo):
    return subprocess.run(command + [repo]).returncode

def repo_test(command, repo):
    return subprocess.run(command + [repo + "/tests"]).returncode

def delete_repo(repo):
    subprocess.run(["rm","-rf", repo])
    
def initialization(repo, branch, dir, config_file):
    path = Path(config_file)
    if not path.is_file():
        raise FileNotFoundError("Config file not found!")
    
    # Open the file and load the file
    clone_repo(repo, branch)
    exitcode = -1
    with open(config_file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        
        install = data['jobs']['build-and-test']['steps']['requirements']['command']
        build = data['jobs']['build-and-test']['steps']['build']['command']
        testing = data['jobs']['build-and-test']['steps']['run']['command']
        syntax = data['jobs']['build-and-test']['steps']['syntax']['command']
        
        if not install == None:
            install_command = install.split()
            install_code = install_requirements(install_command, dir)
        else:
            raise Exception("Please enter requirements command in config file. ?")
        if not build == None:
            build_command = build.split()
            build_code = run_command(build_command, dir)
        elif not syntax == None:
            syntax_command = syntax.split()
            build_code = run_command(syntax_command, dir)
        else:
            raise Exception("Please enter a build or syntax command in config file.")
        if not testing == None:
            testing_command = testing.split()
            test_code = repo_test(testing_command, dir)
        else:
            raise Exception("Please enter unit test command in config file.")
            
        
    delete_repo(dir)
    #pdb.set_trace()
    return test_code, install_code, build_code
