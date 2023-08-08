import pygame
from random import randint


class PlayerShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.bullet_lvl = 0
        self.speed = 5
        self.image = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/copper_space_fighter.png").convert_alpha(),0,2)
        self.rect = self.image.get_rect(center = (400,900))

        # health for player
        self.current_health = 100
        self.target_health = 200
        self.max_health = 200
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 0.8
        self.health_bar_color = (255,0,0)

        # compass and navigator
        self.compass = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/compass.png").convert_alpha(),0,2)
        self.compass_rect = self.compass.get_rect(center = (75,900))

    def draw_health(self,screen):
        transition_width = 0
        transition_color = self.health_bar_color

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = (0,255,0)
        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            transition_width = int((self.current_health - self.target_health) / self.health_ratio)
            transition_color = (255,255,0)

        health_bar_rect = pygame.Rect(10,970,int(self.current_health / self.health_ratio),25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right,970,transition_width,25)

        pygame.draw.rect(screen, self.health_bar_color, health_bar_rect)
        if self.current_health != 100: pygame.draw.rect(screen, transition_color, transition_bar_rect)
        pygame.draw.rect(screen, (255, 255, 255), (10,970,self.health_bar_length,25), 4)

    def draw_navigator(self,screen):
        screen.blit(self.compass,self.compass_rect)

    def increase_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health >= self.max_health:
            self.target_health = self.max_health

    def decrease_health(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def player_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

    def is_died(self):
        if self.current_health <= 0:
            self.kill()

    def update(self, screen):
        self.player_movement()
        self.draw_health(screen)
        self.draw_navigator(screen)
        self.is_died()


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



class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self,enemy):
        super().__init__()
        self.bullet_1 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_bullet_2.png").convert_alpha(), 0, 4)
        self.bullet_2 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/enemy_bullet_1.png").convert_alpha(), 0, 4)
        self.bullets_list = [self.bullet_1, self.bullet_2]
        self.bullet_index = enemy.bullet_lvl

        self.image = self.bullets_list[self.bullet_index]
        self.rect = self.image.get_rect(center = enemy.rect.midbottom)

    def shoot(self):
        self.rect.y += 6
        if self.rect.y >= 1050: self.kill()

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

        if enemy_id <= 3: self.bullet_lvl = 0
        else: self.bullet_lvl = 1

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

