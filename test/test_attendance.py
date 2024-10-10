import os
import django
import pytest
from faker import Faker
import random

# Asegúrate de que el entorno de Django esté configurado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from attendance.models import CustomUser, Attendance  # Importación absoluta

# Instancia de Faker para generar datos aleatorios
faker = Faker()

@pytest.mark.django_db
def test_attendance_creation():
    usuarios_creados = []
    # Crear 100 usuarios de prueba con datos aleatorios
    for _ in range(100):
        # Generar un document_id y un nombre de usuario aleatorio
        document_id = faker.unique.random_number(digits=9, fix_len=True)
        full_name = faker.name()

        # Crear el usuario
        user = CustomUser.objects.create_user(
            document_id=str(document_id),
            password='testpassword',  # puedes usar la misma contraseña para todos
            full_name=full_name
        )
        usuarios_creados.append(user)

        # Asignar un estado de asistencia aleatorio entre "P" (presencial) y "V" (virtual)
        attendance_status = random.choice(['P', 'V'])

        # Crear una instancia de Attendance
        attendance = Attendance.objects.create(
            user=user,
            status=attendance_status
        )

        # Asegurarse de que la asistencia se haya guardado correctamente
        assert attendance.user == user
        assert attendance.status == attendance_status

    # Opción: Imprimir el resultado de los usuarios generados (puedes comentar esto si no lo necesitas)
    print(f"{len(usuarios_creados)} usuarios creados con asistencia registrada.")

