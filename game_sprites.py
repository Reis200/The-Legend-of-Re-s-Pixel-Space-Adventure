import pygame

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 3
        self.image = pygame.image.load("The-Legend-of-Reis-Pixel-Space-Adventure-Assets/copper_space_fighter.png").convert_alpha()
        self.rect = self.image.get_rect(center = (300,500))

    def player_input(self):
        keys = pygame.key.get_pressed()
        # match keys:
        #     case pygame.K_RIGHT: self.rect.x += self.speed
        #     case pygame.K_LEFT: self.rect.x -= self.speed
        #     case pygame.K_UP: self.rect.y += self.speed
        #     case pygame.K_DOWN: self.rect.y -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_LEFT]: self.rect.x -= self.speed
        if keys[pygame.K_UP]: self.rect.y -= self.speed
        if keys[pygame.K_DOWN]: self.rect.y += self.speed

    def destroy(self):
        self.kill()

    def update(self):
        self.player_input()


