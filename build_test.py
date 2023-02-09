import subprocess
from pathlib import Path
import yaml
from yaml.loader import SafeLoader


"""
Summary
This program is a part of a continuous integration platform and its purpose is to clone, build, and test a git repository.
"""


"""
clone_repo
This function clones the specified *git_repo* and *branch*
"""
def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, "https://github.com/" + git_repo + ".git"])

"""
install_requirements
This function installs the specified libraries from a requirements.txt file, the *command* to install the libraries is specified in the config.yml file.
"""
def install_requirements(command, repo):
    return subprocess.run(command + [repo + "/requirements.txt"]).returncode

"""
run_command
This function runs a command in the terminal
"""
def run_command(command, repo):
    return subprocess.run(command + [repo]).returncode

"""
repo_test
This function runs unit test in the /tests folder, the *command* used to run the tests is specified in the config.yml file.
"""
def repo_test(command, repo):
    return subprocess.run(command + [repo + "/tests"]).returncode

"""
delete_repo
This function deletes the cloned git repo.
"""
def delete_repo(repo):
    subprocess.run(["rm","-rf", repo])

"""
initialization
This command clones the specified *repo* and *branch* to the directory *dir*, it reads appropriate commands from the config.yml file
and calls the other methods to install requirements, unit test, compile code and finally delete the repo.

It returns the exit codes for installing libraries, compiling code, and running unit tests.
"""
def initialization(repo, branch, dir, config_file):
    path = Path(config_file)
    if not path.is_file():
        raise FileNotFoundError("Config file not found!")
    
    # Open the file and load the file
    clone_repo(repo, branch)
    install_code = -1
    build_code = -1 
    test_code = -1
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
    return test_code, install_code, build_code
