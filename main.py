import pygame
from renderer import * 
from menu import *
from state import *
from funs import *

renderer = Renderer()
state = State()
menu = Menu(state)
renderer.initRenderer()
renderer.renderMenu(menu)
renderer.gameLoop()
