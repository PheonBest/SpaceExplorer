import pygame, sys
from pygame.locals import *
import os;
import random;
import math;
import threading
import time;

#Set up pygame
pygame.init()
w = 1920
h = 1080
#Set up the window
windowSurface = pygame.display.set_mode((w, h), FULLSCREEN)
pygame.display.set_caption('Space Explorer')

myfont1 = pygame.font.SysFont("monospace", 30, True)
myfont2 = pygame.font.Font(os.path.join('pixelart.ttf'), 30)
myfont3 = pygame.font.Font(os.path.join('pixelart.ttf'), 22)
myfont4 = pygame.font.SysFont("monospace", 26, True)

score=0

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

basicFont = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()

windowSurface.fill(BLACK)

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return qx, qy;

def set_timeout(func, sec):
    global t;
    t.cancel();
    def func_wrapper():
        func()
        t.cancel()
    t = threading.Timer(sec, func_wrapper)
    t.start()

t = threading.Timer(1, set_timeout);
def returnEdgeDist():
    center = [w/2, h/2];
    dist_to_CENTER = [math.fabs(ship.x - center[0]), math.fabs(ship.y - center[1])];
    return  dist_to_CENTER;

def rot_center(image, angle):
    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def calculate_new_x(old_x,speed,angle_in_radians):
    new_x = old_x + (speed*math.cos(angle_in_radians))
    return new_x

def calculate_new_y(old_y,speed,angle_in_radians):
    new_y = old_y + (speed*math.sin(angle_in_radians))
    return new_y

def d6r(d):
    """Convert degrees into radians."""
    return math.radians(d)

fileNumber_total=0
for file_name in os.listdir('images'):
    for file_name in os.listdir('images/'+str(file_name)):
        fileNumber_total+=1
for file_name in os.listdir('planets'):
    for file_name in os.listdir('planets/'+str(file_name)):
        fileNumber_total+=1

def progress(count, total, status, name):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    pygame.display.update()
    windowSurface.fill(BLACK)
    PROGRESS = myfont4.render('[%s] %s%s ...%s/r' + str(bar), 1, GREEN)
    windowSurface.blit(PROGRESS, (PROGRESS.get_rect(center=(w/2, h/2))))
    DETAILS = myfont1.render(str(percents) + ' %  ' + str(status) + ' ' + str(name), 1, WHITE)
    windowSurface.blit(DETAILS, (DETAILS.get_rect(center=(w/2, h/2+h/37))))

current = 0
def currentUpdate():
    global current;
    current+=1;
images = []
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
images.append([])
fileNumber_expl=-1
for file_name in os.listdir('images'):
    sub1=file_name
    images.append([])
    fileNumber_expl+=1
    i=0
    for file_name in os.listdir('images/'+str(file_name)):
        fileN = str(file_name)
        image = pygame.image.load('images/' + sub1 + '/' + str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1]).convert()
        images[int(sub1)].append(image)
        i+=1
        currentUpdate()
        progress(current, fileNumber_total, image, str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1])
        #time.sleep(0.000001)

planets_images = []
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
planets_images.append([])
fileNumber_plan=-1
for file_name in os.listdir('planets'):
    sub1=file_name
    fileNumber_plan+=1
    planets_images.append([])
    i=0
    for file_name in os.listdir('planets/'+str(file_name)):
        fileN = str(file_name)
        image = pygame.image.load('planets/' + sub1 + '/' + str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1]).convert()
        planets_images[int(sub1)].append(image)
        i+=1
        currentUpdate()
        progress(current, fileNumber_total, image, str(i) + '.' + fileN[len(fileN)-3] + fileN[len(fileN)-2] + fileN[len(fileN)-1])
        #time.sleep(0.000001)

class Explosion:
    def __init__(self, x, y, size):
        global fileNumber;
        self.size = size
        self.frame = 0
        self.list = images[random.randint(0,fileNumber_expl)]
        self.image = pygame.transform.scale(self.list[self.frame], (self.size*2, self.size*2))
        self.x = x
        self.y = y
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20
    def update(self):
        now = pygame.time.get_ticks()
        windowSurface.blit(self.image,(self.x,self.y));
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if (self.frame != len(self.list)):
                self.frame += 1
            if self.frame != len(self.list):
                self.image = pygame.transform.scale(self.list[self.frame], (self.size*2, self.size*2))

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x+31
        self.y = y+31
        self.angle = angle
        self.speed = speed
        self.lifetime = 0
    def show(self):
        self.lifetime += 1;
        pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)), 4, 0);
    def refreshPos(self):
        self.x += (self.x - calculate_new_x(self.x, self.speed, d6r(-(self.angle-90))));
        self.y += (self.y - calculate_new_y(self.y, self.speed, d6r(-(self.angle-90))));

