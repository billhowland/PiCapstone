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
    path('gpused/<int:pin>', views.gpused, name='gpused'),
    path('gpnot_used/<int:pin>', views.gpnot_used, name='gpnot_used'),
    path('get_all_pins', views.get_all_pins, name='get_all_pins'),
    path('get_scripts', views.get_scripts, name='get_scripts'),
    path('script1', views.script1, name='script1'),
    path('script2', views.script2, name='script2'),
    path('script3', views.script3, name='script3'),
    path('script/<int:num>', views.script, name='script'),
]
