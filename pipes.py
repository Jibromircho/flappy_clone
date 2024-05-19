import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, flappy, x, y, is_top):
        super().__init__()
        self.screen = flappy.screen
        self.screen_rect = flappy.screen.get_rect()
        self.settings = flappy.settings
        self.image = pygame.image.load("images/pipe.png")
        self.image = pygame.transform.scale(self.image, (340, 360))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        if is_top:
            self.rect.bottomleft = (x, y - self.settings.pipe_gap // 2)
            self.image = pygame.transform.rotate(self.image, 180)
        else:
            self.rect.topleft = (x, y + self.settings.pipe_gap // 2)

    def update(self):
        self.rect.x -= self.settings.pipe_speed
        if self.rect.right < 0:
            self.kill()