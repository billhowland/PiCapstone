from time import sleep
import RPi.GPIO as GPIO
import os  # Yes, this is used!
import socket
from config1 import (pin_info)
# import time
# import pigpio

pins = []
# pin_info = []

# pin order on display is set by the list order here:
# pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
pin_names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
# pi = pigpio.pi()
# pi.hardware_PWM(18, 2, 500000)  # 2Hz 50% dutycycle

# URL -> View -> Piscript


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
        return IP


def get_pin_idx(pin):
    return pin_names.index(pin)


def blink_pin(pin):
    # global test
    GPIO.setup((pin), GPIO.OUT)
    while pins[get_pin_idx(pin)]['test']:
        if GPIO.gpio_function(pin) == 0:
            GPIO.output(pin, GPIO.HIGH)
        sleep(1)
        if GPIO.gpio_function(pin) == 0:
            GPIO.output(pin, GPIO.LOW)
        sleep(1)


def get_pud(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['pud']


def get_used(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['used']


def set_used(pin):
    idx = get_pin_idx(pin)
    pins[idx]['used'] = True


def set_not_used(pin):
    idx = get_pin_idx(pin)
    pins[idx]['used'] = False


def get_all_pins(init=False):
    global pins

    for pin in pin_names:
        func = pin_use(pin)
        in_lvl = read_pin(pin)
        if init:

            used = True
            test = False
            if pin not in [2, 3]:
                pud = 'down'
            else:
                pud = 'up'
            pin_info.append({
                'name': pin,
                'func': func,
                'in_lvl': in_lvl,
                'pud': pud,
                'test': test,
                'used': used,
            })
        else:
            test = get_test(pin)
            pud = get_pud(pin)
            used = get_used(pin)
            pin_info.append({
                'name': pin,
                'func': func,
                'in_lvl': in_lvl,
                'pud': pud,
                'test': test,
                'used': used,
            })

    pins = pin_info
    return pins

# Outputs:


def test_pin(pin):
    # global test
    # test = 1
    idx = get_pin_idx(pin)
    pins[idx]['test'] = True
    blink_pin(pin)


def get_test(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['test']


def untest_pin(pin):
    idx = get_pin_idx(pin)
    pins[idx]['test'] = False


def set_pin_out(pin):
    GPIO.setup((pin), GPIO.OUT)


def pin_out_hi(pin):
    set_pin_out(pin)
    untest_pin(pin)
    GPIO.output((pin), GPIO.HIGH)


def pin_out_low(pin):
    set_pin_out(pin)
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
    idx = get_pin_idx(pin)
    if pins[idx]['name'] not in [2, 3]:
        pins[idx]['pud'] = 'down'


def pud_up(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    idx = get_pin_idx(pin)
    pins[idx]['pud'] = 'up'


def setup_call(mode):
    global pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    if mode:
        for pin in pin_names:
            if pin not in [2, 3]:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(pin, GPIO.IN)
        pins = get_all_pins(init=True)

    else:
        pins = get_all_pins(init=False)
