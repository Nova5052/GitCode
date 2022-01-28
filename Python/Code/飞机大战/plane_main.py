import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")
        # 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 创建游戏时钟 帧率
        self.clock = pygame.time.Clock()
        # 创建精灵和精灵组
        self.__create_sprites()
        # 设置定时器事件 创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def StartGame(self):
        while True:
            # 1.设置帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        """事件监听"""
        for event in pygame.event.get():
            # 退出游戏事件
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 控制英雄移动
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_y = -2
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_y = 2
        else:
            self.hero.speed = 0
            self.hero.speed_y = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        # pygame.sprite.groupcollide(self.hero_group, self.enemy_group, True, True)

        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            pygame.time.set_timer(HERO_FIRE_EVENT, 0)
            self.hero.image = pygame.image.load("./images/me_destroy_1.png")
            self.hero_group.update()
            self.hero_group.draw(self.screen)
            time.sleep(1)
            self.hero.image = pygame.image.load("./images/me_destroy_2.png")
            self.hero_group.update()
            self.hero_group.draw(self.screen)
            time.sleep(1)
            self.hero.image = pygame.image.load("./images/me_destroy_3.png")
            self.hero_group.update()
            self.hero_group.draw(self.screen)
            time.sleep(1)
            self.hero.image = pygame.image.load("./images/me_destroy_4.png")
            self.hero_group.update()
            self.hero_group.draw(self.screen)
            # self.hero.destroy()
            # self.hero.kill()
            # PlaneGame.__game_over()

    def __update_sprites(self):
        # 更新背景
        self.back_group.update()
        self.back_group.draw(self.screen)
        # 更新敌机
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        # 更新英雄
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 子弹精灵组
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.StartGame()
