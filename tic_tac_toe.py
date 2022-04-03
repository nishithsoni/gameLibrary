"""
File: tic_tac_toe.py
Author: Nishith Soni
Date: 01/11/2022
E-mail: nishith03@gmail.com
Description: This program is an implementation of a 2-player tic-tac-toe game.
"""

import pygame
import sys
import numpy as np

pygame.init()

# constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 13
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 13
CROSS_WIDTH = 20
SPACE = 55

# rgb colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

# create board
board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_lines():

    # horizontal line 1
    pygame.draw.line(screen, LINE_COLOR, (15, SQUARE_SIZE), (WIDTH - 15, SQUARE_SIZE), LINE_WIDTH)
    # horizontal line 2
    pygame.draw.line(screen, LINE_COLOR, (15, 2 * SQUARE_SIZE), (WIDTH - 15, 2 * SQUARE_SIZE), LINE_WIDTH)
    # vertical line 1
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 15), (SQUARE_SIZE, HEIGHT - 15), LINE_WIDTH)
    # vertical line 2
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 15), (2 * SQUARE_SIZE, HEIGHT - 15), LINE_WIDTH)


def draw_figures():

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):

            if board[row][col] == 1:
                # draw X
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

            elif board[row][col] == 2:
                # draw O
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def check_win(player):

    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal_line(player)
        return True

    # descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_des_diagonal_line(player)
        return True

    return False


def draw_vertical_winning_line(col, player):

    pos_x = col * SQUARE_SIZE + SQUARE_SIZE // 2

    color = None
    if player == 1:
        color = CROSS_COLOR
    elif player == 2:
        color = CIRCLE_COLOR

    # draw vertical line
    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_winning_line(row, player):

    pos_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    color = None
    if player == 1:
        color = CROSS_COLOR
    elif player == 2:
        color = CIRCLE_COLOR

    # draw horizonal line
    pygame.draw.line(screen, color, (15, pos_y), (WIDTH - 15, pos_y), LINE_WIDTH)


def draw_asc_diagonal_line(player):

    color = None
    if player == 1:
        color = CROSS_COLOR
    elif player == 2:
        color = CIRCLE_COLOR

    # draw ascending diagonal line
    pygame.draw.line(screen, color, (30, HEIGHT - 30), (WIDTH - 30, 30), LINE_WIDTH)


def draw_des_diagonal_line(player):

    color = None
    if player == 1:
        color = CROSS_COLOR
    elif player == 2:
        color = CIRCLE_COLOR

    # draw descending diagonal line
    pygame.draw.line(screen, color, (30, 30), (WIDTH - 30, HEIGHT - 30), LINE_WIDTH)


def restart():

    # reset all game conditions
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


# initialize board and variables
draw_lines()
current_player = 1
game_over = False

# main loop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            # find position clicked
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            # find box clicked
            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)

            if available_square(clicked_row, clicked_col):

                mark_square(clicked_row, clicked_col, current_player)

                # if 3 in a row, game won
                if check_win(current_player):
                    game_over = True

                # switch to next player
                current_player = current_player % 2 + 1

                # draw player's symbol
                draw_figures()

        # restart the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                current_player = 1
                game_over = False

    pygame.display.update()
