from pygame import *
from random import randint
import sys
import os

#! про превращение в .exe файл
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#! ========================================================

win_width, win_height = 1000, 800
window = display.set_mode((win_width, win_height))
display.set_caption("Out of Sight v1.0.1")
display.set_icon(image.load(resource_path("icon_eye.png")))

clock = time.Clock()

ASTERIOD_SPRITE = resource_path("asteroid.png")
BACKGROUND_SPRITE = resource_path("hellworld.jpg")
PLAYER_SPRITE = resource_path("arrow.png")
ENEMY_SPRITE = resource_path("eye.png")
ERROR_ENEMY_SPRITE = resource_path("error_eye.png")

mixer.init()
mixer.music.load(resource_path("music.mp3"))
mixer.music.play()
mixer.music.set_volume(0.750)

font.init()
main_font = font.SysFont("Arial", 45, True, False)
stats_font = font.SysFont("Arial", 31, True, False)
win_text = main_font.render("Good Job", True, (0, 200, 0))
lose_text = main_font.render("Loser XD", True, (0, 200, 0))

#! КЛАССЫ =========================================================

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()

        self.image = transform.smoothscale(
            image.load(img), 
            (w, h)
        )

        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[K_d] or keys[K_RIGHT]:
            if self.rect.x < win_width - self.image.get_width():
                self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        global hp, timer
        self.rect.y += self.speed
        if sprite.collide_rect(self, player):
            hp -= 5
            self.kill()

class Enemy2(GameSprite):
    def update(self):
        global hp, timer
        self.rect.y += self.speed
        if sprite.collide_rect(self, player):
            hp -= 50
            self.kill()

# ! КонецКлассов =========================================================

FPS = 144 #! 1 секунда = 144 тиков
GAME_RUN = True
GAME_FINISHED = False

seconds, timer, hp = 0, 0, 60
spawnrate_delay = FPS * 2
spawnrate_enemy = spawnrate_delay
spawnrate_enemy2 = spawnrate_delay

background = GameSprite(BACKGROUND_SPRITE, 0, 0, win_width, win_height, 0)
player = Player(PLAYER_SPRITE, win_width / 2, win_height - 150, 75, 75, 7)

enemys_group = sprite.Group()

#! ИГРОВОЙ ЦИКЛ ================================================================

while GAME_RUN:

    for ev in event.get():
        if ev.type == QUIT:
            GAME_RUN = False

    if not GAME_FINISHED:

        score_text = stats_font.render("Time: " + str(timer), True, (255, 255, 255))
        lost_text = stats_font.render("Health: " + str(hp), True, (255, 255, 255))

        if spawnrate_enemy < 0:
            enemy = Enemy(resource_path("eye.png"), randint(64, win_width - 64), -64, 100, 100, randint(5, 10))
            enemys_group.add(enemy)
            if spawnrate_delay > FPS * 1:
                spawnrate_delay -= 10
            spawnrate_enemy = spawnrate_delay
        else:
            spawnrate_enemy -= 5

        if spawnrate_enemy2 < 0:
            enemy2 = Enemy2(resource_path("error_eye.png"), randint(64, win_width - 64), -64, 100, 100, randint(10, 15))
            enemys_group.add(enemy2)
            if spawnrate_delay > FPS * 1:
                spawnrate_delay -= 10
            spawnrate_enemy2 = spawnrate_delay
        else:
            spawnrate_enemy2 -= 1

    if FPS == 144:
        seconds += 1
        if seconds == 144:
            timer += 1
            seconds = 0

        background.reset()
        player.reset()
        enemys_group.draw(window)

        player.update()
        enemys_group.update()

        window.blit(score_text, (5, 5))
        window.blit(lost_text, (5, score_text.get_height() + 5))

        #! Если таймер равен 180 секундам
        if timer == 180:
            score_text = stats_font.render("Time: " + str(timer), True, (255, 255, 255))
            end_screen = main_font.render("Great... I think you can go back to your home...", True, (255, 255, 255))
            window.blit(end_screen, (win_width / 2 - end_screen.get_width() / 2, win_height / 2 ))
            GAME_FINISHED = True
        #! =====================================================================================
        
        #! Если здоровье равно 0 или меньше 0
        if hp == 0 :
            lost_text = stats_font.render("Health: " + str(hp), True, (255, 255, 255))
            mixer.music.stop()
            end_screen = main_font.render("Welcome to hell...My new toy", True, (255, 255, 255))
            window.blit(end_screen, (win_width / 2 - end_screen.get_width() / 2, win_height / 2))
            GAME_FINISHED = True
        elif hp <= 0:
            lost_text = stats_font.render("Health: " + str(hp), True, (255, 255, 255))
            mixer.music.stop()
            end_screen = main_font.render("Welcome to hell...My new toy", True, (255, 255, 255))
            window.blit(end_screen, (win_width / 2 - end_screen.get_width() / 2, win_height / 2))
            GAME_FINISHED = True
        #! ======================================================================================

        display.update()

    clock.tick(FPS)