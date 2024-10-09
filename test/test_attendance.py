import os
import django
import pytest

# Asegúrate de que el entorno de Django esté configurado
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from attendance.models import CustomUser, Attendance  # Importación absoluta


@pytest.mark.django_db
def test_attendance_creation():
    # Crear un usuario de prueba
    user = CustomUser.objects.create_user(
        document_id='123456789',
        password='testpassword',
        full_name='Test User'
    )

    # Crear una instancia de Attendance
    attendance = Attendance.objects.create(
        user=user,
        status='P'
    )

    assert attendance.user == user
    assert attendance.status == 'P'
