import pygame as pg
from settings import *
from sprites import *
from utils import *
from pygame.sprite import Sprite
from random import randint
from random import choice
from math import *
from time import *

vec = pg.math.Vector2


# player sprite
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.cd = Cooldown()
        self.image = pg.Surface((50, 50))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.set_colorkey(BLACK)
        # self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
        self.radius = 23
        pg.draw.circle(self.image, (self.r,self.g,self.b), self.rect.center, self.radius)
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT-45)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.jumppower = 25
        self.fired = False
        self.jumps = 2
        self.mpos = (0,0)

    def controls(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.acc.y = -5
        if keys[pg.K_a]:
            self.acc.x = -5
        # if keys[pg.K_s]:
        #     self.acc.y = 5a
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_e]:
            self.fire()
    def fire(self):
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
        self.mpos = pg.mouse.get_pos()
        targetx = self.mpos[0]
        targety = self.mpos[1]
        distance_x = targetx - self.rect.x
        distance_y = targety - self.rect.y
        angle = atan2(distance_y, distance_x)
        speed_x = 10 * cos(angle)
        speed_y = 10 * sin(angle)
        if self.cd.delta > 2:
            p = Pewpew(self.pos.x,self.pos.y - self.rect.height, 30, 30, speed_x, speed_y, "player")
        else:
            p = Pewpew(self.pos.x,self.pos.y - self.rect.height, 10, 10, speed_x, speed_y, "player")

        self.game.all_sprites.add(p)
        self.game.pewpews.add(p)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.all_plats, False)
        self.rect.x += -1
        if hits:
            self.jumps = 2
        if self.jumps > 0:
            self.vel.y = -self.jumppower
            self.jumps -=1
    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
    def update(self):
        self.cd.ticking()

        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.inbounds()
        self.rect.midbottom = self.pos

class Platform(Sprite):
    def __init__(self, x, y, w, h, typeof):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.typeof = typeof
# powerup

class Powerup(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# display image
# class Displayimage(Sprite):
#     def __init__(self, x, y):
#         Sprite.__init__(self)
#         self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#     def update(self):
#         pass


# bullet sprite
class Pewpew(Sprite):
    def __init__(self, x, y, w, h,sx,sy, owner):
        Sprite.__init__(self)
        self.owner = owner
        self.image = pg.Surface((w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if self.owner == 'player':
            self.radius = w/2
            pg.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        else:
            self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y
        self.speed_x = sx
        self.speed_y = sy
        self.fired = False
    
    def update(self):
        if self.owner == "player":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        else:
            self.rect.y += self.speed_y
        if (self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill()

class Healthbar(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def damage(self, newwidth):
        self.rect.w = newwidth

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, color, typeof, health):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.typeof = typeof
        self.health = health
        self.currenthealth = health
        self.initialized = False
        self.healthbar = pg.Surface((self.rect.width, 5))
        self.healthbar.fill(RED)
        self.cd = Cooldown()
        self.canshoot = True
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
    def update(self):
        self.cd.ticking()
        self.healthbar = pg.Surface((self.rect.width*(self.currenthealth/self.health), 5))
        self.healthbar.fill(RED)

        # self.rect.y += self.speed
        if self.typeof == "boss":
            self.rect.x += self.speed*5

            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 25
            if self.rect.bottom > HEIGHT:
                self.rect.top = 0
        else:
            self.rect.x += self.speed
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 15
            if self.cd.delta > randint(2,25) and self.game.enemyPewpews.__len__() < 10:
                self.cd.event_time = floor(pg.time.get_ticks()/1000)
                p = Pewpew(self.rect.x, self.rect.y, 5, 15, 0, 5, 'enemy')
                self.game.all_sprites.add(p)
                self.game.enemyPewpews.add(p)

class Particle(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = randint(2,20)*choice([-1,1])
        self.speedy = randint(2,20)*choice([-1,1])
        self.cd = Cooldown()
        self.cd.event_time = floor(pg.time.get_ticks()/1000)
    def update(self):
        self.cd.ticking()
        self.rect.x += self.speedx
        self.rect.y += self.speedy+PLAYER_GRAV
        if self.cd.delta > 1:
            self.kill()


