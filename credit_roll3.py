import pygame, sys, os, time, random
from base_state import Base_State
import constants as c
from fade import Cutscene_Fadeout, Cutscene_Fadein
from health_message import Health_Message


class Credit_Roll3(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 150
        self.animation_length = len(self.animation_frames) - 1
        self.jelly_image = self.animation_frames[self.frame_index]
        self.jelly_rect = self.jelly_image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2 - 100))
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000
        self.bingus_image = pygame.image.load('graphics/bingusinatophat.png').convert_alpha()
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
        self.display_length =5000
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout2 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein2 = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout3 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fadein3 = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout4 = Cutscene_Fadeout(self.game, 1, 0,0)
        self.scroll_speed = 30  # pixels per second
        self.font2 = pygame.font.Font('graphics/gradius.ttf', 50)
        self.text = "THE END"
        self.text_surface = self.font2.render(self.text, True, c.WHITE)
        self.text_rect = self.text_surface.get_rect(topleft=(450, 860))
        self.pos_x, self.pos_y = self.text_rect.center
        self.end = False

    def update(self, dt, actions):
        if self.end == True:
            self.fadeout4.update(dt, actions)
            if self.fadeout4.fade_complete == True:
                health_message = Health_Message(self.game)
                health_message.enter_state()
        
        
        self.fadein.update(dt, actions)
        
        if pygame.time.get_ticks() - self.display_timer > self.display_length:
                self.pic1 = True
                self.fadeout.update(dt, actions)
                if self.fadeout.fade_complete == True:
                    self.fadein2.update(dt, actions)
                    if pygame.time.get_ticks() - self.display_timer > self.display_length * 2:
                        self.pic2 = True
                        self.fadeout2.update(dt, actions)
                        if self.fadeout2.fade_complete == True:
                            self.animate()
                            self.fadein3.update(dt, actions)
                            if pygame.time.get_ticks() - self.display_timer > self.display_length * 3:
                                self.pic3 = True
                                self.fadeout3.update(dt, actions)
                                if self.fadeout3.fade_complete == True:
                                    self.pos_y -= self.scroll_speed * self.dt
                                    self.text_rect.center = (self.pos_x, self.pos_y)
                                    if self.pos_y <= c.WINDOW_HEIGHT / 2:
                                        self.pos_y = c.WINDOW_HEIGHT / 2
                                        if actions['left_mouse'] == True:
                                            self.end = True
                                            


                                            

    def draw(self, display_surface):
        display_surface.fill(c.BLACK)
        display_surface.blit(self.bingus_image, self.bingus_rect)
        self.fadein.draw(display_surface)
        self.draw_text(display_surface, 'BINGUS IN A TOP HAT', c.WINDOW_WIDTH / 2, 500, c.WHITE)
        if self.pic1 == True:
            self.fadeout.draw(display_surface) 
            if self.fadeout.fade_complete == True:
                display_surface.fill(c.BLACK)
                self.draw_text(display_surface, 'NO ANIMALS WERE HARMED IN THE MAKING OF THIS GAME.', c.WINDOW_WIDTH / 2, 300-100, c.WHITE)
                self.draw_text(display_surface, 'THIS IS A WORK OF FICTION.', c.WINDOW_WIDTH / 2, 350-100, c.WHITE)
                self.draw_text(display_surface, 'ANY SIMILARITY TO ACTUAL PERSONS, ANIMALS, OR EVENTS', c.WINDOW_WIDTH / 2, 400-100, c.WHITE)
                self.draw_text(display_surface, 'IS PURELY COINCIDENTAL.', c.WINDOW_WIDTH / 2, 450-100, c.WHITE)
                self.draw_text(display_surface, 'COPYRIGHT 2023 - TEAM JELLY', c.WINDOW_WIDTH / 2, 500-100, c.WHITE)
                self.draw_text(display_surface, 'ALL RIGHTS RESERVED.', c.WINDOW_WIDTH / 2, 550-100, c.WHITE)
                self.fadein2.draw(display_surface)
                if self.pic2 == True:
                    self.fadeout2.draw(display_surface)
                    if self.fadeout2.fade_complete == True:
                        display_surface.fill(c.BLACK)
                        display_surface.blit(self.jelly_image, self.jelly_rect)
                        self.fadein3.draw(display_surface)
                        if self.pic3 == True:
                            self.fadeout3.draw(display_surface)
                            if self.fadeout3.fade_complete == True:
                                display_surface.blit(self.text_surface, self.text_rect)
                                if self.end == True:
                                    self.fadeout4.draw(display_surface)
                                    
                                
                                
                        
                        
    
    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_animation(self):
        for i in range(0, 17):
            frames = pygame.image.load(f'graphics/teamjelly/{i}.png').convert_alpha()
            self.animation_frames.append(frames)

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index > self.animation_length:
                self.frame_index = self.animation_length
                self.jelly_image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.jelly_image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
        