class Ship:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.angle = 0;
        self.speed= 0;
        self.vel = 0.1;
        self.img = pygame.image.load('ship.png');
        self.dirX = 0;
        self.dirY = 0;
        self.last_used = pygame.time.get_ticks()
        self.cooldown = 200
        self.maxSpeed = 12;
        self.rotate = False;
        self.altitude = 0;
    def show(self):
        windowSurface.blit(rot_center(self.img, self.angle),(self.x,self.y));
    def move(self):
        if (self.rotate and self.angle < 360 and self.speed > 0):
            self.angle+= 5;
            self.speed -= 1;
        else :
            self.rotate = False;
        if (self.angle > 360):
            self.angle = 0;
        if (self.angle < 0):
            self.angle = 360;
        for i in range(len(asteroids)):
            self.dirX = (self.x - calculate_new_x(self.x, self.speed, d6r(-(self.angle + 90))));
            self.dirY = (self.y - calculate_new_y(self.y, self.speed, d6r(-(self.angle + 90))));
            asteroids[i].x += self.dirX;
            asteroids[i].y += self.dirY;
        for i in range(len(explosions)):
            explosions[i].x += self.dirX;
            explosions[i].y += self.dirY;
        for i in range(len(planets)):
            planets[i].x += self.dirX;
            planets[i].y += self.dirY;
        for i in range(len(stars)):
            stars[i].x += ((self.dirX * stars[i].z)/2000)*30;
            stars[i].y += ((self.dirY * stars[i].z)/2000)*30;
        for i in range(len(ground.posX)):
            ground.posX[i] += self.dirX;
            ground.posY[i] += self.dirY;
        self.altitude = int(ground.posY[0]-h/2-70);
        global score;
        score=score+0.1*self.speed
        if (pressed_up and self.speed <= self.maxSpeed):
            self.speed += 0.1;
        if (not pressed_up and self.speed >= 0.1):
            self.speed -= 0.1;
        if (not pressed_down and self.speed <= 0.1):
            self.speed += 0.1;
        if (pressed_down and self.speed >= -5):
            self.speed -= 0.1;
        if (pressed_left):
            self.angle += 4;
        if (pressed_right):
            self.angle -= 4;
    def returnDir(self):
        self.dir = "";
        if (self.dirX <= self.maxSpeed/2 and self.dirX >= -self.maxSpeed/2 and self.dirY > 0):
            self.dir = "up";
        elif (self.dirX <= self.maxSpeed/2 and self.dirX >= -self.maxSpeed/2 and self.dirY < 0):
            self.dir = "down";
        elif (self.dirX <= self.maxSpeed+1 and self.dirX >= -self.maxSpeed/2 and self.dirY <= self.maxSpeed/2 and self.dirY >= -self.maxSpeed/2):
            self.dir = "left";
        elif (self.dirX >= -self.maxSpeed-1 and self.dirX <= -self.maxSpeed/2 and self.dirY <= self.maxSpeed/2 and self.dirY >= -self.maxSpeed/2):
            self.dir = "right";
        return self.dir;
    def shoot(self):
        if (pressed_bar):
            now = pygame.time.get_ticks()
            if (now - self.last_used >= self.cooldown):
                self.last_used = now
                bullets.append(Bullet(self.x, self.y, self.angle, 20));
    def notControlable(self, intensity):
        self.dirX = -intensity*self.dirX
        self.dirY = -intensity*self.dirY;
    def rotateSetTo(self, boole):
        self.rotate = boole;

asteroids_name = ["1 Ceres", "4 Vesta", "2 Pallas", "10 Hygiea", "704 Interamnia", "52 Europa", "511 Davida",
"65 Cybele", "15 Eunomia", "3 Juno", "31 Euphrosyne", "624 Hektor", "88 Thisbe", "324 Bamberga", "451 Patienta",
"532 Herculina", "48 Doris", "375 Ursula", "107 Camilla", "45 Eugenia", "7 Iris", "29 Amphirite", "423 Diotima",
"19 Fortuna", "13 Egeria", "24 Themis", "94 Aurora", "702, Alauda", "121 Hermione", "Aletheia", "372 Palma", "128 Nemenios"]

