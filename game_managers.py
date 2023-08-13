import pygame
from random import randint
import json


class MusicManager:
    def __init__(self):
        self.magic_space = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/magic space.mp3") #in_game music1
        self.space_heroes = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/Space Heroes.ogg") #in_game music2
        self.brave_pilots = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/Brave Pilots (Menu Screen).ogg") # in_start_menu
        self.victory_tune = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/Victory Tune.ogg") #at the end
        self.boss_theme = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/DeathMatch (Boss Theme).ogg") #last lvl
        self.game_over_tune = pygame.mixer.Sound("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/Defeated (Game Over Tune).ogg") #game_over_menu
        self.musics = {"magic_space":self.magic_space,
                       "space_heroes":self.space_heroes,
                       "brave_pilots":self.brave_pilots,
                       "victory_tune":self.victory_tune,
                       "boss_theme": self.boss_theme,
                       "game_over_tune": self.game_over_tune,}

        self.current_music_name = ""

        # magic space

    def set_music(self,music_name):
        self.current_music_name = music_name

    def play_music(self, music_name):
        if music_name == self.current_music_name:
            self.musics[music_name].play(loops = -1)
        else:
            pygame.mixer.stop()
            self.set_music(music_name)
            self.musics[music_name].play(loops=-1)





class LvlManager:

    def save_player_progress_lvl(self):
        with open("save_file.txt","w") as save_file:
            json.dump(self.player_progress_dict,save_file)


    def __init__(self, game_font):
        # Game images
        self.lvl_images_dict = {1: pygame.transform.rotozoom(pygame.image.load("desolate_places/Cloudy Mountains.png").convert_alpha(),0, 3),
                                2: pygame.transform.rotozoom(pygame.image.load("desolate_places/Dusty Moon.png").convert_alpha(), 0, 3),
                                3: pygame.transform.rotozoom(pygame.image.load("desolate_places/Glowing Sea.png").convert_alpha(), 0, 3),
                                4: pygame.transform.rotozoom(pygame.image.load("desolate_places/Hidden Desert.png").convert_alpha(), 0,3),
                                5: pygame.transform.rotozoom(pygame.image.load("desolate_places/Misty Rocks.png").convert_alpha(), 0, 3),
                                6: pygame.transform.rotozoom(pygame.image.load("desolate_places/Starry Peaks.png").convert_alpha(), 0, 3)}

        # Lvl
        self.lvl = 1
        self.enemy_spawn_count_per_timer = 1
        self.max_lvl = 6
        self.is_lvl_finish = False
        self.lvl_length = 50
        self.lvl_background = self.lvl_images_dict[self.lvl]
        self.lvl_text = game_font.render("Lvl Progress: ",False, (255,255,255))
        self.lvl_text_rect = self.lvl_text.get_rect(center = (690,950))
        # Lvl progress mechanic
        self.progress = 0
        self.progress_bar_width = 200
        self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
        self.total_progress = 0
        self.max_progress = 600

        # updates every game
        self.game_finished = False

    def randomize_enemy_spawn(self):
        match self.lvl:
            case 1: return randint(1,3)
            case 2: return randint(1,4)
            case 3: return randint(1,5)
            case 4: return randint(1,6)
            case 5: return randint(1, 7)
            case 6: return randint(1,8)

    def increase_progress(self):
        if self.progress < self.lvl_length and self.total_progress < self.max_progress: self.progress += 10; self.total_progress += 10

    def Lvl_bar_update(self,music_manager):
        if self.lvl != self.max_lvl:
            self.lvl += 1

        self.lvl_background = self.lvl_images_dict[self.lvl]

        match self.lvl:
            case 2: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 70; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 3: self.lvl_length = 90; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width; music_manager.play_music("space_heroes")
            case 4: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 110; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 5: self.lvl_length = 130; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 6: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 150; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width; music_manager.play_music("boss_theme")

        self.is_lvl_finish = False

    def check_lvl_finish(self):
        if self.progress >= self.lvl_length and self.total_progress < self.max_progress:
            self.is_lvl_finish = True

    def return_game_finish(self):
        if self.total_progress >= self.max_progress:
            self.game_finished = True
        return self.game_finished

    def draw_progress_bar(self, screen):
        screen.blit(self.lvl_text,self.lvl_text_rect)
        pygame.draw.rect(screen, (255,255,0),(590,970,self.progress / self.progress_bar_ratio,25))
        pygame.draw.rect(screen, (255,255,255), (590,970,self.progress_bar_width,25), 4)

    def draw_game_background(self, screen):
        screen.fill((28, 41, 81))
        screen.blit(self.lvl_background,(0,0))

    def update(self, screen, music_manager):
        self.draw_game_background(screen)
        self.draw_progress_bar(screen)
        self.check_lvl_finish()
        if self.is_lvl_finish: self.Lvl_bar_update(music_manager)
        self.player_progress_dict = {"lvl":self.lvl,
                                     "progress":self.total_progress,
                                     "percentage_of_finish": int((self.total_progress / self.max_progress) * 100)}


