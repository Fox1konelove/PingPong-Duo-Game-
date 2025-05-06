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
BALL_SPEED = 7  # Постоянная скорость мяча
SCORE_LIMIT = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

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

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.color = GRAY
        self.hover_color = LIGHT_GRAY
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            return True
        return False

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2 - BALL_SIZE // 2,
                               WINDOW_HEIGHT // 2 - BALL_SIZE // 2,
                               BALL_SIZE, BALL_SIZE)
        self.reset()
    
    def reset(self):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])
    
    def update(self):
        # Обновление позиции мяча
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Отскок от верхней и нижней границы
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.speed_y *= -1

        # Возвращаем информацию о голе
        if self.rect.left <= 0:
            self.reset()
            return 'right'  # Гол правому игроку
        elif self.rect.right >= WINDOW_WIDTH:
            self.reset()
            return 'left'   # Гол левому игроку
        return None
ball_img = pygame.image.load('ball.png').convert_alpha()
ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

# Создание объектов
left_paddle = pygame.Rect(0, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WINDOW_WIDTH - PADDLE_WIDTH, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = Ball()

# Счет
left_score = 0
right_score = 0

# Шрифт для отображения счета
font = pygame.font.Font(None, 74)

# Создание кнопок
start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50, 200, 50, "Начать")
exit_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20, 200, 50, "Выйти")
play_again_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20, 200, 50, "Ещё раз")

# Глобальные переменные
global winner_text
winner_text = ""

# Состояния игры
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
game_state = GAME_STATE_MENU

# Игровой цикл
clock = pygame.time.Clock()

last_time = pygame.time.get_ticks()
while True:
    current_time = pygame.time.get_ticks()
    dt = current_time - last_time  # Delta time в миллисекундах
    last_time = current_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_state == GAME_STATE_MENU:
            if start_button.handle_event(event):
                game_state = GAME_STATE_PLAYING
                ball = Ball()
                left_score = 0
                right_score = 0
            elif exit_button.handle_event(event):
                pygame.quit()
                exit()
        
        elif game_state == GAME_STATE_GAME_OVER:
            if play_again_button.handle_event(event):
                game_state = GAME_STATE_PLAYING
                ball = Ball()
                left_score = 0
                right_score = 0

    # Очистка экрана
    screen.blit(bg_image, (0, 0))

    if game_state == GAME_STATE_MENU:
        # Отрисовка кнопок меню
        start_button.draw(screen)
        exit_button.draw(screen)
    
    elif game_state == GAME_STATE_GAME_OVER:
        # Отображение текста победителя
        winner_surface = font.render(winner_text, True, WHITE)
        screen.blit(winner_surface, (WINDOW_WIDTH//2 - winner_surface.get_width()//2, WINDOW_HEIGHT//2 - 100))
        
        # Отрисовка кнопки "Ещё раз"
        play_again_button.draw(screen)
    
    elif game_state == GAME_STATE_PLAYING:
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

        # Обновление мяча
        goal = ball.update()
        if goal == 'left':
            left_score += 1
        elif goal == 'right':
            right_score += 1

        # Отскок мяча от ракеток
        if ball.rect.colliderect(left_paddle) or ball.rect.colliderect(right_paddle):
            ball.speed_x *= -1

        # Отрисовка игровых объектов
        screen.blit(first_player_img, left_paddle)
        screen.blit(second_player_img, right_paddle)
        screen.blit(ball_img, ball.rect)

        # Отображение счета
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WINDOW_WIDTH//4, 20))
        screen.blit(right_text, (3*WINDOW_WIDTH//4, 20))

        # Проверка на победу
        if left_score >= SCORE_LIMIT or right_score >= SCORE_LIMIT:
            game_state = GAME_STATE_GAME_OVER
            winner_text = "Левый игрок победил!" if left_score >= SCORE_LIMIT else "Правый игрок победил!"

    pygame.display.flip()
    clock.tick(60)
