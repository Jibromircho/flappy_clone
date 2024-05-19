import pygame

class Scoreboard:
    def __init__(self):
        """Initializes the scoreboard"""
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)

    def reset_score(self):
        self.score = 0

    def add_score(self):
        self.score += 1

    def update(self):
        pass


    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}",True,(255, 255, 255))
        screen.blit(score_text, (10, 10))