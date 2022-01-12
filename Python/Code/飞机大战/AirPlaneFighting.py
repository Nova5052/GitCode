import pygame
from plane_sprites import *

# 开始前必须调用
pygame.init()
# 创建游戏主窗口
screen = pygame.display.set_mode((480, 700))

# 绘制背景图像
bg = pygame.image.load("./images/background.png")
screen.blit(bg, (0, 0))

# 绘制英雄飞机
hero = pygame.image.load("./images/me1.png")
screen.blit(hero, (200, 500))

# 创建时钟对象
clock = pygame.time.Clock()

hero_rect = pygame.Rect(200, 500, 102, 126)

# 创建敌机精灵
enemy = GameSprite("./images/enemy1.png")
enemy1 = GameSprite("./images/enemy1.png",3)
enemy_group = pygame.sprite.Group(enemy,enemy1)

while True:
    clock.tick(60)  # 设置帧率
    # 监听用户事件
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    hero_rect.y -= 1
    screen.blit(bg, (0, 0))  # 重新绘制背景图像，不然会有飞机的残影
    screen.blit(hero, hero_rect)

    enemy_group.update()
    enemy_group.draw(screen)

    pygame.display.update()

# 退出前必须调用
pygame.quit()
