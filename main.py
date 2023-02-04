import pygame
from renderer import *
from game_objects import *
from menu import *
from state import *
from funs import *

state = State()
clock = pygame.time.Clock()
renderer = Renderer(state)
menu = Menu(state)
renderer.renderMenu(menu)
initEntities()

running = True
lpressed=False

controlsMap = {0:{'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down':pygame.K_s}, 1:{'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down':pygame.K_k}}
player1controls = controlsMap[state.controls[0]]
player2controls = controlsMap[state.controls[1]]


while running:
    dt = clock.tick()
    for entity in entities.values():
        entity.tick(dt)
    renderer.renderFrame()
    for event in pygame.event.get():
        if state.screen == 1:
            t=onRhythm(pygame.mixer.music.get_pos()/1000, 0, 110)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    entities["p1"].moving = -1
                if event.key == pygame.K_d:
                    entities["p1"].moving = 1
                if event.key == pygame.K_w:
                    entities["p1"].jumping = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and entities["p1"].moving == -1:
                    entities["p1"].moving = 0

                if event.key == pygame.K_d and entities["p1"].moving == 1:
                    entities["p1"].moving = 0
        if event.type == pygame.QUIT:
            running = False
