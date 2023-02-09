def multiplication(x,y):
    return x*y

def factorial(num):
    temp = num-1
    while temp > 1:
        num *= temp
        temp -= 1
    return num

def addition(x,y):
    return x+y

def subtraction(x,y):
    return x-y

def max(x,y):
    if x>y:
        return x
    return y