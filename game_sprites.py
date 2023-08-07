import pygame
from random import randint


class PlayerShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.bullet_lvl = 0
        self.speed = 5
        self.image = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/copper_space_fighter.png").convert_alpha(),0,2)
        self.rect = self.image.get_rect(center = (400,900))

    def player_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

    def destroy(self):
        self.kill()

    def update(self):
        self.player_movement()


class PlayerBullets(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()

        self.bullet_1 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/character_bullet_2.png").convert_alpha(),0,4)
        self.bullet_2 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/character_bullet_1.png").convert_alpha(),0,4)
        self.bullets_list = [self.bullet_1, self.bullet_2]
        self.bullet_index = player.bullet_lvl
        self.bullet_image = self.bullets_list[self.bullet_index]

        self.image = self.bullet_image
        self.rect = self.image.get_rect(center=player.rect.midtop)

    def shoot(self):
        self.rect.y -= 6
        if self.rect.y <= -50: self.kill()

    def update(self):
        self.shoot()


class EnemyShip(pygame.sprite.Sprite):

    enemies_dict = {1:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_ship_1.png",
                    2:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_ship_2.png",
                    3:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_ship3.png",
                    4:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_small_boat.png",
                    5:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_small_boat_bomb.png",
                    6:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_small_boat_triplegun.png",
                    7:"The-Legend-of-Reis-Pixel-Space-Adventure-Assets/Pixel space ships boss.png"}

    def __init__(self, enemy_id):
        super().__init__()

        # enemy_id in from 1 - 7
        self.image = pygame.transform.rotozoom(pygame.image.load(self.enemies_dict[enemy_id]),0,3)
        self.rect = self.image.get_rect(center = (randint(80,750),randint(-300,-50)))

        match enemy_id:
            case 1: self.speed = 3
            case 2: self.speed = 3
            case 3: self.speed = 3
            case 4: self.speed = 5
            case 5: self.speed = 5
            case 6: self.speed = 4
            case 7: self.speed = 1

    def move_vertical(self):
        # if randint(0,2):
        self.rect.y += self.speed

    def move_right(self):
        if self.rect.right < 600: self.rect.x += self.speed

    def move_left(self):
        if self.rect.left > 0: self.rect.x -= self.speed

    def destroy(self):
        if self.rect.y >= 1075:
            self.kill()

    def update(self):
        self.move_vertical()
        # self.move_right()
        # self.move_left()
        self.destroy()

