import math
import os
import sys
from datetime import datetime, timedelta
from collections import Counter

global_var = 100
unused_global = "nobody uses me"

def outer_function(a):
    inner_var = a + 1
    def inner_function(b):
        return b * 2
    return inner_function(a)

def unused_outer(x):
    def unused_inner(y):
        return y - 1
    return unused_inner(x + 1)

class MyClass:
    class_var = "static"
    def __init__(self):
        self.instance_var = 42
        self.unused_instance = "hidden"
    
    def used_method(self):
        return self.instance_var * 2
    
    def unused_method(self):
        return self.unused_instance

def tricky_dynamic():
    return "tricky"
eval("tricky_dynamic()")

def main():
    result = outer_function(5)
    obj = MyClass()
    calc = obj.used_method()
    unused_local = "local trash"
    counter = Counter([1, 2, 3])
    now = datetime.now()
    print(f"Result: {result}, Calc: {calc}, Now: {now}")

if __name__ == "__main__":
    main()