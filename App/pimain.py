from .piscripts import (get_all_pins, get_scripts, pin_names, script_2)
import pigpio
pi = pigpio.pi()
init = True


def main():
    global init
    global pins
    global scripts
    
    pins = get_all_pins(init)
    scripts = get_scripts(init)

    # Call start config here:
    script_2()
    init = False


main()
