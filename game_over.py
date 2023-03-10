import pygame, constants as c
from pygame import mixer
from base_state import Base_State
from fade import Cutscene_Fadeout
from health_message import Health_Message
pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus game over.wav')
music.set_volume(0.4)


class Game_Over(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        music.play()
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.done1 = False

    def update(self, dt, actions):
        if self.done1 == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                if self.game.completed_levels >= 2:
                    health_message = Health_Message(self.game)
                    health_message.enter_state()
                else:
                    while len(self.game.state_stack) > 1:
                        self.game.state_stack.pop()

        if actions['left_mouse'] == True:
            self.done1 = True
        
    def draw(self, display_surface):
        self.draw_text(display_surface, "GAME OVER", c.WINDOW_WIDTH/2 - 220, c.WINDOW_HEIGHT/2, c.WHITE)
        if self.done1 == True:
            self.fadeout.draw(display_surface)
        
    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_scaled_surface = pygame.transform.scale2x(text_surface)
        text_rect = text_scaled_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_scaled_surface, text_rect)