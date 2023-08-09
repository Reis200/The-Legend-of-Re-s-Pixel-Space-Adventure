import pygame
from random import randint

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
