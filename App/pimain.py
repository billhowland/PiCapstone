from .piscripts import (get_all_pins, get_scripts, script_0, script_2)
import pigpio
pi = pigpio.pi()
init = True


def main():
    global init
    global pins
    global scripts

    spi_Pins = [16, 19, 20, 21]  # SPI1
    for pin in spi_Pins:
        pi.set_mode((pin), pigpio.ALT0)

    # spi_Pins = [7, 8, 9, 10, 11]  # SPI0
    # for pin in spi_Pins:
    #     pi.set_mode((pin), pigpio.ALT0)

    ser_Pins = [14, 15]
    for pin in ser_Pins:
        pi.set_mode((pin), pigpio.ALT0)

    i2c_Pins = [2, 3]
    for pin in i2c_Pins:
        pi.set_mode((pin), pigpio.ALT0)

    pins = get_all_pins(init)
    scripts = get_scripts(init)

    # Call start config here:
    script_0()
    script_2()
    init = False


main()
