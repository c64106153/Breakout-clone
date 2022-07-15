import random
import pygame
import os

# 遊戲初始化 + 創建視窗
Width = 1000
Height = 750
FPS=60

pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((Width,Height))
screen.fill((0,0,0))
pygame.display.set_caption("打磚塊")
clock = pygame.time.Clock()


# 載入圖片
background_img=pygame.image.load(os.path.join("pic","background1.jpg")).convert()
screen.blit(background_img,(0,0))

# 載入音樂、音效
Hit=pygame.mixer.Sound(os.path.join("sound","hit.mp3"))
Hit.set_volume(0.2)
pygame.mixer.music.load(os.path.join("sound","backsound3.mp3"))
pygame.mixer.music.set_volume(0.3)

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(None,size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_init():
    draw_text(screen,'Click to start!',64, Width/2,Height*0.75)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            play = pygame.mouse.get_pressed()
            if play[0]:
                waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((125,25))
        self.image.fill((0,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx = Width/2
        self.rect.centery = Height-50
        self.speedx = 8

    def update(self):
        (mouse_x,mouse_y) =pygame.mouse.get_pos()
        self.rect.centerx =mouse_x
        if self.rect.right >Width:
            self.rect.right = Width
        if self.rect.left <0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((15,15))
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery-25
        self.lives = 3
        self.speedx = 10
        self.speedy = -10
        self.run = 0

    def update(self):
        if self.run == 0:
            self.rect.centerx = player.rect.centerx
            self.rect.centery = player.rect.centery-25
            play = pygame.mouse.get_pressed()
            if play[0]:
                self.run=1
        elif self.run == 1:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top <0:
                self.rect.top = 0
                self.speedy *= -1
            if self.rect.bottom > Width:
                self.lives -= 1
                self.speedy *= -1
                self.run = 0
            if self.rect.left <0:
                self.rect.left=0
                self.speedx *= -1
            if self.rect.right >Width:
                self.rect.right =Width
                self.speedx *= -1

class brick(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([80,20])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.num =50


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
ball = Ball()
all_sprites.add(ball)
bricks = pygame.sprite.Group()

#新增磚塊
for i in range(5):
    for j in range(0,10):
        R=random.randint(150,250)
        G=random.randint(150,250)
        B=random.randint(150,250)
        Brick=brick((R,G,B),+j*90+50,70+i*40)
        bricks.add(Brick)
        all_sprites.add(Brick)

pygame.mixer.music.play(-1)

running=True
show_init=True
all_sprites.draw(screen)

# 遊戲迴圈
while running:
    
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # 碰撞判定
    hits=pygame.sprite.groupcollide([ball],bricks,False,True)
    for hit in hits:
        Hit.play()
        ball.speedy *= -1
        Brick.num -= 1 

    hits=pygame.sprite.groupcollide([player],[ball],False,False)
    for hit in hits:
            Hit.play()
            ball.speedy *=-1
    
    #背景更新
    screen.fill((0,0,0))
    screen.blit(background_img,(0,0))
    draw_text(screen,'Bricks: '+str(Brick.num),50, Width/5,20)
    draw_text(screen,'Ball: '+str(ball.lives),50, Width-200,20)       

    #gameover後重新設定
    if Brick.num == 0:
        draw_text(screen,'Clear !!',100, Width/2,Height/2)
        show_init=True
        
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        ball = Ball()
        all_sprites.add(ball)
        bricks = pygame.sprite.Group()
        for i in range(5):
            for j in range(0,10):
                R=random.randint(150,250)
                G=random.randint(150,250)
                B=random.randint(150,250)
                Brick=brick((R,G,B),+j*90+50,70+i*40)
                bricks.add(Brick)
                all_sprites.add(Brick)
        Brick.num =50
        ball.lives =3
        pygame.mixer.music.play(-1)
        
    if ball.lives == 0:
        show_init=True
        draw_text(screen,'Game Over!! ',100, Width/2,Height/2)
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        ball = Ball()
        all_sprites.add(ball)
        bricks = pygame.sprite.Group()
        for i in range(5):
            for j in range(0,10):
                R=random.randint(150,250)
                G=random.randint(150,250)
                B=random.randint(150,250)
                Brick=brick((R,G,B),+j*90+50,70+i*40)
                bricks.add(Brick)
                all_sprites.add(Brick)
        pygame.mixer.music.play(-1)

        
        Brick.num =50
        ball.lives =3

    
    
    all_sprites.draw(screen)
    all_sprites.update()
    
    pygame.display.update()
