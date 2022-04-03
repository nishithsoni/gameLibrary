"""
File: pong.py
Author: Nishith Soni
Date: 01/11/2022
E-mail: nishith03@gmail.com
Description: This program is an implementation of a 2-player pong game.
"""

import pygame
import sys

pygame.init()

# constants
WIDTH = 900
HEIGHT = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")


class Ball:
    def __init__(self, surface, color, pos_x, pos_y, radius):
        self.surface = surface
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.dx = 0
        self.dy = 0

        self.show()

    def show(self):
        # draw ball
        pygame.draw.circle(self.surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def start_moving(self):
        # speed of ball in each direction
        self.dx = 10
        self.dy = 5

    def move(self):
        # change position
        self.pos_x += self.dx
        self.pos_y += self.dy

    def paddle_collision(self):
        # ball bounces off in the x direction
        self.dx = -self.dx

    def wall_collision(self):
        # ball bounces off in the y direction
        self.dy = -self.dy

    def restart_pos(self):
        # reset ball
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.show()


class Paddle:
    def __init__(self, surface, color, pos_x, pos_y, width, height):
        self.surface = surface
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.state = "stopped"

        self.show()

    def show(self):
        # draw paddle
        pygame.draw.rect(self.surface, self.color, (self.pos_x, self.pos_y, self.width, self.height))

    def move(self):
        # move up
        if self.state == "up":
            self.pos_y -= 10

        # move down
        elif self.state == "down":
            self.pos_y += 10

    def clamp(self):
        # keep paddle from going above screen
        if self.pos_y <= 0:
            self.pos_y = 0

        # keep paddle from going below screen
        if self.pos_y + self.height >= HEIGHT:
            self.pos_y = HEIGHT - self.height

    def restart_pos(self):
        # reset paddle
        self.pos_y = HEIGHT // 2 - self.height // 2
        self.state = "stopped"
        self.show()


class Score:
    def __init__(self, surface, points, pos_x, pos_y):
        self.surface = surface
        self.points = points
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.font = pygame.font.SysFont("monospace", 80, bold=True, italic=True)
        self.label = self.font.render(self.points, True, WHITE)
        self.show()

    def show(self):
        # print score
        self.surface.blit(self.label, (self.pos_x - self.label.get_rect().width // 2, self.pos_y))

    def increase(self):
        # increment score
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, True, WHITE)

    def restart(self):
        # reset score
        self.points = "0"
        self.label = self.font.render(self.points, True, WHITE)


def between_ball_and_paddle_1(ball, paddle_1):
    # did ball hit left paddle
    if ball.pos_y + ball.radius > paddle_1.pos_y and ball.pos_y - ball.radius < paddle_1.pos_y + paddle_1.height:
        if ball.pos_x - ball.radius <= paddle_1.pos_x + paddle_1.width:
            return True

    return False


def between_ball_and_paddle_2(ball, paddle_2):
    # did ball hit right paddle
    if ball.pos_y + ball.radius > paddle_2.pos_y and ball.pos_y - ball.radius < paddle_2.pos_y + paddle_2.height:
        if ball.pos_x + ball.radius >= paddle_2.pos_x:
            return True

    return False


def between_ball_and_walls(ball):
    # did ball hit top wall
    if ball.pos_y - ball.radius <= 0:
        return True

    # did ball hit bottom wall
    if ball.pos_y + ball.radius >= HEIGHT:
        return True

    return False


def check_goal_player_1(ball):
    # did ball go past screen on the right
    return ball.pos_x - ball.radius >= WIDTH


def check_goal_player_2(ball):
    # did ball go past screen on the left
    return ball.pos_x + ball.radius <= 0


def paint_back():
    # draw game field
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)


def restart():
    # reset game
    paint_back()
    score_1.restart()
    score_2.restart()
    the_ball.restart_pos()
    left_paddle.restart_pos()
    right_paddle.restart_pos()


paint_back()

# create objects
the_ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 15)
left_paddle = Paddle(screen, WHITE, 15, HEIGHT // 2 - 60, 20, 120)
right_paddle = Paddle(screen, WHITE, WIDTH - 20 - 15, HEIGHT // 2 - 60, 20, 120)
score_1 = Score(screen, "0", WIDTH // 4, 15)
score_2 = Score(screen, "0", WIDTH - WIDTH // 4, 15)

playing = False

# main loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # start game
            if event.key == pygame.K_p:
                the_ball.start_moving()
                playing = True

            # restart game
            if event.key == pygame.K_r:
                restart()
                playing = False

            # move left paddle

            if event.key == pygame.K_w:
                left_paddle.state = "up"

            if event.key == pygame.K_s:
                left_paddle.state = "down"

            # move right paddle

            if event.key == pygame.K_UP:
                right_paddle.state = "up"

            if event.key == pygame.K_DOWN:
                right_paddle.state = "down"

        # paddles not moving
        if event.type == pygame.KEYUP:
            left_paddle.state = "stopped"
            right_paddle.state = "stopped"

    if playing:
        paint_back()

        the_ball.move()
        the_ball.show()

        left_paddle.move()
        left_paddle.clamp()
        left_paddle.show()

        right_paddle.move()
        right_paddle.clamp()
        right_paddle.show()

        if between_ball_and_paddle_1(the_ball, left_paddle):
            the_ball.paddle_collision()

        if between_ball_and_paddle_2(the_ball, right_paddle):
            the_ball.paddle_collision()

        if between_ball_and_walls(the_ball):
            the_ball.wall_collision()

        # if left paddle scored
        if check_goal_player_1(the_ball):
            paint_back()
            score_1.increase()
            the_ball.restart_pos()
            left_paddle.restart_pos()
            right_paddle.restart_pos()
            playing = False

        # if right paddle scored
        if check_goal_player_2(the_ball):
            paint_back()
            score_2.increase()
            the_ball.restart_pos()
            left_paddle.restart_pos()
            right_paddle.restart_pos()
            playing = False

    score_1.show()
    score_2.show()

    pygame.display.update()
