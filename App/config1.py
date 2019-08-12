import RPi.GPIO as GPIO
# from App import pimain
from piscripts.py import *

pin_info = []

# BUG: Does not clear test mode/blink!


def main():
    GPIO.setmode(GPIO.BCM)
    setup_call(True)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_low(pin)  # fails to untest pin

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    Unused_Pins = [19, 16, 20, 21, 2, 3]
    for pin in Unused_Pins:
        set_not_used(pin)
        set_pin_in(pin)

    print(pin_info)

    setup_call(False)


main()
