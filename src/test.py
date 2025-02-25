import pygame
import top_down

"ПРИВЕТ"
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

image_size = (300, 800)
point_on_image = (130, 40)
player_width, player_height = top_down.move_set[1].get_size()
player_surf = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
player_surf.blit(top_down.move_set[0], (0, 0))
player_surf.blit(top_down.move_set[1], (0, 0))
player_surf.blit(top_down.move_set[2], (0, 0))
# pygame.draw.ellipse(image, "gray", (0, 0, *image_size))
# pygame.draw.circle(image, "red", point_on_image, 10)
angle = 0

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen_center = screen.get_rect().center
    rotated_player = pygame.transform.rotate(player_surf, angle)

    px = screen_center[0] - image_size[0] // 2 + point_on_image[0]
    py = screen_center[1] - image_size[1] // 2 + point_on_image[1]
    point = pygame.math.Vector2(px, py)
    pivot = pygame.math.Vector2(screen_center)
    rotated_point = (point - pivot).rotate(-angle) + pivot

    screen.fill("white")
    screen.blit(rotated_player, rotated_player.get_rect(center=screen_center))
    pygame.draw.line(screen, "blue", (screen_center[0] - 15, screen_center[1]),
                     (screen_center[0] + 15, screen_center[1]), 3)
    pygame.draw.line(screen, "blue", (screen_center[0], screen_center[1] - 15),
                     (screen_center[0], screen_center[1] + 15), 3)
    pygame.draw.line(screen, "green", (rotated_point[0] - 15, rotated_point[1]),
                     (rotated_point[0] + 15, rotated_point[1]), 3)
    pygame.draw.line(screen, "green", (rotated_point[0], rotated_point[1] - 15),
                     (rotated_point[0], rotated_point[1] + 15), 3)
    pygame.draw.line(screen, "blue", screen_center, rotated_point, 3)
    pygame.display.flip()

    angle += 1

pygame.quit()
exit()