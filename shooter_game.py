#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer

window = display.set_mode((700, 500))

display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

clock = time.Clock()
FPS = 60

num_fire = 0
rel_time = False


global score
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
                                                          
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 5,10)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(0, 635)
            self.rect.y = 0 
            global lost
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

lost = 0

hero = Player('rocket.png', 435, 435, 10, 65, 65)
monsters = sprite.Group()
for i in range (5):
    monster = Enemy('ufo.png', randint(0,635), 0, randint( 1,1), 65, 45)
    monsters.add(monster)


stones = sprite.Group()
for i in range (2):
    stone = Enemy('asteroid.png', randint(0,635), 0,randint( 1,1), 65, 45)
    stones.add(stone) 
bullets = sprite.Group()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
font3 = font.SysFont('Arial', 50)
font4 = font.SysFont('Arial', 50)


Finish = False


game = True
while game:
    if Finish != True:
        

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_chet = font1.render('Счет: '+str(score), 1,  (255, 255, 255))
        
        window.blit(background, (0, 0))
        window.blit(text_chet, (0,25))
        window.blit(text_lose, (0,50))
        hero.reset()
        hero.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        stones.update()
        stones.draw(window) 
        sprites_list = sprite.spritecollide(hero, monsters, False)
        sprites_list1 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.spritecollide(hero, stones, False)
        
      




        for s in sprites_list1: 
            score += 1
            
            monster = Enemy('ufo.png', randint(0,635), 0, randint( 1,1), 65, 45)
            monsters.add(monster) 
        
        if len(sprites_list)>0 or lost>4:
            Finish = True
            lose = font2.render('ИГРА ПРИОСТАНОВЛЕНА ', True, (255,0,0))
            window.blit(lose, (200,200))
        if score > 9:
            Finish = True
            win = font3.render('YOU WIN', True, (255,255,0))
            window.blit(win, (200,200))
        if rel_time == True:
            new_time = timer()
            if new_time - old_time >= 3:
                num_fire = 0 
                rel_time = False
            else:
                wait = font4.render('Wait, reload', True, (0,255,0))
                window.blit(wait, (200,200))



    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    hero.fire()
                    num_fire += 1
                else:
                    rel_time = True
                    old_time = timer()
            
                
        




    
    
    
    display.update()                    
    clock.tick(FPS)