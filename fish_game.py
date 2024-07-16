import pygame
from random import choice, randint, random
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
        pygame.draw.circle(screen, SMOKY_WHITE, (self.x, self.y), 20)

class Small_fish(Creature):
    def __init__(self) -> None:
        self.x = randint(0, SCREEN_WIDTH)
        self.y = randint(0, SCREEN_HEIGHT)
        # self.x = SCREEN_WIDTH / 2
        # self.y = SCREEN_HEIGHT / 2
        self.time = time.time() - 10

    def show(self):
        pygame.draw.circle(screen, DOVE_BLUE, (self.x, self.y), 5)

    def move(self):
        if self.x < SCREEN_WIDTH//2 - 500 or self.y < SCREEN_HEIGHT//2 - 500 or self.x > SCREEN_WIDTH//2 + 500 or self.y > SCREEN_HEIGHT // 2 + 500:
            # self.dx = (SCREEN_WIDTH / 2 - self.x)
            # self.dy = (SCREEN_HEIGHT / 2 - self.y)
            # vector_size = (self.dx ** 2 + self.dy ** 2) ** 0.5
            # self.dx /= vector_size
            # self.dy /= vector_size
            # self.dx *= 2
            # self.dy *= 2
            # self.time = time.time()
            self.time = time.time() - 10
        if time.time() - self.time > 5:
            angle = random() * 2 * pi
            self.dx = cos(angle) * 2
            self.dy = sin(angle) * 2 
            self.time = time.time()
        self.x += self.dx
        self.y += self.dy


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BURGUNDY = (155, 45, 48)
BLUE = (0, 0, 255)
ULTRAMARINE = (18, 10, 143)
PURPLE = (139, 0, 255)
DOVE_BLUE = (96, 110, 140)
CORAL = (255, 127, 80)
BLUE_DEATH = (18, 47, 170)
SMOKY_WHITE = (245, 245, 245)
FPS = 120
clock = pygame.time.Clock()
def restart():
    global game_status, our_fish, our_shark, start, fishes
    game_status = 'game'
    our_fish = Fish()
    our_shark = Shark()
    start = time.time()
    fishes = [Small_fish() for _ in range(100)]
restart()
font = pygame.font.Font(None, 72)
restart_button_width = 600
win_text = font.render("Поздравляем! Вы умерли.", True, WHITE)
lose_text = font.render("К сожалению, вы умерли.", True, WHITE)
restart_text = font.render("Попробовать ещё раз", True, WHITE)
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
    keys = pygame.key.get_pressed()
    our_fish.down = int(keys[pygame.K_s])
    our_fish.up = int(keys[pygame.K_w])
    our_fish.right = int(keys[pygame.K_d])
    our_fish.left = int(keys[pygame.K_a])
   
    if game_status == 'lose':
        screen.fill(BLUE_DEATH)   
        screen.blit(lose_text, place)
        pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH / 2 - restart_button_width // 2, SCREEN_HEIGHT / 2 + 50, restart_button_width, 100))
        screen.blit(restart_text, place_restart_text)
    elif time.time() - start > 50:
        game_status = 'win'        
        screen.fill(BLUE_DEATH)   
        screen.blit(win_text, place)
        pygame.draw.rect(screen, PURPLE, (SCREEN_WIDTH / 2 - restart_button_width // 2, SCREEN_HEIGHT / 2 + 50, restart_button_width, 100))
        screen.blit(restart_text, place_restart_text)
    else:
        screen.fill(ULTRAMARINE)
        pygame.draw.rect(screen, CORAL, (SCREEN_WIDTH / 2 - 0.3 * SCREEN_WIDTH, SCREEN_HEIGHT / 2 + 0.2 * SCREEN_HEIGHT, 200, 200))
        our_fish.move()
        our_fish.show()
        our_shark.move()
        our_shark.show()
        for fish in fishes:
            fish.move()
            fish.show()
        surface.fill(ULTRAMARINE)
        pygame.draw.circle(surface, (255, 255, 255, 0), (our_fish.x, our_fish.y), 250)
        
        rl = our_fish.right - our_fish.left
        ud = our_fish.down - our_fish.up
        angle = blind_zone[(rl, ud)] * pi / 8
        blind_zone[(0, 0)] = blind_zone[(rl, ud)]
        pygame.draw.polygon(surface, ULTRAMARINE,(
            [our_fish.x, our_fish.y], 
            [our_fish.x + 300 * cos(angle), our_fish.y + 300 * sin(angle)], 
            [our_fish.x + 300 * cos(angle + pi / 4), our_fish.y + 300 * sin(angle + pi / 4)]
        ))
        screen.blit(surface, (0, 0))
        our_fish.move()
        our_fish.show()
        our_shark.is_close(our_fish)
      
    pygame.display.update() 
    clock.tick(FPS)


# TODO
# * почему рыба стала быстрее акулы
# * Мелкие рыбки съедаются касанием
# * генерация позиции корала не у центра и не у края
# * мелкие рыбы выплывая за экран возвращаются к кораловой группе
# * скорость у рыбы одинаковая во всех восьми направлениях
# * чувство голода (за N секунд до смерти от голода частичная потеря контроля, а затем вообще замирает)
# * Нет выхода за пределы экрана
# * Кнопка выхода из игры и убрать панель с крестиком сверху
# * Кнопка полноэкранного режима
# * Алгоритмы движения акулы (случайный, центры-углы, запах крови (локатор))
# * мелкие рыбки спавнятся за экраном

# Creatures (Shark, Fish, Hero_fish)
# свой вид движения сводится к рассчёту вектора на текущий такт
# Мелкие рыбки движутся случайно
# Класс кнопок
# Убрать магические числа
