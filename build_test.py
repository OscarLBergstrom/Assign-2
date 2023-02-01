import subprocess

def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, git_repo])

def install_requirements(command):
    subprocess.run(command)

def build_repo(command):
    subprocess.run([command])

def test_repo(command):
    subprocess.run(command).returncode

def delete_repo(repo_name):
    subprocess.run(["rm","-rf",repo_name])

try:
    clone_repo("git@github.com:OscarLBergstrom/Group-13.git","main")
    install_requirements(["pip3","install","-r","requirements.txt"])
    response_test = test_repo(["pytest","-s"])
    print(response_test)
    delete_repo("Group-13")
except Exception as e:
    print("An error ocurred\n")
    print("Error: " + str(e))
