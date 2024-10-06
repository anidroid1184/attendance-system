from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
# from django_countries.fields import CountryField  # Asegúrate de tener django-countries instalado
from django.conf import settings
from cities_light.models import City, Region, Country



# Modelo personalizado de usuario
class CustomUser(AbstractUser):
    username = None # Descartamos el uso de username

    # Añadimos un campo para el nombre completo

    full_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(
            regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$',
            message='El nombre solo puede contener letras y espacios'
        )],
        default='No name'
    )
    document_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=False,
        default=000000
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City
        , on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    document_id_type = models.CharField
    # Opciones para la política de tratamiento
    POLICY_CHOICES = [
        ('S', 'Sí'),
        ('N', 'No'),
    ]

    policy_accept = models.CharField(
        max_length=1,
        choices=POLICY_CHOICES,
        default='S',
        verbose_name="Acepto las condiciones"
    )

    # Relación con grupos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    # Permisos de usuario
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'document_id'  # Identificador document_id
    REQUIRED_FIELDS = []  # campos obligatorios
    # salvar informacion

    def __str__(self):
        return self.full_name  # Devuelve el nombre de usuario al imprimir el objeto


# Modelo de asistencia
class Attendance(models.Model):
    # Opciones de asistencia
    ATTENDANCE_CHOICES = [
        ('P', 'Presencial'),
        ('V', 'Virtual'),
    ]

    # Relación con el usuario personalizado
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Estado de la asistencia
    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_CHOICES,
        default='V',
        verbose_name="Modo de asistencia"
    )

    # Fecha del registro de asistencia
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} - {self.get_status_display()} - {self.date}'
