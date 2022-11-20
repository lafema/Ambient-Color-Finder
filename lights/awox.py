import awoxmeshlight
from lights import interface, helper


class AwoxLightSystem(interface.LightSystem):

    # current Awox mesh light
    awox_light: awoxmeshlight.AwoxMeshLight = None

    def __init__(self, mac_address: str):
        """
        initialises Awox mesh lights
        :param mac_address: MAC-Address of the light
        :type mac_address: str
        """
        self.awox_light = AwoxLightSystem.__awox_mesh_light_connect(mac_address)

    def has_terminated(self) -> bool:
        """
        Check if infinite loop has to stop and the program has to quit otherwise it continues
        For example, check if the light turned off or if the user has pressed the escape key
        :return: if false it will stop the infinite loop
        :rtype: bool
        """
        pass  # TODO

    def set_color(self, rgb_color: tuple[int, int, int]) -> bool:
        """
        Set the rgb color Awox mesh lights
        The format of the color and the brightness are calculate by helper class
        :param rgb_color: color in decimal numbers
        :type rgb_color: tuple[int, int, int]
        :return: if false it will stop the infinite loop and quit the program otherwise it continues
        :rtype: bool
        """

        # calculate needed values for lights system
        hex_color = helper.ReCalculate.convert_rgb_dec_to_hex(rgb_color)  # RGB colors decimal as hexadecimal numbers
        brightness = helper.ReCalculate.get_perceived_brightness(rgb_color)  # get perceptual brightness by color
        hex_brightness = hex(helper.ReCalculate.calculate_percentage_share(brightness, 64))  # hexadecimal 0 to 64

        # set values to light system(s)
        self.__awox_mesh_light_set_values(
            hex_color,
            hex_brightness
        )
        return True

    def reset(self) -> None:
        # TODO
        #  reset lights to warm white and 50% brightness
        pass

    @staticmethod
    def __awox_mesh_light_connect(mac_address: str) -> awoxmeshlight.AwoxMeshLight:
        """
        Initialises Awox mesh lights
        Connect to the mesh and turn on the light
        :param mac_address: MAC-Address of the lights
        :type mac_address: str
        :return: Object of AwoxMeshLight
        :rtype: awoxmeshlight.AwoxMeshLight:
        """
        awox_light = awoxmeshlight.AwoxMeshLight(mac_address)
        awox_light.connect()
        awox_light.on()
        return awox_light

    def __awox_mesh_light_set_values(self, hex_rgb_color: tuple, hex_brightness: str) -> None:
        """
        Set the rgb color Awox mesh lights
        :param hex_rgb_color: RGB colors as hexadecimal numbers
        :type hex_brightness: tuple
        :param hex_brightness: perceptual brightness hexadecimal from 0 to 64
        :type hex_rgb_color: str
        """
        self.awox_light.setColor(hex_rgb_color, hex_brightness)
