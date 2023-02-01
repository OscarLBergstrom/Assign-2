import pytest

def sample_test(x):
    return x + 1

def test_sample():
    assert sample_test(3) == 4
