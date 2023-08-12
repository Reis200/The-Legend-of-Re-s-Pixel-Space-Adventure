import pygame
import json
from sys import exit
from game_sprites import *
from game_managers import *
from random import choice,randint



class Main:

    def __init__(self):
        pygame.init()


        # game window
        self.screen = pygame.display.set_mode((800, 1000))
        pygame.display.set_caption("The-Legend-of-Reis-Pixel-Space-Adventure")
        icon = pygame.image.load("Youtube Icons1.png").convert_alpha()
        pygame.display.set_icon(icon)



        # Game font
        self.game_font = pygame.font.Font("Game_font/LLPIXEL3.ttf",30)

        # Game_states
        self.in_start_menu = True
        self.in_game = False
        self.in_over_menu = False
        self.in_game_finish_menu = False

        # clock
        self.clock = pygame.time.Clock()

        # Objects
        self.lvl_manager = LvlManager(self.game_font)
        self.start_menu_manager = StartMenu(self.lvl_manager)
        self.over_menu_manager = OverMenu()
        self.game_finish_menu_manager = GameEndMenu()

        # Sprite Groups - Player
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player = PlayerShip()
        self.player_sprite_group.add(self.player)

        self.player_assets_group = pygame.sprite.Group()

        # Sprite Groups - Enemy
        self.enemy_sprite_group = pygame.sprite.Group()
        self.enemy_assets_group = pygame.sprite.Group()

        # Sprite Group - PowerUp
        self.power_up_sprite_group = pygame.sprite.Group()


        # Timer
        self.enemy_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_spawn_timer, 2000)

        self.enemy_bullet_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_bullet_timer, 1000)

        self.power_up_spawn_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.power_up_spawn_timer, 18000)



    def in_start_menu_operation(self):
        if self.start_menu_manager.is_in_info_section:
            self.start_menu_manager.in_info_section(self.screen)
        elif self.start_menu_manager.is_in_story_section:
            self.start_menu_manager.in_story_section(self.screen)
        else:
            self.start_menu_manager.update(self.screen)

    def in_over_menu_operation(self):
        self.over_menu_manager.update(self.screen)

    def in_game_finish_operation(self):
        self.game_finish_menu_manager.update(self.screen)

    def in_game_operation(self):

        # lvl manager
        self.lvl_manager.update(self.screen)

        # powerups draw and update
        self.power_up_sprite_group.draw(self.screen)
        self.power_up_sprite_group.update()

        # draw and update player sprite
        self.player_sprite_group.draw(self.screen)
        self.player_sprite_group.update(self.screen)

        # draw and update player bullets
        self.player_assets_group.draw(self.screen)
        self.player_assets_group.update()

        # draw and update enemies
        self.enemy_sprite_group.draw(self.screen)
        self.lvl_manager_updated = self.enemy_sprite_group.update(self.screen, self.lvl_manager)
        if self.lvl_manager_updated != None: self.lvl_manager = self.lvl_manager_updated


        # draw and update enemy bullets
        self.enemy_assets_group.draw(self.screen)
        self.enemy_assets_group.update()

        if self.player_sprite_group.sprite != None:

            # player and PowerUp collision
            if self.power_up_sprite_group.sprites() != None and self.player_sprite_group.sprite != None and pygame.sprite.spritecollideany(self.player_sprite_group.sprite,self.power_up_sprite_group):
                for power_up in self.power_up_sprite_group.sprites():
                    if pygame.sprite.spritecollide(power_up, self.player_sprite_group, False):
                        self.player_sprite_group.sprite.apply_power_up(power_up.effect, power_up.power_up_duration)
                        power_up.kill()

            # player bullets and enemy collision
            if self.enemy_sprite_group.sprites() != None:
                for enemy in self.enemy_sprite_group.sprites():
                    if pygame.sprite.spritecollide(enemy, self.player_assets_group, True):
                        enemy.decrease_health(self.player_sprite_group.sprite.damage)

            if self.enemy_sprite_group.sprites() != None and pygame.sprite.spritecollideany(self.player_sprite_group.sprite,self.enemy_sprite_group) or pygame.sprite.spritecollideany(self.player_sprite_group.sprite,self.enemy_assets_group):

                # enemy bullets and player collision
                for enemy_bullet in self.enemy_assets_group.sprites():
                    if pygame.sprite.spritecollide(self.player_sprite_group.sprite, self.enemy_assets_group, True):
                        self.player_sprite_group.sprite.decrease_health(enemy_bullet.bullet_damage)


                # enemy and player collision
                for enemy in self.enemy_sprite_group.sprites():
                    if pygame.sprite.spritecollide(self.player_sprite_group.sprite, self.enemy_sprite_group, True):
                        self.player_sprite_group.sprite.decrease_health(enemy.damage * 1.5)

        if self.player_sprite_group.sprite == None:
            self.enemy_sprite_group.empty()
            self.enemy_assets_group.empty()
            self.power_up_sprite_group.empty()
            self.player_sprite_group.empty()
            self.player_assets_group.empty()
            try:
                with open("save_file.txt", "r") as save_file:
                    data = json.load(save_file)
                    if data["progress"] >= self.lvl_manager.total_progress: pass
                    else: self.lvl_manager.save_player_progress_lvl()
            except: self.lvl_manager.save_player_progress_lvl()

            self.lvl_manager = LvlManager(self.game_font)
            self.start_menu_manager = StartMenu(self.lvl_manager)
            self.over_menu_manager = OverMenu()
            self.in_game = False; self.in_over_menu = True

        if self.lvl_manager.return_game_finish():
            self.enemy_sprite_group.empty()
            self.enemy_assets_group.empty()
            self.power_up_sprite_group.empty()
            self.player_sprite_group.empty()
            self.player_assets_group.empty()

            try:
                with open("save_file.txt", "r") as save_file:
                    data = json.load(save_file)
                    if data["progress"] >= self.lvl_manager.total_progress: pass
                    else: self.lvl_manager.save_player_progress_lvl()
            except: self.lvl_manager.save_player_progress_lvl()

            self.lvl_manager = LvlManager(self.game_font)
            self.start_menu_manager = StartMenu(self.lvl_manager)
            self.over_menu_manager = OverMenu()

            self.in_game = False; self.in_game_finish_menu = True



    def pygame_loop(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT and not self.in_game:
                    pygame.quit()
                    exit()
                if event.type == pygame.QUIT and self.in_game:
                    try:
                        with open("save_file.txt", "r") as save_file:
                            data = json.load(save_file)
                            if data["progress"] >= self.lvl_manager.total_progress: pass
                            else: self.lvl_manager.save_player_progress_lvl()
                    except:
                        self.lvl_manager.save_player_progress_lvl()

                    pygame.quit()
                    exit()


                if event.type == pygame.MOUSEBUTTONDOWN and self.in_start_menu:
                    if self.start_menu_manager.button_rect.collidepoint(event.pos):
                        self.in_start_menu = False; self.in_game = True
                    elif self.start_menu_manager.info_button_rect.collidepoint(event.pos):
                        self.start_menu_manager.is_in_info_section = True
                    elif self.start_menu_manager.story_button_rect.collidepoint(event.pos):
                        self.start_menu_manager.is_in_story_section = True
                    elif self.start_menu_manager.back_button_rect.collidepoint(event.pos):
                        self.start_menu_manager.is_in_info_section = False
                        self.start_menu_manager.is_in_story_section = False


                if event.type == pygame.MOUSEBUTTONDOWN and self.in_over_menu:
                    if self.over_menu_manager.button_rect.collidepoint(event.pos):
                        self.in_over_menu = False
                        self.in_game = True
                        self.player_sprite_group.add(PlayerShip())
                    elif self.over_menu_manager.main_button_rect.collidepoint(event.pos):
                        self.in_over_menu = False
                        self.in_start_menu = True
                        self.player_sprite_group.add(PlayerShip())

                if event.type == pygame.MOUSEBUTTONDOWN and self.in_game_finish_menu:
                    if self.game_finish_menu_manager.main_button_rect.collidepoint(event.pos):
                        self.in_game_finish_menu = False
                        self.in_start_menu = True
                        self.player_sprite_group.add(PlayerShip())




                if event.type == pygame.KEYDOWN and self.in_game:
                    if event.key == pygame.K_SPACE and self.player_sprite_group.sprite != None:
                        self.player_assets_group.add(PlayerBullets(self.player_sprite_group.sprite))

                    if event.key == pygame.K_e and self.player_sprite_group.sprite != None:
                        print(self.player_sprite_group.sprite.current_health)
                        self.player_sprite_group.sprite.decrease_health(20)
                    if event.key == pygame.K_a and self.player_sprite_group.sprite != None:
                        print(self.player_sprite_group.sprite.current_health)
                        self.player_sprite_group.sprite.increase_health(20)

                    if event.key == pygame.K_h:
                        self.lvl_manager.increase_progress()


                if event.type == self.enemy_spawn_timer and self.in_game:
                    for enemy_spawn_count in range(self.lvl_manager.enemy_spawn_count_per_timer):
                        print(self.lvl_manager.enemy_spawn_count_per_timer)
                        self.enemy_sprite_group.add(EnemyShip(self.lvl_manager.randomize_enemy_spawn()))
                    # self.enemy_sprite_group.add(EnemyShip(7))

                if event.type == self.enemy_bullet_timer and self.in_game:
                    for enemy_ship in self.enemy_sprite_group.sprites():
                        if enemy_ship.alive():
                            self.enemy_assets_group.add(EnemyBullets(enemy_ship))

                if event.type == self.power_up_spawn_timer and self.in_game:
                    self.power_up_sprite_group.add(PowerUp())


            if self.in_start_menu: self.in_start_menu_operation()
            if self.in_game: self.in_game_operation()
            if self.in_over_menu: self.in_over_menu_operation()
            if self.in_game_finish_menu: self.in_game_finish_operation()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.pygame_loop()

