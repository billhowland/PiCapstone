from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .piscripts import (pwm_names, test_pin, script_nums, set_pin_out,
                        pin_out_hi, pin_out_low, pin_tog, set_pin_in, read_pin,
                        pin_use, pud_up, pud_dn, pud_off, get_pud, get_ip, get_test,
                        get_testing, get_used, get_name, get_url, get_running,
                        do_script, get_frq, set_frq, set_cfrq, get_dc, set_dc, get_hfrq, get_hdc,
                        set_hdc, set_hfrq, start_hpwm, spi_names, get_spi_baud, get_spi_flags,
                        set_spi_baud, set_spi_flags, tog_failed, i2c_names, get_i2c_address,
                        set_i2c_address)

from .pimain import *

# These come from main.js and call things in piscripts.py:


@login_required
def main(request):
    IP = 'http://{}:9000'.format(get_ip())  # bash console
    IPB = 'http://{}:9001'.format(get_ip())  # cat console
    IPC = 'http://{}:9002'.format(get_ip())  # picamera stream
    IPD = 'http://{}:9003'.format(get_ip())  # pistream stream
    IPX = ' {}:8080'.format(get_ip())
    return render(request, 'App/main.html', {'IP': IP, 'IPB': IPB, 'IPC': IPC, 'IPD': IPD, 'IPX': IPX})  # 'IPC': IPC,


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


def gpcfrq(request, pin, frq):
    set_cfrq(pin, frq)
    return JsonResponse(frq, safe=False)
    # return HttpResponse('Success')


def gpshfrq(request, pin, hfrq):
    set_hfrq(pin, hfrq)
    if hfrq > 0:
        start_hpwm(pin)
    return JsonResponse(hfrq, safe=False)


def gpdc(request, pin):
    dc = get_dc(pin)
    return JsonResponse(dc, safe=False)


def gpsdc(request, pin, dc):
    set_dc(pin, dc)
    return JsonResponse(dc, safe=False)


def gpshdc(request, pin, hdc):
    set_hdc(pin, hdc)
    if hdc > 0:
        start_hpwm(pin)
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


def get_all_pins(request):  # returns pin data back to the html, does not call get_all_pins in piscripts.
    # This is the spot called by main.js 4 times a second.

    pin_info = []

    if get_running(21):
        pin_names = [8, 9, 10, 11, 13, 17, 23, 6, 19, 25, 26, 16, 20, 21, 18]
    else:
        pin_names = [4, 10, 9, 8, 11, 7, 5, 6, 12, 13, 26, 25, 27, 24, 23, 22, 18, 17, 2, 3, 14, 15, 16, 19, 20, 21]

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
        name = pwm
        func = pin_use(pwm)
        frq = get_frq(pwm)
        dc = get_dc(pwm)
        hfrq = get_hfrq(pwm)
        hdc = get_hdc(pwm)
        pwm_info.append({
            'name': name,
            'func': func,
            'sfrq': frq,
            'sdc': dc,
            'shfrq': hfrq,
            'shdc': hdc,
            })

    return JsonResponse(pwm_info, safe=False)


def get_spis(request):
    spi_info = []
    for spi in spi_names:
        baud = get_spi_baud(spi)
        flags = get_spi_flags(spi)
        spi_info.append({
            'name': spi,
            'baud': baud,
            'flags': flags,
            })

    return JsonResponse(spi_info, safe=False)


def get_i2cs(request):
    i2c_info = []
    for i2c in i2c_names:
        address = get_i2c_address(i2c)
        flags = 0
        i2c_info.append({
            'name': i2c,
            'address': address,
            'flags': flags,
            })

    return JsonResponse(i2c_info, safe=False)


def run_script(request, num):
    # if num == 38:
    #     IPC = 'http://{}:9002'.format(get_ip())
    #     do_script(38)
    #     return HttpResponse('Success')

    if num != 37:  # lock out bash console
        do_script(num)
        return HttpResponse('Success')

    if num == 37:
        if request.user.username == "bill":
            do_script(num)
            return HttpResponse('Success')

        else:
            tog_failed(37)


def gpsspibaud(request, spi, baud):
    set_spi_baud(spi, baud)
    return JsonResponse(baud, safe=False)


def gpsi2caddr(request, i2c, address):
    set_i2c_address(i2c, address)
    return JsonResponse(address, safe=False)


def gpsspiflags(request, spi, flags):
    set_spi_flags(spi, flags)
    return JsonResponse(flags, safe=False)


def gpspibaud(request, spi):
    baud = get_spi_baud(spi)
    return JsonResponse(baud, safe=False)


def gpi2caddr(request, i2c):
    address = get_i2c_address(i2c)
    return JsonResponse(address, safe=False)


def gpspiflags(request, spi):
    flags = get_spi_flags(spi)
    return JsonResponse(flags, safe=False)
