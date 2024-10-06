from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from cities_light.models import Region, City
from .forms import AttendanceForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # Para marcar asistencia tras loegarse
from .forms import CustomLoginForm


# Vista para registro de usuario
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
                login(request, user)
                return redirect('home')  # Redirige a una página después de iniciar sesión
            else:
                form.add_error(None, 'Credenciales incorrectas')
    else:
        form = CustomLoginForm()

    return render(request, 'attendance/login.html', {'form': form})


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
@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user  # Asegúrate de asignar el usuario autenticado
            attendance.save()
            return redirect('home')  # O la vista a la que desees redirigir después
    else:
        form = AttendanceForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})
