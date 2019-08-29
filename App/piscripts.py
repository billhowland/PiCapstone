from time import sleep
import RPi.GPIO as GPIO
import socket
# from .config1 import pin_info
# import time
# import pigpio

pins = []
pin_info = []
script_info = []
# pin order on display is set by the list order here:
# pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
pin_names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
running = False
# script_funcs = {1:script_1(), 2:script_2(), 3:script_3(), 4:script_4(),
# 5:script_5(), 6:script_6(), 7:script_7(), 8:script_8(), 9:script_9(),
# 10:script_10(), 11:script_11(), 12:script_12(), 13:script_13(), 14:script_14(),
# 15:script_15(), 16:script_16(), 17:script_17(), 18:script_18()}

# pi = pigpio.pi()
# pi.hardware_PWM(18, 2, 500000)  # 2Hz 50% dutycycle

# URL -> View -> Piscript


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except ValueError:
        IP = '127.0.0.1'
    finally:
        s.close()
        return IP


def get_pin_idx(pin):
    return pin_names.index(pin)


def blink_pin(pin):  # Not currently used
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
            testing = False
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
                'testing': testing,
            })
        else:
            test = get_test(pin)
            testing = get_testing(pin)
            pud = get_pud(pin)
            used = get_used(pin)
            pin_info.append({
                'name': pin,
                'func': func,
                'in_lvl': in_lvl,
                'pud': pud,
                'test': test,
                'used': used,
                'testing': testing,
            })

    pins = pin_info
    return pins

# Outputs:


def test_pin(pin):  # sets the test flag...
    idx = get_pin_idx(pin)
    pins[idx]['test'] = True


def get_test(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['test']


def get_testing(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['testing']


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


def pin_tog(pin):
    if not get_testing(pin):
        if read_pin(pin) == 0:
            set_pin_out(pin)
            GPIO.output((pin), GPIO.HIGH)
        elif read_pin(pin) == 1:
            set_pin_out(pin)
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


def do_script(num):
    # script_funcs[num]

    if num == 1:
        script_1()
    elif num == 2:
        script_2()
    elif num == 3:
        script_3()

# --script 1----------------------------------------------------------------------------


def script_1():
    global pins
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            pud_dn(pin)
        else:
            GPIO.setup(pin, GPIO.IN)
            pud_up(pin)
        untest_pin(pin)
        set_used(pin)
        pin_out_low(pin)
        set_pin_in(pin)
    get_all_pins(init=True)
    running = False


# --script 2----------------------------------------------------------------------------


def script_2():
    global pins
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        untest_pin(pin)
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    get_all_pins(init=True)

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
    running = False


# --script 2----------------------------------------------------------------------------


def script_3():
    global pins
    GPIO.setmode(GPIO.BCM)  # required by RPi.GPIO
    GPIO.setwarnings(False)  # Allows us to repeat config without errors

    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    get_all_pins(init=True)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    Unused_Pins = [19, 16, 20, 21, 2, 3]
    for pin in Unused_Pins:
        set_not_used(pin)
        set_pin_in(pin)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_hi(pin)
        test_pin(pin)
        sleep(.25)

    running = False
