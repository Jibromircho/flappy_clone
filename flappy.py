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
    start = 0
    playing = 1
    game_over = 2
    def __init__(self):
        """Main function of the game"""
        pygame.init()
        #inintial game settings
        self.clock = pygame.time.Clock()
        self.settings = Settings() 
        self.screen = pygame.display.set_mode((self.settings.resolution))
        pygame.display.set_caption("Flappy Bird Clone")
        #game assets
        self.background = Background(self)
        #set initial game stuff
        self._initialize_game()
        self.add_pipe = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_pipe, self.settings.pipe_frequency)

    def _initialize_game(self):
        #initialize game settings and objects
        self.scoreboard = Scoreboard()
        self.scoreboard.reset_score()
        self.player = Player(self)
        self.pipe_group = pygame.sprite.Group()
        self.game_state = Flappy.start    

    def run_game(self):
        #main game loop
        while True:
            self.clock.tick(60)
            self._check_events()
            if self.game_state == Flappy.playing:
                self.player.update()
                self.pipe_group.update()
                self._check_collision()
                self._check_pipe_passed()
                self.scoreboard.update()
                self.background.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit game
                    sys.exit()
                if self.game_state == Flappy.start:
                    if event.key == pygame.K_SPACE:
                        self.game_state = Flappy.playing
                elif self.game_state == Flappy.playing:
                    if event.key == pygame.K_SPACE:
                        self.player.flap()
                elif self.game_state == Flappy.game_over:
                    if event.key == pygame.K_SPACE:
                        self._restart_game()
            if event.type == self.add_pipe:
                print("Adding pipes")
                self._spawn_pipes()

    def _restart_game(self):
        self._initialize_game()
        self.game_state = Flappy.start

    def _spawn_pipes(self):
        #spawn 2 pipes based on time interval
        y = randint(self.settings.resolution[1] // 3, self.settings.resolution[1] - self.settings.resolution[1] // 3)
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
        self.game_state = Flappy.game_over
        self.pipe_group.empty()

    def _game_paused(self):
        font = pygame.font.SysFont(None, 48)
        pause_text = font.render('Press SPACE to play', True, (255, 0, 0))
        self.screen.blit(pause_text, (self.settings.resolution[0] // 2 - pause_text.get_width() // 2,
                                      self.settings.resolution[1] // 2 - pause_text.get_height() // 2))

    def _check_pipe_passed(self):
        for pipe in self.pipe_group:
            if pipe.rect.centerx == self.player.rect.centerx:
                self.scoreboard.add_score()

    def _show_start_screen(self):
        font = pygame.font.SysFont(None, 48)
        instructions_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        self.screen.blit(instructions_text, (self.settings.resolution[0] // 2 - instructions_text.get_width() // 2, self.settings.resolution[1] // 2))
        
    def _show_game_over_screen(self):
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {int(self.scoreboard.score)}", True, (0, 0, 0))
        restart_game_text = font.render("Press SPACE to restart", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.settings.resolution[0] // 2 - game_over_text.get_width() // 2, self.settings.resolution[1] // 3))
        self.screen.blit(final_score_text, (self.settings.resolution[0] // 2 - final_score_text.get_width() // 2, self.settings.resolution[1] // 2))
        self.screen.blit(restart_game_text, (self.settings.resolution[0] // 2 - restart_game_text.get_width() // 2, self.settings.resolution[1] // 2.5))
    def _update_screen(self):
        #update each frame and flip to the next one
        self.background.draw()
        self.player.draw()
        if self.game_state == Flappy.start:
            self._show_start_screen()
        self.pipe_group.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.game_state == Flappy.game_over:
            self._show_game_over_screen()
        pygame.display.flip()

if __name__ == '__main__':
    flappy = Flappy()
    flappy.run_game()