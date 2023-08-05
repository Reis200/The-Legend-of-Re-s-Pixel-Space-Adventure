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
        self.player_assets = pygame.sprite.Group()
        self.player_assets.add(PlayerShip())


    def pygame_loop(self):
        while True:

            self.screen.fill("#1d1135")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # draw and update player sprite
            self.player_assets.draw(self.screen)
            self.player_assets.update()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.pygame_loop()

