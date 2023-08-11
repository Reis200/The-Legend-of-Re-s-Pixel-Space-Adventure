import pygame
from random import randint
from math import sqrt

class LvlManager:
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

    def randomize_enemy_spawn(self):
        match self.lvl:
            case 1: return randint(1,3)
            case 2: return randint(1,4)
            case 3: return randint(1,5)
            case 4: return randint(1,6)
            case 5: return randint(1, 7)
            case 6: return randint(1,8)

    def increase_progress(self):
        if self.progress < self.lvl_length: self.progress += 1

    def Lvl_bar_update(self):
        if self.lvl != self.max_lvl:
            self.lvl += 1

        self.lvl_background = self.lvl_images_dict[self.lvl]

        match self.lvl:
            case 2: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 70; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 3: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 90; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 4: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 110; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 5: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 130; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width
            case 6: self.enemy_spawn_count_per_timer += 1;self.lvl_length = 150; self.progress = 0; self.progress_bar_ratio = self.lvl_length / self.progress_bar_width

        self.is_lvl_finish = False

    def check_lvl_finish(self):
        if self.progress >= self.lvl_length:
            self.is_lvl_finish = True

    def draw_progress_bar(self, screen):
        screen.blit(self.lvl_text,self.lvl_text_rect)
        pygame.draw.rect(screen, (255,255,0),(590,970,self.progress / self.progress_bar_ratio,25))
        pygame.draw.rect(screen, (255,255,255), (590,970,self.progress_bar_width,25), 4)

    def draw_game_background(self, screen):
        screen.fill((28, 41, 81))
        screen.blit(self.lvl_background,(0,0))

    def update(self, screen):
        self.draw_game_background(screen)
        self.draw_progress_bar(screen)
        self.check_lvl_finish()
        if self.is_lvl_finish: self.Lvl_bar_update()


class StartMenu:
    def __init__(self):

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



    def animate_button(self):
        self.button_animation_index += 0.1
        if self.button_animation_index >= len(self.button_list): self.button_animation_index = 0
        self.button = self.button_list[int(self.button_animation_index)]



    def update(self,screen):
        screen.blit(self.background,self.background_rect)
        screen.blit(self.title_text1,self.title_text_rect1)
        screen.blit(self.title_text2, self.title_text_rect2)

        # button
        self.animate_button()
        screen.blit(self.button,self.button_rect)
        screen.blit(self.button_text,self.button_text_rect)


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


    def update(self,screen):
        screen.blit(self.background,self.background_rect)
        screen.blit(self.game_over_text,self.game_over_text_rect)

        # button
        self.animate_button()
        screen.blit(self.button,self.button_rect)
        screen.blit(self.button_text,self.button_text_rect)




