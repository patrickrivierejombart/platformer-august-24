# Ratio and size
WIDTH, HEIGHT = 1920, 1080
TILE_DISPLAY_WIDTH, TILE_DISPLAY_HEIGHT = 480, 270
CHARACTER_DISPLAY_WIDTH, CHARACTER_DISPLAY_HEIGHT = 960, 540
tile_size = 16
player_size_x = 32
player_size_y = 32
tile_to_character_ratio = 2

# Game pace (around 1/60)
dt = 0.016

# Environment forces
gravity = 25 * tile_size  # 1500

# Player Controls
PLAYER_JUMP = "space"
PLAYER_WALK_RIGHT = "right"
PLAYER_WALK_LEFT = "left"

STOP_PLAYER_JUMP = "no_space"
STOP_PLAYER_WALK_RIGHT = "no_right"
STOP_PLAYER_WALK_LEFT = "no_left"

# Player movement speed
player_jump_speed = 8 * tile_size  # 500
player_walk_speed = 1.35 * tile_size  # 1.35 m/s
