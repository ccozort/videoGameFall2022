# content from kids can code: http://kidscancode.org/blog/
#...
# sources
# getting mouse position: https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.get_pos
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable
# fire towards mouse:
# https://stackoverflow.com/questions/63495823/how-to-shoot-a-bullet-towards-mouse-cursor-in-pygame 
# timer https://www.youtube.com/watch?v=YOCt8nsQqEo 


#  design
'''
Innovation:
Fire projectile at mouse...
Create a timer/cooldown class
Load game background image
Create particles
Create tiny healthbars above all mobs that adjust based on their hitpoints
Add double jump

Goals rules feedback freedom!!!

'''

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
import random
from random import randint
import os
from os import path
from math import *
from time import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# sound added
pg.mixer.init

# images
background = pg.image.load(path.join(img_folder, 'starfield.png'))
background_rect = background.get_rect()
theBell = pg.image.load(path.join(img_folder, 'theBell.png'))
theBell_rect = background.get_rect()
theBell.set_colorkey(BLACK)
theBell = pg.transform.scale(theBell, (200,200))

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        g.screen.blit(text_surface, text_rect)

def colorbyte(x,y):
    if x < 0 or x > 255:
        x = 0
    if y > 255 or y < 0:
        y = 255
    return random.randint(x,y)

# create all classees as sprites...

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font("arial")
        # self.load_data()
    def new(self):
        self.player = Player(self)
        # create groups
        self.all_sprites = pg.sprite.Group()
        self.all_plats = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pewpews = pg.sprite.Group()
        self.enemyPewpews = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.plat = Platform(180, 380, 100, 35, "normal")
        self.plat2 = Platform(289, 180, 100, 35, "ouchie")
        self.powerup1 = Powerup(100,350, 25, 25)
        self.ground = Platform(0, HEIGHT-40, WIDTH, 40, "lava")      
        # instantiate lots of mobs in a for loop and add them to groups
        for i in range(30):
            m = Mob(self,randint(0,WIDTH), randint(0,HEIGHT/2), 25, 25, (colorbyte(0,150),colorbyte(0,255),colorbyte(0,255)), "normal", 5)
            self.all_sprites.add(m)
            self.mobs.add(m)
            # print(m)
        for i in range(2):
            m = Mob(self,randint(0,WIDTH), randint(0,HEIGHT/3), 50, 50, (colorbyte(0,10),colorbyte(150,255),colorbyte(0,100)), "boss", 25)
            self.all_sprites.add(m)
            self.mobs.add(m)
            # print(m)
        # add things to groups...
        self.all_sprites.add(self.player, self.plat, self.plat2, self.ground, self.powerup1)
        self.powerups.add(self.powerup1)
        self.all_plats.add(self.plat, self.plat2, self.ground)


# init game

g = Game()
g.new()

############################# Game loop ###########################################
# starts timer...
start_ticks = pg.time.get_ticks()

running = True
while running:
    delta = g.clock.tick(FPS)
    # print(clock.get_time())
    # keep the loop running using clock
    hits = pg.sprite.spritecollide(g.player, g.all_plats, False)
    if hits:
        # if hits[0].typeof == "ouchie":
        #     print("yikes I'm dead...")
        # if hits[0].typeof == "lava":
        #     print("I'm standing on the LAVA...")
        # if hits[0].typeof == "ouchie":
        #     print("yikes I'm dead...")
        # print("ive struck a plat")
        g.player.pos.y = hits[0].rect.top
        g.player.vel.y = 0

    for p in g.powerups:
        powerUphit = pg.sprite.spritecollide(g.player, g.powerups, True)
        if powerUphit:
            
            print("i got a powerup...")
            g.player.jumppower += 10

    for p in g.enemyPewpews:
        playerhit = pg.sprite.spritecollide(g.player, g.enemyPewpews, True)
        if playerhit:
            for i in range(3):
                particle = Particle(playerhit[0].rect.x, playerhit[0].rect.y, randint(1,3), randint(1,3))
                g.all_sprites.add(particle)
            print('the player has been hit')
            g.player.health -= 1

    for p in g.pewpews:
        mhit = pg.sprite.spritecollide(p, g.mobs, False)
        # print(mhit.keys())
        if mhit:
            if p.rect.width > 10:
                mhit[0].currenthealth -= 5
            else:
                mhit[0].currenthealth -= 1
            for i in range(3):
                    particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,3), randint(1,3))
                    g.all_sprites.add(particle)
            print("mob health is " + str(mhit[0].health))
            if mhit[0].currenthealth < 1:
                for i in range(30):
                    particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,7), randint(1,7))
                    g.all_sprites.add(particle)
                mhit[0].kill()
                SCORE += 1
                
        # if mhit:
        #     print('hit mob ' + str(mhit[0]))
    
    mobhits = pg.sprite.spritecollide(g.player, g.mobs, True)

    if mobhits:
        # print("ive struck a mob")
        g.player.health -= 1
        if g.player.r < 255:
            g.player.r += 15 

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            g.player.fire()
                
            # get a list of all sprites that are under the mouse cursor
            # clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            # for m in mobs:
            #     if m.rect.collidepoint(mpos):
            #         print(m)
            #         m.kill()
            #         SCORE += 1

            # print(clicked_sprites)k 
        # check for keys
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if PAUSED:
                    PAUSED = False
                else:
                    PAUSED = True
            if event.key == pg.K_SPACE:
                g.player.jump()

    if not PAUSED:  
        ############ Update ##############
        # update all sprites
        g.all_sprites.update()
        ############ Draw ################
        # draw the background screen
        
        g.screen.fill(BLACK)
        # screen.blit(background, background_rect)
        # screen.blit(theBell, ((WIDTH/2), HEIGHT/2))
    


    # draw text
    draw_text("FPS: " + str(delta), 22, RED, 64, HEIGHT / 24)
    # draw_text("Timer: " + str(seconds), 22, RED, 64, HEIGHT / 10)
    draw_text("SCORE: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    draw_text("HEALTH: " + str(g.player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    # pg.draw.polygon(screen,BROWN,[(player.rect.x, player.rect.y), (152, 230), (1056, 230),(1056, 190)])
    
    # draw player color
    # player.image.fill((player.r,player.g,player.b))

    if not PAUSED:

        # draw all sprites
        g.all_sprites.draw(g.screen)
        for m in g.mobs:
            g.screen.blit(m.healthbar, m.rect)
        pg.draw.circle(g.player.image, (YELLOW), g.player.rect.center, g.player.cd.delta)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
