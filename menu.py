from time import sleep
import pygame

import sys, os
from Settings import *

import particles
import random


class Menu:
    def __init__(self, options = [], font_size = FONT_SIZE_MENU_B, color = (10, 10, 10), fixed_message = None, fixed_color= (20, 180, 20), burst = False) :
        self.options = options
        self.focus = 0
        self.font = pygame.font.Font(FONT_LOCATION, font_size)
        self.message_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_TITLE)
        self.color = color
        self.fixed_message = fixed_message
        self.fixed_color = fixed_color

        self.trigger = 0
        self.timeout = 300
        self.return_timeout = 1000
        self.check_return = 0

        screen = pygame.display.get_surface()
        screen_rect = screen.get_rect()

        self.particle_groups = pygame.sprite.Group()
        if burst:
            # Create a burst of particles
            N_particles = 50
            velocity = (0, -12)
            particles.confetti_burst(self.particle_groups,
                screen_rect.width / 3, screen_rect.height, N_particles, velocity)
            particles.confetti_burst(self.particle_groups,
                screen_rect.width * 2 / 3, screen_rect.height, N_particles, velocity)

        #self.sound = pygame.mixer.Sound(os.path.join("data", "sounds", "beep.wav")) 
        self.offset_y = 64

    def update(self):
        self.particle_groups.update()

        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RETURN]:
            self.trigger = 0
            self.check_return = 0

        if ticks - self.trigger > self.timeout:
            
            if (keys[pygame.K_UP]):
                #self.sound.play()
                self.focus -= 1
                self.trigger = ticks
            elif (keys[pygame.K_DOWN]):
                #self.sound.play()
                self.focus += 1
                self.trigger = ticks


        if self.focus < 0:
            self.focus = 0
        if self.focus >= len(self.options):
            self.focus = len(self.options) - 1
        
        if keys[pygame.K_RETURN] and ticks - self.check_return > self.return_timeout:
            self.check_return = ticks
            return self.options[self.focus]
        return None
            


    def draw(self, screen):
        total_size_y = 0
        text_surfaces = []

        width = screen.get_rect().width
        height = screen.get_rect().height

        # Add a fixed message that cannot be clicked
        focus_offset = 0
        if self.fixed_message:
            for i, fx_msg in enumerate(self.fixed_message):
                text_surface = self.message_font.render(fx_msg, False, self.fixed_color, (0,0,0))
                text_surface.set_colorkey((0,0,0))
                text_surfaces.append(text_surface)
                text_rect = text_surface.get_rect()
                total_size_y += text_rect.height
                focus_offset += 1

                if i > 0:
                    total_size_y += self.offset_y


        for i, opt in enumerate(self.options):
            text_surface = self.font.render(opt, False, self.color, (0,0,0))
            text_surface.set_colorkey((0,0,0))
            text_surfaces.append(text_surface)
            text_rect = text_surface.get_rect()
            total_size_y += text_rect.height
            if i > 0 or self.fixed_message:
                total_size_y += self.offset_y

        # Enlight a bit the background
        enlgith_surface = pygame.Surface(WINDOW_SIZE)
        enlgith_surface.fill((255, 255, 255))
        enlgith_surface.set_alpha(80)
        screen.blit(enlgith_surface, (0,0))

        self.particle_groups.draw(screen)

        
        # Display the focus and the text
        current_y = 0
        for i, surf in enumerate(text_surfaces):
            rect = surf.get_rect()
            outer_rect = rect.inflate(32, 32)
            inner_rect = outer_rect.inflate(-16, -16)
            midtop = (width // 2, height // 2 - total_size_y // 2 + current_y)

            
            if self.focus + focus_offset == i:
                rect_surface = pygame.Surface((outer_rect.width, outer_rect.height))
                rect_surface.fill((255, 0, 0))
                inner_rect.x = 8
                inner_rect.y = 8
                pygame.draw.rect(rect_surface, (0, 0, 0), inner_rect)
                rect_surface.set_colorkey((0,0,0))
                outer_rect.midtop = midtop
                outer_rect.y -= 16
                screen.blit(rect_surface, outer_rect)


            rect.midtop = midtop
            current_y += rect.height + self.offset_y
            outer_rect.center = rect.center
            screen.blit(surf, rect)




