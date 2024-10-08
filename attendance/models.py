from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from cities_light.models import City, Region, Country


# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, document_id, password=None, **extra_fields):
        if not document_id:
            raise ValueError('El campo Document ID debe estar definido')
        user = self.model(document_id=document_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, document_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(document_id, password, **extra_fields)


# Modelo personalizado de usuario
class CustomUser(AbstractUser):
    username = None  # Descartamos el uso de username

    full_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(
            regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$',
            message='El nombre solo puede contener letras y espacios'
        )],
        default='No name'
    )
    document_id = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        null=False,
        default='000000'
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
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

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

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'document_id'  # Identificador document_id
    REQUIRED_FIELDS = []  # Campos obligatorios

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name


# Modelo de asistencia
class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('P', 'Presencial'),
        ('V', 'Virtual'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_CHOICES,
        default='V',
        verbose_name="Modo de asistencia"
    )

    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (
        'user', 'date')  # Asegurarse de que un usuario no pueda registrar asistencia más de una vez por día

    def __str__(self):
        return f'{self.user.full_name} - {self.get_status_display()} - {self.date}'
