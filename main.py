import pygame
from renderer import * 
from menu import *

renderer = Renderer()
menu = Menu()
renderer.initRenderer()
renderer.renderMenu(menu)
renderer.gameLoop()