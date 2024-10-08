from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Attendance

# Registrar el modelo CustomUser en el admin
admin.site.register(CustomUser)
# Registrar el modelo de Asistencia
admin.site.register(Attendance)
