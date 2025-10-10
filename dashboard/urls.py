from django.urls import path
from django.contrib import admin
from . import views

urlpatterns= [
  path('admin/', admin.site.urls),
  path('', views.index, name='index'), 
  path("api/arduino/pacote/", views.receber_pacote_arduino, name="receber_pacote_arduino"), 
  path("api/pacote/", views.listar_pacotes, name="listar_pacotes"),
]