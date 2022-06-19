import re
import pygame
import player
import letter
import present_word
import ui
import random
import custom_group
import enemy 
import menu
from Settings import *




class World:
    def __init__(self):
        self.horizontal_platform_middle = pygame.image.load(os.path.join("data", "ground", "middle_pencil.png")).convert()
        self.horizontal_platform_middle = pygame.transform.scale(self.horizontal_platform_middle, (TILE_SIZE, TILE_SIZE))
        self.horizontal_platform_start = pygame.image.load(os.path.join("data", "ground", "start_pencil.png")).convert_alpha()
        self.horizontal_platform_start = pygame.transform.scale(self.horizontal_platform_start, (TILE_SIZE, TILE_SIZE))
        self.horizontal_platform_end = pygame.image.load(os.path.join("data", "ground", "back_pencil.png")).convert_alpha()
        self.horizontal_platform_end = pygame.transform.scale(self.horizontal_platform_end, (TILE_SIZE, TILE_SIZE))

        self.vertical_platform_middle = pygame.image.load(os.path.join("data", "ground", "middle_pencil_vert.png")).convert()
        self.vertical_platform_middle = pygame.transform.scale(self.vertical_platform_middle, (TILE_SIZE, TILE_SIZE))
        self.vertical_platform_start = pygame.image.load(os.path.join("data", "ground", "start_pencil_down.png")).convert_alpha()
        self.vertical_platform_start = pygame.transform.scale(self.vertical_platform_start, (TILE_SIZE, TILE_SIZE))
        self.vertical_platform_end = pygame.image.load(os.path.join("data", "ground", "back_pencil_top.png")).convert_alpha()
        self.vertical_platform_end = pygame.transform.scale(self.vertical_platform_end, (TILE_SIZE, TILE_SIZE))


        all_platforms = [self.horizontal_platform_middle,
            self.vertical_platform_middle]
        self.winning = False

        # Reduce contrast
        for platform in all_platforms:
            rect = platform.get_rect()
            surface = pygame.Surface((rect.width, rect.height))
            surface.fill((255, 255, 255))
            surface.set_alpha(70)

            platform.blit(surface, (0,0))



        self.ground_top = pygame.image.load(GROUND_TOP).convert()
        self.ground_topleft = pygame.image.load(GROUND_TOPLEFT).convert_alpha()
        self.ground_left = pygame.image.load(GROUND_LEFT).convert()
        self.ground_bulk = pygame.image.load(GROUND_BULK).convert()
        self.ground_right = pygame.transform.flip(self.ground_left, True, False)
        self.ground_topright = pygame.transform.flip(self.ground_topleft, True, False)
        self.ground_leftright =  pygame.image.load(GROUND_LEFTRIGHT).convert()
        self.ground_topleftright =  pygame.image.load(GROUND_TOPLEFTRIGHT).convert_alpha()


        self.ground_top = pygame.transform.scale(self.ground_top, (TILE_SIZE, TILE_SIZE))
        self.ground_topleft = pygame.transform.scale(self.ground_topleft, (TILE_SIZE, TILE_SIZE))
        self.ground_left = pygame.transform.scale(self.ground_left, (TILE_SIZE, TILE_SIZE))
        self.ground_bulk = pygame.transform.scale(self.ground_bulk, (TILE_SIZE, TILE_SIZE))
        self.ground_right = pygame.transform.scale(self.ground_right, (TILE_SIZE, TILE_SIZE))
        self.ground_topright = pygame.transform.scale(self.ground_topright, (TILE_SIZE, TILE_SIZE))
        self.ground_leftright = pygame.transform.scale(self.ground_leftright, (TILE_SIZE, TILE_SIZE))
        self.ground_topleftright = pygame.transform.scale(self.ground_topleftright, (TILE_SIZE, TILE_SIZE))


        self.target_word = None

        # Background properties
        #self.background = pygame.Surface((64, 64))
        #self.background.fill((0, 0, 50))
        self.background = pygame.image.load(os.path.join(DATA_DIR, "background.png")).convert()
        new_dim = [self.background.get_rect().width * SCALE_FACTOR,
            self.background.get_rect().height * SCALE_FACTOR]
        self.background = pygame.transform.scale(self.background, new_dim)
        self.distance_factor = 0.2


        # The font properties
        self.font_small = pygame.font.Font(FONT_LOCATION, FONT_SIZE_SMALL)
        self.font_title = pygame.font.Font(FONT_LOCATION, FONT_SIZE_TITLE)

        # Menu 
        self.menu = menu.Menu(["Start Game", "Main Menu"], fixed_message=["Pause"], fixed_color=(10, 10, 10))
        self.final_menu = None
        self.display_final_menu = False
        self.display_menu = False
        """
        self.loading_surface = pygame.Surface(WINDOW_SIZE)
        self.loading_surface.fill((0,0,0))
        text_surf = self.font_title.render("Loading level ...", False, (255, 255, 255), (0,0,0))
        text_rect = text_surf.get_rect()
        text_rect.center = (WINDOW_SIZE[0]//2, WINDOW_SIZE[1] // 2)
        self.loading_surface.blit(text_surf, text_rect)
        """
        
        self.player = None
        self.tiles = []


        self.camera = pygame.math.Vector2(0,0)

        self.visible_group = custom_group.MyGroup(self.camera)
        self.collision_group = pygame.sprite.Group()
        self.collectable_group = pygame.sprite.Group()
        self.winning_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.spawners = []

        # Intro camera
        self.trigger_start = 0
        self.timer_camera_move = 1000
        self.timer_camera_stop = 500
        self.correct_letter_positions = []
        self.is_in_intro = True



        # General info
        self.pause = False
        self.level = 0
        self.max_level = len([x for x in os.listdir(DATA_DIR) if x.startswith("level_") and x.endswith(".txt")])
        self.ui = ui.UserInterface(self.player, self.font_title)

        # Music
        self.clock_sound = pygame.mixer.Sound(os.path.join("data", "audio", "clock.wav"))
        self.clock_sound.set_volume(0.005)
        self.clock_playing = False

        self.win_sound = pygame.mixer.Sound(os.path.join("data", "win.wav"))
        self.win_sound.set_volume(0.8)

        self.defeat_sound = pygame.mixer.Sound(os.path.join("data", "defeat.wav"))
        self.defeat_sound.set_volume(0.8)

        self.music = pygame.mixer.Sound(os.path.join(DATA_DIR, "superbook.wav"))
        self.music_volume = 0.4
        self.music_pause_volume = 0.1
        self.music.set_volume(self.music_volume)
        self.music.play(-1)

    
    def __setattr__(self, __name, __value):
        if __name == "player":
            if "ui" in self.__dict__:
                self.ui.player = __value   

        super().__setattr__(__name, __value)
    
        
    
    def save(self):
        with open(SAVE_FILE, "w") as fp:
            fp.write(str(self.level))


    def load(self):
        if not os.path.exists(SAVE_FILE):
            self.save()

        with open(SAVE_FILE, "r") as fp:
            self.level = int(fp.read().strip())

        self.start_level()


    def background_blit(self, screen):
        origin = -self.camera * self.distance_factor
        
        screen_width = screen.get_rect().width
        screen_height = screen.get_rect().height

        background_width = self.background.get_rect().width
        background_height = self.background.get_rect().height


        origin.x = origin.x % background_width - background_width
        origin.y = origin.y % background_height - background_height


        start_x = origin.x
        while start_x < screen_width:
            start_y = origin.y
            while start_y < screen_width:
                screen.blit(self.background, (start_x, start_y))
                start_y += background_height
            start_x += background_width

    """
    def check_death(self):
        if self.player.remaining_oil <= 0:
            return True
        return False
    """


    def paused(self):
        return self.pause or self.display_final_menu or self.is_in_intro

    def update_music(self):
        if not self.paused():
            self.music.set_volume(self.music_volume)
        else:
            self.music.set_volume(self.music_pause_volume)


    def check_win(self):

        if len(self.collectable_group) == 0 or self.player.timer <= 0:
            if not self.pause:
                score = self.ui.get_score()
                win_condition = score > .5 and self.player.timer > 0
                self.winning = win_condition

                if win_condition:
                    self.final_menu = menu.Menu(["Next Level", "Retry", "Main Menu"], fixed_message=["Contratulations!"], burst=True)
                    self.win_sound.play()

                else:
                    self.defeat_sound.play()
                    message = ["The order of letters", "is important!"]
                    if self.player.timer <= 0:
                        message = ["Out of time!"]
                    self.final_menu = menu.Menu(["Retry", "Main Menu"], fixed_message=message, fixed_color=(180, 20, 20)) 

            return True
        return False
        for sprite in self.winning_group.sprites():
            if sprite.rect.colliderect(self.player.hitbox):
                return True
        return False

    def update_clock_sound(self):
        if self.pause or self.display_menu:
            self.clock_sound.set_volume(0)
            if self.clock_playing:
                self.clock_sound.stop()
                self.clock_playing = False
        else:
            if not self.clock_playing:
                self.clock_sound.play(-1)
                self.clock_playing = True
            remaining_time = self.player.timer
            if remaining_time > 15:
                volume = 0.0005
            else:   
                volume = 1 / (1 + .2 * remaining_time**2)
            self.clock_sound.set_volume(volume)



    def blit_text_on_center(self, text, surface, below = None, offset = 50):

        text_surface = self.font_title.render(text, False, (255, 255, 255), (0,0,0))
        text_surface.set_colorkey((0,0,0))

        text_rect = text_surface.get_rect()
        screen_rect = surface.get_rect()

        text_rect.center = screen_rect.center

        if below is not None:
            text_rect.midtop = below.midbottom
            text_rect.y += offset


        surface.blit(text_surface, text_rect)
        return text_rect


    def check_enemy_collision(self):
        for sprite in self.enemy_group.sprites():
            if self.player.hitbox.colliderect(sprite.hitbox):
                good_collision = self.player.push_back(sprite.push_back, sprite.direction.x - self.player.direction.x)
                if len(self.ui.current_word) and good_collision:
                    char = self.ui.current_word.pop(-1)
                    x, y =  self.ui.original_positions.pop(-1)
                    letter.Letter(x, y, char, self.visible_group, self.collectable_group)

                # Stop the enemy from walking
                sprite.stun_trigger = pygame.time.get_ticks()

    def check_pause(self):
        keys = pygame.key.get_pressed()
        ticks = pygame.time.get_ticks()
        if (keys[pygame.K_RETURN]) and ticks - self.menu.check_return > self.menu.return_timeout:
            self.menu.check_return = ticks

            if self.pause == False:
                self.menu.focus = 0
            self.pause = True
            self.display_menu = True
        if not keys[pygame.K_RETURN]:
            self.menu.check_return = 0


    def camera_intro(self):

        ticks = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Targets of the came
        targets = [self.player.rect.center]
        for lpos in self.correct_letter_positions:
            targets.append(lpos)
        targets.append(self.player.rect.center)

        total_camera_time = self.timer_camera_move * (len(targets) - 1)
        total_camera_time += self.timer_camera_stop * len(targets)

        if ticks - self.trigger_start < total_camera_time:
            self.is_in_intro = True

            camera_time = ticks - self.trigger_start

            start_index = 0
            end_index = 0
            current_timer = camera_time
            #start_time = 0
            #end_time = 0
            while camera_time > 0:

                camera_time -=  self.timer_camera_stop
                if camera_time < 0:
                    break
                
                end_index += 1

                current_timer = camera_time
                camera_time -= self.timer_camera_move
                if camera_time > 0:
                    start_index += 1

            if start_index > 0:
                if keys[pygame.K_RETURN]:
                    self.trigger_start -= 100000

            
            direction = pygame.math.Vector2(targets[end_index][0],targets[end_index][1])
            direction.x -= targets[start_index][0]
            direction.y -= targets[start_index][1]

            camera_pos = [x for x in targets[start_index]]
            ratio_time = current_timer / self.timer_camera_move
            camera_pos[0] += direction.x * ratio_time
            camera_pos[1] += direction.y * ratio_time

            screen_rect = pygame.display.get_surface().get_rect()
            self.camera.x = camera_pos[0] - screen_rect.width / 2
            self.camera.y = camera_pos[1] - screen_rect.height / 2

        else:
            self.is_in_intro = False

    def reset(self):
        self.ui.current_word = []
        self.pause = False
        self.display_final_menu = False
        self.display_menu = False


    def update(self, screen):
        # Update all 

        self.update_clock_sound()

        self.update_music()

        self.camera_intro()


        if not self.pause and not self.display_menu and not self.is_in_intro:
            self.check_pause()
            self.visible_group.update(self.collision_group)

            for spawner in self.spawners:
                spawner.update()

            
            self.player.update_camera(self.camera, screen.get_width(), screen.get_height())
        
        
            self.check_enemy_collision()

        self.player.update_collectable(self.collectable_group, self.ui, self.visible_group)
        #for sprite in self.visible_group.sprites():
        #    sprite.update_rect(self.camera)

        self.background_blit(screen)
        self.visible_group.draw(screen)

        # Update the User Interface
        self.ui.draw()

        if self.check_win():
            self.display_final_menu = True


        if self.display_final_menu:
            self.pause = True
            result = self.final_menu.update()
            if result is not None:
                self.pause = False

                return_value =  {"result": self.winning, "word" : [x for x in self.ui.current_word]}
                self.ui.current_word = []

                return_value["action"] = result
                self.display_final_menu = False
                return return_value
            self.final_menu.draw(screen)




        if self.display_menu:
            result = self.menu.update()
            if result is not None:
                if result == "Start Game":
                    self.display_menu = False
                    self.pause = False
                    """
                elif result == "Save":
                    self.save()

                    self.display_menu = False
                    self.pause = False

                elif result == "Load":
                    self.display_menu = False
                    self.pause = False

                    # Play again the music
                    self.load()
                    """

                elif result == "Main Menu":
                    self.display_menu = False
                    self.pause = False
                    return_value =  {"result": False, "word" : [], "action":"Main Menu"}
                    return return_value

            self.menu.draw(screen)

        # Check death
        """
        if self.check_death():

            if self.pause == False:
                self.player.sound_death.play()
            self.pause = True

            t1 = self.blit_text_on_center("The moster of darkness got you!", screen)
            t2 = self.blit_text_on_center("Press enter to restart...", screen, below = t1)

            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.start_level()
                self.pause = False
        """
        """
        if self.check_win():

            if self.pause == False:
                self.level += 1
                self.player.sound_target.play()
            self.pause = True

            if self.level < self.max_level:
                t1 = self.blit_text_on_center("Huppy! We got an escape!", screen)
                t2 = self.blit_text_on_center("Press enter to continue...", screen, below = t1)
            else:
                # We finished the game
                t1 = self.blit_text_on_center("GAME COMPLETED!", screen)
                t2 = self.blit_text_on_center("Press enter to restart the game", screen, below = t1)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:

                if self.level == self.max_level:
                    self.level = 0
                self.start_level()
                self.pause = False
        """

    def start_level(self):
        self.reset()
        # Reset the group
        self.collision_group.empty()
        self.visible_group.empty()
        self.collectable_group.empty()
        self.winning_group.empty()
        self.enemy_group.empty()

        self.player = None
        self.ui.current_word = []

        level_file = os.path.join(DATA_DIR, "level_{}.txt".format(self.level))
        
        screen = pygame.display.get_surface()
        #screen.blit(self.loading_surface, (0,0))
        pygame.display.flip()
        self.create_world(level_file)

        # Create the word shower
        present_word.PresentWord(self.ui.target_word).run()

        self.trigger_start = pygame.time.get_ticks()
        



    def update_tile_images(self, maxx):
        for tile in self.visible_group:
            if tile.kind != "tile":
                continue

            has_left = False
            has_right = False
            has_top = False
            has_bottom = False

            for secondtile in self.visible_group:
                if secondtile.kind != "tile":
                    continue

                delta_x = tile.rect.x - secondtile.rect.x

                if delta_x <= - 2*TILE_SIZE or delta_x >= 2*TILE_SIZE:
                    continue

                delta_y = tile.rect.y - secondtile.rect.y
                if delta_y <= - 2*TILE_SIZE or delta_y >= 2*TILE_SIZE:
                    continue

                if abs(delta_x - TILE_SIZE) < EPSILON and abs(delta_y) < EPSILON:
                    has_left = True
                elif abs(delta_x + TILE_SIZE) < EPSILON and abs(delta_y) < EPSILON:
                    has_right = True
                
                if abs(delta_y  - TILE_SIZE) < EPSILON and abs(delta_x) < EPSILON:
                    has_top = True

                if abs(delta_y  + TILE_SIZE) < EPSILON and abs(delta_x) < EPSILON:
                    has_bottom = True

                #print("TILE AT: {} AND {}: L:{} R:{} T:{}".format( (tile.x// TILE_SIZE, tile.y//TILE_SIZE),
                #    (secondtile.x// TILE_SIZE, secondtile.y//TILE_SIZE),
                #    has_left, has_right, has_top))

            
            
            if has_left and has_right and has_top and has_bottom:
                tile.image = self.vertical_platform_middle
            elif has_left and has_right and not has_top and not has_bottom:
                tile.image = self.horizontal_platform_middle
            elif not has_left and has_right and not has_top and not has_bottom:
                tile.image = self.horizontal_platform_start 
            elif has_left and not has_right and not has_top and not has_bottom:
                tile.image = self.horizontal_platform_end
            elif not has_top:
                tile.image = self.vertical_platform_end
            elif not has_bottom:
                tile.image = self.vertical_platform_start    
            else:
                tile.image = self.vertical_platform_middle
            
            #else:
            #    tile.image = self.ground_bulk
                


    def create_world(self, data_file = DATA_WORLD, offset_tiles = 5):
        maxx = 0
        maxy = 0

        self.winning = False

        total_lamps = 0
        with open(data_file, "r") as fp:
            lines = fp.readlines()
        
        self.target_word = lines.pop(0).strip()
        self.ui.target_word = self.target_word

        # Total time is 5 seconds per letter
        total_time = 6 * len(self.target_word)
        if len(self.target_word) > 6:
            total_time += 5 * (len(self.target_word) - 6)


        shuffle_letters = list(self.target_word)
        random.shuffle(shuffle_letters)

        # Get the letter position
        ordered_indices = []
        remaining_indices = [i for i in range(len(shuffle_letters))]
        for good_index, char in enumerate(shuffle_letters):
            for i in range(len(remaining_indices) - 1, -1, -1):
                index = remaining_indices[i]

                if char == self.target_word[index]:
                    ordered_indices.append(index)
                    remaining_indices.pop(i)
                    break
                    
        self.correct_letter_positions = [None] * len(self.target_word)
        appended_order = [None] * len(self.target_word)
        letter_index = 0

        
        for yindex, line in enumerate(lines):
            for xindex, character in enumerate(line):
                x = xindex * TILE_SIZE
                y = yindex * TILE_SIZE

                if x > maxx:
                    maxx = x
                if y > maxy: 
                    maxy = y

                if character == "1":
                    Tile(x, y, self.visible_group, self.collision_group)
                elif character == "P":
                    self.player = player.Player(x, y, self.visible_group)
                    self.player.timer = total_time
                elif character == "W":
                    lchar =  shuffle_letters.pop(0)
                    letter.Letter(x, y, lchar, self.visible_group, self.collectable_group)
                    self.correct_letter_positions[ordered_indices[letter_index]] = (x, y)
                    appended_order[ordered_indices[letter_index]] = lchar
                    letter_index += 1
                elif character == "E":
                    enemy.Eraser(x, y, self.visible_group, self.enemy_group)
                elif character == "O":
                    self.spawners.append(enemy.EnemySpawner(x, y, self.visible_group, self.enemy_group))
                else:
                    continue

        #if self.player is not None:
        #    self.visible_group.move_to_front(self.player)

        # Fill the border with tiles
        for x in range(-1, offset_tiles):
            for y in range(offset_tiles):
                # Create the tiles in the corners
                Tile(-(x+1) * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + (x+1) * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(-(x+1) * TILE_SIZE, maxy +(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx + (x + 1) * TILE_SIZE, maxy + (1 + y) * TILE_SIZE, self.visible_group, self.collision_group)

        
        for x in range( offset_tiles):
            for y in range(maxy // TILE_SIZE + 1):
                Tile(-(x+1) * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(maxx+ (x) * TILE_SIZE, y * TILE_SIZE, self.visible_group, self.collision_group)

        for y in range(offset_tiles):
            for x in range(maxx // TILE_SIZE):
                Tile(x * TILE_SIZE, -(y+1) * TILE_SIZE, self.visible_group, self.collision_group)
                Tile(x * TILE_SIZE, maxy + (1 + y) * TILE_SIZE, self.visible_group, self.collision_group)


        self.update_tile_images(maxx)

        #self.ui.reset_counter(total_lamps)



class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self._layer = 1
        self.kind = "tile"
        self.image = pygame.Surface((64, 64))
        self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.friction = 0.18


    def update(self, dumb = None):
        pass


