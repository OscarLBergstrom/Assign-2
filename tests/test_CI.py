import pytest
from flask import Flask
import requests


data_complete = {
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
