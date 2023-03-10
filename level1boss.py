import pygame, constants as c, sys, math
from base_state import Base_State
from game_over import Game_Over
from level_complete import LevelComplete
from pause import Pause
from resources import *

pygame.init()
pygame.mixer.init()

boss_music = pygame.mixer.Sound('sounds/boss1.wav')
boss_music.set_volume(0.8)



class Level1Boss(Base_State):
    def __init__(self, game, score, health, explosion_group, ship, background):
        Base_State.__init__(self, game)
        self.game = game
        self.score = score
        self.health = health
        self.ship = ship
        self.background = background
        self.explosion_group = explosion_group
        #boss_music.play()
        self.clock = pygame.time.Clock()
        #sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        #sprite creation
        self.spaceship_group.add(self.ship)
        #explosion animation
        #self.explosion_group = pygame.sprite.Group()
        self.boss_explosion_group = pygame.sprite.GroupSingle()
        #Boss group
        self.boss = Boss1()
        self.boss_group = pygame.sprite.Group()
        self.boss_group.add(self.boss)
        #score text
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        #invulnerability
        self.vulnerable = True
        self.hit_time = None
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
        #health and bar
        self.health_sprites = []
        for i in range(1, 51):
            sprite = pygame.image.load(f'graphics/health_bar.png').convert_alpha()
            rect = sprite.get_rect(midbottom = (200 + i * 50, 710))
            self.health_sprites.append((sprite, rect))
        self.health_surf = self.font.render(f"HEALTH:", True, (255,255,255))
        self.health_rect = self.health_surf.get_rect(midbottom = (100, 710))

        self.boss_explosion_done = False
        boss_music.play(-1)

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
        if self.boss_time == True:
            self.boss_group.update(dt,self.ship)
        if not self.boss_vulnerable:
            currentboss_time = pygame.time.get_ticks()  
            if currentboss_time - self.boss_hit_time > 500:
                self.boss_vulnerable = True
        self.fire_collision()
        self.boss_collision()
        self.boss_laser_collision()
        self.boss_explosion_group.update(dt)
        self.explosion_group.update(dt)
        self.boss.fire_group.update(dt)
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()  
            if current_time - self.hit_time > 2000:
                self.vulnerable = True
        if self.boss_dead == True:
            self.ship.laser_group.empty()
            if self.boss_explosion.animation_done == True:
                self.boss.kill()
                self.boss_group.empty()
                boss_music.fadeout(1500)
                if pygame.time.get_ticks() - self.boss_explosion.boss_death_timer > 3000:
                    self.game.completed_levels += 1
                    lc1 = LevelComplete(self.game, self.score, self.health)
                    lc1.enter_state()

    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.ship.laser_group.draw(display_surface)
        self.spaceship_group.draw(display_surface)
        self.explosion_group.draw(display_surface)
        self.boss.fire_group.draw(display_surface)
        if self.boss_time == True: 
            self.boss_group.draw(display_surface)
            self.boss_explosion_group.draw(display_surface)
        self.display_score(display_surface)
        display_surface.blit(self.health_surf, self.health_rect)
        #health bar
        for i in range(self.health):
            display_surface.blit(*self.health_sprites[i])

    def boss_collision(self):
        for boss in self.boss_group:
            if pygame.sprite.collide_mask(self.ship, boss) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def fire_collision(self):
        for fire in self.boss.fire_group:
            if pygame.sprite.collide_mask(self.ship, fire) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    boss_music.stop()
                    self.ship.explosion_sound.play()
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def boss_laser_collision(self):
        for laser in self.ship.laser_group:
            for floppa in self.boss_group:
                if pygame.sprite.collide_mask(laser, floppa) and self.boss_vulnerable == True:
                    self.boss.health -= 1
                    self.takedamage.play()
                    laser.kill()
                    self.boss.damage_boss = True
                    self.boss_vulnerable = False
                    self.boss_hit_time = pygame.time.get_ticks()
                    if self.boss.health <= 0:
                        self.boss_dead = True
                        self.score += 10000
                        self.boss_explosion = BossExplosion(self.boss.rect.center)
                        self.boss_explosion_group.add(self.boss_explosion)
                        
    def display_score(self, display_surface):
        self.score += 1
        self.score_text = f'{self.score}'
        self.text_surf = self.font.render(f"SCORE: {self.score_text}", True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (1000, 50))
        display_surface.blit(self.text_surf,self.text_rect)

