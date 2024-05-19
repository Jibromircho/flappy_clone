import sys
import pygame
from random import randint

from settings import Settings
from player import Player
from pipes import Pipe
from background import Background
from scoreboard import Scoreboard

class Flappy:
    """The whoe class for the game"""

    def __init__(self):
        """Main function of the game"""
        pygame.init()
        #inintial game settings
        self.clock = pygame.time.Clock()
        self.settings = Settings() 
        self.screen = pygame.display.set_mode((self.settings.resolution), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Flappy Bird Clone")
        #game assets
        self.player = Player(self)
        self.pipe_group = pygame.sprite.Group()
        self.backgound = Background(self)
        self.scoreboard = Scoreboard()
        #pipe spawn event
        self.add_pipe = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe, self.settings.pipe_frequency)

    def run_game(self):
        #main game loop
        while True:
            self.clock.tick(60)
            self._check_events()
            self.player.update()
            self.pipe_group.update()
            self._check_collision()
            self.scoreboard.update()
            self.backgound.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit game
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    #make jump
                    self.player.flap()
            if event.type == self.add_pipe:
                #spawn 2 pipes based on time interval
                y = randint(self.settings.resolution[1] // 4, self.settings.resolution[1] - self.settings.resolution[1] // 4)
                top_pipe = Pipe(self,self.settings.resolution[0], y, True)
                bottom_pipe = Pipe(self,self.settings.resolution[0], y, False)
                self.pipe_group.add(top_pipe)
                self.pipe_group.add(bottom_pipe)

    def _check_collision(self):
        #check for collision between pipes and player
        if pygame.sprite.spritecollideany(self.player, self.pipe_group, pygame.sprite.collide_mask):
            self._player_lose()

    def _player_lose(self):
        #end game if player hits pipe or falls down
        print("player dead")
        pass





    def _update_screen(self):
        #update each frame and flip to the next one
        self.backgound.draw()
        self.player.draw()
        self.pipe_group.draw(self.screen)
        self.scoreboard.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    flappy = Flappy()
    flappy.run_game()