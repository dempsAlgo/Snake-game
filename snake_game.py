import pygame
import random
from math import pi
from time import sleep
pygame.init()

class Snake_head():
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.z = 'x'
        self.speed_x = 3
        self.speed_y = 0
    def draw(self):
        pygame.draw.rect(window, (0, 255, 0), [self.x-2, self.y-2, 16, 16], 0)
    def direction(self, z):
        self.z = z
        if self.z == '-y':
            self.speed_y = -3
            self.speed_x = 0
        elif self.z == '-x':
            self.speed_y = 0
            self.speed_x = -3
        elif self.z == 'x':
            self.speed_x = 3
            self.speed_y = 0
        else:
            self.speed_x = 0
            self.speed_y = 3
    def move(self):
        self.x = (self.x + self.speed_x) % WIDTH
        self.y = (self.y + self.speed_y) % HEIGHT
        self.draw()
    def add_block(self):
        block = Block(self.x, self.y)
        
class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        blocks_list.append(self)
    def draw(self):
        pygame.draw.rect(window, (0, 255, 0), [self.x, self.y, 12, 12], 0)

class Level():
    def __init__(self, level, walls = []):
        self.level = level
        self.walls = walls
    def collision(self, x, y):
        for line in self.walls:
            if x>line[0]-6 and x<line[2]+6 and y>line[1]-6 and y<line[3]+6:
                return True
        return False
    def draw(self):
        for line in self.walls:
            pygame.draw.rect(window, (255, 255, 0), [line[0], line[1], line[2]-line[0], line[3]-line[1]], 0)
        
HEIGHT = 600
WIDTH = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
ok = True
start_screen = True
SCORE_FONT = pygame.font.SysFont("Comic Sans MS", 30)
clock = pygame.time.Clock()
levels = [Level(1), Level(2, [(0, 0, WIDTH, 12), (0, HEIGHT-12, WIDTH, HEIGHT), (0, 0, 12, HEIGHT), (WIDTH-12, 0, WIDTH, HEIGHT)])]

levels.append(Level(3, [(0, 0, 276, 12), (0, 0, 12, 180), (WIDTH-276, 0, WIDTH, 12), (WIDTH-12, 0, WIDTH, 180), (WIDTH/2 - 240, HEIGHT/2 - 60, WIDTH/2 + 240, HEIGHT/2 - 48), (0, HEIGHT-12, 276, HEIGHT), (0, HEIGHT-180, 12, HEIGHT), (WIDTH-276, HEIGHT-12, WIDTH, HEIGHT), (WIDTH-12, HEIGHT-180, WIDTH, HEIGHT), (WIDTH/2 - 240, HEIGHT/2 + 48, WIDTH/2 + 240, HEIGHT/2 + 60)]))

levels.append(Level(4, [(280, 0, 292, 240), (WIDTH - 292, HEIGHT - 240, WIDTH - 280, HEIGHT), (0, 360, 360, 372), (WIDTH - 360, HEIGHT - 360, WIDTH, HEIGHT - 372)]))

levels.append(Level(5, [(500, 0, 512, 240), (WIDTH - 512, HEIGHT-240, WIDTH-500, HEIGHT), (0, 240, 512, 252), (WIDTH - 512, HEIGHT-252, WIDTH, HEIGHT-240), (WIDTH - 200, 240, WIDTH, 252), (0, HEIGHT-252, 200, HEIGHT-240)]))
l = 1
while ok:
    #Start screen
    while start_screen:
        try:
            score_surface = SCORE_FONT.render(str(score), False, (255, 255, 255))
            window.blit(score_surface, (WIDTH - 100, 10))
        except:
            pass
        pygame.display.flip()
        window.fill((0, 0, 0))
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
                ok =  False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                l = 1
                start_screen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                l = 2
                start_screen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                l = 3
                start_screen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                l = 4
                start_screen = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                l = 5
                start_screen = False
            if start_screen == False:
                blocks_list = []
                for i in range(15):
                    a = Block(WIDTH // 2, HEIGHT // 2)
                a = Snake_head()
                food_x = random.randint(10, WIDTH-10)
                food_y = random.randint(10, HEIGHT-10)
                while levels[l-1].collision(food_x, food_y):
                    food_x = random.randint(10, WIDTH-10)
                    food_y = random.randint(10, HEIGHT-10)
                counter = 8
                tmp_direction = 'x'
                score = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ok =  False       
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if a.z != 'y':
                tmp_direction = '-y'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if a.z != 'x':
                tmp_direction = '-x'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if a.z != '-x':
                tmp_direction = 'x'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if a.z != '-y':
                tmp_direction = 'y'
    if counter == 0:
        counter = 6
        a.direction(tmp_direction)
    counter -= 1
    a.add_block()
    del blocks_list[0]
    pygame.draw.circle(window, (255, 0, 0), [food_x, food_y], 7)
    if a.x - food_x < 3 and a.x - food_x > -20 and a.y - food_y < 3 and a.y - food_y > -20:
        food_x = random.randint(10, WIDTH-10)
        food_y = random.randint(10, HEIGHT-10)
        while levels[l-1].collision(food_x, food_y):
            food_x = random.randint(10, WIDTH-10)
            food_y = random.randint(10, HEIGHT-10)
        score += 1
        for i in range(5):
            b = Block(a.x, a.y)
    levels[l-1].draw()
    a.move()
    for i in range(len(blocks_list)-15, len(blocks_list)):
        blocks_list[i].draw()
    for i in range(len(blocks_list)-15):
        blocks_list[i].draw()
        if a.x - blocks_list[i].x < 5 and a.x - blocks_list[i].x > -5 and a.y - blocks_list[i].y < 5 and a.y - blocks_list[i].y > -5:
            start_screen = True
    if levels[l-1].collision(a.x+8, a.y+8):
        start_screen = True
        
    score_surface = SCORE_FONT.render(str(score), False, (255, 255, 255))
    window.blit(score_surface, (WIDTH - 100, 10))
    pygame.display.flip()
    window.fill((0, 0, 0))
    clock.tick(40)
pygame.quit()