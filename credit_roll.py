import pygame, sys, os, time, random
from base_state import Base_State
import constants as c
from fade import Cutscene_Fadeout, Cutscene_Fadein
from credit_roll2 import Credit_Roll2 

class Credit_Roll(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000
        self.bingus_image = pygame.image.load('graphics/binguscutscene2.png').convert_alpha()
        self.bingus_rect = self.bingus_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.pic1 = False
        self.floppa_image = pygame.image.load('graphics/cutscenefloppa.png').convert_alpha()
        self.floppa_rect = self.floppa_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.pic2 = False
        self.parasite_image = pygame.image.load('graphics/finalbosscredits.png').convert_alpha()
        self.parasite_rect = self.parasite_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.pic3 = False
        self.jetpack_image = pygame.image.load('graphics/floppaboss1/0.png').convert_alpha()
        self.jetpack_rect = self.jetpack_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.pic4 = False
        self.hotair_image = pygame.image.load('graphics/hotairfloppa/0.png').convert_alpha()
        self.hotair_rect = self.hotair_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.pic5 = False
        self.display_timer = pygame.time.get_ticks()
        self.display_length = 6000
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout2 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein2 = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout3 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein3 = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout4 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein4 = Cutscene_Fadein(self.game, 1, 0,0) 
        self.fadeout5 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein5 = Cutscene_Fadein(self.game, 1, 0,0) 

    def update(self, dt, actions):
        self.fadein.update(dt, actions)
        if self.pic1 == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                self.fadein2.update(dt, actions)
                if self.pic2 == True:
                    self.fadeout2.update(dt, actions)
                    if self.fadeout2.fade_complete == True:
                        self.fadein3.update(dt, actions)
                        if self.pic3 == True:
                            self.fadeout3.update(dt, actions)
                            if self.fadeout3.fade_complete == True:
                                self.fadein4.update(dt, actions)
                                if self.pic4 == True:
                                    self.fadeout4.update(dt, actions)
                                    if self.fadeout4.fade_complete == True:
                                        self.fadein5.update(dt, actions)
                                        if self.pic5 == True:
                                            self.fadeout5.update(dt, actions)
                                            if self.fadeout5.fade_complete == True:
                                                credit_roll2 = Credit_Roll2(self.game)
                                                credit_roll2.enter_state()
                
        if pygame.time.get_ticks() - self.display_timer > self.display_length:
            self.pic1 = True
        if self.pic1 == True and pygame.time.get_ticks() - self.display_timer > (self.display_length * 2 + 1000):
            self.pic2 = True
        if self.pic2 == True and pygame.time.get_ticks() - self.display_timer > (self.display_length * 3 + 1000):
            self.pic3 = True
        if self.pic3 == True and pygame.time.get_ticks() - self.display_timer > (self.display_length * 4 + 1000):
            self.pic4 = True
        if self.pic4 == True and pygame.time.get_ticks() - self.display_timer > (self.display_length * 5 + 1000):
            self.pic5 = True
            
        

    def draw(self, display_surface):
        display_surface.fill(c.BLACK)
        display_surface.blit(self.bingus_image, self.bingus_rect)
        self.fadein.draw(display_surface)
        self.draw_text(display_surface, 'BINGUS', c.WINDOW_WIDTH / 2, 500, c.WHITE)
        self.draw_text(display_surface, 'BINGUS HARRINGTON', c.WINDOW_WIDTH / 2, 600, c.WHITE)
        if self.pic1 == True:
            self.fadeout.draw(display_surface) 
            if self.fadeout.fade_complete == True:
                display_surface.blit(self.floppa_image, self.floppa_rect)
                self.fadein2.draw(display_surface)
                self.draw_text(display_surface, 'FLOPPA', c.WINDOW_WIDTH / 2, 500, c.WHITE)
                self.draw_text(display_surface, 'FLOPPA ZETA-JONES-SANCHEZ III', c.WINDOW_WIDTH / 2, 600, c.WHITE)
                if self.pic2 == True:
                    self.fadeout2.draw(display_surface)
                    if self.fadeout2.fade_complete == True:
                        display_surface.blit(self.parasite_image, self.parasite_rect)
                        self.fadein3.draw(display_surface)
                        self.draw_text(display_surface, 'EVIL PARASITE', c.WINDOW_WIDTH / 2, 500, c.WHITE)
                        self.draw_text(display_surface, 'LEONARDUS DECAPLIO', c.WINDOW_WIDTH / 2, 600, c.WHITE)
                        if self.pic3 == True:
                            self.fadeout3.draw(display_surface)
                            if self.fadeout3.fade_complete == True:
                                display_surface.blit(self.jetpack_image, self.jetpack_rect)
                                self.fadein4.draw(display_surface)
                                self.draw_text(display_surface, 'JETPACK FLOPPA', c.WINDOW_WIDTH / 2, 500, c.WHITE)
                                self.draw_text(display_surface, 'SHOWER HANDULZ', c.WINDOW_WIDTH / 2, 600, c.WHITE)
                                if self.pic4 == True:
                                    self.fadeout4.draw(display_surface)
                                    if self.fadeout4.fade_complete == True:
                                        display_surface.blit(self.hotair_image, self.hotair_rect)
                                        self.fadein5.draw(display_surface)
                                        self.draw_text(display_surface, 'HOT AIR BALOON FLOPPA', c.WINDOW_WIDTH / 2, 500, c.WHITE)
                                        self.draw_text(display_surface, 'MR. BEASTLY', c.WINDOW_WIDTH / 2, 600, c.WHITE)
                                        if self.pic5 == True:
                                            self.fadeout5.draw(display_surface)
                                            
            

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

        
           
