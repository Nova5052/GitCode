class Dog(object):

    def __init__(self, name):
        self.name = name

    def game(self):
        print("%s 一般的玩儿" % self.name)


class XiaoTianQuan(Dog):

    def game(self):
        print("%s 牛逼的玩儿" % self.name)


class Person(object):

    def __init__(self, name):
        self.name = name

    def play_with_dog(self, dog):
        print("%s 和 %s 快乐的玩耍" % (self.name, dog.name))
        dog.game()


wangcai = XiaoTianQuan("哮天犬")
xiaoming = Person("小明")
xiaoming.play_with_dog(wangcai)
