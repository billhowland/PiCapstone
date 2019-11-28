from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('gptest/<int:pin>', views.gptest, name='gptest'),
    path('gpout/<int:pin>', views.gpout, name='gpout'),
    path('gphigh/<int:pin>', views.gphigh, name='gphigh'),
    path('gplow/<int:pin>', views.gplow, name='gplow'),
    path('gpin/<int:pin>', views.gpin, name='gpin'),
    path('gpread/<int:pin>', views.gpread, name='gpread'),
    path('gpuse/<int:pin>', views.gpuse, name='gpuse'),
    path('gpup/<int:pin>', views.gpup, name='gpup'),
    path('gpdn/<int:pin>', views.gpdn, name='gpdn'),
    path('gpoff/<int:pin>', views.gpoff, name='gpoff'),
    path('gpused/<int:pin>', views.gpused, name='gpused'),
    path('gpnot_used/<int:pin>', views.gpnot_used, name='gpnot_used'),
    path('get_all_pins', views.get_all_pins, name='get_all_pins'),
    path('get_scripts', views.get_scripts, name='get_scripts'),
    path('get_pwms', views.get_pwms, name='get_pwms'),
    path('run_script/<int:num>/', views.run_script, name='run_script'),
    path('gpfrq/<int:pin>', views.gpfrq, name='gpfrq'),
    path('gpsfrq/<int:pin>/<int:frq>', views.gpsfrq, name='gpsfrq'),
    path('gpcfrq/<int:pin>/<int:frq>', views.gpcfrq, name='gpcfrq'),
    path('gpdc/<int:pin>', views.gpdc, name='gpdc'),
    path('gpsdc/<int:pin>/<int:dc>', views.gpsdc, name='gpsdc'),
    path('gphdc/<int:pin>', views.gphdc, name='gphdc'),
    path('gphfrq/<int:pin>', views.gphfrq, name='gphfrq'),
    path('gpshdc/<int:pin>/<int:hdc>', views.gpshdc, name='gpshdc'),
    path('gpshfrq/<int:pin>/<int:hfrq>', views.gpshfrq, name='gpshfrq'),

    path('gpspibaud/<int:spi>', views.gpspibaud, name='gpspibaud'),
    path('gpspiflags/<int:spi>', views.gpspiflags, name='gpspiflags'),
]
