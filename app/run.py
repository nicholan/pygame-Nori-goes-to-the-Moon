import pygame
from game import Game 

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.run()
    pygame.quit()