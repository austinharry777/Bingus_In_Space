import pygame
from base_state import Base_State
from title import Title
import constants as c
from fade import Cutscene_Fadeout
from pygame import mixer
pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus intro.wav')


class Intro(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        
        music.play()
        self.load_assets() 
        self.text_orig = "BINGUS WANDER FOREST."
        self.text_orig1 = "BINGUS FIND ROCKET SHIP."
        self.text_orig2 = "BINGUS FLY TO MOON."
        self.text_orig3 = "NOT IF FLOPPA GET HIM FIRST."
        self.text_orig4 = "HELP BINGUS!"
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.m = 0
        self.done7 = False
        self.done6 = False
        self.done5 = False
        self.done1 = False
        self.done2 = False
        self.done3 = False
        self.done4 = False
        self.text = ""
        self.current_time = pygame.time.get_ticks()
        self.current_text_time = pygame.time.get_ticks()    
        self.delay = 2000 # 3 seconds
        self.delaytext = 500 # 0.5 seconds
        self.delaytext2 = 850 # 0.85 seconds 
        self.fade = Cutscene_Fadeout(self.game, 1, 0,0)
    
    def update(self, dt, actions):
        if actions['space_bar'] == True or actions['enter'] == True or actions['left_mouse'] == True or actions['right_mouse'] == True:
            self.done6 = True
            
        if self.done6 == True:
            music.fadeout(2000)
            for text_sound in self.text_sounds:
                text_sound.stop()
            
            self.fade.update(dt, actions)
            if self.fade.fade_complete == True:
                title = Title(self.game)
                title.enter_state()
        
        if self.done5 == True and pygame.time.get_ticks() - self.current_time > self.delay * 5:
            self.done6 = True
            
        self.i += 0.1
        if self.done4 == True and pygame.time.get_ticks() - self.current_time > self.delay * 4:
            self.text = ""
            self.m += 0.1
            while self.done5 == False:
                self.text_sound4.play()
                self.text += self.text_orig4[len(self.text)]
                if len(self.text) == len(self.text_orig4):
                    self.done5 = True
                    
        elif self.done3 == True and pygame.time.get_ticks() - self.current_time > self.delay * 3:
            self.text = ""
            self.l += 0.1
            while self.done4 == False:
                self.text_sound3.play()
                self.text += self.text_orig3[len(self.text)]
                if len(self.text) == len(self.text_orig3):
                    self.done4 = True
                    
        elif self.done2 == True and pygame.time.get_ticks() - self.current_time > self.delay * 2:
            self.text = ""
            self.k += 0.1
            while self.done3 == False:
                self.text_sound2.play()
                self.text += self.text_orig2[len(self.text)]
                if len(self.text) == len(self.text_orig2):
                    self.done3 = True
                    
        elif self.done1 == True and pygame.time.get_ticks() - self.current_time > self.delay:
            self.text = ""
            self.j += 0.1
            while self.done2 == False:
                self.text_sound1.play()
                self.text += self.text_orig1[len(self.text)]
                if len(self.text) == len(self.text_orig1):
                    self.done2 = True
                    
        else:
            while self.done1 == False:
                self.text_sound.play()
                self.text += self.text_orig[len(self.text)]
                if len(self.text) == len(self.text_orig):
                    self.done1 = True
                    
    def load_assets(self):
        self.background = pygame.image.load('graphics/bingusgameintro.png').convert()
        self.text_sound = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound.set_volume(0.2)
        self.text_sound1 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound1.set_volume(0.2)
        self.text_sound2 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound2.set_volume(0.2)
        self.text_sound3 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound3.set_volume(0.2)
        self.text_sound4 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound4.set_volume(0.2)
        self.text_sounds = [self.text_sound, self.text_sound1, self.text_sound2, 
                            self.text_sound3, self.text_sound4]


    def draw(self, display_surface):
        display_surface.blit(self.background, (0,0))
        self.draw_text(display_surface, self.text_orig[:int(self.i)], 550, 200, c.WHITE)
        if pygame.time.get_ticks() - self.current_text_time > self.delaytext:
            self.text_sound.stop()
        if pygame.time.get_ticks() - self.current_time > self.delay:
            self.draw_text(display_surface, self.text_orig1[:int(self.j)], 550, 200 + 75, c.WHITE)
            if pygame.time.get_ticks() - self.current_time > self.delay + self.delaytext:
                self.text_sound1.stop()
            if pygame.time.get_ticks() - self.current_time > self.delay * 2:
                self.draw_text(display_surface, self.text_orig2[:int(self.k)], 550, 200 + 150, c.WHITE)
                if pygame.time.get_ticks() - self.current_time > self.delay * 2 + self.delaytext:
                    self.text_sound2.stop()
                if pygame.time.get_ticks() - self.current_time > self.delay * 3:
                    self.draw_text(display_surface, self.text_orig3[:int(self.l)], 550, 200 + 225, c.WHITE)
                    if pygame.time.get_ticks() - self.current_time > self.delay * 3 + self.delaytext2:
                        self.text_sound3.stop()
                    if pygame.time.get_ticks() - self.current_time > self.delay * 4:
                        self.draw_text(display_surface, self.text_orig4[:int(self.m)], 550, 200 + 300, c.WHITE)
                        if pygame.time.get_ticks() - self.current_time > self.delay * 4 + self.delaytext:
                            self.text_sound4.stop()
        if self.done6 == True:
            music.fadeout(2000)
            for text_sound in self.text_sounds:
                text_sound.stop()
            self.fade.draw(display_surface)
    
    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_surface, text_rect)
    

        
           
        
            
        
            
     

        
        

        

        
        