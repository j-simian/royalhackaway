import pygame
import pygame_menu


class Menu():
    def __init__(self, state) -> None:
        self.state = state
    def set_controls(self, player, controls):
        self.state.controls[player] = controls
        # 0: wasd, 1: ijkl
    def set_name(self, player, name):
        self.state.names[player] = name

    def start_the_game(self):
    # Do the job here !
        if self.state.controls[0] != self.state.controls[1]:
            self.state.screen = 1
            pygame.mixer.init()
            pygame.mixer.music.load("assets/music/STELLAR.mp3")
            pygame.mixer.music.set_volume(self.state.VOLUME)
            pygame.mixer.music.play()
            self.menu.disable()
    def setp1name(self, val):
        self.state.player1name = val
    def setp2name(self,val):
        self.state.player2name = val
    def render(self, screen):

        self.nyatheme = pygame_menu.themes.THEME_SOLARIZED.copy()

        self.menubg = pygame_menu.baseimage.BaseImage(
            image_path="assets/imgs/menu2bg.png",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
        )
        self.nyatheme.background_color = self.menubg
        self.nyatheme.title_background_color=(240, 0, 110)
        self.nyatheme.widget_selection_effect=pygame_menu.widgets.RightArrowSelection()
        self.nyatheme.widget_font=pygame_menu.font.FONT_NEVIS
        self.nyatheme.title_font=pygame_menu.font.FONT_8BIT
        self.nyatheme.title_font_color=(255,255,255)
        self.nyatheme.widget_font_color=(179,0,83)
        self.nyatheme.widget_font_size=50
        self.nyatheme.title_font_size=70
        self.nyatheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        self.nyatheme.widget_selection_color=(255,92,127)



        self.controlsmenu = pygame_menu.Menu('Controls', self.state.WIDTH, self.state.HEIGHT,
                    theme=self.nyatheme, mouse_motion_selection=True)
        self.controlsmenu.add.label("P1 Controls")
        self.controlsmenu.add.selector('', [["wasd",0], ["ijkl",1]], onchange=(lambda _, y: self.set_controls(0, y)))
        self.controlsmenu.add.label("P2 Controls")
        self.controlsmenu.add.selector('', [["ijkl",1], ["wasd",0]], onchange=(lambda _, y: self.set_controls(1, y)))
        self.controlsmenu.add.button('Return', pygame_menu.events.BACK)


        self.menu = pygame_menu.Menu('Nya Nya Revolution', self.state.WIDTH, self.state.HEIGHT,
                    theme=self.nyatheme, mouse_motion_selection=True)
        self.menu.add.label("Fight to the beat!")
        self.menu.add.text_input('P1 Name: ', default='Caterina', onchange=(lambda y: self.set_name(0, y)))
        self.menu.add.text_input('P2 Name: ', default='Nyatalie', onchange=(lambda y: self.set_name(1, y)))


        self.playbuttonimage = pygame_menu.BaseImage(image_path="assets/imgs/playbtn.png",) #play button
        self.menu.add.banner(self.playbuttonimage, self.start_the_game)
        self.menu.add.button('Controls', self.controlsmenu)
# quit: pygame_menu.events.EXIT


        self.menu.mainloop(screen)
