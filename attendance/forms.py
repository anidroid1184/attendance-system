from email.policy import default

from django import forms
from django.contrib.auth.forms import UserCreationForm
from cities_light.models import Country, Region, City  # Usamos los modelos de cities_light
from .models import CustomUser, Attendance
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model  # Para el login


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    document_id = forms.CharField(required=True)

    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Carga dinámica de país, región y ciudad usando los modelos de cities_light
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region = forms.ModelChoiceField(
        queryset=Region.objects.none(),  # Se cargará dinámicamente
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # Se cargará dinámicamente
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'email',
            'document_id',
            'country',
            'region',
            'city',
            'policy_accept',
            'password1',
            'password2'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'document_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'policy_accept': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'full_name': 'Ingrese su nombre completo',
            'email': 'Ingrese su correo electrónico',
            'document_id': 'Ingrese su documento de identidad',
            'policy_accept': '¿Acepta la política de tratamiento de datos?',
            'country': 'Seleccione su país de origen',
            'region': 'Seleccione su región o departamento',
            'city': 'Seleccione su ciudad de origen'
        }

        error_messages = {
            'full_name': {
                'max_length': "El nombre no puede ser mayor a 150 caracteres",
            },
            'email': {
                'max_length': "El correo no puede ser mayor a 254 caracteres",
            },
            'document_id': {
                'max_length': "El documento de identidad no puede ser mayor a 20 caracteres",
            },
        }

    # Sobreescribimos el init para cargar las regiones y ciudades dinámicamente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['region'].queryset = Region.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['city'].queryset = City.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.fields['region'].queryset = Region.objects.none()
            self.fields['city'].queryset = City.objects.none()

    # Guardado de los datos
    def save(self, commit=True):
        user = super().save(commit=False)
        # Limpiar el registro
        user.email = self.cleaned_data['email']
        user.document_id = self.cleaned_data['document_id']
        user.country = self.cleaned_data['country']
        user.region = self.cleaned_data['region']
        user.city = self.cleaned_data['city']

        if commit:
            user.save()
        return user


# Login form
class CustomLoginForm(AuthenticationForm):
    document_id = forms.CharField(
        label="Documento de identidad",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="Contraseña"
    )


    # Elminar campo de username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removemos  el campo de username
        if 'username' in self.fields:
            self.fields.pop('username')


    def clean(self):
        # Sobreescribimos el clean para que autentique con document_id
        document_id = self.cleaned_data.get('document_id')
        password = self.cleaned_data.get('password')

        if document_id and password:
            try:
                # Se busca el usuario utilizando document_id
                user = CustomUser.objects.get(document_id=document_id)
                if not user.check_password(password):
                    # Mostrar si la contraseña es incorrecta
                    raise forms.ValidationError("Contraseña Incorrecta.")
            except CustomUser.DoesNotExist:
                # Validar si el documento de identidad es correcto
                raise forms.ValidationError("Documento de identidad Incorrecto.")
        return super().clean()

    def get_user(self):
        # Este método se utiliza para devolver el usuario autenticado
        document_id = self.cleaned_data.get('document_id')
        user = CustomUser.objects.get(document_id=document_id)
        return user


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']  # Campo de asistencia
        widgets = {
            'status':forms.RadioSelect(),
        }
        labels = {
            'status':'Estado de la Asistencia',
        }


