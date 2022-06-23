import pygame
import random
import sys
import os
import time
from enum import Enum

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('Tanks 2D')

screen = pygame.display.set_mode((800,600))
backgroundImg = pygame.image.load("img/singleplayer/background.png")
wall_image = pygame.image.load('img/singleplayer/brick.jpg')

bonus_sound = pygame.mixer.Sound('sounds/bonus.wav')

menu_sound = pygame.mixer.Sound('sounds/menu_scroll.wav')

collision_sound = pygame.mixer.Sound('sounds/collision.wav')

shootmusic = pygame.mixer.Sound('sounds/shoot.wav')

#game_music = pygame.mixer.Sound('game.wav')
#game_music.set_volume(0.05)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def single_mode():
    class Tank:

        def __init__(self, x, y, speed, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
            self.x = x
            self.y = y
            self.speed = speed
            self.width = 31
            self.direction = Direction.RIGHT
            self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN}
            self.fire = False
            self.lives = 3
            self.points = 0

        def draw(self):
            tanke = pygame.image.load("img/singleplayer/tank2.png")
            screen.blit(tanke, (self.x, self.y))

            if self.direction == Direction.RIGHT:
                tankr2 = pygame.image.load("img/singleplayer/tank2.png")
                screen.blit(tankr2, (self.x, self.y))
            if self.direction == Direction.LEFT:
                tankl2 = pygame.image.load("img/singleplayer/tank2left.png")
                screen.blit(tankl2, (self.x, self.y))
            if self.direction == Direction.UP:
                tanku2 = pygame.image.load("img/singleplayer/tank2up.png")
                screen.blit(tanku2, (self.x, self.y))
            if self.direction == Direction.DOWN:
                tankd2 = pygame.image.load("img/singleplayer/tank2down.png")
                screen.blit(tankd2, (self.x, self.y))
            
        def changeDirection(self, direction):
            self.direction = direction

        def move(self):
            if self.direction == Direction.RIGHT:
                self.x += self.speed   
                if self.x > screen.get_size()[0]:
                    self.x = -31 
            if self.direction == Direction.LEFT:
                self.x -= self.speed
                if self.x < screen.get_size()[0] - 800-31:
                    self.x = 831
            if self.direction == Direction.UP:
                self.y -= self.speed
                if self.y < screen.get_size()[1] - 600-31:
                    self.y = 631
            if self.direction == Direction.DOWN:
                self.y += self.speed
                if self.y> screen.get_size()[1]:
                    self.y = -31

            self.draw()

        def health_check(self):
            font =pygame.font.Font('COLEMAN.otf', 30)
            pnt = font.render("Life: " + str(self.lives), True, (0, 0, 0))
            screen.blit(pnt, (20, 20))

        def point_checks(self):
            font =pygame.font.Font('COLEMAN.otf', 36)
            pnt = font.render("Score: " + str(self.points), True, (255, 255, 255))
            screen.blit(pnt, (600, 20))

    def game_over():
        gameovr_img = pygame.image.load('img/singleplayer/bcg.jpg')
        font2 = pygame.font.Font('Guilty Pleasure DEMO.otf', 56)
        pnt = font2.render("Score: " + str(tankb.points), True, (255,255,255))
        pnt2 = font2.render("Score: " + str(tankb.points), True, (255,127,39))
        txt = font2.render('to restart press "r"', True, (255,127,39))
        txt2 = font2.render('to back to the menu press"q"', True, (255,127,39))

        gameoverloop = True
        while gameoverloop:
            screen.blit(gameovr_img, (0,0))
            screen.blit(pnt, (70, 150))
            screen.blit(pnt2, (74, 150))
            screen.blit(txt, (70, 240))
            screen.blit(txt2, (70, 310))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        single_mode()
                    if event.key == pygame.K_q:
                        game.menu()
            pygame.display.update()

    bullets = []

    class Bullet:
        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.direction = direction
            self.speed = 15
            self.status = True

        def draw(self):
            if self.status:
                if self.direction == Direction.RIGHT:
                    bul_r = pygame.image.load('img/singleplayer/bullet.png')
                    screen.blit(bul_r, (int(self.x-10), int(self.y-1)))
                if self.direction == Direction.LEFT:
                    bul_l = pygame.image.load('img/singleplayer/bullet3.png')
                    screen.blit(bul_l, (int(self.x-10), int(self.y-1)))
                if self.direction == Direction.UP:
                    bul_u = pygame.image.load('img/singleplayer/bullet1.png')
                    screen.blit(bul_u, (int(self.x-1), int(self.y-18)))
                if self.direction == Direction.DOWN:
                    bul_d = pygame.image.load('img/singleplayer/bullet2.png')
                    screen.blit(bul_d, (int(self.x-1), int(self.y-18)))

        def above_walls(self):
            if self.x >= screen.get_size()[0]:
                self.status = False
            if self.x <= 0:
                self.status = False
            if self.y >= screen.get_size()[1]:
                self.status = False
            if self.y <= 0:
                self.status = False

        def move(self): 
            self.draw() 
            self.above_walls()
            if self.direction == Direction.RIGHT:
                self.x += self.speed
            if self.direction == Direction.LEFT:
                self.x-= self.speed
            if self.direction == Direction.UP:
                self.y-= self.speed
            if self.direction == Direction.DOWN:
                self.y+= self.speed

    class Wall(object):
    
        def __init__(self, pos):
            walls.append(self)
            self.img  =  (pos[0], pos[1])

    class Bonus():
        def __init__(self):
            self.x = random.randint(10, 764)
            self.y = random.randint(40, 664)
        
        def draw(self):
            bonus = pygame.image.load('img/singleplayer/bonus.png')
            screen.blit(bonus, (self.x, self.y))


    done = True
    tankb = Tank(400, 100, 4)
    tanks = [tankb]
    walls = []
    bonus = Bonus()

    level1 = [
"                             ",
"  W       W                  ",                   
"  W       W                  ",
"  WWWWWWWWW      WWWWWWWW    ",
"                 W      W    ",
"                 W      W    ",                                              
"                             ",
"                             ",
"       W                     ",
"       W                     ",
"    WWWWWWW                  ",
"                             ",
"                   WWWWWW    ",
"                 WWW         ",         
"                             ",
"      W         WWWWWW       ",
"   WWWWWW    WWWW            ",
"                             ",
"                             ",
    ]
    level2 = [
"                             ",
"                             ",                   
"          W        WW        ",
"  WWWWWWWWW             WW   ",
"  W                          ",
"  W                 WW       ",                                              
"  WWWWW                      ",
"                             ",
"         WWWWWWWWW           ",
"  W                          ",
"  W                          ",
"  W           WWW            ",
"  W         W      WWWWWW    ",
"  W         W    WWW         ",         
"  W         W                ",
"  WWWWW         WWWWWW       ",
"   WWWWWW    WWWW            ",
"                             ",
"                             ",
    ]
    level3 = [
"                             ",
"                    WWWWWW   ",                   
"  WWWWWWWW          W        ",
" WWWWWW  W          W        ",
"W      W W          W        ",
"W      W W          W        ",                                              
"W      W W     WWWWWW        ",
"W      W W     W             ",
"W      W W     WWWWWWWWWWWW  ",
"W      W W                   ",
"W      W W                   ",
"W      W  W W WWWWWW         ",
"W      W           W         ",
"W       WWWWWWWWWWWW         ",         
"W                            ",
" W              WWWWWWW W WWW",
"   WWWWWW    WWWW            ",
"                             ",
"                             ",
    ]
    level4 = [
"                             ",
"                             ",                   
"      WWWWWWWWWWWWW          ",
"     W             WWWW      ",
"   WW                  WW    ",
"  W                      W   ",                                              
"  W                       W  ",
"   W                       W ",
"   W                         ",
"    W       WWWWWWWW         ",
"     W                 W     ",
"     W                W W    ",
"    W             WWWW   WWWW",
"    W             W        W ",         
"   WWW              W  W  W  ",
"      W            W  W W  W ",
"     WW           WWW     WWW",
"      W                      ",
"       W WWWWW  WWWWWWWWWW   ",
    ]
    level5=[
"         WWWWWWWWW           ",
"        WW        WW         ",                   
"       W            W        ",
"      W              W       ",
"     W                W      ",
"    W     WW     WW    W     ",                                              
"    W     WW     WW    W     ",
"    W                   W    ",
"    W       W    W      W    ",
"    W        WWWW       W    ",
"    W                   W    ",
"    W                   W    ",
"   W                    WWW  ",
" WW                        W ",         
"W                         W  ",
" WW        W             W   ",
"   WWWWWW  WWWWWWWWWWWWWW    ",
"          W                  ",
"                             ",        
]
    levels=[level1,level2,level3,level4, level5]
    level=levels[random.randint(0,4)]


    x,y = 0,0
    for row in level:
        for col in row:
            if col == 'W':
                Wall((x,y))
            x+=31
        y+=31
        x=0

    FPS = 30
    clock = pygame.time.Clock()
    frame_count = 0
    t = 0
    while done:
        mill = clock.tick(FPS)
        seconds = mill/1000
        total_seconds = frame_count // FPS
        minutes = total_seconds // 60
        secondss = total_seconds % 60
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    tanks[0].fire = True
                    shootmusic.play()
                    if tanks[0].direction == Direction.RIGHT:
                        bullet = Bullet((tanks[0].x + tanks[0].width), (tanks[0].y + tanks[0].width//2), tanks[0].direction)
                    
                    if tanks[0].direction == Direction.LEFT:
                        bullet = Bullet((tanks[0].x), (tanks[0].y + tanks[0].width//2), tanks[0].direction)

                    if tanks[0].direction == Direction.UP:
                        bullet = Bullet((tanks[0].x + tanks[0].width//2), (tanks[0].y), tanks[0].direction)

                    if tanks[0].direction == Direction.DOWN:
                        bullet = Bullet((tanks[0].x + tanks[0].width//2), (tanks[0].y + tanks[0].width), tanks[0].direction)
                    bullets.append(bullet)                
                    
                for tank in tanks:
                    if event.key in tank.KEY.keys():
                        tank.changeDirection(tank.KEY[event.key])

        for wall in walls:
            for tank in tanks: 
                if tankb.y in range(wall.img[1]-25, wall.img[1]+31):
                    if (wall.img[0] in range(tankb.x+25, tankb.x + 31)):
                        collision_sound.play()
                        tanks[0].lives -= 1
                        walls.remove(wall)
                        if tanks[0].lives == 0:
                            tanks[0].speed = 0
                            tanks.remove(tank)
                    if (tankb.x in range(wall.img[0]+25, wall.img[0] + 31)):
                        collision_sound.play()
                        tanks[0].lives -= 1
                        walls.remove(wall)
                        if tanks[0].lives == 0:
                            tanks[0].speed = 0
                            tanks.remove(tank)
                
                if (tankb.x in range(wall.img[0]-25, wall.img[0] + 31)):
                    if (wall.img[1] in range(tankb.y+25, tankb.y + 31)):
                        collision_sound.play()
                        tanks[0].lives -= 1
                        walls.remove(wall)
                        if tanks[0].lives == 0:
                            tanks[0].speed = 0
                            tanks.remove(tank)
                    if (tankb.y in range(wall.img[1]+25, wall.img[1]+31)):
                        collision_sound.play()
                        tanks[0].lives -= 1
                        walls.remove(wall)
                        if tanks[0].lives == 0:
                            tanks[0].speed = 0
                            tanks.remove(tank)



        for wall in walls:
            for bullet in bullets:
                if bullet.x >= wall.img[0] - 4 and bullet.x <= wall.img[0] + 32 and bullet.y>= wall.img[1]-4 and bullet.y <= wall.img[1]+32:
                    collision_sound.play()
                    bullet.status == False
                    bullets.remove(bullet)
                    walls.remove(wall)
                    tanks[0].points += 1

        for tank in tanks:
            if bonus.x>=tanks[0].x - 31 and bonus.x<=tanks[0].x + 31 and bonus.y>=tanks[0].y - 31 and bonus.y<=tanks[0].y+31:
                bonus_sound.play()
                tank.speed += 3
                t = secondss
                bonus.x = random.randint(20,750)
                bonus.y = random.randint(40,550)
                if tank.speed >= 12:
                    tank.speed == 10
            if secondss == t + 5:
                    tank.speed = 3

        for bullet in bullets:
            if bullet.x >= bonus.x-4 and bullet.x <= bonus.x + 32 and bullet.y>= bonus.y-4 and bullet.y <= bonus.y+32:
                bonus_sound.play()
                bullet.status == False
                bullets.remove(bullet)
                tank.speed += 3
                t = secondss
                bonus.x = random.randint(20,750)
                bonus.y = random.randint(40,550)
                if tank.speed >= 12:
                    tank.speed == 10
            if secondss == t + 5:
                    tank.speed = 3
        
        for wall in walls:
            if bonus.x >= wall.img[0]-20 and bonus.x<=wall.img[0]+25 and bonus.y>=wall.img[1]-20 and bonus.y<=wall.img[1]+25:
                bonus.x = random.randint(20,750)
                bonus.y = random.randint(40,550)
        


        screen.blit(backgroundImg, (0,0))
        bonus.draw()
        for bullet in bullets:
            bullet.move()
        for tank in tanks:
            tank.move()
            tanks[0].health_check()
            tanks[0].point_checks()
        for wall in walls:
            screen.blit(wall_image, (wall.img))
        if tankb.lives == 0:
            game_over()
        #if tankb.points in range(109, 111) or tankb.points in range
        pygame.display.flip()



def multi_player():
    import pika
    import uuid
    import json
    from threading import Thread
    import pygame
    import sys


    IP='34.254.177.17'
    PORT =5672
    VIRTUAL_HOST = 'dar-tanks'
    USERNAME ='dar-tanks'
    PASSWORD ='5orPLExUYnyVYZg48caMpX'


    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1100, 600))


    class TankRpcClient:
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
            auto_delete=True,
            exclusive=True 
            )
            self.callback_queue = queue.method.queue
            self.channel.queue_bind(
                exchange = 'X:routing.topic',
                queue= self.callback_queue
            )

            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.on_response,
                auto_ack=True
            )

            self.response = None
            self.corr_id = None
            self.token = None
            self.tank_id = None
            self.room_id = None

        def on_response(self, ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = json.loads(body)
                print(self.response)

        def call(self, key, message={}):
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key=key,
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id,
                ),
                body=json.dumps(message)
            )
            while self.response is None:
                self.connection.process_data_events()

        def check_server_status(self):
            self.call('tank.request.healthcheck')
            return self.response['status'] == '200'

        def obtain_token(self, room_id):
            message = {
                'roomId': room_id
            }
            self.call('tank.request.register', message)
            if 'token' in self.response:
                self.token = self.response['token']
                self.tank_id = self.response['tankId']
                self.room_id = self.response['roomId']
                return True
            return False


        def turn_tank(self, token, direction):
            message = {
                'token': token,
                'direction': direction
            }
            self.call('tank.request.turn', message)

        def fire_bullet(self, token):
            message = {
                'token' : token
            }
            self.call('tank.request.fire', message)

    class TankConsumerClient(Thread):
        def __init__(self, room_id):
            super().__init__()
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = IP,
                    port = PORT,
                    virtual_host=VIRTUAL_HOST,
                    credentials=pika.PlainCredentials(
                        username=USERNAME,
                        password=PASSWORD
                    )
                )
            )
            self.channel = self.connection.channel()
            queue = self.channel.queue_declare(queue='',
                                                auto_delete=True,
                                                exclusive=True 
                                                )
            event_listener = queue.method.queue
            self.channel.queue_bind(exchange='X:routing.topic', 
                                    queue = event_listener,
                                    routing_key='event.state.'+ room_id)

            self.channel.basic_consume(
                queue=event_listener,
                on_message_callback=self.on_response,
                auto_ack=True
            )
            self.response=None

        def on_response(self, ch, method, props, body):
            self.response = json.loads(body)
            print(self.response)

        def run(self):
            self.channel.start_consuming()

    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


    def draw_tank(x,y,direction,**kwargs):
        if direction == 'RIGHT':
            tank_right = pygame.image.load('img/multiplayer/tank_right.png')
            screen.blit(tank_right, (x,y))
        if direction == 'LEFT':
            tank_left = pygame.image.load('img/multiplayer/tank_left.png')
            screen.blit(tank_left, (x,y))
        if direction == 'UP':
            tank_up = pygame.image.load('img/multiplayer/tank_up.png')
            screen.blit(tank_up, (x,y))
        if direction == 'DOWN':
            tank_down = pygame.image.load('img/multiplayer/tank_down.png')
            screen.blit(tank_down, (x,y))

    def draw_tank_opponents(x,y,direction,**kwargs):
        if direction == 'RIGHT':
            tanksright = pygame.image.load('img/multiplayer/tanksright')
            screen.blit(tanksright, (x,y))
        if direction == 'LEFT':
            tanksleft = pygame.image.load('img/multiplayer/tanksleft.png')
            screen.blit(tanksleft, (x,y))
        if direction == 'UP':
            tanksup = pygame.image.load('img/multiplayer/tanksup.png')
            screen.blit(tanksup, (x,y))
        if direction == 'DOWN':
            tanksdown = pygame.image.load('img/multiplayer/tanksdown')
            screen.blit(tanksdown, (x,y))

    def draw_bullet(owner, x, y, width, height, direction, **kwargs):
        if direction == 'RIGHT':
            bul_right = pygame.image.load('img/singleplayer/bullet.png')
            screen.blit(bul_right, (x, y))
        if direction == 'LEFT':
            bul_left = pygame.image.load('img/singleplayer/bullet3.png')
            screen.blit(bul_left, (x, y))
        if direction == 'UP':
            bul_up = pygame.image.load('img/singleplayer/bullet1.png')
            screen.blit(bul_up, (x, y))
        if direction == 'DOWN':
            bul_down = pygame.image.load('img/singleplayer/bullet2.png')
            screen.blit(bul_down, (x, y))

    def draw_bullet1(x, y, width, height, direction):
        pygame.draw.rect(screen, (0, 0, 255),(x,y,width,height))

    def game_play():
        multi_loop = True

        sredniy_shrift = pygame.font.Font('Marlboro.ttf', 35) 
        big_shrift = pygame.font.Font('Marlboro.ttf', 45) 
        melkiy_shrift = pygame.font.Font('Marlboro.ttf', 20)

        while multi_loop:
            screen.fill((0, 0, 0))
            multi_background = pygame.image.load('img/multiplayer/bcg_multi.png')
            screen.blit(multi_background,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    multi_loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        multi_loop = False
                    if event.key == pygame.K_d:
                        client.turn_tank(client.token, RIGHT)
                    if event.key == pygame.K_a:
                        client.turn_tank(client.token, LEFT)
                    if event.key == pygame.K_w:
                        client.turn_tank(client.token, UP)
                    if event.key == pygame.K_s:
                        client.turn_tank(client.token, DOWN)
                    if event.key==pygame.K_SPACE:
                        client.fire_bullet(client.token)
                        shootmusic.play()
                
        


            try:
                remaining_time = event_client.response['remainingTime']

                text = sredniy_shrift.render('Remaining Time: {}'.format(remaining_time), True, (255, 255, 255)) 
                textRect = text.get_rect()
                textRect.center = (965, 20)
                screen.blit(text, textRect)

                text2 = sredniy_shrift.render('OPPONENTS', True, (255,255,255))
                screen.blit(text2, (840, 56))

                text3 = melkiy_shrift.render('ID:', True, (255,255,255))
                text4 = melkiy_shrift.render('score:', True, (255,255,255))
                text5 = melkiy_shrift.render('health:', True, (255,255,255))
                screen.blit(text3, (842, 95))
                screen.blit(text4, (922, 95))
                screen.blit(text5, (982, 95))

                tanks = event_client.response['gameField']['tanks'] 

                for tank in tanks:
                    if tank["id"] == client.tank_id:
                        draw_tank(**tank)
                    else:
                        draw_tank_opponents(**tank)

                for tank in tanks :
                    if tank["id"] == client.tank_id:
                        my_score = tank['score']
                        my_health = tank['health']

                bullets = event_client.response['gameField']['bullets']    
                for bullet in bullets:
                    if bullet["owner"] == client.tank_id:
                        draw_bullet(**bullet)
                    else:
                        draw_bullet1(**bullet)

                for tank in tanks :
                    if tank["id"] == client.tank_id:
                        myscore = sredniy_shrift.render("Score: {}".format(tank['score']), True, (255,255,255))
                        myhealth = sredniy_shrift.render("Health: {}".format(tank['health']), True, (255,255,255))
                        screen.blit(myscore, (851, 410))
                        screen.blit(myhealth, (851, 440))

                koordy = 115
                for tank in sorted(tanks, key = lambda x:x['score'],reverse=True):
                    if tank["id"] == client.tank_id:
                        text1 = melkiy_shrift.render('{}'.format(tank["id"])+'     {}'.format(tank["score"])+ '     {}'.format(tank["health"]), True, (236, 28, 36))
                    else:
                        text1 = melkiy_shrift.render('{}'.format(tank["id"])+'     {}'.format(tank["score"])+ '     {}'.format(tank["health"]), True, (253, 136, 166))
                    screen.blit(text1, (842, koordy))
                    koordy+=20

                winners = event_client.response['winners']
                for winner in winners:
                    if winner['id'] == client.tank_id:
                        multi_loop = False
                losers = event_client.response['losers']
                for loser in losers:
                    if loser['id'] == client.tank_id:
                        multi_loop = False
                kickeds = event_client.response['kicked']
                for kickeds in kicked:
                    if kickeds['id'] == client.tank_id:
                        multi_loop = False

            except:
                pass 
                



            pygame.display.flip()
        client.connection.close()
        pygame.quit()   


    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-1')
    player_id = client.tank_id
    event_client = TankConsumerClient('room-1')
    event_client.start()
    game_play()    






class Menu:
    def __init__(self, punkts = [120, 250, u'Punkt', (250,250,30), (250,30,250), 0]):
        self.punkts = punkts

    def to_Display(self, poverhnost, font, punkt_n):
        for i in self.punkts:
            if punkt_n == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        menu_bcg = pygame.image.load('img/menu.jpg')
        done = True
        font_menu = pygame.font.Font('COLEMAN.otf', 50)
        punkt = 0

        while done:

            screen.blit(menu_bcg, (0,0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+ 50:
                    punkt = i[5]
            self.to_Display(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt>0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        menu_sound.play()
                        play_mode.menu()
                    elif punkt == 1:
                        menu_sound.play()
                        sys.exit()

                pygame.display.flip()

punkts = [(120, 250, u'Play', (24,60,32), (0,0,0), 0),
          (120, 320, u'Quit', (24,60,32), (0,0,0), 1)]

class Play_modes:
    def __init__(self, punkts = [120, 150, u'Punkt', (250,250,30), (250,30,250), 0]):
        self.punkts = punkts

    def to_Display(self, poverhnost, font, punkt_n):
        for i in self.punkts:
            if punkt_n == i[5]:
                menu_sound.play
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
    
    def menu(self):
        menu_bcg = pygame.image.load('img/menu_img.jpg')
        done = True
        font_menu = pygame.font.Font('COLEMAN.otf', 60)
        punkt = 0

        while done:

            screen.blit(menu_bcg, (0,0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+250 and mp[1]>i[1] and mp[1]<i[1]+ 60:
                    punkt = i[5]
            self.to_Display(screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if punkt>0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        menu_sound.play()
                        single_mode()
                    elif punkt == 1:
                        menu_sound.play()
                        multi_player()
                    elif punkt == 2:
                        menu_sound.play()
                        sys.exit()
                    elif punkt == 3:
                        menu_sound.play()
                        sys.exit()

                pygame.display.flip()

rezhimy = [(100, 160, u'SINGLE MODE', (24,60,32), (0,0,0), 0),
          (100, 240, u'MULTI PLAYER MODE', (24,60,32), (0,0,0), 1),
          (100, 320, u'AI MODE', (24,60,32), (0,0,0), 2),
          (100, 400, u'QUIT', (24,60,32), (0,0,0), 3)]
    



play_mode = Play_modes(rezhimy)
game = Menu(punkts)
game.menu()
pygame.quit()