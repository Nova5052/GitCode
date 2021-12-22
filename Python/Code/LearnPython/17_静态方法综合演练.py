class Game(object):

    # 历史最高分
    top_score=0

    def __init__(self,name):
        self.name=name

    @staticmethod
    def show_help():
        print("请按说明开始有戏")

    @classmethod
    def show_score(cls):
        print("历史最高分是: %d" % cls.top_score)

    def start_game(self):
        print("%s 开始玩儿有戏了" % self.name)


Game.show_help()
Game.show_score()