class Asteroid:
    def __init__(self, x, y, size):
        self.x = x;
        self.y = y;
        self.spawnX = x;
        self.spawnY = y;
        self.size = size;
        self.maxlife = int(size/20)
        self.life = self.maxlife
        self.dist = 1;
        # generation des variables aleatoires
        self.nbrRandom = [];
        for i in range(16):
            self.nbrRandom.append(random.randint(0, size))

        self.refreshPos();
        if (random.randint(0, 10) <= 8):
            self.color = WHITE
        else:
            self.color = RED
        # chaque asteroide est en mouvement dance l'espace, on genere les directions
        self.moveDir = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.name = asteroids_name[random.randint(0, len(asteroids_name)-1)]
    def refreshPos(self):
        # generation de la forme de base de l'hexagon
        self.v1 = [self.x            , self.y];
        self.v2 = [self.x+self.size  , self.y-self.size];
        self.v3 = [self.x+self.size*2, self.y-self.size];
        self.v4 = [self.x+self.size*3, self.y];
        self.v5 = [self.x+self.size*3, self.y+self.size];
        self.v6 = [self.x+self.size*2, self.y+self.size*2];
        self.v7 = [self.x+self.size  , self.y+self.size*2];
        self.v8 = [self.x            , self.y+self.size];

        # on ajoute nos valeurs aleatoires
        self.v1[0] += self.nbrRandom[0];
        self.v1[1] += self.nbrRandom[1];

        self.v2[0] += self.nbrRandom[2];
        self.v2[1] += self.nbrRandom[3];

        self.v3[0] += self.nbrRandom[4];
        self.v3[1] += self.nbrRandom[5];

        self.v4[0] += self.nbrRandom[6];
        self.v4[1] += self.nbrRandom[7];

        self.v5[0] += self.nbrRandom[8];
        self.v5[1] += self.nbrRandom[9];

        self.v6[0] += self.nbrRandom[10];
        self.v6[1] += self.nbrRandom[11];

        self.v7[0] += self.nbrRandom[12];
        self.v7[1] += self.nbrRandom[13];

        self.v8[0] += self.nbrRandom[14];
        self.v8[1] += self.nbrRandom[15];
    def show(self):
        self.bestY = self.v1[1];
        if (self.v2[1] < self.bestY):
            self.bestY = self.v2[1];
        if (self.v3[1] < self.bestY):
            self.bestY = self.v3[1];
        if (self.v4[1] < self.bestY):
            self.bestY = self.v4[1];

        self.mostInRight = self.v3[0];
        if (self.v4[0] > self.mostInRight):
            self.mostInRight = self.v4[0];
        if (self.v5[0] > self.mostInRight):
            self.mostInRight = self.v5[0];
        if (self.v6[0] > self.mostInRight):
            self.mostInRight = self.v6[0];

        self.mostInLeft = self.v2[0];
        if (self.v1[0] < self.mostInLeft):
            self.mostInLeft = self.v1[0];
        if (self.v8[0] < self.mostInLeft):
            self.mostInLeft = self.v8[0];
        if (self.v7[0] < self.mostInLeft):
            self.mostInLeft = self.v7[0];

        self.toDisplay=False
        if (self.v1[0]>0 and self.v1[0]<w and self.v6[1]>0 and self.v1[1]<h):
            self.toDisplay=True
        elif (self.v6[0]>0 and self.v6[0]<w and self.v6[1]>0 and self.v6[1]<h):
            self.toDisplay=True
        elif (self.v3[0]>0 and self.v3[0]<w and self.v3[1]>0 and self.v3[1]<h):
            self.toDisplay=True
        elif (self.v4[0]>0 and self.v4[0]<w and self.v4[1]>0 and self.v4[1]<h):
            self.toDisplay=True
        elif (self.v5[0]>0 and self.v5[0]<w and self.v5[1]>0 and self.v5[1]<h):
            self.toDisplay=True
        elif (self.v6[0]>0 and self.v6[0]<w and self.v6[1]>0 and self.v6[1]<h):
            self.toDisplay=True
        elif (self.v7[0]>0 and self.v7[0]<w and self.v7[1]>0 and self.v7[1]<h):
            self.toDisplay=True
        elif (self.v8[0]>0 and self.v8[0]<w and self.v8[1]>0 and self.v8[1]<h):
            self.toDisplay=True
        if (self.toDisplay):
            self.toDisplay=False

            pygame.draw.polygon(windowSurface, self.color, [self.v1, self.v2, self.v3, self.v4, self.v5, self.v6, self.v7, self.v8], 4)
            if (self.size > 100):
                NAME = myfont3.render(self.name, 1, (255, 255, 0))
                windowSurface.blit(NAME, (self.mostInRight, (self.y+self.size)))

                SIZE = myfont3.render("SIZE  " + str(self.size), 1, (255, 255, 0))
                windowSurface.blit(SIZE, (self.mostInRight, (self.y+self.size+self.size/4)))
        #pygame.draw.line(windowSurface, (255, 255, 255), (self.spawnX, self.spawnY), ((self.x, self.y )))
    def move(self):
        if (self.color == WHITE):
            self.x += (self.moveDir[0] * 100)/((self.size)*1);
            self.y += (self.moveDir[1] * 100)/((self.size)*1);
        else :
            self.x += (self.moveDir[0] * 100) / ((self.size) * 30);
            self.y += (self.moveDir[1] * 100) / ((self.size) * 30);
            # Différence des x et différence des y
            dx, dy = self.x - ship.x, self.y - ship.y
            # On cherche l'hypoténuse du triangle formé par dx et dy
            self.dist = math.hypot(dx, dy)

            dx, dy = dx / self.dist, dy / self.dist
            # move along this normalized vector towards the player at current speed
            self.x += -200 * (dx / self.size)
            self.y += -200 * (dy / self.size)
    def health(self):
        if (self.maxlife > 1):
            health = (self.life * self.size / self.maxlife)
            pygame.draw.rect(windowSurface, GREEN, (self.mostInLeft, self.bestY, health*(self.mostInRight-self.mostInLeft)/70,  self.size/3))

