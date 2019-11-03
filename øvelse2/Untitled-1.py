print("hello world")

def my_function():
  print("Hello from a function")

def funcmake_function(name, n : int):
    funcs = []

    for i in range(n):
        l = lambda j = i: print("hello i am " + name + str(j))
        funcs.append(l)

    return funcs


my_function()

asd = {1,2,3,4}

for a in asd:
    print(a)

myfuncs = funcmake_function("asd", 10)

for f in myfuncs:
    f()