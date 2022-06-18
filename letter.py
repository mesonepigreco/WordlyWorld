import pygame

from Settings import *
class Letter(pygame.sprite.Sprite):

    def __init__(self, x, y, letter, *groups) -> None:
        super().__init__(*groups)

        self.x = x
        self.y = y
        self.letter = letter
        self.kind = "letter"
        self._layer = 4

        # Image
        self.back_font = pygame.font.Font(FONT_LOCATION, FONT_LETTER_B)
        self.font = pygame.font.Font(FONT_LOCATION, FONT_LETTER)

        self.image = self.back_font.render(letter, False, (10, 10, 10), (0,0,0)).convert_alpha()
        self.image.set_colorkey((0,0,0))

        clear_letter =  self.font.render(letter, False, (50, 255, 50), (0,0,0)).convert_alpha()
        clear_letter.set_colorkey((0,0,0)) 
        cl_rect = clear_letter.get_rect()
        cl_rect.center = self.image.get_rect().center
        self.image.blit(clear_letter, cl_rect)
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.average_y = self.y
        self.direction = pygame.math.Vector2(0,1)
        self.speed = 0.5
        self.offset_move = 16

    def update(self, *args):
        if abs(self.y - self.average_y) > self.offset_move:
            self.direction.y *= -1

        self.y += self.direction.y * self.speed

        self.rect.x = self.x
        self.rect.y = self.y
        

        