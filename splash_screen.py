import pygame
import math
import sys, os
from Settings import *


def sinf(x, phase=0):
    return .5 * (1 + math.sin(2 * math.pi * x + math.pi/4 * phase ))

def signf(x):
    v = sinf(x)
    if v > .5:
        return 1
    return 0

class SplashScreen:

    def __init__(self):

        self.time_splash = 500
        self.image = pygame.image.load(os.path.join("data", "SplashScreen.png")).convert()
        self.image = pygame.transform.scale(self.image, WINDOW_SIZE)
        self.image.set_colorkey((0,0, 255))

        self.font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU_B)

        self.fricle_period = 500
        self.press_start_timer = 1500

        self.current_status = -1

        self.press_start_sound = pygame.mixer.Sound(os.path.join("data", "audio", "collect.wav"))

        self.tutorials = []
        for i in range(1, 7):
            tutorial = pygame.image.load(os.path.join("data", "tutorial", "tutorial{:d}.png".format(i))).convert()
            tutorial = pygame.transform.scale(tutorial, WINDOW_SIZE)
            self.tutorials.append(tutorial) 

    def get_color(self):
        ticks = pygame.time.get_ticks()
        

        xvalue = ticks / self.fricle_period
        red = 100 + 155 * sinf(xvalue, 0)
        green = 100 + 155 * sinf(2*xvalue, 0)
        blue = 100 + 155 * sinf(3*xvalue, 0)

        return (red, green, blue)

    def draw_press_start(self, screen):
        ticks = pygame.time.get_ticks()
        text = self.font.render("Press Enter", False, (10, 10, 10), (0,0,0)).convert_alpha()
        text.set_colorkey((0,0,0))
        text.set_alpha(255 * signf(ticks / self.press_start_timer))

        screen_rect = screen.get_rect()

        text_rect = text.get_rect()
        text_rect.midbottom = screen_rect.midbottom
        text_rect.y -= screen_rect.height / 8

        screen.blit(text, text_rect)


    def run(self):
        running = True
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        while running:
            clock.tick(60)

            screen.fill(self.get_color())
            screen.blit(self.image, (0,0))
            
            if self.current_status >= 0:
                screen.blit(self.tutorials[self.current_status], (0,0))
            
            self.draw_press_start(screen)


            pygame.display.flip()

            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.press_start_sound.play()
                        self.current_status += 1
                        if self.current_status >= len(self.tutorials):
                            return 
