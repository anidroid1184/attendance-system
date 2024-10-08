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
 # Para asegurarte de que solo usuarios autenticados puedan registrar asistencia


@login_required(login_url='/login/')
def mark_attendance(request):
    # Verificar que el usuario esté autenticado
    if request.user.is_authenticated:
        print(f"Usuario autenticado: {request.user}")
    else:
        print("Usuario no autenticado")
        return redirect('login')

    # Manejar la solicitud POST para registrar asistencia
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Crear la instancia de asistencia pero no guardarla aún
            attendance = form.save(commit=False)
            # Asignar el usuario autenticado al registro de asistencia
            attendance.user = request.user

            # Imprimir los datos para depuración
            print(f"Usuario autenticado: {request.user}, Datos del formulario: {form.cleaned_data}")

            try:
                # Intentar guardar la asistencia en la base de datos
                attendance.save()
                print(f"Asistencia registrada para el usuario: {request.user}")
                return redirect('home')  # Redirigir a la página de inicio después de guardar
            except Exception as e:
                # Si hay un error, imprimirlo en la consola y añadir un error al formulario
                print(f"Error al guardar asistencia: {str(e)}")
                form.add_error(None, "Ocurrió un error al registrar la asistencia.")
    else:
        form = AttendanceForm()  # Si no es POST, mostrar un formulario vacío

    # Renderizar el formulario de asistencia
    return render(request, 'attendance/mark_attendance.html', {'form': form})
