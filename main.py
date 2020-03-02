# (C) mishgribushenkov
from stuff import *


class Level:
    def __init__(self, game, map_filename, background_filename):
        self.game = game
        self.width = 0
        self.height = 0
        self.img = None
        self.background = None
        self.set_background(background_filename)
        self.map_a = None
        self.colorkey = None
        self.set_map(map_filename)

        self.sprites = pygame.sprite.Group()
        self.player = None
        self.cam_pos = [0, 0]
        self.game.levels.append(self)

        self.gravity = 1

    def set_map(self, map_filename):
        path = os.path.join('levels', map_filename)
        img = pygame.image.load(path).convert()
        img.set_colorkey(img.get_at((2, 2)))
        self.width = img.get_width()
        self.height = img.get_height()
        map_k = pygame.sprite.Sprite()
        map_k.image = img
        map_k.rect = img.get_rect()
        map_k.mask = pygame.mask.from_surface(img)
        self.map_a = pygame.sprite.Group(map_k)
        self.img = pygame.Surface((self.width, self.height)).convert()
        self.colorkey = img.get_at((1, 1))
        self.game.canvas.set_colorkey(self.colorkey)

    def set_background(self, background_filename):
        path = os.path.join('backgrounds', background_filename)
        self.background = pygame.image.load(path).convert()

    def draw(self):
        self.game.canvas.blit(self.img, (0, 0), (self.cam_pos[0], self.cam_pos[1],
                                                 WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, eventolist):
        self.sprites.update(eventolist)
        self.img.fill((0, 1, 1))
        self.img.blit(self.background, (self.cam_pos[0], self.cam_pos[1]))
        self.map_a.draw(self.img)
        self.sprites.draw(self.img)


class Game:
    def __init__(self):
        self.levels = []
        self.current_level = None

        self.continues = True
        self.exit = False
        self.timer = pygame.time.Clock()

        pygame.init()
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.menu_sprites = pygame.sprite.Group()
        self.btn_start, self.btn_exit = AnimatedSprite(300, 200), AnimatedSprite(300, 400)
        self.init_menu()

    def init_menu(self):
        background = pygame.sprite.Sprite(self.menu_sprites)
        background.image = pygame.Surface((799, 599))  # pygame.image.load()
        background.rect = background.image.get_rect()

        btn_start_sht = Spritesheet('btn_start.png', 2, 1)
        btn_exit_sht = Spritesheet('btn_exit.png', 2, 1)
        self.btn_start.add_animation('not_pressed', btn_start_sht, [0])
        self.btn_start.add_animation('pressed', btn_start_sht, [1])
        self.btn_exit.add_animation('not_pressed', btn_exit_sht, [0])
        self.btn_exit.add_animation('pressed', btn_exit_sht, [1])
        self.btn_start.set_animation('not_pressed')
        self.btn_exit.set_animation('not_pressed')

        self.menu_sprites.add(self.btn_start)
        self.menu_sprites.add(self.btn_exit)

    def menu(self):
        self.exit = False
        self.continues = True
        while self.continues:
            eventolist = self.proc_events()
            for i in eventolist:
                if i.type == pygame.MOUSEBUTTONDOWN:
                    m_pos = pygame.mouse.get_pos()
                    if self.btn_start.rect.collidepoint(m_pos):
                        self.continues = False
                    elif self.btn_exit.rect.collidepoint(m_pos):
                        self.continues = False
                        self.exit = True

            self.menu_sprites.update()
            self.btn_start.move(self.btn_start.x, self.btn_start.y)
            self.btn_exit.move(self.btn_exit.x, self.btn_exit.y)

            self.canvas.fill((0, 0, 0))
            self.menu_sprites.draw(self.canvas)

            pygame.display.flip()
        if not self.exit:
            self.main()

    def main(self):
        self.continues = True
        while self.continues:
            eventolist = self.proc_events()
            if self.current_level is not None:
                self.current_level.update(eventolist)
                self.current_level.draw()
                pygame.display.flip()
            self.timer.tick(FRAMES_PER_SECOND)

    def proc_events(self):
        eventolist = pygame.event.get()
        for little_event in eventolist:
            if little_event.type == pygame.QUIT:
                self.continues = False
        return eventolist

    def set_level(self, num):
        self.current_level = self.levels[num]
