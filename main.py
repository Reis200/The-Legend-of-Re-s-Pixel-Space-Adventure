import pygame
from sys import exit
from game_sprites import *


class Main:

    def __init__(self):
        pygame.init()

        # game window
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("The-Legend-of-Reis-Pixel-Space-Adventure")
        icon = pygame.image.load("Youtube Icons1.png")
        pygame.display.set_icon(icon)

        # clock
        self.clock = pygame.time.Clock()

        # Sprite Groups - Player
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player = PlayerShip()
        self.player_sprite_group.add(self.player)

        self.player_assets_group = pygame.sprite.Group()

        # Sprite Groups - Enemy
        self.enemy_sprite_group = pygame.sprite.Group()


        # Timer
        self.enemy_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_spawn_timer, 1000)


    def pygame_loop(self):
        while True:

            self.screen.fill("#1d1135")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player_assets_group.add(PlayerBullets(self.player))
                if event.type == self.enemy_spawn_timer:
                    self.enemy_sprite_group.add(EnemyShip(1))




            # draw and update player sprite
            self.player_sprite_group.draw(self.screen)
            self.player_sprite_group.update()

            # draw and update player bullets
            self.player_assets_group.draw(self.screen)
            self.player_assets_group.update()

            # draw and update enemies
            self.enemy_sprite_group.draw(self.screen)
            self.enemy_sprite_group.update()

            # player bullets and enemy collision
            pygame.sprite.groupcollide(self.player_assets_group,self.enemy_sprite_group, True, True)

            # enemy and player collision
            if pygame.sprite.spritecollide(self.player_sprite_group.sprite,self.enemy_sprite_group,True): exit();player_sprite_group.sprite.kill()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.pygame_loop()

