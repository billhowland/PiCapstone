import RPi.GPIO as GPIO
from App.piscripts import set_not_used
pins = []

def main():
    global pins
    GPIO.setmode(GPIO.BCM)
    # pin_names = [4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 2, 3] (24 pins)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output((pin), GPIO.HIGH)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    Unused_Pins = [19, 16, 20, 21, 2, 3]
    for pin in Unused_Pins:
        GPIO.setup(pin, GPIO.IN)
        set_not_used(pin)

main()
