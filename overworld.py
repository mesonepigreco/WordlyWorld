import pygame
import sys, os

from Settings import *
import json
import ui
import level
import credits

class OverWorld:

    def __init__(self):

        self.normal_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU_B)
        self.small_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE_MENU)
        self.word_font = pygame.font.Font(FONT_LOCATION, FONT_TITLE_B)

        self.press_start_sound = pygame.mixer.Sound(os.path.join("data", "audio", "collect.wav"))
        self.select_sound = pygame.mixer.Sound(os.path.join("data", "audio", "select.wav"))


        self.background_color = ((255, 255, 255))
        self.text_color = ((10,10,10))
        self.word_color = ((50, 180, 50))
        self.bare_color = ((180,180, 50))
        self.bad_color = ((180, 50, 50))

        self.book_image = pygame.image.load(os.path.join("data", "book", "book.png")).convert_alpha()
        self.book_image = pygame.transform.scale(self.book_image, (TILE_SIZE, TILE_SIZE))
        self.book_rect = self.book_image.get_rect()

        self.start_timer = -1000
        self.total_time = 4000
        self.initial_timeout = 100

        self.focus = 0
        self.world = level.World()

        self.current_progress = {"guessed_words" : []}
        self.fname = "player_progress.json"

        self.level_surfaces = []

        self.focus_color = (255, 50, 50)
        self.focus = 0
        self.n_levels = 0
        self.target_words = []

        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.leftright_margin = 32
        self.hspace = 32
        self.wspace = 32

        self.max_selectable_level = 0

    def read_all_words(self):
        levels = [x for x in os.listdir("data") if x.startswith("level_") and x.endswith(".txt")]

        self.n_levels = len(levels)

        for i in range(self.n_levels):
            with open(os.path.join("data", "level_{:d}.txt".format(i)), "r") as fp:
                for j, line in enumerate(fp.readlines()):
                    if j == 0:
                        self.target_words.append(line.strip())
                        break

        while len(self.current_progress["guessed_words"]) < self.n_levels:
            self.current_progress["guessed_words"].append(None)


    def create_level_surface(self, level_id):
        guessed_word = self.current_progress["guessed_words"][level_id]
        surface = pygame.Surface((self.screen_rect.width - 2*self.leftright_margin, 
            self.screen_rect.height / 6 - self.hspace))
        
        surface_rect = surface.get_rect()

        if level_id != self.focus:
            surface.fill((10, 10, 10))
        else:
            surface.fill(self.focus_color)
        inner_rect = surface_rect.inflate(-16, -16)
        inner_rect.center = surface_rect.center
        pygame.draw.rect(surface, (255,255,255), inner_rect)

        # Draw the level text
        text = self.small_font.render("Lvl. {:d}".format(level_id+1), False, self.text_color, (0,0,0)).convert_alpha()
        text.set_colorkey((0,0,0))

        text_rect = text.get_rect()
        text_rect.midleft = inner_rect.midleft
        text_rect.x += self.wspace // 4

        surface.blit(text, text_rect)

        self.background_image = pygame.image.load(os.path.join("data", "SplashScreen.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, WINDOW_SIZE)
        self.background_image.set_colorkey((0,0, 255))



        # Find out if the word has been guessed
        if guessed_word is None:
            text_target = self.small_font.render("???", False, self.bad_color, 
                (0,0,0))

            text_guess = self.small_font.render("???", False, self.bad_color, 
                (0,0,0))

            text_score = self.small_font.render("??/??", False, self.bad_color, 
                (0,0,0))
        else:
            text_target = self.small_font.render(self.target_words[level_id], False, self.text_color, 
                (0,0,0))

            score = ui.similar(self.target_words[level_id], guessed_word)
            
            # Produce a color that shifts from yellow to green
            # As the score increases
            score_factor = 2 * (score - .5)
            score_color = [0,0,0]
            for k in range(3):
                x = self.bare_color[k]
                y = self.word_color[k]
                score_color[k] = int(x + (y - x) * score_factor)

            text_guess = self.small_font.render(guessed_word, False, score_color, 
                (0,0,0))
            
            text_score = self.small_font.render("{:.0f}/10".format(score * 10), False, score_color, 
                (0,0,0))

        
        text_target.set_colorkey((0,0,0))
        text_guess.set_colorkey((0,0,0))
        text_score.set_colorkey((0,0,0))

        rect_target = text_target.get_rect()
        rect_guess = text_guess.get_rect()
        rect_score = text_score.get_rect()

        rect_target.midleft = surface_rect.midleft
        rect_target.x += surface_rect.width * 0.255
        rect_guess.midleft = surface_rect.midleft
        rect_guess.x += surface_rect.width * 0.65
        rect_score.midright = inner_rect.midright
        rect_guess.x -= self.wspace * 2

        surface.blit(text_target, rect_target)
        surface.blit(text_guess, rect_guess)
        surface.blit(text_score, rect_score)

        return surface


    def build_levels(self):
        print("N LEVELS:", self.n_levels)
        self.level_surfaces = []
        for i in range(self.n_levels):
            self.level_surfaces.append(self.create_level_surface(i))

            # Show at least 1 extra level to be selected
            if self.current_progress["guessed_words"][i] is None:
                self.max_selectable_level = i
                break
        
        print("CURRENT PROGRESS:", self.current_progress)
    
    def init(self):
        self.read_all_words()
        self.load()
        self.build_levels()


    def load(self):
        if os.path.exists(self.fname):
            with open(self.fname, "r") as fp:
                self.current_progress = json.load(fp)


    def save(self):
        with open(self.fname, "w") as fp:
            json.dump(self.current_progress, fp)

    def draw(self):
        # TODO: Draw a background
        self.screen.fill((50, 255, 50))
        self.screen.blit(self.background_image, (0,0))

        smooth_surface = pygame.Surface(WINDOW_SIZE)
        smooth_surface.fill((255, 255, 255))
        smooth_surface.set_alpha(180)
        self.screen.blit(smooth_surface, (0,0))


        # Select level surface
        select_level_text = self.normal_font.render("Select the level", False, self.text_color, (0,0,0)).convert_alpha()
        select_level_text.set_colorkey((0,0,0))
        select_level_rect = select_level_text.get_rect()
        select_level_rect.midtop = self.screen_rect.midtop
        select_level_rect.y += self.hspace

        self.screen.blit(select_level_text, select_level_rect)

        n_display = 4 # How many surface to display
        start = self.focus - 2
        if start < 0:
            start = 0

        current_top = select_level_rect.bottom + self.hspace

        for i in range(n_display):
            level_index = start + i

            if level_index >= len(self.level_surfaces):
                break

            # Draw the surfaces
            surf = self.level_surfaces[level_index]
            rect = surf.get_rect()
            rect.top = current_top
            rect.centerx = self.screen_rect.centerx

            self.screen.blit(surf, rect)

            current_top += rect.height + self.hspace

            if self.focus == level_index:
                # Draw the book image
                self.book_rect.center = rect.bottomleft
        
        self.screen.blit(self.book_image, self.book_rect)

    def can_press_return(self):
        ticks = pygame.time.get_ticks()
        if ticks - self.start_timer > self.initial_timeout:
            return True 
        return False

    def run(self):

        screen = pygame.display.get_surface()
        self.start_timer = pygame.time.get_ticks()


        clock = pygame.time.Clock()
        running = True

        self.focus = len(self.level_surfaces) - 1
        self.build_levels()



        in_level = False
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
                if not in_level:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and self.can_press_return():
                            self.press_start_sound.play()
                            self.world.level = self.focus
                            self.world.start_level()
                            in_level = True
                        elif event.key == pygame.K_UP:
                            if self.focus > 0:
                                self.select_sound.play()
                                self.focus -= 1
                        elif event.key == pygame.K_DOWN:
                            if self.focus < len(self.level_surfaces) - 1:
                                self.select_sound.play()
                                self.focus += 1
                        
                        print("FOCUS:", self.focus)
                        self.build_levels()
            
            if in_level:
                result = self.world.update(self.screen)
                #print("RESULTED IN :", result)

                if result is not None:
                    if result["result"]:
                        old_word = self.current_progress["guessed_words"][self.world.level]
                        new_word = "".join(result["word"])

                        print("WORDS:", old_word, self.target_words[self.world.level])
                        if old_word is None:
                            max_score = -1
                        else:
                            max_score = ui.similar(self.target_words[self.world.level], old_word)
                        current_score = ui.similar(self.target_words[self.world.level], new_word)

                        if current_score > max_score:
                            self.current_progress["guessed_words"][self.world.level] = new_word
                            self.save()
                            self.build_levels()


                        # If we won the last level show the credits
                        if self.world.level == self.n_levels - 1:
                            cc = credits.Credits()
                            cc.run()
                    
                    if result["action"] == "Main Menu":
                        in_level = False
                        self.start_timer = pygame.time.get_ticks()
                    elif result["action"] == "Next Level":
                        if self.focus < self.n_levels - 1:
                            self.focus += 1
                            self.world.level = self.focus
                            self.world.reset()
                            self.world.start_level()
                        else:
                            in_level = False
                    elif result["action"] == "Retry":
                        self.world.reset()
                        self.world.start_level()
                    
            else:
                self.draw()



            pygame.display.flip()




