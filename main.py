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
renderer.gameLoop()
