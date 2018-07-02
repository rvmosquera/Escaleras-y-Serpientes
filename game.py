import pygame
from cell import Cell
import random
import sys


def get_num_row(number):
    start_s = str(number)

    if len(start_s) == 1:
        return 1
    elif len(start_s) == 3:
        return 10
    else:
        return int(start_s[0]) + 1


def exist_num(list, num):
    var = False
    for elemen in list:
        if elemen[0] == num or elemen[1] == num:
            var = True
            break

    return var


def get_ladders_cells():
    ladder_se = []
    for i in range(1, 7):
        start = random.randint(3, 89)

        while exist_num(ladder_se, start):
            start = random.randint(3, 89)

        row_s = get_num_row(start)

        if row_s == 9:
            row = 10
        else:
            row = row_s + 2

        end = 0
        row_e = 1

        while row_e < row:
            end = random.randint(start, 98)
            if exist_num(ladder_se, end):
                continue

            row_e = get_num_row(end)

        ladder_se.append([start, end])
    ladder_se.sort()

    return ladder_se


def get_snakes_cells(ladders_se):
    snakes_se = []
    list = ladders_se[:]
    for i in range(1, 7):
        start = random.randint(3, 89)

        while exist_num(list, start):
            start = random.randint(3, 89)

        row_s = get_num_row(start)

        if row_s == 9:
            row = 10
        else:
            row = row_s + 2

        end = 0
        row_e = 1

        while row_e < row:
            end = random.randint(start, 98)
            if exist_num(list, end):
                continue

            row_e = get_num_row(end)

        snakes_se.append([start, end])
        list.append([start, end])

    snakes_se.sort()

    return snakes_se

def draw_all_ladders(ladder_points):

    for element in ladder_points:
        draw_ladder(Cells[element[0]], Cells[element[1]])
#    draw_ladder(Cells[6], Cells[31])
#    draw_ladder(Cells[20], Cells[39])
#    draw_ladder(Cells[61], Cells[99])
#    draw_ladder(Cells[67], Cells[86])
#    draw_ladder(Cells[71], Cells[92])
#    draw_ladder(Cells[77], Cells[97])


def draw_all_snakes(snake_points):

    for element in snake_points:
        draw_snake(Cells[element[1]], Cells[element[0]])
#    draw_snake(Cells[53], Cells[34])
#    draw_snake(Cells[63], Cells[37])
#    draw_snake(Cells[68], Cells[27])
#    draw_snake(Cells[75], Cells[43])
#    draw_snake(Cells[96], Cells[83])


def draw_pointer(player, x, y):
    if player == 1:
        pygame.draw.circle(gameDisplay, blue, (int(x), int(y)), 25, 2)
    else:
        pygame.draw.circle(gameDisplay, white, (int(x), int(y)), 25, 2)


def text_objects(text, font, color):
    textsurface = font.render(text, True, color)
    return textsurface, textsurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smalltext = pygame.font.Font("freesansbold.ttf", 20)
    textsurf, textrect = text_objects(msg, smalltext, yellow)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textsurf, textrect)


def random_generator():
    global to_move
    global number_of_moves

    smalltext = pygame.font.Font("freesansbold.ttf", 40)
    pygame.draw.circle(gameDisplay, black, (1100, 600), 30, 0)
    pygame.draw.circle(gameDisplay, black, (100, 600), 30, 0)

    to_move = random.randint(1, 6)  # Dado
    number_of_moves += 1
    textsurf, textrect = text_objects(str(to_move), smalltext, yellow)
    if number_of_moves % 2 == 0:
        textrect.center = (100, 600)
    else:
        textrect.center = (1100, 600)
    gameDisplay.blit(textsurf, textrect)

    move_pointer()


