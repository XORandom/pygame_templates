"""Простой пример обработки столкновений"""

from random import randint

import pygame

pygame.init()
pygame.mixer.init()
# Создание окна
WIDTH = 1000
"Ширина окна игры"
HEIGHT = 1000
"Высота окна игры"

font_text = pygame.font.SysFont("monospace", 30)
"Шрифт для текста"

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна игры с параметрами ширины и высоты окна
pygame.display.set_caption("Collision")  # Название нашей игры

# Квадрат 1
object1_width = 50
object1_height = 50
object1 = pygame.surface.Surface((object1_width, object1_height))
object1_x = WIDTH // 2 - object1_width
object1_y = HEIGHT - 116
object1_rect = pygame.Rect(object1_x, object1_y, object1_width, object1_height)
object1_speed = 10

# Квадраты 2
object2 = pygame.surface.Surface((20, 20))
object2.fill("blue")
object2_width = object2.get_width()
object2_height = object2.get_height()

object2_list = []
object2_list_rect = []
for _ in range(5):
    object2_x = randint(0, WIDTH)
    object2_y = randint(0, HEIGHT)
    object2_list.append((object2_x, object2_y))


# ------------------

def collision_fire(x1, y1, w1, h1, x2, y2, w2, h2) -> bool:
    """
    Функция для определения столкновения между двумя прямоугольниками
    :param x1: x координата первого прямоугольника
    :param y1: y координата первого прямоугольника
    :param w1: ширина первого прямоугольника
    :param h1: высота первого прямоугольника
    :param x2: x координата второго прямоугольника
    :param y2: y координата второго прямоугольника
    :param w2: ширина второго прямоугольника
    :param h2: высота второго прямоугольника
    :return: True - коллизия, False - её отсутствие
    """
    return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1


# ------------------


# Контроль FPS
clock = pygame.time.Clock()
FPS = 30

direction = pygame.math.Vector2()
"Направление движения"
running = True
refresh = False

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                refresh = True

    if refresh:
        for i, (object2_x, object2_y) in enumerate(object2_list):
            object2_list[i] = (randint(0, WIDTH), randint(0, HEIGHT))
        refresh = False
        object1.fill("black")

    keys = pygame.key.get_pressed()
    # Движение

    direction.x = keys[pygame.K_d] - keys[pygame.K_a]
    direction.y = keys[pygame.K_s] - keys[pygame.K_w]

    if direction.magnitude() != 0:
        """Нормализация необходима для того, 
        чтобы при движении по диагонали наша скорость не была выше. 
        Благодаря нормализации длина вектора direction всегда будет равна 1.
        Т.е. к примеру без нормализации при движении, если мы движемся со скоростью 1 в одном направлении,
        с зажатыми кнопками вправо и вверх 
        мы будем двигаться по диагонали (по теореме Пифагора) со скоростью √2 (~1.41).
        А с нормализацией будем двигаться по диагонали со скоростью 1.
        Условие self.direction.magnitude() != 0 необходимо для того, чтобы pygame не выдавал ошибку
        т.к. нулевой вектор нельзя нормализовать."""
        direction = direction.normalize()

    object1_x += object1_speed * direction.x
    object1_y += object1_speed * direction.y

    object1_rect = pygame.Rect(object1_x, object1_y, object1_width, object1_height)

    for object2_x, object2_y in object2_list:
        if collision_fire(object1_x, object1_y, object1_width, object1_height,
                          object2_x, object2_y, object2_width, object2_height):
            object1.fill('red')

    # фон
    screen.fill((255, 255, 255))
    # fire
    screen.blit(object1, (object1_x, object1_y))
    # water
    for object2_x, object2_y in object2_list:
        screen.blit(object2, (object2_x, object2_y))

    screen.blit(font_text.render("space - сбросить, поменяв расположение прямоугольников",
                                 True, "black"), (10, 10))
    screen.blit(font_text.render("w, s, a, d - движение", True, "black"), (10, 30))
    screen.blit(font_text.render("при касании черный прямоугольник становится красным",
                                 True, "black"), (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
