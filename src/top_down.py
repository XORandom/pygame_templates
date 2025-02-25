# /// script
# requires-python = ">=3.12"
# dependencies = [
# pygame-ce,
# numpy,
# math,
# json,
# PIL
# ]
# [tool.uv]
# exclude-newer = "2025-02-12T00:00:00Z"
# ///

"""Заготовка под игру с видом сверху-вниз"""
import pygame
import numpy as np
import math
import json
from os import walk




# Сохранение и загрузка позволяют нам работать с настройками пользователя
# а также сохранять прогресс и уровни
user_settings_dict = {}

def save_game_data(data: list):
    """
    Сохраняем данные в JSON. 


    :param data: список, содержит ровно 1 ключ и 1 значение, которое в данный момент изменяется
    :return:
    """
    user_settings_dict[data[0]] = data[1]

    # json_object = json.dumps(user_settings_dict, indent=4)
    # with open("./user_data/user_settings.json", "w") as outfile:
    #     outfile.write(json_object)
    # Или так
    with open("./user_data/user_settings.json", "w") as outfile:
        json.dump(user_settings_dict, outfile)
    pass

def load_game_data():
    with open("./user_data/user_settings.json", "r") as openfile:
        user_settings_dict = json.load(openfile)
    return user_settings_dict

user_settings_dict = load_game_data()


pygame.init()

WIDTH = user_settings_dict["widht"]
"Ширина окна игры"
HEIGHT = user_settings_dict["height"]
"Высота окна игры"
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна игры с параметрами ширины и высоты окна
pygame.display.set_caption("Top-down")  # Название нашей игры
game_icon = pygame.image.load('assets/sprite/top-down_icon.png')
pygame.display.set_icon(game_icon)  # Иконка нашей игры
grab_cursor: bool = user_settings_dict["grab_cursor"]
"""Курсор заблокирован"""
pygame.event.set_grab(grab_cursor)  # Блокирует перемещение мыши за границу экрана

# Контроль FPS
clock = pygame.time.Clock()
FPS = user_settings_dict["fps"]
"Скорость игры"

# Игровые переменные
current_scene: str = "menu"
"Текущая сцена"
volume = user_settings_dict["volume"]
"Громкость музыки"
image_scale = user_settings_dict["image_scale"]
"масштаб изображенйи в игре"

barrel_offset = (100, 0) * image_scale
"Настраиваемое смещение дула турели"

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
            image_surf = pygame.transform.rotozoom(image_surf, 0, image_scale)
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
            image_surf = pygame.transform.rotozoom(image_surf, 0, image_scale)
            # image_surf = pygame.transform.scale(image_surf, (100, 100))# либо можно задать размер изображений
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
        print('Изображение не найдено, ошибка: ', e)
        raise SystemExit()
    return image


