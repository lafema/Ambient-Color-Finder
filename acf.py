"""
Ambient Color Finder

This Script will find the dominant color on the current screen
and set it to a light system for example light bulbs or led straps

Must be installed for main system:
pip install pyscreenshot    Python Screenshot 2.2     https://github.com/ponty/pyscreenshot
pip install Pillow          Pillow (PIL fork) 8.1     https://github.com/python-pillow/Pillow
pip install colorthief      Color Thief 0.2.1         https://github.com/fengsp/color-thief-py

Must be installed for test system (test_color_on_screen):
pip install pygame          Pygame 2.0.0              https://github.com/pygame/

Must be installed for Awox mesh light bulbs / only works on Linux (awox_mesh_light):
pip install awoxmeshlight   Awox mesh light 0.2.0     https://github.com/leiaz/python-awox-mesh-light
awoxmeshlight also install  bluepy 1.3.0              https://github.com/IanHarvey/bluepy
awoxmeshlight also install  pycryptodome 3.9.9        https://github.com/Legrandin/pycryptodome/
if bluepy fails with "ERROR: Failed building wheel for bluepy" do:
    apt install unixodbc-dev
    pip install pyodbc

"""

import pyscreenshot
from io import BytesIO
from PIL import ImageChops, ImageStat
from PIL.Image import Image, BILINEAR
from colorthief import ColorThief

'''
Configuration

test_color_on_screen
awox_mesh_light
'''
LIGHT_SYSTEM = 'awox_mesh_light'


def take_screenshot(bbox: tuple = (0, 0, 0, 0)) -> Image:
    """
    Take a screenshot of the current screen
    reduced to the middle of the screen to improve performance if bounding box is set
    :param bbox: bounding box with 4 coordinates (left top, left bottom, right top, right bottom)
    :type bbox: tuple
    :return: a screenshot as a PIL Image object
    :rtype: Image
    """
    if bbox == (0, 0, 0, 0):
        image = pyscreenshot.grab(backend='mss', childprocess=False)
    else:
        image = pyscreenshot.grab(bbox=bbox, backend='mss', childprocess=False)
    return image


def quickly_resize_image(image: Image, size: int = 200) -> Image:
    """
    Reduce image size as quickly as possible to improve performance for the next steps.
    The size and quality of the image is not so important for the detection of the dominant color.
    :param image: image object (should be a screenshot in full screen size)
    :type image: Image
    :param size: maximum width or height pixels to resize the image (small but not too small)
    :type size: int
    :return: a smaller image without anti-aliasing (bad quality)
    :rtype: Image
    """
    image.thumbnail((size, size), BILINEAR)
    return image


def get_screen_bounding_box(image: Image, border: int = 100) -> tuple:
    """
    Calculates a bounding box to get the center part of the given image based on a border.
    :param image: image object (should be a screenshot in full screen size)
    :type image: Image
    :param border: edge to be cut off the image in pixel
    :type border: int
    :return: bounding box with 4 coordinates (left top, left bottom, right top, right bottom)
    :rtype: tuple
    """
    img_size = image.size
    img_with, img_height = img_size
    return border, border, img_with - border, img_height - border


def images_are_different(img1: Image, img2: Image, different_at: int = 5) -> bool:
    """
    Check two images if they are different.
    :param img1: image object one which will be compared
    :type img1: Image
    :param img2: image object two which will be compared
    :type img2 Image
    :param different_at: threshold at which the images are different
    :type different_at: int
    :return: true if pictures are different enough otherwise false
    :rtype: bool
    """
    img_diff = ImageChops.difference(img1, img2)
    img_stat = ImageStat.Stat(img_diff)
    diff_ratio = sum(img_stat.mean) / (len(img_stat.mean) * 255)
    return (diff_ratio * 100) > different_at


