from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .piscripts import (test_pin, set_pin_out, pin_out_hi, pin_out_low, set_pin_in, read_pin, pin_use)
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# These come from main.js and call things in piscripts.py


@login_required
def main(request):
    # set all the GPIOs to IN so we know
    return render(request, 'App/main.html', {})


def gptest(request, pin):
    test_pin(pin)
    out_lvl = 2
    return JsonResponse(out_lvl, safe=False)


def gpout(request, pin):
    set_pin_out(pin)
    return HttpResponse('Success')


def gphigh(request, pin):
    pin_out_hi(pin)
    out_lvl = {pin: read_pin(pin)}
    return JsonResponse(out_lvl, safe=False)


def gplow(request, pin):
    pin_out_low(pin)
    out_lvl = {pin: read_pin(pin)}
    return JsonResponse(out_lvl, safe=False)


def gpin(request, pin):
    set_pin_in(pin)
    return HttpResponse('Success')


def gpreadr(request, pin):
    out_lvl = {pin: read_pin(pin)}
    return JsonResponse(out_lvl, safe=False)


def gpread(request, pin):
    in_lvl = {pin: read_pin(pin)}
    return JsonResponse(in_lvl, safe=False)


def gpuse(request, pin):
    pin_use(pin)
    return HttpResponse('Success')


def get_all_pins(request):
    pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
    pin_info = []
    for pin in pins:
        func = pin_use(pin)
        if func == 1:
            in_lvl = read_pin(pin)
        else:
            in_lvl = False

        pin_info.append({
            'name': pin,
            'func': func,
            'in_lvl': in_lvl,
        })
    return JsonResponse(pin_info, safe=False)