def find_all_poi(image_name: str, folder_path: str) -> dict:
    """ 
    Позволяет отпределить координаты точек интереса
    
    """
    import PIL.Image
    try:
        image = PIL.Image.open(f'{folder_path}/{image_name}').convert("RGB")
    except FileNotFoundError as e:
        print('Изображение не найдено, ошибка: ', e)
        raise SystemExit()
    
    points_dict: dict = {
        "turret":(0, 0),    # центр вращения турели
        "wep1":(0, 0),      # центр основного оружия
        "wep2":(0, 0),      # центр основного оружия
        "rl1":(0, 0),       # центр ракетной установки
        "rl2":(0, 0),       # центр ракетной установки
        }
    "словарь, к который мы сохраняем координаты"

    # так как картинки расположены не прямо в левом верхнем углу, нам нужны смещения


    # Вычисляем где должны располагаться центр орудий, турели и т.д.
    # это делается за счёт указанный на изображении ярких точек
    # для ускорения вычислений, используем numpy
    im_arr = np.array(image)
    # -------------------------------------------------------------
    turret_pont_color=np.array([255,0,255],dtype=np.uint8)
    "цвет ключевой точки для туррели [255,0,255] На изображении не увидеть эту точку, поскольку она прозрачная (alpha=0)"
    turret_point=np.where(np.all((im_arr==turret_pont_color),axis=-1))
    "Находим коодинату центра туррели (для данного рисунка, центр туррели на 1 пиксель левее)"
    # Добавляем информацию в словарь
    points_dict["turret"] = (turret_point[0][0].item()*image_scale, turret_point[1][0].item()*image_scale)
    # -------------------------------------------------------------
    rocket_ponts_color=np.array([0,255,255],dtype=np.uint8)
    "цвет ключевых точек для ракетных установок [0,255,255]"
    rocket_ponts=np.where(np.all((im_arr==rocket_ponts_color),axis=-1))
    "Находим коодинаты ракетных установок"
    # Добавляем информацию в словарь
    points_dict["rl1"] = (94*image_scale,  # y
                          499*image_scale)   # x
    points_dict["rl2"] = (673*image_scale,
                          499*image_scale)
    # points_dict["rl1"] = (rocket_ponts[1][0].item()*image_scale, 
                        #   rocket_ponts[0][0].item()*image_scale)
    # points_dict["rl2"] = (rocket_ponts[1][1].item()*image_scale, 
    #                       rocket_ponts[0][1].item()*image_scale)
    # -------------------------------------------------------------
    veapon_ponts_color=np.array([0,255,254],dtype=np.uint8)
    "цвет ключевых точек для остновных орудий [0,255,254]"
    veapon_ponts=np.where(np.all((im_arr==veapon_ponts_color),axis=-1))
    "Находим коодинаты ракетных установок"
    # Добавляем информацию в словарь
    points_dict["wep1"] = (veapon_ponts[1][0].item()*image_scale, 
                           veapon_ponts[0][0].item()*image_scale)
    points_dict["wep2"] = (veapon_ponts[1][1].item()*image_scale, 
                           veapon_ponts[0][1].item()*image_scale)
    # -------------------------------------------------------------

    # Оставляю для того, чтобы было легче разобраться с тем, что происходит. Можно раскомментировать две строчки ниже и посмотреть
    # print(f"turret_point{turret_point}, rocket_ponts{rocket_ponts}, veapon_ponts {veapon_ponts}")
    # print(points_dict)
    return points_dict


def centered_images(poi: dict, images_list: list) -> dict:
    """

    Берет массив точек интереса find_all_poi() и указывает нужные координаты центра с учетом размера изображений

    :param poi: Интересуемая позиция
    :param images_list: Загруженные изображений
    :return: Координаты точек с учетом корреции
    """

    pass

# ---------------------------------------------------------------------------------------------------------------------


move_set = import_folder(folder_path="assets/sprite/player/spaceship_vol2")
"""Словарь со всеми спрайтами персонажа"""
points_dict = find_all_poi("large_2.png",folder_path="assets/sprite/player/spaceship_vol2")
"словарь с координатами ключевых точек"
# Ширина и высота корабля соответствуют изображению
player_width, player_height = move_set[1].get_size()
print(move_set[1].get_size())
# Теперь создаем поверхность заданного размера
player_surf = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
"поверхность, на которйо расположен наш корабль"

def create_ship() -> None:
    """Функция для создания корабля

    """
    pass



