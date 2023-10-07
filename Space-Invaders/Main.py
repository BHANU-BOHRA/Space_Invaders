import random

import pygame as pg

# initailizing the pygame
pg.init()
_running = True

# Setting up the Display
screen = pg.display.set_mode((800, 600))

# Setting the Title
pg.display.set_caption("Space Invaders")

# Setting up the Logo
pg.display.set_icon(pg.image.load('ufo.png'))

# Setting up the Background
bg_img = pg.image.load('background.png')

# Setting up the Background Music
pg.mixer.music.load('background.wav')
pg.mixer.music.play(-1)

# Setting up Score
score_val = 0
font = pg.font.Font('freesansbold.ttf', 32)
fontX = 10
fontY = 10

def getScore(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Setting the Game Over text
over_font = pg.font.Font('freesansbold.ttf', 70)

def game_over():
    gm_over = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gm_over, (200, 250))

# Player
playerImg = pg.image.load('player.png')
playerX = 360
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_num = 6

for i in range(enemy_num):
    enemyImg.append(pg.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(30, 180))
    enemyX_change.append(1.25)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = False  # False means Bullet is not fired and True means Bullet is currently Fired

def fire(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImg, (x + 16, y + 10))

def hit(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
    if distance < 27: return True
    return False

# Game Loop
while _running:
    screen.fill((0, 0, 0))
    screen.blit(bg_img, (0, 0))
    for evnt in pg.event.get():
        if evnt.type == pg.QUIT: _running = False

        # Checking the Key Stroke
        if evnt.type == pg.KEYDOWN:
            match evnt.key:
                case pg.K_LEFT: playerX_change = -1.75
                case pg.K_RIGHT: playerX_change = 1.75
                case pg.K_SPACE:
                    if not bullet_state:
                        pg.mixer.Sound('laser.wav').play()
                        bulletX = playerX
                        fire(bulletX, bulletY)
        if evnt.type == pg.KEYUP:
            if evnt.key == pg.K_LEFT or evnt.key == pg.K_RIGHT:
                playerX_change = 0

    # Player Changes
    playerX += playerX_change
    if playerX <= 0: playerX = 0
    elif playerX >= 736: playerX = 736
    player(playerX, playerY)

    # Bullet changes
    if bullet_state:
        fire(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= -32:
            bullet_state = False
            bulletY = 480

    # Enemy Changes
    for i in range(enemy_num):
        enemyX[i] += enemyX_change[i]

        # Movement of Enemey
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        # Condition of Game Over
        if enemyY[i] >= 440:
            for j in range(enemy_num): enemyY[j] = 1000
            game_over()
            break

        # Bullet hit the Enemy
        if hit(enemyX[i], enemyY[i], bulletX, bulletY):
            pg.mixer.Sound('explosion.wav').play()
            bullet_state = False
            bulletY = 480
            score_val += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(30, 180)

        enemy(enemyX[i], enemyY[i], i)

    getScore(fontX, fontY)
    pg.display.update()
