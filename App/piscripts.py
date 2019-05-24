from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pins = [4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
test = 0
# URL -> View -> Piscript


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
    GPIO.setup((pin), GPIO.IN)


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
