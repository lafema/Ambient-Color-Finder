import os
import pygame
from PIL.Image import Image
from lights import interface


class TestShowColorOnScreen(interface.LightSystem):

    system: pygame.Surface = None

    def __init__(self):
        """
        initializes a window that displays the current dominant color
        and a thumbnail of the screenshot for testing purposes
        """
        self.system = TestShowColorOnScreen.__initiate_window_where_test_are_shown()

    def has_terminated(self) -> bool:
        """
        check if Pygame was quit (is needed to make Pygame work properly)
        :return: if false it will stop the infinite loop and quit the program otherwise it continues
        :rtype: bool
        """
        #
        return TestShowColorOnScreen.__check_has_to_quit()

    def set_thumbnail(self, thumbnail: Image) -> None:
        """
        set the screenshot as a thumbnail into the Pygame window (for visual assessment)
        :param thumbnail: screenshot as a thumbnail from current screen
        :type thumbnail: PIL.Image.Image
        """
        self.__set_thumbnail_to_test_window(thumbnail)

    def set_color(self, rgb_color: tuple[int, int, int]) -> None:
        """
        set the rgb color to as background color to the Pygame window and check if Pygame was quit
        :param rgb_color: color in decimal numbers
        :type rgb_color: tuple[int, int, int]
        """

        # set the current dominant color as background color to the Pygame window
        self.__draw_color_to_test_window(rgb_color)

    def reset(self) -> None:
        """
        not required for the test system
        """
        pass

    @staticmethod
    def __initiate_window_where_test_are_shown() -> pygame.Surface:
        """
        Initialises Pygame to display a window with thumbnail and background color to validate color and screen
        :return: Pygame window 800x60 pixel on top left on screen with background color
        :rtype: pygame.Surface
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100, 30'  # set position (x, y) of the window
        py_gui = pygame.display.set_mode((800, 50))  # set with and height of the window
        py_gui.fill((255, 255, 255))  # initialize window background color with white
        return py_gui

    def __draw_color_to_test_window(self, rgb_color: tuple[int, int, int]) -> None:
        """
        Set the current dominant color as background color to the Pygame window
        :param rgb_color: color in decimal numbers
        :type rgb_color: tuple[int, int, int]
        """
        surface = pygame.display.get_surface()
        rect = pygame.Rect(10, 10, 10, 10)
        surface.fill((255, 0, 0), rect)
        self.system.fill(rgb_color)
        pygame.display.flip()

    def __set_thumbnail_to_test_window(self, thumbnail: Image) -> None:
        """
        Place the current screenshot as thumbnail in the Pygame window
        to validate witch dominant color is on the screen
        (there are some video players that only show black screen on screenshot)
        :param thumbnail: thumbnail of the screenshot
        :type thumbnail: PIL.Image.Image
        """
        screen_view = pygame.image.frombuffer(
            thumbnail.tobytes(),
            thumbnail.size,
            thumbnail.mode
        )
        self.system.blit(
            screen_view.convert(),
            screen_view.get_rect(
                center=(0, 0)
            )
        )
        pygame.display.flip()

    @staticmethod
    def __check_has_to_quit() -> bool:
        """
        Quits test system when PyGame is stopped
        and stops infinite loop because without Pygame will crash
        :return: false if Pygame windows is closed otherwise true
        :rtype: bool
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
