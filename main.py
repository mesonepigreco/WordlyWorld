import pygame
import sys, os
import player
import level

pygame.init()
screen = pygame.display.set_mode((800, 600))


clock = pygame.time.Clock()


visible_sprites = pygame.sprite.Group()
collision_sprites = pygame.sprite.Group()

world = level.World()
world.start_level()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.update(screen)

    pygame.display.flip()