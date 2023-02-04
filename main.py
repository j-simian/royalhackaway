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
while running:
    dt = clock.tick(60)
    for entity in entities.values():
        entity.tick(dt)
    renderer.renderFrame()
    for event in pygame.event.get():
        if state.screen == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    entities["p1"].moving = -1
                if event.key == pygame.K_d:
                    entities["p1"].moving = 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and entities["p1"].moving == -1:
                    entities["p1"].moving = 0

                if event.key == pygame.K_d and entities["p1"].moving == 1:
                    entities["p1"].moving = 0
        if event.type == pygame.QUIT:
            running = False

