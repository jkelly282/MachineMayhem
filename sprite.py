import pygame, sys
import pygame.locals as GAME_GLOBALS
import typing
import random

class Food(pygame.sprite.Sprite):

    '''
    Class containing all the methods for food
    '''

    def __init__(self, surface, food_size, colour = (255,0,0)):
        super().__init__()
        self.surface = surface
        self.food = food_size
        self.image = pygame.Surface([food_size, food_size])
        self.image.fill(colour)
        self.rect = self.image.get_rect()



    def make_apple(self):

        w, h = self.surface.get_size()
        if self.food_eaten == True:
            self.x= random.randint(0,w)
            self.y = random.randint(0,h)




    def draw_food(self):
        pass



class SnakeBody(pygame.sprite.Sprite):

    def __init__(self, shape_size, name, colour = (0,255,0)):
        super().__init__()
        self.image = pygame.Surface([shape_size, shape_size])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.name = name



class Snake(pygame.sprite.Sprite):
    """
    Class containing all the methods required to make a snake
    """

    def __init__(self, starting_positionX, starting_positionY, shape_size, surface, movespeed):
        pygame.sprite.Sprite.__init__(self)
        self.shapeX = starting_positionX
        self.shapeY = starting_positionY
        self.shape_size = shape_size
        self.UI = surface
        colour = (0,255,0)
        self.movespeed =movespeed
        self.segments = 20
        self.body = []
        self.first_time = True
        self.image = pygame.Surface([shape_size, shape_size])
        self.image.fill(colour)
        self.group = pygame.sprite.Group()
        self.growth = 8
        self.body_group = pygame.sprite.Group()


    def draw_head(self):

        for i in range(self.segments):
            if self.first_time ==True:
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


    def draw_body(self)-> None:

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
        body_snake = SnakeBody(self.shape_size, "body")
        body_snake.rect.x = self.shapeX
        body_snake.rect.y = self.shapeY

        neck_snake = SnakeBody(self.shape_size, "neck")
        neck_snake.rect.x = self.shapeX
        neck_snake.rect.y = self.shapeY

        self.body.insert(0, head_snake)
        self.body[1] = neck_snake
        self.body[2] = body_snake
        self.body_group = self.body[15:]

        self.draw_body()


    def move(self, leftDown, rightDown, upDown, down, playervX, playervY, windowWidth, windowHeight):
        game_alive = True
        if leftDown:

            if self.shapeX >0:
                self.shapeX -= self.movespeed
                self.make_coordinates()
            elif self.shapeX ==0:
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

    def grow(self):
        for i in range(self.growth):
          body = SnakeBody(self.shape_size, "body")
          body.rect.x = self.shapeX + self.shape_size
          body.rect.y = self.shapeY
          self.body.append(body)
          self.make_coordinates()

    def collision_check(self, food):
        collides = pygame.sprite.groupcollide(food, self.group, False, False
                                              )
        if collides:
            return True

        return False

    def self_collision_check(self):
        collides = pygame.sprite.spritecollideany(self.body[0], self.body_group, False)
        if collides:
            print('Head_collides')



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
    food = Food(window, shape_size/2)
    group = pygame.sprite.Group()
    food.rect.x = random.randint(0,windowHeight)
    food.rect.y = random.randint(0,windowWidth)
    group.add(food)

    pygame.display.set_caption('Python Snake! ')

    while True:
        window.fill((0, 0, 0))
        snake.draw_head()
        snake.first_time = False
        clock.tick(60)
        group.draw(window)
        collision = snake.collision_check(group)
        if collision:
            snake.grow()
            food.rect.x = random.randint(0,windowHeight)
            food.rect.y = random.randint(0,windowWidth)
            group.draw(window)
        crash_self = snake.self_collision_check()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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


        game_alive = snake.move(leftDown, rightDown, upDown, down, playervX, playervY, windowWidth, windowHeight)
        if game_alive == False:
            window.fill((255,255,255))
        pygame.display.update()


main()