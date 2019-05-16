from django.shortcuts import render
from .piscripts import (test_pin, set_pin_out, pin_out_hi, pin_out_low, set_pin_in, read_pin)
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def main(request):
    # set all the GPIOs to IN so we know
    return render(request, 'App/main.html', {})


def gptest(request, pin):
    test_pin(pin)


def gpout(request, pin):
    set_pin_out(pin)


def gphigh(request, pin):
    pin_out_hi(pin)


def gplow(request, pin):
    pin_out_low(pin)


def gpin(request, pin):
    set_pin_in(pin)


def gpread(request, pin):
    read_pin(pin)
