import random

import pygame


class Food:
    """
    Class containing all the methods for food
    """

    def __init__(self, surface, food_size):
        self.surface = surface
        self.food = food_size
        w, h = self.surface.get_size()
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)

    def make_apple(self):

        w, h = self.surface.get_size()
        if self.food_eaten == True:
            self.x = random.randint(0, w)
            self.y = random.randint(0, h)

    def draw_food(self):
        pygame.draw.circle(
            self.surface, (255, 0, 0), (self.x, self.y), int(self.food), int(self.food)
        )


class Snake:
    """
    Class containing all the methods required to make a snake
    """

    def __init__(
            self, starting_positionX, starting_positionY, shape_size, surface, movespeed
    ):
        self.shapeX = starting_positionX
        self.shapeY = starting_positionY
        self.shape_size = shape_size
        self.UI = surface
        self.movespeed = movespeed
        self.segments = 50
        self.body = []
        self.first_time = True

    def draw_head(self):

        for i in range(self.segments):

            x = self.shapeX
            y = self.shapeY
            pygame.draw.rect(
                self.UI, (0, 255, 0), (x, y, self.shape_size, self.shape_size)
            )

            if self.first_time == True:
                self.body.append((x, y))

    def draw_body(self) -> None:
        for i in self.body:
            pygame.draw.rect(
                self.UI, (0, 255, 0), (i[0], i[1], self.shape_size, self.shape_size)
            )

    def make_coordinates(self):
        del self.body[-1]

        insert = (self.shapeX, self.shapeY)
        self.body.insert(0, insert)

        self.draw_body()

    def move(
            self,
            leftDown,
            rightDown,
            upDown,
            down,
            playervX,
            playervY,
            windowWidth,
            windowHeight,
    ):
        game_alive = True
        if leftDown:

            if self.shapeX > 0:
                self.shapeX -= self.movespeed
                self.make_coordinates()
            elif self.shapeX == 0:
                self.draw_body()

        if rightDown:
            if self.shapeX + self.shape_size < windowWidth:
                self.shapeX += self.movespeed
                self.make_coordinates()

            elif self.shapeX + self.shape_size == windowWidth:
                self.draw_body()

        if upDown:
            if playervY > 0.0:
                playervY = self.movespeed
                playervY = -playervY
                if self.shapeY > 0:
                    self.shapeY -= self.movespeed
                    self.make_coordinates()
                elif self.shapeY == 0:
                    self.draw_body()

        if down:
            if playervY < 0.0:
                playervY = self.movespeed

            if self.shapeY + self.shape_size < windowHeight:
                self.shapeY += self.movespeed
                self.make_coordinates()

            elif self.shapeY + self.shape_size == windowHeight:
                self.draw_body()
                game_alive = False
        return game_alive


def main():
    # Pygame Variables
    clock = pygame.time.Clock()
    pygame.init()
    windowWidth = 800
    windowHeight = 800
    shape_size = 20
    shape_size_height = 20
    shapeX = windowWidth / 2
    shapeY = windowHeight / 2
    playervX = 1.0
    playervY = 1.0
    movespeed = 5
    leftDown = False
    rightDown = False
    upDown = False
    down = False
    window = pygame.display.set_mode((windowWidth, windowHeight))
    snake = Snake(shapeX, shapeY, shape_size, window, movespeed)
    food = Food(window, shape_size / 4)

    pygame.display.set_caption("Python Snake! ")

    while True:
        window.fill((0, 0, 0))
        snake.draw_head()
        snake.first_time = False
        clock.tick(60)
        food.draw_food()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if rightDown != True:
                        leftDown = True
                        rightDown = False
                        upDown = False
                        down = False

                if event.key == pygame.K_RIGHT:
                    if leftDown != True:
                        leftDown = False
                        rightDown = True
                        upDown = False
                        down = False

                if event.key == pygame.K_UP:
                    if down != True:
                        leftDown = False
                        rightDown = False
                        upDown = True
                        down = False

                if event.key == pygame.K_DOWN:
                    if upDown != True:

                        leftDown = False
                        rightDown = False
                        upDown = False
                        down = True

                if event.key == pygame.K_SPACE:
                    snake.segments += 100

        game_alive = snake.move(
            leftDown,
            rightDown,
            upDown,
            down,
            playervX,
            playervY,
            windowWidth,
            windowHeight,
        )
        if game_alive == False:
            window.fill((255, 255, 255))
        pygame.display.update()


main()
