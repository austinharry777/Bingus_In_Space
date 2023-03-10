import pygame, sys, os, random, math, time, json
import constants as c
from pygame import mixer
from pygame.math import Vector2 as vec
from random import randint, uniform
from math import sin 

explosion_sound = pygame.mixer.Sound('sounds/explosion2.wav')
explosion_sound.set_volume(0.5)


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        self.load_animation()
        self.frame_index = 0
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(center = (c.WINDOW_WIDTH/2, c.WINDOW_HEIGHT/2))
        original_center = self.rect.center
        # make ship hitbox smaller
        self.scaled_image = pygame.image.load('graphics/shiphitbox.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.scaled_image)
        #align hitbox to center of ship
        self.rect.center = original_center
        self.rect = self.scaled_image.get_rect(center = original_center)
        self.can_shoot = True
        self.shoot_time = None 
        self.shoot_delay = 500
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion2.wav')
        self.explosion_sound.set_volume(0.3)
        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.laser_sound.set_volume(0.35)
        self.laser_group = pygame.sprite.Group()
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,0)
        self.speed = 500
        self.damage_ship = False
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.shoot_delay:
                self.can_shoot = True   
    
    def update(self, dt, actions):
        self.laser_timer()
        self.laser_shoot(actions)
        self.damage_animate()
        
        #player input
        if actions['left']:
            self.direction.x = -1
        elif actions['right']:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if actions['up']:
            self.direction.y = -1
        elif actions['down']:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize()
        #update the position
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt
        if self.direction == 0:
            self.pos.x += 0
            self.pos.y += 0
        self.rect.center = self.pos
        #screen wrap
        if self.pos.x < 45:
            self.pos.x = 45
        if self.pos.x > c.WINDOW_WIDTH - 45:
            self.pos.x = c.WINDOW_WIDTH - 45
        if self.pos.y < 37:
            self.pos.y = 37
        if self.pos.y > c.WINDOW_HEIGHT - 37:
            self.pos.y = c.WINDOW_HEIGHT - 37

    def laser_shoot(self, actions):
        if actions['left_mouse'] and self.can_shoot or pygame.key.get_pressed()[pygame.K_SPACE] and self.can_shoot:
                self.laser_sound_timer = pygame.time.get_ticks()
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                self.laser = Laser((self.rect.midtop[0]+12, self.rect.midtop[1]))
                self.laser_group.add(self.laser)
                self.laser_sound.play()

    def load_animation(self):
        for i in range(0, 6):
            frames = (pygame.image.load(f'graphics/ship_damage/{i}.png').convert_alpha())
            self.animation_frames.append(frames)

        self.image = self.animation_frames[0]

    def damage_animate(self):
       if self.damage_ship:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.animation_frames[0]
                    self.frame_index = 0
                    self.damage_ship = False
                    
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600
        
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()


class Powerup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/powerup.png')
        self.rect = self.image.get_rect(center = pos)
        # make the powerup hitbox bigger
        self.scale_factor = 2
        self.scaled_image = pygame.transform.scale(self.image, (int(self.rect.width * self.scale_factor), int(self.rect.height * self.scale_factor)))
        self.rect = self.scaled_image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.scaled_image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, 1)
        self.speed = 200

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = round(self.pos.x), round(self.pos.y)
        if self.rect.top > c.WINDOW_HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.animation_frames = []
        self.load_animation()
        self.rect = self.image.get_rect(center = pos)
        self.frame_index = 0
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 50
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        #self.scaled_image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def load_animation(self):
        for i in range(0, 8):
            frames = (pygame.image.load(f'graphics/explosion/{i}.png').convert_alpha())
            scaled_frames = pygame.transform.scale(frames, (self.size, self.size))
            self.animation_frames.append(scaled_frames)

        self.image = self.animation_frames[0]
            
    def update(self, dt):
        self.animate()
        
    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.kill()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)


