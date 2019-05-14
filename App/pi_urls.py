from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('set_pin/<int:pin>', views.gptest, name='gptest')
]
