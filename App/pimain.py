from .piscripts import (get_all_pins, get_scripts, pin_names, script_2)
import pigpio
pi = pigpio.pi()
init = True


def main():
    global init
    global pins
    global scripts
    # GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO  # CHANGE
    # GPIO.setwarnings(False)  # Allows us to repeat config without errors  # CHANGE

    for pin in pin_names:
        if pin not in [2, 3]:
            # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # CHANGE
            pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_DOWN)
        else:
            # GPIO.setup(pin, GPIO.IN)  # CHANGE
            pi.set_mode((pin), pigpio.INPUT)
    pins = get_all_pins(init)
    scripts = get_scripts(init)

    # Call start config here:
    script_2()
    init = False


main()
