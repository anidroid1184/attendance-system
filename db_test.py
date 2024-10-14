import os
import django

# Configura la variable de entorno DJANGO_SETTINGS_MODULE para apuntar a tus settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

# Inicializa Django
django.setup()

from cities_light.models import Country

try:
    print("Intentando conectarse a la base de datos...")
    countries = Country.objects.all()
    print(f"Se encontraron {countries.count()} países en la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
