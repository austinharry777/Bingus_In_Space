import os, time, pygame, sys
import constants as c
from pygame import mixer
from intro import Intro
from random import randint, uniform
from  level1 import *
import json
from level_complete3 import LevelComplete3
from ending import Ending
from credit_roll2 import Credit_Roll2
mixer.init()
pygame.mouse.set_visible(False) #hide mouse cursor



#Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

with open(os.path.join("ps4_keys.json"), 'r+') as file:
    button_keys = json.load(file)
# 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }


class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.canvas = pygame.Surface((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        self.running = True
        self.playing = True  
        #control dictionary
        self.actions = {'left_mouse': False, 'right_mouse': False, 'space_bar': False, 'enter': False,
        'left': False, 'right': False, 'up': False, 'down': False}
        self.delt = 0
        self.prev_time = 0
        self.state_stack = []
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        
        # variables for health boosts upon 2 levels completed
        self.completed_levels = 0
        self.playthroughs_completed = 0
        
        self.load_states()
        self.current_time = pygame.time.get_ticks()
        
        
    #game loop
    def game_loop(self):
        while self.playing:
            self.get_delt()
            self.get_events()
            self.update()
            self.draw()
        
    #event handler
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.JOYHATMOTION:
                hat_value = joystick.get_hat(0)
                if hat_value == (1, 0):
                    self.actions['right'] = True
                elif hat_value == (-1, 0):
                    self.actions['left'] = True
                elif hat_value == (0, 1):
                    self.actions['up'] = True
                elif hat_value == (0, -1):
                    self.actions['down'] = True
                elif hat_value == (1,1):
                    self.actions['right'] = True
                    self.actions['up'] = True
                elif hat_value == (-1,1):
                    self.actions['left'] = True
                    self.actions['up'] = True
                elif hat_value == (1,-1):
                    self.actions['right'] = True
                    self.actions['down'] = True
                elif hat_value == (-1,-1):
                    self.actions['left'] = True
                    self.actions['down'] = True
                    
                else:
                    self.actions['right'] = False
                    self.actions['left'] = False
                    self.actions['up'] = False
                    self.actions['down'] = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        self.playing = False
                        self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actions['space_bar'] = True
                if event.key == pygame.K_RETURN:
                        self.actions['enter'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.actions['space_bar'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['enter'] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions['left_mouse'] = True
                if event.button == 3:
                    self.actions['right_mouse'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions['left_mouse'] = False
                if event.button == 3:
                    self.actions['right_mouse'] = False
            
            #HANDLES KEY PRESSES (may use for keyboard controls)
            
            # if pygame.key.get_pressed()[pygame.K_a]:
            #     self.actions['left'] = True
            # if not pygame.key.get_pressed()[pygame.K_a]:
            #     self.actions['left'] = False
            # if pygame.key.get_pressed()[pygame.K_d]:
            #     self.actions['right'] = True
            # if not pygame.key.get_pressed()[pygame.K_d]:
            #     self.actions['right'] = False
            # if pygame.key.get_pressed()[pygame.K_s]:    
            #     self.actions['down'] = True
            # if not pygame.key.get_pressed()[pygame.K_s]:
            #     self.actions['down'] = False
            # if pygame.key.get_pressed()[pygame.K_w]:
            #     self.actions['up'] = True
            # if not pygame.key.get_pressed()[pygame.K_w]:
            #     self.actions['up'] = False
            # if pygame.key.get_pressed()[pygame.K_SPACE]:
            #     self.actions['left_mouse'] = True
            # if not pygame.key.get_pressed()[pygame.K_SPACE]:
            #     self.actions['left_mouse'] = False
            
            # HANDLES BUTTON PRESSES
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == button_keys['left_arrow']:
                    self.actions['left'] = True
                if event.button == button_keys['right_arrow']:
                    self.actions['right'] = True
                if event.button == button_keys['down_arrow']:
                    self.actions['down'] = True
                if event.button == button_keys['up_arrow']:
                    self.actions['up'] = True
                if event.button == button_keys['x']\
                    or event.button == button_keys['circle']\
                    or event.button == button_keys['triangle']\
                    or event.button == button_keys['square']:
                        self.actions['left_mouse'] = True
                if event.button == button_keys['options']:
                    self.actions['enter'] = True
            # HANDLES BUTTON RELEASES
            if event.type == pygame.JOYBUTTONUP:
                if event.button == button_keys['left_arrow']:
                    self.actions['left'] = False
                if event.button == button_keys['right_arrow']:
                    self.actions['right'] = False
                if event.button == button_keys['down_arrow']:
                    self.actions['down'] = False
                if event.button == button_keys['up_arrow']:
                    self.actions['up'] = False
                if event.button == button_keys['x']\
                    or event.button == button_keys['circle']\
                    or event.button == button_keys['triangle']\
                    or event.button == button_keys['square']:
                        self.actions['left_mouse'] = False
                if event.button == button_keys['options']:
                    self.actions['enter'] = False

            #HANDLES ANALOG INPUTS
            if event.type == pygame.JOYAXISMOTION:
                analog_keys[event.axis] = event.value
                
                # Horizontal Analog
                if abs(analog_keys[0]) < .1:
                    analog_keys[0] = 0
                if abs(analog_keys[1]) < .1:
                    analog_keys[1] = 0
                if analog_keys[0] < -.2:
                    self.actions['left'] = True
                else:
                    self.actions['left'] = False
                if analog_keys[0] > .2:
                    self.actions['right'] = True
                else:
                    self.actions['right'] = False
                # Vertical Analog
                

                if analog_keys[1] < -.2:
                    self.actions['up'] = True
                else:
                    self.actions['up'] = False
                if analog_keys[1] > .2:
                    self.actions['down'] = True
                else:
                    self.actions['down'] = False

    def update(self):
        self.state_stack[-1].update(self.delt, self.actions)
    
    def draw(self):
        self.state_stack[-1].draw(self.canvas)
        self.screen.blit(pygame.transform.scale(self.canvas, (c.WINDOW_WIDTH, c.WINDOW_HEIGHT)), (0,0))
        pygame.display.flip()

    def get_delt(self):
        now = time.time()
        self.delt = now - self.prev_time
        self.prev_time = now 

    #function for drawing text
    def draw_text(self, surface, text, color, x,y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        surface.blit(text_surface, text_rect)

    def load_states(self):
        self.title_screen = Intro(self)        
        self.state_stack.append(self.title_screen)
        
    
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
















