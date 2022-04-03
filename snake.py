"""
File: snake.py
Author: Nishith Soni
Date: 01/11/2022
E-mail: nishith03@gmail.com
Description: This program is an implementation of a single player snake game.
"""

import pygame
import math
import random
import sys

# constants
WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = WIDTH // PIXELS

BG1 = (156, 210, 54)
BG2 = (147, 203, 57)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class Snake:
    def __init__(self):
        self.color = BLUE
        self.head_x = random.randrange(0, WIDTH, PIXELS)
        self.head_y = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.body_color = 255
        self.state = "STOP"

    def move_head(self):
        if self.state == "UP":
            self.head_y -= PIXELS

        elif self.state == "DOWN":
            self.head_y += PIXELS

        elif self.state == "RIGHT":
            self.head_x += PIXELS

        elif self.state == "LEFT":
            self.head_x -= PIXELS

    def move_body(self):
        if len(self.bodies) > 0:

            for i in range(len(self.bodies) - 1, -1, -1):

                if i == 0:
                    # move head of snake
                    self.bodies[0].pos_x = self.head_x
                    self.bodies[0].pos_y = self.head_y

                else:
                    # move snake body to position of the next body
                    self.bodies[i].pos_x = self.bodies[i - 1].pos_x
                    self.bodies[i].pos_y = self.bodies[i - 1].pos_y

    def add_body(self):
        # make color darker
        if self.body_color > 0:
            self.body_color -= 5

        # add body
        body = Body((0, 0, self.body_color), self.head_x, self.head_y)
        self.bodies.append(body)

    def draw(self, surface):
        # draw snake head
        pygame.draw.rect(surface, self.color, (self.head_x, self.head_y, PIXELS, PIXELS))

        # draw snake body
        if len(self.bodies) > 0:
            for body in self.bodies:
                body.draw(surface)

    def die(self):
        # reset snake
        self.head_x = random.randrange(0, WIDTH, PIXELS)
        self.head_y = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.body_color = 255
        self.state = "STOP"


class Body:

    def __init__(self, color, pos_x, pos_y):
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw(self, surface):
        # draw snake body
        pygame.draw.rect(surface, self.color, (self.pos_x, self.pos_y, PIXELS, PIXELS))


class Apple:
    def __init__(self):
        self.color = RED
        self.spawn()
        self.pos_x = random.randrange(0, WIDTH, PIXELS)
        self.pos_y = random.randrange(0, HEIGHT, PIXELS)

    def spawn(self):
        # new apple at random position
        self.pos_x = random.randrange(0, WIDTH, PIXELS)
        self.pos_y = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.pos_x + PIXELS // 2, self.pos_y + PIXELS // 2), PIXELS // 2)


class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont('monospace', 30, bold=False, italic=True)

    def increase(self):
        self.points += 1

    def reset(self):
        self.points = 0

    def show(self, surface):
        # print score label
        label = self.font.render(f"Score: {self.points}", True, BLACK)
        surface.blit(label, (5, 5))


def between_snake_and_apple(snake, apple):
    # snake collides with apple
    distance = math.sqrt(math.pow((snake.head_x - apple.pos_x), 2) + math.pow((snake.head_y - apple.pos_y), 2))
    return distance < PIXELS


def between_snake_and_walls(snake):
    # snake collides with wall
    if snake.head_x < 0 or snake.head_x > WIDTH - PIXELS or snake.head_y < 0 or snake.head_y > HEIGHT - PIXELS:
        return True
    return False


def between_head_and_body(snake):
    # snake collides with itself
    for body in snake.bodies:
        distance = math.sqrt(math.pow((snake.head_x - body.pos_x), 2) + math.pow((snake.head_y - body.pos_y), 2))
        if distance < PIXELS:
            return True
    return False


def draw(surface):
    # draw colored screen
    surface.fill(BG2)
    counter = 0
    for row in range(SQUARES):
        for col in range(SQUARES):
            if counter % 2 == 0:
                pygame.draw.rect(surface, BG1, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
            if col != SQUARES - 1:
                counter += 1


def main():
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SNAKE")

    # create objects
    snake = Snake()
    apple = Apple()
    score = Score()

    # main loop
    while True:

        # display everything
        draw(screen)
        snake.draw(screen)
        apple.draw(screen)
        score.show(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # move snake up
                if event.key == pygame.K_UP:
                    if snake.state != "DOWN":
                        snake.state = "UP"

                # move snake down
                if event.key == pygame.K_DOWN:
                    if snake.state != "UP":
                        snake.state = "DOWN"

                # move snake right
                if event.key == pygame.K_RIGHT:
                    if snake.state != "LEFT":
                        snake.state = "RIGHT"

                # move snake left
                if event.key == pygame.K_LEFT:
                    if snake.state != "RIGHT":
                        snake.state = "LEFT"

                # stop the snake
                if event.key == pygame.K_p:
                    snake.state = "STOP"

        # snake gets apple
        if between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()

        # move snake
        if snake.state != "STOP":
            snake.move_body()
            snake.move_head()

        # snake hits wall
        if between_snake_and_walls(snake):
            snake.die()
            apple.spawn()
            score.reset()

        # snake hits itself
        if between_head_and_body(snake):
            snake.die()
            apple.spawn()
            score.reset()

        pygame.time.delay(150)

        pygame.display.update()


main()
