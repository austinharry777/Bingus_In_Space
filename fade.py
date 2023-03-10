import pygame
import constants as c 


class Cutscene_Fadein:
    def __init__(self, game, speed, x,y):
        self.game = game
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y
        self.speed = speed #0 = slower fade in, 1 = faster fade in 
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0

    def update(self, dt, actions):
        self.animate(dt)

    def draw(self, display_surface):
        display_surface.blit(self.curr_image,(self.position_x, self.position_y))
        
    def animate(self, dt):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += dt
        #progress animation
        if self.fade_complete == True:
            self.curr_image = self.curr_anim_list[len(self.curr_anim_list) - 1]
        else:
            if self.speed == 0:
                if self.last_frame_update > .14:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            elif self.speed == 1:
                if self.last_frame_update > .07:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            
            if self.current_frame >= len(self.curr_anim_list) - 1: 
                self.current_frame = len(self.curr_anim_list) - 1
                self.fade_complete = True
        return self.fade_complete 

    def load_sprites(self):
        #make fade in animation sprite lists
        self.fade_in_sprites = []
        for i in range(25):
            fade_in = pygame.image.load(f"graphics/cutscene_fadein/{i}.png").convert_alpha()
            fade_in = pygame.transform.scale(fade_in, (c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
            self.fade_in_sprites.append(fade_in)
        self.curr_image = self.fade_in_sprites[0]
        self.curr_anim_list = self.fade_in_sprites



class Cutscene_Fadeout:
    def __init__(self, game, speed, x,y):
        self.game = game
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y 
        self.speed = speed #0 = slower fade in, 1 = faster fade in
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0

    def update(self, dt, actions):
        self.animate(dt)

    def draw(self, display_surface):
        display_surface.blit(self.curr_image,(self.position_x, self.position_y))
        
    def animate(self, dt):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += dt
        #progress animation
        if self.fade_complete == True:
            self.curr_image = self.curr_anim_list[len(self.curr_anim_list) - 1]
        else:
            if self.speed == 0:
                if self.last_frame_update > .14:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            elif self.speed == 1:
                if self.last_frame_update > .07:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            
            if self.current_frame >= len(self.curr_anim_list) - 1: 
                self.current_frame = len(self.curr_anim_list) - 1
                self.fade_complete = True
        return self.fade_complete 

    def load_sprites(self):
        #make out animation sprite lists
        self.fade_out_sprites = []
        for i in range(25):
            fade_out = pygame.image.load(f"graphics/cutscene_fadeout/{i}.png").convert_alpha()
            fade_out = pygame.transform.scale(fade_out, (c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
            self.fade_out_sprites.append(fade_out)
        self.curr_image = self.fade_out_sprites[0]
        self.curr_anim_list = self.fade_out_sprites