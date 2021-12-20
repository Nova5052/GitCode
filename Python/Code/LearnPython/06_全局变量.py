num = 10


def demo1():
    global num
    num = 99
    print(id(num))


def demo2():
    print(id(num))


print(id(num))
demo1()
demo2()
