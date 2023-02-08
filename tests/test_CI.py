import pytest
from pathlib import Path
from build_test import *
import pdb

"""
This tests if the cloning function works properly
"""
def test_clone_repo():
    clone_repo("OscarLBergstrom/Group-13", "testfest")
    path = Path('Group-13')
    assert path.exists() == True

"""
This tests if installation of required libraries works properly
"""
def test_installation():
    code = install_requirements(['pip', 'install', '-r'], "Group-13")
    assert code == 0

"""
This tests whether compilation/syntax testing is working properly
"""
def test_syntax():
    code = run_command(['python', '-m', 'compileall'], "Group-13")
    assert code == 0

"""
This tests if the automatic unit testing functionality is working.
"""
def test_testing():
    code = repo_test(['python', '-m', 'pytest'], "Group-13")
    assert code == 2
"""
This tests if the program successfully deletes the repository
"""
def test_delete_repo():
    delete_repo("Group-13")
    path = Path('Group-13')
    assert path.exists() == False

"""
These tests checks if the correct exceptions are thrown when a faulty config file is used.
"""
def test_exception_installation():
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'config_example_noinstall.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)
    
def test_exception_unittest():
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'config_example_notest.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)

def test_exception_buildandsyntax():
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'config_example_nobuildandsyntax.yml'
    with pytest.raises(Exception):
        codes = initialization(repo, branch, dir, config_file)

def test_no_exception():
    repo = 'OscarLBergstrom/Group-13'
    branch = 'testfest'
    dir = 'Group-13'
    config_file = 'config_example.yml'
    codes = initialization(repo, branch, dir, config_file)
    assert codes == (2, 0, 0)