class StartMenu:
    def __init__(self, lvl_manager):

        self.backgrounds_dict = {1:"Space_Backgrounds/Space Background_1.png",
                                 2:"Space_Backgrounds/Space Background_2.png",
                                 3:"Space_Backgrounds/Space Background_3.png",
                                 4:"Space_Backgrounds/Space Background_4.png",
                                 5:"Space_Backgrounds/Space Background_5.png"}

        self.background = pygame.image.load(self.backgrounds_dict[randint(1,5)]).convert()
        self.background_rect = self.background.get_rect(topleft = (0,0))


        # menu text
        self.font = pygame.font.Font("Game_font/LLPIXEL3.ttf",50)
        self.title_text1 = self.font.render("The Legend of Reis", False, (255,255,255))
        self.title_text_rect1 = self.title_text1.get_rect(center = (400,300))
        self.title_text2 = self.font.render("Pixel Space Adventure", False, (255, 255, 255))
        self.title_text_rect2 = self.title_text2.get_rect(center=(400, 350))

        # play button
        button1 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[1] Normal.png").convert_alpha(),0,4)
        button2 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[2] Clicked.png").convert_alpha(),0,4)
        button3 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[3] Hover.png").convert_alpha(),0,4)

        self.button_list = [button1,button2,button3]
        self.button_animation_index = 0
        self.button = self.button_list[self.button_animation_index]
        self.button_rect = self.button.get_rect(center = (400,450))

        self.button_text = self.font.render("PLAY", False, (255,255,255))
        self.button_text_rect = self.button_text.get_rect(center = (400,445))

        # info button
        self.is_in_info_section = False
        self.info_button_list = [button1, button2, button3]
        self.info_button_animation_index = 0
        self.info_button = self.info_button_list[self.info_button_animation_index]
        self.info_button_rect = self.info_button.get_rect(center=(400, 550))

        self.info_button_text = self.font.render("INFO", False, (255, 255, 255))
        self.info_button_text_rect = self.info_button_text.get_rect(center=(400, 545))

        #read progress
        self.lvl_manager = lvl_manager
        try:
            with open("save_file.txt", "r") as save_file:
                data = json.load(save_file)
                self.best_progress_rect = pygame.Rect(100,400,data["progress"],50)
                self.progress_percentage_text = self.font.render(f"{data['percentage_of_finish']}%", False, (252,250,249))

        except:
            self.best_progress_rect = pygame.Rect(200, 400, 0, 50)
            self.progress_percentage_text = self.font.render(f"{0}%",False,(252,250,249))

        self.best_progress_rect_border = pygame.Rect(100, 400, self.lvl_manager.max_progress, 50)

        self.progress_text = self.font.render("Best progress...", False, (255, 255, 255))
        self.progress_text_rect = self.progress_text.get_rect(center=(400, 350))

        self.progress_percentage_text_rect = self.progress_percentage_text.get_rect(center = (self.best_progress_rect_border.center))

        # story
        self.story_font = pygame.font.Font("Game_font/LLPIXEL3.ttf", 30)
        self.story_text_1 = self.story_font.render("Once upon a time, in a distant land...",False, (255, 255, 255))
        self.story_text_2 = self.story_font.render("There was a courages warrior named ReIs", False, (255, 255, 255))
        self.story_text_3 = self.story_font.render("He was in search for a new planet: a new home", False, (255, 255, 255))
        self.story_text_4 = self.story_font.render("In order to get more muscular", False, (255, 255, 255))
        self.story_text_5 = self.story_font.render("and realise his purpose in life", False, (255, 255, 255))
        self.story_text_6 = self.story_font.render("This was not a simple quest after all...", False, (255, 255, 255))
        self.story_text_7 = self.story_font.render("But our warrior was ready to what it takes...", False, (255, 255, 255))

        self.story_dict = {self.story_text_1:self.story_text_1.get_rect(center = (400,200)),
                                self.story_text_2:self.story_text_2.get_rect(center = (400,270)),
                                self.story_text_3:self.story_text_3.get_rect(center = (400,340)),
                                self.story_text_4:self.story_text_4.get_rect(center = (400,410)),
                                self.story_text_5: self.story_text_5.get_rect(center = (400,450)),
                                self.story_text_6:self.story_text_6.get_rect(center = (400,550)),
                                self.story_text_7:self.story_text_7.get_rect(center = (400,620))}

        # button
        self.is_in_story_section = False
        self.story_button_list = [button1, button2, button3]
        self.story_button_animation_index = 0
        self.story_button = self.story_button_list[self.story_button_animation_index]
        self.story_button_rect = self.story_button.get_rect(center=(400, 650))

        self.story_button_text = self.font.render("STORY", False, (255, 255, 255))
        self.story_button_text_rect = self.story_button_text.get_rect(center=(400, 645))

        # go back button
        self.back_button_list = [button1, button2, button3]
        self.back_button_animation_index = 0
        self.back_button = self.back_button_list[self.back_button_animation_index]
        self.back_button_rect = self.back_button.get_rect(center=(400, 500))

        self.back_button_text = self.font.render("BACK", False, (255, 255, 255))
        self.back_button_text_rect = self.back_button_text.get_rect(center=(400, 495))


    def animate_play_button(self):
        self.button_animation_index += 0.1
        if self.button_animation_index >= len(self.button_list): self.button_animation_index = 0
        self.button = self.button_list[int(self.button_animation_index)]

    def animate_info_button(self):
        self.info_button_animation_index += 0.1
        if self.info_button_animation_index >= len(self.info_button_list): self.info_button_animation_index = 0
        self.info_button = self.info_button_list[int(self.info_button_animation_index)]

    def animate_story_button(self):
        self.story_button_animation_index += 0.1
        if self.story_button_animation_index >= len(self.story_button_list): self.story_button_animation_index = 0
        self.story_button = self.story_button_list[int(self.story_button_animation_index)]

    def animate_back_button(self):
        self.back_button_animation_index += 0.1
        if self.back_button_animation_index >= len(self.back_button_list): self.back_button_animation_index = 0
        self.back_button = self.back_button_list[int(self.back_button_animation_index)]

    def in_info_section(self,screen):
        screen.blit(self.background,self.background_rect)
        screen.blit(self.progress_text,self.progress_text_rect)
        pygame.draw.rect(screen, (0,255,0), self.best_progress_rect)
        pygame.draw.rect(screen, (255, 253, 250), self.best_progress_rect_border, 4)
        screen.blit(self.progress_percentage_text,self.progress_percentage_text_rect)

        # back button
        self.animate_back_button()
        self.back_button_rect.center, self.back_button_text_rect.center = ((400, 500), (400, 495))
        screen.blit(self.back_button, self.back_button_rect)
        screen.blit(self.back_button_text, self.back_button_text_rect)

    def in_story_section(self,screen):
        screen.blit(self.background,self.background_rect)

        #story
        for text in self.story_dict:
            rect = self.story_dict[text]
            screen.blit(text,rect)
        # back button
        self.animate_back_button()
        self.back_button_rect.center, self.back_button_text_rect.center = ((400, 800), (400, 795))
        screen.blit(self.back_button, self.back_button_rect)
        screen.blit(self.back_button_text, self.back_button_text_rect)


    def update(self,screen):
        screen.blit(self.background,self.background_rect)
        screen.blit(self.title_text1,self.title_text_rect1)
        screen.blit(self.title_text2, self.title_text_rect2)

        # play button
        self.animate_play_button()
        screen.blit(self.button,self.button_rect)
        screen.blit(self.button_text,self.button_text_rect)

        # info button
        self.animate_info_button()
        screen.blit(self.info_button, self.info_button_rect)
        screen.blit(self.info_button_text, self.info_button_text_rect)

        # menu button
        self.animate_story_button()
        screen.blit(self.story_button, self.story_button_rect)
        screen.blit(self.story_button_text, self.story_button_text_rect)