class AmoebaExplosion(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.size = size
        self.animation_frames = []
        self.load_animation()
        self.rect = self.image.get_rect(center = pos)
        self.frame_index = 0
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 50
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        #self.scaled_image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def load_animation(self):
        for i in range(0, 9):
            frames = (pygame.image.load(f'graphics/amoebaexplosion/{i}.png').convert_alpha())
            scaled_frames = pygame.transform.scale(frames, (self.size, self.size))
            self.animation_frames.append(scaled_frames)

        self.image = self.animation_frames[0]
            
    def update(self, dt):
        self.animate()
        
    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.kill()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)


#BOSSES

class Boss1(pygame.sprite.Sprite): #Jetpack floppa version 1 
    def __init__(self):
        super().__init__()
        self.animation_frames = []
        self.flipped_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(center = (400, -200))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None 
        self.health = 20 
        self.fire_sound = pygame.mixer.Sound('sounds/fire.wav')
        self.fire_sound.set_volume(0.6)
        self.fire_group = pygame.sprite.Group()
       
        
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,1)
        self.speed = 400
        self.damage_boss = False
        self.fire_interval = 1000
        #health
        self.health = 25
        
    def load_animation(self):
        for i in range(0,4):
            frames = (pygame.image.load(f'graphics/floppaboss1/{i}.png').convert_alpha())
            flipped_frames = pygame.transform.flip(frames, True, False)
            self.animation_frames.append(frames)
            self.flipped_frames.append(flipped_frames)

        self.image = self.animation_frames[self.frame_index]
        
    
    def fire_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.fire_interval:
                self.can_shoot = True   
    
    def update(self, dt, ship):
        self.fire_timer()
        self.damage_animate()
        self.fire_shoot()

        if self.health <= 0:
            self.speed = 0
            self.fire_interval = 300000
            self.image = self.animation_frames[0]

        else:
            #boss logic
            if self.health <= 10:
                self.speed = 150
                self.fire_interval = 2000
                if self.rect.centerx > ship.rect.centerx + 10:
                    self.direction.x = -1
                if self.rect.centerx < ship.rect.centerx - 10:
                    self.direction.x = 1
                if self.rect.centery > ship.rect.centery + 10:
                    self.direction.y = -1
                if self.rect.centery < ship.rect.centery - 10:
                    self.direction.y = 1
            else:
            
                if self.rect.top >= 50:
                    self.direction.y = 0 
                if self.rect.right >= c.WINDOW_WIDTH - 20 or self.rect.left <= 20: 
                    self.direction.x *= -1
            
            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()
            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)
            
            #adjust image based on direction
            if self.direction.x > 0:
                self.image = self.flipped_frames[self.frame_index]
            else:
                self.image = self.animation_frames[self.frame_index]

    def damage_animate(self):
       if self.damage_boss:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.animation_frames[self.frame_index]
                    self.frame_index = 0
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                    
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

    def fire_shoot(self):
        if self.can_shoot:
                
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                self.fire = BossFire(self.rect.midbottom)
                self.fire_group.add(self.fire)
                self.fire_sound.play()


