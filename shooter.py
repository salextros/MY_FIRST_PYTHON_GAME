import pygame, random
import sys

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text,True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface,text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('shooter-pygame-master/assets/player.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()
        
        
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10  or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('shooter-pygame-master/assets/laser1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
meteor_images = []
meteor_list = ['shooter-pygame-master/assets/meteorGrey_big1.png',
               'shooter-pygame-master/assets/meteorGrey_big2.png',
               'shooter-pygame-master/assets/meteorGrey_big3.png',
               'shooter-pygame-master/assets/meteorGrey_big4.png'
               ,'shooter-pygame-master/assets/meteorGrey_med1.png',
               'shooter-pygame-master/assets/meteorGrey_med2.png',
               'shooter-pygame-master/assets/meteorGrey_small1.png',
               'shooter-pygame-master/assets/meteorGrey_small2.png',
               'shooter-pygame-master/assets/meteorGrey_tiny1.png',
               'shooter-pygame-master/assets/meteorGrey_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

            
# Cargar imagen de fondo
background = pygame.image.load('shooter-pygame-master/assets/background.png').convert() 

# Cargar sonidos
laser_sound = pygame.mixer.Sound('shooter-pygame-master/assets/laser5.ogg')
explosion_sound = pygame.mixer.Sound('shooter-pygame-master/assets/explosion.wav')
pygame.mixer.music = pygame.mixer.Sound('shooter-pygame-master/assets/music.ogg')
pygame.mixer.music.set_volume(0.2)


     
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

score = 0
pygame.mixer.music.play(loops=-1)
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
    all_sprites.update()
    
#COLISIONES - METEORO - LASER

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

#CHEQUEAR COLISIONES - JUGADOR - METEORO
    
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    if hits:
        running = False
    
    
    screen.blit(background,[0,0])
    
    all_sprites.draw(screen)
    
#MARCADOR
    draw_text(screen, str(score),25,WIDTH // 2, 10)
    
    pygame.display.flip()
pygame.quit()

