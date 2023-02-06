import pytest
from pathlib import Path
from build_test import *
import pdb

def test_clone_repo():
    clone_repo("OscarLBergstrom/Group-13", "testfest")
    path = Path('./Group-13')
    assert path.exists() == True

def test_delete_repo():
    delete_repo("Group-13")
    path = Path('Group-13')
    assert path.exists() == False
