from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Trials, Patients, Measurements

admin.site.register(Trials)
admin.site.register(Patients)
admin.site.register(Measurements)