class Planet:
    def __init__(self, x, y, size):
        global fileNumber_plan;
        self.size = size
        self.list = planets_images[random.randint(0,fileNumber_plan)]
        self.image = self.list[0]
        img_size = self.image.get_size()
        self.size_X = int(img_size[0]*(self.size/img_size[0]))
        self.size_Y = int(img_size[1]*(self.size/img_size[0]))
        self.image = self.image= pygame.transform.scale(self.image, (self.size_X, self.size_Y))
        self.x = x
        self.y = y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20
    def update(self):
        now = pygame.time.get_ticks()
        # Différence des x et différence des y
        dx, dy = (self.x)*2 - ship.x, (self.y)*2 - ship.y
        # On cherche l'hypoténuse du triangle formé par dx et dy
        self.dist = math.hypot(dx, dy)
        dx, dy = dx / self.dist, dy / self.dist
        # move along this normalized vector towards the player at current speed
        self.x += -100 * (dx/1000  )
        self.y += -100 * (dy/1000  )
        if (self.x>0-self.size and self.x<w+self.size and self.y>0-self.size and self.y<h+self.size):
            windowSurface.blit(self.image,(self.x,self.y));
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                if (self.frame == len(self.list)-1):
                    self.frame = 0
                else:
                    self.frame += 1
                self.image= pygame.transform.scale(self.list[self.frame], (self.size_X, self.size_Y))
class Star:
    def __init__(self, x, y, z):
        self.x = x;
        self.y = y;
        self.z = z;
    def show(self):
        if (self.z > 0):
            pygame.draw.circle(windowSurface, WHITE, (int(self.x), int(self.y)),int(self.z/100));

def map(n, start1, stop1, start2, stop2):
    newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2;
    if (start2 < stop2):
        return max(min(newval, stop2), start2)
        #return this.constrain(newval, start2, stop2);
    else:
        return max(min(newval, start2), stop2)
        #return this.constrain(newval, stop2, start2);