def get_dominant_color(image: Image, quality: int = 1) -> tuple:
    """
    Get the dominant color of given image object.
    :param image: image
    :type image: PIL.Image.Image
    :param quality: quality (1=highest quality / >1 faster)
    :type quality: int
    :return: RGB of dominant color in image in decimal
    :rtype: tuple
    """
    stream = BytesIO()
    image.save(stream, format='png')
    color_thief = ColorThief(stream)
    return color_thief.get_color(quality)


def colors_are_different(color1: tuple, color2: tuple) -> bool:
    """
    Compare two rgb colors if they are different
    :param color1: first rgb color in decimal numbers
    :type color1: tuple
    :param color2: second rgb color in decimal numbers
    :type color2: tuple
    :return: true if colors are different otherwise false
    :rtype: bool
    """
    return color1 != color2


def convert_rgb_dec_to_hex(rgb: tuple) -> tuple:
    """
    Convert RGB colors decimal (0 to 255) to hexadecimal numbers
    :param rgb: color in decimal numbers
    :type rgb: tuple
    :return: RGB color in hexadecimal numbers in string form
    :rtype: tuple
    """
    r, g, b = rgb
    return hex(r), hex(g), hex(b)


def gamma_decode(color_channel: int) -> float:
    """
    Convert a gamma encoded 8-bit color to a linear value.
    :param color_channel: 8-bit color
    :type color_channel: int
    :return linearized value between 0.0 and 1.0
    :rtype: float
    """
    vl = color_channel / 255  # 8bit color to dec
    if vl <= 0.0404482362771076:
        return vl / 12.92
    else:
        return pow((vl + 0.055) / 1.055, 2.4)


def get_linear_luminance(rgb: tuple) -> float:
    """
    Find Luminance (Y) by applying the standard coefficients for sRGB
    :param rgb: color in decimal numbers
    :type rgb: tuple
    :return: Luminance (Y) value between 0.0 and 1.0
    :rtype: float
    """
    r, g, b = rgb
    r = gamma_decode(r)
    g = gamma_decode(g)
    b = gamma_decode(b)
    return 0.2125862307855955516 * r + 0.7151703037034108499 * g + 0.07220049864333622685 * b


def get_perceived_lightness(rgb: tuple) -> float:
    """
    Calculation of the perceived lightness, which is close to the perception of nonlinear human vision
    (based on https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color)
    :param rgb: color in decimal numbers
    :type rgb: tuple
    :return: returns L* which is "perceptual lightness"
    :rtype: float
    """
    y = get_linear_luminance(rgb)
    if y <= 216 / 24389:
        return y * (24389 / 27)
    else:
        return pow(y, (1 / 3)) * 116 - 16


def calculate_percentage_value(percent_figure: float, basic_value: int) -> int:
    """
    Calculate percentage value
    :param percent_figure: Percentage figure (p)
    :type percent_figure: float
    :param basic_value: Basic value (G)
    :type basic_value: int
    :return: percentage value (W)
    :rtype: int
    """
    return round(percent_figure * basic_value / 100)


def set_values_to_light_system(rgb_color, brightness, system: str) -> bool:
    """
    Set the pre-calculate color and brightness to an available and configured light system
    :param rgb_color: color in decimal numbers
    :param brightness: brightness close to human vision
    :param system: name of the configured light system
    :return: if false it will stop the infinite loop and quit the program otherwise it continues
    :rtype: bool
    """
    if system == 'test_color_on_screen':
        test_color_on_screen_draw_color(
            rgb_color
        )
    elif system == 'awox_mesh_light':
        awox_mesh_light_set_values(
            convert_rgb_dec_to_hex(rgb_color),  # RGB colors decimal as hexadecimal numbers
            hex(calculate_percentage_value(brightness, 64))  # hexadecimal value of the brightness 0 to 64
        )
    else:
        print('ERROR: Unknown lightning system configured.')
        return False
    return True


