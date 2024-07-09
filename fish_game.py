import pygame
from random import choice
import time 
from math import sin, cos, pi


class Creature():   
    def __init__(self) -> None:
        self.x, self.y = 0, 0

    def is_close(self, other):
        distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        if self.target and distance < 20:
            global game_status
            game_status = 'lose'
        elif not self.target and distance < 100:
            self.target = other

class Fish(Creature):
    def __init__(self) -> None:
        self.x, self.y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        self.left = self.right = self.up = self.down = 0
    
    def move(self):
        self.x += self.right - self.left
        self.y += self.down - self.up

    def show(self):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 10)

class Shark(Creature):
    def __init__(self) -> None:
        self.x, self.y = 20, 20
        self.to_center = True
        self.angle = None
        self.target = None
    
    def move_to(self, destination):        
        dx = (destination.x - self.x)
        dy = (destination.y - self.y)
        vector_size = (dx ** 2 + dy ** 2) ** 0.5
        dx /= vector_size
        dy /= vector_size
        dx *= 2
        dy *= 2
        self.x += dx
        self.y += dy 

    def move(self):
        if self.target:
            dx = (self.target.x - self.x)
            dy = (self.target.y - self.y)
            vector_size = (dx ** 2 + dy ** 2) ** 0.5
        elif self.to_center:
            dx = (SCREEN_WIDTH / 2 - self.x)
            dy = (SCREEN_HEIGHT / 2 - self.y)
            vector_size = (dx ** 2 + dy ** 2) ** 0.5
            if vector_size <= 1:
                self.to_center = False
                self.angle = (choice((20, SCREEN_WIDTH - 20)), choice((20, SCREEN_HEIGHT - 20)))
        else:
            dx = (self.angle[0] - self.x)
            dy = (self.angle[1] - self.y)
            vector_size = (dx ** 2 + dy ** 2) ** 0.5
            if vector_size <= 1:
                self.to_center = True
                self.angle = None
        dx /= vector_size
        dy /= vector_size
        dx *= 2
        dy *= 2
        self.x += dx
        self.y += dy

    def show(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 20)



SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (139, 0, 255)
FPS = 120
clock = pygame.time.Clock()
def restart():
    global game_status, our_fish, our_shark, start
    game_status = 'game'
    our_fish = Fish()
    our_shark = Shark()
    start = time.time()
restart()
font = pygame.font.Font(None, 72)
restart_button_width = 600
win_text = font.render("Поздравляем! Вы умерли.", True, BLACK)
lose_text = font.render("К сожалению, вы умерли.", True, BLACK)
restart_text = font.render("Поробовать ещё раз", True, WHITE)
place = win_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
place_restart_text = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

blind_zone = {
    (0, 0): 3, 
    (-1, -1): 1,
    (0, -1): 3,
    (1, -1): 5,
    (1, 0): 7,
    (1, 1): 9,
    (0, 1): 11,
    (-1, 1): 13,
    (-1, 0): 15
} 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if  SCREEN_WIDTH / 2 - 200 <= x <= SCREEN_WIDTH / 2 + 200 and SCREEN_HEIGHT / 2 + 50 <= y <= SCREEN_HEIGHT / 2 + 150:
                restart()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                our_fish.left = 1
            elif event.key == pygame.K_d:
                our_fish.right = 1
            elif event.key == pygame.K_w:
                our_fish.up = 1
            elif event.key == pygame.K_s:
                our_fish.down = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                our_fish.left = 0
            elif event.key == pygame.K_d:
                our_fish.right = 0
            elif event.key == pygame.K_w:
                our_fish.up = 0
            elif event.key == pygame.K_s:
                our_fish.down = 0

    screen.fill(BLUE)
    if game_status == 'lose':
        screen.blit(lose_text, place)
        pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH / 2 - restart_button_width // 2, SCREEN_HEIGHT / 2 + 50, restart_button_width, 100))
        screen.blit(restart_text, place_restart_text)
    elif time.time() - start > 50:
        game_status = 'win'
        screen.blit(win_text, place)
        pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH / 2 - restart_button_width // 2, SCREEN_HEIGHT / 2 + 50, restart_button_width, 100))
        screen.blit(restart_text, place_restart_text)
    else:
        our_fish.move()
        our_fish.show()
        our_shark.move()
        our_shark.show()
        surface.fill(BLACK)
        pygame.draw.circle(surface, (255, 255, 255, 0), (our_fish.x, our_fish.y), 250)
        
        rl = our_fish.right - our_fish.left
        ud = our_fish.down - our_fish.up
        angle = blind_zone[(rl, ud)] * pi / 8
        blind_zone[(0, 0)] = blind_zone[(rl, ud)]
        pygame.draw.polygon(surface, BLACK,(
            [our_fish.x, our_fish.y], 
            [our_fish.x + 300 * cos(angle), our_fish.y + 300 * sin(angle)], 
            [our_fish.x + 300 * cos(angle + pi / 4), our_fish.y + 300 * sin(angle + pi / 4)]
        ))
        screen.blit(surface, (0, 0))
        our_shark.is_close(our_fish)
      
    pygame.display.update() 
    clock.tick(FPS)



# TODO
# 1) рыбки поменьше, которых можно захавать
# 2) чувство голода (за N секунд до смерти от голода частичная потеря контроля, а затем вообще замирает)
# 3) Мелкие рыбки съедаются касанием
# 4) Нет выхода за пределы экрана
# 5) Кнопка выхода из игры и убрать панель с крестиком сверху
# 6) Кнопка полноэкранного режима
# 7) Алгоритмы движения акулы (случайный, центры-углы, запах крови (локатор))
# 8) мелкие рыбки спавнятся за экраном

# Creatures (Shark, Fish, Hero_fish)
# свой вид движения сводится к рассчёту вектора на текущий такт
# Мелкие рыбки движутся случайно
# Класс кнопок
# Убрать магические числа