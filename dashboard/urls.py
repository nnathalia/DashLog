from django.urls import path
from django.contrib import admin
from . import views

urlpatterns= [
  path('admin/', admin.site.urls),
  path('', views.index, name='index'), 
  path("api/get-pacote/", views.get_pacote, name="get_pacote"),
   path('fake-api/', views.fake_api_externa, name='fake_api_externa'),  # rota fake
]