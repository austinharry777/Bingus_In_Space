import pygame, constants as c
from pygame import mixer
from base_state import Base_State
from fade import Cutscene_Fadeout
from ending import Ending
pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus all clear.wav')
music.set_volume(0.6)


class All_Clear(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.done1 = False
        self.done_timer = pygame.time.get_ticks()
        self.delay = 11000 # 5 seconds
        music.play()

    def update(self, dt, actions):
        if self.done1 == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                ending = Ending(self.game)
                ending.enter_state()

        
        if pygame.time.get_ticks() - self.done_timer > self.delay:
            self.done1 = True

    def draw(self, display_surface):
        self.draw_text(display_surface, "ALL CLEAR", c.WINDOW_WIDTH/2 , c.WINDOW_HEIGHT/2, c.WHITE)
        if self.done1 == True:
            self.fadeout.draw(display_surface)

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_scaled_surface = pygame.transform.scale2x(text_surface)
        text_rect = text_scaled_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_scaled_surface, text_rect)