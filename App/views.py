from django.shortcuts import render
from .piscripts import test_pin
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def main(request):
    return render(request, 'App/main.html', {})


def gptest(request, pin):
    test_pin(pin)