class GameEndMenu:
    def __init__(self):
        self.backgrounds_dict = {1: "Space_Backgrounds/Space Background_11.png",
                                 2: "Space_Backgrounds/Space Background_12.png",
                                 3: "Space_Backgrounds/Space Background_13.png",
                                 4: "Space_Backgrounds/Space Background_14.png",
                                 5: "Space_Backgrounds/Space Background_15.png"}

        self.background = pygame.image.load(self.backgrounds_dict[randint(1, 5)]).convert()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        self.planet_backgrounds_dict = {1:pygame.image.load("Planet/tile000.png").convert_alpha(),
                                        2:pygame.image.load("Planet/tile001.png").convert_alpha(),
                                        3:pygame.image.load("Planet/tile002.png").convert_alpha(),
                                        4:pygame.image.load("Planet/tile003.png").convert_alpha(),
                                        5:pygame.image.load("Planet/tile004.png").convert_alpha(),
                                        6:pygame.image.load("Planet/tile005.png").convert_alpha(),
                                        7:pygame.image.load("Planet/tile006.png").convert_alpha(),
                                        8:pygame.image.load("Planet/tile007.png").convert_alpha(),
                                        9:pygame.image.load("Planet/tile008.png").convert_alpha(),
                                        10:pygame.image.load("Planet/tile009.png").convert_alpha(),
                                        11:pygame.image.load("Planet/tile010.png").convert_alpha(),
                                        12:pygame.image.load("Planet/tile011.png").convert_alpha(),
                                        13:pygame.image.load("Planet/tile012.png").convert_alpha(),
                                        14:pygame.image.load("Planet/tile013.png").convert_alpha(),
                                        15:pygame.image.load("Planet/tile014.png").convert_alpha(),
                                        16:pygame.image.load("Planet/tile015.png").convert_alpha(),
                                        17:pygame.image.load("Planet/tile016.png").convert_alpha(),
                                        18:pygame.image.load("Planet/tile017.png").convert_alpha(),
                                        19:pygame.image.load("Planet/tile018.png").convert_alpha(),
                                        20:pygame.image.load("Planet/tile019.png").convert_alpha(),
                                        21:pygame.image.load("Planet/tile020.png").convert_alpha(),
                                        22:pygame.image.load("Planet/tile021.png").convert_alpha(),
                                        23:pygame.image.load("Planet/tile022.png").convert_alpha(),
                                        24:pygame.image.load("Planet/tile023.png").convert_alpha(),
                                        25:pygame.image.load("Planet/tile024.png").convert_alpha(),
                                        26:pygame.image.load("Planet/tile025.png").convert_alpha(),
                                        27:pygame.image.load("Planet/tile026.png").convert_alpha(),
                                        28:pygame.image.load("Planet/tile027.png").convert_alpha(),
                                        29:pygame.image.load("Planet/tile028.png").convert_alpha(),
                                        30:pygame.image.load("Planet/tile029.png").convert_alpha(),
                                        31:pygame.image.load("Planet/tile030.png").convert_alpha(),
                                        32:pygame.image.load("Planet/tile031.png").convert_alpha(),
                                        33:pygame.image.load("Planet/tile032.png").convert_alpha(),
                                        34:pygame.image.load("Planet/tile033.png").convert_alpha(),
                                        35:pygame.image.load("Planet/tile034.png").convert_alpha(),
                                        36:pygame.image.load("Planet/tile035.png").convert_alpha(),
                                        37:pygame.image.load("Planet/tile036.png").convert_alpha(),
                                        38:pygame.image.load("Planet/tile037.png").convert_alpha(),
                                        39:pygame.image.load("Planet/tile038.png").convert_alpha(),
                                        40:pygame.image.load("Planet/tile039.png").convert_alpha(),
                                        41:pygame.image.load("Planet/tile040.png").convert_alpha(),
                                        42:pygame.image.load("Planet/tile041.png").convert_alpha(),
                                        43:pygame.image.load("Planet/tile042.png").convert_alpha(),
                                        44:pygame.image.load("Planet/tile043.png").convert_alpha(),
                                        45:pygame.image.load("Planet/tile044.png").convert_alpha(),
                                        46:pygame.image.load("Planet/tile045.png").convert_alpha(),
                                        47:pygame.image.load("Planet/tile046.png").convert_alpha(),
                                        48:pygame.image.load("Planet/tile047.png").convert_alpha(),
                                        49:pygame.image.load("Planet/tile048.png").convert_alpha(),
                                        50:pygame.image.load("Planet/tile049.png").convert_alpha()}
        self.planet_backgrounds_index = 1
        self.planet_background = pygame.transform.rotozoom(self.planet_backgrounds_dict[self.planet_backgrounds_index],0,2)
        self.planet_background_rect = self.planet_background.get_rect(center = (400,750))

        # end story
        self.story_font = pygame.font.Font("Game_font/LLPIXEL3.ttf", 30)
        self.story_text_1 = self.story_font.render("Our warrior has successfully defeated the alien horde", False,(255, 255, 255))
        self.story_text_2 = self.story_font.render("ReIs: I think I should settle on this planet...", False, (255, 255, 255))
        self.story_text_3 = self.story_font.render("So the epic adventure of ReIs awaits him...", False,(255, 255, 255))
        self.story_text_4 = self.story_font.render("In this mysterious planet...", False, (255, 255, 255))
        self.story_text_5 = self.story_font.render("To Be Continued...", False, (255, 255, 255))
        self.story_text_6 = self.story_font.render("The Legend of ReIs Chapter-1", False, (255, 255, 255))
        self.story_text_7 = self.story_font.render("by Reis200", False, (255, 255, 255))

        self.story_dict = {self.story_text_1: self.story_text_1.get_rect(center=(400, 200)),
                           self.story_text_2: self.story_text_2.get_rect(center=(400, 270)),
                           self.story_text_3: self.story_text_3.get_rect(center=(400, 340)),
                           self.story_text_4: self.story_text_4.get_rect(center=(400, 410)),
                           self.story_text_5: self.story_text_5.get_rect(center=(400, 450)),
                           self.story_text_6: self.story_text_6.get_rect(center=(400, 550)),
                           self.story_text_7: self.story_text_7.get_rect(center=(400, 620))}

        # main menu button
        button1 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[1] Normal.png").convert_alpha(), 0, 4)
        button2 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[2] Clicked.png").convert_alpha(), 0, 4)
        button3 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[3] Hover.png").convert_alpha(), 0,4)
        self.font = pygame.font.Font("Game_font/LLPIXEL3.ttf",50)
        self.main_button_list = [button1, button2, button3]
        self.main_button_animation_index = 0
        self.main_button = self.main_button_list[self.main_button_animation_index]
        self.main_button_rect = self.main_button.get_rect(center=(400, 950))

        self.main_button_text = self.font.render("MAIN", False, (255, 255, 255))
        self.main_button_text_rect = self.main_button_text.get_rect(center=(400, 945))

    def animate_main_button(self):
        self.main_button_animation_index += 0.1
        if self.main_button_animation_index >= len(self.main_button_list): self.main_button_animation_index = 0
        self.main_button = self.main_button_list[int(self.main_button_animation_index)]

    def animate_planet(self):
        self.planet_backgrounds_index += 0.1
        if self.planet_backgrounds_index >= len(self.planet_backgrounds_dict): self.planet_backgrounds_index = 1
        self.planet_background = pygame.transform.rotozoom(self.planet_backgrounds_dict[int(self.planet_backgrounds_index)],0,2)

    def update(self,screen):
        screen.blit(self.background,self.background_rect)

        # story
        for text in self.story_dict:
            rect = self.story_dict[text]
            screen.blit(text, rect)
        # animate planet
        self.animate_planet()
        screen.blit(self.planet_background,self.planet_background_rect)

        # main button
        self.animate_main_button()
        screen.blit(self.main_button, self.main_button_rect)
        screen.blit(self.main_button_text, self.main_button_text_rect)



