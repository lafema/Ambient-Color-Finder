Ambient Color Finder
====================

This Script will find the dominant color on the current screen
and set it to a lights system for example lights bulbs or led straps.

Requirements
------------

Must be installed for main system:
    Python Screenshot 2.2
        pip install pyscreenshot <https://github.com/ponty/pyscreenshot>
    Pillow (PIL fork) 8.1
        pip install Pillow <https://github.com/python-pillow/Pillow>
    Color Thief 0.2.1
        pip install colorthief <https://github.com/fengsp/color-thief-py>

Must be installed for test system:
    Pygame 2.0.0
        pip install pygame <https://github.com/pygame/>

Must be installed for Awox mesh lights bulbs (only on Linux):
    Awox mesh lights 0.2.0
        pip install awoxmeshlight <https://github.com/leiaz/python-awox-mesh-light>
    awoxmeshlight also install
        * bluepy 1.3.0 <https://github.com/IanHarvey/bluepy>
        * pycryptodome 3.9.9 <https://github.com/Legrandin/pycryptodome/>

    if bluepy fails with "ERROR: Failed building wheel for bluepy" do
        * apt install unixodbc-dev
        * pip install pyodbc
