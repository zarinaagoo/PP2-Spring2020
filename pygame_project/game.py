import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800,600))
backgroundImg = pygame.image.load("background1.png")
yourscore = 0
scoretxt = pygame.font.SysFont("times new roman", 25)
yourlife = 3
lifetxt = pygame.font.SysFont("times new roman", 18)
gameOvertxt = pygame.font.SysFont("times new roman", 35)
gameOverstr = gameOvertxt.render("Game Over, You Lose!", 40, (0,0,0))

playerImg = pygame.image.load("basket.png")
player_x = 20
player_y = 440
def player(x,y):
    screen.blit(playerImg, (x,y))

main_object = pygame.image.load("apple.png")
main_x = random.randint(0, 720)
main_y = 0
mdy = 4
def mainobject(x, y):
    screen.blit(main_object, (x,y))

main_obj2 = pygame.image.load("bittenapple.png")
main2_x = random.randint(0,720)
main2_y = 0
m2dy = 4
def mainobj2(x,y):
    screen.blit(main_obj2, (x,y))
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT]:
        player_x += 6
    if pressed[pygame.K_LEFT]:
        player_x -=6
    main_y += mdy
    if main_y > player_y and main_y < player_y + 75 and main_x > player_x and main_x < player_x+75:
        main_y = 0
        main_x = random.randint(0, player_x + 200)
        yourscore += 1
    if main_y>440 and main_y<590 and (main_x < player_x or main_x > player_x+150):
        main_y = 0
        main_x = random.randint(0, player_x + 200)

    main2_y += m2dy 
    if main2_y>460 and (main2_x < player_x or main2_x > player_x+150):
        main2_y = 0
        main2_x = random.randint(0, 660)
    if main2_y > player_y and main2_y < player_y + 75 and main2_x > player_x and main2_x < player_x+75:
        main2_y = 0
        main2_x = random.randint(0, 660)
        yourlife -= 1

    score = scoretxt.render("score:" + str(yourscore), 0, (0,0,0))
    life = lifetxt.render("lives:" + str(yourlife), 28, (0,0,0))
    gamescore = gameOvertxt.render("SCORE: "+ str(yourscore), 200, (0,0,0))
    
    def lifeov(count):
        if count == 0:
            pygame.draw.rect(screen, (80, 200, 120), pygame.Rect(0, 0, 800, 600))
            screen.blit(gameOverstr,(200,200))
            screen.blit(gamescore, (265,250))

    screen.blit(backgroundImg, (0,0))
    mainobject(main_x, main_y)
    mainobj2(main2_x, main2_y)
    screen.blit(score, (0,0))
    screen.blit(life, (0,28))
    player(player_x,player_y)
    lifeov(yourlife)
    pygame.display.flip()