class Minimap:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
        self.size = 200;
        self.zoomW = render_distance[0]
        self.zoomH = render_distance[1]
    def show(self):
        pygame.draw.rect(windowSurface, [255, 255, 255], (self.x, self.y, self.size, self.size), 12);
        windowSurface.fill(BLACK, rect=[self.x, self.y,  self.size,  self.size])

        pX = self.size/2
        pY = pX

        pygame.draw.circle(windowSurface, BLUE, (int(pX), int(pY)), 5)

        for i in range(len(asteroids)):
            if (asteroids[i].y > -self.zoomH and asteroids[i].y < self.zoomH):
                if (asteroids[i].x < self.zoomW or asteroids[i].x > -self.zoomW):
                    x = map(asteroids[i].x, -self.zoomW, self.zoomW, 0, self.size);
                    y = map(asteroids[i].y, -self.zoomH, self.zoomH, 0, self.size);
                    size = map(asteroids[i].size, 0, max_ast_size, 1, 6);
                    pygame.draw.circle(windowSurface, asteroids[i].color, (int(x*3.32/3.425), int(y*3.32/3.425)), int(size));
        for i in range(len(planets)):
            if (planets[i].y > -self.zoomH and planets[i].y < self.zoomH):
                if (planets[i].x < self.zoomW or planets[i].x > -self.zoomW):
                    x = map(planets[i].x, -self.zoomW, self.zoomW, 0, self.size);
                    y = map(planets[i].y, -self.zoomH, self.zoomH, 0, self.size);
                    size = map(planets[i].size, 0, max_ast_size, 1, 6);
                    pygame.draw.circle(windowSurface, GREEN, (int(x*3.32/3.425), int(y*3.32/3.425)), int(size));

class Ground:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

        self.posX = [];
        self.posY = [];

        for i in range(1000):
            self.posX.append(10*i);
            self.posY.append(5*h/6+random.randint(-5, 5))

    def show(self):
        for i in range(len(self.posX)):
            if (self.posX[i] > w):
                self.posX[i] = 0
            elif (self.posX[i] < 0):
                self.posX[i] = w;
        if self.posY[0]-75<=h:
            if self.posY[0]-70<= h/2:
                ship.speed = -1*ship.speed;
            try:
                for i in range(len(self.posX)):
                    pygame.draw.circle(windowSurface, (255, 255, 255), (int(self.posX[i]), int(self.posY[i])), 3)
            except:
                pass;
        # pygame.draw.polygon(windowSurface, [255, 255, 255], [[0, h], [w/2, h-100], [w, h]], 5)

stars = [];
explosions = [];
asteroids = [];
bullets = [];
planets = [];
rdm = 6
render_distance = [w*rdm, h*rdm]
minimap = Minimap(0,0);

min_ast_size = 40;
max_ast_size = 120;

def spawnAsteroids(xMin,xMax, yMin, yMax):
    for i in range(2):
        for j in range(2):
            x = random.randint(xMin, xMax);
            y = random.randint(yMin, yMax);
            size = random.randint(min_ast_size, max_ast_size);
            if y < 2*h:
                asteroids.append(Asteroid(x, y, size));
#for i in range(80):
    #planets.append(Planet(random.randint(-w*50, w*50), random.randint(-h*100, -h), random.randint(500, 750)));
#for i in range(1000):
    #stars.append(Star(random.randint(0, w), random.randint(0, h), random.randint(1, 140)))

asteroids.append(Asteroid(w/2, -10*h, 40));
ground = Ground(0,0);
ship = Ship(w/2, h/2);
pressed_left = False;
pressed_right = False;
pressed_up = False;
pressed_down = False;
pressed_bar = False;

SCORE_COOLDOWN = 1000;
SCORE_UP_AMOUNT = 0;
SCORE_UP_SHOW = False;
def scoreUpToFalse():
    global SCORE_UP_SHOW
    SCORE_UP_SHOW = False;
def set_timeout(func, sec):
    t = None
    def func_wrapper():
        func()
        t.cancel()
    t = threading.Timer(sec, func_wrapper)
    t.start()

