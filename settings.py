WIDTH, HEIGHT = 1920, 1080
tile_size = 16
player_size_x = 12
player_size_y = 30
BG_IMG = 'assets/textures/terrain/bg.jpg'
# Game pace
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
