from django import forms
from django.contrib.auth.forms import UserCreationForm
from cities_light.models import Country, Region, City  # Usamos los modelos de cities_light
from .models import CustomUser, Attendance


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    document_id = forms.CharField(required=True)

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
            'username',
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
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'document_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'policy_accept': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'username': 'Ingrese su nombre completo',
            'email': 'Ingrese su correo electrónico',
            'document_id': 'Ingrese su documento de identidad',
            'policy_accept': '¿Acepta la política de tratamiento de datos?',
            'country': 'Seleccione su país de origen',
            'region': 'Seleccione su región o departamento',
            'city': 'Seleccione su ciudad de origen'
        }

        error_messages = {
            'username': {
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
        user.email = self.cleaned_data['email']
        user.document_id = self.cleaned_data['document_id']
        if commit:
            user.save()
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

