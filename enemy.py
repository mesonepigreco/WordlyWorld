import pygame
from Settings import *

import sys, os

class Enemy(pygame.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layer = 3
        self.kind = "enemy"

        self.status = "idle"
        self.push_back = 2
        self.steal_oil = 10
        self.hitbox = None


        self.direction = pygame.math.Vector2(0,0)
        self.speed = 0
        self.is_going_left = False
        self.is_going_right = False
        self.affected_by_gravity = True
        self.is_grounded = False

        self.stun_trigger = 0
        self.stun_timeout = 700


    def update_rect(self):
        self.rect.center = self.hitbox.center
    
    def update_image(self):
        pass

    def trigger_horizontal_collision(self):
        pass


    def update(self, collision_group):
        ticks = pygame.time.get_ticks()

        self.update_direction()
        self.update_image()

        if ticks - self.stun_trigger > self.stun_timeout:
            self.status = "idle"
            self.hitbox.x += self.direction.x * self.speed
            self.detect_collistions(collision_group, left_right= True)
            self.hitbox.y += self.direction.y * self.speed
            self.detect_collistions(collision_group, left_right=False)
        else:
            self.status = "stun"

        self.update_rect()

    def detect_collistions(self, collision_group, left_right = True):
        is_colliding = False

        empty_left = True
        empty_right = True



        for sprite in collision_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                is_colliding = True

                if left_right:
                    if self.is_going_right:
                        self.hitbox.right = sprite.rect.left
                    elif self.is_going_left:
                        self.hitbox.left = sprite.rect.right
                    
                    self.trigger_horizontal_collision()
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        if not self.is_grounded:
                            self.is_grounded = True
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom 

                    self.direction.y = 0
            

        # Detect the change in the direction to avoid falling
        if left_right:  
            collision_right = list(self.hitbox.midbottom)
            collision_right[1] += self.direction.y * self.speed
            collision_left = [value for value in collision_right]
            collision_right[0] += 8
            collision_left[0] -= 8
            for sprite in collision_group.sprites():
                if left_right:
                    if sprite.rect.collidepoint(collision_right):
                        empty_right = False
                    if sprite.rect.collidepoint(collision_left):
                        empty_left = False

            if empty_left and not empty_right:
                self.direction.x = abs(self.direction.x)
            elif not empty_left and empty_right:
                self.direction.x = - abs(self.direction.x)


        if not left_right:
            if not is_colliding:

                if self.is_grounded:
                    self.is_grounded = False
        

        


    def update_direction(self):
        if self.direction.x > 0:
            self.is_going_right = True
            self.is_going_left = False
        elif self.direction.x < 0:
            self.is_going_right = False
            self.is_going_left = True
        else:
            self.is_going_right = False
            self.is_going_left = False


        if self.affected_by_gravity:
            self.direction.y += GRAVITY
            if self.direction.y > MAX_VERTICAL_SPEED:
                self.direction.y = MAX_VERTICAL_SPEED

        



class Eraser(Enemy):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define a static surface
        self.image = pygame.image.load(os.path.join("data", "eraser", "idle0000.png")).convert_alpha()
        rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (rect.width * SCALE_FACTOR, rect.height * SCALE_FACTOR))

        # Load animation
        self.animations = {
            "idle_right" : [self.image],
            "idle_left" : [pygame.transform.flip(self.image, True, False)],
            "walk_right" : [],
            "walk_left" : []
        }
        
        for i in range(7):
            surface = pygame.image.load(os.path.join(DATA_DIR, "eraser", "walk{:04d}.png".format(i))).convert_alpha()
            rect = surface.get_rect()
            surface = pygame.transform.scale(surface, (rect.width * SCALE_FACTOR, rect.height * SCALE_FACTOR))
            
            self.animations["walk_right"].append(surface)
            self.animations["walk_left"].append(pygame.transform.flip(surface, True, False))
        

        self.frame_count = 0
        self.animation_speed = 0.1
        self.image = self.animations["walk_right"][0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y + TILE_SIZE + 100)
        self.hitbox = self.rect.inflate(-8, -16)
        self.hitbox.midbottom = self.rect.midbottom

        self.direction.x = 1
        self.speed = 2

    def trigger_horizontal_collision(self):
        self.direction.x *= -1

    def update(self, collision_group):
        super().update(collision_group)

        suffix = ""
        if self.direction.x > 0 :
            suffix = "_right"
        elif self.direction.x < 0:
            suffix = "_left"

        animation = "walk"
        if self.status == "stun":
            animation = "idle"
        
        animation += suffix

        # Play the animation
        frame = int(self.frame_count) % len(self.animations[animation])
        self.image = self.animations[animation][frame]

        self.frame_count += self.animation_speed

    

class EnemySpawner:

    def __init__(self, x, y, visible_group, enemy_group):
        self.timer = 5000
        self.trigger = 0

        self.visible_group = visible_group
        self.enemy_group = enemy_group
        self.x = x
        self.y = y

    def update(self):
        ticks = pygame.time.get_ticks()

        if ticks - self.trigger > self.timer:
            slug = Slug(self.x, self.y, self.visible_group, self.enemy_group)
            self.trigger = ticks





        

