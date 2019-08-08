from .piscripts import *

def main():
    global pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN)
    GPIO.setup(3, GPIO.IN)
    for pin in pin_names:
        if pin not in [2, 3]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            GPIO.setup(pin, GPIO.IN)
    pins = get_all_pins(init=True)
    os.system("gotty bash &")

main()
