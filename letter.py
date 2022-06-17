import pygame 
class Letter(pygame.sprite.Sprite):

    def __init__(self, x, y, letter, font, *groups) -> None:
        super().__init__(*groups)

        self.x = x
        self.y = y
        self.letter = letter
        self.kind = "letter"
        self._layer = 4

        # Image
        self.image = font.render(letter, False, (100, 255, 0), (0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y