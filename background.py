import pygame

class Background:
    """Class for managing the background"""
    def __init__(self, flappy):
        #some backgound settings
        self.screen = flappy.screen
        self.settings = flappy.settings
        self.bg_image = pygame.image.load("images/background.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (1250, 800))
        self.bg_width = self.bg_image.get_width()
        self.bg_x1 = 0
        self.bg_x2 = self.bg_width

    def update(self):
        #update bg position for moving effect
        self.bg_x1 -= self.settings.bg_speed
        self.bg_x2 -= self.settings.bg_speed
        
        if self.bg_x1 <= -self.bg_width:
            self.bg_x1 = self.bg_width
        if self.bg_x2 <= -self.bg_width:
            self.bg_x2 = self.bg_width

    def draw(self):
        self.screen.blit(self.bg_image, (self.bg_x1, 0))
        self.screen.blit(self.bg_image, (self.bg_x2, 0))

