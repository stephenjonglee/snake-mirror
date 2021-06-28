import pygame
import sys
import random
import pickle
from wall import Wall
from food import Food
from player import Player

__author__ = 'Stephen Lee'
__email__ = 'stephenjonglee@csu.fullerton.edu'
__maintainer__ = 'stephenjonglee'

def main():
    """ Main Function """
    # initialize pygame
    pygame.init()

    # screen resolution
    size = (720, 720)

    # display the window
    screen = pygame.display.set_mode(size)
    bg = pygame.Color('black')
    reset_screen(screen, bg)

    # caption title
    title = 'Snake on the Next Level'
    pygame.display.set_caption(title)

    # text settings
    font = pygame.font.SysFont("adiro", 35)
    color = pygame.Color('yellow')

    # clock
    clock = pygame.time.Clock()

    # snake settings
    direction = "right"
    fps = 25

    # score record
    score = 0

    # play loop
    again = True

    start_screen(screen, font, color, clock)
    reset_screen(screen, bg)
    print('start screen ended')
    while again:
        print('playing')
        play(screen, clock, fps)
        reset_screen(screen, bg)
        print('end')
        again = end_screen(screen, font, color, clock, score)
        reset_screen(screen, bg)
        print('again: ', again)
    close_screen(screen, font, color, clock)
    # quit pygame
    pygame.quit()
    print('pygame quitted')
    sys.exit()

def reset_screen(screen, color):
    screen.fill(color)

def start_screen(screen, font, color, clock):
    """ Function displays the start up screen """
    (w, h) = screen.get_size()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        show_message(screen, "Rules: Don't eat yourself or hit the wall.", font, color, 200)
        show_message(screen, "You get a point for every 3 seconds", font, color, 245)
        show_message(screen, "or when you eat a food", font, color, 290)
        show_message(screen, "Controls: To control the snake, use the keyboard", font, color, 400)
        show_message(screen, "down/left/right keys.", font, color, 445)
        show_message(screen, "Press any key to start.", font, color, 600)
        pygame.display.update()
        clock.tick(15)

def end_screen(screen, font, color, clock, score):
    """ Function displays the start up screen """
    again = True
    (w, h) = screen.get_size()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    running = False
                    again = True
                if event.key == pygame.K_n:
                    running = False
                    again = False
        show_message(screen, "Game Over.", font, color, 200)
        show_message(screen, f"You're score is {score}.", font, color, 400)
        show_message(screen, "Try again? (Press y/n).", font, color, 600)
        pygame.display.update()
        clock.tick(15)
    return again

def close_screen(screen, font, color, clock):
    """ Function displays the start up screen """
    (w, h) = screen.get_size()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        show_message(screen, "Thank You for playing!", font, color, 200)
        show_message(screen, "Please come again!", font, color, 400)
        show_message(screen, "Press any key to exit.", font, color, 600)
        pygame.display.update()
        clock.tick(15)

def show_message(screen, text, font, color, h):
    """ Functions shows the message on screen at center width and desired height """
    w = screen.get_width()
    text = font.render(text, True, color)
    text_pos = text.get_rect(center=(w/2, h))
    screen.blit(text, text_pos)

def create_walls(screen):
    (w, h) = screen.get_size()
    wall_color = pygame.Color('gray')
    cell_size = 10
    """ Draw the wall """
    walls = list()
    top_wall = Wall(screen, 0, 0, w, cell_size, wall_color)
    bottom_wall = Wall(screen, 0, h - cell_size, w, cell_size, wall_color)
    left_wall = Wall(screen, 0, 0, cell_size, h, wall_color)
    right_wall = Wall(screen, w - cell_size, 0, cell_size, h, wall_color)

    walls.append(top_wall)
    walls.append(bottom_wall)
    walls.append(left_wall)
    walls.append(right_wall)

    return walls

def play(screen, clock, fps):
    """ Function play the game """

    # Game Settings
    direction = ''
    (w, h) = screen.get_size()
    player_pos = (200, 200)
    player_color = pygame.Color('black')
    food_pos = (int(w / 2) - 10, int(h / 2) - 10)
    food_color = pygame.Color('red')

    score = 0
    score_str = "Score:0"

    # Initialize the game
    walls = create_walls(screen)
    player = Player(screen, player_pos, 5, player_color)
    food = Food(screen, food_pos, food_color)

    # Keeps track of the direction of the snake.
    dx, dy = 0, 0

    running = True

    while running:
        """ Events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    dx = -1
                    dy = 0
                if event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    dx = 1
                    dy = 0
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    dy = -1
                    dx = 0
                if event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    dy = 1
                    dx = 0

        """ Update snake """
        player.move(dx, dy)

        player_rect = player.get_rect()
        food_rect = food.get_rect()

        """ If snake at itself """
        if player.ate_itself():
            running = False

        """ If snake hit a wall """
        for wall_block in walls:
            wall_rect = wall_block.get_rect()
            if wall_rect.colliderect(player_rect):
                running = False

        """ If snake hits a food """
        # if snake collides with food, increase its length.
        if food_rect.colliderect(player_rect):
            score += 1
            player.increment_length()

            # generate food at random x, y.
            food.generate_food()

        """ Draw """
        screen.fill((255, 255, 255))

        # draw the food and snake.
        player.draw()
        food.draw()

        # draw the blocks.
        for wall_block in walls:
            wall_block.draw()

        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main()
