import pygame
import math
import pygame_gui
from random import randint, choice
import sys
import os
from datetime import datetime
import sqlite3

start_time = datetime.now()

FPS = 50

pygame.init()
size = WIDTH, HEIGHT = 700, 1000
score = 0
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
field = [[0] * 10 for i in range(10)]

LEVELS = ['Легко', 'Средне', 'Сложно', 'Ввести количество шаров']
MODES = ['На время', 'Бесконечный']
TIME = 120


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def final_screen():
    global score
    score = 0
    screen.fill('black')
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    go_to_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 125, 300), (250, 75)),
                                               text='Вернуться к началу игры',
                                               manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 125, 380), (250, 75)),
                                               text='Выйти из игры',
                                               manager=manager)
    con = sqlite3.connect('my_tries.sql.db')
    cur = con.cursor()
    scores = cur.execute('''SELECT score from information''').fetchall()
    print(scores)
    max_scores = []
    for i in scores:
        max_scores.append(*i)
    max_score = max(max_scores)
    font = pygame.font.Font(None, 20)
    text = font.render(f"Максимальное количество набранных очков: {max_score}", True, (100, 255, 100))
    text_x = 10
    text_y = 50
    screen.blit(text, (text_x, text_y))
    count = cur.execute('''SELECT COUNT (*) from information''').fetchone()[0]
    text_1 = font.render(f"Вы сделали {count} попыток", True, (100, 255, 100))
    text_x1 = 10
    text_y1 = 100
    screen.blit(text_1, (text_x1, text_y1))
    pygame.display.flip()
    time_delta = clock.tick(FPS) / 1000.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == go_to_start:
                    go_to_start.kill()
                    exit_button.kill()
                    return start_screen()
                elif event.ui_element == exit_button:
                    terminate()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    global start_time
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 300), (150, 75)),
                                                text='Начать игру',
                                                manager=manager)
    cnt_mode = 0
    mode_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 380), (150, 75)),
                                               text=MODES[cnt_mode],
                                               manager=manager)
    cnt_level = 0
    level_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 75, 460), (150, 75)),
                                                text=LEVELS[cnt_level],
                                                manager=manager)
    inp_cnt_balls = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH // 2 + 80, 460), (150, 75)),
                                                        manager=manager)
    time_delta = clock.tick(FPS) / 1000.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    start_time = datetime.now()
                    start_button.kill()
                    level_button.kill()
                    mode_button.kill()
                    inp_cnt_balls.kill()
                    try:
                        if cnt_level == 3:
                            return MODES[cnt_mode], LEVELS[cnt_level], int(inp_cnt_balls.get_text())
                        else:
                            return MODES[cnt_mode], LEVELS[cnt_level], inp_cnt_balls.get_text()
                    except ValueError:
                        print('Целое неотрицательное количество шаров')
                        terminate()
                if event.ui_element == mode_button:
                    cnt_mode += 1
                    cnt_mode %= len(MODES)
                    mode_button.set_text(MODES[cnt_mode])
                if event.ui_element == level_button:
                    cnt_level += 1
                    cnt_level %= len(LEVELS)
                    level_button.set_text(LEVELS[cnt_level])
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():
    global start_time
    delta_time = (datetime.now() - start_time)
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 125, 300), (250, 75)),
                                               text='Выйти из игры',
                                               manager=manager)
    return_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 125, 380), (250, 75)),
                                                 text='Вернуться к игре',
                                                 manager=manager)
    go_to_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 125, 460), (250, 75)),
                                               text='Вернуться к началу игры',
                                               manager=manager)
    time_delta = clock.tick(FPS) / 1000.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == return_button:
                    exit_button.kill()
                    return_button.kill()
                    go_to_start.kill()
                    start_time = datetime.now() - delta_time
                    player.reset()
                    return
                elif event.ui_element == exit_button:
                    terminate()
                elif event.ui_element == go_to_start:
                    go_to_start.kill()
                    return_button.kill()
                    exit_button.kill()
                    player.reset()
                    return start_screen()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = pygame.transform.scale(load_image('bucket.png', -1), (50, 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(100, 800)
        self.move_left = 0
        self.move_right = 0

    def reset(self, reset_pos=False):
        self.move_left = 0
        self.move_right = 0
        if reset_pos:
            self.rect = self.image.get_rect().move(100, 800)

    def update(self, *args):
        if args and args[0] == 'move':
            past_rect = self.rect.copy()
            if self.move_left and self.rect.x >= 3:
                self.rect.x -= 3
            if self.move_right and self.rect.x + self.rect.width + 3 <= WIDTH:
                self.rect.x += 3
            tmp = pygame.sprite.spritecollide(player, all_sprites, collided=pygame.sprite.collide_mask, dokill=False)
            if tmp:
                if self.rect != past_rect:
                    self.rect = past_rect
                elif not player.rect.y > tmp[0].rect.y:
                    if tmp[0].rect.x < player.rect.x:
                        self.rect.x += 3
                    else:
                        self.rect.x -= 3
                    if self.rect.x < 0 or self.rect.x + self.rect.width > WIDTH:
                        self.rect = past_rect
            return
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_LEFT:
                self.move_left = 1
            if args[0].key == pygame.K_RIGHT:
                self.move_right = 1
        if args and args[0].type == pygame.KEYUP:
            if args[0].key == pygame.K_LEFT:
                self.move_left = 0
            if args[0].key == pygame.K_RIGHT:
                self.move_right = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.radius = randint(10, 20)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        colors = ['red', 'green', 'blue', 'pink', 'silver',
                  'gold', 'brown', 'yellow']
        pygame.draw.circle(self.image, pygame.Color(choice(colors)),
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect().move(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.vy = 0
        self.vx = 0
        self.rect.x = randint(0, WIDTH - self.radius)
        while self.vy <= 1.00001 or self.vx <= 1.000001:
            self.v = randint(8, 40) / 4
            self.angle = (randint(10, 170)) / 180 * math.pi
            self.vx = self.v * math.cos(self.angle)
            self.vy = self.v * math.sin(self.angle)

    def update(self, *args):
        global score
        if args and args[0] == 'move':
            if not pygame.sprite.collide_mask(self, player):
                if (self.rect.x <= 0 and self.vx < 0) or \
                        (self.rect.x + 2 * self.radius >= WIDTH and self.vx > 0):
                    self.vx *= -1
                if self.rect.y >= HEIGHT:
                    all_sprites.remove(self)
                    return
                self.rect.y += self.vy
                self.rect.x += self.vx
            else:
                if player.rect.x - self.rect.x > self.radius:
                    if self.vx > 0:
                        self.vx *= -1
                    self.rect.x += self.vx
                    self.rect.y += self.vy
                elif (player.rect.x + player.rect.width) - self.rect.x < self.radius:
                    if self.vx < 0:
                        self.vx *= -1
                    self.rect.x += self.vx
                    self.rect.y += self.vy
                elif self.rect.y < player.rect.y:
                    score += (abs(self.vx) + abs(self.vy)) / (self.radius / 10)
                    score = round(score, 2)
                    all_sprites.remove(self)


def draw(screen):
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(score), True, (100, 255, 100))
    screen.blit(text, (0, 0))
    if mode == 'На время':
        text = font.render(str(TIME - (datetime.now() - start_time).seconds), True, (100, 255, 100))
        screen.blit(text, (WIDTH - text.get_width(), 0))


def how_much_balls(level, player_cnt_balls):
    if level == LEVELS[0]:
        return 2
    elif level == LEVELS[1]:
        return 5
    elif level == LEVELS[2]:
        return 10
    elif level == LEVELS[3]:
        return player_cnt_balls


mode, level, cnt = start_screen()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = Player()

fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

cnt_balls = how_much_balls(level, cnt)

while len(all_sprites) < cnt_balls:
    Ball()

pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 50, 0), (100, 40)),
                                            text='Пауза',
                                            manager=manager)
