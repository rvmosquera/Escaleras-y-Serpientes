import pygame
import random

white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 200, 0)
black = (0, 0, 0)

cell_width = 70
cell_height = 70

fill = white  # RMP


def text_objects(text, font):
    textsurface = font.render(text, True, yellow)
    return textsurface, textsurface.get_rect()


class Cell:

    def __init__(self, x, y, number, game_display):
        self.x = x
        self.y = y
        self.center_x = x + cell_width / 2
        self.center_y = y + cell_height / 2
        self.number = str(number)

        if int(number) % 6 == 0:
            fill = white
        elif int(number) % 6 == 1:
            fill = red
        elif int(number) % 6 == 2:
            fill = blue
        elif int(number) % 6 == 3:
            fill = yellow
        elif int(number) % 6 == 4:
            fill = green
        elif int(number) % 6 == 5:
            fill = black

        # pygame.draw.rect(gameDisplay, fill, (
        # x, y, cell_width, cell_height))
        pygame.draw.rect(game_display, white, (x, y, cell_width, cell_height), 2)
        smalltext = pygame.font.SysFont('comicsansms', 20)  # 30)
        textsurf, textrect = text_objects(number, smalltext)
        textrect.center = (x + (cell_width / 2), (y + (cell_height / 2)))
        # textRect.center = (x + 10, (y + cell_height + 10))
        game_display.blit(textsurf, textrect)

