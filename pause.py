import pygame, constants as c
from pygame import mixer
from base_state import Base_State


class Pause(Base_State):
    def __init__(self,game):
        Base_State.__init__(self, game)
        self.game = game
        self.pause_timer = pygame.time.get_ticks()
        self.pause_speed = 1000
        self.pause_time = False
        
    def update(self, dt, actions):
        if pygame.time.get_ticks() - self.pause_timer > self.pause_speed:
            self.pause_time = True
        if actions['enter'] == True and self.pause_time == True:
            self.game.state_stack.pop()
        self.game.reset_keys()
        
    def draw(self, display_surface):
        self.draw_text(display_surface, "PAUSED", c.WINDOW_WIDTH/2 - 160, c.WINDOW_HEIGHT/2, c.WHITE)
          
    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_scaled_surface = pygame.transform.scale2x(text_surface)
        text_rect = text_scaled_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_scaled_surface, text_rect)