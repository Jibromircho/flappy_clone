import sys
import pygame

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/player.png")
        self.image = pygame.transform.scale(self.image, (70, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    def draw(self):
        self.screen.blit(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Image Scaling Demo")

    player = Player(screen)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the player
        player.draw()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()