class Boss1Plus(pygame.sprite.Sprite): #Jetpack floppa version 2 with homing lasers
    def __init__(self, ship):
        super().__init__()
        self.animation_frames = []
        self.flipped_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(center = (400, -200))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None 
        self.can_shoot3 = True
        self.shoot_time3 = None
        self.health = 20 
        self.fire_sound = pygame.mixer.Sound('sounds/fire.wav')
        self.fire_sound.set_volume(0.6)
        self.laser_sound = pygame.mixer.Sound('sounds/bombthrow.wav')
        self.laser_sound.set_volume(0.6)
        self.fire_group = pygame.sprite.Group()
        self.homing_laser_group = pygame.sprite.Group()
        self.homing_laser_interval = 5 #milliseconds
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(-1,1)
        self.speed = 400
        self.damage_boss = False
        self.fire_interval = 2750
        #health
        self.health = 20
        self.ship = ship
        
    def load_animation(self):
        for i in range(0,4):
            frames = (pygame.image.load(f'graphics/floppaboss1/{i}.png').convert_alpha())
            flipped_frames = pygame.transform.flip(frames, True, False)
            self.animation_frames.append(frames)
            self.flipped_frames.append(flipped_frames)

        self.image = self.animation_frames[self.frame_index]
        
    
    def fire_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.fire_interval:
                self.can_shoot = True   
    
    def update(self, dt, ship):
        self.fire_timer()
        self.damage_animate()
        self.fire_shoot()
        self.homing_laser_shoot()
        self.homing_laser_timer()

        if self.health <= 0:
            self.speed = 0
            self.fire_interval = 300000
            self.image = self.animation_frames[0]

        else:
            #boss logic
            if self.health <= 10:
                self.speed = 150
                self.fire_interval = 2000
                if self.rect.centerx > ship.rect.centerx + 10:
                    self.direction.x = -1
                if self.rect.centerx < ship.rect.centerx - 10:
                    self.direction.x = 1
                if self.rect.centery > ship.rect.centery + 10:
                    self.direction.y = -1
                if self.rect.centery < ship.rect.centery - 10:
                    self.direction.y = 1
            else:
            
                if self.rect.top >= 50:
                    self.direction.y = 0 
                if self.rect.right >= c.WINDOW_WIDTH - 20 or self.rect.left <= 20: 
                    self.direction.x *= -1
            
            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()
            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)
            
            #adjust image based on direction
            if self.direction.x > 0:
                self.image = self.flipped_frames[self.frame_index]
            else:
                self.image = self.animation_frames[self.frame_index]

    def damage_animate(self):
       if self.damage_boss:
            
            #self.health -= 1
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.animation_frames[self.frame_index]
                    self.frame_index = 0
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                    
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

    def fire_shoot(self):
        if self.can_shoot:
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                self.fire = BossFire(self.rect.midbottom)
                self.fire_group.add(self.fire)
                self.fire_sound.play()

    def homing_laser_shoot(self):
        if self.can_shoot3 and self.wave_value():
            self.can_shoot3 = False
            self.shoot_time3 = pygame.time.get_ticks()
            self.homing_laser = Boss1HomingLaser((self.rect.midtop[0], self.rect.midtop[1] + 70), self.ship)
            if self.direction.x > 0:
                self.homing_laser.direction.x = 1
            else:
                self.homing_laser.direction.x = -1
            self.homing_laser_group.add(self.homing_laser)
            self.laser_sound.play()

    def homing_laser_timer(self):
        if not self.can_shoot3:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time3 > self.homing_laser_interval:
                self.can_shoot3 = True

    def wave_value(self):
        value = sin(((pygame.time.get_ticks() / 1000) + 8) * 1.4 * math.pi)
        if value >= 0:
            return True
        return False

