import pygame

class Pipe(pygame.sprite.Sprite):
    """A class for managing the pipes"""
    def __init__(self, flappy, x, y, is_top):
        #pipe settings
        super().__init__()
        self.screen = flappy.screen
        self.settings = flappy.settings
        #load image
        self.image = pygame.image.load("images/pipe.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pipe_mask = pygame.mask.from_surface(self.image)
        #check if we need a top or bottom pipe
        if is_top:
            self.rect.bottomleft = (x, y - self.settings.pipe_gap // 2)
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.rect.topleft = (x, y + self.settings.pipe_gap // 2)
        

    def update(self):
        #simple movement adn deletion for the pipes
        self.rect.x -= self.settings.pipe_speed
        if self.rect.right < 0:
            self.kill()
    
