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
        self.game_active = False
        #game assets
        self.backgound = Background(self)
        #pipe spawn event
        self.add_pipe = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe, self.settings.pipe_frequency)
        self._initialize_game()

    def _initialize_game(self):
        #initialize game settings and objects
        self.scoreboard = Scoreboard()
        self.player = Player(self)
        self.pipe_group = pygame.sprite.Group()
        self.scoreboard.reset_score()

    def run_game(self):
        #main game loop
        while True:
            self.clock.tick(60)
            self._check_events()
            if self.game_active:
                self.player.update()
                self.pipe_group.update()
                self._check_collision()
                self._check_pipe_passed()
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
                    #make jump or start game 
                    if not self.game_active:
                        self._restart_game()
                    else:
                        self.player.flap()
            if event.type == self.add_pipe:
                self._spawn_pipes()

    def _restart_game(self):
        self._initialize_game()
        self.game_active = True

    def _spawn_pipes(self):
        #spawn 2 pipes based on time interval
        y = randint(self.settings.resolution[1] // 4, self.settings.resolution[1] - self.settings.resolution[1] // 4)
        top_pipe = Pipe(self,self.settings.resolution[0], y, True)
        bottom_pipe = Pipe(self,self.settings.resolution[0], y, False)
        self.pipe_group.add(top_pipe)
        self.pipe_group.add(bottom_pipe)

    def _check_collision(self):
        #check for collision between pipes and player
        if pygame.sprite.spritecollideany(self.player, self.pipe_group, pygame.sprite.collide_mask):
            self._player_lost()
        if self.player.rect.bottom >= self.settings.resolution[1]:
            self._player_lost()

    def _player_lost(self):
        #end game if player hits pipe or falls down
        self.game_active = False
        pass

    def _game_paused(self):
        font = pygame.font.SysFont(None, 48)
        pause_text = font.render('Press SPACE to play', True, (255, 0, 0))
        self.screen.blit(pause_text, (self.settings.resolution[0] // 2 - pause_text.get_width() // 2,
                                      self.settings.resolution[1] // 2 - pause_text.get_height() // 2))

    def _check_pipe_passed(self):
        for pipe in self.pipe_group:
            if pipe.rect.centerx == self.player.rect.centerx:
                self.scoreboard.add_score()

    def _update_screen(self):
        #update each frame and flip to the next one
        self.backgound.draw()
        self.player.draw()
        self.pipe_group.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if not self.game_active:
            self._game_paused()
        pygame.display.flip()

if __name__ == '__main__':
    flappy = Flappy()
    flappy.run_game()