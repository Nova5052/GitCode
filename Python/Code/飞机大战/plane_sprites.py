import random
import time
import pygame

# 屏幕大小 常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 定时发射子弹
HERO_FIRE_EVENT = pygame.USEREVENT + 1


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

    # def __del__(self):
    #     print("敌机挂了 %s" % self.rect)
    def destroy(self):
        self.image = pygame.image.load("./images/enemy1_down3.png")


class Hero(GameSprite):
    """英雄精灵"""

    def __init__(self):
        super().__init__("./images/me1.png", 0)

        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.speed_y = 0

        self.bullet_group = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        self.rect.y += self.speed_y
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.bottom >= SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        for i in (0, 1, 2):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - 20 * i
            bullet.rect.centerx = self.rect.centerx
            self.bullet_group.add(bullet)

    # def __del__(self):
    #     print("英雄牺牲")

    def destroy(self):
        self.image = pygame.image.load("./images/me_destroy_1.png")
        time.sleep(1)
        self.image = pygame.image.load("./images/me_destroy_2.png")
        time.sleep(1)
        self.image = pygame.image.load("./images/me_destroy_3.png")
        time.sleep(1)
        self.image = pygame.image.load("./images/me_destroy_4.png")



class Bullet(GameSprite):
    """子弹精灵"""

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super(Bullet, self).update()
        if self.rect.bottom < 0:
            self.kill()
