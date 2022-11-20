class ReCalculate:

    @staticmethod
    def convert_rgb_dec_to_hex(rgb: tuple[int, int, int]) -> tuple[hex, hex, hex]:
        """
        Convert RGB colors decimal (0 to 255) to hexadecimal numbers
        :param rgb: color in decimal numbers
        :type rgb: tuple[int, int, int]
        :return: RGB color in hexadecimal numbers in string form
        :rtype: tuple[hex, hex, hex]
        """
        r, g, b = rgb
        return hex(r), hex(g), hex(b)

    @staticmethod
    def calculate_percentage_share(percent_figure: float, basic_value: int) -> int:
        """
        Calculate Percentage share
        :param percent_figure: Percentage figure (p)
        :type percent_figure: float
        :param basic_value: Basic value (G)
        :type basic_value: int
        :return: percentage value (W)
        :rtype: int
        """
        return round(percent_figure * basic_value / 100)

    @staticmethod
    def get_perceived_brightness(rgb: tuple[int, int, int]) -> float:
        """
        Calculation of the perceived brightness, which is close to the perception of nonlinear human vision
        (based on https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color)
        :param rgb: color in decimal numbers
        :type rgb: tuple[int, int, int]
        :return: returns L* which is perceptual brightness
        :rtype: float
        """
        y = ReCalculate.__get_linear_luminance(rgb)
        if y <= 216.0 / 24389.0:
            return y * (24389.0 / 27.0)
        else:
            return pow(y, (1.0 / 3.0)) * 116.0 - 16.0

    @staticmethod
    def __get_linear_luminance(rgb: tuple[int, int, int]) -> float:
        """
        Find Luminance (Y) by applying the standard coefficients for sRGB
        :param rgb: color in decimal numbers
        :type rgb: tuple[int, int, int]
        :return: Luminance (Y) value between 0.0 and 1.0
        :rtype: float
        """
        r, g, b = rgb
        r = ReCalculate.__gamma_decode(r)
        g = ReCalculate.__gamma_decode(g)
        b = ReCalculate.__gamma_decode(b)
        return 0.2125862307855955516 * r + 0.7151703037034108499 * g + 0.07220049864333622685 * b

    @staticmethod
    def __gamma_decode(color_channel: int) -> float:
        """
        Convert a gamma encoded 8-bit color to a linear value
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
