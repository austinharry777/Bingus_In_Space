import pygame, constants as c, random
from base_state import Base_State
from fade import Cutscene_Fadein, Cutscene_Fadeout
from level1 import Level1
pygame.init()

music1 = pygame.mixer.Sound('sounds/bingus_title1.wav')
music2 = pygame.mixer.Sound('sounds/bingus_title2.wav')
music3 = pygame.mixer.Sound('sounds/bingus_title3.wav')
music4 = pygame.mixer.Sound('sounds/bingus_title4.wav')
musiclist = [music1, music2, music3, music4]
for music in musiclist:
    music.set_volume(0.9)


class Title(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        
        self.game = game
        self.health = 3
        self.text_orig = "PRESS LEFT MOUSE OR ANY CONTROLLER BUTTON TO START"
        self.load_assets()
        self.fade = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.done1 = False
        self.current_time = pygame.time.get_ticks()
        self.delay = 20000 # 13 seconds
        self.code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT]
        self.cheat = False
        self.music = random.choice(musiclist)
        self.music.play()
        
    def update(self, dt, actions):
        if self.cheat == True:
            self.health = 50
        self.fade.update(dt, actions)
        if self.done1 == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                for i in range(self.game.playthroughs_completed):
                    self.health += 1
                if self.game.completed_levels >= 2:
                    self.health += 1
                    self.game.playthroughs_completed += 1
                    self.game.completed_levels = 0
                    if self.health >= 7:
                        self.health = 7
                level1 = Level1(self.game, self.health)
                level1.enter_state()
        if actions['left_mouse'] == True:
            self.done1 = True

        #secret cheat code
        if actions['up'] == True and actions['left_mouse'] == True:
            self.cheat = True
            
    def load_assets(self):
        self.title_screen = pygame.image.load('graphics/titlescreen.png')
        
    def draw(self, display_surface):
        
        if pygame.time.get_ticks() - self.current_time > self.delay or self.done1 == True:
            self.music.fadeout(2000)
        display_surface.blit(self.title_screen, (0,0))
        self.draw_text(display_surface, self.text_orig, c.WINDOW_WIDTH/2 - 570, c.WINDOW_HEIGHT - 50, c.WHITE)
        self.fade.draw(display_surface)
        if self.done1 == True:
            self.fadeout.draw(display_surface)

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_surface, text_rect)



   