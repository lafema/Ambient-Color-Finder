from acf import AmbientColorFinder
from lights import test as test_light


def main():

    # initialize one or more lights bulbs or LED straps
    try:
        light_one = test_light.TestShowColorOnScreen()
    except Exception as e:
        print("At initialize light(s) error raised: ", e)
        return

    # find color on screen and set to light(s)
    try:
        # initialize one AmbientColorFinder per display
        acf = AmbientColorFinder()  # find color on a screen at display / position

        # infinite loop
        do_loop = True  # initialize loop variable
        while do_loop:

            # stop look if necessary
            do_loop = light_one.has_terminated()

            # set thumbnail of the screenshot only for testing purposes
            light_one.set_thumbnail(acf.get_screen_current())

            # only if the screenshot and the color is different from before
            if acf.has_changed():

                # set new color to one or more lights systems
                light_one.set_color(
                    acf.get_rgb_color_current()  # get the new color
                )

    except Exception as e:
        print("At color set to light(s) error raised: ", e)

    finally:

        # reset color and brightness after program loop ends
        light_one.reset()


if __name__ == '__main__':
    main()
