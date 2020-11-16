import random
import pygame


class Food(pygame.sprite.Sprite):
    """
    Class containing all the methods for food
    """

    def __init__(self, surface, food_size, colour=(255, 0, 0)):
        super().__init__()
        self.surface = surface
        self.food = food_size
        self.image = pygame.Surface([food_size, food_size])
        self.image.fill(colour)
        self.rect = self.image.get_rect()

    def make_apple(self):
        w, h = self.surface.get_size()
        if self.food_eaten == True:
            self.x = random.randint(0, w)
            self.y = random.randint(0, h)

    def draw_food(self):
        pass


class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, shape_size, name, colour=(0, 255, 0)):
        super().__init__()
        self.image = pygame.Surface([shape_size, shape_size])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.name = name


class Button:
    def __init__(
        self, positionX, positionY, shape_size, surface, text, colour=(0, 0, 255)
    ):
        self.positionX = positionX
        self.positionY = positionY
        self.shape_size = shape_size
        self.UI = surface
        self.button_text = text
        self.colour = colour
        self.font = pygame.font.SysFont(None, 24)

    def draw_rect(self):
        pygame.draw.rect(
            self.UI,
            self.colour,
            (self.positionX, self.positionY, self.shape_size * 4, self.shape_size),
        )
        self.UI.blit(
            self.font.render(self.button_text, True, (255, 0, 0)),
            (self.positionX, self.positionY),
        )

    def check_pos(self, position):
        if int(position[0]) in range(
            int(self.positionX), int(self.positionX + self.shape_size * 4)
        ):
            if int(position[1]) in range(
                int(self.positionY), int(self.positionY + self.shape_size)
            ):

                return True


class Snake(pygame.sprite.Sprite):
    """
    Class containing all the methods required to make a snake
    """

    def __init__(
        self, starting_positionX, starting_positionY, shape_size, surface, movespeed
    ):
        pygame.sprite.Sprite.__init__(self)
        self.shapeX = starting_positionX
        self.shapeY = starting_positionY
        self.shape_size = shape_size
        self.UI = surface
        colour = (0, 255, 0)
        self.movespeed = movespeed
        self.segments = 25
        self.body = []
        self.first_time = True
        self.image = pygame.Surface([shape_size, shape_size])
        self.image.fill(colour)
        self.group = pygame.sprite.Group()
        self.growth = 8
        self.body_group = pygame.sprite.Group()
        self.counter = 0
        self.time_delta = 0
        self.last_time = 0
        self.first_up = False
        self.first_down = False

    def draw_head(self):

        for i in range(self.segments):
            if self.first_time == True:
                if i == 0:

                    body_snake = SnakeBody(self.shape_size, "head")
                    body_snake.rect.x = self.shapeX
                    body_snake.rect.y = self.shapeY
                    self.body.append(body_snake)

                else:

                    body_snake = SnakeBody(self.shape_size, "body")
                    body_snake.rect.x = self.shapeX
                    body_snake.rect.y = self.shapeY
                    self.body.append(body_snake)

                    self.make_coordinates()

    def draw_body(self) -> None:

        for i in self.group:
            i.kill()
        for i in self.body:
            self.group.add(i)

        self.group.draw(self.UI)

    def make_coordinates(self):
        del self.body[-1]
        head_snake = SnakeBody(self.shape_size, "head")
        head_snake.rect.x = self.shapeX
        head_snake.rect.y = self.shapeY
        self.body.insert(0, head_snake)
        self.body_group = self.body[20:]
        self.draw_body()

    def move(
        self,
        left_down,
        right_down,
        up_down,
        down,
        playerv_y,
        window_width,
        window_height,
    ):
        game_alive = True
        if left_down:

            if self.shapeX > 0:
                self.shapeX -= self.movespeed

                self.make_coordinates()
            elif self.shapeX == 0:
                self.draw_body()

            self.first_up = True
            self.first_down = True

        if right_down:

            if self.shapeX + self.shape_size < window_width:

                self.shapeX += self.movespeed

                self.make_coordinates()
            elif self.shapeX + self.shape_size == window_width:
                self.draw_body()

            self.first_up = True
            self.first_down = True

        if up_down:

            if playerv_y > 0.0:

                if self.shapeY > 0:
                    if self.first_up:
                        self.shapeY -= self.shape_size
                        self.first_up = False

                    else:
                        self.shapeY -= self.movespeed

                    self.make_coordinates()
                elif self.shapeY == 0:
                    self.draw_body()

        if down:
            if self.shapeY + self.shape_size < window_height:
                if self.first_down:
                    self.shapeY += self.shape_size
                    self.first_down = False
                else:
                    self.shapeY += self.movespeed
                self.make_coordinates()

            elif self.shapeY + self.shape_size == window_height:
                self.draw_body()
                game_alive = False

        return game_alive

    def grow(self):
        for i in range(self.growth):
            body = SnakeBody(self.shape_size, "body")
            body.rect.x = self.shapeX + self.shape_size
            body.rect.y = self.shapeY + self.shape_size
            self.body.insert((len(self.body) + 1), body)
            self.make_coordinates()

    def collision_check(self, food):
        collides = pygame.sprite.groupcollide(food, self.group, False, False)
        if collides:
            return True

        return False

    def self_collision_check(self):
        collides = pygame.sprite.spritecollideany(self.body[0], self.body_group, False)

        if collides:
            self.counter += 1
            print(f"Head_collides {self.counter}")


