import pytest
from pathlib import Path
from build_test import *
from flask import Flask
import requests
import notify
from server import app


def test_clone_repo():
    """
    This tests if the cloning function works properly
    """
    clone_repo("OscarLBergstrom/Group-13", "testfest")
    path = Path('Group-13')
    assert path.exists() == True


def test_installation():
    """
    This tests if installation of required libraries works properly
    """
    code = install_requirements(['pip', 'install', '-r'], "Group-13")
    assert code == 0


def test_syntax():
    """
    This tests whether compilation/syntax testing is working properly
    """
    code = run_command(['python', '-m', 'compileall'], "Group-13")
    assert code == 0


def test_testing():
    """
    This tests if the automatic unit testing functionality is working.
    """
    res = repo_test(['python', '-m', 'pytest'], "Group-13")
    exit_code = res[0]
    assert exit_code == 2


def test_delete_repo():
    """
    This tests if the program successfully deletes the repository
    """
    delete_repo("Group-13")
    path = Path('Group-13')
    assert path.exists() == False


def test_exception_installation():
    """
    This test checks if the correct exception is thrown when a faulty config file is used.
    """
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'yml_configs/config_example_noinstall.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)


def test_exception_unittest():
    """
    This test checks if the correct exception is thrown when a faulty config file is used.
    """
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'yml_configs/config_example_notest.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)


def test_exception_buildandsyntax():
    """
    This test checks if the correct exception is thrown when a faulty config file is used.
    """
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'yml_configs/config_example_nobuildandsyntax.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)


def test_no_exception():
    """
    This test checks if the correct exception is thrown when a faulty config file is used.
    """
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'yml_configs/config_example.yml'
    codes = initialization(repo, branch, dir, config_file)
    codes = codes[:-1]  # to get rid of the log
    assert codes == (2, 0, 0)


def test_generate_build_test_message_success():  # Test for correct message with all error codes correct
    user_email = "test@gmail.com"

    commit_id = "test_commit"
    result = [0, 0, 0, "test logs here"]
    message = notify.generate_build_test_message(user_email, result, commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    assert "Test: All test passed" in content
    assert "Install: Install successfull" in content
    assert "Build: Build successfull" in content


def test_generate_build_test_message_failed():  # Tests with every step failed
    user_email = "test@gmail.com"
    commit_id = "test_commit"
    test_logs = "test logs here"
    result = [1, 1, 1, test_logs]
    message = notify.generate_build_test_message(user_email, result, commit_id)
    content = message.get_content()
    assert message["To"] == user_email
    assert message["Subject"] == "Result from group13CI"
    # Check that extra text is not in the message
    assert "Test: All test passed" not in content
    assert "Install: Install successfull" not in content
    assert "Build: Build successfull" not in content
    # Check correct text is in the message
    assert "Test: One or more test cases failed" in content
    assert "Install: Something went wrong in the installation step" in content
    assert "Build: Something went wrong in the build step" in content
    assert test_logs in content


def test_server_response():
    response = requests.post(
        "https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io/payload", json=data_complete)
    assert response.status_code == 200


def test_server_invalid_data():
    response = requests.post(
        "https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io/payload", json=data_without_url)
    assert response.status_code == 400


@pytest.fixture()
def client():
    return app.test_client()


def test_display_builds(client):
    response = requests.get("https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io/build")
    assert b"All builds:" in response.content
    ngrok_address = "https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io"
    assert bytes("Build 63e4b8aeda0c14382f8ec65e of commit 1 can be found <a href=\"" + \
            ngrok_address + "/build/63e4b8aeda0c14382f8ec65e\">here</a><br>", "utf-8") in response.content


def test_display_build_found(client):
    response = requests.get("https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io/build/63e4b8aeda0c14382f8ec65e")
    assert b"Build successfull" in response.content
    assert b"Commit 1 was built on: 12/12/12" in response.content


def test_display_build_not_found(client):
    response = requests.get("https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io/build/test100")
    assert b"This build was not found" in response.content


# Json files for testing


data_complete = {
    "ref": "refs/heads/test_branch",
    "before": "17250413f46c4117edc89b256fec7d4819bbf48e",
    "after": "4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
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
        },
        "html_url": "https://github.com/OscarLBergstrom/Test_repo",
        "description": None,
        "fork": False,
        "url": "https://github.com/OscarLBergstrom/Test_repo",
        "forks_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/forks",
        "keys_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/teams",
        "hooks_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/hooks",
        "issue_events_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues/events{/number}",
        "events_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/events",
        "assignees_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/assignees{/user}",
        "branches_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/branches{/branch}",
        "tags_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/tags",
        "blobs_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/languages",
        "stargazers_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/stargazers",
        "contributors_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/contributors",
        "subscribers_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/subscribers",
        "subscription_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/subscription",
        "commits_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/contents/{+path}",
        "compare_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/merges",
        "archive_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/downloads",
        "issues_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues{/number}",
        "pulls_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/labels{/name}",
        "releases_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/releases{/id}",
        "deployments_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/deployments",
        "created_at": 1675248077,
        "updated_at": "2023-02-01T10:44:03Z",
        "pushed_at": 1676032346,
        "git_url": "git://github.com/OscarLBergstrom/Test_repo.git",
        "ssh_url": "git@github.com:OscarLBergstrom/Test_repo.git",
        "clone_url": "https://github.com/OscarLBergstrom/Test_repo.git",
        "svn_url": "https://github.com/OscarLBergstrom/Test_repo",
        "homepage": None,
        "size": 5,
        "stargazers_count": 0,
        "watchers_count": 0,
        "language": "Python",
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "has_discussions": False,
        "forks_count": 0,
        "mirror_url": None,
        "archived": False,
        "disabled": False,
        "open_issues_count": 0,
        "license": None,
        "allow_forking": True,
        "is_template": False,
        "web_commit_signoff_required": False,
        "topics": [

        ],
        "visibility": "public",
        "forks": 0,
        "open_issues": 0,
        "watchers": 0,
        "default_branch": "main",
        "stargazers": 0,
        "master_branch": "main"
    },
    "pusher": {
        "name": "OscarLBergstrom",
        "email": "64008380+OscarLBergstrom@users.noreply.github.com"
    },
    "sender": {
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
    },
    "created": False,
    "deleted": False,
    "forced": False,
    "base_ref": None,
    "compare": "https://github.com/OscarLBergstrom/Test_repo/compare/17250413f46c...4f2c5d1d9255",
    "commits": [
        {
            "id": "4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
            "tree_id": "9e8202856b04d93d7a36eb2938ec2d44a59eb531",
            "distinct": True,
            "message": "added reqs",
            "timestamp": "2023-02-10T13:32:20+01:00",
            "url": "https://github.com/OscarLBergstrom/Test_repo/commit/4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
            "author": {
                "name": "Oscar Bergstrom",
                "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
            },
            "committer": {
                "name": "Oscar Bergstrom",
                "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
            },
            "added": [
                "requirements.txt"
            ],
            "removed": [

            ],
            "modified": [

            ]
        }
    ],
    "head_commit": {
        "id": "4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
        "tree_id": "9e8202856b04d93d7a36eb2938ec2d44a59eb531",
        "distinct": True,
        "message": "added reqs",
        "timestamp": "2023-02-10T13:32:20+01:00",
        "url": "https://github.com/OscarLBergstrom/Test_repo/commit/4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
        "author": {
            "name": "Oscar Bergstrom",
            "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
        },
        "committer": {
            "name": "Oscar Bergstrom",
            "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
        },
        "added": [
            "requirements.txt"
        ],
        "removed": [

        ],
        "modified": [

        ]
    }
}

