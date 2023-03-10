import pygame, constants as c
from pygame import mixer
from base_state import Base_State
from fade import Cutscene_Fadeout
from cutscene3 import Cutscene3
pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus level complete.wav')
music.set_volume(0.9)


class LevelComplete3(Base_State):
    def __init__(self, game, score, health):
        Base_State.__init__(self, game)
        self.score = score
        self.health = health
        self.game = game
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.done1 = False
        self.done_timer = pygame.time.get_ticks()
        self.delay = 5000 # 5 seconds
        music.play()

    def update(self, dt, actions):
        if self.done1 == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                cutscene3 = Cutscene3(self.game, self.score, self.health)
                cutscene3.enter_state()

        # if actions['left_mouse'] == True:
        #     self.done1 = True
        if pygame.time.get_ticks() - self.done_timer > self.delay:
            self.done1 = True

    def draw(self, display_surface):
        self.draw_text(display_surface, "LEVEL COMPLETE", c.WINDOW_WIDTH/2 - 320, c.WINDOW_HEIGHT/2, c.WHITE)
        if self.done1 == True:
            self.fadeout.draw(display_surface)

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_scaled_surface = pygame.transform.scale2x(text_surface)
        text_rect = text_scaled_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_scaled_surface, text_rect)