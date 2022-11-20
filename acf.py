import pyscreenshot
from io import BytesIO
from PIL import ImageChops, ImageStat
from PIL.Image import Image, BILINEAR
from colorthief import ColorThief


class AmbientColorFinder:

    # bounding box with 4 coordinates (left top, left bottom, right top, right bottom) - initialized in constructor
    __bounding_box: tuple[int, int, int, int] = None

    # remembered screenshot (PIL.Image.Image) - initialized in constructor
    __screen_before: Image = None

    # current screenshot (PIL.Image.Image) - initialized in constructor
    __screen_current: Image = None

    # remembered rgb color (decimal numbers) - initialize with white
    __rgb_color_before: tuple[int, int, int] = (255, 255, 255)

    # current rgb color (decimal numbers) - initialize with white
    __rgb_color_current: tuple[int, int, int] = (255, 255, 255)

    def __init__(self):
        """
        instantiates an ambient color finder with ...
        TODO
         define display and position in constructor
          - display has to use in self.__take_screenshot()
          - position must have impact on calculating the bounding box
        """

        # take first screenshot (has original size of the screen)
        self.__screen_before = self.__take_screenshot()

        # getting bounding box out of the first screenshot
        self.__bounding_box = self.__calculate_screen_bounding_box(self.__screen_before)
        
        # take second screenshot limited to a bounding box and resized (to improve performance)
        self.__take_current_screen()

    def has_changed(self) -> bool:
        """
        check if the screenshot and the color is different from before
        and takes a new screenshot every time
        :return: color has changed
        :rtype: bool
        """
        # only if the screenshot is different from before
        if AmbientColorFinder.__are_images_different(self.__screen_before, self.__screen_current):

            # remember screenshot
            self.__screen_before = self.__screen_current

            # get the dominant color on the screen
            self.__rgb_color_current = AmbientColorFinder.__dominant_color_in_image(self.__screen_current)

            # only if color is different from before
            if AmbientColorFinder.__are_colors_different(self.__rgb_color_current, self.__rgb_color_before):

                self.__rgb_color_before = self.__rgb_color_current  # remember color
                self.__take_current_screen()  # take new resized screenshot
                return True  # color has changed

        self.__take_current_screen()  # take new resized screenshot
        return False  # color has not changed

    def get_rgb_color_current(self) -> tuple[int, int, int]:
        """
        get the current dominant color on screen
        :return: rgb color in decimal numbers
        :rtype: tuple[int, int, int]
        """
        return self.__rgb_color_current

    def get_screen_current(self) -> Image:
        """
        get the current screenshot
        :return: screenshot as image object
        :rtype: PIL.Image.Image
        """
        return self.__screen_current

    def __take_current_screen(self) -> None:
        """
        Takes a resized screenshot (to improve performance) limited to a bounding box
        """
        self.__screen_current = self.__quickly_resize_image(
            self.__take_screenshot(self.__bounding_box)
        )

    @staticmethod
    def __take_screenshot(bbox: tuple = (0, 0, 0, 0)) -> Image:
        """
        Take a screenshot of the current screen
        reduced to the middle of the screen to improve performance if bounding box is set
        :param bbox: bounding box with 4 coordinates (left top, left bottom, right top, right bottom)
        :type bbox: tuple
        :return: a screenshot as a PIL Image object
        :rtype: PIL.Image.Image
        """
        if bbox == (0, 0, 0, 0):
            image = pyscreenshot.grab(backend='mss', childprocess=False)
        else:
            image = pyscreenshot.grab(bbox=bbox, backend='mss', childprocess=False)
        return image

    @staticmethod
    def __quickly_resize_image(image: Image, size: int = 200) -> Image:
        """
        Reduce image size as quickly as possible to improve performance for the next steps.
        The size and quality of the image is not so important for the detection of the dominant color
        :param image: image object (should be a screenshot in full screen size)
        :type image: PIL.Image.Image
        :param size: maximum width or height pixels to resize the image (small but not too small)
        :type size: int
        :return: a smaller image without anti-aliasing (bad quality)
        :rtype: PIL.Image.Image
        """
        image.thumbnail((size, size), BILINEAR)
        return image

    @staticmethod
    def __calculate_screen_bounding_box(image: Image, border: int = 100) -> tuple:
        """
        Calculates a bounding box to get the center part of the given image based on a border
        :param image: image object (should be a screenshot in full screen size)
        :type image: PIL.Image.Image
        :param border: edge to be cut off the image in pixel
        :type border: int
        :return: bounding box with 4 coordinates (left top, left bottom, right top, right bottom)
        :rtype: tuple
        """
        img_size = image.size
        img_with, img_height = img_size
        return border, border, img_with - border, img_height - border

    @staticmethod
    def __are_images_different(img1: Image, img2: Image, different_at: int = 5) -> bool:
        """
        Check two images if they are different
        :param img1: image object one which will be compared
        :type img1: PIL.Image.Image
        :param img2: image object two which will be compared
        :type img2 PIL.Image.Image
        :param different_at: threshold at which the images are different
        :type different_at: int
        :return: true if pictures are different enough otherwise false
        :rtype: bool
        """
        img_diff = ImageChops.difference(img1, img2)
        img_stat = ImageStat.Stat(img_diff)
        diff_ratio = sum(img_stat.mean) / (len(img_stat.mean) * 255)
        return (diff_ratio * 100) > different_at

    @staticmethod
    def __dominant_color_in_image(image: Image, quality: int = 1, palette: int = 10) -> tuple:
        """
        Get the dominant color of given image object.
        :param image: image
        :type image: PIL.Image.Image
        :param quality: quality (1=highest quality / >1 faster) of finding the dominant color
        :type quality: int
        :param palette: palette size of colors that are used
        :type palette: int
        :return: RGB of dominant color in image in decimal
        :rtype: tuple
        """
        stream = BytesIO()
        image.save(stream, format='png')
        color_thief = ColorThief(stream)
        colors = color_thief.get_palette(palette, quality)
        return colors[0]

    @staticmethod
    def __are_colors_different(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> bool:
        """
        Compare two rgb colors if they are different
        :param color1: first rgb color in decimal numbers
        :type color1: tuple[int, int, int]
        :param color2: second rgb color in decimal numbers
        :type color2: tuple[int, int, int]
        :return: true if colors are different otherwise false
        :rtype: bool
        """
        return color1 != color2
