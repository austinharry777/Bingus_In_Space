import pygame, constants as c, math
from random import randint, uniform, choice
from base_state import Base_State
from game_over import Game_Over
from resources import *
from math import sin 
from pause import Pause
from level4boss import Level4Boss
pygame.init()
pygame.mixer.init()

music = pygame.mixer.Sound('sounds/bingus level4.wav')
amoeba_explosion_sound = pygame.mixer.Sound('sounds/amoebaexplosion.wav')


class Level4(Base_State):
    def __init__(self, game, score, health):
        Base_State.__init__(self, game)
        self.game = game
        self.score = score
        self.health = health
        
        self.clock = pygame.time.Clock()
        self.background = Background4()
        self.foreground = Foreground4()
        #sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.amoeba_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        #sprite creation
        self.ship = Ship()
        self.spaceship_group.add(self.ship)
        #create meteor timer
        self.meteor_timer = pygame.time.get_ticks()
        self.meteor_spawn_time = 2500 #milliseconds
        #create amoeba timer
        self.amoeba_timer = pygame.time.get_ticks()
        self.amoeba_spawn_time = 2500 #milliseconds
        #explosion animation
        self.explosion_group = pygame.sprite.Group()
        self.amoeba_explosion_group = pygame.sprite.Group()
        #create powerup timer
        self.powerup_timer = pygame.time.get_ticks()
        self.powerup_spawn_time = 10000 #milliseconds
        #create powerup group
        self.powerup_group = pygame.sprite.Group()
        self.powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
        #Boss group
        self.boss_group = pygame.sprite.Group()
        self.boss2_group = pygame.sprite.Group()
        #self.boss2_group = pygame.sprite.Group()
        self.boss = Boss1()
        self.boss2 = Boss1Plus(self.ship)
        self.boss_group.add(self.boss)
        self.boss2_group.add(self.boss2)
        self.boss_time = False
        self.boss_timer = pygame.time.get_ticks()
        self.boss_spawn_time = 90000 # 90 seconds
        #boss invulnerability
        self.boss_vulnerable = True
        self.boss_hit_time = None
        self.boss2_vulnerable = True
        self.boss2_hit_time = None
        self.boss_time = False
        self.boss_time_timer = pygame.time.get_ticks()
        self.boss_time_delay = 3000
        self.boss_dead = False
        self.next_level_timer = pygame.time.get_ticks()
        self.next_level_delay = 3000
        self.next_level_bool = False
        # boss explosion
        self.boss_explosion_group = pygame.sprite.Group()
        #score text
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        #music and sounds
        music.play(-1)
        #invulnerability
        self.vulnerable = True
        self.hit_time = None
        self.takedamage = pygame.mixer.Sound('sounds/takedamage.wav')
        self.takedamage.set_volume(0.5)
        #game over timer and bool
        self.game_over_delay = 1000
        self.game_over = False
        self.game_over_timer = pygame.time.get_ticks()
        #health and bar
        self.health_sprites = []
        for i in range(1, 51):
            sprite = pygame.image.load(f'graphics/health_bar.png').convert_alpha()
            rect = sprite.get_rect(midbottom = (200 + i * 50, 710))
            self.health_sprites.append((sprite, rect))
        self.health_surf = self.font.render(f"HEALTH:", True, (255,255,255))
        self.health_rect = self.health_surf.get_rect(midbottom = (100, 710))
        self.confused_nick_group = pygame.sprite.Group()
        self.confused_nick = ConfusedNick()
        self.confused_nick_group.add(self.confused_nick)

    def update(self, dt, actions):
        if actions['enter'] == True:
            pause_menu = Pause(self.game)
            pause_menu.enter_state()
        if self.game_over == True and pygame.time.get_ticks() - self.game_over_timer > self.game_over_delay:
                pygame.mixer.stop()
                game_over = Game_Over(self.game)
                game_over.enter_state()
        self.laser_collision()
        if self.background.end_level == True:
            music.fadeout(1000)
            self.meteor_group.empty()
            if self.boss_group:
                self.boss_group.empty()
                self.boss.fire_group.empty()
                self.boss_explosion = BossExplosion(self.boss.rect.center)
                self.boss_explosion_group.add(self.boss_explosion)
            if self.boss2_group:
                self.boss2_group.empty()
                self.boss2.fire_group.empty()
                self.boss2_explosion = BossExplosion(self.boss2.rect.center)
                self.boss_explosion_group.add(self.boss2_explosion)
                self.boss2.homing_laser_group.empty()
            if self.boss_explosion.animation_done == True:
                level4boss = Level4Boss(self.game, self.score, self.health, self.explosion_group,
                self.boss_explosion_group, self.ship, self.background, self.foreground)
                level4boss.enter_state()

        if self.boss_time == True:
            self.meteor_spawn_time = 500000
            self.amoeba_spawn_time = 500000
            self.boss_group.update(dt, self.ship)
            self.boss2_group.update(dt, self.ship)
        if not self.boss_vulnerable:
            currentboss_time = pygame.time.get_ticks()  
            if currentboss_time - self.boss_hit_time > 500:
                self.boss_vulnerable = True
        if not self.boss2_vulnerable:
            currentboss2_time = pygame.time.get_ticks()  
            if currentboss2_time - self.boss2_hit_time > 500:
                self.boss2_vulnerable = True
        self.boss_collision()
        self.boss2_collision()
        self.boss_laser_collision()
        self.boss2_laser_collision()
        self.fire_collision()
        #self.fire2_collision()
        self.boss.fire_group.update(dt)
        #self.boss2.fire_group.update(dt)
        self.boss2.homing_laser_group.update(dt, self.ship)
            
        if pygame.time.get_ticks() - self.boss_timer > self.boss_spawn_time:
            self.boss_time = True
            
        if pygame.time.get_ticks() - self.meteor_timer > self.meteor_spawn_time:
            meteor_y_pos = randint(0, 720)
            meteor_x_pos = choice([-100, 1380])
            self.meteor = Meteor((meteor_x_pos, meteor_y_pos))
            self.meteor_group.add(self.meteor)
            self.meteor_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.amoeba_timer > self.amoeba_spawn_time:
            amoeba_y_pos = randint(-150, -100)
            amoeba_x_pos = randint(-100, 1380)
            self.amoeba = Amoeba2((amoeba_x_pos, amoeba_y_pos))
            self.amoeba_group.add(self.amoeba)
            self.amoeba_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.powerup_timer > self.powerup_spawn_time:
            powerup_y_pos = randint(-150,-50)
            powerup_x_pos = randint(200, c.WINDOW_WIDTH - 200)
            self.powerup = Powerup((powerup_x_pos, powerup_y_pos))
            self.powerup_group.add(self.powerup)
            self.powerup_spawn_time = 80000
            self.powerup_timer = pygame.time.get_ticks()
        self.powerup_group.update(dt)
        self.background.update(dt)
        self.confused_nick_group.update(dt)
        self.foreground.update(dt)
        self.ship.laser_group.update(dt)
        self.spaceship_group.update(dt, actions)
        self.meteor_group.update(dt,self.ship)
        self.amoeba_group.update(dt)
        self.meteor_collision()
        self.amoeba_collision()
        self.laser_amoeba_collision()
        self.powerup_collision()
        self.explosion_group.update(dt)
        self.amoeba_explosion_group.update(dt)
        self.boss_explosion_group.update(dt)
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()  
            if current_time - self.hit_time > 2000:
                self.vulnerable = True
       
    def draw(self, display_surface):
        self.background.draw(display_surface)
        self.confused_nick_group.draw(display_surface)
        self.meteor_group.draw(display_surface)
        self.amoeba_group.draw(display_surface)
        self.foreground.draw(display_surface)
        self.ship.laser_group.draw(display_surface)
        self.spaceship_group.draw(display_surface)
        self.explosion_group.draw(display_surface)
        self.amoeba_explosion_group.draw(display_surface)
        self.display_score(display_surface)
        if self.boss_time == True:
            self.boss_group.draw(display_surface)
            self.boss2_group.draw(display_surface)
            self.boss.fire_group.draw(display_surface)
            #self.boss2.fire_group.draw(display_surface)
            self.boss2.homing_laser_group.draw(display_surface)
            self.boss_explosion_group.draw(display_surface)
        display_surface.blit(self.health_surf, self.health_rect)
        for i in range(self.health):
            display_surface.blit(*self.health_sprites[i])
        self.powerup_group.draw(display_surface)
        
    def meteor_collision(self):
        for meteor in self.meteor_group:
            if pygame.sprite.collide_mask(self.ship, meteor) and self.vulnerable == True:
                amoeba_explosion_sound.play()
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

    def amoeba_collision(self):
        for amoeba in self.amoeba_group:
            if pygame.sprite.collide_mask(self.ship, amoeba) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                amoeba.kill()
                if self.health <= 0:
                    self.ship.kill()
                    self.amoeba_group.empty()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()
                
    def laser_collision(self): 
            for laser in self.ship.laser_group:
                for meteor in self.meteor_group:
                    if pygame.sprite.collide_mask(laser, meteor):
                        self.meteor.health -= 1
                        self.score += 1000
                        laser.kill()
                        if self.meteor.health <= 0:
                            meteor.kill()
                            self.amoeba_explosion = AmoebaExplosion(meteor.rect.center, (meteor.meteor_size.x * 1.2))
                            self.amoeba_explosion_group.add(self.amoeba_explosion)
                            amoeba_explosion_sound.play()
                            self.score += 5000
                        
    def laser_amoeba_collision(self):
        for laser in self.ship.laser_group:
            for amoeba in self.amoeba_group:
                if pygame.sprite.collide_mask(laser, amoeba):
                    laser.kill()

    def powerup_collision(self):
        for powerup in self.powerup_group:
            if pygame.sprite.collide_mask(self.ship, powerup):
                self.ship.shoot_delay = self.ship.shoot_delay / 2
                if self.ship.shoot_delay <= 100:
                    self.ship.shoot_delay = 100
                powerup.kill()
                self.powerup_sound.play()
                    
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
                    self.meteor_group.empty()
                    self.ship.explosion_sound.play()
                    self.explosion = Explosion(self.ship.rect.center, (self.ship.rect.width * 1.2))
                    self.explosion_group.add(self.explosion)
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def boss2_collision(self):
        for boss in self.boss2_group:
            if pygame.sprite.collide_mask(self.ship, boss) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.meteor_group.empty()
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
                    self.meteor_group.empty()
                    self.ship.explosion_sound.play()
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def fire2_collision(self):
        for fire in self.boss2.fire_group:
            if pygame.sprite.collide_mask(self.ship, fire) and self.vulnerable == True:
                self.ship.explosion_sound.play()
                self.ship.damage_ship = True
                self.health -= 1
                self.vulnerable = False
                self.hit_time = pygame.time.get_ticks()
                if self.health <= 0:
                    self.ship.kill()
                    self.meteor_group.empty()
                    self.ship.explosion_sound.play()
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()

    def boss_laser_collision(self):
        for laser in self.ship.laser_group:
            for floppa in self.boss_group:
                if pygame.sprite.collide_mask(laser, floppa) and self.boss_vulnerable == True:
                    self.takedamage.play()
                    self.boss.health -= 1
                    laser.kill()
                    self.boss.damage_boss = True
                    self.boss_vulnerable = False
                    self.boss_hit_time = pygame.time.get_ticks()
                    if self.boss.health <= 0:
                        self.score += 10000
                        self.boss_explosion = BossExplosion(floppa.rect.center)
                        self.boss_explosion_group.add(self.boss_explosion)
                        self.boss.kill()
                        self.boss_group.empty()
                        self.boss.fire_group.empty()

    def boss2_laser_collision(self):
        for laser in self.ship.laser_group:
            for floppa in self.boss2_group:
                if pygame.sprite.collide_mask(laser, floppa) and self.boss2_vulnerable == True:
                    self.takedamage.play()
                    self.boss2.health -= 1
                    laser.kill()
                    self.boss2.damage_boss = True
                    self.boss2_vulnerable = False
                    self.boss2_hit_time = pygame.time.get_ticks()
                    if self.boss2.health <= 0:
                        self.score += 10000
                        self.boss_explosion = BossExplosion(floppa.rect.center)
                        self.boss_explosion_group.add(self.boss_explosion)
                        self.boss2.kill()
                        self.boss2_group.empty()
                        self.boss2.homing_laser_group.empty()

    def homing_laser_collision(self):
        for laser in self.boss2.homing_laser_group:
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
                    music.stop() 
                    self.ship.explosion_sound.play()
                    self.game_over = True
                    self.game_over_timer = pygame.time.get_ticks()
                        
    def display_score(self, display_surface):
        self.score += 1
        self.score_text = f'{self.score}'
        self.text_surf = self.font.render(f"SCORE: {self.score_text}", True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (1000, 50))
        display_surface.blit(self.text_surf,self.text_rect)

    
