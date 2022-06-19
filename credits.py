from turtle import pos
import pygame
import sys, os
import splash_screen
from splash_screen import sinf, signf
from Settings import *

import random
import particles

class Credits:

    def __init__(self):

        self.time_splash = 500
        self.image = pygame.image.load(os.path.join("data", "SplashScreen.png")).convert()
        self.image = pygame.transform.scale(self.image, WINDOW_SIZE)
        self.image.set_colorkey((0,0, 255))

        self.font = pygame.font.Font(FONT_LOCATION, FONT_LETTER)
        self.font_small = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU_B)

        self.fricle_period = 500
        self.press_start_timer = 1500

        self.current_status = -1

        self.press_start_sound = pygame.mixer.Sound(os.path.join("data", "audio", "collect.wav"))

        self.sparkle_burst_rate = 0.08

    def get_color(self):
        ticks = pygame.time.get_ticks()
        

        xvalue = ticks / self.fricle_period
        red = 100 + 155 * sinf(xvalue, 0)
        green = 100 + 155 * sinf(2*xvalue, 0)
        blue = 100 + 155 * sinf(3*xvalue, 0)

        return (red, green, blue)

    def draw_text(self, screen):
        ticks = pygame.time.get_ticks()
        text = self.font.render("Contratulations!", False, self.get_color(), (0,0,0)).convert_alpha()
        text.set_colorkey((0,0,0))

        screen_rect = screen.get_rect()

        text_rect = text.get_rect()
        text_rect.center = screen_rect.center

        screen.blit(text, text_rect)

        text= self.font_small.render("Crafted in 48 hours", False,
            (10,10,10), (0,0,0)).convert_alpha()
        text.set_colorkey((0,0,0))
        text2_rect = text.get_rect()
        text2_rect.midtop = text_rect.midbottom
        text2_rect.y += 128
        screen.blit(text, text2_rect)
        text= self.font_small.render("By Mesonepigreco", False,
            (10,10,10), (0,0,0)).convert_alpha()
        text.set_colorkey((0,0,0))
        text3_rect = text.get_rect()
        text3_rect.midtop = text2_rect.midbottom
        text3_rect.y += 32
        screen.blit(text, text3_rect)





    def run(self):
        running = True
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()

        particles_group = pygame.sprite.Group()

        timer = pygame.time.get_ticks()
        while running:
            clock.tick(60)

            screen.fill(self.get_color())
            screen.blit(self.image, (0,0))

            smooth_surface = pygame.Surface(WINDOW_SIZE)
            smooth_surface.fill((255, 255, 255))
            smooth_surface.set_alpha(180)
            screen.blit(smooth_surface, (0,0))

            particles_group.update()
            particles_group.draw(screen)

            if random.random() < self.sparkle_burst_rate:

                position = (random.randint(0, screen.get_width()), 
                    random.randint(0, screen.get_height()))

                if random.random() < .5:
                    direction = (5.*(random.random()*2 - 1), -5.)
                    particles.confetti_burst(particles_group, position[0], position[1], 50, direction)
                else:
                    particles.sparkles_burst(particles_group, position, 50, 3,  random_colors=True)

            self.draw_text(screen)




            pygame.display.flip()

            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if pygame.time.get_ticks() - timer > 1500:
                            self.press_start_sound.play()
                            return 
