import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20
PADDLE_SPEED = 5
BALL_SPEED = 7
SCORE_LIMIT = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Загрузка изображений
bg_image = pygame.image.load('bg.jpg').convert()
bg_image = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
first_player_img = pygame.image.load('first_player.png').convert_alpha()
first_player_img = pygame.transform.scale(first_player_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
second_player_img = pygame.image.load('second_player.png').convert_alpha()
second_player_img = pygame.transform.scale(second_player_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
ball_img = pygame.image.load('ball.png').convert_alpha()
ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

# Создание объектов
left_paddle = pygame.Rect(0, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WINDOW_WIDTH - PADDLE_WIDTH, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WINDOW_WIDTH//2 - BALL_SIZE//2, WINDOW_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Начальная скорость мяча
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Счет
left_score = 0
right_score = 0

# Шрифт для отображения счета
font = pygame.font.Font(None, 74)

def reset_ball():
    """Сброс мяча в центр экрана"""
    ball.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    global ball_speed_x, ball_speed_y
    ball_speed_x = BALL_SPEED * random.choice((1, -1))
    ball_speed_y = BALL_SPEED * random.choice((1, -1))

# Игровой цикл
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Управление ракетками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < WINDOW_HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < WINDOW_HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок мяча от верхней и нижней границ
    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ball_speed_y *= -1

    # Отскок мяча от ракеток
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Подсчет очков
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WINDOW_WIDTH:
        left_score += 1
        reset_ball()

    # Проверка на победу
    if left_score >= SCORE_LIMIT or right_score >= SCORE_LIMIT:
        winner_text = "Левый игрок победил!" if left_score >= SCORE_LIMIT else "Правый игрок победил!"
        winner_surface = font.render(winner_text, True, WHITE)
        screen.blit(winner_surface, (WINDOW_WIDTH//2 - winner_surface.get_width()//2, WINDOW_HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        left_score = right_score = 0

    # Отрисовка
    screen.blit(bg_image, (0, 0))
    screen.blit(first_player_img, left_paddle)
    screen.blit(second_player_img, right_paddle)
    screen.blit(ball_img, ball)

    # Отображение счета
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WINDOW_WIDTH//4, 20))
    screen.blit(right_text, (3*WINDOW_WIDTH//4, 20))

    pygame.display.flip()
    clock.tick(60)
