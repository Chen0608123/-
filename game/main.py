import pygame
import random
import os

# 設定變數
WIDTH = 600
HIGH = 800
FPS = 60
# 遊戲內顏色
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)


# 初始化 
pygame.init()
# 創建視窗(width,height)
screen = pygame.display.set_mode((WIDTH,HIGH))
# 設定標題
pygame.display.set_caption("第一次")
# 管理使間
clock = pygame.time.Clock()

#載入圖片
        #                         #   py裡的     img資料夾
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()

# 玩家生成
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
                      #更改圖片大小           圖片          寬,高
        self.image = pygame.transform.scale(player_img , (50,38)) 
                        #要刪除的部分
        self.image.set_colorkey(WHITE) # 將圖片中的部分刪除
        self.rect = self.image.get_rect() # 物件定位並框起來
        self.rect.centerx = WIDTH/2 # 定位
        self.rect.bottom = HIGH - 10
        self.speedx = 8 #物件移動速度


    def update(self):
        key_pressed = pygame.key.get_pressed() # 判斷鍵盤按鍵是否被按下，回傳布林值
        if key_pressed[pygame.K_d]: # 若d鍵被按下
            self.rect.x += self.speedx 
        if key_pressed[pygame.K_a]: # 若a鍵被按下
            self.rect.x -= self.speedx
        # 將物件鎖在視窗內
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        #self.rect.x += 2 
        #if self.rect.left > WIDTH: # 若左座標 > 寬 
            #self.rect.right = 0 # 則右座標 = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top) # 傳入座標的參數(X,Y)
        all_Sprites.add(bullet) # 將此事傳入群組裡
        bullets.add(bullet)
# 生成石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(rock_img , (35,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # 物件定位並框起來
        self.rect.x = random.randrange(0,WIDTH - self.rect.width) # 定位 位於0~視窗寬度-自身寬度
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,10) # 物件掉落移動速度
        self.speedx = random.randrange(-3,3) # 物件左右移動速度


    def update(self):
        self.rect.y += self.speedy # 物件隨機掉落
        self.rect.x += self.speedx # 物件隨機左右晃動
            #若頂度超出則重製           #若左大於視窗寬則重製     #若右小於0則重製
        if  self.rect.top > HIGH or self.rect.left > WIDTH or self.rect.right < 0: 
            self.rect.x = random.randrange(0 , WIDTH - self.rect.width) 
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10) 
            self.speedx = random.randrange(-3,3)

# 生成子彈、碰撞判定
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y): # 創建子彈時，要根據玩家位置生成
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img , (10,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # 物件定位並框起來
        self.rect.centerx = x 
        self.rect.bottom = y
        self.speedy = -10 # 子彈是向上射所以是-10


    def update(self):
        self.rect.y += self.speedy 
        if self.rect.bottom < 0: # 若子彈的底部<0代表超過視窗
            self.kill() # 將自身從所有群組刪除

# Sprite 群組 
all_Sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group() 
bullets = pygame.sprite.Group()
player = Player() 
all_Sprites.add(player)
# 重複執行生成石頭
for i in range(8):
    r = Rock()
    all_Sprites.add(r)
    rocks.add(r)


#設定遊戲持續的變數
running = True
#遊戲迴圈
while running:
    #一秒鐘之內最多能被執行()次，()內的數被稱為fps
    clock.tick(FPS)
    # 取得輸入
                        # 回傳現在發生的事件
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # 偵測輸入鍵
            if event.key == pygame.K_SPACE: # 若輸入鍵為空白建
                player.shoot() # 回傳函數


    # 更新遊戲
    all_Sprites.update() # 執行all_Sprites裡的update程式
                                  #  傳入兩個群組   是否要刪除
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True) # 物件碰撞
    for hit in hits: # 因為碰觸後刪除，所以將其加回all_Sprites
        r = Rock()
        all_Sprites.add(r)
        rocks.add(r)

    hits = pygame.sprite.spritecollide(player,rocks,False) # 若玩家碰觸到石頭
    if hits:
        running = False # 關閉遊戲
    
    # 畫面顯示
             #(R,G,B)
    screen.fill(BLACK)
             #  畫的圖         位置
    screen.blit(background_img,(0,0))

    all_Sprites.draw(screen) # draw() = 將all_Sprites裡的物件畫在screen上
    pygame.display.update()

pygame.quit()