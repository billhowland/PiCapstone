from time import sleep
import RPi.GPIO as GPIO
import socket
import os
os.system("sudo pigpiod")
os.system('gotty --config "/home/pi/.gotty" bash &')  # permit writes with -w
os.system('gotty --config "/home/pi/.gotty9001" cat &')
# import time
import pigpio
pi = pigpio.pi()


pins = []
pin_info = []
scripts = []
script_info = []
# pin order on display is set by the list order here:
# pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
pin_names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
script_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
script_names = ["Default Configuration", "My Hat Configuration", "Test Hat LEDs", "PWM Test", "Strobe", "Script 6",
                "Script 7", "Script 8", "Script 9", "Script 10", "Script 11", "Script 12", "Script 13",
                "Script 14", "Script 15", "Script 16", "Script 17", "Script 18", "Script 19", "Script 20"]
script_urls = ["script1", "script2", "script3", "script4", "script5",
               "script6", "script7", "script8", "script9", "script10", "script11",
               "script12", "script13", "script14", "script15", "script16", "script17", "script18", "script19", "script20"]


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


def tty_message(message):
    (_, _, ttynames) = next(os.walk("/dev/pts"))
    tty_msg = str.encode("\r\n" + "Msg:> " + message + "\r\n")
    for ttyname in ttynames:
        if ttyname != "ptmx":
            tty = os.open("/dev/pts/" + ttyname, os.O_RDWR)
            os.write(tty, tty_msg)


def get_scripts(init):
    global scripts
    script_info = []
    for scr in script_nums:
        if init:
            name = get_name(scr)
            url = get_url(scr)
            running = False
            script_info.append({
                'num': scr,
                'name': name,
                'url': url,
                'running': running,
                })
        else:
            name = get_name(scr)
            url = get_url(scr)
            running = get_running(scr)
            script_info.append({
                'num': scr,
                'name': name,
                'url': url,
                'running': running,
                })
    scripts = script_info


def get_scr_idx(scr):
    return script_nums.index(scr)


def get_running(scr):
    scr = scripts[get_scr_idx(scr)]
    return scr['running']


def get_name(scr):
    scr = script_names[get_scr_idx(scr)]
    return scr


def get_url(scr):
    scr = script_urls[get_scr_idx(scr)]
    return scr


def set_running(scr):
    scr = get_scr_idx(scr)
    scripts[scr]['running'] = True


def clr_running(scr):
    scr = get_scr_idx(scr)
    scripts[scr]['running'] = False


def do_script(num):
    # script_funcs[num]

    if num == 1:
        script_1()
    elif num == 2:
        script_2()
    elif num == 3:
        script_3()
    elif num == 4:
        script_4()
    elif num == 5:
        script_5()

# --script 1----------------------------------------------------------------------------


def script_1():
    global pins
    set_running(1)
    clr_running(2)
    sleep(0.25)

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

    sleep(0.25)
    # clr_running(1)


# --script 2----------------------------------------------------------------------------


def script_2():
    global pins
    set_running(2)
    clr_running(1)
    sleep(0.25)

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

    sleep(0.25)
    # clr_running(2)


# --script 3----------------------------------------------------------------------------


def script_3():
    global pins
    set_running(3)
    script_2()
    tty_message("All pins to 'Test' mode at 250ms interval.")
    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_hi(pin)
        test_pin(pin)
        sleep(.25)

    clr_running(3)
    tty_message("Script terminated.")

# --script 4----------------------------------------------------------------------------


def script_4():
    if get_running(4):
        clr_running(4)
    else:
        set_running(4)
        for pin in pin_names:
            untest_pin(pin)
            if pin not in [2, 3]:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(pin, GPIO.IN)
        get_all_pins(init=True)

        used_Pins = [2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 17]
        for pin in used_Pins:
            set_used(pin)
            pud_up(pin)

        Unused_Pins = [6, 12, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        for pin in Unused_Pins:
            set_not_used(pin)
            set_pin_in(pin)

        h = ()
        h2 = ()
        h3 = ()
        pwmPin = 5
        ledPin = 4
        butPin = 17
        exitPin = 13

        dc = 80  # duty cycle (0-100) for PWM pin

        # Pin Setup:

        set_pin_out(ledPin)  # LED pin set as output
        set_pin_out(pwmPin)  # PWM pin set as output
        pwm = GPIO.PWM(pwmPin, 5)  # Initialize PWM on pwmPin 100Hz frequency
        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        # Initial state for LEDs:
        pin_out_low(ledPin)
        pwm.start(dc)
        set_pin_out(18)
        pi.hardware_PWM(18, 1, 500000)  # 2Hz 50% dutycycle
        h2 = pi.i2c_open(1, 0x53)  # open device at address 0x53 on bus 1
        h = pi.spi_open(1, 50000, 3)  # This one works!
        h3 = pi.serial_open("/dev/serial0", 9600)
        # pi.spi_write(h, b'a')
        # spi_data = pi.spi_read(h, 1)

        tty_message("Hardware PWM on pin 18")

        while get_running(4) and read_pin(exitPin):
            if read_pin(butPin) == 0:
                pwm.ChangeDutyCycle(dc)
                pin_out_low(ledPin)
            else:
                pwm.ChangeDutyCycle(100-dc)
                pin_out_hi(ledPin)
                sleep(0.1)
                pin_out_low(ledPin)
                sleep(0.1)

        pwm.stop()  # stop PWM
        pi.hardware_PWM(18, 0, 500000)
        pi.spi_close(h)
        pi.i2c_close(h2)
        pi.serial_close(h3)
        tty_message("Script terminated.")
        script_2()
        #    GPIO.cleanup() # cleanup all GPIO
        clr_running(4)

# --script 5----------------------------------------------------------------------------


def script_5():
    if get_running(5):
        clr_running(5)
    else:
        set_running(5)
        script_2()
        tty_message("One LED at a time...")
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
        while get_running(5):
            for pin in LED_Pins:
                set_used(pin)
                pin_out_hi(pin)
                sleep(.25)
                pin_out_low(pin)
                # sleep(.1)

        clr_running(5)
        tty_message("Script terminated.")
