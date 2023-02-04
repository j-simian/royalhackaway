import pygame
from renderer import * 
from game_objects import * 
from menu import *
from state import *
from funs import *

state = State()
renderer = Renderer(state)
menu = Menu(state)
initEntities()
renderer.renderMenu(menu)

running = True
lpressed=False
while running:
    for entity in entities:
        entity.tick()
    renderer.renderFrame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

