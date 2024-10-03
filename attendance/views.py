from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from cities_light.models import Region, City
from .forms import AttendanceForm

# Vista para registro de usuario
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'attendance/register.html', {'form': form})

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
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return redirect('home')
    else:
        form = AttendanceForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})
