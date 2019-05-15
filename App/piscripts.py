from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

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


def pin_out_lo(pin):
    GPIO.output((pin), GPIO.LOW)

# Inputs:


def set_pin_in(pin):
    GPIO.setup((pin), GPIO.IN)


def read_pin(pin):
    return GPIO.input(pin)
