import os
from time import sleep
import socket
# Daemon must be started FIRST!:
os.system("sudo pigpiod")
import pigpio  # NOT an error, DO NOT MOVE!
pi = pigpio.pi()
os.system('gotty --config "/home/pi/.gotty" bash &')  # permit writes with -w
os.system('gotty --config "/home/pi/.gotty9001" cat &')
os.system('python3 picam_8000.py &')

pins = []
pin_info = []
scripts = []
script_info = []
pwms = []
pwm_info = []
# pin order on display is set by the list order here:
# pin_names = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
# pin_names = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
# pin_names = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 22, 23, 24, 25, 26, 27, 2, 3, 14, 15, 16, 19, 20, 21]
pin_names = [4, 10, 9, 8, 11, 7, 5, 6, 12, 13, 26, 25, 27, 24, 23, 22, 18, 17, 2, 3, 14, 15, 16, 19, 20, 21]
pwm_names = [4, 10, 9, 8, 11, 7, 5, 6, 12, 13, 26, 25, 27, 24, 23, 22, 18, 17, 2, 3, 14, 15, 16, 19, 20, 21]
script_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
               22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
script_names = ["Full Configuration", "GPIO Configuration", "Flash LEDs", "Hardware PWM Test",
                "Strobe LEDs", "Wave Test", "Software PWM LEDs", "Script 8",
                "Dimmer", "Script 10", "Script 11", "Script 12", "Script 13", "Script 14",
                "Script 15", "Script 16", "SPI Menu", "Show Pinout", "Hardware PWM", "Software PWM",
                "Script 21", "Script 22", "Script 23", "Script 24", "Script 25", "Script 26",
                "Script 27", "Script 28", "Script 29", "Script 30", "Script 31", "Script 32",
                "Script 33", "Script 34", "Script 35", "Script 36", "Script 37", "PiCamera",
                "Hardware Clock", "Clear All"]
script_urls = ["script1", "script2", "script3", "script4", "script5",
               "script6", "script7", "script8", "script9", "script10", "script11",
               "script12", "script13", "script14", "script15", "script16", "script17",
               "script18", "script19", "script20", "script21", "script22", "script23",
               "script24", "script25", "script26", "script27", "script28", "script29",
               "script30", "script31", "script32", "script33", "script34", "script35",
               "script36", "script37", "script38", "script39", "script40"]
IP = '127.0.0.1'

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


