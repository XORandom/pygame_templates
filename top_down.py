"""Заготовка под игру с видом сверху-вниз"""
import pygame
from os import walk

pygame.init()

WIDTH = 1000
"Ширина окна игры"
HEIGHT = 1000
"Высота окна игры"
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна игры с параметрами ширины и высоты окна
pygame.display.set_caption("Top-down")  # Название нашей игры
game_icon = pygame.image.load('assets/sprite/top-down_icon.png')
pygame.display.set_icon(game_icon)  # Иконка нашей игры

# Контроль FPS
clock = pygame.time.Clock()
FPS = 30
"Скорость игры"

# Игровые переменные
current_scene: str = "menu"
"Текущая сцена"
volume = 0.1
"Громкость музыки"

slow = 8
"Скорость анимации (idle, hit, game_over)"
slow_roll = 4
"Скорость анимации (roll)"
slow_run = 2
"Скорость анимации (run)"

# Флаги
flag_custom_cursor = True
"Используется ли пользовательский курсор"

# Музыка
pygame.mixer.init()
pygame.mixer.music.load('assets/music/632269__roloxi__metal-dripsv3.ogg')
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

sound_button_click = pygame.mixer.Sound('assets/music/564507__moogleoftheages__1keystrokeone.ogg')
"Звук при клике"
sound_button_click.set_volume(0.9)
sound_button_hold = pygame.mixer.Sound('assets/music/442313__daddo22__metal-tssht.ogg')
"Звук при наведении мышки на кнопку"
sound_button_hold.set_volume(0.9)
sound_jump = pygame.mixer.Sound('assets/music/264828__cmdrobot__text-message-or-videogame-jump.ogg')
"Звук при прыжке"
sound_button_hold.set_volume(0.9)

# Шрифты
font_text = pygame.font.SysFont("monospace", 30)
"Шрифт для текста"
font_title = pygame.font.SysFont("monospace", 100)
"Шрифт для заголовков"

# Изображения
# bg = pygame.image.load('assets/bg.png')


if flag_custom_cursor:
    pygame.mouse.set_visible(False)  # Делаем системный курсор невидимым
    cursor_image = pygame.image.load('assets/sprite/ui/cursor.png')  # Загружаем картинку курсора
    cursor_image = pygame.transform.scale(cursor_image, (25, 25))  # Масштабируем до нужного размера
    cursor_image.set_alpha(255)  # Насколько курсор будет видно. 0-255, где 0 - невидимый, 255 - полностью видимый

# Игровые функции
"""Игра, меню, настройки, главный экран - это все игровые циклы. Я могу поочередно переключать их"""


def button(text: str, x: int, y: int, width: int, height: int,
           inactive_color: list | tuple | str = (15, 113, 115),
           active_color: list | tuple | str = (188, 163, 172),
           action=None, action_arg=None) -> bool:
    """Функция для отрисовки кнопок

    :param text: Текст, что будет отображен на кнопке.
    :param x: Координата Х (левый верхний угол прямоугольника кнопки).
    :param y: Координата Y (левый верхний угол прямоугольника кнопки).
    :param width: Ширина прямоугольника.
    :param height: Высота прямоугольника.
    :param inactive_color: Цвет неактивной кнопки, без наведения мышки.
    :param active_color: Цвет активной кнопки, на которую навели мышь.
    :param action: Функция, которая будет выполняться при нажатии. (может быть любой на ваш вкус)
    :param action_arg: Аргумент функции, которая будет выполняться при нажатии.
    :return:
    """

    return_flag = False
    "флаг, говорящий, что на кнопку навели мышку, может пригодиться"
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:  # Если мышь находится внутри прямоугольника
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            sound_button_click.play()
            action(action_arg)
        return_flag = True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    screen.blit(font_text.render(text, True, (0, 0, 0)), (x + 10, y + 10))  # Рисуем текст на кнопке
    return return_flag


# Загрузка изображений. Я представил 3 способа, можно их комбинировать или выбрать один.

def import_folder(folder_path: str) -> list:
    """ Загрузить в список все спрайты из папки. Этой функции не важны названия изображений или их расширения. \n
    Важно только, чтобы в папке не было ничего лишнего.
    :param folder_path: Полный путь к папке с изображениями.
    :return: На выходе список, содержащий все изображения.
    """

    surface_list = []

    for _, __, img_files in walk(folder_path):
        """folder_path = (path, [список папок внутри этой папки], [список img_files]), 
        нам нужно только img_files(список изображений)"""
        for image in img_files:
            full_path = folder_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            # Так как все фрагменты имеют разный размер,
            # то вместо transform.scale() удобнее использовать transform.rotozoom()
            image_surf = pygame.transform.rotozoom(image_surf, 0, 0.5)
            surface_list.append(image_surf)
    return surface_list


def import_folder_dict(folder_path: str) -> dict:
    """ Загружает все изображения из папки в словарь, полезно, если хочется обращаться к изображениям по имени. \n
    Но нужно знать, что такое словарь в Python. \n
    Также в этом варианте я добавил загрузку зеркальных копий спрайтов. \n
    :param folder_path: Полный путь к папке с изображениями.
    :return: На выходе словарь, содержащий все изображения с ключами в виде их названий.
    """

    surface_dict = {}

    for _, __, img_files in walk(folder_path):
        """folder_path = (path, [список папок внутри этой папки], [список img_files]), нам нужно только img_files"""
        for image in img_files:
            full_path = folder_path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (100, 100))
            surface_dict[image.split('.')[0]] = image_surf
            image_surf_mirror = pygame.transform.flip(image_surf, True, False)  # Зеркальная копия спрайта
            surface_dict[image.split('.')[0] + "-mirror"] = image_surf_mirror

    return surface_dict


