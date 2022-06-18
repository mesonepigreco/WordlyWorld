import re
import pygame
from Settings import *
import sys, os

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class UserInterface():

    def __init__(self, player, simple_font):
        self.player = player
        self.font = simple_font
        self.small_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU)
        self.score_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU_B)

        # Get the lamp image
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        self.offset = 16
        self.target_word = None
        self.current_word = []
        self.original_positions = []



        """
        self.lamp_rect.topleft = self.screen_rect.topleft
        self.lamp_rect.x += offset
        self.lamp_rect.y += offset

        self.total_number_of_lamps = number_of_lamps
        """

        self.bar_rect = pygame.rect.Rect(self.offset, self.screen_rect.height - self.offset - 16,
            160, 16)


    def get_bar_color(self):
        if self.player.timer > 15:
            return (0, 255, 0)
        elif self.player.timer > 5:
            return (255, 255, 0)
        else:
            return(255, 0, 0)

    def set_bar_length(self):
        self.bar_rect.width = 10 * self.player.timer

    def get_score(self):
        current_string = "".join(self.current_word)

        score = similar(self.target_word, current_string)
        return score

    def draw_score(self):

        surface = pygame.Surface((184, 80))
        surface.fill((10, 10, 10))

        rect = surface.get_rect().inflate(-4, -4)
        rect.center = surface.get_rect().center
        pygame.draw.rect(surface, (255, 255, 255), rect)


        score_text = self.small_font.render("Score:", False, (0,0,0), (255, 255, 255))
        score_text.set_colorkey((255, 255,255))
        score_text_rect = score_text.get_rect()
        score_text_rect.midtop = surface.get_rect().midtop
        score_text_rect.y += 8

        surface.blit(score_text, score_text_rect)

        score = self.get_score()
        color = (200, 0, 0)
        if score > .5:
            color = (0, 200, 0)

        score_surface = self.score_font.render("{:.0f}/10".format(score * 10), False, color, (0,0,0))
        score_surface.set_colorkey((0,0,0))
        rect = score_surface.get_rect()
        rect.midtop = score_text_rect.midbottom
        rect.y += 8
        surface.blit(score_surface, rect)

        tot_rect = surface.get_rect()
        tot_rect.topright = self.screen.get_rect().topright
        tot_rect.y += self.offset
        tot_rect.x -= self.offset
        self.screen.blit(surface, tot_rect)


    def draw(self):
        
        # Create the target word
        target_word_surface = self.font.render(self.target_word, False, (20, 20, 20), (0,0,0))
        target_word_surface.set_colorkey((0,0,0))
        target_rect = target_word_surface.get_rect()

        self.screen.blit(target_word_surface, (self.offset, self.offset))

        # Create the target word
        current_word_surface = self.font.render("".join(self.current_word), False, (100, 255, 0), (0,0,0))
        current_word_surface.set_colorkey((0,0,0))

        self.screen.blit(current_word_surface, (self.offset, 1.5*self.offset + target_rect.height))

        self.draw_score()


        # Lets write the timer on the bottom of the screen
        # Replace it with a hourglass
        self.set_bar_length()
        
        outline = self.bar_rect.inflate(8, 8)
        outline.center = self.bar_rect.center

        pygame.draw.rect(self.screen, (10, 10, 10), outline)
        pygame.draw.rect(self.screen, self.get_bar_color(), self.bar_rect)
        """
        timer_surface = self.font.render("{:.0f}".format(abs(self.player.timer)), False, (100, 0, 0), (0,0,0))
        timer_surface.set_colorkey((0,0,0))
        rect = timer_surface.get_rect()
        rect.bottomleft = self.screen.get_rect().bottomleft
        rect.x += self.offset
        rect.y -= self.offset
        self.screen.blit(timer_surface, rect)"""

        """
        text = "{} / {}".format(self.collected_lamps, self.total_number_of_lamps)

        text_surface = self.font.render(text, False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))

        text_rect = text_surface.get_rect()
        text_rect.midbottom = self.lamp_rect.midbottom
        text_rect.y += 20

        self.screen.blit(text_surface, text_rect)


        # Add the Level text
        text_surface = self.font.render("Level " + str(level + 1), False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.topright = (WINDOW_SIZE[0], 0)
        text_rect.y += 16
        text_rect.x -= 16

        self.screen.blit(text_surface, text_rect)
        """







