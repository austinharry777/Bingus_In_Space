import pygame
from base_state import Base_State
from game_over import Game_Over
from level_complete3 import LevelComplete3
from pause import Pause
from resources import *

pygame.init()
pygame.mixer.init()

boss_music = pygame.mixer.Sound('sounds/boss3.wav')
boss_music.set_volume(0.7)


class Level3Boss(Base_State):
    def __init__(self, game, score, health, explosion_group, ship, background):
        Base_State.__init__(self, game)
        self.game = game
        self.score = score
        self.health = health
        self.ship = ship
        self.background = background
        #boss_music.play()
        self.clock = pygame.time.Clock()
        #sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        #sprite creation
        self.spaceship_group.add(self.ship)
        #explosion animation
        self.explosion_group = explosion_group
        self.boss_explosion_group = pygame.sprite.GroupSingle()
        #Boss group and hitbox
        self.boss = Boss3(self.ship)
        self.boss_group = pygame.sprite.Group()
        self.boss_group.add(self.boss)
        self.hitbox = BossHitbox(self.ship, self.boss)
        self.hitbox_group = pygame.sprite.GroupSingle()
        self.hitbox_group.add(self.hitbox)
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
            self.hitbox_group.update(dt, self.ship, self.boss)
            self.boss_group.update(dt, self.ship)
        if not self.boss_vulnerable:
            currentboss_time = pygame.time.get_ticks()  
            if currentboss_time - self.boss_hit_time > 500:
                self.boss_vulnerable = True
        self.homing_laser_collision()
        self.big_laser_collision()
        self.longlaser_collision()
        self.boss_collision()
        self.boss_laser_collision()
        self.bullet_collision()
        self.boss_explosion_group.update(dt)
        self.explosion_group.update(dt)
        self.boss.explosion_group.update(dt)
        self.boss.longlaser_group.update(dt)
        self.boss.bullet_group.update(dt)
        self.boss.biglaser_group.update(dt) 
        self.boss.homing_laser_group.update(dt,self.ship)
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()  
            if current_time - self.hit_time > 2000:
                self.vulnerable = True
        if self.boss_dead == True:
            self.ship.laser_group.empty()
            if self.boss_explosion.animation_done == True:
                self.boss.kill()
                self.boss_group.empty()
                boss_music.stop()
                if pygame.time.get_ticks() - self.boss_explosion.boss_death_timer > 3000:
                    self.game.completed_levels += 1
                    lc3 = LevelComplete3(self.game, self.score, self.health)
                    lc3.enter_state()
        
    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.ship.laser_group.draw(display_surface)
        self.spaceship_group.draw(display_surface)
        self.explosion_group.draw(display_surface)
        self.boss.longlaser_group.draw(display_surface)
        self.boss.biglaser_group.draw(display_surface)
        self.boss.explosion_group.draw(display_surface)
        if self.boss_time == True: 
            self.hitbox_group.draw(display_surface)
            self.boss_group.draw(display_surface)
            self.boss_explosion_group.draw(display_surface)
            self.boss.homing_laser_group.draw(display_surface)
            self.boss.bullet_group.draw(display_surface)
        self.display_score(display_surface)
        display_surface.blit(self.health_surf, self.health_rect)
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

    def longlaser_collision(self):
        for laser in self.boss.longlaser_group:
            if pygame.sprite.collide_mask(self.ship, laser) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                self.explosion_group.add(self.explosion)
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
    
    def bullet_collision(self):
        for bullet in self.boss.bullet_group:
            if pygame.sprite.collide_mask(self.ship, bullet) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                self.explosion_group.add(self.explosion)
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
        if self.boss.health <= 20:
            for laser in self.ship.laser_group:
                if pygame.sprite.collide_mask(laser, self.hitbox) and self.boss_vulnerable == True:
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
        else:
            for laser in self.ship.laser_group:
                for floppa in self.boss_group:
                    if pygame.sprite.collide_mask(laser, floppa) and self.boss_vulnerable == True:
                        self.boss.health -= 1
                        self.takedamage.play()
                        laser.kill()
                        self.boss.damage_boss = True
                        self.boss_vulnerable = False
                        self.boss_hit_time = pygame.time.get_ticks()
                        
    def big_laser_collision(self):
        for laser in self.boss.biglaser_group:
            if pygame.sprite.collide_mask(self.ship, laser) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                self.explosion_group.add(self.explosion)
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

    def homing_laser_collision(self):
        for laser in self.boss.homing_laser_group:
            if pygame.sprite.collide_mask(self.ship, laser) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                self.explosion_group.add(self.explosion)
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

    def display_score(self, display_surface):
        self.score += 1
        self.score_text = f'{self.score}'
        self.text_surf = self.font.render(f"SCORE: {self.score_text}", True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (1000, 50))
        display_surface.blit(self.text_surf,self.text_rect)


