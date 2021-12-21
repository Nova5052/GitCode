class Cat:

    def __init__(self, new_name):
        self.name = new_name
        print('初始化调用 猫的名字 %s' % self.name)

    def eat(self):
        print('%s 吃东西' % self.name)

    def __del__(self):
        print('%s 走了' % self.name)

    def __str__(self):
        return "我是小猫[%s]" % self.name


cat_tom = Cat("tom")
cat_tom.eat()

print(cat_tom)
# del cat_tom
# print('*'*50)
