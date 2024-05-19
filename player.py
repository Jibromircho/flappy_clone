import pygame

class Player:

    def __init__(self,flappy):
        """A class to manage the player"""
        #init some player settings 
        self.screen = flappy.screen
        self.screen_rect = flappy.screen.get_rect()
        self.settings = flappy.settings
        self.velocity = 1
        self.angle = 0
        #load player image
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 60))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.player_mask = pygame.mask.from_surface(self.image)
        #postition player initialy
        self.rect.midleft = self.screen_rect.midleft
        self.rect.centerx += 200
        self.rect.centery = self.screen_rect.centery


    def draw(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        #update function for updating the players postition and angle based on gravity/velocity
        self.velocity += self.settings.gravity
        self.rect.y += self.velocity
        self.angle = -self.velocity * 3
        self.angle = max(min(self.angle, 25), -25)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def flap(self):
        #a simple flap function to handle what happends when the plyer "flaps"
        self.velocity = self.settings.flap_strenght
