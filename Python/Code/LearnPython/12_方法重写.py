class Anmial:

    def eat(self):
        print("吃")

    def run(self):
        print("跑")


class Dog(Anmial):
    def shark(self):
        print("汪汪叫")


class XiaoTianQuan(Dog):
    
    def fly(self):
        print("飞")

    def shark(self):
        print("呜呜呜")
        super().shark()


xiao = XiaoTianQuan()
xiao.shark()
# xiao.fly()
