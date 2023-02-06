import subprocess
import os

repo = "temp"

def clone_repo(git_repo, branch):
    subprocess.run(["git","clone","-b", branch, "https://github.com/" + git_repo + ".git", "../" + repo])

def install_requirements(command):
    subprocess.run(command)

def build_repo(command):
    subprocess.run([command])

def test_repo(repo):
   # subprocess.run(["cd", "../" + repo])
    subprocess.run(["python3", "-m", "pytest", "tests", "../" + repo])

def delete_repo(repo_name):
    subprocess.run(["rm","-rf","../"+repo_name])

 #https://github.com/OscarLBergstrom/Group-13.git
 
clone_repo("OscarLBergstrom/Group-13", "testfest")
install_requirements(["pip", "install", "-r", "../temp/requirements.txt"])
test_repo(repo)
delete_repo(repo)

# try:
#     clone_repo("git@github.com:OscarLBergstrom/Group-13.git","main")
#     install_requirements(["pip3","install","-r","requirements.txt"])
#     response_test = test_repo(["pytest","-s"])
#     print(response_test)
#     delete_repo("Group-13")
# except Exception as e:
#     print("An error ocurred\n")
#     print("Error: " + str(e))
