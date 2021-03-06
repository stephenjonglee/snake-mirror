#!/usr/bin/env python3
""" Snake on the Next Level Game - Main File """

__author__ = 'Stephen Lee'
__email__ = 'stephenjonglee@csu.fullerton.edu'
__maintainer__ = 'stephenjonglee'

import sys
import pickle
import os
from datetime import date
import pygame
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
    size = (720, 760)

    # display the window
    screen = pygame.display.set_mode(size)
    background_color = pygame.Color('black')
    screen.fill(background_color)

    # caption title
    title = 'Snake on the Next Level'
    pygame.display.set_caption(title)

    # text settings
    font = pygame.font.SysFont("Roboto", 35)
    color = pygame.Color('yellow')
    score_color = pygame.Color('orange')

    # clock
    clock = pygame.time.Clock()
    time = 0

    # snake settings
    fps = 25

    # score data
    data_file = 'data.pkl'

    # play loop
    again = True

    # start screen with rules and controls
    start_screen(screen, background_color, font, color, clock)
    while again:
        # start time
        start_time = pygame.time.get_ticks()
        # play the snake game
        score = play(screen, background_color, font, score_color, clock, start_time, fps)
        # get the total time played
        time = pygame.time.get_ticks() - start_time
        # end screen prompt to play again
        again = end_screen(screen, background_color, font, color, clock, score, time, data_file)
    close_screen(screen, background_color, font, color, clock)

    # quit pygame
    print('exiting')
    pygame.quit()
    sys.exit()


def start_screen(screen, background_color, font, color, clock):
    """ Function displays the start up screen """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exiting')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False
        screen.fill(background_color)
        show_message(screen, "Rules: Don't eat yourself or hit the wall.", font, color, 200)
        show_message(screen, "You get a point for every 3 seconds", font, color, 245)
        show_message(screen, "or when you eat a food", font, color, 290)
        show_message(screen, "Controls: To control the snake, use the keyboard", font, color, 400)
        show_message(screen, "down/left/right keys.", font, color, 445)
        show_message(screen, "Press any key to start.", font, color, 600)
        pygame.display.update()
        clock.tick(15)


def end_screen(screen, background_color, font, color, clock, score, time, data_file):
    """ Function displays the start up screen """
    # get scores data
    scores = read_score(data_file)
    high_score = max(scores, key=lambda x: x['Score'])

    again = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exiting')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    running = False
                    again = True
                if event.key == pygame.K_n:
                    running = False
                    again = False
        screen.fill(background_color)
        show_message(screen, "Game Over.", font, color, 100)
        show_message(screen, f"You're score is {score}.", font, color, 200)
        show_message(screen, f"High score: {high_score['Score']}", font, color, 300)
        if score > high_score['Score']:
            show_message(screen, f"You beat the high score!", font, color, 400)
        else:
            show_message(screen, f"You didn't beat high score...", font, color, 400)
        show_message(screen, "Try again? (Press y/n).", font, color, 500)
        pygame.display.update()
        clock.tick(15)

    # save score
    today = date.today()
    data = {'Date': today, 'Time': time, 'Score': score}
    scores.append(data)
    save_score(data_file, scores)

    return again


def close_screen(screen, background_color, font, color, clock):
    """ Function displays the start up screen """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exiting')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False
        screen.fill(background_color)
        show_message(screen, "Thank You for playing!", font, color, 200)
        show_message(screen, "Please come again!", font, color, 400)
        show_message(screen, "Press any key to exit.", font, color, 600)
        pygame.display.update()
        clock.tick(15)


def show_message(screen, text, font, color, height):
    """ Functions shows the message on screen at center width and desired height """
    width = screen.get_width()
    text = font.render(text, True, color)
    text_pos = text.get_rect(center=(width/2, height))
    screen.blit(text, text_pos)


def create_walls(screen):
    """ Function creates the list of walls """
    (width, height) = screen.get_size()
    wall_color = pygame.Color('gray')
    cell_size = 10
    buffer = 40
    walls = list()

    top_wall = Wall(screen, 0, 0 + buffer, width, cell_size, wall_color)
    bottom_wall = Wall(screen, 0, height - cell_size, width, cell_size, wall_color)
    left_wall = Wall(screen, 0, 0 + buffer, cell_size, height, wall_color)
    right_wall = Wall(screen, width - cell_size, 0 + buffer, cell_size, height, wall_color)

    walls.append(top_wall)
    walls.append(bottom_wall)
    walls.append(left_wall)
    walls.append(right_wall)

    return walls


def play(screen, background_color, font, color, clock, start_time, fps):
    """ Function play the game """
    # Game Settings
    direction = ''
    (width, height) = screen.get_size()
    player_pos = (200, 200)
    player_color = pygame.Color('yellow')
    food_pos = (int(width / 2) - 10, int(height / 2) - 10)
    food_color = pygame.Color('green')
    score = 0
    interval_start = start_time

    # Initialize the game
    walls = create_walls(screen)
    player = Player(screen, player_pos, 5, player_color)
    food_list = []
    food_list.append(food_pos)
    food = Food(screen, food_pos, food_color)

    # Direction of the player
    x_dir, y_dir = 0, 0

    running = True

    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    x_dir = -1
                    y_dir = 0
                if event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    x_dir = 1
                    y_dir = 0
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    y_dir = -1
                    x_dir = 0
                if event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    y_dir = 1
                    x_dir = 0

        # update player
        player.move(x_dir, y_dir)

        # get rectangle objects for collision check
        player_rect = player.get_rect()

        # check if player ate itself
        if player.ate_itself():
            running = False

        # check if player hit wall
        for wall_block in walls:
            wall_rect = wall_block.get_rect()
            if wall_rect.colliderect(player_rect):
                running = False

        # check if player ate a food
        for pos in food_list:
            food = Food(screen, pos, food_color)
            food_rect = food.get_rect()
            if food_rect.colliderect(player_rect):
                score += 1
                player.increment_length()
                food_list.remove(pos)

        # every 3 seconds increase score and generate another food
        interval = pygame.time.get_ticks() - interval_start
        if interval > 3000:
            score += 1
            pos = food.generate_food()
            if pos not in food_list:
                food_list.append(pos)
            interval_start = pygame.time.get_ticks()

        # draw
        screen.fill(background_color)

        # draw the player
        player.draw()

        # draw the list of food
        for pos in food_list:
            food = Food(screen, pos, food_color)
            food.draw()

        # draw the blocks.
        for wall_block in walls:
            wall_block.draw()

        # draw the score
        score_text = font.render(f'Score: {score}', True, color)
        screen.blit(score_text, (300, 10, 20, 20))

        pygame.display.update()
        clock.tick(fps)

    return score

def save_score(data_file, data):
    """ Function saves the score into the data file """
    with open(data_file, 'wb') as file:
        pickle.dump(data, file)

def read_score(data_file):
    """ Function reads the data file, if empty return default data """
    if os.path.isfile(data_file):
        with open(data_file, 'rb') as file:
            data = pickle.load(file)
    else:
        data = [{'Date': 0, 'Time': 0, 'Score': 0}]
        with open(data_file, 'wb') as file:
            pickle.dump(data, file)
    return data

if __name__ == '__main__':
    main()
