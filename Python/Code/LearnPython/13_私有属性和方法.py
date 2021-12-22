class A:

    def __init__(self):
        self.num1 = 100
        self.__num2 = 200

    def __test(self):
        print("%d  %d" % (self.num1, self.__num2))


class B(A):

    pass

# a = A()
# print(a.num1)
# a.test()

b=B()
b.test()