class Boss1HomingLaser(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        self.image = pygame.image.load('graphics/boss3homing.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 700
        self.homing_timer = pygame.time.get_ticks()
        self.homing_delay = 400
        self.following_timer = pygame.time.get_ticks()
        self.following_delay = 420
        self.homing_state = True 
        self.direction = pygame.math.Vector2(0,0)
         
    def update(self, dt, ship):
        if self.homing_state == False:
            self.pos += self.direction * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
        else:
            if pygame.time.get_ticks() - self.homing_timer > self.homing_delay:
                self.speed = 700
                self.direction = pygame.math.Vector2(ship.rect.center) - pygame.math.Vector2(self.rect.center)

                if pygame.time.get_ticks() - self.following_timer > self.following_delay:
                    self.homing_state = False
                    
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720 or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class BossFire(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100
        self.animation_length = len(self.animation_frames) - 1
        #self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        #self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,1)
        self.speed = 400

    def update(self, dt):
            self.animate()
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
            if self.rect.top > 720:
                self.kill()
            

    def load_animation(self):
        for i in range(3):
            frames = (pygame.image.load(f'graphics/bossfire/{i}.png').convert_alpha())
            scaled_frames = pygame.transform.scale2x(frames)
            self.animation_frames.append(scaled_frames)

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


class Boss2(pygame.sprite.Sprite): #Hot air balloon floppa
    def __init__(self, ship):
        super().__init__()
        self.animation_frames = []
        self.damage_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 75
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(center = (400, -400))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None 
        self.health = 20 
        self.bomb_sound = pygame.mixer.Sound('sounds/bombthrow.wav')
        self.bomb_sound.set_volume(0.6)
        self.bomb_group = pygame.sprite.Group()
        self.ship = ship
        

    #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,1)
        self.speed = 100
        self.damage_boss = False
        self.bomb_interval = 1000 #ms
        #health
        self.health = 50
        
    def load_animation(self):
        for i in range(0,5):
            frames = (pygame.image.load(f'graphics/hotairfloppa/{i}.png').convert_alpha())
            # flipped_frames = pygame.transform.flip(frames, True, False)
            self.animation_frames.append(frames)
            # self.flipped_frames.append(flipped_frames)

        for i in range(0,4):
            frames = (pygame.image.load(f'graphics/hotairfloppadamage/{i}.png').convert_alpha())
            # flipped_frames = pygame.transform.flip(frames, True, False)
            self.damage_frames.append(frames)
            # self.flipped_damage_frames.append(flipped_frames)

        self.image = self.animation_frames[self.frame_index]
        
    
    def bomb_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.bomb_interval:
                self.can_shoot = True   
    
    def update(self, dt, ship):
        self.bomb_timer()
        self.animate()
        self.bomb_shoot()

        if self.health <= 0:
            self.speed = 0
            self.bomb_interval = 300000
            self.image = self.animation_frames[0]
        else:
        
            #boss logic
            if self.health <= 20:
                
                self.speed = 150
                self.bomb_interval = 1500
                if self.rect.centerx > ship.rect.centerx + 10:
                    self.direction.x = -1
                if self.rect.centerx < ship.rect.centerx - 10:
                    self.direction.x = 1
                if self.rect.centery > ship.rect.centery + 10:
                    self.direction.y = -1
                if self.rect.centery < ship.rect.centery - 10:
                    self.direction.y = 1
            else:
            
                if self.rect.top >= -20:
                    self.direction.y = 0 
                if self.rect.right >= c.WINDOW_WIDTH - 20 or self.rect.left <= 20: 
                    self.direction.x *= -1
            
            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()
            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)
            
    def animate(self):
        if self.damage_boss:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.animation_frames[self.frame_index]
                    self.frame_index = 0
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.damage_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

        elif not self.damage_boss:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.frame_index = 0
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

    def bomb_shoot(self):
        if self.can_shoot:
                
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()
                self.bomb = BombThrow((self.rect.center[0]- 10, self.rect.center[1] + 115), self.ship)
                self.bomb_group.add(self.bomb)
                self.bomb_sound.play()

class BombThrow(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        bomb_surf = pygame.image.load('graphics/bomb.png').convert_alpha()
        self.bomb_size = pygame.math.Vector2(bomb_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(bomb_surf, self.bomb_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 600
        self.direction = pygame.math.Vector2(ship.rect.center) - pygame.math.Vector2(self.rect.center)
        # rotation logic
        self.rotation = 0
        self.rotation_speed = randint(-300, 300)
    
    def update(self, dt):
        
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720 or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rotate(dt)
        
    def rotate(self,dt):
        self.rotation += self.rotation_speed * dt
        rotate_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation,1)
        self.image = rotate_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


class Boss3(pygame.sprite.Sprite): # floppa ship 
    def __init__(self, ship):
        super().__init__()
        self.animation_frames = []
        self.damage_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 75
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(center = (400, -400))
        self.mask = pygame.mask.from_surface(self.image)
        self.ship = ship
        self.can_shoot = True
        self.shoot_time = None 
        self.can_shoot2 = True
        self.shoot_time2 = None
        self.can_shootbig = True
        self.shoot_timebig = None
        self.can_shoot3 = True
        self.shoot_time3 = None 
        self.laser_sound = pygame.mixer.Sound('sounds/bombthrow.wav')
        self.laser_sound.set_volume(0.6)
        self.longlaser_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.biglaser_group = pygame.sprite.Group()
        self.homing_laser_group = pygame.sprite.Group()
        self.phase_2 = False
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,1)
        self.speed = 300
        self.damage_boss = False
        self.laser_interval = 1000 #ms
        self.biglaser_interval = 1500 #ms
        self.hominglaser_interval = 5 #ms
        #health
        self.health = 50
        self.explosion_not_happened = True
        
    def load_animation(self):
        for i in range(0,4):
            frames = (pygame.image.load(f'graphics/boss3/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
            
        for i in range(0,4):
            frames = (pygame.image.load(f'graphics/boss3damaged/{i}.png').convert_alpha())
            self.damage_frames.append(frames)
           
        self.image = self.animation_frames[self.frame_index]
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.laser_interval:
                self.can_shoot = True  

    def bullet_timer(self):
        if not self.can_shoot2:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time2 > self.laser_interval * 1.5:
                self.can_shoot2 = True 

    def biglaser_timer(self):
        if not self.can_shootbig:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_timebig > self.biglaser_interval:
                self.can_shootbig = True

    def homing_laser_timer(self):
        if not self.can_shoot3:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time3 > self.hominglaser_interval:
                self.can_shoot3 = True

    def wave_value(self):
        value = sin(((pygame.time.get_ticks() / 1000) + 5) * 1.4 * math.pi)
        if value >= 0:
            return True
        return False

    def update(self, dt, ship):
        self.animate()
        self.laser_timer()
        self.laser_shoot()
        self.bullet_shoot()
        self.bullet_timer()
        self.big_laser_shoot()
        self.biglaser_timer()
        self.homing_laser_shoot()
        self.homing_laser_timer()
       
        if self.health <= 0:
            self.speed = 0
            self.laser_interval = 300000
            self.image = self.damage_frames[0]
        else:
            #boss logic
            if self.health <= 20:
                if self.explosion_not_happened:
                    self.explosion_not_happened = False
                    self.explosion1 = Explosion(self.rect.midbottom, 200)
                    self.explosion2 = Explosion(self.rect.bottomleft, 200)
                    self.explosion3 = Explosion(self.rect.bottomright , 200)
                    self.explosion_group.add(self.explosion1, self.explosion2, self.explosion3)
                    explosion_sound.play()
                    
                self.phase_2 = True
                self.speed = 150
                self.hitbox_speed = 150
                self.laser_interval = 1500
                if self.rect.centerx > ship.rect.centerx + 10:
                    self.direction.x = -1
                if self.rect.centerx < ship.rect.centerx - 10:
                    self.direction.x = 1
                self.direction.y = 0 

            else:
            
                if self.rect.top >= -20:
                    self.direction.y = 0 
                if self.rect.right >= c.WINDOW_WIDTH - 20 or self.rect.left <= 20: 
                    self.direction.x *= -1

            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()

            #update the position
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)

    def animate(self):
        if self.damage_boss and self.phase_2 == False:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.animation_frames[self.frame_index]
                    self.frame_index = 0
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

        elif not self.damage_boss and self.phase_2 == False:
            self.image = self.animation_frames[0]
            
        elif self.damage_boss and self.phase_2 == True:    
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.damage_frames[self.frame_index]
                    self.frame_index = 0
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.damage_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

        elif not self.damage_boss and self.phase_2 == True:
            self.image = self.damage_frames[0]

    def laser_shoot(self):
        if self.can_shoot and self.phase_2 == False:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.longlaser = LongLaser(self.rect.bottomright, self.ship)
            self.longlaser_group.add(self.longlaser)
            self.laser_sound.play()

    def bullet_shoot(self):
        if self.can_shoot2 and self.phase_2 == False:
            self.can_shoot2 = False
            self.shoot_time2 = pygame.time.get_ticks()
            bullet_directions = [(0.8, 1), (-0.8, 1), (0, 1), (0.4, 1), (-0.4, 1)]
            self.bullet_group.add(Bullet(self.rect.center, 
            (pygame.math.Vector2(*direction))) 
            for direction in bullet_directions)
            self.laser_sound.play()
        
    def big_laser_shoot(self):
        if self.can_shootbig and self.phase_2 and self.health > 0:
            self.can_shootbig = False
            self.shoot_timebig = pygame.time.get_ticks()
            self.biglaser = BigLaser(self.rect.bottomright) 
            self.biglaser_group.add(self.biglaser)
            self.laser_sound.play()
    
    def homing_laser_shoot(self):
        if self.can_shoot3 and self.phase_2 and self.wave_value() and self.health > 0:
            self.can_shoot3 = False
            self.shoot_time3 = pygame.time.get_ticks()
            self.hominglaser = HomingLaser((self.rect.center[0] - 100, self.rect.center[1]), self.ship)
            self.hominglaser2 = HomingLaser((self.rect.center[0] + 100, self.rect.center[1]), self.ship)
            self.homing_laser_group.add(self.hominglaser)
            self.homing_laser_group.add(self.hominglaser2)
            self.laser_sound.play()


class BossHitbox(pygame.sprite.Sprite):
    def __init__(self, ship, boss):
        super().__init__()
        self.image = pygame.image.load('graphics/boss3core.png').convert_alpha()
        self.rect = self.image.get_rect(center = (400,-400))
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(1,1)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        self.damage_boss = False
        self.ship = ship
        self.boss = boss

    def update(self, dt, ship, boss):
        if boss.health <= 0:
            self.speed = 0
            self.kill()
        else:
            #boss logic
            if boss.health <= 20:
                
                self.speed = 150
                if self.rect.centerx > ship.rect.centerx + 10:
                    self.direction.x = -1
                if self.rect.centerx < ship.rect.centerx - 10:
                    self.direction.x = 1
                self.direction.y = 0 

            else:
            
                if self.rect.top >= -20:
                    self.direction.y = 0 
                if self.rect.right >= c.WINDOW_WIDTH - 20 or self.rect.left <= 20: 
                    self.direction.x *= -1

            #normalize the direction vector
            if self.direction.magnitude() != 0:   
                self.direction = self.direction.normalize()

            self.pos += self.direction * self.speed * dt
            self.rect.topleft = round(self.pos.x), round(self.pos.y)

        
class LongLaser(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        self.image = pygame.image.load('graphics/boss3laser.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 600
        self.direction = pygame.math.Vector2(0,1)
       
    def update(self, dt):
        
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720: #or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.speed = 300
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        if self.rect.top > c.WINDOW_HEIGHT or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > c.WINDOW_WIDTH:
            self.kill()

        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize()

class BigLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/biglaser1.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 800
        self.direction = pygame.math.Vector2(0,1)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if self.rect.top > 720:
            self.kill()

class HomingLaser(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        self.image = pygame.image.load('graphics/boss3homing.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300
        self.homing_timer = pygame.time.get_ticks()
        self.homing_delay = 500
        self.following_timer = pygame.time.get_ticks()
        self.following_delay = 570
        self.homing_state = True 
        self.direction = pygame.math.Vector2(0,-1)
         
    def update(self, dt, ship):
        if self.homing_state == False:
            self.pos += self.direction * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
        else:
            if pygame.time.get_ticks() - self.homing_timer > self.homing_delay:
                self.speed = 700
                self.direction = pygame.math.Vector2(ship.rect.center) - pygame.math.Vector2(self.rect.center)

                if pygame.time.get_ticks() - self.following_timer > self.following_delay:
                    self.homing_state = False
                    
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720 or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))


class BossExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.rect = self.image.get_rect(center = pos)
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 100
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.boss_explosion_sound = pygame.mixer.Sound('sounds/bossexplosion.wav')
        self.boss_explosion_sound.play()
        self.animation_done = False
        self.boss_death_timer = pygame.time.get_ticks()
         
    def load_animation(self):
        for i in range(1, 35):
            frames = (pygame.image.load(f'graphics/bossexplosion/bossexplosion{i}.png').convert_alpha())
            self.animation_frames.append(frames)

        self.image = self.animation_frames[self.frame_index]
            
    def update(self, dt):
        self.animate()
        
    def animate(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.animation_done = True
                self.boss_death_timer = pygame.time.get_ticks()
                self.kill()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
        return self.animation_done, self.boss_death_timer
         
    def draw(self, display_surface):
        display_surface.blit(self.image, self.rect)


class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        self.animation_frames = []
        self.damage_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 75
        self.animation_length = len(self.animation_frames) - 1
        self.image = self.animation_frames[self.frame_index]
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect(topleft = (0,-350))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None 
        self.can_worm = True
        self.worm_time = None
        self.can_bullet = True
        self.bullet_time = None
        self.health = 50
        self.damage_boss = False
        self.ship = ship
        
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 100    
        self.direction = pygame.math.Vector2(0,1)
        self.laser_group = pygame.sprite.Group()
        self.worm_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.laser_interval = 2000
        self.worm_interval = 3000
        self.bullet_interval = 3000

        self.boss_attack_timer = pygame.time.get_ticks()
        self.boss_attack_delay = 3000

    def load_animation(self):
        for i in range(0,6):
            frames = (pygame.image.load(f'graphics/finalboss/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
            
        for i in range(0,6):
            frames = (pygame.image.load(f'graphics/finalbossdamage/{i}.png').convert_alpha())
            self.damage_frames.append(frames)
           
        self.image = self.animation_frames[self.frame_index]

    def update(self, dt):
        self.animate()
        if pygame.time.get_ticks() - self.boss_attack_timer > self.boss_attack_delay:
            self.laser_timer()
            self.laser_shoot()
            self.worm_timer()
            self.worm_shoot()
            self.bullet_shoot()
            self.bullet_timer()
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.top > 0:
            self.rect.top = 0
            self.direction = pygame.math.Vector2(0,0)
            self.speed = 0

    def animate(self):
        if self.damage_boss:
            self.image = self.damage_frames[self.frame_index]
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.image = self.damage_frames[self.frame_index]
                    self.damage_boss = False
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.damage_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

        elif not self.damage_boss:
            if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
                self.frame_index += 1
                if self.frame_index >= self.animation_length:
                    self.frame_index = 0
                    self.animation_timer = pygame.time.get_ticks()
                else:
                    self.image = self.animation_frames[self.frame_index]
                    self.animation_timer = pygame.time.get_ticks()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.laser_interval:
                self.can_shoot = True

    def worm_timer(self):
        if not self.can_worm:
            current_time = pygame.time.get_ticks()
            if current_time - self.worm_time > self.worm_interval:
                self.can_worm = True

    def bullet_timer(self):
        if not self.can_bullet:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time > self.bullet_interval:
                self.can_bullet = True

    def laser_shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            if random.randint(0,1) == 0:
                self.laser1 = FinalLaser((229,265))
                self.laser_group.add(self.laser1)
                self.laser2 = FinalLaser((545, 312))
                self.laser_group.add(self.laser2)
                self.laser3 = FinalLaser((914, 282))
                self.laser_group.add(self.laser3)
            else:
                self.laser1 = FinalLaser((382,285))
                self.laser_group.add(self.laser1)
                self.laser2 = FinalLaser((743, 310))
                self.laser_group.add(self.laser2)
                self.laser3 = FinalLaser((1090, 268))
                self.laser_group.add(self.laser3)
            #self.laser_sound.play()

    def worm_shoot(self):
        if self.can_worm:
            self.can_worm = False
            self.worm_time = pygame.time.get_ticks()
            if random.randint(0,1) == 0:
                worm_y_pos = random.randint(360,700)
                worm_x_pos = -100
                self.worm1 = WormLeft((worm_x_pos, worm_y_pos))
                self.worm_group.add(self.worm1)
            else:
                worm_y_pos = random.randint(360,700)
                worm_x_pos = 1380
                self.worm1 = WormRight((worm_x_pos, worm_y_pos))
                self.worm_group.add(self.worm1)

    def bullet_shoot(self):
        if self.can_bullet:
            self.can_bullet = False
            self.bullet_time = pygame.time.get_ticks()
            self.bullet1 = BloodBullet1((603, 186),self.ship)
            self.bullet_group.add(self.bullet1)
            self.bullet2 = BloodBullet2((676,187),self.ship)
            self.bullet_group.add(self.bullet2)
            
        
class FinalLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/finalbosslaser.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 500
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 600
        self.direction = pygame.math.Vector2(0,1)

    def update(self, dt):
        
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720: 
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class WormLeft(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 75
        self.animation_length = len(self.animation_frames)
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300
        self.direction = pygame.math.Vector2(1,0)

    def load_animation(self):
        for i in range(0,2):
            frames = (pygame.image.load(f'graphics/finalbossworm/{i}.png').convert_alpha())
            flipped_frames = pygame.transform.flip(frames, True, False)
            self.animation_frames.append(flipped_frames)
        self.image = self.animation_frames[self.frame_index]
    
    def update(self, dt):
        self.animate()
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.left > 1280: 
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def animate(self):
        self.image = self.animation_frames[self.frame_index]
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()
        


class WormRight(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 75
        self.animation_length = len(self.animation_frames) 
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topright)
        self.speed = 300
        self.direction = pygame.math.Vector2(-1,0)

    def load_animation(self):
        for i in range(0,2):
            frames = (pygame.image.load(f'graphics/finalbossworm/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
        self.image = self.animation_frames[self.frame_index]
    
    def update(self, dt):
        self.animate()
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.right < 0: 
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def animate(self):
        self.image = self.animation_frames[self.frame_index]
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

class BloodBullet1(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 25
        self.animation_length = len(self.animation_frames)
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 100
        self.homing_timer = pygame.time.get_ticks()
        self.homing_delay = random.randint(1000, 2000) 
        self.following_timer = pygame.time.get_ticks()
        self.following_delay = 570
        self.homing_state = True 
        self.direction = pygame.math.Vector2(-1,1)

    def load_animation(self):
        for i in range(0,2):
            frames = (pygame.image.load(f'graphics/bloodbullet/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        self.image = self.animation_frames[self.frame_index]
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

    def update(self, dt, ship):
        self.animate()
        if self.homing_state == False:
            self.pos += self.direction * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
        else:
            if pygame.time.get_ticks() - self.homing_timer > self.homing_delay:
                self.speed = 550
                self.direction = pygame.math.Vector2(ship.rect.center) - pygame.math.Vector2(self.rect.center)

                if pygame.time.get_ticks() - self.following_timer > self.following_delay:
                    self.homing_state = False
                    
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720 or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class BloodBullet2(pygame.sprite.Sprite):
    def __init__(self, pos, ship):
        super().__init__()
        self.animation_frames = []
        self.frame_index = 0
        self.load_animation()
        self.animation_timer = pygame.time.get_ticks()
        self.animation_speed = 25
        self.animation_length = len(self.animation_frames)
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        #float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 100
        self.homing_timer = pygame.time.get_ticks()
        self.homing_delay = random.randint(1000, 2000) 
        self.following_timer = pygame.time.get_ticks()
        self.following_delay = 570
        self.homing_state = True 
        self.direction = pygame.math.Vector2(1,1)

    def load_animation(self):
        for i in range(0,2):
            frames = (pygame.image.load(f'graphics/bloodbullet/{i}.png').convert_alpha())
            self.animation_frames.append(frames)
        self.image = self.animation_frames[self.frame_index]

    def animate(self):
        self.image = self.animation_frames[self.frame_index]
        if pygame.time.get_ticks() - self.animation_timer > self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= self.animation_length:
                self.frame_index = 0
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.image = self.animation_frames[self.frame_index]
                self.animation_timer = pygame.time.get_ticks()

    def update(self, dt, ship):
        self.animate()
        if self.homing_state == False:
            self.pos += self.direction * self.speed * dt
            self.rect.center = (round(self.pos.x), round(self.pos.y))
        else:
            if pygame.time.get_ticks() - self.homing_timer > self.homing_delay:
                self.speed = 550
                self.direction = pygame.math.Vector2(ship.rect.center) - pygame.math.Vector2(self.rect.center)

                if pygame.time.get_ticks() - self.following_timer > self.following_delay:
                    self.homing_state = False
                    
        #normalize the direction vector
        if self.direction.magnitude() != 0:   
            self.direction = self.direction.normalize() 
        
        if self.rect.top > 720 or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > 1280:
                self.kill()
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        
        
    
        