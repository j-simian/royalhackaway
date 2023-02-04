import pygame
from renderer import * 
from menu import *
from state import *
from funs import *

state = State()
renderer = Renderer(state)
menu = Menu(state)
renderer.renderMenu(menu)
renderer.gameLoop()
