import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Установка размеров окна
width = 800
height = 600

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Размер блока змейки
block_size = 20

# Установка скорости змейки и начальной скорости
base_speed = 5  # Уменьшение начальной скорости
speed_increment = 1

# Создание окна
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)
large_font = pygame.font.SysFont(None, 50)

# Звуковые эффекты
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
pygame.mixer.music.load("background_music.mp3")

# Функция рисования змейки
def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

# Функция вывода сообщения на экран
def message_to_screen(msg, color, y_displace=0, size="small"):
    if size == "small":
        text_surface = font.render(msg, True, color)
    else:
        text_surface = large_font.render(msg, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width / 2), (height / 2) + y_displace
    gameDisplay.blit(text_surface, text_rect)

# Функция отображения счета
def display_score(score):
    score_text = font.render(f"Score: {score}", True, white)
    gameDisplay.blit(score_text, [0, 0])

# Главное меню
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gameLoop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Welcome to Snake", green, y_displace=-100, size="large")
        message_to_screen("Press C to play or Q to quit. Press P for pause", white, y_displace=0, size="small")
        pygame.display.update()
        clock.tick(15)

# Основная игровая функция
def gameLoop():
    pygame.mixer.music.play(-1)  # Запуск фоновой музыки
    gameExit = False
    gameOver = False
    gameOverSoundPlayed = False  # Флаг для воспроизведения звука конца игры один раз
    lead_x = width / 2
    lead_y = height / 2
    lead_x_change = 0
    lead_y_change = 0
    snakeList = []
    snakeLength = 1
    score = 0  # Инициализация счета
    # Инициализация положения фрукта
    randAppleX = round(random.randrange(0, width - block_size) / float(block_size)) * block_size
    randAppleY = round(random.randrange(0, height - block_size) / float(block_size)) * block_size
    speed = base_speed

    while not gameExit:
        while gameOver:
            if not gameOverSoundPlayed:
                pygame.mixer.music.stop()  # Остановка фоновой музыки
                pygame.mixer.Sound.play(game_over_sound)
                gameOverSoundPlayed = True  # Установка флага, чтобы звук проигрался один раз
            gameDisplay.fill(black)
            message_to_screen("Game over", red, y_displace=-50, size="large")
            message_to_screen("Press C to play again or Q to quit", white, 50, size="small")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_s:
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and lead_x_change == 0:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and lead_x_change == 0:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP and lead_y_change == 0:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and lead_y_change == 0:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        # Проверка на выход змейки за границы окна
        if lead_x >= width or lead_x < 0 or lead_y >= height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])

        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        display_score(score)  # Отображение счета

        pygame.display.update()

        # Проверка съедения фрукта
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, width - block_size) / float(block_size)) * block_size
            randAppleY = round(random.randrange(0, height - block_size) / float(block_size)) * block_size
            snakeLength += 1
            score += 1  # Увеличение счета
            speed += speed_increment
            pygame.mixer.Sound.play(eat_sound)

        clock.tick(speed)

    pygame.quit()
    quit()

# Функция паузы
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Paused", white, y_displace=-50, size="large")
        message_to_screen("Press C to continue or Q to quit", white, 50, size="small")
        pygame.display.update()
        clock.tick(5)

# Запуск главного меню
game_intro()
