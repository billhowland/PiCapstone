import os
from time import sleep
import socket
# Daemon must be started FIRST!:
os.system("sudo pigpiod")
import pigpio
pi = pigpio.pi()
os.system('gotty --config "/home/pi/.gotty" bash &')  # permit writes with -w
os.system('gotty --config "/home/pi/.gotty9001" cat &')


pins = []
pin_info = []
scripts = []
script_info = []
# pin order on display is set by the list order here:
# pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
# pin_names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
pin_names = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 22, 23, 24, 25, 26, 27, 2, 3, 14, 15, 16, 19, 20, 21]
script_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
script_names = ["Show Full Configuration", "GPIO Configuration", "Flash LEDs", "Hardware PWM Test", "Strobe LEDs", "Wave Test",
                "Software PWM LEDs", "Official PIGPIO Wave", "Script 9", "Script 10", "Script 11", "Script 12", "Script 13",
                "Script 14", "Script 15", "Script 16", "Script 17", "Script 18", "Script 19", "More Options"]
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
    # 40 = GPIO.SERIAL      2 = pi.ALT5
    # 41 = GPIO.SPI         3 = pi.ALT4
    # 42 = GPIO.I2C         4 = pi.ALT0
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
    h3 = pi.serial_open("/dev/ttyAMA0", 115200, 0)  # pins 14, 15
    pi.serial_write(h3, tty_msg)
    pi.serial_close(h3)


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
    elif num == 6:
        script_6()
    elif num == 7:
        script_7()
    elif num == 8:
        script_8()
    elif num == 9:
        script_9()
    elif num == 10:
        script_10()
    elif num == 11:
        script_11()
    elif num == 12:
        script_12()
    elif num == 13:
        script_13()
    elif num == 14:
        script_14()
    elif num == 15:
        script_15()
    elif num == 16:
        script_16()
    elif num == 17:
        script_17()
    elif num == 18:
        script_18()
    elif num == 19:
        script_19()
    elif num == 20:
        script_20()


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

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        pin_out_low(pin)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    sleep(0.25)

# --script 2-My Hat Configuration-------------------------------------------------------


def script_2():
    global pins
    set_running(2)
    clr_running(1)
    sleep(0.25)
    pi.wave_tx_stop()  # stop waveform
    pi.wave_clear()  # clear all waveforms

    for pin in pin_names:
        untest_pin(pin)
        set_not_used(pin)
    get_all_pins(init=True)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        pin_out_low(pin)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        set_used(pin)
        pud_up(pin)

    sleep(0.25)


# --script 3-All LEDs to Flash Mode-----------------------------------------------------


def script_3():
    global pins
    set_running(3)

    tty_message("Script 3: all pins to 'Test' mode at 750ms interval.")
    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        set_used(pin)
        # pi.set_PWM_frequency((pin), 10)
        # pi.set_PWM_dutycycle((pin), 128) # PWM 1/2 on
        test_pin(pin)
        sleep(.75)

    clr_running(3)
    tty_message("Script terminated.")

# --script 4 PWM Test-------------------------------------------------------------------


