import pygame
from base_state import Base_State
import constants as c
from pygame import mixer
from nose_scene import NoseScene
pygame.mixer.init()
music = pygame.mixer.Sound('sounds/bingus cutscene1.wav')
music.set_volume(0.6)


class Cutscene3(Base_State):
    def __init__(self, game, score, health):
        Base_State.__init__(self, game)
        self.score = score
        self.health = health
        self.game = game
        self.load_assets() 
        self.bing_orig = "BINGUS FRIEND OF FLOPPA."
        self.bing_orig1 = "FLOPPA BEING CONTROLLED."
        self.bing_orig2 = "BINGUS KNOW NOW."
        self.bing_orig3 = "KNOW WHAT MUST BE DONE."
        self.flop_orig = "FLOPPA HATE BINGUS."
        self.flop_orig1 = "FLOPPA RAGE INSIDE."
        self.flop_orig2 = "FLOPPA FEEL SICK."
        self.flop_orig3 = "FLOPPA NO REMEMBER."
        self.reset_rect = pygame.Rect(450, 150, 300, 300)
        self.reset_image = pygame.surface.Surface((300, 300))
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.m = 0
        self.n = 0
        self.o = 0
        self.p = 0
        self.done1 = False
        self.done2 = False
        self.done3 = False
        self.done4 = False
        self.done5 = False
        self.done6 = False
        self.done7 = False
        self.done8 = False
        self.done9 = False
        self.text = ""
        self.current_time = pygame.time.get_ticks()
        self.current_text_time = pygame.time.get_ticks()    
        self.delay = 2000 # 3 seconds
        self.delaytext = 500 # 0.5 seconds
        self.delaytext2 = 850 # 0.85 seconds 
        # self.fade = Cutscene_Fadeout(self.game, 1, 0,0)
        self.animation_done = False
        music.play(-1)
        

    def update(self, dt, actions):
        if actions['space_bar'] == True or actions['enter'] == True or actions['left_mouse'] == True or actions['right_mouse'] == True:
            self.done9 = True
            
        if self.done9 == True:
            music.fadeout(2000)
            for text_sound in self.text_sounds:
                text_sound.stop()
            nose_scene = NoseScene(self.game, self.score, self.health)
            nose_scene.enter_state()
            
        if self.done8 == True and pygame.time.get_ticks() - self.current_time > self.delay * 8:
            self.done9 = True
        self.i += 0.1

        if self.done7 == True and pygame.time.get_ticks() - self.current_time > self.delay * 7:
            self.text = ""
            self.p += 0.1
            while self.done8 == False:
                self.text_sound8.play()
                self.text += self.flop_orig3[len(self.text)]
                if len(self.text) == len(self.flop_orig3):
                    self.done8 = True

        elif self.done6 == True and pygame.time.get_ticks() - self.current_time > self.delay * 6:
            self.text = ""
            self.o += 0.1
            while self.done7 == False:
                self.text_sound7.play()
                self.text += self.flop_orig2[len(self.text)]
                if len(self.text) == len(self.flop_orig2):
                    self.done7 = True
        
        elif self.done5 == True and pygame.time.get_ticks() - self.current_time > self.delay * 5:
            self.text = ""
            self.n += 0.1
            while self.done6 == False:
                self.text_sound4.play()
                self.text += self.bing_orig3[len(self.text)]
                if len(self.text) == len(self.bing_orig3):
                    self.done6 = True

        elif self.done4 == True and pygame.time.get_ticks() - self.current_time > self.delay * 4:
            self.text = ""
            self.m += 0.1
            while self.done5 == False:
                self.text_sound2.play()
                self.text += self.bing_orig2[len(self.text)]
                if len(self.text) == len(self.bing_orig2):
                    self.done5 = True
        
        elif self.done3 == True and pygame.time.get_ticks() - self.current_time > self.delay * 3:
            self.text = ""
            self.l += 0.1
            while self.done4 == False:
                self.text_sound6.play()
                self.text += self.flop_orig1[len(self.text)]
                if len(self.text) == len(self.flop_orig1):
                    self.done4 = True
        
        elif self.done2 == True and pygame.time.get_ticks() - self.current_time > self.delay * 2:
            self.text = ""
            self.k += 0.1
            while self.done3 == False:
                self.text_sound5.play()
                self.text += self.flop_orig[len(self.text)]
                if len(self.text) == len(self.flop_orig):
                    self.done3 = True
        
        
        elif self.done1 == True and pygame.time.get_ticks() - self.current_time > self.delay:
            self.text = ""
            self.j += 0.1
            while self.done2 == False:
                self.text_sound1.play()
                self.text += self.bing_orig1[len(self.text)]
                if len(self.text) == len(self.bing_orig1):
                    self.done2 = True
        
        
        else:
            while self.done1 == False:
                    self.text_sound.play()
                    self.text += self.bing_orig[len(self.text)]
                    if len(self.text) == len(self.bing_orig):
                        self.done1 = True
    
    
    
    
    
    def load_assets(self):
        self.bingusimage = pygame.image.load('graphics/binguscutscene2.png').convert()
        self.floppaimage = pygame.image.load('graphics/floppacutscene2.png').convert()
        self.text_sound = pygame.mixer.Sound('sounds/bingustext.wav') # write a for loop to fix this later
        self.text_sound.set_volume(0.2)
        self.text_sound1 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound1.set_volume(0.2)
        self.text_sound2 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound2.set_volume(0.2)
        self.text_sound3 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound3.set_volume(0.2)
        self.text_sound4 = pygame.mixer.Sound('sounds/bingustext.wav')
        self.text_sound4.set_volume(0.2)
        self.text_sound5 = pygame.mixer.Sound('sounds/floppatext.wav')
        self.text_sound5.set_volume(0.2)
        self.text_sound6 = pygame.mixer.Sound('sounds/floppatext.wav')
        self.text_sound6.set_volume(0.2)
        self.text_sound7 = pygame.mixer.Sound('sounds/floppatext.wav')
        self.text_sound7.set_volume(0.2)
        self.text_sound8 = pygame.mixer.Sound('sounds/floppatext.wav')
        self.text_sound8.set_volume(0.2)
        self.text_sounds = [self.text_sound, self.text_sound1, self.text_sound2, 
                            self.text_sound3, self.text_sound4, self.text_sound5, 
                            self.text_sound6, self.text_sound7, self.text_sound8]


    
    def draw(self, display_surface):
        display_surface.fill(c.BLACK)
        display_surface.blit(self.bingusimage, (100,100))
        display_surface.blit(self.floppaimage, (940,380))
        
        self.draw_text(display_surface, self.bing_orig[:int(self.i)], 450, 150, c.WHITE)
        if pygame.time.get_ticks() - self.current_text_time > self.delaytext:
            self.text_sound.stop()
        if pygame.time.get_ticks() - self.current_time > self.delay:
            self.draw_text(display_surface, self.bing_orig1[:int(self.j)], 450, 150 + 75, c.WHITE)
            if pygame.time.get_ticks() - self.current_time > self.delay + self.delaytext:
                self.text_sound1.stop()
            if pygame.time.get_ticks() - self.current_time > self.delay * 2:
                self.draw_text(display_surface, self.flop_orig[:int(self.k)], 370, 420, c.WHITE)
                if pygame.time.get_ticks() - self.current_time > self.delay * 2 + self.delaytext:
                    self.text_sound5.stop()
                if pygame.time.get_ticks() - self.current_time > self.delay * 3:
                    self.draw_text(display_surface, self.flop_orig1[:int(self.l)], 430, 420 + 75, c.WHITE)
                    if pygame.time.get_ticks() - self.current_time > self.delay * 3 + self.delaytext:
                        self.text_sound6.stop()
                    if pygame.time.get_ticks() - self.current_time > self.delay * 4:
                        pygame.draw.rect(display_surface, c.BLACK, (400, -700, 1000, 1000))
                        self.draw_text(display_surface, self.bing_orig2[:int(self.m)], 450, 150, c.WHITE)
                        if pygame.time.get_ticks() - self.current_time > self.delay * 4 + self.delaytext:
                            self.text_sound3.stop()
                        if pygame.time.get_ticks() - self.current_time > self.delay * 5:
                            self.draw_text(display_surface, self.bing_orig3[:int(self.n)], 450, 150 + 75, c.WHITE)
                            if pygame.time.get_ticks() - self.current_time > self.delay * 5 + self.delaytext:
                                self.text_sound4.stop()
                            if pygame.time.get_ticks() - self.current_time > self.delay * 6:
                                pygame.draw.rect(display_surface, c.BLACK, (-70, 400, 1000, 1000))
                                self.draw_text(display_surface, self.flop_orig2[:int(self.o)], 430, 420, c.WHITE)
                                if pygame.time.get_ticks() - self.current_time > self.delay * 6 + self.delaytext:
                                    self.text_sound7.stop()
                                if pygame.time.get_ticks() - self.current_time > self.delay * 7:
                                    self.draw_text(display_surface, self.flop_orig3[:int(self.p)], 350, 420 + 75, c.WHITE)
                                    if pygame.time.get_ticks() - self.current_time > self.delay * 7 + self.delaytext:
                                        self.text_sound8.stop()
        
        if self.done9 == True:
            music.fadeout(2000)
            for text_sound in self.text_sounds:
                text_sound.stop()
            
    def draw_text(self, surface, text, x, y, color):
        font = pygame.font.Font('graphics/gradius.ttf', 25)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x, y)
        surface.blit(text_surface, text_rect)


