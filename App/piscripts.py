import os
os.system("sudo pigpiod")
from time import sleep
import socket
import pigpio
pi = pigpio.pi()
os.system('gotty --config "/home/pi/.gotty" bash &')  # permit writes with -w
os.system('gotty --config "/home/pi/.gotty9001" cat &')
h3 = ()
h3 = pi.serial_open("/dev/ttyAMA0", 9600, 0)  # pins 14, 15

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
            pud = 'off'
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
    pi.set_mode((pin), pigpio.OUTPUT)


def pin_out_hi(pin):
    set_pin_out(pin)
    untest_pin(pin)
    pi.write((pin), 1)


def pin_out_low(pin):
    set_pin_out(pin)
    untest_pin(pin)
    pi.write((pin), 0)


def pin_tog(pin):
    if not get_testing(pin):
        if read_pin(pin) == 0:
            set_pin_out(pin)
            pi.write((pin), 1)
        elif read_pin(pin) == 1:
            set_pin_out(pin)
            pi.write((pin), 0)
# Inputs:


def set_pin_in(pin):
    pud = get_pud(pin)
    if pud == 'down':
        pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_DOWN)
    else:
        pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_UP)


def read_pin(pin):
    return pi.read(pin)

# Usage:


def pin_use(pin):
    return pi.get_mode(pin)
    # RPi.GPIO #            pigpio #
    # 0 = GPIO.OUT          0 = pi.INPUT
    # 1 = GPIO.IN           1 = pi.OUTPUT
    # 40 = GPIO.SERIAL      2 = pi.ALT5 PWM
    # 41 = GPIO.SPI         3 = pi.ALT4
    # 42 = GPIO.I2C         4 = pi.ALT0 SPI
    # 43 = GPIO.HARD_PWM    5 = pi.ALT1
    # -1 = GPIO.UNKNOWN     6 = pi.ALT2
    #                       7 = pi.ALT3

# pull_up_down


def pud_dn(pin):
    pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_DOWN)
    idx = get_pin_idx(pin)
    if pins[idx]['name'] not in [2, 3]:
        pins[idx]['pud'] = 'down'


def pud_up(pin):
    pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_UP)
    idx = get_pin_idx(pin)
    pins[idx]['pud'] = 'up'


def pud_off(pin):
    pi.set_mode((pin), pigpio.INPUT), pi.set_pull_up_down((pin), pigpio.PUD_OFF)
    idx = get_pin_idx(pin)
    pins[idx]['pud'] = 'off'


def tty_message(message):
    (_, _, ttynames) = next(os.walk("/dev/pts"))
    tty_msg = str.encode("\r\n" + "Msg:> " + message + "\r\n")
    for ttyname in ttynames:
        if ttyname != "ptmx":
            tty = os.open("/dev/pts/" + ttyname, os.O_RDWR)
            os.write(tty, tty_msg)
    pi.serial_write(h3, tty_msg)

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
        untest_pin(pin)
        set_used(pin)
    get_all_pins(init=True)


# --script 2----------------------------------------------------------------------------


def script_2():
    global pins
    set_running(2)
    clr_running(1)
    sleep(0.25)

    for pin in pin_names:
        untest_pin(pin)
    get_all_pins(init=True)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_low(pin)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    Unused_Pins = [14, 15, 19, 16, 20, 21, 2, 3]
    for pin in Unused_Pins:
        set_not_used(pin)
    sleep(0.25)


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
        get_all_pins(init=True)

        used_Pins = [2, 3, 7, 8, 9, 10, 11, 13, 14, 15, 17, 18]
        for pin in used_Pins:
            set_used(pin)

        spi_Pins = [7, 8, 9, 10, 11]
        for pin in spi_Pins:
            pi.set_mode((pin), pigpio.ALT0)
            # pud_off(pin)

        # ser_Pins = [14, 15]
        # for pin in ser_Pins:
        #     pi.set_mode((pin), pigpio.ALT0)
            # pud_off(pin)

        Unused_Pins = [4, 5, 6, 12, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        for pin in Unused_Pins:
            set_not_used(pin)
            # set_pin_in(pin)

        h = ()
        h2 = ()
        # h3 = ()
        pwmPin = 18
        butPin = 17
        exitPin = 13

        # Pin Setup:
        # pi.set_mode((18), pigpio.ALT5)
        # set_pin_out(pwmPin)  # PWM pin set as output

        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        set_pin_out(pwmPin)
        pi.hardware_PWM(18, 1, 500000)  # 2Hz 50% dutycycle

        h2 = pi.i2c_open(1, 0x53)  # open device at address 0x53 on bus 1, pins 2 & 3
        h = pi.spi_open(1, 50000, 3)  # This one works, pins 7, 8, 9, 10, 11
        # h3 = pi.serial_open("/dev/ttyAMA0", 9600, 0)  # pins 14, 15
        # pi.serial_write(h3, "this is a test and only a test")
        pi.spi_write(h, b'a')
        spi_data = pi.spi_read(h, 1)

        tty_message("Hardware PWM on pin 18")

        while get_running(4) and read_pin(exitPin):
            pi.hardware_PWM(18, 1, 500000)

        pi.hardware_PWM(18, 0, 500000)
        pi.spi_close(h)
        pi.i2c_close(h2)
        # pi.serial_close(h3)
        tty_message("Script terminated.")
        sleep(.25)
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
