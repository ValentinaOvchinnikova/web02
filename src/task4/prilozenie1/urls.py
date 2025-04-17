from django.urls import path
from . import views

# Пути перехода
urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('success/', views.success, name='success'),
    path('add_patient/', views.add_patient, name='add_patient')
]