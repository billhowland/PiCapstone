from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# URL -> View -> Piscript


def test_pin(pin):
    led = LED(pin)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)

# Outputs:


def set_pin_out(pin):
    GPIO.setup((pin), GPIO.OUT)


def pin_out_hi(pin):
    GPIO.output((pin), GPIO.HIGH)


def pin_out_low(pin):
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
