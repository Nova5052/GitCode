class Tools(object):
    # 类属性
    totals = 0

    # 类方法
    @classmethod
    def show_counts(cls):
        print("类方法 工具数量是: %d" % cls.totals)

    def __init__(self, name):
        self.name = name
        Tools.totals = Tools.totals + 1


tool1=Tools("斧头")
tool2=Tools("锤子")

print(Tools.totals)
print(tool2.totals)

Tools.show_counts()