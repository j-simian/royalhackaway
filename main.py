import pygame
from renderer import * 
from menu import *
from state import *


renderer = Renderer()
state = State()
menu = Menu(state)
renderer.initRenderer()
renderer.renderMenu(menu)
renderer.gameLoop()