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


class Button():
    def __init__(self, positionX, positionY, shape_size, surface, text, colour = (0,0,255)):

        self.positionX = positionX
        self.positionY = positionY
        self.shape_size = shape_size
        self.UI = surface
        self.button_text = text
        self.colour = colour
        self.font = pygame.font.SysFont(None, 24)


    def draw_rect(self):
        pygame.draw.rect(self.UI,self.colour,(self.positionX,self.positionY, self.shape_size *4, self.shape_size))
        self.UI.blit(self.font.render(self.button_text, True, (255,0,0)), (self.positionX, self.positionY))

    def check_pos(self, position):
        if position[0] > self.positionX and position[0] < self.positionX + self.shape_size:
            print('HODHFOI')
            return True


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
        self.last_time =0
        self.first_up = False
        self.first_down = False




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
        self.body.insert(0, head_snake)
        self.body_group = self.body[20:]
        self.draw_body()


    def move(self, leftDown, rightDown, upDown, down, playervX, playervY, windowWidth, windowHeight):
        game_alive = True
        if leftDown:


            if self.shapeX >0:
                self.shapeX -= self.movespeed

                self.make_coordinates()
            elif self.shapeX ==0:
                self.draw_body()

            self.first_up = True
            self.first_down = True

        if rightDown:


            if self.shapeX + self.shape_size < windowWidth:

                self.shapeX += self.movespeed


                self.make_coordinates()
            elif self.shapeX + self.shape_size == windowWidth:
                self.draw_body()

            self.first_up = True
            self.first_down = True

        if upDown:

            if playervY > 0.0:
                playervY = self.movespeed
                playervY = -playervY
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

            if playervY < 0.0:
                playervY = self.movespeed

            if self.shapeY + self.shape_size < windowHeight:
                if self.first_down:
                    self.shapeY += self.shape_size
                    self.first_down = False
                else:
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
          body.rect.y = self.shapeY + self.shape_size
          self.body.insert((len(self.body)+1),body)
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
            self.counter += 1
            print(f'Head_collides {self.counter}')


def main_menu(window):
    w, h = pygame.display.get_surface().get_size()
    start_game = False

    start_button = Button((w/2)-80,h/4,40,window,'Start Game')
    scores = Button((w/2)-80, h/2, 40, window, 'Scores')



    while start_game == False:
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
                print('hello2')

        pygame.display.update()






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
    button = Button(windowHeight/2,windowWidth/2,20,window, 'hellp')
    snake = Snake(shapeX, shapeY, shape_size, window, movespeed)
    food = Food(window, shape_size/2)
    group = pygame.sprite.Group()
    food.rect.x = random.randint(0,windowHeight)
    food.rect.y = random.randint(0,windowWidth)
    group.add(food)
    moving_snake = False
    BLUE = (0,0,255)
    #font = pygame.font.SysFont(None, 240, italic=True)
    #img = font.render('Python \n Snake ', True, BLUE)
    main_menu(window)


    pygame.display.set_caption('Python Snake! ')

    while True:
        window.fill((0, 0, 0))


        clock.tick(60)
        group.draw(window)

        collision = snake.collision_check(group)
        if collision:
            snake.grow()
            food.rect.x = random.randint(0,windowHeight)
            food.rect.y = random.randint(0,windowWidth)


        snake.draw_head()
        snake.first_time = False


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

                  if event.key == pygame.K_SPACE:
                      move_snake = False
                      while move_snake == False:
                          snake.draw_body()
                          snake.movespeed = 0
                          pygame.draw.rect(window, (255,255,255), (windowHeight/2, windowWidth/2, 10,100) )
                          pygame.draw.rect(window, (255,255,255), (windowHeight/2 + 40, windowWidth/2, 10,100) )
                          pygame.display.update()
                          for event in pygame.event.get():
                              if event.type == pygame.KEYDOWN:
                                  if event.key == pygame.K_SPACE:
                                    move_snake = True
                                    snake.movespeed = movespeed




                  else:

                    moving_snake = False




        game_alive = snake.move(leftDown, rightDown, upDown, down, playervX, playervY, windowWidth, windowHeight)
        if game_alive == False:
            window.fill((255,255,255))
        pygame.display.update()


main()