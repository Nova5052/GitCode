class VedioPlayer(object):

    # 记录第一个被创建对象的引用
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):  # 分配空间
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if VedioPlayer.init_flag:
            return
        print("初始化")
        VedioPlayer.init_flag = True

player1 = VedioPlayer()
print(player1)

print(" ")

player2 = VedioPlayer()
print(player2)