from django.urls import path
from . import views
from .views import add_patient

urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('success/', views.success, name='success'),
    path('add_patient/', views.add_patient, name='add_patient')
]