def get_hfrq(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['hfrq']


def get_hdc(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['hdc']


def set_hfrq(pin, hfrq):
    idx = get_pwm_idx(pin)
    pins[idx]['hfrq'] = hfrq


def set_hdc(pin, hdc):
    idx = get_pwm_idx(pin)
    pins[idx]['hdc'] = hdc


def start_hpwm(pin):
    hfrq = get_hfrq(pin)
    hdc = get_hdc(pin)
    pi.hardware_PWM((pin), (hfrq), (hdc))


def stop_hpwm(pin):
    hfrq = 0
    hdc = 0
    pi.hardware_PWM((pin), (hfrq), (hdc))


def get_pud(pin):
    pin = pins[get_pin_idx(pin)]
    return pin['pud']


def get_frq(pin):
    frq = pi.get_PWM_frequency(pin)
    return frq


def set_frq(pin, frq):
    pi.set_PWM_frequency(pin, frq)  # returns nearest good frequency


def set_cfrq(pin, frq):
    if frq < 4689:
        frq = 4689
    pi.hardware_clock(pin, frq)  # returns 0 if OK


def get_dc(pin):
    try:
        dc = pi.get_PWM_dutycycle(pin)
    except pigpio.error:
        dc = 0
    return dc


def set_dc(pin, dc):
    pi.set_PWM_dutycycle(pin, dc)


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
            frq = 10
            set_frq(pin, frq)
            dc = 0
            hfrq = 10
            hdc = 500000
            pin_info.append({
                'name': pin,
                'func': func,
                'in_lvl': in_lvl,
                'pud': pud,
                'test': test,
                'used': used,
                'testing': testing,
                'frq': frq,
                'dc': dc,
                'hfrq': hfrq,
                'hdc': hdc,
            })
        else:
            test = get_test(pin)
            testing = get_testing(pin)
            pud = get_pud(pin)
            used = get_used(pin)
            frq = get_frq(pin)
            dc = get_dc(pin)
            hfrq = get_hfrq(pin)
            hdc = get_hdc(pin)
            pin_info.append({
                'name': pin,
                'func': func,
                'in_lvl': in_lvl,
                'pud': pud,
                'test': test,
                'used': used,
                'testing': testing,
                'frq': frq,
                'dc': dc,
                'hfrq': hfrq,
                'hdc': hdc,
            })

    pins = pin_info
    # return pins

# Outputs:


def test_pin(pin):  # sets the test flag...
    idx = get_pin_idx(pin)
    pins[idx]['test'] = True
    # blink_pin(pin)


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


def blink_pin(pin):  # Only blinks one pin at a time because each new wave terminates the previous
    flash_pin = []
    set_used(pin)
    set_pin_out(pin)
    flash_pin.append(pigpio.pulse(1 << (pin), 0,  100000))
    flash_pin.append(pigpio.pulse(0, 1 << (pin),  100000))
    # pi.wave_clear()
    pi.wave_add_generic(flash_pin)  # 500 ms flashes
    f500 = pi.wave_create()  # create and save id
    tty_message(str(f500))
    pi.wave_send_repeat(f500)
    sleep(.1)

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
    # pigpio #
    # 0 = pi.INPUT
    # 1 = pi.OUTPUT
    # 2 = pi.ALT5
    # 3 = pi.ALT4
    # 4 = pi.ALT0
    # 5 = pi.ALT1
    # 6 = pi.ALT2
    # 7 = pi.ALT3

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
    tty_msg = str.encode("\r\n" + "-> " + message + " <-\r\n")
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


def get_pwms():
    global pwms
    pwm_info = []
    for pwm in pwm_names:
        func = pin_use(pwm)
        frq = get_frq(pwm)
        dc = get_dc(pwm)
        hfrq = get_hfrq(pwm)
        hdc = get_hdc(pwm)
        pwm_info.append({
            'name': pwm,
            'func': func,
            'sfrq': frq,
            'sdc': dc,
            'shfrq': hfrq,
            'shdc': hdc,
            })
    pwms = pwm_info


def get_scr_idx(scr):
    return script_nums.index(scr)


def get_pwm_idx(pwm):
    return pwm_names.index(pwm)


def get_running(scr):
    scr = scripts[get_scr_idx(scr)]
    return scr['running']


def get_name(scr):
    scr = script_names[get_scr_idx(scr)]
    return scr


def get_url(scr):
    scr = script_urls[get_scr_idx(scr)]
    return scr


def get_pwm(pwm):
    pwm = pwm_names[get_pwm_idx(pwm)]
    return pwm


def set_running(scr):
    scr = get_scr_idx(scr)
    scripts[scr]['running'] = True


def clr_running(scr):
    scr = get_scr_idx(scr)
    scripts[scr]['running'] = False


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

# --script 4 Hardware PWM Test----------------------------------------------------------


def script_4():
    pwmPina = 12
    pwmPinb = 18
    pwmPinc = 13
    pwmPind = 19
    butPin = 17
    exitPin = 25
    pud_up(butPin)  # Button pin set as input w/ pull-up
    pud_up(exitPin)

    if  get_running(4):
        clr_running(4)
        stop_hpwm(pwmPina)
        stop_hpwm(pwmPinb)
        stop_hpwm(pwmPinc)
        stop_hpwm(pwmPind)
        pi.set_mode((pwmPina), pigpio.OUTPUT)
        pi.set_mode((pwmPinb), pigpio.INPUT)
        pi.set_mode((pwmPinc), pigpio.INPUT)
        pi.set_mode((pwmPind), pigpio.OUTPUT)
        pud_up(pwmPinb)
        pud_up(pwmPinc)
        pin_out_low(pwmPina)
        pin_out_low(pwmPind)
        pi.set_mode((19), pigpio.ALT0)
        tty_message("Script terminated.")
        if get_running(1):
            script_1()
        if get_running(2):
            script_2()
        clr_running(4)

    else:
        tty_message("Script 4: Hardware PWM test.")
        set_running(4)
        for pin in pin_names:
            untest_pin(pin)
        get_all_pins(init=True)

        for pin in pin_names:
            set_not_used(pin)

        used_Pins = [(pwmPina), (pwmPinb), (pwmPinc), (pwmPind), (butPin), (exitPin)]
        for pin in used_Pins:
            set_used(pin)

        sleep(.125)
        set_pin_out(pwmPind)
        set_hfrq(pwmPind, 2)
        set_hdc(pwmPind, 500000)
        set_pin_out(pwmPinb)

        start_hpwm(pwmPind)
        set_hfrq(pwmPinb, 1)
        set_hdc(pwmPinb, 500000)
        start_hpwm(pwmPinb)

        set_pin_out(pwmPina)
        pi.set_mode((pwmPina), pigpio.ALT0)
        set_pin_out(pwmPinc)
        pi.set_mode((pwmPinc), pigpio.ALT0)

        tty_message("Hardware PWM on pins 12, 13, 18, 19")
        tty_message("Press GPIO 25 to terminate")
        tty_message("Press GPIO 17 button for fun")

        while get_running(4):
            if read_pin(butPin):
                set_hfrq(pwmPinb, 1)
                set_hdc(pwmPinb, 500000)
            elif read_pin(butPin) == 0:
                set_hfrq(pwmPinb, 5)
                set_hdc(pwmPinb, 100000)
            if read_pin(exitPin):
                start_hpwm(pwmPinb)
            elif read_pin(exitPin) == 0:
                script_4()



# --script 5 Strobe LEDs----------------------------------------------------------------


def script_5():
    if get_running(5):
        clr_running(5)
    else:
        set_running(5)
        tty_message("Script 5: one LED at a time...")
        tty_message("Back -n- Forth...")
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]

        butPin = 17
        exitPin = 25
        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        while get_running(5) and read_pin(exitPin):
            for pin in LED_Pins:
                set_used(pin)
                pin_out_hi(pin)
                sleep(.04)
                pin_out_low(pin)
                # sleep(.1)
            for pin in reversed(LED_Pins):
                set_used(pin)
                pin_out_hi(pin)
                sleep(.04)
                pin_out_low(pin)

        clr_running(5)
        tty_message("Script terminated.")

# --script 6 PIGPIO Wave Test-----------------------------------------------------------


def script_6():
    if get_running(6):
        clr_running(6)
    else:
        set_running(6)
        tty_message("Script 6: wave test.")
        flash_500 = []  # flash every 500 ms
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]

        butPin = 17
        exitPin = 25
        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        for pin in LED_Pins:
            set_used(pin)
            set_pin_out(pin)
            # create a new flash function
            flash_500.append(pigpio.pulse(1 << (pin), 0,  10000))
            flash_500.append(pigpio.pulse(0, 1 << (pin),  10000))
        pi.wave_clear()
        pi.wave_add_generic(flash_500)  # 500 ms flashes
        f500 = pi.wave_create()  # create and save id
        # tty_message(str(f500))  # returning 0

        while get_running(6) and read_pin(exitPin):
            pi.wave_send_repeat(f500)
            sleep(.18)

        pi.wave_tx_stop()  # stop waveform
        pi.wave_clear()  # clear all waveforms
        sleep(.25)
        clr_running(6)
        tty_message("Script terminated.")

