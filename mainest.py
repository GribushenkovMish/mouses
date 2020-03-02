# (C) mishgribushenkov

import main

game = main.Game()

level1 = main.Level(game, '1.png', '1.jpeg')
game.set_level(0)

player_sht = main.Spritesheet('player.png', 8, 4)
enemy_sht = main.Spritesheet('enemy.png', 8, 4)

player = main.Player(level1, 10, 10, st_velocity=4, delay=2)
player.add_animation('walk_right', player_sht, [0, 1, 2, 3, 4, 5, 6, 7])
player.add_animation('walk_left', player_sht, [16, 17, 18, 19, 20, 21, 22, 23])
player.add_animation('jump_right', player_sht, [24, 25])
player.add_animation('jump_left', player_sht, [8, 9])
player.add_animation('stay_right', player_sht, [11])
player.add_animation('stay_left', player_sht, [27])
player.add_animation('jump_right', player_sht, [8, 9])
player.add_animation('jump_left', player_sht, [24, 25])
player.add_animation('fall_right', player_sht, [10])
player.add_animation('fall_left', player_sht, [26])
player.add_animation('land_right', player_sht, [11, 12, 9])
player.add_animation('land_left', player_sht, [27, 28, 25])

player.set_animation('walk_right')
level1.sprites.add(player)

enemy = main.Enemy(level1, 200, 10, st_velocity=4, delay=2)
enemy.add_animation('walk_right', enemy_sht, [0, 1, 2, 3, 4, 5, 6, 7])
enemy.add_animation('walk_left', enemy_sht, [16, 17, 18, 19, 20, 21, 22, 23])
enemy.add_animation('jump_right', enemy_sht, [24, 25])
enemy.add_animation('jump_left', enemy_sht, [8, 9])
enemy.add_animation('stay_right', enemy_sht, [11])
enemy.add_animation('stay_left', enemy_sht, [27])
enemy.add_animation('jump_right', enemy_sht, [8, 9])
enemy.add_animation('jump_left', enemy_sht, [24, 25])
enemy.add_animation('fall_right', enemy_sht, [10])
enemy.add_animation('fall_left', enemy_sht, [26])
enemy.add_animation('land_right', enemy_sht, [11, 12, 9])
enemy.add_animation('land_left', enemy_sht, [27, 28, 25])

enemy.set_animation('walk_right')
level1.sprites.add(enemy)

game.menu()
