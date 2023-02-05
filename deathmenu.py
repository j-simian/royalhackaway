import pygame
import pygame_menu


class DeathMenu():
    def __init__(self, state) -> None:
        self.state = state

    def start_game(self):
        self.state.screen = 0
        self.menu.disable()

    def render(self, screen):

        self.dietheme = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.menubg = pygame_menu.baseimage.BaseImage(
            image_path="assets/imgs/menubg.png",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
        )
        self.dietheme.background_color = self.menubg

        self.dietheme.title_background_color=(240, 0, 110)
        self.dietheme.widget_selection_effect=pygame_menu.widgets.RightArrowSelection()
        self.dietheme.widget_font=pygame_menu.font.FONT_NEVIS
        self.dietheme.title_font=pygame_menu.font.FONT_8BIT
        self.dietheme.title_font_color=(255,255,255)
        self.dietheme.widget_font_color=(179,0,83)
        self.dietheme.widget_font_size=50
        self.dietheme.title_font_size=70
        self.dietheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        self.dietheme.widget_selection_color=(255,92,127)

        self.menu = pygame_menu.Menu('Game Over', self.state.WIDTH, self.state.HEIGHT,
                    theme=self.dietheme, mouse_motion_selection=True)

        self.menu.add.button('Play Again', self.start_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()
        self.menu.mainloop(screen)