def script_4():
    if get_running(4):
        clr_running(4)
    else:
        tty_message("Script 4: PWM test.")
        set_running(4)
        for pin in pin_names:
            untest_pin(pin)
        get_all_pins(init=True)

        pwmPina = 12
        pwmPinb = 18
        pwmPinc = 13
        pwmPind = 19

        butPin = 17
        exitPin = 25

        for pin in pin_names:
            set_not_used(pin)

        used_Pins = [(pwmPina), (pwmPinb), (pwmPinc), (pwmPind), (butPin), (exitPin)]
        for pin in used_Pins:
            set_used(pin)

        # h = ()
        # h2 = ()
        # Pin Setup:
        # pi.set_mode((18), pigpio.ALT5)
        # set_pin_out(pwmPin)  # PWM pin set as output

        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        set_pin_out(pwmPina)
        pi.hardware_PWM((pwmPina), 1, 500000)  # 2Hz 50% dutycycle
        sleep(.125)
        set_pin_out(pwmPinc)
        pi.hardware_PWM((pwmPinc), 2, 500000)  # 2Hz 50% dutycycle

        set_pin_out(pwmPinb)
        pi.set_mode((pwmPinb), pigpio.ALT5)
        set_pin_out(pwmPind)
        pi.set_mode((pwmPind), pigpio.ALT5)
        # h2 = pi.i2c_open(1, 0x53)  # open device at address 0x53 on bus 1, pins 2 & 3
        # h = pi.spi_open(1, 50000, 3)  # This one works, pins 7, 8, 9, 10, 11
        # pi.spi_write(h, b'a')
        # spi_data = pi.spi_read(h, 1)

        tty_message("Hardware PWM on pins 12, 13, 18, 19")
        tty_message("Press GPIO 25 to terminate")
        tty_message("Press GPIO 17 to change duty cycle")

        while get_running(4) and read_pin(exitPin):
            pass

        pi.hardware_PWM((pwmPina), 0, 500000)
        pi.hardware_PWM((pwmPinc), 0, 500000)
        # pi.spi_close(h)
        # pi.i2c_close(h2)

        pud_up(pwmPinb)
        pud_up(pwmPinc)
        pin_out_low(pwmPina)
        pi.set_mode((19), pigpio.ALT0)
        tty_message("Script terminated.")
        sleep(.25)
        clr_running(4)
        script_2()

# --script 5 Strobe LEDs----------------------------------------------------------------


def script_5():
    if get_running(5):
        clr_running(5)
    else:
        set_running(5)
        script_2()
        tty_message("Script 5: one LED at a time...")
        tty_message("Back -n- Forth...")
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
        while get_running(5):
            for pin in LED_Pins:
                set_used(pin)
                pin_out_hi(pin)
                sleep(.05)
                pin_out_low(pin)
                # sleep(.1)
            for pin in reversed(LED_Pins):
                set_used(pin)
                pin_out_hi(pin)
                sleep(.05)
                pin_out_low(pin)

        clr_running(5)
        tty_message("Script terminated.")

# --script 6 PIGPIO Wave Test-----------------------------------------------------------


def script_6():
    if get_running(6):
        clr_running(6)
    else:
        set_running(6)
        script_2()
        tty_message("Script 6: wave test.")
        flash_500 = []  # flash every 500 ms
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
        for pin in LED_Pins:
            set_used(pin)
            set_pin_out(pin)
            # create a new flash function
            flash_500.append(pigpio.pulse(1 << (pin), 0,  100000))
            flash_500.append(pigpio.pulse(0, 1 << (pin),  100000))
        pi.wave_clear()
        pi.wave_add_generic(flash_500)  # 500 ms flashes
        f500 = pi.wave_create()  # create and save id
        tty_message(str(f500))  # returning 0

        # while get_running(6):
        #     pi.wave_send_repeat(f500)
        #     sleep(1.8)
            # pass

        pi.wave_send_repeat(f500)
        sleep(.1)

        # pi.wave_tx_stop()  # stop waveform
        # pi.wave_clear()  # clear all waveforms
        sleep(.25)
        clr_running(6)
        tty_message("Script terminated.")

# --script 7----------------------------------------------------------------------------


def script_7():
    global pins
    if get_running(7):
        clr_running(7)
    else:
        set_running(7)

        tty_message("Script 7: Software PWM at 20Hz.")
        tty_message("Back -n- Forth...")
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]

        while get_running(7):
            dc = 1
            for pin in LED_Pins:
                set_used(pin)
                pi.set_PWM_frequency((pin), 10)
                pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                dc = dc + 31
                if (dc == 256):
                    dc = 255
                sleep(.15)
            dc = 1
            for pin in reversed(LED_Pins):
                set_used(pin)
                pi.set_PWM_frequency((pin), 10)
                pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                dc = dc + 31
                if (dc == 256):
                    dc = 255
                sleep(.15)

    for pin in LED_Pins:
        pin_out_low(pin)
    clr_running(7)
    tty_message("Script terminated.")


