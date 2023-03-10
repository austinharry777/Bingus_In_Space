import pygame, constants as c, math
from random import randint, uniform, choice
from base_state import Base_State
from game_over import Game_Over
from resources import *
from math import sin 
from pause import Pause
from all_clear import All_Clear
pygame.init()
pygame.mixer.init()

final_message = pygame.mixer.Sound('sounds/final speech.wav')


class Death_Message(Base_State):
    def __init__(self, game, score, health, ship, background, foreground, finalboss):
        Base_State.__init__(self, game)
        self.game = game
        self.score = score
        self.health = health
        self.ship = ship
        self.background = background
        self.foreground = foreground
        self.finalboss = finalboss
        self.finalboss_group = pygame.sprite.GroupSingle()
        self.finalboss_group.add(self.finalboss)
        self.last_explosion_group = pygame.sprite.GroupSingle()
        self.clock = pygame.time.Clock()
        final_message.play()
        self.message_time = pygame.time.get_ticks()
        self.message_delay = 12000
        self.done = False
        self.explosion = False 

    def update(self, dt, actions):
        self.finalboss_group.update(dt)
        self.last_explosion_group.update(dt)
        if pygame.time.get_ticks() - self.message_time > self.message_delay and self.explosion == False:
           self.last_explosion = BossExplosion(self.finalboss.rect.center)
           self.last_explosion_group.add(self.last_explosion)
           self.explosion = True
           self.done = True
        
        if self.done == True:
            if self.last_explosion.animation_done == True:
                all_clear = All_Clear(self.game)
                all_clear.enter_state()

    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.foreground.draw(display_surface)
        self.finalboss_group.draw(display_surface)
        self.last_explosion_group.draw(display_surface)

            

        
        

