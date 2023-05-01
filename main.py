import pygame
import time
import math
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

    def checkCollision(self, fish):
        fish_midpoint = fish.y - (self.height / 2)

        if fish_midpoint > self.y and fish_midpoint < self.y + self.height:
            print("COLLISION")

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
        pygame.display.update()

        cursor.checkCollision(fish)

        clock.tick(100)
    
    pygame.quit()

def main():
    window, clock = init()
    gameLoop(window, clock)

main()