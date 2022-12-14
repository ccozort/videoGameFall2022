# content from kids can code: http://kidscancode.org/blog/
# sources
# getting mouse position: https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.get_pos
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable
# fire towards mouse:
# https://stackoverflow.com/questions/63495823/how-to-shoot-a-bullet-towards-mouse-cursor-in-pygame 
# timer https://www.youtube.com/watch?v=YOCt8nsQqEo 
'''
Goals: Blast all enemies, avoid being hit
Rules: Click to fire at mouse, cannot 'move' vertically
Feedback: Lost health when hit, particles when hit, points
Freedom: Can move side to side, shoot at mouse position, jump
Innovation:
Fire projectile at mouse...
Create a timer/cooldown class
Load game background image
Create particles
Create tiny healthbars above all mobs that adjust based on their hitpoints
Add double jump
'''
import pygame as pg
from settings import *
from sprites import *
from random import randint
import os
from os import path
from math import *
from time import *

vec = pg.math.Vector2
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
pg.mixer.init
background = pg.image.load(path.join(img_folder, 'starfield.png'))
background_rect = background.get_rect()
theBell = pg.image.load(path.join(img_folder, 'theBell.png'))
theBell_rect = background.get_rect()
theBell.set_colorkey(BLACK)
theBell = pg.transform.scale(theBell, (200,200))

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
    def new(self):
        self.player = Player(self)
        self.score = 0
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
        for i in range(30):
            m = Mob(self,randint(0,WIDTH), randint(0,HEIGHT/2), 25, 25, (colorbyte(0,150),colorbyte(0,255),colorbyte(0,255)), "normal", 5)
            self.all_sprites.add(m)
            self.mobs.add(m)
        for i in range(2):
            m = Mob(self,randint(0,WIDTH), randint(0,HEIGHT/3), 50, 50, (colorbyte(0,10),colorbyte(150,255),colorbyte(0,100)), "boss", 25)
            self.all_sprites.add(m)
            self.mobs.add(m)
        self.all_sprites.add(self.player, self.plat, self.plat2, self.ground, self.powerup1)
        self.powerups.add(self.powerup1)
        self.all_plats.add(self.plat, self.plat2, self.ground)
        print('new')
        self.run()
    def run(self):
        self.playing = True
        while self.playing:
            self.delta = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                self.player.fire()
            # clicked_sprites = [s for s in self.mobs if s.rect.collidepoint(mpos)]
            for m in self.mobs:
                if m.rect.collidepoint(self.player.mpos):
                    pass
                    # print(m)
                    # m.kill()
                    # SCORE += 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    if PAUSED:
                        PAUSED = False
                    else:
                        PAUSED = True
                if event.key == pg.K_SPACE:
                    self.player.jump()
        hits = pg.sprite.spritecollide(g.player, g.all_plats, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0
        for p in self.powerups:
            powerUphit = pg.sprite.spritecollide(self.player, self.powerups, True)
            if powerUphit:
                self.player.jumppower += 10
        for p in self.enemyPewpews:
            playerhit = pg.sprite.spritecollide(self.player, self.enemyPewpews, True)
            if playerhit:
                for i in range(3):
                    particle = Particle(playerhit[0].rect.x, playerhit[0].rect.y, randint(1,3), randint(1,3))
                    self.all_sprites.add(particle)
                self.player.health -= 1
        for p in self.pewpews:
            mhit = pg.sprite.spritecollide(p, self.mobs, False)
            if mhit:
                if p.rect.width > 10:
                    mhit[0].currenthealth -= 5
                else:
                    mhit[0].currenthealth -= 1
                for i in range(3):
                        particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,3), randint(1,3))
                        self.all_sprites.add(particle)
                if mhit[0].currenthealth < 1:
                    for i in range(30):
                        particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,7), randint(1,7))
                        self.all_sprites.add(particle)
                    mhit[0].kill()
                    self.score += 1
        mobhits = pg.sprite.spritecollide(g.player, g.mobs, True)
        if mobhits:
            self.player.health -= 1
            if self.player.r < 255:
                self.player.r += 15 
    def update(self):
        # pass
        self.all_sprites.update()
    def draw(self):
        self.screen.fill(BLACK)
        draw_text(self.screen, "FPS: " + str(self.delta), 22, RED, 64, HEIGHT / 24)
        draw_text(self.screen, "SCORE: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 24)
        draw_text(self.screen, "HEALTH: " + str(self.player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
        self.all_sprites.draw(self.screen)
        for m in self.mobs:
            self.screen.blit(m.healthbar, m.rect)
        pg.draw.circle(self.player.image, (YELLOW), self.player.rect.center, self.player.cd.delta)
        pg.display.flip()
    def show_start_screen():
        pass    
    def show_go_screen():
        pass    
g = Game()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