class OverMenu(StartMenu):
    def __init__(self):

        self.backgrounds_dict = {6: "Space_Backgrounds/Space Background_6.png",
                                 7: "Space_Backgrounds/Space Background_7.png",
                                 8: "Space_Backgrounds/Space Background_8.png",
                                 9: "Space_Backgrounds/Space Background_9.png",
                                 10: "Space_Backgrounds/Space Background_10.png"}

        self.background = pygame.image.load(self.backgrounds_dict[randint(6, 10)]).convert()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        # menu text
        self.font = pygame.font.Font("Game_font/LLPIXEL3.ttf", 50)
        self.game_over_text = self.font.render("Game Over", False, (255, 255, 255))
        self.game_over_text_rect = self.game_over_text.get_rect(center=(400, 300))

        # play button
        button1 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[1] Normal.png").convert_alpha(), 0, 4)
        button2 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[2] Clicked.png").convert_alpha(), 0, 4)
        button3 = pygame.transform.rotozoom(pygame.image.load("UI_assets/[6] Silver/[3] Hover.png").convert_alpha(), 0, 4)

        self.button_list = [button1, button2, button3]
        self.button_animation_index = 0
        self.button = self.button_list[self.button_animation_index]
        self.button_rect = self.button.get_rect(center=(400, 450))

        self.button_text = self.font.render("RETRY", False, (255, 255, 255))
        self.button_text_rect = self.button_text.get_rect(center=(400, 445))

        # main menu button
        self.main_button_list = [button1, button2, button3]
        self.main_button_animation_index = 0
        self.main_button = self.main_button_list[self.main_button_animation_index]
        self.main_button_rect = self.main_button.get_rect(center=(400, 550))

        self.main_button_text = self.font.render("MAIN", False, (255, 255, 255))
        self.main_button_text_rect = self.main_button_text.get_rect(center=(400, 545))


    def animate_main_button(self):
        self.main_button_animation_index += 0.1
        if self.main_button_animation_index >= len(self.main_button_list): self.main_button_animation_index = 0
        self.main_button = self.main_button_list[int(self.main_button_animation_index)]

    def update(self,screen):
        screen.blit(self.background,self.background_rect)
        screen.blit(self.game_over_text,self.game_over_text_rect)

        # button
        self.animate_play_button()
        screen.blit(self.button,self.button_rect)
        screen.blit(self.button_text,self.button_text_rect)

        # main button
        self.animate_main_button()
        screen.blit(self.main_button, self.main_button_rect)
        screen.blit(self.main_button_text, self.main_button_text_rect)




