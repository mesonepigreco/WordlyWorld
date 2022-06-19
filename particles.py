import pygame
import random

class Confetti(pygame.sprite.Sprite):

    def __init__(self, x, y, velocity, color = (0, 255, 0), *args):
        super().__init__(*args)
        self.x = x
        self.y = y
        self.velocity = velocity

        self.image = pygame.Surface((8,8))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y
        self.gravity = 0.3
        self.max_velocity = 2
        self.lifetime = 300

    def update(self, *args):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.velocity.y += self.gravity
        if self.velocity.y > self.max_velocity:
            self.velocity.y = self.max_velocity

        self.lifetime -= 1

        if self.lifetime < 0:
            self.kill()

class Sparkle(Confetti):
    def __init__(self, x, y, velocity, radius = 4, color = (255, 255, 255)):
        super().__init__(x, y, velocity)

        self.lifetime = 45

        self._layer = 5

        # Redefine the image to be a small circle
        self.image = pygame.Surface((2*radius, 2*radius))
        self.image.fill((0,0,0))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.image.set_colorkey((0,0,0))
        self.gravity = 0

        self.start_lifetime = self.lifetime
    
    def update(self, *args):
        x = (self.lifetime / self.start_lifetime) * 255
        self.image.set_alpha(x)

        return super().update(*args)



def confetti_burst(visible_sprite, x, y, N, preferred_direction, av_speed = 3, avoid_gravity = False, lifetime = None):

    # Random colors
    colors = [(255, 100, 100), (50, 255, 255), (100, 255, 100),
        (100, 100, 255), (255, 255, 50), (255, 50, 255)]

    for i in range(N):
        velocity = pygame.math.Vector2(preferred_direction[0], preferred_direction[1])
        velocity.x += random.uniform(-1., 1.) * av_speed
        velocity.y += random.uniform(-1., 1.) * av_speed

        color = colors[random.randint(0, len(colors)-1)]
        conf = Confetti(x + random.uniform(-8, 8), y, velocity, color)
        if avoid_gravity:
            conf.gravity = 0
        
        if lifetime is not None:
            conf.lifetime = lifetime

        visible_sprite.add(conf)

def sparkles_burst(visible_sprites,  pos, N, av_speed = 1.7, random_colors = False):

    if random_colors:
        # Random colors
        colors = [(255, 100, 100), (50, 255, 255), (100, 255, 100),
            (100, 100, 255), (255, 255, 50), (255, 50, 255)]
        color = colors[random.randint(0, len(colors)-1)]
    else:
        color = (255, 255, 255)

    x, y = pos
    for i in range(N):
        velocity = pygame.math.Vector2(0,0)
        velocity.x += random.uniform(-1., 1.) * av_speed
        velocity.y += random.uniform(-1., 1.) * av_speed

        sparkle = Sparkle(x + random.uniform(-8, 8), y + random.uniform(-8, 8), velocity, color = color)
        visible_sprites.add(sparkle)