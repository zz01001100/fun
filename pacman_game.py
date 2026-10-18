
import random
import pygame
from collections import deque

pygame.init()

# SETUP -------------------------------------------------------------------

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Ecosystem")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)
small_font = pygame.font.SysFont(None, 19)
title_font = pygame.font.SysFont(None, 32)

BLACK = (15, 15, 30)
PANEL = (28, 30, 50)
WHITE = (240, 240, 245)
YELLOW = (255, 220, 0)
BLUE = (65, 170, 255)
RED = (245, 75, 85)
GREEN = (80, 220, 140)
GREY = (140, 145, 165)

GAME_WIDTH = 650

# MODEL -------------------------------------------------------------------

pacman = pygame.Vector2(GAME_WIDTH / 2, HEIGHT / 2)
pacman_alive = True
respawn_timer = 0

ghosts = [
    pygame.Vector2(
        random.randint(20, GAME_WIDTH - 20),
        random.randint(100, HEIGHT - 20)
    )
    for _ in range(8)
]

speed = 3
ghost_speed = 1.2
max_ghosts = 80
death_threshold = 30

# STATISTICS ---------------------------------------------------------------

ghosts_eaten = 0
deaths = 0
elapsed_frames = 0
current_life_frames = 0
longest_life = 0

history = deque(maxlen=150)
history.append(len(ghosts))

# MAIN LOOP ----------------------------------------------------------------

running = True

while running:
    clock.tick(60)
    elapsed_frames += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # PAC-MAN MOVEMENT ------------------------------------------------------
    if pacman_alive:
        if keys[pygame.K_LEFT]:
            pacman.x -= speed
        if keys[pygame.K_RIGHT]:
            pacman.x += speed
        if keys[pygame.K_UP]:
            pacman.y -= speed
        if keys[pygame.K_DOWN]:
            pacman.y += speed

        pacman.x = max(15, min(GAME_WIDTH - 15, pacman.x))
        pacman.y = max(80, min(HEIGHT - 15, pacman.y))

        current_life_frames += 1

    # GHOST REPRODUCTION ----------------------------------------------------
    if ghosts and len(ghosts) < max_ghosts:
        if random.random() < 0.025:
            parent = random.choice(ghosts)

            new_ghost = parent + pygame.Vector2(
                random.randint(-30, 30),
                random.randint(-30, 30)
            )

            new_ghost.x = max(15, min(GAME_WIDTH - 15, new_ghost.x))
            new_ghost.y = max(80, min(HEIGHT - 15, new_ghost.y))

            ghosts.append(new_ghost)

    # GHOST MOVEMENT --------------------------------------------------------
    if pacman_alive:
        for ghost in ghosts:
            direction = pacman - ghost

            if direction.length() > 0:
                ghost += direction.normalize() * ghost_speed

    # PAC-MAN EATS GHOSTS ---------------------------------------------------
    if pacman_alive:
        survivors = []

        for ghost in ghosts:
            if ghost.distance_to(pacman) < 23:
                ghosts_eaten += 1
            else:
                survivors.append(ghost)

        ghosts = survivors

    # PAC-MAN DEATH ---------------------------------------------------------
    if pacman_alive and len(ghosts) >= death_threshold:
        pacman_alive = False
        respawn_timer = 180
        deaths += 1
        longest_life = max(longest_life, current_life_frames)
        current_life_frames = 0

    # RESPAWN ---------------------------------------------------------------
    if not pacman_alive:
        respawn_timer -= 1

        if respawn_timer <= 0:
            pacman_alive = True
            pacman.update(GAME_WIDTH / 2, HEIGHT / 2)

    # STORE HISTORY ---------------------------------------------------------
    if elapsed_frames % 6 == 0:
        history.append(len(ghosts))

    # DRAW GAME -------------------------------------------------------------
    screen.fill(BLACK)

    pygame.draw.rect(
        screen, PANEL,
        (GAME_WIDTH, 0, WIDTH - GAME_WIDTH, HEIGHT)
    )

    pygame.draw.line(
        screen, GREY,
        (GAME_WIDTH, 0), (GAME_WIDTH, HEIGHT), 2
    )

    for ghost in ghosts:
        pygame.draw.circle(
            screen, BLUE,
            (int(ghost.x), int(ghost.y)), 10
        )

    if pacman_alive:
        pygame.draw.circle(
            screen, YELLOW,
            (int(pacman.x), int(pacman.y)), 14
        )
    else:
        text = font.render("PAC-MAN RESPAWNING", True, RED)
        screen.blit(text, (150, HEIGHT // 2))

    # DASHBOARD -------------------------------------------------------------
    x = GAME_WIDTH + 20
    y = 20

    screen.blit(title_font.render("ECOSYSTEM", True, WHITE), (x, y))
    y += 45

    stats = [
        ("Ghost population", len(ghosts), BLUE),
        ("Ghosts eaten", ghosts_eaten, GREEN),
        ("Pac-Man deaths", deaths, RED),
        ("Alive now", "YES" if pacman_alive else "NO",
         GREEN if pacman_alive else RED),
        ("Current life (sec)", f"{current_life_frames / 60:.1f}", YELLOW),
        ("Longest life (sec)", f"{longest_life / 60:.1f}", WHITE),
        ("Simulation time", f"{elapsed_frames / 60:.1f} s", WHITE),
    ]

    for label, value, color in stats:
        screen.blit(small_font.render(label, True, GREY), (x, y))
        screen.blit(font.render(str(value), True, color), (x, y + 20))
        y += 52

    # POPULATION CHART ------------------------------------------------------
    y += 5
    screen.blit(font.render("Ghost population history", True, WHITE), (x, y))
    y += 30

    chart_width = WIDTH - x - 20
    chart_height = 130

    pygame.draw.rect(
        screen, BLACK,
        (x, y, chart_width, chart_height)
    )

    pygame.draw.line(
        screen, GREY,
        (x, y + chart_height),
        (x + chart_width, y + chart_height), 1
    )

    if len(history) > 1:
        max_value = max(max(history), death_threshold, 1)

        points = []
        for i, value in enumerate(history):
            px = x + i * chart_width / (len(history) - 1)
            py = y + chart_height - (value / max_value) * chart_height
            points.append((int(px), int(py)))

        pygame.draw.lines(screen, BLUE, False, points, 2)

        threshold_y = y + chart_height - (
            death_threshold / max_value
        ) * chart_height

        pygame.draw.line(
            screen, RED,
            (x, int(threshold_y)),
            (x + chart_width, int(threshold_y)), 1
        )

    screen.blit(
        small_font.render("Red line = death threshold", True, GREY),
        (x, y + chart_height + 8)
    )

    pygame.display.flip()

pygame.quit()