class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 50
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        #self.scaled_image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = randint(90, 150)
        self.health = 2 
        
    def update(self, dt, ship):
        self.animate()
        if self.wave_value():
            if self.rect.centerx > ship.rect.centerx + 10:
                self.direction.x = -1
            if self.rect.centerx < ship.rect.centerx - 10:
                self.direction.x = 1
            if self.rect.centery > ship.rect.centery + 10:
                self.direction.y = -1
            if self.rect.centery < ship.rect.centery - 10:
                self.direction.y = 1
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
            
            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()
            
            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)  

    def wave_value(self):
        value = sin(((pygame.time.get_ticks() / 1000) + 8) * 1.1 * math.pi)
        if value >= 0:
            return True
        else:
            return False
        
    def load_animation(self):
        self.meteor_size = pygame.math.Vector2(100) * uniform(0.5, 1.5)
        for i in range(0, 6):
            frames = (pygame.image.load(f'graphics/amoeba/{i}.png').convert_alpha())
            self.scaled_surf = pygame.transform.scale(frames, self.meteor_size)
            new_frames = self.scaled_surf
            self.animation_frames.append(new_frames)

        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

class Amoeba2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 50
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(200, 400)
        
    def update(self, dt):
        self.animate()
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize()
         
        if self.rect.top > c.WINDOW_HEIGHT:
            self.kill() 

    def load_animation(self):
        self.meteor_size = pygame.math.Vector2(100) * uniform(0.5, 1.5)
        for i in range(0, 7):
            frames = (pygame.image.load(f'graphics/amoeba2/{i}.png').convert_alpha())
            self.scaled_surf = pygame.transform.scale(frames, self.meteor_size)
            new_frames = self.scaled_surf
            self.animation_frames.append(new_frames)

        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()


