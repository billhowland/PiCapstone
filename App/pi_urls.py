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
    path('run_script/<int:num>/', views.run_script, name='run_script'),
    path('gpfrq/<int:pin>', views.gpfrq, name='gpfrq'),
    path('gpsfrq/<int:pin>', views.gpsfrq, name='gpsfrq'),
    path('gpdc/<int:pin>', views.gpdc, name='gpdc'),
    path('gpsdc/<int:pin>', views.gpsdc, name='gpsdc'),
]
