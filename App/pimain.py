# import os
from .piscripts import (GPIO, get_all_pins, pin_names)


def main():
    global pins
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    pins = get_all_pins(init=True)
    # os.system("gotty bash &")


main()
