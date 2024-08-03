import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entity
# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
# delta time
dt = 0

# Create an entity named "player" using the "Entity" class
player = entity.Entity(100, 4, [20, 40], [screen.get_width() / 2, 0])

while running:
    # Check when the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing
    screen.fill("purple")
    pygame.draw.rect(screen, "gray", rect=[pygame.Vector2(0, screen.get_height()//5*4), pygame.Vector2(screen.get_width(), screen.get_height()//5)])
    pygame.draw.circle(screen, "red", pygame.Vector2(player.pos[0], player.pos[1]), 40)

    # Check keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.direction.left()
        player.go_forward(300 * dt)
    if keys[pygame.K_d]:
        player.direction.right()
        player.go_forward(300 * dt)

    # Check collisions
    if player.is_in_object( (player.pos[0], player.pos[1]+player.object_size[1]) , (player.pos[0], (screen.get_height()//5*4)) ):
        player.pos[1] += abs(screen.get_height()//5*4-player.object_size[1]-player.pos[1])*30 * dt
    else:
        player.pos[1] += 300*dt

    # Showing
    pygame.display.flip()

    dt = clock.tick(60) / 1000

# Close the drawings :(
pygame.quit()