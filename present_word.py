import pygame
import math
import sys, os

from Settings import *


class PresentWord:

    def __init__(self, word):

        self.word = word 

        self.normal_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU_B)
        self.small_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU)

        self.word_font = pygame.font.Font(FONT_LOCATION, FONT_TITLE_B)

        self.background_color = ((255, 255, 255))
        self.text_color = ((10,10,10))
        self.word_color = ((50, 180, 50))
        
        self.start_timer = -1000
        self.total_time = 4000
        self.time_after_word = 1000
        self.word_shrik_time = 100
        self.resize = 10
        self.start_resize = 500
        
    def get_word_surface(self):

        word_surface = self.word_font.render(self.word, False, self.word_color, (0,0,0)).convert_alpha()
        word_surface.set_colorkey((0,0,0))

        rect = word_surface.get_rect()

        ticks = pygame.time.get_ticks()

        # TODO: Here by manipulating the math cool things can happen
        x_factor = (ticks - self.start_timer) / self.time_after_word
        x_factor = x_factor**2  # Faster at the end (sqrt is slower at the end)
        if x_factor > 1:
            x_factor = 1

        mult_factor = self.resize + (1 - self.resize) * x_factor

        new_size = (rect.width * mult_factor, rect.height * mult_factor)

        new_surface = pygame.transform.scale(word_surface, new_size)
        new_surface.set_colorkey((0,0,0))
        return new_surface

    def can_press_return(self):
        ticks = pygame.time.get_ticks()
        if ticks - self.start_timer > self.start_resize + self.word_shrik_time:
            return True 
        return False

    def blit_text(self, screen):
        ticks = pygame.time.get_ticks()

        text = self.normal_font.render("Compose the word...", False, self.text_color, (0,0,0))
        text.set_colorkey((0,0,0))

        text_rect = text.get_rect()
        screen_rect = screen.get_rect()

        text_rect.center = screen_rect.center
        text_rect.y = screen_rect.height / 3 - text_rect.height / 2

        screen.blit(text, text_rect)

        if self.can_press_return():
            text =  self.small_font.render("Press enter to start", False, self.text_color, (0,0,0))
            text.set_colorkey((0,0,0))
            text_rect = text.get_rect()
            screen_rect = screen.get_rect()

            text_rect.center = screen_rect.center
            text_rect.y = screen_rect.height * 2 / 3

            # Make it flicker
            alpha = (math.sin(2 * math.pi * ticks / 800) + 1) / 2
            alpha *= 255
            text.set_alpha(alpha) 

            screen.blit(text, text_rect)

        if ticks - self.start_timer > self.start_resize:
            # Blit the main word here
            surface = self.get_word_surface()
            surf_rect = surface.get_rect()
            surf_rect.center = screen_rect.center

            screen.blit(surface, surf_rect)


    def run(self):

        screen = pygame.display.get_surface()
        self.start_timer = pygame.time.get_ticks()


        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN and self.can_press_return():
                        running = False
            
            screen.fill(self.background_color)
            self.blit_text(screen)

            pygame.display.flip()




