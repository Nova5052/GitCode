import pygame


class GameSprite(pygame.sprite.Sprite):
    """飞机大战 游戏精灵"""

    def __init__(self, image_name, speed=1):
        # 调用父类初始化方法
        super(GameSprite, self).__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
