### DISPLAY VARIABLES ###
# Ratio and size
WIDTH, HEIGHT = 1920, 1080
CHARACTER_DISPLAY_WIDTH, CHARACTER_DISPLAY_HEIGHT = 384, 216  # MAIN DISPLAY : character and tiles have the same size 384, 216
TILE_SIZE = 32
# Character sizes
PLAYER_SIZE_X = 32
PLAYER_SIZE_Y = 32

### GAME PACE ###
# Game pace (around 1/60)
DT = 0.016

### GAME PHYSICS ###
# Environment forces
GRAVITY = 25 * TILE_SIZE  # 1500
# Player movement speed (by default)
PLAYER_JUMP_SPEED = 8 * TILE_SIZE  # 500
PLAYER_WALK_SPEED = 1.75 * TILE_SIZE  # 1.35 m/s

### CHARACTERS ###
# Player Controls
PLAYER_JUMP = "space"
PLAYER_WALK_RIGHT = "right"
PLAYER_WALK_LEFT = "left"
STOP_PLAYER_JUMP = "no_space"
STOP_PLAYER_WALK_RIGHT = "no_right"
STOP_PLAYER_WALK_LEFT = "no_left"
# Game calculus delay
CHARACTER_STATUS_DELAY = 10
