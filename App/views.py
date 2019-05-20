from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .piscripts import (test_pin, set_pin_out, pin_out_hi, pin_out_low, set_pin_in, read_pin, pin_use)
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# These come from main.js and call things in piscripts.py

def main(request):
    # set all the GPIOs to IN so we know
    return render(request, 'App/main.html', {})


def gptest(request, pin):
    test_pin(pin)
    return HttpResponse('Success')


def gpout(request, pin):
    set_pin_out(pin)
    return HttpResponse('Success')


def gphigh(request, pin):
    pin_out_hi(pin)
    return HttpResponse('Success')


def gplow(request, pin):
    pin_out_low(pin)
    return HttpResponse('Success')


def gpin(request, pin):
    set_pin_in(pin)
    return HttpResponse('Success')


def gpread(request, pin):
    in_lvl = read_pin(pin)
    return JsonResponse(in_lvl, safe=False)


def gpuse(request, pin):
    pin_use(pin)
    return HttpResponse('Success')


def get_all_pins(request):
    pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    pin_func = [[pin, pin_use(pin)] for pin in pins]
    # for pin in pins:
    #     pin_func[pin] = pin_use(pin)
    return JsonResponse(pin_func, safe=False)