def load_sprite(image_name: str, folder_path: str) -> pygame.Surface:
    """ Функция для загрузки одного изображения
    :param image_name: Название изображения
    :param folder_path: Путь к папке с изображением
    :return: Загруженное изображение
    """
    try:
        image = pygame.image.load(f'{folder_path}/{image_name}')
    except FileNotFoundError as e:
        print('File not found, error: ', e)
        raise SystemExit()
    return image


# ---------------------------------------------------------------------------------------------------------------------


move_set = import_folder(folder_path="assets/sprite/player/spaceship_vol2")
"""Словарь со всеми спрайтами персонажа"""

player_width, player_height = move_set[1].get_size()
# Для того чтобы не проводить сложные расчеты центра вращения и угла, можно создать поверхность,
# на нее разместить турель и уже её вращать.
player_surf = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
player_pos = (WIDTH // 2, HEIGHT // 2)

player_surf.blit(move_set[2], (191, 197))


def create_player2(player_pos: list | tuple = (WIDTH // 2, HEIGHT // 2),
                   iteration: int = 0, mirror: str = "", player_angle: float = 0, turret_angle: float = 0) -> None:
    """Функция для рисования персонажа

    :param player_pos: (x, y) - координаты центра персонажа
    :param player_angle: Угол поворота персонажа
    :param turret_angle: Угол поворота турели
    :param iteration: Номер кадра, для анимации
    :param mirror: В какую сторону смотрит персонаж, "" или "-mirror"
    :return:
    """

    turret_x = player_pos[0] + 50
    turret_y = player_pos[1] + 50

    # Для того, чтобы не проводить сложные расчеты центра вращения и угла, можно создать поверхность,
    # на нее разместить корабль со всеми делалями и уже их вращать.
    point = pygame.math.Vector2(turret_x, turret_y)

    rotated_image = pygame.transform.rotate(move_set[1], player_angle)
    screen.blit(rotated_image, player_pos)
    screen.blit(move_set[3], (turret_x, turret_y))


def switch_scene(new_scene: str = "exit"):
    """ Переключение сцены, в том числе и сцены выхода их игры. \n
    game - основной игровой цикл. \n
    menu - главный экран. \n
    exit - экран выхода из игры.
    :param new_scene: На какую сцену переключиться.
    :return:
    """
    global current_scene
    current_scene = new_scene
    if current_scene == "exit":
        exit_screen()
    elif current_scene == "game":
        game()
    elif current_scene == "menu":
        main_menu()
    elif current_scene == "settings":
        settings()


# ---------------------------------------------------------------------------------------------------------------------


def main_menu():
    """Главный экран"""
    while current_scene == "menu":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажатие на крестик
                switch_scene("exit")
        screen.fill("black")
        screen.blit(font_title.render("Top-down", True, "white"), (WIDTH // 2 - 250, 50))
        button("Play", x=WIDTH // 2 - 100, y=200, width=200, height=50,
               action=switch_scene, action_arg="game")
        button("Settings", WIDTH // 2 - 100, 300, 200, 50,
               action=switch_scene, action_arg="settings")
        button("Exit", WIDTH // 2 - 100, 400, 200, 50,
               action=switch_scene, action_arg="exit")
        if current_scene == "exit":  # Прерываем цикл
            break
        if flag_custom_cursor:
            screen.blit(cursor_image, pygame.mouse.get_pos())
        pygame.display.flip()


def exit_screen():
    """ Экран выхода из игры. Нужен чтобы что-то отобразить при выходе из игры.
    Если нужно выйти сразу, то цикл можно закомментировать, оставив только pass.

    :return:
    """

    for _ in range(30):
        clock.tick(FPS)
        screen.fill("black")
        # Можно добавить прощальное сообщение
        screen.blit(font_text.render("До новых встреч!", True, "white"), (50, 50))
        pygame.display.flip()
    pass


def settings():
    """ Настройки.

    :return:
    """
    clock.tick(FPS)
    while current_scene == "settings":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажатие на крестик
                switch_scene("exit")
        screen.fill("black")
        pygame.display.flip()


def game():
    """Основной игровой цикл"""

    # Меняю музыку
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/music/19772__amby26__asianbeatz-riff-1.ogg")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    direction = pygame.math.Vector2()
    "Направление движения"
    full_rocket = True
    speed = 20
    rotate_speed = 10
    x = 2
    y = 2
    angle = 0
    while current_scene == "game":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажатие на крестик
                switch_scene("exit")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    full_rocket = not full_rocket
        if current_scene == "exit":  # Прерываем цикл
            break

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

        x += direction.x * speed
        y += direction.y * speed
        angle += (keys[pygame.K_q] - keys[pygame.K_e]) * rotate_speed

        screen.fill("black")

        rotated_player = pygame.transform.rotate(player_surf, angle)
        screen.blit(move_set[1], (x, y))  # корабль
        if full_rocket:
            screen.blit(move_set[7], (x + 115, y + 230))
            screen.blit(move_set[7], (x + 270, y + 230))
        else:
            screen.blit(move_set[6], (x + 115, y + 233))
            screen.blit(move_set[6], (x + 270, y + 233))

        screen.blit(rotated_player, rotated_player.get_rect(center=(x + player_width // 2, y + player_height // 2)))

        screen.blit(font_text.render("space - ракеты", True, "white"), (10, 10))
        screen.blit(font_text.render("q, e - поворот турели", True, "white"), (10, 30))
        screen.blit(font_text.render("w, s, a, d - движение", True, "white"), (10, 50))

        if flag_custom_cursor:
            screen.blit(cursor_image, pygame.mouse.get_pos())

        pygame.display.flip()
    else:
        print("Game over")


if __name__ == '__main__':
    main_menu()
    pygame.quit()