data_without_url = {
    "ref": "refs/heads/test_branch",
    "before": "17250413f46c4117edc89b256fec7d4819bbf48e",
    "after": "4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
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
        },
        "html_url": "https://github.com/OscarLBergstrom/Test_repo",
        "description": None,
        "fork": False,
        "url": "https://github.com/OscarLBergstrom/Test_repo",
        "forks_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/forks",
        "keys_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/teams",
        "hooks_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/hooks",
        "issue_events_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues/events{/number}",
        "events_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/events",
        "assignees_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/assignees{/user}",
        "branches_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/branches{/branch}",
        "tags_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/tags",
        "blobs_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/languages",
        "stargazers_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/stargazers",
        "contributors_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/contributors",
        "subscribers_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/subscribers",
        "subscription_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/subscription",
        "commits_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/contents/{+path}",
        "compare_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/merges",
        "archive_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/downloads",
        "issues_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/issues{/number}",
        "pulls_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/labels{/name}",
        "releases_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/releases{/id}",
        "deployments_url": "https://api.github.com/repos/OscarLBergstrom/Test_repo/deployments",
        "created_at": 1675248077,
        "updated_at": "2023-02-01T10:44:03Z",
        "pushed_at": 1676032346,
        "git_url": "git://github.com/OscarLBergstrom/Test_repo.git",
        "ssh_url": "git@github.com:OscarLBergstrom/Test_repo.git",
        "clone_url": "https://github.com/OscarLBergstrom/Test_repo.git",
        "svn_url": "https://github.com/OscarLBergstrom/Test_repo",
        "homepage": None,
        "size": 5,
        "stargazers_count": 0,
        "watchers_count": 0,
        "language": "Python",
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "has_discussions": False,
        "forks_count": 0,
        "mirror_url": None,
        "archived": False,
        "disabled": False,
        "open_issues_count": 0,
        "license": None,
        "allow_forking": True,
        "is_template": False,
        "web_commit_signoff_required": False,
        "topics": [

        ],
        "visibility": "public",
        "forks": 0,
        "open_issues": 0,
        "watchers": 0,
        "default_branch": "main",
        "stargazers": 0,
        "master_branch": "main"
    },
    "pusher": {
        "name": "OscarLBergstrom",
        "email": "64008380+OscarLBergstrom@users.noreply.github.com"
    },
    "sender": {
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
    },
    "created": False,
    "deleted": False,
    "forced": False,
    "base_ref": None,
    "compare": "https://github.com/OscarLBergstrom/Test_repo/compare/17250413f46c...4f2c5d1d9255",
    "commits": [
        {
            "tree_id": "9e8202856b04d93d7a36eb2938ec2d44a59eb531",
            "distinct": True,
            "message": "added reqs",
            "timestamp": "2023-02-10T13:32:20+01:00",
            "author": {
                "name": "Oscar Bergstrom",
                "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
            },
            "committer": {
                "name": "Oscar Bergstrom",
                "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
            },
            "added": [
                "requirements.txt"
            ],
            "removed": [

            ],
            "modified": [

            ]
        }
    ],
    "head_commit": {
        "id": "4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
        "tree_id": "9e8202856b04d93d7a36eb2938ec2d44a59eb531",
        "distinct": True,
        "message": "added reqs",
        "timestamp": "2023-02-10T13:32:20+01:00",
        "url": "https://github.com/OscarLBergstrom/Test_repo/commit/4f2c5d1d9255cfbdda1ceb16bf98f8b9c0c926e3",
        "author": {
            "name": "Oscar Bergstrom",
            "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
        },
        "committer": {
            "name": "Oscar Bergstrom",
            "email": "Nonethyjvqvhjncjzbbdxu@tmmbt.com"
        },
        "added": [
            "requirements.txt"
        ],
        "removed": [

        ],
        "modified": [

        ]
    }
}
