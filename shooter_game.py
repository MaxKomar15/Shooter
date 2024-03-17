
from typing import Any
from pygame import *
from random import randint
from pygame import *
init()
mixer.init()
font.init()

FPS = 60
screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
flags = FULLSCREEN
window = display.set_mode((WIDTH, HEIGHT), flags)

font1 = font.SysFont("Arial", 40)
font2 = font.SysFont("Arial", 50)

mixer.music.load("space.ogg") 
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

fire_sound = mixer.Sound('fire.ogg')

kick_sound = mixer.Sound('fire.ogg')
kick_sound.play()

window = display.set_mode((WIDTH, HEIGHT)) #створюємо вікно 
display.set_caption("Shooter")
clock = time.Clock() # Створюємо ігровий таймер

bg = image.load("infinite_starts.jpg") # завантажуємо картинку в гру
bg = transform.scale(bg, (WIDTH, HEIGHT)) #змінюємо розмір картинки
player_img = image.load('spaceship.png')
enemy_img = image.load('alien.png')
bullet_img = image.load('lazer.png')
bg_y1 = 0
bg_y2 = -HEIGHT


sprites = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)
        self.start_rect = self.rect
        self.hp = 100
        self.damage = 20
        self.points = 0
        self.speed = 10
        self.bg_speed = 2

    def update(self):
        global hp_text
        self.old_pos = self.rect.x, self.rect.y

        keys = key.get_pressed() #отримуємо список натиснутих клавіш
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.bg_speed = 4
        elif keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.bg_speed = 1
        else:
            self.bg_speed = 2

        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.y)
        fire_sound.play()





enemys = sprite.Group()

class Enemy(GameSprite):
        def __init__(self):
            rand_x = randint(0, WIDTH-70)
            y = -150
            super().__init__(enemy_img, 100, 70, rand_x, y)
            self.speed = 5
            enemys.add(self)


        def update(self):
            self.rect.y += self.speed
            if self.rect.y > HEIGHT:
                self.kill()
            
bullets = sprite.Group()

class Bullet(GameSprite):
        def __init__(self, player_x, player_y):
            super().__init__(bullet_img, 20, 40, player_x, player_y)
            self.rect.centerx = player_x
            self.rect.bottom = player_y
            self.speed = 15
            bullets.add(self)

        def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.kill()


player = Player(player_img, 90, 100, 300, 300)

hp_text = font1.render(F"HP: {player.hp}", True, (255, 255, 255))
points_text = font1.render(F"Points: {player.points}", True, (255, 255, 255))
finish_text = font2.render("[>GAME OVER<]", True, (255, 0, 0))

finish = False
Enemy()
last_spawn_time = time.get_ticks()
spawn_interval = randint(1000, 3000)

while True:
    #оброби подію «клік за кнопкою "Закрити вікно"
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                player.fire()

    if not finish:
        now = time.get_ticks()
        if now - last_spawn_time > spawn_interval:
            Enemy()
            last_spawn_time = time.get_ticks()
            spawn_interval = randint(1000, 3000)
        
        bullets_collide = sprite.groupcollide(bullets, enemys, True, True, sprite.collide_mask)
        collide_list = sprite.spritecollide(player, enemys, False, sprite.collide_mask)
        for enemy in collide_list:
            player.hp -= 50
            hp_text = font1.render(F"HP: {player.hp}", True, (255, 255, 255))
            enemys.remove(enemy)

        sprites.update()
      
        if player.hp <= 0:
            finish = True

        window.blit(bg, (0,bg_y1))
        window.blit(bg, (0,bg_y2))
        bg_y1 += player.bg_speed
        bg_y2 += player.bg_speed
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT
    sprites.draw(window)
    window.blit(hp_text, (10, 10))
    window.blit(points_text, (WIDTH-200, 10))
    if finish:
        window.blit(finish_text, (300, 250))
    display.update()
    clock.tick(FPS)