# --script 7: Software PWM Test----------------------------------------------------------


def script_7():
    global pins
    if get_running(7):
        clr_running(7)
        clr_running(20)
    else:
        set_running(7)

        tty_message("Script 7: Software PWM at 20Hz.")
        tty_message("Back -n- Forth...")
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
        for pin in LED_Pins:
            set_used(pin)
            pi.set_PWM_frequency((pin), 10)

        butPin = 17
        exitPin = 25
        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        while get_running(7) and read_pin(exitPin):
            dc = 1
            for pin in LED_Pins:
                pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                dc = dc + 31
                if (dc == 256):
                    dc = 255
                sleep(.15)
            dc = 1
            for pin in reversed(LED_Pins):
                pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                dc = dc + 31
                if (dc == 256):
                    dc = 255
                sleep(.15)
            get_pwms()

    for pin in LED_Pins:
        pin_out_low(pin)
    clr_running(7)
    tty_message("Script terminated.")


# --script 8: ---------------------------------------------------------------------------

def script_8():
    set_running(8)
    tty_message("Script 8 Not Implemented.")
    sleep(.25)
    clr_running(8)

# Original PIGPIO Wave Example:

    # G1 = 4
    # G2 = 5
    #
    # set_pin_out(G1)
    # set_pin_out(G2)
    #
    # flash_500 = []  # flash every 500 ms
    # flash_100 = []  # flash every 100 ms
    #
    # #                              ON     OFF  DELAY
    #
    # flash_500.append(pigpio.pulse(1 << G1, 0, 500000))
    # flash_500.append(pigpio.pulse(0, 1 << G1, 500000))
    #
    # flash_100.append(pigpio.pulse(1 << G1, 1 << G2, 100000))
    # flash_100.append(pigpio.pulse(1 << G2, 1 << G1, 100000))
    #
    # pi.wave_clear()  # clear any existing waveforms
    #
    # pi.wave_add_generic(flash_500)  # 500 ms flashes
    # f500 = pi.wave_create()  # create and save id
    # # tty_message(str(flash_500))
    #
    # pi.wave_add_generic(flash_100)  # 100 ms flashes
    # f100 = pi.wave_create()  # create and save id
    # # tty_message(str(flash_100))
    #
    # pi.wave_send_repeat(f500)
    # sleep(4)
    # pi.wave_send_repeat(f100)
    # sleep(4)
    # pi.wave_send_repeat(f500)
    # sleep(4)
    #
    # pi.wave_tx_stop()  # stop waveform
    # pi.wave_clear()  # clear all waveforms
    # clr_running(8)


