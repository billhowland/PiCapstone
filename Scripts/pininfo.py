import RPi.GPIO as GPIO
# from App import pimain
from App.piscripts import *

# BUG: Does not clear test mode/blink!


def main():
    GPIO.setmode(GPIO.BCM)
    setup_call(False)

    print(pin_info)


main()
