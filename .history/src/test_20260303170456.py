# src/test.py
import pygame

# 初始化Pygame
pygame.init()
# 创建一个空白窗口
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("测试窗口")

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 填充白色背景
    screen.fill((255, 255, 255))
    # 更新窗口
    pygame.display.update()

# 退出Pygame
pygame.quit()