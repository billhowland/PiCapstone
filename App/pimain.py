import os
from .piscripts import (GPIO, get_all_pins, get_scripts, pin_names, script_2)


init = True


def main():
    global init
    global pins
    global scripts
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    pins = get_all_pins(init)
    scripts = get_scripts(init)
    os.system("sudo pigpiod")
    os.system("gotty bash &")  # permit writes with -w

    # Call start config here:

    script_2()
    init = False


main()
