import pygame, constants as c, math
from random import randint, uniform, choice
from base_state import Base_State
from game_over import Game_Over
from resources import *
from math import sin 
from pause import Pause
from death_message import Death_Message
pygame.init()
pygame.mixer.init()

final_music = pygame.mixer.Sound('sounds/bingusfinalboss.wav')
final_music.set_volume(0.8)


class Level4Boss(Base_State):
    def __init__(self, game, score, health, explosion_group, boss_explosion_group, 
    ship, background, foreground):
        Base_State.__init__(self, game)
        self.game = game
        self.score = score
        self.health = health
        self.boss_explosion_group = boss_explosion_group
        self.ship = ship
        self.background = background
        self.foreground = foreground
        self.clock = pygame.time.Clock()
        #sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        #sprite creation
        self.spaceship_group.add(self.ship)
        #explosion animation
        self.explosion_group = explosion_group
        self.boss_explosion_group = boss_explosion_group
        self.boss_explosion_group2 = pygame.sprite.GroupSingle()
        final_music.play(-1)
        #score text
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        #invulnerability
        self.vulnerable = True
        self.hit_time = None
        #boss groups
        self.finalboss_group = pygame.sprite.GroupSingle()
        self.finalboss = FinalBoss(self.ship)
        self.finalboss_group.add(self.finalboss)
        #boss invulnerability
        self.boss_vulnerable = True
        self.boss_hit_time = None
        self.boss_time = False
        self.boss_time_timer = pygame.time.get_ticks()
        self.boss_time_delay = 3000
        self.boss_dead = False
        #game over timer and bool
        self.game_over_delay = 1000
        self.game_over = False
        self.game_over_timer = pygame.time.get_ticks()
        self.takedamage = pygame.mixer.Sound('sounds/takedamage.wav')
        self.takedamage.set_volume(1)
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosion_sound.set_volume(0.8)
        #health and bar
        self.health_sprites = []
        for i in range(1, 51):
            sprite = pygame.image.load(f'graphics/health_bar.png').convert_alpha()
            rect = sprite.get_rect(midbottom = (200 + i * 50, 710))
            self.health_sprites.append((sprite, rect))
        self.health_surf = self.font.render(f"HEALTH:", True, (255,255,255))
        self.health_rect = self.health_surf.get_rect(midbottom = (100, 710))
        #Initialize boss attack timer
        

    def update(self, dt, actions):
        if actions['enter'] == True:
            pause_menu = Pause(self.game)
            pause_menu.enter_state()
        if pygame.time.get_ticks() - self.boss_time_timer > self.boss_time_delay:
            self.boss_time = True
        if self.game_over == True and pygame.time.get_ticks() - self.game_over_timer > self.game_over_delay:
                pygame.mixer.stop()
                game_over = Game_Over(self.game)
                game_over.enter_state()
        self.background.update(dt)
        self.ship.laser_group.update(dt)
        self.spaceship_group.update(dt, actions)
        self.explosion_group.update(dt)
        self.finalboss_group.update(dt)
        self.finalboss.laser_group.update(dt)
        self.finalboss.worm_group.update(dt)
        self.finalboss.bullet_group.update(dt, self.ship)
        self.boss_laser_collision()
        self.boss_bullet_collision()
        self.boss_blood_laser_collision()
        self.worm_collision()
        self.boss_collision()
        self.boss_explosion_group2.update(dt)

        self.boss_explosion_group.update(dt)
        if not self.boss_vulnerable:
            currentboss_time = pygame.time.get_ticks()  
            if currentboss_time - self.boss_hit_time > 500:
                self.boss_vulnerable = True
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()  
            if current_time - self.hit_time > 2000:
                self.vulnerable = True
        if self.boss_dead == True:
            self.ship.laser_group.empty()
            if self.finalboss_explosion.animation_done == True:
                final_music.fadeout(1000)
                death_message = Death_Message(self.game, self.score, self.health, self.ship, self.background, self.foreground, self.finalboss)
                death_message.enter_state()

    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.finalboss.worm_group.draw(display_surface)
        self.foreground.draw(display_surface)
        self.finalboss.laser_group.draw(display_surface)
        self.finalboss_group.draw(display_surface)
        self.finalboss.bullet_group.draw(display_surface)
        self.ship.laser_group.draw(display_surface)
        self.spaceship_group.draw(display_surface)
        self.explosion_group.draw(display_surface)
        self.boss_explosion_group.draw(display_surface)
        self.boss_explosion_group2.draw(display_surface)
        
        self.display_score(display_surface)
        display_surface.blit(self.health_surf, self.health_rect)
        for i in range(self.health):
            display_surface.blit(*self.health_sprites[i])

    def boss_laser_collision(self):
        for laser in self.ship.laser_group:
                for floppa in self.finalboss_group:
                    if pygame.sprite.collide_mask(laser, floppa):
                        laser.kill()
                    if pygame.sprite.collide_mask(laser, floppa) and self.boss_vulnerable == True:
                        self.finalboss.health -= 1
                        self.takedamage.play()
                        self.finalboss.damage_boss = True
                        self.boss_vulnerable = False
                        self.boss_hit_time = pygame.time.get_ticks()
                        if self.finalboss.health <= 0:
                            self.finalboss.laser_group.empty()
                            self.finalboss.bullet_group.empty()
                            self.finalboss.worm_group.empty()
                            self.boss_dead = True
                            self.score += 100000
                            self.finalboss_explosion = BossExplosion(self.finalboss.rect.center)
                            self.boss_explosion_group2.add(self.finalboss_explosion)
                            self.finalboss.laser_interval = 200000
                            self.finalboss.worm_interval = 300000
                            self.finalboss.bullet_interval = 300000

                            

    def boss_bullet_collision(self):
        for bullet in self.finalboss.bullet_group:
            if pygame.sprite.collide_mask(self.ship, bullet) and self.vulnerable == True:
                self.ship.damage_ship = True
                self.health -= 1
                self.explosion_sound.play()
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def boss_blood_laser_collision(self):
        for laser in self.finalboss.laser_group:
            if pygame.sprite.collide_mask(self.ship, laser) and self.vulnerable == True:
                self.ship.damage_ship = True
                self.health -= 1
                self.explosion_sound.play()
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def worm_collision(self):
        for worm in self.finalboss.worm_group:
            if pygame.sprite.collide_mask(self.ship, worm) and self.vulnerable == True:
                self.ship.damage_ship = True
                self.health -= 1
                self.explosion_sound.play()
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def boss_collision(self):   
        for floppa in self.finalboss_group:
            if pygame.sprite.collide_mask(self.ship, floppa) and self.vulnerable == True:
                self.ship.damage_ship = True
                self.health -= 1
                self.explosion_sound.play()
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def display_score(self, display_surface):
        self.score += 1
        self.score_text = f'{self.score}'
        self.text_surf = self.font.render(f"SCORE: {self.score_text}", True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (1000, 50))
        display_surface.blit(self.text_surf,self.text_rect)