class Foreground4:
    def __init__(self):
        self.background_surf2 = pygame.image.load('graphics/insidefloppa.png').convert_alpha()
        self.background_surf2_height = self.background_surf2.get_height()
        self.scroll2 = 0
        self.scroll_timer = pygame.time.get_ticks()
        self.scroll_speed2 = 70

    def update(self, dt):
         self.scroll2 += self.scroll_speed2 * dt
         if self.scroll2 >= self.background_surf2_height - c.WINDOW_HEIGHT:
            self.scroll_speed2 = 0

    def draw(self, display_surface):
        display_surface.blit(self.background_surf2, (0, -10800 + self.scroll2))


class Background4:
    def __init__(self):  
        self.background_surf = pygame.image.load('graphics/insidefloppa2.png').convert()
        self.background_surf_height = self.background_surf.get_height()
        self.scroll = 0
        self.scroll_timer = pygame.time.get_ticks()
        self.scroll_speed = 33
        self.end_level = False
        
    def update(self, dt):
        self.scroll += self.scroll_speed * dt
        if self.scroll >= self.background_surf_height - c.WINDOW_HEIGHT:
            self.scroll_speed = 0
            self.end_level = True
        return self.end_level
        
    def draw(self, display_surface):
        display_surface.fill(c.BLACK)
        display_surface.blit(self.background_surf, (0, -5040 + self.scroll))

class ConfusedNick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/confusednick.png').convert_alpha()
        self.rect = self.image.get_rect(center = (c.WINDOW_WIDTH + 320, c.WINDOW_HEIGHT / 2 -100))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 100
        self.nick_timer = pygame.time.get_ticks()
        self.nick_delay = 90000 #90 seconds
        self.nick_withdraw_delay = 105000 #15 seconds
        self.nick_time = False #timer for nick to leave

        
    def update(self, dt):
        if self.nick_time == True:
            self.direction = pygame.math.Vector2(1, 0)
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
            if self.rect.left > c.WINDOW_WIDTH:
                self.kill()
        else:
            if pygame.time.get_ticks() - self.nick_timer > self.nick_withdraw_delay:
                self.nick_time = True
            elif self.rect.right < c.WINDOW_WIDTH:
                self.direction = (0, 0)

            else:
                if pygame.time.get_ticks() - self.nick_timer > self.nick_delay:
                    self.direction = pygame.math.Vector2(-1, 0)
                    self.pos += self.direction * self.speed * dt
                    self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        
    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)
            
        









