import pytest
from server_connect import *

def test_connection():
    ssh_tunnel, http_tunnel = connect_kth()
    assert ssh_tunnel != None and http_tunnel != None
