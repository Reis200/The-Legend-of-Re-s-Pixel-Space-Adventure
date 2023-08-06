import pygame
from sys import exit
from game_sprites import *
from random import choice,randint


class Main:

    def __init__(self):
        pygame.init()

        # game window
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("The-Legend-of-Reis-Pixel-Space-Adventure")
        icon = pygame.image.load("Youtube Icons1.png").convert_alpha()
        pygame.display.set_icon(icon)


        # Game images
        self.blue_planet = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/blue_planet.png").convert_alpha(), 0 , 2)
        self.blue_saturn = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/blue_saturn.png").convert_alpha(), 0 , 2)
        self.died_star = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/died_star.png").convert_alpha(), 0 , 2)
        self.moon = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/moon.png").convert_alpha(), 0 , 2)
        self.small_planet_blue = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/small_planet_blue.png").convert_alpha(), 0 , 2)
        self.small_planet_red = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/small_planet_red.png").convert_alpha(), 0 , 2)

        # Game_states
        self.start_menu = True
        self.in_game = False
        self.in_menu = False

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

    def draw_game_background(self):
        self.screen.fill((28, 41, 81))
        self.screen.blit(self.blue_planet,(0,0))
        self.screen.blit(self.blue_saturn,(150,0))
        self.screen.blit(self.died_star,(250,300))
        self.screen.blit(self.moon,(100,400))
        self.screen.blit(self.small_planet_blue,(500,440))
        self.screen.blit(self.small_planet_red,(300,150))
        self.screen.blit(self.blue_saturn, (350, 50))
        self.screen.blit(self.small_planet_blue, (200,  440))



    def start_menu_operation(self):
        pass

    def in_game_operation(self):
        pass

    def in_menu_operation(self):
        pass



    def pygame_loop(self):
        while True:

            self.draw_game_background()

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

