# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
# from platform import platform
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

vec = pg.math.Vector2

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30

# player settings
PLAYER_FRIC = -0.2
PLAYER_GRAV = .98
POINTS = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# sprites...
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False

    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.y = 0
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.y = 0
            self.acc.x = 5
        if keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s]:
            self.acc.y = 5
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False


        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                # print("xdif " + str(xdiff))
                # print("ydif " + str(ydiff))

                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.top - self.rect.height/2
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.pos.y = hits[0].rect.bottom + self.rect.height/2
                self.vel.y = 0
                self.centery = self.pos.y
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

 
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        # friction
        self.rect.center = self.pos
        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity



class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mob(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 5*random.choice([-1,1])
        self.speedy = 5*random.choice([-1,1])
        self.inbounds = True
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery

    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1

    def update(self):
        self.boundscheck()
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(WIDTH/2, HEIGHT/3, 25, 75)
plat1 = Platform(75, 300, 75 ,75)
# mob = Mob(25, 57, 25, 25)

# add instances to groups
all_sprites.add(player)
all_sprites.add(plat)
all_sprites.add(plat1)
# all_sprites.add(mob)
all_platforms.add(plat)
all_platforms.add(plat1)

for i in range(8):
    # instantiate mob class repeatedly
    m = Mob(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    all_sprites.add(m)
    mobs.add(m)
for m in mobs:
    print(type(m))


# print(mobs)
# Game loop
running = True
while running:
    # keep the loop running using clock
    dt = clock.tick(FPS)

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    
    # update all sprites
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        POINTS += 1
        # print(POINTS)
        # print("i've collided...with a mob")
        # print(mobhits[0].color)
    all_sprites.update()
    
    ############ Draw ################
    # draw the background screen

    screen.fill(BLACK)
    # draw all sprites
    all_sprites.draw(screen)
    draw_text("POINTS: " + str(POINTS), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    if mobhits:
        pg.draw.line(screen, (RED), [player.rect.centerx, player.rect.centery], [mobhits[0].rect.centerx, mobhits[0].rect.centery], 5)
    if player.colliding:
        pg.draw.line(screen, (RED), [player.rect.centerx, player.rect.centery], [player.hitx, player.hity], 5)

    # draw_text("FPS: " + str(dt), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw_text("asdfasdfasdfasdfasdf: " + str(dt), 22, WHITE, WIDTH / 2, HEIGHT / 24)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()