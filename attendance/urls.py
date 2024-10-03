from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Ruta de la pagina principal (HOME)
    path('', views.home, name='home'),
    # Ruta para el registro de usuarios
    path('register/', views.register, name='register'),
    # Ruta para el inicio de sesión utilizando LoginView
    path('login/', auth_views.LoginView.as_view(template_name='attendance/login.html'), name='login'),
    # Ruta para el cierre de sesión utilizando LogoutView
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Ruta para el formulario de asistencia
    path('mark-attendance/', views.mark_attendance, name='mark-attendance'),
    # URLs para las vistas AJAX de las ciudades y departamentos
    path('ajax/load-regions/', views.load_regions, name='ajax_load_regions'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]