time_delta = clock.tick(FPS) / 1000.0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == pause_button:
                pause_button.kill()
                tmp = pause_screen()
                if tmp is not None:
                    mode, level, cnt_balls_tmp = tmp
                    cnt_balls = how_much_balls(level, cnt_balls_tmp)
                    for i in all_sprites:
                        all_sprites.remove(i)
                pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 50, 0), (100, 40)),
                                                            text='Пауза',
                                                            manager=manager)
        all_sprites.update(event)
        player_group.update(event)
        manager.process_events(event)
    all_sprites.update('move')
    player_group.update('move')
    draw(screen)
    all_sprites.draw(screen)
    player_group.draw(screen)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()
    while len(all_sprites) < cnt_balls:
        Ball()
    clock.tick(FPS)
    if mode == 'На время' and (datetime.now() - start_time).seconds >= TIME:
        con = sqlite3.connect('my_tries.sql.db')
        cur = con.cursor()
        cur.execute('''INSERT INTO information(level, mode, score) VALUES (1, 1, ?)''', (score,))
        con.commit()
        con.close()
        pause_button.kill()
        mode, level, cnt_balls_tmp = final_screen()
        cnt_balls = how_much_balls(level, cnt_balls_tmp)
        for i in all_sprites:
            all_sprites.remove(i)
        pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH // 2 - 50, 0), (100, 40)),
                                                    text='Пауза',
                                                    manager=manager)
        player.reset(True)