# --script 9----------------------------------------------------------------------------


def script_9():
    global pins
    if get_running(9):
        clr_running(9)
        clr_running(20)
    else:
        set_running(9)
        tty_message("Script 9: Software PWM dimmer")

        ALED_Pins = [4, 9, 11, 5, 12]
        for pin in ALED_Pins:
            set_used(pin)
            pi.set_PWM_frequency((pin), 100)

        BLED_Pins = [10, 8, 7, 6]
        for pin in BLED_Pins:
            set_used(pin)
            pi.set_PWM_frequency((pin), 100)

        butPin = 17
        exitPin = 25
        pud_up(butPin)  # Button pin set as input w/ pull-up
        pud_up(exitPin)

        while get_running(9) and read_pin(exitPin):

            for dc in range (0, 255):
                for pin in ALED_Pins:
                    pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                for pin in BLED_Pins:
                    pi.set_PWM_dutycycle((pin), (255 - dc))  # PWM 1/2 on
                sleep(.015)
            for dc in range (255, 0, -1):
                for pin in ALED_Pins:
                    pi.set_PWM_dutycycle((pin), (dc))  # PWM 1/2 on
                for pin in BLED_Pins:
                    pi.set_PWM_dutycycle((pin), (255 - dc))  # PWM 1/2 on
                sleep(.015)
            get_pwms()

    for pin in ALED_Pins:
        pin_out_low(pin)
    for pin in BLED_Pins:
        pin_out_low(pin)

    clr_running(9)
    tty_message("Script terminated.")


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
    spiCS0 = 16
    spiMOSI = 19
    spiMISO = 20
    spiSCLK = 21

    if get_running(17):
        clr_running(17)
        if get_running(1):
            script_1()
        if get_running(2):
            script_2()

    else:
        if get_running(20):
            script_20()
        if get_running(19):
            script_19()
        if get_running(38):
            script_38()
        if get_running(39):
            script_39()
        set_running(17)

        for pin in pin_names:
            set_not_used(pin)

        used_Pins = [(spiCS0), (spiMOSI), (spiMISO), (spiSCLK)]
        for pin in used_Pins:
            set_used(pin)
            pi.set_mode((pin), pigpio.ALT0)
            get_all_pins(init=True)
        sleep(.25)

