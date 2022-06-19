import pygame
import sys, os
from overworld import OverWorld
import player
import level
import splash_screen
import credits


if __name__ == "__main__":
    # Force the execution in the directory of the script
    total_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(total_path)


    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()


    visible_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()

    overworld = OverWorld()
    overworld.init()

    splash = splash_screen.SplashScreen()
    splash.run()

    overworld.run()

    #world = level.World()
    #world.start_level()
    """
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        result = world.update(screen)

        if result == "Quit":
            running = False

        pygame.display.flip()
    """