def main_menu(window):
    w, h = pygame.display.get_surface().get_size()
    start_game = False

    start_button = Button((w / 2) - 80, h / 4, 40, window, "Start Game")
    scores = Button((w / 2) - 80, h / 2, 40, window, "Scores")

    while start_game is False:
        window.fill((0, 0, 0))
        start_button.draw_rect()
        scores.draw_rect()
        position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            pressed = start_button.check_pos(position)
            if pressed:
                start_game = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    start_game = True
                    print("hello2")

        pygame.display.update()


def main():
    clock = pygame.time.Clock()
    pygame.init()

    window_width = 800
    window_height = 800
    shape_size = 20

    shape_x = window_width / 2
    shape_y = window_height / 2

    playerv_y = 1.0
    movespeed = 5

    left_down = False
    right_down = False
    up_down = False
    down = False

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Python Snake!")

    snake = Snake(shape_x, shape_y, shape_size, window, movespeed)

    food = Food(window, shape_size / 2)
    food_group = pygame.sprite.Group()
    food.rect.x = random.randint(0, window_height)
    food.rect.y = random.randint(0, window_width)
    food_group.add(food)

    main_menu(window)

    while True:
        window.fill((0, 0, 0))
        clock.tick(60)
        food_group.draw(window)
        collision = snake.collision_check(food_group)
        if collision:
            snake.grow()
            food.rect.x = random.randint(0, window_height)
            food.rect.y = random.randint(0, window_width)

        snake.draw_head()
        snake.first_time = False

        crash_self = snake.self_collision_check()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if right_down is not True:
                        left_down = True
                        right_down = False
                        up_down = False
                        down = False

                if event.key == pygame.K_RIGHT:
                    if left_down is not True:
                        left_down = False
                        right_down = True
                        up_down = False
                        down = False

                if event.key == pygame.K_UP:

                    if down is not True:
                        left_down = False
                        right_down = False
                        up_down = True
                        down = False

                if event.key == pygame.K_DOWN:
                    if up_down is not True:
                        left_down = False
                        right_down = False
                        up_down = False
                        down = True

                if event.key == pygame.K_SPACE:
                    move_snake = False
                    while move_snake is False:
                        snake.draw_body()
                        snake.movespeed = 0
                        pygame.draw.rect(
                            window,
                            (255, 255, 255),
                            (window_height / 2, window_width / 2, 10, 100),
                        )
                        pygame.draw.rect(
                            window,
                            (255, 255, 255),
                            (window_height / 2 + 40, window_width / 2, 10, 100),
                        )
                        pygame.display.update()
                        for pause in pygame.event.get():
                            if pause.type == pygame.KEYDOWN:
                                if pause.key == pygame.K_SPACE:

                                    move_snake = True
                                    snake.movespeed = movespeed

        game_alive = snake.move(
            left_down, right_down, up_down, down, playerv_y, window_width, window_height
        )
        if game_alive is False:
            window.fill((255, 255, 255))
        pygame.display.update()


if __name__ == "__main__":
    main()
