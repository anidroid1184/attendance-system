from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Attendance


# Pruebas unitarias
class AttendanceTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = CustomUser.objects.create_user(
            document_id='123456789', password='testpassword', full_name='Test User'
        )
        self.user.save()

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'document_id': '123456789',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Se espera una redirección tras login exitoso

    def test_mark_attendance_view(self):
        self.client.login(document_id='123456789', password='testpassword')
        response = self.client.get(reverse('mark-attendance'))
        self.assertEqual(response.status_code, 200)


