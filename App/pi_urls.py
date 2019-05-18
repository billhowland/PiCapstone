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
    path('get_all_pins', views.get_all_pins, name='get_all_pins')
]
