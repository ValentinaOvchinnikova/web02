from django.urls import path
from . import views
# файл описывает пути перехода по формам
urlpatterns = [
    path('', views.input_form, name='input_form'),
]