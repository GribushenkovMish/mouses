import pygame
import os
from math import sin, cos, atan


WINDOW_HEIGHT = 599
WINDOW_WIDTH = 799
FRAMES_PER_SECOND = 45


def get_len(vector) -> float:
    """Длина вектора"""
    return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def normalize(vector) -> (float, float):
    """Приведение к единичной длине"""
    vec_len = get_len(vector)
    return (0, 0) if vec_len == 0 else (vector[0] / vec_len,
                                        vector[1] / vec_len)


def dot_product(vector1, vector2) -> float:
    """Скалярное произведение"""
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def vector_product_z(vector1, vector2) -> float:
    """Компонента Z векторного произведения"""
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]


def mult_vector_by_scal(vector, scal) -> (float, float):
    """Умножение вектора на число"""
    return vector[0] * scal, vector[1] * scal


class Spritesheet:
    def __init__(self, filename, width, height):
        self.images = []
        img = pygame.image.load(os.path.join('sprites', filename)).convert()
        x, y = img.get_width(), img.get_height()
        x1, y1 = x // width, y // height
        for i1 in range(height):
            for i in range(width):
                img1 = pygame.Surface((x1, y1)).convert()
                img1.blit(img, (0, 0), (x1 * i, y1 * i1, x1 * (i + 1), y1 * (i1 + 1)))
                img1.set_colorkey(img1.get_at((0, 0)))
                self.images.append(img1)

    def get_image(self, num):
        return self.images[num] if num in range(len(self.images) - 1) else None


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, delay=1):
        self.animations = {}
        self.frame = 0
        self.st_frame = 0
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.animations['none'] = [self.image]
        self.cur_animation_name = 'none'

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = x, y

        self.delay = delay
        self.d = 0

    def add_animation(self, name, spritesheet, order):
        self.animations[name] = [spritesheet.get_image(i) for i in order]

    def set_animation(self, name):
        if name not in self.animations.keys() or name == self.cur_animation_name:
            return
        self.cur_animation_name = name
        self.st_frame = len(self.animations[name]) - 1
        self.frame = 0

    def update(self, eventolist=None):
        self.d = self.d + 1 if self.d < self.delay else 0
        if self.d == 0:
            self.frame = self.frame + 1 if self.frame < self.st_frame else 0
            self.image = self.animations[self.cur_animation_name][self.frame]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        self.x, self.y = x, y
        self.rect.x = self.x
        self.rect.y = self.y


