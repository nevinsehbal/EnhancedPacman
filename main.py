from pacman import *

def init_environment():
    # Call this function so the Pygame library can initialize itself
    pygame.init()

    #Add music
    pygame.mixer.init()
    pygame.mixer.music.load('pacman.mp3')
    pygame.mixer.music.play(-1, 0.0)

    # Create an 606x606 sized screen
    screen = pygame.display.set_mode([606, 606])

    # Set the title of the window
    pygame.display.set_caption('Pacman')
    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())
    # Used for converting color maps and such
    background = background.convert()
    # Fill the screen with a black background
    background.fill(black)
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)
    return screen, clock, font


if __name__ == '__main__':

    screen, clock, font = init_environment()
    startGame(screen, clock, font)
    pygame.quit()