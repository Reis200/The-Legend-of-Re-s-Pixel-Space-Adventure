import pygame
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
        self.start_menu = False
        self.in_game = True
        self.in_menu = False

        # clock
        self.clock = pygame.time.Clock()

        # Objects
        self.lvl_manager = LvlManager(self.game_font)

        # Sprite Groups - Player
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player = PlayerShip()
        self.player_sprite_group.add(self.player)

        self.player_assets_group = pygame.sprite.Group()

        # Sprite Groups - Enemy
        self.enemy_sprite_group = pygame.sprite.Group()
        self.enemy_assets_group = pygame.sprite.Group()


        # Timer
        self.enemy_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_spawn_timer, 2000)

        self.enemy_bullet_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_bullet_timer, 1000)



    def start_menu_operation(self):
        pass

    def in_menu_operation(self):
        pass

    def in_game_operation(self):

        # lvl manager
        self.lvl_manager.update(self.screen)

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

        # player bullets and enemy collision
        if self.enemy_sprite_group.sprites() != None:
            for enemy in self.enemy_sprite_group.sprites():
                if pygame.sprite.spritecollide(enemy, self.player_assets_group, True):
                    enemy.decrease_health(self.player_sprite_group.sprite.damage)

        if self.player_sprite_group.sprite != None and pygame.sprite.spritecollideany(self.player_sprite_group.sprite,self.enemy_sprite_group):

            # enemy bullets and player collision
            for enemy_bullet in self.enemy_assets_group.sprites():
                if pygame.sprite.spritecollide(self.player_sprite_group.sprite, self.enemy_assets_group, True):
                    self.player_sprite_group.sprite.decrease_health(enemy_bullet.bullet_damage)

            # enemy and player collision
            for enemy in self.enemy_sprite_group.sprites():
                if pygame.sprite.spritecollide(self.player_sprite_group.sprite, self.enemy_sprite_group, True):
                    self.player_sprite_group.sprite.decrease_health(enemy.damage * 1.5)


    def pygame_loop(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player_sprite_group.sprite != None:
                        self.player_assets_group.add(PlayerBullets(self.player))

                    if event.key == pygame.K_e and self.player_sprite_group.sprite != None:
                        print(self.player_sprite_group.sprite.current_health)
                        self.player_sprite_group.sprite.decrease_health(20)
                    if event.key == pygame.K_a and self.player_sprite_group.sprite != None:
                        print(self.player_sprite_group.sprite.current_health)
                        self.player_sprite_group.sprite.increase_health(20)

                    if event.key == pygame.K_h:
                        self.lvl_manager.progress += 10


                if event.type == self.enemy_spawn_timer:
                    for enemy_spawn_count in range(self.lvl_manager.enemy_spawn_count_per_timer):
                        self.enemy_sprite_group.add(EnemyShip(self.lvl_manager.randomize_enemy_spawn()))
                    # self.enemy_sprite_group.add(EnemyShip(7))

                if event.type == self.enemy_bullet_timer:
                    for enemy_ship in self.enemy_sprite_group.sprites():
                        if enemy_ship.alive():
                            self.enemy_assets_group.add(EnemyBullets(enemy_ship))

            self.in_game_operation()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.pygame_loop()

