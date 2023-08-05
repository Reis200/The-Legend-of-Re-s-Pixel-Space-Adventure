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

        # Sprite Groups
        self.player_sprite_group = pygame.sprite.Group()
        self.player = PlayerShip()
        self.player_sprite_group.add(self.player)


        # Timer
        # self.player_shoot_timer = pygame.USEREVENT + 1
        # pygame.time.set_timer(self.player_shoot_timer, 100)


    def pygame_loop(self):
        while True:

            self.screen.fill("#1d1135")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player_sprite_group.add(PlayerBullets(self.player))



            # draw and update player sprite
            self.player_sprite_group.draw(self.screen)
            self.player_sprite_group.update()
            print(self.player_sprite_group)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.pygame_loop()

