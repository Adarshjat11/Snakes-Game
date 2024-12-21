import pygame
import random as r 
import os

pygame.mixer.init()
pygame.init()

#Colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

#Setup display
screen_width = 800
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load('sn0.png')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
homescreen = pygame.image.load('sn1.jpg')
homescreen = pygame.transform.scale(homescreen, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snakes")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y) :
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for snake_x, snake_y in snk_list:
        pygame.draw.rect(gameWindow, red, [snake_x, snake_y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((223, 220, 229))
        gameWindow.blit(homescreen, (0, 0))
        text_screen("Welcome to Snakes", black, 210, 200)
        text_screen("Press Enter key to Play", black, 180, 250)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                exit_game = True
            
            if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        pygame.mixer.music.load('back.mp3')
                        pygame.mixer.music.play()
                        gameloop()
        
        pygame.display.update()
        clock.tick(60)
#Game Loop
def gameloop():
    #Game Specific variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    velocity_x = 0
    velocity_y = 0 

    food_x = r.randint(20, int(screen_width/2))
    food_y = r.randint(20, int(screen_height/2))
    score = 0
    init_velocity = 4
    snake_size = 20
    fps = 60
    
    snk_list = []
    snk_length = 1 

    if(not os.path.exists("Highscore.txt")) :
        with open("Highscore.txt", 'w') as hs:
         hs.write("0")
    
    with open("Highscore.txt", 'r') as hs:
     hiscore = hs.read()

    while not exit_game :
        if game_over :
            gameWindow.fill(black)
            with open("Highscore.txt", 'w') as hs:
                hs.write(str(hiscore))
            
            text_screen("Game Over! Press Enter to continue", white, 75, 225)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game = True

                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        welcome()
                        
        else :
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game = True
                    
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity 
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs (snake_x - food_x)<15 and abs (snake_y - food_y)<15 :
                score += 10
                food_x = r.randint(20, int(screen_width/2))
                food_y = r.randint(20, int(screen_height/2))
                snk_length += 5 
                if score > int(hiscore) :
                    hiscore = score

            
            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score=" + str(score) + "  High Score=" + str(hiscore), black, 1, 1)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size])
            
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1] :
                game_over = True
                pygame.mixer.music.load('explosion.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height :
                game_over = True
                pygame.mixer.music.load('explosion.mp3')
                pygame.mixer.music.play()
            
            #pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
gameloop()