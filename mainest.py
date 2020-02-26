# (C) mishgribushenkov

import main

game = main.Game()

level1 = main.Level(game, '1.png', '1.jpeg')
game.set_level(0)

sprtsht1 = main.Spritesheet('7OP3Z.png', 8, 4)

sprt1 = main.Player(level1, 10, 10, st_velocity=4, delay=2)
sprt1.add_animation('walk_right', sprtsht1, [0, 1, 2, 3, 4, 5, 6, 7])
sprt1.add_animation('walk_left', sprtsht1, [16, 17, 18, 19, 20, 21, 22, 23])
sprt1.add_animation('jump_right', sprtsht1, [24, 25])
sprt1.add_animation('jump_left', sprtsht1, [8, 9])
sprt1.add_animation('stay_right', sprtsht1, [10])
sprt1.add_animation('stay_left', sprtsht1, [26])
sprt1.add_animation('jump_right', sprtsht1, [8, 9])
sprt1.add_animation('jump_left', sprtsht1, [24, 25])
sprt1.add_animation('fall_right', sprtsht1, [10])
sprt1.add_animation('fall_left', sprtsht1, [26])
sprt1.add_animation('land_right', sprtsht1, [11, 12, 9])
sprt1.add_animation('land_left', sprtsht1, [27, 28, 25])


sprt1.set_animation('walk_right')
level1.sprites.add(sprt1)

game.main()
