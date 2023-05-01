import pygame
import random
import os

# Define colour constants
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

class Cursor():
    def __init__(self, window : pygame.Surface):
        self.momentum = 0
        self.width = 20
        self.height = 80
        self.y = window.get_height() - self.height
        self.progress_bar = ProgressBar(window=window)
    
    def spacePressed(self):
        if self.y > 0:
            self.y -= 3
            self.momentum -= 0.5
            self.y = max(self.momentum + self.y, 0)
        
    def noKeyPressed(self, window : pygame.Surface):
        if self.y < window.get_height() - self.height:
            self.y += 3
            self.momentum += 0.5
            self.y = min(self.momentum + self.y, window.get_height() - self.height)

    def draw(self, window : pygame.Surface):
        if self.y < 0:
            self.y = 0
        elif self.y > window.get_height() - self.height:
            self.y = window.get_height() - self.height
        pygame.draw.rect(window, green, [0, self.y, self.width, self.height])

        self.progress_bar.draw(window=window)

    def checkCollision(self, fish):
        fish_midpoint = fish.y - (self.height / 2)

        if fish_midpoint > self.y and fish_midpoint < self.y + self.height:
            self.progress_bar.update("Collision")
        else: 
            self.progress_bar.update("No Collision")

class Fish():
    def __init__(self, window : pygame.Surface, name : str):
        self.momentum = 0
        self.width = 20
        self.height = 20
        self.y = window.get_height() - self.height
        self.name = name 
        self.image = pygame.image.load(os.path.join(os.sys.path[0], name + ".png"))

    def draw(self, window : pygame.Surface):
        window.blit(self.image, (0, self.y))

    def move(self, window : pygame.Surface):
        move = random.randint(-2, 2)
        self.y = min(move + self.y, window.get_height() - self.height)
        self.y = self.y = max(move + self.y, 0)

class ProgressBar():
    def __init__(self, window : pygame.Surface):
        self.width = 20
        self.x = 40
        self.y = window.get_height()
        self.height = window.get_height()
        self.complete = False

    def update(self, update : str):
        if update == "Collision":
            self.y -= 5
        else:
            if self.y < self.height:
                self.y += 5
        
        if self.y == 0:
            self.complete = True
        
    def draw(self, window : pygame.Surface):
        pygame.draw.rect(window, green, [self.x, self.y, self.width, self.height])

def init():
    # Initialise PyGame window
    pygame.init()

    # Define window height and width
    window_width = 600
    window_height = 600

    # Set up display window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Fishing Game")

    clock = pygame.time.Clock()

    return window, clock

def gameLoop(window, clock):
    game_over = False
    cursor = Cursor(window=window)
    fish = Fish(window, "fish")

    while not game_over:
        space_pressed = False

        fish.move(window=window)

        # Code for human player events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    cursor.spacePressed()
                    space_pressed = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            cursor.spacePressed()
            space_pressed = True

        if not space_pressed:
            cursor.noKeyPressed(window=window)
        
        window.fill(black)
        cursor.draw(window=window)
        fish.draw(window=window)
        cursor.checkCollision(fish)
        pygame.display.update()

        if cursor.progress_bar.complete:
            print("COMPLETED!")
            pygame.quit()

        clock.tick(100)
    
    pygame.quit()

def main():
    window, clock = init()
    gameLoop(window, clock)

main()