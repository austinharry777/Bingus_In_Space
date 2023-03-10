import pygame, constants as c, math
from random import randint, uniform
from base_state import Base_State
from game_over import Game_Over
from level2boss import Level2Boss
from pause import Pause
from resources import *
pygame.mixer.init()
pygame.init()

music = pygame.mixer.Sound('sounds/bingus level2.wav')
music.set_volume(0.9)


class Level2(Base_State):
    def __init__(self, game, score, health):
        Base_State.__init__(self, game)
        self.game = game
        self.health = health
        self.clock = pygame.time.Clock()
        self.background = Background2()
        #sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        #self.laser_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        #sprite creation
        self.ship = Ship()
        self.spaceship_group.add(self.ship)
        #create meteor timer
        self.meteor_timer = pygame.time.get_ticks()
        self.meteor_spawn_time = 300 #milliseconds
        #create powerup timer
        self.powerup_timer = pygame.time.get_ticks()
        self.powerup_spawn_time = 10000 #milliseconds
        #create powerup group
        self.powerup_group = pygame.sprite.Group()
        self.powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
        #explosion animation
        self.explosion_group = pygame.sprite.Group()
        #score text
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        self.score = score
        #self.score = 0
        #music and sounds
        music.play(-1)
        #damage animation and invulnerability
        self.vulnerable = True
        self.hit_time = None
        #game over timer and bool
        self.game_over_delay = 1000
        self.game_over = False
        self.game_over_timer = pygame.time.get_ticks()
        #level progression counter
        self.dead_floppas = 0 # destroy 30 floppas to progress to next level
        #health and bar
        self.health_sprites = []
        for i in range(1, 51):
            sprite = pygame.image.load(f'graphics/health_bar.png').convert_alpha()
            rect = sprite.get_rect(midbottom = (200 + i * 50, 710))
            self.health_sprites.append((sprite, rect))
        self.health_surf = self.font.render(f"HEALTH:", True, (255,255,255))
        self.health_rect = self.health_surf.get_rect(midbottom = (100, 710))
        
    def update(self, dt, actions):
        if actions['enter'] == True:
            pause_menu = Pause(self.game)
            pause_menu.enter_state()
        if self.game_over == True and pygame.time.get_ticks() - self.game_over_timer > self.game_over_delay:
                music.stop()
                self.score_text = f'{0}'
                game_over = Game_Over(self.game)
                game_over.enter_state()
        self.laser_collision()
        self.background.update(dt)
        self.ship.laser_group.update(dt)
        self.spaceship_group.update(dt, actions)
        if pygame.time.get_ticks() - self.meteor_timer > self.meteor_spawn_time:
            meteor_y_pos = randint(-150,-50)
            meteor_x_pos = randint(-600, c.WINDOW_WIDTH + 600)
            self.meteor = Meteor((meteor_x_pos, meteor_y_pos))
            self.meteor_group.add(self.meteor)
            self.meteor_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.powerup_timer > self.powerup_spawn_time:
            powerup_y_pos = randint(-150,-50)
            powerup_x_pos = randint(200, c.WINDOW_WIDTH - 200)
            self.powerup = Powerup((powerup_x_pos, powerup_y_pos))
            self.powerup_group.add(self.powerup)
            self.powerup_spawn_time = 100000
            self.powerup_timer = pygame.time.get_ticks()
        self.powerup_group.update(dt)
        self.meteor_group.update(dt)
        self.meteor_collision()
        self.powerup_collision()
        self.explosion_group.update(dt)
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()  
            if current_time - self.hit_time > 2000:
                self.vulnerable = True
        
    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.ship.laser_group.draw(display_surface)
        self.meteor_group.draw(display_surface)
        self.powerup_group.draw(display_surface)
        self.spaceship_group.draw(display_surface)
        self.explosion_group.draw(display_surface)
        self.display_score(display_surface)
        self.floppa_counter(display_surface)
        display_surface.blit(self.health_surf, self.health_rect)
        for i in range(self.health):
            display_surface.blit(*self.health_sprites[i])
            
    def meteor_collision(self):
        for meteor in self.meteor_group:
            if pygame.sprite.collide_mask(self.ship, meteor) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                meteor.kill()
                if self.health <= 0:
                    self.ship.kill()
                    self.meteor_group.empty()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()
                
    def laser_collision(self):
        if self.dead_floppas >= 30:
            for meteor in self.meteor_group:
                self.explosion = Explosion(meteor.rect.center, (meteor.meteor_size.x * 1.2))
                self.explosion_group.add(self.explosion)
            music.fadeout(2000)
            self.meteor_spawn_time = 300000
            level2boss = Level2Boss(self.game, self.score, self.health, self.explosion_group, self.ship, self.background)
            level2boss.enter_state()
            
        else:
            for laser in self.ship.laser_group:
                for meteor in self.meteor_group:
                    if pygame.sprite.collide_mask(laser, meteor):
                        self.score += 1000
                        self.dead_floppas += 1
                        meteor.kill()
                        self.explosion = Explosion(meteor.rect.center, (meteor.meteor_size.x * 1.2))
                        self.explosion_group.add(self.explosion)
                        laser.kill()
                        self.ship.explosion_sound.play()

    def powerup_collision(self):
        for powerup in self.powerup_group:
            if pygame.sprite.collide_mask(self.ship, powerup):
                self.ship.shoot_delay = self.ship.shoot_delay / 2
                if self.ship.shoot_delay <= 100:
                    self.ship.shoot_delay = 100
                powerup.kill()
                self.powerup_sound.play()

    def display_score(self, display_surface):
        self.score += 1
        self.score_text = f'{self.score}'
        self.text_surf = self.font.render(f"SCORE: {self.score_text}", True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (1000, 50))
        display_surface.blit(self.text_surf,self.text_rect)

    def floppa_counter(self, display_surface):
        self.floppa_surf = self.font.render(f"BLIMPS REMAINING: {30 - self.dead_floppas}", True, (255,255,255))
        self.floppa_rect = self.floppa_surf.get_rect(midbottom = (300, 50))
        display_surface.blit(self.floppa_surf,self.floppa_rect)
        
    
