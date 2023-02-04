import pygame
from renderer import *
from handle_input import *
from menu import *
from state import *
from funs import *

state = State()
clock = pygame.time.Clock()
renderer = Renderer(state)
menu = Menu(state)
timer = Timer(110, 2.28)
renderer.renderMenu(menu)
entities = initEntities(state)
running = True

controlsMap = {0:{'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down':pygame.K_s, 'attack': pygame.K_q}, 1:{'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down':pygame.K_k, 'attack': pygame.K_u}}
player1controls = controlsMap[state.controls[0]]
player2controls = controlsMap[state.controls[1]]

def tickEntities():
    for (key, entity) in list(entities.items()):
        entity.tick(dt, entities)
        if hasattr(entity, 'dead') and entity.dead:
            del entities[key]
        if hasattr(entity, 'health') and entity.health <= 0:
            state.screen = 2

while running:
    if state.screen == 1:
        dt = clock.tick()
        tickEntities()
        renderer.renderFrame(timer, entities)
        renderer.blitScreen()
        for event in pygame.event.get():
            if state.screen == 1:
                handleMove(entities["p1"], player1controls, event, timer, state, entities["p2"], entities)
                handleMove(entities["p2"], player2controls, event, timer, state, entities["p1"], entities)
            if event.type == pygame.QUIT:
                running = False
    elif state.screen == 2:
        dt = clock.tick(1)
        renderer.renderFrame(timer, entities)
        renderer.renderDeathMenu()
        renderer.blitScreen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

