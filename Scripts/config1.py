import RPi.GPIO as GPIO
# from App import pimain
from ..App.piscripts import *


print(pin_info)  # is empty here
print(pins)  # is empty here


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    get_all_pins(True)  # since local pin_info = [], pins set to [] here.
    print(pin_info)  # local pin_info compiled here
    print(pins)  # still empty

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

    print(pin_info)  # this pin_info is local to config1.py and not the same as pin_info inside piscripts.py
    print(pins)  # is never assigned

    get_all_pins(False)  # this will build a new


main()
