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
timer = Timer(110, 0)
renderer.renderMenu(menu)
initEntities(state)

running = True
lpressed=False

controlsMap = {0:{'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down':pygame.K_s}, 1:{'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down':pygame.K_k}}
player1controls = controlsMap[state.controls[0]]
player2controls = controlsMap[state.controls[1]]


while running:
    dt = clock.tick()
    for entity in entities.values():
        entity.tick(dt)
    renderer.renderFrame(timer)
    for event in pygame.event.get():
            
        if state.screen == 1:
            handleMove(entities["p1"], player1controls, event, timer, state.lastdash)
            handleMove(entities["p2"], player2controls, event, timer, state.lastdash)
        if event.type == pygame.QUIT:
            running = False
