import pygame
from base_state import Base_State
import constants as c
from fade import Cutscene_Fadeout
from pygame import mixer
from level4 import Level4
pygame.mixer.init()

sound = pygame.mixer.Sound('sounds/floppanosecutscene.wav')


class NoseScene(Base_State):
    def __init__(self, game, score, health):
        Base_State.__init__(self, game)
        self.score = score
        self.health = health
        self.game = game
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_done = False
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.animation_speed = 150
        self.fade = Cutscene_Fadeout(self.game, 1, 0,0)
        sound.play()

    def update(self, dt, actions):
        self.animate()
        if self.animation_done:
            self.fade.update(dt, actions)
            if self.fade.fade_complete:
                level_4 = Level4(self.game, self.score, self.health)
                level_4.enter_state()

    def draw(self, display_surface):
        display_surface.blit(self.image, (0, 0))
    
    def load_animation(self):
        for i in range(0, 36):
            frames = (pygame.image.load(f'graphics/floppanosecutscene/{i}.png').convert_alpha())
            self.animation_frames.append(frames)

        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = len(self.animation_frames) - 1
                self.image = self.animation_frames[self.frame_index]
                self.animation_done = True
                
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

        # return self.animation_done
    
    def draw(self, display_surface):
        display_surface.blit(self.image, (0, 0))
        if self.animation_done:
            self.fade.draw(display_surface)