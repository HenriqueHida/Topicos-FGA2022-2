import pygame, random
from pygame.locals import *
from Pilot import Pilot
from time import sleep
import os

os.system(f"rm ./out/* && rm ./pddlConvertedOut/* && rm ./inputs/*")

# # Helper functions
def on_grid_random(grid):
    x = random.randint(0,(grid/100)-1)
    y = random.randint(0,(grid/100)-1)
    return (x * 100, y * 100)


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Macro definition for snake movement.
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
display_max = 600
pygame.init()
screen = pygame.display.set_mode((display_max, display_max))
pygame.display.set_caption('Snake')

snake = [(100, 100), (200, 100), (300,100)]
snake_skin = pygame.Surface((98,98))
snake_skin.fill((255,165,0)) #White
snake_head = pygame.Surface((100,100))
snake_head.fill((250,10,15))

apple_pos = on_grid_random(display_max)
apple = pygame.Surface((100,100))
apple.fill((124,252,0))
instance = 0

my_direction = RIGHT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0
pilot = Pilot()
game_over = False
instance = pilot.loopLoader(snake, apple_pos)-1
    
          
def readInputsFromFile(count):
    lines = []
    with open('./pddlConvertedOut/cmds'+str(count)+'.txt', 'r') as f:
        last_line = f.readlines()[-1]
    f.close()
    return last_line.split(',')[0:-1]

prevpos = apple_pos

collided = 0
while not game_over:
    for cmd in readInputsFromFile(instance):

        my_direction = int(cmd)
        if(game_over):
            break

        sleep(0.1)

        if collision(snake[0], apple_pos):
            snake.append((0,0))
            fora = False
            while not fora:       
                dentro = False
                apple_pos = on_grid_random(display_max)
                for j in snake:
                    if apple_pos == j:
                        dentro = True
                if not dentro:
                    fora = True
            score = score + 1
            collided = 1
            
            instance = pilot.loopLoader(snake, apple_pos)-1
            print(instance)
            break 
        
        # Check if snake collided with boundaries
        if snake[0][0] == display_max or snake[0][1] == display_max or snake[0][0] < 0 or snake[0][1] < 0:
            game_over = True
            print("Out of bounds")

            break
        
        # Check if the snake has hit itself
        for i in range(1, len(snake) - 1):
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                game_over = True
                break

        if game_over:
            break
        
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i-1][0], snake[i-1][1])
        
        # Actually make the snake move.
        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 100)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 100)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 100, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 100, snake[0][1])
        
        screen.fill((0,0,0))
        screen.blit(apple, apple_pos)
        
        for x in range(0, display_max, 100): # Draw vertical lines
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, display_max))
        for y in range(0, display_max, 100): # Draw vertical lines
            pygame.draw.line(screen, (40, 40, 40), (0, y), (display_max, y))
        
        score_font = font.render('Score: %s' % (score), True, (135,206,235))
        score_rect = score_font.get_rect()
        score_rect.topleft = (570 - 60, 15)
        screen.blit(score_font, score_rect)
        
        screen.blit(snake_head,snake[0])
        pos=1
        for pos in snake:
            screen.blit(snake_skin,pos)

        pygame.display.update()

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 45)
    game_over_screen = game_over_font.render('Game Over', True, (220,20,60))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 80)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()