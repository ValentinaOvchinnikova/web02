from django.urls import path
from . import views
# Пути перехода
urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('success/', views.input_form, name='success'),
]