# --script 18---------------------------------------------------------------------------


def script_18():
    if get_running(18):
        clr_running(18)
    else:
        set_running(18)
    sleep(.25)


# --script 19-Hardware PWM Menu----------------------------------------------------------


def script_19():
    pwmPina = 12
    pwmPinb = 18
    pwmPinc = 13
    pwmPind = 19

    if get_running(19):
        # Shut down PWMs:
        stop_hpwm(pwmPina)
        stop_hpwm(pwmPinb)
        stop_hpwm(pwmPinc)
        stop_hpwm(pwmPind)
        # Default config the pins:
        pin_out_low(pwmPina)
        pud_up(pwmPinb)
        pud_up(pwmPinc)
        pi.set_mode((19), pigpio.ALT0)

        clr_running(19)
        if get_running(1):
            script_1()
        if get_running(2):
            script_2()

    else:
        if get_running(20):
            script_20()
        if get_running(17):
            script_17()
        if get_running(38):
            script_38()
        if get_running(39):
            script_39()
        set_running(19)
        for pin in pin_names:
            set_not_used(pin)

        used_Pins = [(pwmPina), (pwmPinb), (pwmPinc), (pwmPind)]
        for pin in used_Pins:
            set_used(pin)
            set_pin_out(pin)

        pi.set_mode((pwmPina), pigpio.ALT0)
        pi.set_mode((pwmPinb), pigpio.ALT5)
        start_hpwm(pwmPina)
        pi.set_mode((pwmPinc), pigpio.ALT0)
        pi.set_mode((pwmPind), pigpio.ALT5)
        start_hpwm(pwmPinc)

    sleep(.25)


# --script 20-Software PWM Menu----------------------------------------------------------


def script_20():

    if get_running(20):
        clr_running(20)
        if not get_running(7):
            if get_running(1):
                script_1()
            if get_running(2):
                script_2()
    else:
        if get_running(19):
            script_19()
        if get_running(17):
            script_17()
        if get_running(38):
            script_38()
        if get_running(39):
            script_39()
        LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
        for pin in LED_Pins:
            set_used(pin)
            pi.set_PWM_dutycycle((pin), 48)
        set_running(20)

    sleep(.25)


# --script 21---------------------------------------------------------------------------


def script_21():
    set_running(21)
    tty_message("Script 21 Not Implemented.")
    sleep(.25)
    clr_running(21)


# --script 22---------------------------------------------------------------------------


def script_22():
    set_running(22)
    tty_message("Script 22 Not Implemented.")
    sleep(.25)
    clr_running(22)


# --script 23---------------------------------------------------------------------------


def script_23():
    set_running(23)
    tty_message("Script 23 Not Implemented.")
    sleep(.25)
    clr_running(23)


# --script 24---------------------------------------------------------------------------


def script_24():
    set_running(24)
    tty_message("Script 24 Not Implemented.")
    sleep(.25)
    clr_running(24)


# --script 25---------------------------------------------------------------------------


def script_25():
    set_running(25)
    tty_message("Script 25 Not Implemented.")
    sleep(.25)
    clr_running(25)


# --script 26---------------------------------------------------------------------------


def script_26():
    set_running(26)
    tty_message("Script 26 Not Implemented.")
    sleep(.25)
    clr_running(26)


# --script 27---------------------------------------------------------------------------


def script_27():
    set_running(27)
    tty_message("Script 27 Not Implemented.")
    sleep(.25)
    clr_running(27)


# --script 28---------------------------------------------------------------------------


def script_28():
    set_running(28)
    tty_message("Script 28 Not Implemented.")
    sleep(.25)
    clr_running(28)