while True:
    ast_already_in_screen = False;
    pygame.display.update()
    windowSurface.fill(BLACK)
    index_bullet_to_remove = [];
    index_asteroid_to_remove = [];
    index_explosion_to_remove = [];

    if (ship.altitude > 3000 and len(stars) < 100):
         stars.append(Star(random.randint(0, w), random.randint(0, h), random.randint(1, 140)))
    if (ship.altitude > 10000 and len(planets) < 80):
        planets.append(Planet(random.randint(-w*50, w*50), random.randint(-h*100, -h*4), random.randint(500, 800)));

    for i in range(len(explosions)):
        explosions[i].update();
        if explosions[i].frame == len(explosions[i].list):
            index_explosion_to_remove.append(i);

    for i in range(len(planets)):
        planets[i].update();
        distFromCenterX = w/2 - planets[i].x;
        distFromCenterY = h/2 - planets[i].y;
        radiusX=int(math.fabs(distFromCenterX)/100)
        radiusY=int(math.fabs(distFromCenterY)/100)
        Show = True;
        if radiusX>30000:
            Show = False;
        elif radiusX>150:
            radiusX=150
        if radiusY>30000:
            Show = False;
        elif radiusY>150:
            radiusY=150
        if (Show):
            #Gauche
            if (planets[i].x < 0):
                pygame.draw.circle(windowSurface, GREEN, (0, int(planets[i].y+planets[i].size/2)), radiusX, 1);
            #Droite
            if (planets[i].x > w):
                pygame.draw.circle(windowSurface, GREEN, (w-10, int(planets[i].y+planets[i].size/2)), radiusX, 1);
            #Haut
            if (planets[i].y < 0):
                pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x+planets[i].size/2), 10), radiusY, 1);
            #Bas
            if (planets[i].y > h):
                pygame.draw.circle(windowSurface, GREEN, (int(planets[i].x+planets[i].size/2), h-10), radiusY, 1);

    for i in range(len(asteroids)):
        #pygame.draw.lines(windowSurface, WHITE, False, [[asteroids[i].x, asteroids[i].y], [ship.x, ship.y]], 1)
        asteroids[i].move();
        asteroids[i].refreshPos();
        asteroids[i].show();
        distFromCenterX = w/2 - asteroids[i].x;
        distFromCenterY = h/2 - asteroids[i].y;
        if (math.fabs(distFromCenterX) > render_distance[0]*1.4 and len(asteroids) > 1 or math.fabs(distFromCenterY) > render_distance[1]*1.4 and len(asteroids) > 1):
            index_asteroid_to_remove.append(i);
        if (asteroids[i].maxlife != asteroids[i].life):
            asteroids[i].health();
        if (asteroids[i].x < 0 and asteroids[i].x > -w*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (0, int(asteroids[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        elif (asteroids[i].x > w and asteroids[i].x < w*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (w-10, int(asteroids[i].y)), int(math.fabs(distFromCenterX)/100), 1);
        elif (asteroids[i].y < 0 and asteroids[i].y > -h*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (int(asteroids[i].x), 10), int(math.fabs(distFromCenterY)/100), 1);
        elif (asteroids[i].y > h and asteroids[i].y < h*2):
            pygame.draw.circle(windowSurface, asteroids[i].color, (int(asteroids[i].x), h-10), int(math.fabs(distFromCenterY)/100), 1);

        if (asteroids[i].x > -w and asteroids[i].x < w and asteroids[i].y > -h and asteroids[i].y < h):
            ast_already_in_screen = True;
            if (ground.posY[0] <= asteroids[i].v2[1] or ground.posY[0] <= asteroids[i].v7[1]):
                xExpl = asteroids[i].x+asteroids[i].size
                yExpl = asteroids[i].y-2/asteroids[i].size
                explosions.append(Explosion(xExpl,yExpl,asteroids[i].size));
                index_asteroid_to_remove.append(i);

        if (ship.x + 31< asteroids[i].v4[0] and ship.x + 31 > asteroids[i].v1[0] and ship.y + 31> asteroids[i].v2[1] and ship.y + 31< asteroids[i].v7[1]):
            #random.choice(expl_sounds).play()
            xExpl = asteroids[i].x+asteroids[i].size
            yExpl = asteroids[i].y-2/asteroids[i].size
            explosions.append(Explosion(xExpl,yExpl,asteroids[i].size));
            if (asteroids[i].size/1.8 > 20):
                for e in range(2):
                    asteroids.append(Asteroid(asteroids[i].x, asteroids[i].y, int(asteroids[i].size/1.8)));
            index_asteroid_to_remove.append(i);
            ship.rotateSetTo(True);
            ship.notControlable(0.5);
            last_up=-10*asteroids[i].size
            if ((score+last_up)<=0):
                score=0;
            else:
                score+=last_up;
            SCORE_UP_SHOW = True;
            set_timeout(scoreUpToFalse, 1)

    for i in range(len(bullets)):
        bullets[i].refreshPos();
        bullets[i].show()
        for j in range(len(asteroids)):
            if (bullets[i].x >= asteroids[j].v1[0] and bullets[i].x <= asteroids[j].v4[0]  and bullets[i].y >= asteroids[j].v2[1] and bullets[i].y <= asteroids[j].v7[1]):
                #random.choice(expl_sounds).play()
                if (asteroids[j].life==1):
                    xExpl = asteroids[j].x+asteroids[j].size
                    yExpl = asteroids[j].y-2/asteroids[j].size
                    explosions.append(Explosion(xExpl,yExpl,asteroids[j].size));
                    index_asteroid_to_remove.append(j);

                    last_up=10*asteroids[j].size
                    score+=last_up
                    SCORE_UP_SHOW = True;
                    set_timeout(scoreUpToFalse, 1)

                    if (asteroids[j].size/1.8 > 20):
                        for e in range(2):
                            asteroids.append(Asteroid(asteroids[j].x, asteroids[j].y, int(asteroids[j].size/1.8)));
                else:
                    asteroids[j].life-=1
                index_bullet_to_remove.append(i);

        if (bullets[i].lifetime > 70 and i not in bullets):
            index_bullet_to_remove.append(i);


    for i in range(len(index_explosion_to_remove)):
        try:
            explosions.remove(explosions[index_explosion_to_remove[i]]);
        except:
            continue

    for i in range(len(index_bullet_to_remove)):
        try:
            bullets.remove(bullets[ index_bullet_to_remove[i]]);
        except:
            continue

    for i in range(len(index_asteroid_to_remove)):
        try:
            asteroids.remove(asteroids[ index_asteroid_to_remove[i]])
        except:
            spawnAsteroids(-w*2, w/2, -h*2, -h)
            pass;

    if (not ast_already_in_screen):
        if (pressed_up and ship.altitude > 6000):
            if (ship.returnDir() == "up"):
                for i in range(2):
                    spawnAsteroids(-render_distance[0], render_distance[0]/2, -render_distance[1], 0);
            if (ship.returnDir() == "down"):
                for i in range(2):
                    spawnAsteroids(-render_distance[0], render_distance[0], 1000, render_distance[1]);
            if (ship.returnDir() == "left"):
                spawnAsteroids(-render_distance[0], render_distance[0], -render_distance[1], render_distance[1]);
            if (ship.returnDir() == "right"):
                spawnAsteroids(-render_distance[0], render_distance[0], -render_distance[1], render_distance[1]);
    ship.show();
    ship.move();
    ship.shoot();
    ground.show();
    for i in range(len(stars)):
        stars[i].x += stars[i].z/1000;
        stars[i].y += stars[i].z/1000;
        stars[i].show();
        if (stars[i].x > w):
            stars[i].x = 0;
        if (stars[i].x < 0):
            stars[i].x = w;

        if (stars[i].y > h):
            stars[i].y = 0;
        if (stars[i].y < 0):
            stars[i].y = h;
    minimap.show();
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed();
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pressed_up = True;
            if event.key == pygame.K_DOWN:
                pressed_down = True;
            if event.key == pygame.K_RIGHT:
                pressed_right = True;
            if event.key == pygame.K_LEFT:
                pressed_left = True;
            if event.key == pygame.K_SPACE:
                pressed_bar = True;
            if event.key == pygame.K_ESCAPE:
                event.type = QUIT;

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pressed_up = False;
            if event.key == pygame.K_DOWN:
                pressed_down = False;
            if event.key == pygame.K_RIGHT:
                pressed_right = False;
            if event.key == pygame.K_LEFT:
                pressed_left = False;
            if event.key == pygame.K_SPACE:
                pressed_bar = False;
        if event.type == QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    scoretext = myfont2.render("SCORE: "+str(round(score)), 1, (77,255,77))
    windowSurface.blit(scoretext, (w-200, h-110))
    ALTITUDE = myfont2.render('ALTITUDE: ' + str(ship.altitude), 1, (77,255,77))
    windowSurface.blit(ALTITUDE, (20, minimap.size+25))
    DIRECTION = myfont2.render('DIRECTION: ' + ship.returnDir(), 1, (77,255,77))
    windowSurface.blit(DIRECTION, (20, minimap.size+55))
    HUD = myfont3.render("FPS: "+str(round(clock.get_fps(), 2)), 1, WHITE)
    windowSurface.blit(HUD, (w-200, h-70))
    if (SCORE_UP_SHOW):
        if (last_up<=0):
            SCORE_UP = myfont1.render("- "+str(-1*(last_up)), 1, (255,77,77));
        else:
            SCORE_UP = myfont1.render("+ "+str(last_up), 1, (77,255,77));
        windowSurface.blit(SCORE_UP, (w-200, h-150))
    clock.tick(60);
