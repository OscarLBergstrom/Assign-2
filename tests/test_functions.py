from functions import *
import pytest

def test_addition():

    assert addition(2,4) == 6

def test_factorial():
    assert factorial(5) == 120

def test_multiplication():
    assert multiplication(10,10) == 100

def test_multiplication_negative():
    assert not multiplication(2,2) == 6

def test_max():
    assert max(100,4) == 100

def test_max_negative():
    assert not max(100,4) == 4

def test_subtraction():
    assert subtraction (3,1) == 2


