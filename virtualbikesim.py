import pygame
import sys

# Initialize pygame
pygame.init()

# Create window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")

clock = pygame.time.Clock()

# ====== PLAYER SETUP ======
player_x = 100
player_y = 100
player_size = 50
player_color = (0, 255, 0)

dx, dy = 0, 0   # velocity

# Obstacles
obstacles = [
    pygame.Rect(300, 200, 100, 50),
    pygame.Rect(500, 400, 150, 30),
    pygame.Rect(150, 350, 60, 120)
]

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000  # seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ====== INPUT ======
    ax, ay = 0, 0
    speed = 800  # acceleration strength

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ax = -speed
    if keys[pygame.K_RIGHT]:
        ax = speed
    if keys[pygame.K_UP]:
        ay = -speed
    if keys[pygame.K_DOWN]:
        ay = speed

    # ====== PHYSICS ======
    dx += ax * dt
    dy += ay * dt

    friction = 0.05
    dx = dx - friction*dx
    dy = dy - friction*dy

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # ---- X AXIS ----
    player_rect.x += dx * dt
    bounce = 0.7
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            if dx > 0:
                player_rect.right = obstacle.left
                dx = -dx*bounce
            elif dx < 0:
                player_rect.left = obstacle.right
            dx = -dx*bounce

    # ---- Y AXIS ----
    player_rect.y += dy * dt
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            if dy > 0:
                player_rect.bottom = obstacle.top
                dy = -dy*bounce
            elif dy < 0:
                player_rect.top = obstacle.bottom
            dy = -dy*bounce

    player_x, player_y = player_rect.x, player_rect.y

    # ====== CLAMP TO SCREEN ======
    player_x = max(0, min(player_x, width - player_size))
    player_y = max(0, min(player_y, height - player_size))

    # ====== DRAW ======
    screen.fill((30, 30, 30))

    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)

    pygame.display.flip()

# Quit properly
pygame.quit()
sys.exit()