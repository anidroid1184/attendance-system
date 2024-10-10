from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from cities_light.models import Region, City
from .forms import AttendanceForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # Para marcar asistencia tras loegarse
from .forms import forms, CustomLoginForm
from .models import Attendance, CustomUser
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages


# Vista para registro de usuario
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Ahora puede iniciar sesión.')
            return redirect('home')
        else:
            print(f"Errores: {form.errors}")
            print(form.errors.as_data())
            # Aquí se renderiza el formulario con errores si no es válido
            return render(request, 'attendance/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'attendance/register.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            # Autenticar con document_id
            document_id = form.cleaned_data.get('document_id')
            password = form.cleaned_data.get('password')
            user = authenticate(request, document_id=document_id, password=password)
            if user is not None:
                print(f'Inicio de sesión exitoso {user}')
                login(request, user)
                next_url = request.POST.get('next') or 'mark-attendance'
                return redirect(next_url)  # Redirige a una página después de iniciar sesión
            else:
                form.add_error(None, 'Credenciales incorrectas')
    else:
        form = CustomLoginForm()

    return render(request, 'attendance/login.html', {'form': form, 'next': request.GET.get('next','')})


# Vista para cargar regiones según el país seleccionado
def load_regions(request):
    country_id = request.GET.get('country_id')
    regions = Region.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(regions.values('id', 'name')), safe=False)

# Vista para cargar ciudades según la región seleccionada
def load_cities(request):
    region_id = request.GET.get('region_id')
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


# Vista para la página de inicio
def home(request):
    return render(request, 'attendance/home.html')

# Vista para registrar asistencia

@login_required(login_url='/login/')
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Obtener el usuario y la fecha actual
            user = request.user
            today = timezone.now().date()

            # Verificar si ya existe un registro de asistencia para el usuario y la fecha
            attendance, created = Attendance.objects.get_or_create(user=user, date=today)
            if not created:
                form.add_error(None, 'Ya has registrado asistencia para hoy.')
            else:
                attendance.status = form.cleaned_data['status']
                attendance.save()
                return redirect('home')  # Redirigir después de guardar

    else:
        form = AttendanceForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})


# Formulario para seleccionar el rango de fechas
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label="Fecha de inicio")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label="Fecha de fin")

PORCENTAJE = 0.7
def attendance_summary(request):
    form = DateRangeForm(request.GET or None)
    users_with_70_percent = []

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Contar las asistencias y comparar con el 70% en el rango de fechas
        total_days = (end_date - start_date).days + 1
        required_attendance = int(PORCENTAJE * total_days)

        users_with_70_percent = CustomUser.objects.annotate(
            attendance_count=Count('attendance', filter=Q(attendance__date__range=(start_date, end_date)))
        ).filter(attendance_count__gte=required_attendance)

    return render(request, 'attendance/attendance_summary.html', {'form': form, 'users': users_with_70_percent})