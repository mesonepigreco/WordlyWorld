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

        #self.bar_rect = pygame.rect.Rect(self.lamp_rect.x, self.lamp_rect.y,
        #    160, 16)

        #self.bar_rect.midleft = self.lamp_rect.midright


    def get_bar_color(self):
        if self.player.remaining_oil > 50:
            return (0, 255, 0)
        elif self.player.remaining_oil > 25:
            return (255, 255, 0)
        else:
            return(255, 0, 0)

    def get_score(self):
        current_string = "".join(self.current_word)

        score = similar(self.target_word, current_string)
        return score



    def draw(self):
        
        # Create the target word
        target_word_surface = self.font.render(self.target_word, False, (80, 80, 80), (0,0,0))
        target_word_surface.set_colorkey((0,0,0))
        target_rect = target_word_surface.get_rect()

        self.screen.blit(target_word_surface, (self.offset, self.offset))

        # Create the target word
        current_word_surface = self.font.render("".join(self.current_word), False, (100, 255, 0), (0,0,0))
        current_word_surface.set_colorkey((0,0,0))

        self.screen.blit(current_word_surface, (self.offset, 1.5*self.offset + target_rect.height))


        score_surface = self.font.render("{:.2f}".format(self.get_score()), False, (255, 255, 40), (0,0,0))
        score_surface.set_colorkey((0,0,0))
        rect = score_surface.get_rect()
        rect.topright = self.screen.get_rect().topright
        rect.x -= self.offset
        rect.y += self.offset
        self.screen.blit(score_surface, rect)


        # Lets write the timer on the bottom of the screen
        # Replace it with a hourglass
        timer_surface = self.font.render("{:.0f}".format(abs(self.player.timer)), False, (100, 0, 0), (0,0,0))
        timer_surface.set_colorkey((0,0,0))
        rect = timer_surface.get_rect()
        rect.bottomleft = self.screen.get_rect().bottomleft
        rect.x += self.offset
        rect.y -= self.offset
        self.screen.blit(timer_surface, rect)

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