class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #randomize meteor size
        meteor_surf = pygame.image.load('graphics/floppablimp.png').convert_alpha()
        self.meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf, self.meteor_size)
        self.image = self.scaled_surf
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.8, 0.8), 1)
        self.speed = randint(500,700)
        # rotation logic
        self.rotation = 0
        self.rotation_speed = randint(-100, 100)

    def rotate(self,dt):
        self.rotation += self.rotation_speed * dt
        rotate_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation,1)
        self.image = rotate_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        if self.direction.x > 0:
            self.image = self.flipped_image
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        #self.rotate(dt)  
        if self.rect.top > c.WINDOW_HEIGHT + 300:
            self.kill() 


class Background2:
    def __init__(self):  
        self.background_surf = pygame.image.load('graphics/sky.png').convert()
        self.background_surf_height = self.background_surf.get_height()
        self.background_surf2 = pygame.image.load('graphics/clouds.png').convert_alpha()
        self.background_surf2_height = self.background_surf2.get_height()
        self.scroll = 0
        self.scroll2 = 0
        self.tiles = math.ceil(c.WINDOW_HEIGHT / self.background_surf_height) + 1
        self.tiles2 = math.ceil(c.WINDOW_HEIGHT / self.background_surf2_height) + 1
        self.scroll_timer = pygame.time.get_ticks()
        self.scroll_speed = 50
        self.scroll_speed2 = 100
        
    def update(self, dt):
        self.scroll += self.scroll_speed * dt
        self.scroll2 += self.scroll_speed2 * dt
        if self.scroll >= self.background_surf_height:
            self.scroll = 0
        if self.scroll2 >= self.background_surf2_height:
            self.scroll2 = 0

    def draw(self, display_surface):
        if self.scroll_speed >= 2000:
            self.scroll_speed = 2000
            self.scroll_speed2 = 3000
        else:    
            for i in range(-1, self.tiles):
                display_surface.blit(self.background_surf, (0, i * self.background_surf_height + self.scroll))
            for i in range(-2, self.tiles2):    
                display_surface.blit(self.background_surf2, (0, i * self.background_surf2_height + self.scroll2))
        
        if pygame.time.get_ticks() - self.scroll_timer >= 10000:
            self.scroll_speed += 75
            self.scroll_speed2 += 112.5 
            self.scroll_timer = pygame.time.get_ticks()