# --script 29---------------------------------------------------------------------------


def script_29():
    set_running(29)
    tty_message("Script 29 Not Implemented.")
    sleep(.25)
    clr_running(29)


# --script 30---------------------------------------------------------------------------


def script_30():
    set_running(30)
    tty_message("Script 30 Not Implemented.")
    sleep(.25)
    clr_running(30)


# --script 31---------------------------------------------------------------------------


def script_31():
    set_running(31)
    tty_message("Script 31 Not Implemented.")
    sleep(.25)
    clr_running(31)


# --script 32---------------------------------------------------------------------------


def script_32():
    set_running(32)
    tty_message("Script 32 Not Implemented.")
    sleep(.25)
    clr_running(32)


# --script 33---------------------------------------------------------------------------


def script_33():
    set_running(33)
    tty_message("Script 33 Not Implemented.")
    sleep(.25)
    clr_running(33)


# --script 34---------------------------------------------------------------------------


def script_34():
    set_running(34)
    tty_message("Script 34 Not Implemented.")
    sleep(.25)
    clr_running(34)


# --script 35---------------------------------------------------------------------------


def script_35():
    set_running(35)
    tty_message("Script 35 Not Implemented.")
    sleep(.25)
    clr_running(35)


# --script 36---------------------------------------------------------------------------


def script_36():
    set_running(36)
    tty_message("Script 36 Not Implemented.")
    sleep(.25)
    clr_running(36)


# --script 37---------------------------------------------------------------------------


def script_37():
    set_running(37)
    tty_message("Script 37 Not Implemented.")
    sleep(.25)
    clr_running(37)


# --script 38-Pi Camera-----------------------------------------------------------------


def script_38():

    if get_running(38):
        clr_running(38)
    else:
        set_running(38)
    sleep(.25)


# --script 39-Hardware Clock Menu-------------------------------------------------------


def script_39():

    if get_running(39):
        clr_running(39)
        pi.hardware_clock(4, 0)
        pin_out_low(4)
    else:
        if get_running(19):
            script_19()
        if get_running(17):
            script_17()
        if get_running(20):
            script_20()
        if get_running(38):
            script_38()
        pi.hardware_clock(4, 5000)
        sleep(.25)
        set_running(39)


# --script 40-Clear All-----------------------------------------------------------------


def script_40():
    set_running(40)
    global pins

    hpwms = [12, 13, 18, 19]

    for hpwm in hpwms:
        stop_hpwm(hpwm)
        pi.set_mode((hpwm), pigpio.ALT0)

    for pin in pin_names:
        untest_pin(pin)
    get_all_pins(init=True)

    LED_Pins = [4, 10, 9, 8, 11, 7, 5, 6, 12]
    for pin in LED_Pins:
        pin_out_low(pin)

    Pushbutton_Pins = [18, 17, 23, 22, 27, 24, 25, 13, 26]
    for pin in Pushbutton_Pins:
        pud_up(pin)

    if get_running(1):
        scriptrunning = 1
    if get_running(2):
        scriptrunning = 2

    for script in script_nums:
        clr_running(script)

    tty_message("All scripts terminated.")
    sleep(0.25)
    if scriptrunning == 1:
        script_1()
    if scriptrunning == 2:
        script_2()


# -------------------------------------------------------------------------------------


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
    elif num == 21:
        script_21()
    elif num == 22:
        script_22()
    elif num == 23:
        script_23()
    elif num == 24:
        script_24()
    elif num == 25:
        script_25()
    elif num == 26:
        script_26()
    elif num == 27:
        script_27()
    elif num == 28:
        script_28()
    elif num == 29:
        script_29()
    elif num == 30:
        script_30()
    elif num == 31:
        script_31()
    elif num == 32:
        script_32()
    elif num == 33:
        script_33()
    elif num == 34:
        script_34()
    elif num == 35:
        script_35()
    elif num == 36:
        script_36()
    elif num == 37:
        script_37()
    elif num == 38:
        script_38()
    elif num == 39:
        script_39()
    elif num == 40:
        script_40()
