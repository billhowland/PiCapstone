from gpiozero import LED
from time import sleep


def test_pin(pin):
    led = LED(17)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)
