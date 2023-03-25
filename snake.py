import pygame, sys, random
from pygame.math import Vector2

class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number-1) 
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load("Graphics/apple.png").convert_alpha()
    def draw_fruit(self):
        # create a rectangle
        fruit_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y * cell_size, cell_size,cell_size)
        # draw the rectangle 
        #pygame.draw.ellipse(screen, (0,255,0),fruit_rect)
        screen.blit(self.apple,fruit_rect)

    def reposition_fruit(self):
        self.x = random.randint(0, cell_number-1) 
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)
        
class Snake:
    def __init__(self):
        self.direction = Vector2(1,0)
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        for index,block in enumerate(self.body):
            # get the position
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size

            # create rect
            snake_block = pygame.Rect(x_pos,y_pos,cell_size, cell_size)
            # draw block
            if index == 0 :
                snake_head = self.draw_head()
                #pygame.draw.rect(screen, (255,0,0),snake_block)
                screen.blit(snake_head, snake_block)
            elif index == len(self.body) - 1:
                snake_tail = self.draw_tail()
                screen.blit(snake_tail, snake_block)
            else:
                snake_body = self.draw_body(block,index)
                screen.blit(snake_body, snake_block)

    def move_snake(self):
        if self.new_block == True:
            body = self.body[:]
            self.new_block = False
        else:
            body = self.body[:-1]
        body.insert(0,body[0] + self.direction)
        self.body = body[:]

    def draw_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            return self.head_left
        elif head_relation == Vector2(-1,0):
            return self.head_right
        elif head_relation == Vector2(0,1):
            return self.head_up
        elif head_relation == Vector2(0,-1):
            return self.head_down
        
    def draw_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            return self.tail_left
        elif tail_relation == Vector2(-1,0): 
            return self.tail_right
        elif tail_relation == Vector2(0,1): 
            return self.tail_up
        elif tail_relation == Vector2(0,-1): 
            return self.tail_down

    def draw_body(self,block,block_index):
        previous_block = self.body[block_index + 1] - block
        next_block = self.body[block_index - 1] - block
        if previous_block.x == next_block.x:
            return self.body_vertical
        elif previous_block.y == next_block.y:
            return self.body_horizontal
        else:
            if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                return self.body_tl
            elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                return self.body_bl
            elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                return self.body_tr
            elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                return self.body_br

    def add_block(self):
        self.new_block = True

    def play_crunsh_sound(self):
        self.crunch_sound.play()

    def reset(self):
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
            self.direction = Vector2(0,0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update_game(self):
        self.snake.move_snake()
        self.check_fail()
        self.eat_fruit()

    def eat_fruit(self):
        if self.snake.body[0] == self.fruit.pos :
            print("snake")
            # add new block to the snake
            self.snake.add_block()
            # reposition the fruit
            self.fruit.reposition_fruit()
            # play crunsh sound
            self.snake.play_crunsh_sound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.reposition_fruit()

    def draw_all(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_fail(self):
        # if the snake hit the wall
        if self.snake.body[0].x < 0  or self.snake.body[0].x >= cell_number or self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number:
            print("wall")
            self.game_over()

        # if the snake hit him self
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print("body")
                self.game_over()
    
    def game_over(self):
        self.snake.reset()

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_surface = font.render(score,True,(26,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(self.fruit.apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)
        screen.blit(score_surface,score_rect)

        
pygame.init()
pygame.display.set_caption('Snake Game')

# game parameters
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number,cell_size * cell_number))
font = pygame.font.Font("Font/PoetsenOne-Regular.ttf",25)

# update the screen each 150ms
# each 150ms update screen event fired up
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

game = Game()

# start the game
while True:
    # loop trough all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update_game()
        # handle user input's
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1,0)
    # draw all our elements
    screen.fill((175,215,70))
    game.draw_all()
    
    pygame.display.update()