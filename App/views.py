from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .piscripts import (pin_names, pwm_names, test_pin, script_nums, set_pin_out,
                        pin_out_hi, pin_out_low, pin_tog, set_pin_in, read_pin,
                        pin_use, pud_up, pud_dn, pud_off, get_pud, get_ip, get_test,
                        get_testing, get_used, get_name, get_url, get_running,
                        do_script, get_frq, set_frq, get_dc, set_dc, get_hfrq, get_hdc,
                        set_hdc, set_hfrq)

from .pimain import *

# These come from main.js and call things in piscripts.py:


@login_required
def main(request):
    IP = 'http://{}:9000'.format(get_ip())
    IPB = 'http://{}:9001'.format(get_ip())
    IPX = ' {}:8080'.format(get_ip())
    return render(request, 'App/main.html', {'IP': IP, 'IPB': IPB, 'IPX': IPX})


# @login_required
# def addons(request):
#     IPY = ' {}:8080'.format(get_ip())
#     return render(request, 'App/addons.html', {'IPY': IPY})


def gptest(request, pin):
    test_pin(pin)
    test = 2  # was out_lvl = ("Test")
    return JsonResponse(test, safe=False)  # was out_lvl


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

# --


def gphdc(request, pin):

    hdc = get_hdc(pin)
    return JsonResponse(hdc, safe=False)


def gpfrq(request, pin):
    frq = get_frq(pin)
    return JsonResponse(frq, safe=False)


def gpsfrq(request, pin, frq):
    set_frq(pin, frq)
    # frq = {pin: read_pin(pin)}
    return JsonResponse(frq, safe=False)


def gpshfrq(request, pin, hfrq):
    set_hfrq(pin, hfrq)
    # frq = {pin: read_pin(pin)}
    return JsonResponse(hfrq, safe=False)


def gpdc(request, pin):
    dc = get_dc(pin)
    return JsonResponse(dc, safe=False)


def gpsdc(request, pin, dc):
    set_dc(pin, dc)
    return JsonResponse(dc, safe=False)


def gpshdc(request, pin, hdc):
    set_hdc(pin, hdc)
    return JsonResponse(hdc, safe=False)


def gphfrq(request, pin):

    hfrq = get_hfrq(pin)
    return JsonResponse(hfrq, safe=False)

# --


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


def gpoff(request, pin):
    pud = ("Off")
    pud_off(pin)
    return JsonResponse(pud, safe=False)


def get_all_pins(request):  # returns pin data back to the html, does not call
    # get_all_pins in piscripts!
    # if this is the spot called by main.js 4 times a
    # second, blinking s/b done here!

    pin_info = []

    for pin in pin_names:
        testing = get_testing(pin)
        func = pin_use(pin)
        in_lvl = read_pin(pin)
        pud = get_pud(pin)
        test = get_test(pin)
        frq = get_frq(pin)
        dc = get_dc(pin)
        hfrq = get_hfrq(pin)
        hdc = get_hdc(pin)
        if not testing:
            if test:
                pin_tog(pin)
                testing = True
        used = get_used(pin)
        pin_info.append({
            'name': pin,
            'func': func,
            'in_lvl': in_lvl,
            'pud': pud,
            'test': test,
            'used': used,
            'testing': testing,
            'frq': frq,
            'dc': dc,
            'hfrq': hfrq,
            'hdc': hdc,
        })
    return JsonResponse(pin_info, safe=False)


def get_scripts(request):
    script_info = []
    for scr in script_nums:
        name = get_name(scr)
        url = get_url(scr)
        running = get_running(scr)
        script_info.append({
            'num': scr,
            'name': name,
            'url': url,
            'running': running,
            })

    return JsonResponse(script_info, safe=False)


def get_pwms(request):
    pwm_info = []
    for pwm in pwm_names:
        name = pwm_name(pwm)
        pwm_info.append({
            'name': name,
            })

    return JsonResponse(pwm_info, safe=False)


def run_script(request, num):
    do_script(num)
    return HttpResponse('Success')


# def get_hpwm0(request):
#     get_hpwm0()
#     return HttpResponse('Success')
#
#
# def get_hpwm1(request):
#     get_hpwm1()
#     return HttpResponse('Success')
