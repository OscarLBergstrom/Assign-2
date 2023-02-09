import pytest
import mail
from flask import Flask
import requests

def test_generate_build_test_message_success():  #Test for correct message with all error codes correct
    user_email = "test@gmail.com"
    commit_id = "test_commit"   
    result = [0,0,0]
    message = mail.generate_build_test_message(user_email, result,commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    assert "Test: All test passed" in content
    assert "Install: Install successfull" in content
    assert "Build: Build successfull" in content
    
    

def test_generate_build_test_message_failed(): #Tests with every step failed
    user_email = "test@gmail.com"
    commit_id = "test_commit"  
    result = [1,1,1]
    message = mail.generate_build_test_message(user_email, result,commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    #Check that extra text is not in the message
    assert "Test: All test passed" not in content
    assert "Install: Install successfull" not in content
    assert "Build: Build successfull" not in content
    #Check correct text is in the message
    assert "Test: One or more test cases failed" in content
    assert "Install: Something went wrong in the installation step" in content
    assert "Build: Something went wrong in the build step" in content


data_complete = {
    "repository": {
    "id": 596040156,
    "node_id": "R_kgDOI4bZ3A",
    "name": "Test_repo",
    "full_name": "OscarLBergstrom/Test_repo",
    "private": False,
    "owner": {
      "name": "OscarLBergstrom",
      "email": "64008380+OscarLBergstrom@users.noreply.github.com",
      "login": "OscarLBergstrom",
      "id": 64008380,
      "node_id": "MDQ6VXNlcjY0MDA4Mzgw",
      "avatar_url": "https://avatars.githubusercontent.com/u/64008380?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/OscarLBergstrom",
      "html_url": "https://github.com/OscarLBergstrom",
      "followers_url": "https://api.github.com/users/OscarLBergstrom/followers",
      "following_url": "https://api.github.com/users/OscarLBergstrom/following{/other_user}",
      "gists_url": "https://api.github.com/users/OscarLBergstrom/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/OscarLBergstrom/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/OscarLBergstrom/subscriptions",
      "organizations_url": "https://api.github.com/users/OscarLBergstrom/orgs",
      "repos_url": "https://api.github.com/users/OscarLBergstrom/repos",
      "events_url": "https://api.github.com/users/OscarLBergstrom/events{/privacy}",
      "received_events_url": "https://api.github.com/users/OscarLBergstrom/received_events",
      "type": "User",
      "site_admin": False
    }},
    "ref": "refs/heads/test_branch",
    "commits":[{
    "id": "7ce2a310efa9b56d54bb136e6961724eec1239ad",
    "tree_id": "f52085b17a33459de7c30fdc825bab20f306377b",
    "distinct": True,
    "message": "fix #2 fix #1 modify function to clone build and test the cloned repo",
    "timestamp": "2023-02-01T12:44:39+01:00",
    "url": "https://github.com/OscarLBergstrom/Assign-2/commit/7ce2a310efa9b56d54bb136e6961724eec1239ad",
    "author": {
        "name": "Felipe Oliver",
        "email": "felioliver96@gmail.com",
        "username": "Yatex"
    },
    "committer": {
        "name": "Felipe Oliver",
        "email": "felioliver96@gmail.com",
        "username": "Yatex"
    },
    "added": [
        "__pycache__/build_test.cpython-310-pytest-7.2.1.pyc",
        "tests/__pycache__/test_CI.cpython-310-pytest-7.2.1.pyc"
    ],
    "removed": [

    ],
    "modified": [
        "build_test.py"
    ]
    }]
}

data_without_url = {
      "id": "7ce2a310efa9b56d54bb136e6961724eec1239ad",
      "tree_id": "f52085b17a33459de7c30fdc825bab20f306377b",
      "distinct": True,
      "message": "fix #2 fix #1 modify function to clone build and test the cloned repo",
      "timestamp": "2023-02-01T12:44:39+01:00",
      "author": {
        "name": "Felipe Oliver",
        "email": "felioliver96@gmail.com",
        "username": "Yatex"
      },
      "committer": {
        "name": "Felipe Oliver",
        "email": "felioliver96@gmail.com",
        "username": "Yatex"
      },
      "added": [
        "__pycache__/build_test.cpython-310-pytest-7.2.1.pyc",
        "tests/__pycache__/test_CI.cpython-310-pytest-7.2.1.pyc"
      ],
      "removed": [

      ],
      "modified": [
        "build_test.py"
      ]
    }

def test_server_response(): 
    response = requests.post("https://8cb3-2001-6b0-1-1041-b50e-adce-a282-b70e.eu.ngrok.io/payload",json = data_complete)
    assert response.status_code == 200

def test_server_invalid_data():
    response = requests.post("https://8cb3-2001-6b0-1-1041-b50e-adce-a282-b70e.eu.ngrok.io/payload",json = data_without_url)
    assert response.status_code == 400
