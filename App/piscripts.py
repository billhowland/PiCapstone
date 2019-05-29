from time import sleep
import RPi.GPIO as GPIO
import os

test = 0
pins = []


def blink_pin(pin):
    global test
    GPIO.setup((pin), GPIO.OUT)
    while test == 1:
        print(test)
        if GPIO.gpio_function(pin) == 0 and test == 1:
            GPIO.output(pin, GPIO.HIGH)
            sleep(1)
            if GPIO.gpio_function(pin) == 0 and test == 1:
                GPIO.output(pin, GPIO.LOW)
                sleep(1)
            else:
                test = 0
        else:
            test = 0
            continue


def get_pud(pin):
    pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    pin = pins[pin_names.index(pin)]
    return pin['pud']


def get_all_pins(init=False):
    global pins
    pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    pin_info = []
    for pin in pin_names:
        func = pin_use(pin)
        in_lvl = read_pin(pin)
        if init:
            if pin not in [2, 3]:
                pud = 'down'
            else:
                pud = 'up'
        else:
            pud = get_pud(pin)

        pin_info.append({
            'name': pin,
            'func': func,
            'in_lvl': in_lvl,
            'pud': pud,
        })
    pins = pin_info
    return pins

# Outputs:


def test_pin(pin):
    global test
    test = 1
    blink_pin(pin)


def untest_pin(pin):
    print("untest called")
    global test
    test = 0


def set_pin_out(pin):
    GPIO.setup((pin), GPIO.OUT)


def pin_out_hi(pin):
    untest_pin(pin)
    GPIO.output((pin), GPIO.HIGH)


def pin_out_low(pin):
    untest_pin(pin)
    GPIO.output((pin), GPIO.LOW)

# Inputs:


def set_pin_in(pin):
    pud = get_pud(pin)
    if pud == 'down':
        GPIO.setup((pin), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    else:
        GPIO.setup((pin), GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_pin(pin):
    return GPIO.input(pin)

# Usage:


def pin_use(pin):
    return GPIO.gpio_function(pin)
    # 0 = GPIO.OUT
    # 1 = GPIO.IN
    # 40 = GPIO.SERIAL
    # 41 = GPIO.SPI
    # 42 = GPIO.I2C
    # 43 = GPIO.HARD_PWM
    # -1 = GPIO.UNKNOWN

# pull_up_down


def pud_dn(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    idx = pin_names.index(pin)
    pins[idx]['pud'] = 'down'


def pud_up(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    idx = pin_names.index(pin)
    pins[idx]['pud'] = 'up'


def main():
    global pins
    GPIO.setmode(GPIO.BCM)
    pin_names = [4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(3, GPIO.IN)
    for pin in pin_names:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    os.system("gotty bash")
    pins = get_all_pins(init=True)
    # URL -> View -> Piscript


main()