def render_ship(full_rocket: bool = True, 
                player_pos: list | tuple = (WIDTH // 2, HEIGHT // 2), 
                player_angle: float = 0.0, 
                turret_angle: float = 0) -> None:
    """Функция для отображения корабля


    :param iteration: Номер кадра, для анимации
    :param player_pos: (x, y) - координаты центра персонажа
    :param player_angle: Угол поворота персонажа
    :param turret_angle: Угол поворота турели
    :return: ничего, но на экране должен отрисоваться корабль
    """

    player_surf.fill(pygame.Color(0,0,0,0))
    # Размещаем корабль на поверхности
    player_surf.blit(move_set[1], (0,0))

    # Размещаем боковые орудия
    player_surf.blit(move_set[3], points_dict["wep1"])
    player_surf.blit(pygame.transform.flip(move_set[3], True, False), points_dict["wep2"])

    # размещаем ракеты
    # Показывать ракеты?
    if full_rocket:
        player_surf.blit(move_set[7], points_dict["rl1"])
        player_surf.blit(move_set[7], points_dict["rl2"])
    else:
        player_surf.blit(move_set[6], points_dict["rl1"])
        player_surf.blit(move_set[6], points_dict["rl2"])

    # Размещаем турель
    turret_image_copy = pygame.transform.rotate(move_set[2], turret_angle)
    "во время вращения изображение меняется, сохраняем копию для того, чтобы узнать его ширину и высоту"
    # Для того, чтобы изображение вращалось правильно нужно вычесть половину ширины и высоты из координат
    player_surf.blit(turret_image_copy, (points_dict["turret"][0]-turret_image_copy.get_width()/2,
                                         points_dict["turret"][1]-turret_image_copy.get_height()/2
                                         ))

    rotated_player_surf = pygame.transform.rotate(player_surf, player_angle)
    screen.blit(rotated_player_surf, (
                player_pos[0] - rotated_player_surf.get_width()/2,
                player_pos[1] - rotated_player_surf.get_height()/2
                ))


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
        screen.blit(font_text.render("Это настройки!", True, "white"), (50, 50))

        button("Settings", WIDTH // 2 - 100, 400, 200, 50,
                action=switch_scene, action_arg="settings")
        button(f"Масштабирование | {grab_cursor}", WIDTH // 2 - 100, 500, 200, 50,
                action=save_game_data, action_arg=["image_scale", 1])
        button(f"Захват курсора | {grab_cursor}", WIDTH // 2 - 100, 600, 200, 50,
                action=save_game_data, action_arg=["grab_cursor", False])
        button(f"Громкость музыки | {volume}", WIDTH // 2 - 100, 700, 200, 50,
                action=save_game_data, action_arg=["volume", 0])
        button("Выход", WIDTH // 2 - 100, 800, 200, 50,
                action=switch_scene, action_arg="exit")
        if flag_custom_cursor:
            screen.blit(cursor_image, pygame.mouse.get_pos())
        pygame.display.flip()


def create_projectile(pr_x: int, pr_y: int, pr_dir_x: float, pr_dir_y: float, pr_speed:int=10) -> dict:
    """
    Если знаете, что такое Класс, переделайте в него, это будет гораздо проще

    создает словарь, содержащий основные данные нашего снаряда, его коодинаты, скорость
    :param pr_x: текущая координата x
    :param pr_y: текущая координата y
    :param pr_dir_x: напрвление движения по x
    :param pr_dir_y: напрвление движения по y
    :param pr_speed: скорость
    :return: 
    """
    projectile_data = {
        "x":pr_x,
        "y":pr_y,
        "dir_x":pr_dir_x,
        "dir_y":pr_dir_y,
        "speed":pr_speed,
    }
    return projectile_data


def update_projectile(projectiles: list[dict]):
    """
    Обновляем все существуюшие в игре снаряды


    """
    for projectile in projectiles:
        projectile["x"] += projectile["dir_x"] * projectile["speed"]
        projectile["y"] += projectile["dir_y"] * projectile["speed"]
        pygame.draw.circle(screen, (255, 0, 0), (int(projectile["x"]), int(projectile["y"])), 5)

    # Удаляем снаряды, вышедшие за пределы экрана
    projectiles = [p for p in projectiles if 0 < p["x"] < WIDTH and 0 < p["y"] < HEIGHT]


def update_homing_projectile(projectiles: list[dict], target: list|tuple):
    """
    Обновляем самонаводящиеся снаряды
    Пока что все они будут преследовать одну цель
    Это можно при желании изменить

    """


    
    for projectile in projectiles:
        # Находим евклидово расстояние до цели
        # dist_to_target = math.sqrt(pow(projectile["x"]-target.x, 2)+pow(projectile["y"]-target.y, 2))
        # или так, находим гипотенузу
        # dist_to_target = math.hypot(target.x - projectile["x"], target.y - pow(projectile["y"])
        # или используя встроенные функции
        dist_to_target = pygame.math.Vector2(projectile["x"], projectile["y"]).distance_to((target.x, target.y))

        # находим угол до цели
        angle_to_target = pygame.math.Vector2().angle_to(dist_to_target)
        print(f"{dist_to_target} an {angle_to_target}")

        projectile["dir_x"] = angle_to_target.x
        projectile["dir_y"] = angle_to_target.y


        projectile["x"] += projectile["dir_x"] * projectile["speed"]
        projectile["y"] += projectile["dir_y"] * projectile["speed"]


    pass


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
    rotate_speed_ship = 10 # скорость 
    rotate_speed_turret = 10 # скорость 
    x = 2
    y = 2
    angle_turret = 180
    angle_ship = 0
    projectiles = []
    offset_x = 0
    offset_y = 0
    "Список для хранения снарядов"


    while current_scene == "game":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Нажатие на крестик
                switch_scene("exit")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    full_rocket = not full_rocket
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Правая кнопка мыши
                    # Создаём снаряд
                    total_angle = math.radians(angle_ship + angle_turret - 90)  # Общий угол, меньше расчётов
                    
                    # здесь необходимы базовые тригонометрические знания, вкратце, sin используется для оси y, cos для оси x
                    # функция sin(угол) возвращает значения в диапазоне [-1, 1]
                    # надо представить прямоугольный треугольник с заданным углом
                    # sin(заданный угол) возвращает значение противоположной (углу) стороны треугольника (катета), делённое на гипотенузу
                    # есть еще арктангенс для обеих осей
                    offset_x = barrel_offset[0] * math.cos(total_angle)
                    offset_y = barrel_offset[0] * -math.sin(total_angle)

                    # Так как наш корабль тоже поворачивается, надо это учитывать
                    direction_x = math.cos(total_angle) # -90, так как турель по умолчанию повернута вниз, а не вправо 
                    direction_y = -math.sin(total_angle)  # -math, т.к. Y растёт вниз
                    # Поворачиваем смещение дула на угол турели
                    projectile: dict = create_projectile(x+offset_x, y+offset_y, direction_x, direction_y, 30)
                    projectiles.append(projectile)

        if current_scene == "exit":  # Прерываем цикл
            break

        keys = pygame.key.get_pressed()
        # Движение

        # direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        # direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        # if direction.magnitude() != 0:
        #     """Нормализация необходима для того, 
        #     чтобы при движении по диагонали наша скорость не была выше. 
        #     Благодаря нормализации длина вектора direction всегда будет равна 1.
        #     Т.е. к примеру без нормализации при движении, если мы движемся со скоростью 1 в одном направлении,
        #     с зажатыми кнопками вправо и вверх 
        #     мы будем двигаться по диагонали (по теореме Пифагора) со скоростью √2 (~1.41).
        #     А с нормализацией будем двигаться по диагонали со скоростью 1.
        #     Условие self.direction.magnitude() != 0 необходимо для того, чтобы pygame не выдавал ошибку
        #     т.к. нулевой вектор нельзя нормализовать."""
        #     direction = direction.normalize()

        # x += direction.x * speed
        # y += direction.y * speed


        """ Вот так выглядит направление
                90
        180     @       0
                270
        
        """
        if keys[pygame.K_a]:
            angle_ship += rotate_speed_ship
        if keys[pygame.K_d]:
            angle_ship -= rotate_speed_ship
        if keys[pygame.K_w]:
            x += speed * math.cos(math.radians(angle_ship+90))# +90 потому, что корабль повернут влево, относительно нулевой точки (это напрвление вправо)
            y -= speed * math.sin(math.radians(angle_ship+90))  # Y растёт вниз, поэтому '-'
        if keys[pygame.K_s]:
            x -= speed * math.cos(math.radians(angle_ship+90))
            y += speed * math.sin(math.radians(angle_ship+90))  # Движение назад

        angle_turret += (keys[pygame.K_q] - keys[pygame.K_e]) * rotate_speed_turret
        angle_ship += (keys[pygame.K_x] - keys[pygame.K_c]) * rotate_speed_ship

        # Теперь топология этой вселенной - бублик
        x = x % (WIDTH + 100)
        y = y % (HEIGHT+ 100)



        screen.fill("black")

        render_ship(turret_angle=angle_turret, player_pos=(x,y), player_angle=angle_ship, full_rocket=full_rocket)


        pygame.draw.line(screen, "green", (x+offset_x, y+offset_y), (x, y), 3)

        screen.blit(font_text.render("space - ракеты", True, "white"), (10, 10))
        screen.blit(font_text.render("q, e - поворот турели", True, "white"), (10, 30))
        # screen.blit(font_text.render("w, s, a, d - движение", True, "white"), (10, 50))
        screen.blit(font_text.render("w, s - движение вперёд/назад", True, "white"), (10, 50))
        screen.blit(font_text.render("a, d - поворот корабля", True, "white"), (10, 70))
        screen.blit(font_text.render("ПКМ - стрельба", True, "white"), (10, 90)) 


        update_projectile(projectiles)

        if flag_custom_cursor:
            screen.blit(cursor_image, pygame.mouse.get_pos())

        pygame.display.flip()
    else:
        print("Game over")


if __name__ == '__main__':
    main_menu()
    pygame.quit()
