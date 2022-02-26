import pygame
import pygame_gui
from random import randint
import sys
import os

FPS = 50

pygame.init()
size = WIDTH, HEIGHT = 700, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
field = [[0] * 10 for i in range(10)]


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

def show_statistic():
    pass

def start_screen():

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((342, 300), (150, 75)),
                                                text='Начать игру',
                                                manager=manager)
    # statistic_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((342, 400), (150, 75)),
    #                                             text='Статистика',
    #                                             manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
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

    def update(self, *args):
        if args and args[0] == 'move':
            if self.move_left:
                self.rect.x -= 3
            if self.move_right:
                self.rect.x += 3
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
        self.radius = 15
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect().move(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.vx = randint(-4, 4)
        self.vy = randint(1, 4)

    def update(self, *args):
        if args and args[0] == 'move':
            if not pygame.sprite.collide_mask(self, player):
                if (self.rect.x <= 0 and self.vx < 0) or\
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
                elif self.rect.x - player.rect.x - player.rect.width > self.radius:
                    if self.vx < 0:
                        self.vx *= -1
                    self.rect.x += self.vx
                    self.rect.y += self.vy


def draw(screen):
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))


start_screen()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = Player()
Ball()

fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        all_sprites.update(event)
        player_group.update(event)
    all_sprites.update('move')
    player_group.update('move')
    draw(screen)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    if len(all_sprites) == 0:
        Ball()
    clock.tick(FPS)