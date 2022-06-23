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

collision_sound = pygame.mixer.Sound('sounds/collision.wav')
collision_sound.set_volume(0.3)

shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
shoot_sound.set_volume(0.3)


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

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_d: RIGHT
}


def draw_tank(x, y, width, height, direction,health):
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
def draw_tank_opponents(x, y, width, height, direction,health):
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

    if owner == player_id:
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
    
    else:
        pygame.draw.rect(screen, (0, 0, 255),(x,y,width,height))
def game_isOver:
    gmvr = pygame.image.load('menuu.jpg')
    font = 
    result 
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
                    shoot_sound.play()
                
       


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

            hits = event_client.response['hits']
            winners = event_client.response['winners']
            losers = event_client.response['losers']
            kickeds = event_client.response['kicked']


            for winner in winners:
                if winner['id'] == client.tank_id:
                    multi_loop = False
            for loser in losers:
                if loser['id'] == client.tank_id:
                    multi_loop = False

            tanks = event_client.response['gameField']['tanks'] 

            for tank in tanks :
                if tank["id"] == client.tank_id:
                    my_score = tank['score']
                    my_hp = tank['health']

            for tank in tanks:
                if tank["id"] == client.tank_id:
                    tank_x = tank['x']
                    tank_y = tank['y']
                    tank_width = tank['width']
                    tank_height = tank['height']
                    tank_direction = tank['direction']
                    tank_health = tank['health']
                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction, tank_health)
                else:
                    tank1_x = tank['x']
                    tank1_y = tank['y']
                    tank1_width = tank['width']
                    tank1_height = tank['height']
                    tank1_direction = tank['direction']
                    tank1_health = tank['health']
                    draw_tank_opponents(tank1_x,tank1_y, tank1_width, tank1_height, tank1_direction, tank1_health)

            bullets = event_client.response['gameField']['bullets']    
            for bullet in bullets:
                draw_bullet(**bullet) 

            for tank in tanks :
                if tank["id"] == client.tank_id:
                    myscore = sredniy_shrift.render("Score: {}".format(tank['score']), True, (255,255,255))
                    myhealth = sredniy_shrift.render("Health: {}".format(tank['health']), True, (255,255,255))
                    screen.blit(myscore, (851, 410))
                    screen.blit(myhealth, (851, 440))

            koordy = 115
            for tank in sorted(tanks, key = lambda x:x['score'],reverse=True):
                if tank["id"] == client.tank_id:
                    text1 = melkiy_shrift.render('{}'.format(tank["id"])+'     {}'.format(tank["score"])+ '     {}'.format(tank["health"]), True, (255, 255, 0))
                else:
                    text1 = melkiy_shrift.render('{}'.format(tank["id"])+'     {}'.format(tank["score"])+ '     {}'.format(tank["health"]), True, (255, 255, 255))
                screen.blit(text1, (842, koordy))
                koordy+=20

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