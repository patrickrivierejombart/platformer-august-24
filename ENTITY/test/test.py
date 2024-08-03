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
dt = 0

player_pos = [screen.get_width() / 2, screen.get_height() / 2]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")


    pygame.draw.circle(screen, "red", pygame.Vector2(player_pos[0], player_pos[1]), 40)
    pygame.draw.rect(screen, "gray", rect=[pygame.Vector2(0, screen.get_height()//5*4), pygame.Vector2(screen.get_width(), screen.get_height()//5)])

    lastY = player_pos[1]


    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player_pos[1] -= 300 * dt
    if keys[pygame.K_s]:
        player_pos[1] += 300 * dt
    if keys[pygame.K_q]:
        player_pos[0] -= 300 * dt
    if keys[pygame.K_d]:
        player_pos[0] += 300 * dt

    if player_pos[1]+40 >screen.get_height()//5*4:
        player_pos[1] = screen.get_height()//5*4-41

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()