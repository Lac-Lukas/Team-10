import pygame, sys
from settings import *
from mainmenu import mainmenu

class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #creates display surface and a clock
        pygame.display.set_caption('RPG')
        self.clock = pygame.time.Clock()

        #set up game audio
        pygame.mixer.init()
        pygame.mixer.music.load("../Audio/background.ogg")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

        self.mainmenu = mainmenu(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.mainmenu.run(self.screen, self.clock, "RPG GAME")
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__': #checks if its the mainfile then creates an instance of the game and runs it
    game = Game()
    game.run()