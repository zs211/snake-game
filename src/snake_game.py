# src/snake_game.py
# 导入必要的库
import pygame
import random
import sys

# ====================== 初始化配置 ======================
# 初始化Pygame所有模块
pygame.init()

# 游戏窗口大小（像素）
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# 网格大小（蛇和食物的基本单位）
GRID_SIZE = 20
# 计算网格数量（方便后续定位）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义（RGB格式）
BLACK = (0, 0, 0)       # 背景色
WHITE = (255, 255, 255) # 文字色
RED = (255, 0, 0)       # 食物色
GREEN = (0, 255, 0)     # 蛇的颜色
BLUE = (0, 0, 255)      # 备用色

# 方向常量（x轴，y轴）
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# 设置窗口标题
pygame.display.set_caption("贪吃蛇游戏 - Python版")

# 时钟（控制游戏帧率）
clock = pygame.time.Clock()
# 字体（用于显示分数和游戏结束提示）
font = pygame.font.SysFont(None, 40)

# ====================== 游戏绘制函数 ======================
def draw_snake(snake_body):
    """绘制蛇的身体"""
    for segment in snake_body:
        # 绘制每个蛇段（-1是为了留缝隙，更美观）
        pygame.draw.rect(
            screen, 
            GREEN, 
            (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
        )

def draw_food(food_pos):
    """绘制食物"""
    pygame.draw.rect(
        screen, 
        RED, 
        (food_pos[0]*GRID_SIZE, food_pos[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1)
    )

def draw_score(score):
    """绘制当前分数"""
    score_text = font.render(f"分数: {score}", True, WHITE)
    # 将文字绘制到窗口左上角（10,10位置）
    screen.blit(score_text, (10, 10))

# ====================== 游戏主逻辑 ======================
def game_loop():
    """游戏主循环"""
    # 初始化蛇的位置（窗口正中间）
    snake_body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    # 初始方向（向右）
    direction = RIGHT
    # 初始分数
    score = 0

    # 生成初始食物（随机位置，避免和蛇重叠）
    def generate_food():
        """生成食物的辅助函数"""
        food_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        # 如果食物位置在蛇身上，重新生成
        while food_pos in snake_body:
            food_pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        return food_pos

    food_pos = generate_food()

    # 游戏运行状态
    running = True
    game_over = False

    # 主循环
    while running:
        # ===== 游戏结束处理 =====
        while game_over:
            # 填充黑色背景
            screen.fill(BLACK)
            # 绘制游戏结束提示
            game_over_text = font.render(
                f"游戏结束！分数: {score} | 按Q退出 | 按C重新开始", 
                True, 
                RED
            )
            # 文字居中显示
            screen.blit(game_over_text, (WINDOW_WIDTH//6, WINDOW_HEIGHT//2))
            # 更新窗口显示
            pygame.display.update()

            # 处理游戏结束后的按键
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q键退出
                        running = False
                        game_over = False
                    if event.key == pygame.K_c:  # C键重新开始
                        game_loop()
                if event.type == pygame.QUIT:  # 点击关闭按钮退出
                    running = False
                    game_over = False

        # ===== 游戏运行中处理 =====
        # 处理用户输入（按键）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击关闭按钮
                running = False
            # 方向键控制（避免反向移动，比如向上时不能直接向下）
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        # 移动蛇：计算新头部位置
        head_x, head_y = snake_body[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # 碰撞检测：边界碰撞（超出窗口则游戏结束）
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_over = True

        # 碰撞检测：自身碰撞（咬到自己则游戏结束）
        if new_head in snake_body:
            game_over = True

        # 添加新头部到蛇身
        snake_body.insert(0, new_head)

        # 吃到食物的判断
        if new_head == food_pos:
            score += 10  # 分数+10
            food_pos = generate_food()  # 重新生成食物
        else:
            # 没吃到食物则删除尾部（蛇移动的核心逻辑）
            snake_body.pop()

        # ===== 绘制游戏界面 =====
        screen.fill(BLACK)  # 清空背景
        draw_snake(snake_body)  # 绘制蛇
        draw_food(food_pos)    # 绘制食物
        draw_score(score)      # 绘制分数
        pygame.display.update() # 更新窗口

        # 控制游戏帧率（数值越大，蛇移动越快）
        clock.tick(10)

    # 退出游戏
    pygame.quit()
    sys.exit()

# ====================== 启动游戏 ======================
if __name__ == "__main__":
    game_loop()