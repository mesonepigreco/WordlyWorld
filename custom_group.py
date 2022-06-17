import pygame

class MyGroup(pygame.sprite.Group):

    def __init__(self, camera, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = camera

    def draw(self, surface):

        for sprite in sorted(self.sprites(), key= lambda x : x._layer):
            x = sprite.rect.x - self.camera.x
            y = sprite.rect.y - self.camera.y
            surface.blit(sprite.image, (x,y))

