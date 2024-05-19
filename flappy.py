import sys
import pygame
from random import randint

from settings import Settings
from player import Player
from pipes import Pipe

class Flappy:
    """The whoe class for the game"""

    def __init__(self):
        """Main function of the game"""
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.settings = Settings() 
        self.screen = pygame.display.set_mode((self.settings.resolution))
        pygame.display.set_caption("Flappy Bird Clone")
        self.player = Player(self)
        self.pipe_group = pygame.sprite.Group()
        self.add_pipe = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe, self.settings.pipe_frequency)

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self.pipe_group.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    #make jump
                    self.player.flap()
            if event.type == self.add_pipe:
                y = randint(self.settings.resolution[1] // 4, self.settings.resolution[1] - self.settings.resolution[1] // 4)
                top_pipe = Pipe(self,self.settings.resolution[0], y, True)
                bottom_pipe = Pipe(self,self.settings.resolution[0], y, False)
                self.pipe_group.add(top_pipe)
                self.pipe_group.add(bottom_pipe)




    def _update_screen(self):
        self.screen.fill((250, 250, 250))
        self.player.draw()
        self.pipe_group.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    flappy = Flappy()
    flappy.run_game()