def move_pointer():
    global pointer_location_1  # For player 1
    global pointer_location_2  # For player 2
    global to_move
    global Ladders
    global Snakes
    global done
    global won
    global jugador  # RMP 25.06.2018 12:41

    if number_of_moves % 2 == 0:  # RMP 25.06.2018 12:41
        jugador = 2
    else:
        jugador = 1

    if jugador == 1:  # RMP 25.06.2018 12:41
        pointer_location = pointer_location_1
    elif jugador == 2:
        pointer_location = pointer_location_2

    current_cell = Cells[pointer_location]
    pygame.draw.rect(gameDisplay, black, (current_cell.x, current_cell.y, cell_width, cell_height), 0)
    c = Cell(current_cell.x, current_cell.y, str(pointer_location + 1), gameDisplay)

    pointer_location = pointer_location + to_move

    if pointer_location >= 99:
        done = True
        won = True
        print_victory_message()

    else:
        new_cell = Cells[pointer_location]

        if new_cell in Ladders.keys():
            new_cell = Ladders[new_cell]
            draw_pointer(jugador, new_cell.center_x, new_cell.center_y)

        elif new_cell in Snakes.keys():
            new_cell = Snakes[new_cell]
            draw_pointer(jugador, new_cell.center_x, new_cell.center_y)

        else:
            draw_pointer(jugador, new_cell.center_x, new_cell.center_y)

        pointer_location = int(new_cell.number) - 1

        if pointer_location == 99:
            done = True
            print_victory_message()

        if jugador == 1:  # RMP 25.06.2018 12:41
            pointer_location_1 = pointer_location  # RMP 25.06.2018 12:41
        elif jugador == 2:  # RMP 25.06.2018 12:41
            pointer_location_2 = pointer_location  # RMP 25.06.2018 12:41


def print_victory_message():
    global number_of_moves
    pygame.mixer.music.stop
    smalltext = pygame.font.SysFont('comicsansms', 50)
    textsurf, textrect = text_objects("Ganaste! Acabaste en " + str(number_of_moves) + " jugadas", smalltext, red)
    textrect.center = (600, 100)
    gameDisplay.blit(textsurf, textrect)


def draw_ladder(start, end):
    ladder_color = (240, 84, 12)
    pygame.draw.line(gameDisplay, ladder_color,
                     (start.center_x, start.center_y),
                     (end.center_x, end.center_y), 4)
    Ladders[start] = end


def draw_snake(start, end):
    snake_color = (179, 240, 12)
    pygame.draw.line(gameDisplay, snake_color, (start.center_x, start.center_y), (end.center_x, end.center_y), 6)
    Snakes[start] = end


'''
main loop with the game loop inside
'''

pygame.init()

display_width = 1200
display_height = 900

cell_width = 70
cell_height = 70

first_cell_x = 250
first_cell_y = 600
# pygame.mixer.music.load("")

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Serpientes y Escaleras v. 1.1')

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
bright_green = (0, 255, 0)
green = (0, 200, 0)

pygame.mixer.music.load('musica.mp3')  #Valeria

clock: None = pygame.time.Clock()
done = False
won = False

Cells = []
Ladders = {}
Snakes = {}

to_move = 0
pointer_location_1 = 0
pointer_location_2 = 0
jugador = 1
number_of_moves = 0

draw_pointer(1, first_cell_x + int(cell_width / 2), first_cell_y + int(cell_height / 2))  # Player 1

ladder_se = get_ladders_cells()
snakes_se = get_snakes_cells(ladder_se)
#snakes_se = [[44, 3], [53, 34], [63, 37], [68, 27], [75, 43], [96, 83]]

pygame.mixer.music.play()
while not done:
    fwd = True
    cur_x, cur_y = first_cell_x, first_cell_y
    for i in range(10):
        for j in range(1, 11):
            if fwd:
                c = Cell(cur_x, cur_y, str(i * 10 + j), gameDisplay)
                cur_x = cur_x + cell_width
                Cells.append(c)
            else:
                c = Cell(cur_x, cur_y, str(i * 10 + j), gameDisplay)
                cur_x = cur_x - cell_width
                Cells.append(c)

        cur_y = cur_y - cell_height
        if fwd:
            cur_x = cur_x - cell_width
        else:
            cur_x = cur_x + cell_width

        fwd = not fwd

    draw_all_ladders(ladder_se)
    draw_all_snakes(snakes_se)

    if number_of_moves % 2 == 0:
        pygame.draw.rect(gameDisplay, black, (70, 400, 150, 50))
        button("Lanza el dado!", 1000, 400, 150, 50, green, bright_green, random_generator)
    else:
        pygame.draw.rect(gameDisplay, black, (1000, 400, 150, 50))
        button("Lanza el dado!", 70, 400, 150, 50, green, bright_green, random_generator)

    if number_of_moves == 1:
        draw_pointer(2, first_cell_x + int(cell_width / 2), first_cell_y + int(cell_height / 2))  # Player 2

    pygame.draw.circle(gameDisplay, blue, (1100, 600), 50, 5)  # Player 1
    pygame.draw.circle(gameDisplay, white, (100, 600), 50, 5)  # Player 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                random_generator()

    pygame.display.update()
    clock.tick(30)

if done and not won:
    pygame.quit()

else:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()