def test_color_on_screen_initialize_window():
    """
    Initialises Pygame to display a window with thumbnail and background color to validate color and screen
    :return: Pygame window 800x60 pixel on top left on screen with background color
    :rtype: pygame.Surface
    """
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100, 0'  # set position (x, y) of the window
    py_gui = pygame.display.set_mode((800, 50))  # set with and height of the window
    py_gui.fill(rgb_color_before)  # initialize window background color with white
    return py_gui


def test_color_on_screen_quit() -> bool:
    """
    Quits test system / stops infinite loop
    and is needed to make Pygame work properly (without Pygame will crash)
    :return: false if Pygame windows is closed otherwise true
    :rtype: bool
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def test_color_on_screen_set_thumbnail():
    """
    Place the current screenshot as thumbnail in the Pygame window
    to validate witch dominant color is on the screen
    (there are some video players that only show black screen on screenshot)
    """
    screen_view = pygame.image.fromstring(
        screen_current.tobytes(),
        screen_current.size,
        screen_current.mode
    )
    system.blit(
        screen_view.convert(),
        screen_view.get_rect(
            center=(0, 0)
        )
    )
    pygame.display.flip()


def test_color_on_screen_draw_color(rgb_color: tuple):
    """
    Set the current dominant color as background color to the Pygame window
    :param rgb_color: color in decimal numbers
    :type rgb_color: tuple
    """
    surface = pygame.display.get_surface()
    rect = pygame.Rect(10, 10, 10, 10)
    surface.fill((255, 0, 0), rect)
    system.fill(rgb_color)
    pygame.display.flip()


def awox_mesh_light_connect():
    """
    Initialises Awox mesh light
    Connect to the mesh and turn on the light
    :return:
    """
    awox_light = awoxmeshlight.AwoxMeshLight('AA:BB:CC:DD:EE:FF')
    awox_light.connect()
    awox_light.on()
    return awox_light


def awox_mesh_light_set_values(hex_rgb_color: tuple, hex_brightness: str):
    system.setColor()
    pass


# Main
def start():

    # initial values
    screen_before = take_screenshot()  # take first screenshot (has original size of the screen)
    bounding_box = get_screen_bounding_box(screen_before)  # getting bounding box out of the first screenshot
    rgb_color_before = (255, 255, 255)  # initialize color with white

    if LIGHT_SYSTEM == 'test_color_on_screen':
        # initialises Pygame to display a window with thumbnail and background color to validate color and screen
        import pygame
        system = test_color_on_screen_initialize_window()
    elif LIGHT_SYSTEM == 'awox_mesh_light':
        # initialises Awox mesh light
        import awoxmeshlight
        system = awox_mesh_light_connect()

    # infinite loop
    try:
        do_loop = True
        while do_loop:

            # take screenshot limited to bounding box and resized (to improve performance)
            screen_current = take_screenshot(bounding_box)
            screen_current = quickly_resize_image(screen_current)

            # system to test the color without light system
            if LIGHT_SYSTEM == 'test_color_on_screen':
                do_loop = test_color_on_screen_quit()  # quits test system (is needed to make Pygame work properly)
                test_color_on_screen_set_thumbnail()  # set the screenshot as a thumbnail into the Pygame window

            # only if the screenshot is different from before
            if images_are_different(screen_before, screen_current):

                screen_before = screen_current  # remember screenshot
                rgb_color_current = get_dominant_color(screen_current)  # get the dominant color on the screen

                # only if color is different from before
                if colors_are_different(rgb_color_current, rgb_color_before):

                    rgb_color_before = rgb_color_current  # remember color

                    # setup calculated values to any LIGHT_SYSTEM (stop the loop if false)
                    do_loop = set_values_to_light_system(
                        rgb_color_current,  # set new color
                        get_perceived_lightness(rgb_color_current),  # set brightness close to human vision
                        LIGHT_SYSTEM  # configured light system (see above in the file)
                    )

    finally:

        if LIGHT_SYSTEM == 'awox_mesh_light':
            # TODO: reset light to warm white / 50% brightness
            pass
