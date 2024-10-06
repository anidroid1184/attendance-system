from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

# Registrar el modelo CustomUser en el admin
admin.site.register(CustomUser)
