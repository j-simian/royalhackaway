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
initEntities()
renderer.renderMenu(menu)

running = True
while running:
    dt = clock.tick(60)
    for entity in entities.values():
        entity.tick(dt)
    renderer.renderFrame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

