import pygame, sys, os, time, random
from base_state import Base_State
import constants as c
from fade import Cutscene_Fadeout, Cutscene_Fadein
from credit_roll3 import Credit_Roll3

class Credit_Roll2(Base_State):
    def __init__(self, game):
        Base_State.__init__(self, game)
        self.game = game
        self.fadeout = Cutscene_Fadeout(self.game, 1, 0,0)
        self.fade_timer = pygame.time.get_ticks()
        self.fade_delay = 49000
        self.fade_bool = False
        #scroll speed
        self.scroll_speed = 18  # pixels per second
        #font sizes
        self.font = pygame.font.Font('graphics/gradius.ttf', 25)
        self.font2 = pygame.font.Font('graphics/gradius.ttf', 50)
        #text
        self.text0 = "STAFF"
        self.text0_surface = self.font.render(self.text0, True, c.WHITE)
        self.text0_rect = self.text0_surface.get_rect(topleft=(100, 860))
        
        self.text1 = "LEAD PROGRAMMER"
        self.text1_surface = self.font.render(self.text1, True, c.WHITE)
        self.text1_rect = self.text1_surface.get_rect(topleft=(100, 1060))
        self.text2 = "AUSTIN HARRY"
        self.text2_surface = self.font2.render(self.text2, True, c.WHITE)
        self.text2_rect = self.text2_surface.get_rect(topleft=(100, 1100))

        self.text3 = "GAME PLANNING AND DIRECTION"
        self.text3_surface = self.font.render(self.text3, True, c.WHITE)
        self.text3_rect = self.text3_surface.get_rect(topleft=(100, 1325))
        self.text4 = "AUSTIN HARRY"
        self.text4_surface = self.font2.render(self.text4, True, c.WHITE)
        self.text4_rect = self.text4_surface.get_rect(topleft=(100, 1365))
        self.text5 = "NOLAN HARRY"
        self.text5_surface = self.font2.render(self.text5, True, c.WHITE)
        self.text5_rect = self.text5_surface.get_rect(topleft=(100, 1430))

        self.text6 = "ART"
        self.text6_surface = self.font.render(self.text6, True, c.WHITE)
        self.text6_rect = self.text6_surface.get_rect(topleft=(100, 1655))
        self.text7 = "AUSTIN HARRY"
        self.text7_surface = self.font2.render(self.text7, True, c.WHITE)
        self.text7_rect = self.text7_surface.get_rect(topleft=(100, 1695))
        self.text8 = "NOLAN HARRY"
        self.text8_surface = self.font2.render(self.text8, True, c.WHITE)
        self.text8_rect = self.text8_surface.get_rect(topleft=(100, 1760))
        self.text9 = "DALL-E"
        self.text9_surface = self.font2.render(self.text9, True, c.WHITE)
        self.text9_rect = self.text9_surface.get_rect(topleft=(100, 1825))

        self.text10 = "SOUND AND MUSIC"
        self.text10_surface = self.font.render(self.text10, True, c.WHITE)
        self.text10_rect = self.text10_surface.get_rect(topleft=(100, 2050))
        self.text11 = "AUSTIN HARRY"
        self.text11_surface = self.font2.render(self.text11, True, c.WHITE)
        self.text11_rect = self.text11_surface.get_rect(topleft=(100, 2090))

        self.text12 = "CULTURAL SENSITIVITY CONSULTANT"
        self.text12_surface = self.font.render(self.text12, True, c.WHITE)
        self.text12_rect = self.text12_surface.get_rect(topleft=(100, 2315))
        self.text13 = "TOLERANCE LITTLE-PETERS"
        self.text13_surface = self.font2.render(self.text13, True, c.WHITE)
        self.text13_rect = self.text13_surface.get_rect(topleft=(100, 2355))

        self.text14 = "SPECIAL THANKS"
        self.text14_surface = self.font.render(self.text14, True, c.WHITE)
        self.text14_rect = self.text14_surface.get_rect(topleft=(100, 2580))
        self.text15 = "ERIN HARRY"
        self.text15_surface = self.font2.render(self.text15, True, c.WHITE)
        self.text15_rect = self.text15_surface.get_rect(topleft=(100, 2620))
        self.text16 = "MICAH HARRY"    
        self.text16_surface = self.font2.render(self.text16, True, c.WHITE)
        self.text16_rect = self.text16_surface.get_rect(topleft=(100, 2685))
        self.text17 = "JOE GODWIN"
        self.text17_surface = self.font2.render(self.text17, True, c.WHITE)
        self.text17_rect = self.text17_surface.get_rect(topleft=(100, 2750))
        self.text18 = "GITHUB COPILOT"
        self.text18_surface = self.font2.render(self.text18, True, c.WHITE)
        self.text18_rect = self.text18_surface.get_rect(topleft=(100, 2815))
        self.text19 = "'CHAT' GPT-3" 
        self.text19_surface = self.font2.render(self.text19, True, c.WHITE)
        self.text19_rect = self.text19_surface.get_rect(topleft=(100, 2880))

        self.text20 = "THANK YOU FOR PLAYING!"
        self.text20_surface = self.font2.render(self.text20, True, c.WHITE)
        self.text20_rect = self.text20_surface.get_rect(topleft=(125, 3655))

        self.pos_x0, self.pos_y0 = self.text0_rect.center
        self.pos_x1, self.pos_y1 = self.text1_rect.center
        self.pos_x2, self.pos_y2 = self.text2_rect.center
        self.pos_x3, self.pos_y3 = self.text3_rect.center
        self.pos_x4, self.pos_y4 = self.text4_rect.center
        self.pos_x5, self.pos_y5 = self.text5_rect.center
        self.pos_x6, self.pos_y6 = self.text6_rect.center
        self.pos_x7, self.pos_y7 = self.text7_rect.center
        self.pos_x8, self.pos_y8 = self.text8_rect.center
        self.pos_x9, self.pos_y9 = self.text9_rect.center
        self.pos_x10, self.pos_y10 = self.text10_rect.center
        self.pos_x11, self.pos_y11 = self.text11_rect.center
        self.pos_x12, self.pos_y12 = self.text12_rect.center
        self.pos_x13, self.pos_y13 = self.text13_rect.center
        self.pos_x14, self.pos_y14 = self.text14_rect.center
        self.pos_x15, self.pos_y15 = self.text15_rect.center
        self.pos_x16, self.pos_y16 = self.text16_rect.center
        self.pos_x17, self.pos_y17 = self.text17_rect.center
        self.pos_x18, self.pos_y18 = self.text18_rect.center
        self.pos_x19, self.pos_y19 = self.text19_rect.center
        self.pos_x20, self.pos_y20 = self.text20_rect.center
        
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(120) / 1000

    def update(self, dt, actions):
        if self.fade_bool:
            self.fadeout.update(dt, actions)
            if self.fadeout.fade_complete:
                credit_roll3 = Credit_Roll3(self.game)
                credit_roll3.enter_state()
        self.pos_y0 -= self.scroll_speed * self.dt
        self.text0_rect.center = (self.pos_x0, self.pos_y0)
        self.pos_y1 -= self.scroll_speed * self.dt
        self.text1_rect.center = (self.pos_x1, self.pos_y1)
        self.pos_y2 -= self.scroll_speed * self.dt
        self.text2_rect.center = (self.pos_x2, self.pos_y2)
        self.pos_y3 -= self.scroll_speed * self.dt
        self.text3_rect.center = (self.pos_x3, self.pos_y3)
        self.pos_y4 -= self.scroll_speed * self.dt
        self.text4_rect.center = (self.pos_x4, self.pos_y4)
        self.pos_y5 -= self.scroll_speed * self.dt
        self.text5_rect.center = (self.pos_x5, self.pos_y5)
        self.pos_y6 -= self.scroll_speed * self.dt
        self.text6_rect.center = (self.pos_x6, self.pos_y6)
        self.pos_y7 -= self.scroll_speed * self.dt
        self.text7_rect.center = (self.pos_x7, self.pos_y7)
        self.pos_y8 -= self.scroll_speed * self.dt
        self.text8_rect.center = (self.pos_x8, self.pos_y8)
        self.pos_y9 -= self.scroll_speed * self.dt
        self.text9_rect.center = (self.pos_x9, self.pos_y9)
        self.pos_y10 -= self.scroll_speed * self.dt
        self.text10_rect.center = (self.pos_x10, self.pos_y10)
        self.pos_y11 -= self.scroll_speed * self.dt
        self.text11_rect.center = (self.pos_x11, self.pos_y11)
        self.pos_y12 -= self.scroll_speed * self.dt
        self.text12_rect.center = (self.pos_x12, self.pos_y12)
        self.pos_y13 -= self.scroll_speed * self.dt
        self.text13_rect.center = (self.pos_x13, self.pos_y13)
        self.pos_y14 -= self.scroll_speed * self.dt
        self.text14_rect.center = (self.pos_x14, self.pos_y14)
        self.pos_y15 -= self.scroll_speed * self.dt
        self.text15_rect.center = (self.pos_x15, self.pos_y15)
        self.pos_y16 -= self.scroll_speed * self.dt
        self.text16_rect.center = (self.pos_x16, self.pos_y16)
        self.pos_y17 -= self.scroll_speed * self.dt
        self.text17_rect.center = (self.pos_x17, self.pos_y17)
        self.pos_y18 -= self.scroll_speed * self.dt
        self.text18_rect.center = (self.pos_x18, self.pos_y18)
        self.pos_y19 -= self.scroll_speed * self.dt
        self.text19_rect.center = (self.pos_x19, self.pos_y19)
        self.pos_y20 -= self.scroll_speed * self.dt
        self.text20_rect.center = (self.pos_x20, self.pos_y20)
        if self.pos_y20 <= c.WINDOW_HEIGHT / 2:
            self.pos_y20 = c.WINDOW_HEIGHT / 2
        
    def draw(self, display_surface):
        display_surface.fill(c.BLACK)
        display_surface.blit(self.text0_surface, self.text0_rect)
        display_surface.blit(self.text1_surface, self.text1_rect)
        display_surface.blit(self.text2_surface, self.text2_rect)
        display_surface.blit(self.text3_surface, self.text3_rect)
        display_surface.blit(self.text4_surface, self.text4_rect)
        display_surface.blit(self.text5_surface, self.text5_rect)
        display_surface.blit(self.text6_surface, self.text6_rect)
        display_surface.blit(self.text7_surface, self.text7_rect)
        display_surface.blit(self.text8_surface, self.text8_rect)
        display_surface.blit(self.text9_surface, self.text9_rect)
        display_surface.blit(self.text10_surface, self.text10_rect)
        display_surface.blit(self.text11_surface, self.text11_rect)
        display_surface.blit(self.text12_surface, self.text12_rect)
        display_surface.blit(self.text13_surface, self.text13_rect)
        display_surface.blit(self.text14_surface, self.text14_rect)
        display_surface.blit(self.text15_surface, self.text15_rect)
        display_surface.blit(self.text16_surface, self.text16_rect)
        display_surface.blit(self.text17_surface, self.text17_rect)
        display_surface.blit(self.text18_surface, self.text18_rect)
        display_surface.blit(self.text19_surface, self.text19_rect)
        display_surface.blit(self.text20_surface, self.text20_rect)

        if pygame.time.get_ticks() - self.fade_timer >= self.fade_delay:
            self.fade_bool = True
            self.fadeout.draw(display_surface)

        

        


    
        
