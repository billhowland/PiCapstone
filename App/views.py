from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .piscripts import (pin_names, scripts, running, test_pin, set_pin_out, pin_out_hi,
pin_out_low, set_pin_in, read_pin, pin_use, pud_up, pud_dn, get_pud, get_ip,
get_test, get_used, get_scripts)
from .pimain import *

# These come from main.js and call things in piscripts.py

@login_required
def main(request):
    IP = 'http://{}:9000'.format(get_ip())
    IPX = ' {}:8080'.format(get_ip())
    return render(request, 'App/main.html', {'IP': IP, 'IPX': IPX})


def gptest(request, pin):
    test_pin(pin)
    out_lvl = ("Test")
    return JsonResponse(out_lvl, safe=False)


def gpout(request, pin):
    set_pin_out(pin)
    out_lvl = {pin: read_pin(pin)}
    return JsonResponse(out_lvl, safe=False)


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
    in_lvl = {pin: read_pin(pin)}
    return JsonResponse(in_lvl, safe=False)


def gpread(request, pin):
    in_lvl = {pin: read_pin(pin)}
    return JsonResponse(in_lvl, safe=False)


def gpuse(request, pin):
    pin_use(pin)
    return HttpResponse('Success')


def gpused(request, pin):
    used = True
    get_used(pin)
    return JsonResponse(used, safe=False)


def gpnot_used(request, pin):
    used = False
    get_used(pin)
    return JsonResponse(used, safe=False)


def gpup(request, pin):
    pud = ("Up")
    pud_up(pin)
    return JsonResponse(pud, safe=False)


def gpdn(request, pin):
    pud = ("Down")
    pud_dn(pin)
    return JsonResponse(pud, safe=False)


def get_all_pins(request):

    pin_info = []
    for pin in pin_names:
        func = pin_use(pin)
        in_lvl = read_pin(pin)
        pud = get_pud(pin)
        test = get_test(pin)
        used = get_used(pin)
        pin_info.append({
            'name': pin,
            'func': func,
            'in_lvl': in_lvl,
            'pud': pud,
            'test': test,
            'used': used,
        })
    return JsonResponse(pin_info, safe=False)


def python_term():
    return HttpResponse('Success')

def get_scripts(request):

    script_info = []
    for script in scripts:
        script_info.append({
            'name': script,
            'running': running,
        })
    return JsonResponse(script_info, safe=False)
