from abc import ABC, abstractmethod


class LightSystem(ABC):

    @abstractmethod
    def has_terminated(self) -> bool:
        """
        Check if infinite loop has to stop and the program has to quit otherwise it continues
        For example, check if the light turned off or if the user has pressed the escape key
        :return: if false it will stop the infinite loop
        :rtype: bool
        """
        raise NotImplementedError()

    @abstractmethod
    def set_color(self, rgb_color: tuple[int, int, int]) -> None:
        """
        Set the rgb color an available and configured lights system.
        The format of the color or brightness can calculate by helper class if needed
        :param rgb_color: color in decimal numbers
        :type rgb_color: tuple[int, int, int]
        """
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        """
        Methode to reset the lights bubble or led strip to a color and brightness after
        the end of the program loop
        """
        raise NotImplementedError()
