import pygame
import pygame_menu

pygame.init()


class Menu():
    def __init__(self, state) -> None:
        self.state = state
    def set_controls(self, player, controls):
        self.state.controls[player] = controls
        # 0: wasd, 1: ijkl

    def start_the_game(self):
    # Do the job here !
        if self.state.controls[0] != self.state.controls[1]:
            self.state.screen = 1
            pygame.mixer.init()
            pygame.mixer.music.load("assets/music/metronome110.mp3")
            pygame.mixer.music.set_volume(self.state.VOLUME)
            pygame.mixer.music.play()
            self.menu.disable()
    def render(self, screen):

        self.nyatheme = pygame_menu.themes.THEME_SOLARIZED.copy()

        self.menubg = pygame_menu.baseimage.BaseImage(
            image_path="assets/catbg.jpg",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
        )
        self.nyatheme.background_color = self.menubg
        self.nyatheme.title_background_color=(240, 0, 110)
        self.nyatheme.widget_selection_effect=pygame_menu.widgets.RightArrowSelection()
        self.nyatheme.widget_font=pygame_menu.font.FONT_MUNRO
        self.nyatheme.title_font=pygame_menu.font.FONT_MUNRO
        self.nyatheme.title_font_color=(255,255,255)

        self.menu = pygame_menu.Menu('Nya Nya Revolution', self.state.WIDTH, self.state.HEIGHT,
                       theme=self.nyatheme, mouse_motion_selection=True, columns = 2, rows = 3)

        self.menu.add.text_input('Player1 Name :', default='Catgirl 1')
        self.menu.add.selector('Player 1 Controls:', [["wasd",0], ["ijkl",1]], onchange=(lambda _, y: self.set_controls(0, y)))
        self.menu.add.button('Play', self.start_the_game)
        self.menu.add.text_input('Player2 Name :', default='Catgirl 2')
        self.menu.add.selector('Player 2 Controls:', [["ijkl",1], ["wasd",0]], onchange=(lambda _, y: self.set_controls(1, y)))
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(screen)