from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .piscripts import (pin_names, test_pin,
                        set_pin_out, pin_out_hi, pin_out_low, set_pin_in, read_pin, pin_use, pud_up,
                        pud_dn, get_pud, get_ip, get_test, get_used, running, blink_pin,
                        script_1, script_2, script_3)

from .pimain import *

script_names = ["Base Configuration", "My Hat Configuration 1", "Blinkies!", "Script 4", "Script 5", "Script 6",
                "Script 7", "Script 8", "Script 9", "Script 10", "Script 11", "Script 12", "Script 13",
                "Script 14", "Script 15", "Script 16", "Script 17", "Script 18"]
script_urls = ["script1", "script2", "script3", "script4", "script5",
               "script6", "script7", "script8", "script9", "script10", "script11",
               "script12", "script13", "script14", "script15", "script16", "script17", "script18"]
# running = []
scripts = zip(script_urls, script_names)

# These come from main.js and call things in piscripts.py


@login_required
def main(request):
    IP = 'http://{}:9000'.format(get_ip())
    IPX = ' {}:8080'.format(get_ip())
    return render(request, 'App/main.html', {'IP': IP, 'IPX': IPX})


def gptest(request, pin):
    test_pin(pin)
    test = 2  # was out_lvl = ("Test")
    return JsonResponse(test, safe=False) # was out_lvl


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


def get_all_pins(request):  # returns pin data back to the html, does not call
                            # get_all_pins in piscripts!
                            # if this is the spot called by main.js 4 times a
                            # second, blinking s/b done here!

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


def get_scripts(request):
    scripts = zip(script_urls, script_names)
    script_info = []
    for script_url, script_name in scripts:
        script_info.append({
            'name': script_name,
            'url': script_url,
            'running': running,
        })
    return JsonResponse(script_info, safe=False)


def script1(request):
    script_1()
    running = True
    return JsonResponse(running, safe=False)


def script2(request):
    script_2()
    running = True
    return JsonResponse(running, safe=False)


def script3(request):
    script_3()
    running = True
    return JsonResponse(running, safe=False)