# --script 8----------------------------------------------------------------------------


def script_8():
    set_running(8)
    tty_message("Script 8: PIGPIO Wave Test")
    sleep(.25)

    G1 = 4
    G2 = 5

    set_pin_out(G1)
    set_pin_out(G2)

    # pi.set_mode(G1, pigpio.OUTPUT)
    # pi.set_mode(G2, pigpio.OUTPUT)

    flash_500 = []  # flash every 500 ms
    flash_100 = []  # flash every 100 ms

    #                              ON     OFF  DELAY

    flash_500.append(pigpio.pulse(1 << G1, 0, 500000))
    flash_500.append(pigpio.pulse(0, 1 << G1, 500000))

    flash_100.append(pigpio.pulse(1 << G1, 1 << G2, 100000))
    flash_100.append(pigpio.pulse(1 << G2, 1 << G1, 100000))

    pi.wave_clear()  # clear any existing waveforms

    pi.wave_add_generic(flash_500)  # 500 ms flashes
    f500 = pi.wave_create()  # create and save id
    tty_message(str(flash_500))

    pi.wave_add_generic(flash_100)  # 100 ms flashes
    f100 = pi.wave_create()  # create and save id
    tty_message(str(flash_100))

    pi.wave_send_repeat(f500)
    sleep(4)
    pi.wave_send_repeat(f100)
    sleep(4)
    pi.wave_send_repeat(f500)
    sleep(4)

    pi.wave_tx_stop()  # stop waveform
    pi.wave_clear()  # clear all waveforms
    clr_running(8)


# --script 9----------------------------------------------------------------------------


def script_9():
    set_running(9)
    tty_message("Script 9 Not Implemented.")
    sleep(.25)
    clr_running(9)


# --script 10----------------------------------------------------------------------------


def script_10():
    set_running(10)
    tty_message("Script 10 Not Implemented.")
    sleep(.25)
    clr_running(10)


# --script 11----------------------------------------------------------------------------


def script_11():
    set_running(11)
    tty_message("Script 11 Not Implemented.")
    sleep(.25)
    clr_running(11)


# --script 12---------------------------------------------------------------------------


def script_12():
    set_running(12)
    tty_message("Script 12 Not Implemented.")
    sleep(.25)
    clr_running(12)


# --script 13---------------------------------------------------------------------------


def script_13():
    set_running(13)
    tty_message("Script 13 Not Implemented.")
    sleep(.25)
    clr_running(13)


# --script 14---------------------------------------------------------------------------


def script_14():
    set_running(14)
    tty_message("Script 14 Not Implemented.")
    sleep(.25)
    clr_running(14)


# --script 15---------------------------------------------------------------------------


def script_15():
    set_running(15)
    tty_message("Script 15 Not Implemented.")
    sleep(.25)
    clr_running(15)


# --script 16---------------------------------------------------------------------------


def script_16():
    set_running(16)
    tty_message("Script 16 Not Implemented.")
    sleep(.25)
    clr_running(16)


# --script 17---------------------------------------------------------------------------


def script_17():
    set_running(17)
    tty_message("Script 17 Not Implemented.")
    sleep(.25)
    clr_running(17)


# --script 18---------------------------------------------------------------------------


def script_18():
    set_running(18)
    tty_message("Script 18 Not Implemented.")
    sleep(.25)
    clr_running(18)


# --script 19---------------------------------------------------------------------------


def script_19():
    set_running(19)
    tty_message("Script 19 Not Implemented.")
    sleep(.25)
    clr_running(19)


# --script 20---------------------------------------------------------------------------


def script_20():
    set_running(20)
    tty_message("Script 20 Not Implemented.")
    sleep(.25)
    clr_running(20)