class Creature(AnimatedSprite):
    def __init__(self, level, x, y, st_velocity=10, jump_velocity=20, delay=5, height=20):
        super().__init__(x, y, delay)  # xydelay.
        self.level = level
        self.velocity = [0, 0]
        self.st_velocity = st_velocity  # Наибольшая скорость бега
        self.run_velocity = 0
        self.jump_velocity = jump_velocity
        self.height = height
        self.standing = False
        self.was_standing = False
        self.actions = {'walk_right': False, 'walk_left': False, 'jump': False}

    def update(self, eventolist=None):
        super().update()

        if self.run_velocity:
            self.run_velocity = self.run_velocity - 0.5 if self.run_velocity > 0\
                else self.run_velocity + 0.5
        if eventolist is not None:
            self.event_getter(eventolist)

        self.velocity[1] += self.level.gravity
        self.move(self.x + self.velocity[0] + self.run_velocity * self.get_walking_posib(),
                  self.y + self.velocity[1])

        self.update_standing()
        self.update_action()
        if not self.standing and self.was_standing:
            self.velocity[0] = self.run_velocity
            self.run_velocity = 0

        for i in self.level.sprites:
            if i == self:
                continue
            self.collider(i)
        for i in self.level.map_a:
            self.collider(i)

        self.was_standing = self.standing

    def event_getter(self, eventolist):
        pass

    def collider(self, obj):
        if not pygame.sprite.collide_mask(self, obj):
            return
        vec = normalize(self.velocity)
        if vec == (0, 0):
            vec = (0, 1)
        while pygame.sprite.collide_mask(self, obj):
            self.move(self.x - vec[0], self.y - vec[1])
        self.velocity = [0, 0]

    def walk_left(self):
        self.run_velocity = max(self.run_velocity - 2, -self.st_velocity)

    def walk_right(self):
        self.run_velocity = min(self.run_velocity + 2, self.st_velocity)

    def jump(self):
        self.velocity[1] -= self.jump_velocity
        self.move(self.x, self.y - 2)

    def update_action(self):
        if self.standing and (self.cur_animation_name not in ('land_right', 'land_left')
                              or self.frame == self.st_frame):
            if self.actions['walk_left'] == self.actions['walk_right']:
                if self.run_velocity > 0:
                    self.set_animation('stay_right')
                elif self.run_velocity < 0:
                    self.set_animation('stay_left')
                else:
                    self.set_animation('stay_right' if self.cur_animation_name in
                                       ('jump_right', 'walk_right', 'stay_right', 'fall_right', 'land_right')
                                                    else 'stay_left')
                self.run_velocity = 0
            elif self.actions['walk_right']:
                self.walk_right()
                self.set_animation('walk_right')
            elif self.actions['walk_left']:
                self.walk_left()
                self.set_animation('walk_left')
            if not self.was_standing:
                self.set_animation('land_right' if self.cur_animation_name in
                                               ('jump_right', 'walk_right', 'stay_right', 'fall_right')
                                   else 'land_left')
        if self.actions['jump'] and self.was_standing:
            self.set_animation('jump_right' if self.cur_animation_name
                                               in ('stay_right', 'walk_right',
                                                   'jump_right', 'fall_right')
                               else 'jump_left')
        if self.cur_animation_name in ('jump_right', 'jump_left')\
                and self.frame == self.st_frame and self.d == self.delay:
            self.set_animation('fall_right' if self.cur_animation_name == 'jump_right'
                               else 'fall_left')

    def get_walking_posib(self):
        pos0 = self.x, self.y
        num = 0
        self.move(self.x + self.run_velocity, self.y)
        while pygame.sprite.collide_mask(self, [i for i in self.level.map_a][0]):
            self.move(self.x, self.y - 1)
            num += 1
        self.move(*pos0)
        return (self.height - num) / self.height

    def update_standing(self):
        self.move(self.x, self.y + 3)
        if pygame.sprite.collide_mask(self, [i for i in self.level.map_a][0]):
            self.standing = True
        else:
            self.standing = False
        self.move(self.x, self.y - 3)


class Player(Creature):
    def __init__(self, level, x, y, st_velocity=10, jump_velocity=20, delay=5, height=20):
        super().__init__(level, x, y, st_velocity, jump_velocity, delay, height)

    def update(self, eventolist=None):
        super().update(eventolist)
        if WINDOW_WIDTH // 2 < self.x < self.level.width - WINDOW_WIDTH // 2:
            self.level.cam_pos[0] = self.x - WINDOW_WIDTH // 2
        if WINDOW_HEIGHT // 2 < self.y < self.level.height - WINDOW_HEIGHT // 2:
            self.level.cam_pos[1] = self.y - WINDOW_HEIGHT // 2

    def event_getter(self, eventolist):
        super().event_getter(eventolist)
        for i in eventolist:
            if i.type in (pygame.KEYDOWN, pygame.KEYUP):
                down = True if i.type == pygame.KEYDOWN else False
                i = i.key
                if i == pygame.K_LEFT:
                    self.actions['walk_left'] = down
                if i == pygame.K_RIGHT:
                    self.actions['walk_right'] = down
                if i == pygame.K_UP:
                    self.actions['jump'] = down
                    if down and self.standing:
                        self.jump()


class Enemy(Creature):
    def __init__(self, level, x, y, st_velocity=10, jump_velocity=20, delay=5, height=20, walk_distance=120):
        super().__init__(level, x, y, st_velocity, jump_velocity, delay, height)
        self.walk_distance = walk_distance
        self.turn_timer = self.walk_distance  # Кадры до поворота
        self.actions['walk_right'] = True

    def update(self, eventolist=None):
        super().update(eventolist)
        if self.turn_timer:
            self.turn_timer -= 1
        else:
            self.turn_timer = self.walk_distance
            self.actions['walk_right'] = not self.actions['walk_right']
            self.actions['walk_left'] = not self.actions['walk_left']



class Gun(AnimatedSprite):
    def __init__(self, anchor, x1, y1):
        super().__init__(anchor.x + x1, anchor.y + y1)
        self.anchor, self.x1, self.y1 = anchor, x1, y1


class Bullet(AnimatedSprite):
    def __init__(self, x, y, image, velocity=(5, 4)):
        self.velocity = list(velocity)
        super().__init__(x, y)
        self.prepare_sprites(image)

    def prepare_sprites(self, image):
        sprites = []
        for angl in range(0, 360, 2):
            angl *= 0.01745

