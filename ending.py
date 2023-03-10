import pygame
from base_state import Base_State
import constants as c
from fade import Cutscene_Fadeout, Cutscene_Fadein
from pygame import mixer
from pygame.math import Vector2 as vec
from random import randint, uniform
from credit_roll import Credit_Roll

pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus end complete.wav')
music.set_volume(0.8)

class Ending(Base_State):   
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        self.clock = pygame.time.Clock()
        music.play()
        self.load_assets()
        self.hug_image = pygame.image.load('graphics/cathugs.png').convert_alpha()
        self.text_orig = "BINGUS DESTROY PARASITE."
        self.text_orig1 = "BINGUS HAVE FLOPPA BACK AS FRIEND."
        self.text_orig2 = "BINGUS AND FLOPPA..."
        self.text_orig3 = "NOW FIRST 'CATS' ON MOON!"
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.done1 = False
        self.done2 = False
        self.done3 = False
        self.done4 = False
        self.done = False
        self.text = ""
        self.current_time = pygame.time.get_ticks()
        self.current_text_time = pygame.time.get_ticks()    
        self.delay = 3500 
        self.delaytext = 1000 # 0.5 seconds
        self.delaytext2 = 750 # 0.85 seconds
        self.fade = Cutscene_Fadein(self.game, 1, 0,0)
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.bingus_group = pygame.sprite.Group()
        self.floppa_group = pygame.sprite.Group()
        self.bingus = Bingus()
        self.floppa = Floppa()
        self.bingus_group.add(self.bingus)
        self.floppa_group.add(self.floppa)

        
    def load_assets(self):
        self.ending_image = pygame.image.load('graphics/ending.png').convert()
        self.text_sound = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound.set_volume(0.2)
        self.text_sound1 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound1.set_volume(0.2)
        self.text_sound2 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound2.set_volume(0.2)
        self.text_sound3 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound3.set_volume(0.2)

    def update(self, dt, actions):
        self.fade.update(dt, actions)
        self.bingus_group.update(dt, actions)
        self.floppa_group.update(dt, actions)
        
        if self.done == True:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete == True:
                credit_roll = Credit_Roll(self.game)
                credit_roll.enter_state()

        self.i += 0.08

        if self.done4 == True and pygame.time.get_ticks() - self.current_time > self.delay * 4:
            self.done = True
                
        
        
        elif self.done3 == True and pygame.time.get_ticks() - self.current_time > self.delay * 3:
            self.bingus_group.remove(self.bingus)
            self.floppa_group.remove(self.floppa)
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
        
            
                
    
    def draw(self, display_surface):
        display_surface.blit(self.ending_image, (0,0))
        self.bingus_group.draw(display_surface)
        self.floppa_group.draw(display_surface)
        self.fade.draw(display_surface)
        self.draw_text(display_surface, self.text_orig[:int(self.i)], 150, 100, c.WHITE)
        if pygame.time.get_ticks() - self.current_text_time > self.delaytext:
            self.text_sound.stop()
        if pygame.time.get_ticks() - self.current_time > self.delay:
            self.draw_text(display_surface, self.text_orig1[:int(self.j)], 150, 100 + 75, c.WHITE)
            if pygame.time.get_ticks() - self.current_time > self.delay + self.delaytext:
                self.text_sound1.stop()
            if pygame.time.get_ticks() - self.current_time > self.delay * 2:
                self.draw_text(display_surface, self.text_orig2[:int(self.k)], 150, 100 + 150, c.WHITE)
                if pygame.time.get_ticks() - self.current_time > self.delay * 2 + self.delaytext2:
                    self.text_sound2.stop()
                if pygame.time.get_ticks() - self.current_time > self.delay * 3:
                    display_surface.blit(self.hug_image, (460, 390))
                    self.draw_text(display_surface, self.text_orig3[:int(self.l)], 350, 100 + 225, c.WHITE)
                    if pygame.time.get_ticks() - self.current_time > self.delay * 3 + self.delaytext:
                        self.text_sound3.stop()

        if self.done == True:
            self.fadeout.draw(display_surface)
        

    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_surface, text_rect)


class Floppa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        clock = pygame.time.Clock()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 250
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index] 
        self.rect = self.image.get_rect(center = (1380,540))
        #movement
        self.pos_x, self.pos_y = self.rect.center
        self.speed = 18
        self.dt = clock.tick(60) / 1000
        
    def update(self, dt, actions):
        self.animate()
        self.pos_x -= self.speed * self.dt 
        self.rect.center = (self.pos_x, self.pos_y)
        if self.pos_x <= 710:
            self.speed = 0
            self.image = self.animation_frames[1]

    def load_animation(self):
        for i in range(0,2):
            frames = (pygame.image.load(f'graphics/floppawalk/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index > self.animation_length:
                self.frame_index = 0
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
        


class Bingus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        clock = pygame.time.Clock()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 250
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index] 
        self.rect = self.image.get_rect(center = (-100,540))
        #movement
        self.pos_x, self.pos_y = self.rect.center
        self.speed = 18
        self.dt = clock.tick(60) / 1000
        
    def update(self, dt, actions):
        self.animate()
        self.pos_x += self.speed * self.dt 
        self.rect.center = (self.pos_x, self.pos_y)
        if self.pos_x >= 570:
            self.speed = 0
            self.image = self.animation_frames[1]
        
    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index > self.animation_length:
                self.frame_index = 0
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

    def load_animation(self):
        for i in range(0,2):
            frames = pygame.image.load(f'graphics/binguswalk/{i}.png').convert_alpha()
            self.animation_frames.append(frames)
        self.image = self.animation_frames[self.frame_index]

        
        

