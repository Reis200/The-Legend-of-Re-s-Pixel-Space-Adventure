import pygame

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.bullet_lvl = 0
        self.speed = 3
        self.image = pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/copper_space_fighter.png").convert_alpha()
        self.rect = self.image.get_rect(center = (300,500))



    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed


    def destroy(self):
        self.kill()

    def update(self):
        self.player_input()



class PlayerBullets(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()

        self.bullet_1 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/character_bullet_2.png").convert_alpha(),0,2)
        self.bullet_2 = pygame.transform.rotozoom(pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/character_bullet_1.png").convert_alpha(),0,2)
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