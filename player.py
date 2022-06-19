import pygame
import os
import math
import particles
from Settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kind = "player"
        self._layer = 2

        self.timer = 0


        #self.image = pygame.Surface((64, 64*2))
        #self.image.fill(PLAYER_COLOR)
        miner_img_path = os.path.join("data", "miner", "miner.png")
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 0))

        self.image = pygame.image.load(os.path.join("data", "book", "book.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, 1.5*TILE_SIZE))

        #self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))


        self.facing_right_surface = self.image.copy()
        self.facing_left_surface = pygame.transform.flip(self.image, True, False)


        # Load animations
        self.animations = {
            "fall_left" : [self.facing_left_surface],
            "fall_right" : [self.facing_right_surface],
            "idle_left" : [self.facing_left_surface],
            "idle_right" : [self.facing_right_surface],
            "walk_left" : [self.facing_left_surface],
            "walk_right" : [self.facing_right_surface]}

        self.load_animations( os.path.join("data", "book"), "walk_right", "walk", 3, 0, flip = False)
        self.load_animations( os.path.join("data", "book"), "walk_left", "walk", 3, 0, flip = True)

        self.load_animations( os.path.join("data", "book"), "idle_right", "idle_right", 17, 4, flip = False)
        self.load_animations( os.path.join("data", "book"), "idle_left", "idle_right", 17, 4, flip = True)

        #self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "idle"), "idle_right", "idle", 13, 6, False)
        #self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "idle"), "idle_left", "idle", 13, 6, True)
        #self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "fall"), "fall_right", "fall", 18, 13, False)
        #self.load_animations( os.path.join(PLAYER_ANIMATION_DATA, "fall"), "fall_left", "fall", 18, 13, True)

        self.status = "idle"
        self.current_frame = 0

        self.animation_speed = {"idle" : 0.15, "walk" : 0.15, "fall" : 0.15}


        # Hitbox and rect
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y + TILE_SIZE)

        self.hitbox = self.rect.inflate(-20, 0)

        # Moovment
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4.3
        self.jump_speed = 5.6

        self.is_going_left = False
        self.is_going_right = True
        self.is_grounded = False
        self.current_friction = 0

        # Triggers
        self.trigger_onfalling = 0 
        self.onfalling_timeout = 100
        self.trigger_onceiling = 0
        self.onceiling_timeout = 200
        self.trigger_jump = 0
        self.jump_timeout = 150
        self.slowdown_gravity = 0.2
        self.trigger_stun = -10000
        self.stun_timeout = 500
        self.immortality_timeout = 1200


        # Sounds
        
        self.sound_jump = pygame.mixer.Sound(os.path.join(DATA_DIR, "audio", "jump.wav"))
        self.sound_hit = pygame.mixer.Sound(os.path.join(DATA_DIR, "audio", "hit.wav"))
        self.sound_boing = pygame.mixer.Sound(os.path.join(DATA_DIR, "audio", "boing.wav"))
        #self.sound_target = pygame.mixer.Sound(os.path.join(DATA_DIR, "sounds", "target.wav"))
        #self.sound_death = pygame.mixer.Sound(os.path.join(DATA_DIR, "sounds", "death.wav"))
        self.sound_collect = pygame.mixer.Sound(os.path.join(DATA_DIR, "audio", "collect.wav"))

        #self.sound_death.set_volume(0.1)
        self.sound_boing.set_volume(0.3)
        self.sound_jump.set_volume(0.3)
        self.sound_collect.set_volume(0.5)
        self.sound_hit.set_volume(0.8)
        
    


    def load_animations(self, directory, animation_name, basename, end_frame, start_frame = 0, flip = False):
        frames = []
        for i in range(start_frame, end_frame):
            filename = os.path.join(directory, "{}{:04d}.png".format(basename, i))
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE, 1.5*TILE_SIZE))
            if flip:
                image = pygame.transform.flip(image, True, False)
            frames.append(image)
        
        self.animations[animation_name] = frames
            


    def update_rect(self):
        self.rect.center = self.hitbox.center
    

    def update_status(self):
        if self.is_grounded:
            if abs(self.direction.x) > EPSILON:
                self.status = "walk"
            else:
                self.status = "idle"
        else:
            self.status = "fall" 


    def update_image(self):
        current_animation = self.status + "_"
        if self.is_going_left:
            current_animation += "left"
        elif self.is_going_right:
            current_animation += "right"
        
        # Update frames
        self.current_frame += self.animation_speed[self.status]

        animation = self.animations[current_animation]

        total_frames = len(animation)
        self.image = animation[int(self.current_frame) % total_frames]

        ticks = pygame.time.get_ticks()

        if ticks - self.trigger_stun < self.immortality_timeout:
            transparency = math.sin(2 * math.pi * ticks / 50)
            transparency += 1
            transparency /= 2
            transparency *= 255
            self.image.set_alpha(int(transparency))
        else:
            self.image.set_alpha(255)


    def update_collectable(self, collectable_group, ui_menu, visible_group):
        ticks = pygame.time.get_ticks()

        if ticks - self.trigger_stun > self.immortality_timeout:
            for sprite in collectable_group.sprites():
                if sprite.rect.colliderect(self.hitbox):
                    if sprite.kind == "letter":

                        ui_menu.current_word.append(sprite.letter)
                        ui_menu.original_positions.append((sprite.x, sprite.y))
                        self.sound_collect.play()
                        sprite.kill()

                        # Add a small particle bust
                        particles.sparkles_burst(visible_group, self.rect.center, 25)


    def update(self, collision_group):
        self.update_direction()

        self.update_image()

        self.hitbox.x += self.direction.x * self.speed
        self.detect_collistions(collision_group, left_right= True)
        self.hitbox.y += self.direction.y * self.speed
        self.detect_collistions(collision_group, left_right=False)


        self.update_rect()

        self.update_status()

        self.timer -= 1 / 60 # Remove 1 second each 60 frames



    def update_camera(self, camera_origin, screen_width, screen_height):
        # Player specific stuff
        player_vector = pygame.math.Vector2(self.hitbox.x,self.hitbox.y) + pygame.math.Vector2(self.rect.width / 2, self.rect.height / 2)
        dist_vect = player_vector - camera_origin

        if self.kind == "player":
            if dist_vect.x > screen_width - CAMERA_XBORDER:
                camera_origin.x = player_vector.x - screen_width + CAMERA_XBORDER
            elif dist_vect.x < CAMERA_XBORDER:
                camera_origin.x = player_vector.x - CAMERA_XBORDER


            if dist_vect.y  > screen_height - CAMERA_YBORDER:
                camera_origin.y = player_vector.y - screen_height + CAMERA_YBORDER
            elif dist_vect.y < CAMERA_YBORDER:
                camera_origin.y = player_vector.y - CAMERA_YBORDER
        



    def detect_collistions(self, collision_group, left_right = True):
        
        is_colliding = False

        for sprite in collision_group.sprites():
            if sprite.rect.colliderect(self.hitbox):
                is_colliding = True

                if left_right:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                        self.current_friction = sprite.friction
                        if not self.is_grounded:
                            self.is_grounded = True
                            self.sound_boing.play()
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom 
                        self.trigger_onceiling = pygame.time.get_ticks()

                    self.direction.y = 0


        if not left_right:
            if not is_colliding:

                if self.is_grounded:
                    self.is_grounded = False
                    self.trigger_onfalling = pygame.time.get_ticks()

    def push_back(self, force, direction):
        ticks = pygame.time.get_ticks()

        if ticks - self.trigger_stun > self.immortality_timeout:
            self.sound_hit.play()
            self.direction.x = force * math.copysign(1, direction)
            
            self.trigger_stun = ticks

            return True
        return False


    def update_direction(self):
        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()

        moving_force = 1.8
        if ticks - self.trigger_stun > self.stun_timeout:


            if keys[pygame.K_LEFT]:
                self.direction.x = -moving_force
                self.is_going_left = True
                self.is_going_right= False
            elif keys[pygame.K_RIGHT]:
                self.direction.x = moving_force
                self.is_going_left = False
                self.is_going_right= True

    
        if self.is_grounded and self.direction.x != 0:
            sign =  math.copysign(1, self.direction.x)
            self.direction.x -= sign * self.current_friction 

            if sign * self.direction.x < 0:
                self.direction.x = 0
        else:
            self.direction.x -= self.direction.x * AIR_FRICTION
            if self.direction.y > 0:
                self.direction.y -= self.direction.y * AIR_FRICTION
            #self.is_going_left = False
            #self.is_going_right= False


        if keys[pygame.K_SPACE]:

            if ticks - self.trigger_jump > self.jump_timeout:
                if self.is_grounded or (ticks - self.trigger_onfalling) < self.onfalling_timeout :
                    self.direction.y = -self.jump_speed
                    self.trigger_jump = ticks
                    self.sound_jump.play()
            


        factor = 1
        if ticks - self.trigger_onceiling < self.onceiling_timeout:
            factor = self.slowdown_gravity
        
        self.direction.y += GRAVITY * factor
        if self.direction.y > MAX_VERTICAL_SPEED:
            self.direction.y = MAX_VERTICAL_SPEED


