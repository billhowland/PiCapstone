import os
from .piscripts import (GPIO, get_all_pins, pin_names, set_used, pin_out_low, pud_up, set_not_used, set_pin_in)


def main():
    global pins
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    get_all_pins(True)  # since local pin_info = [], pins set to [] here.

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_low(pin)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    Unused_Pins = [19, 16, 20, 21, 2, 3]
    for pin in Unused_Pins:
        set_not_used(pin)
        set_pin_in(pin)

#  Below is generic setup:

    # for pin in pin_names:
    #     if pin not in [2, 3]:
    #         GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #     else:
    #         GPIO.setup(pin, GPIO.IN)
    # pins = get_all_pins(init=True)
    # os.system("gotty bash &")


main()
