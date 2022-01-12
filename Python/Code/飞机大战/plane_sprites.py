import random
import pygame

# 屏幕大小 常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT


class GameSprite(pygame.sprite.Sprite):
    """飞机大战 游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类初始化方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class BackGround(GameSprite):
    """游戏背景 精灵"""

    def __init__(self, is_replace=False):
        super().__init__("./images/background.png")
        if is_replace:
            self.rect.y = self.rect.height

    def update(self):
        # 调用父类方法
        super().update()

        # 背景超出屏幕，则重新将背景放在屏幕正上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 4)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # 从精灵组移除
            self.kill()

    def __del__(self):
        print("敌机挂了 %s" % self.rect)
