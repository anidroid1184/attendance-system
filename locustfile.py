from locust import HttpUser, task, between
import random

class UserBehavior(HttpUser):
    wait_time = between(1, 5)  # Tiempo de espera entre las tareas
    host = "http://127.0.0.1:8000"  # Cambia esto al URL de tu aplicación

    @task
    def login(self):
        document_id = f"{random.randint(1000000000, 9999999999)}"  # Generar un ID de documento aleatorio
        self.client.post("/login/", {
            "document_id": document_id,
            "password": "yourpassword"  # Reemplaza con la contraseña correcta
        })

    @task
    def register(self):
        document_id = f"{random.randint(1000000000, 9999999999)}"  # Generar un ID de documento aleatorio
        self.client.post("/register/", {
            "full_name": "Test User",
            "email": "test@example.com",
            "document_id": document_id,
            "country": "1",  # Reemplaza con un ID de país válido
            "region": "1",  # Reemplaza con un ID de región válido
            "city": "1",  # Reemplaza con un ID de ciudad válido
            "policy_accept": "S",
            "password1": "yourpassword",  # Reemplaza con la contraseña deseada
            "password2": "yourpassword",  # Debe coincidir con password1
        })

    @task
    def mark_attendance(self):
        self.client.post("/mark-attendance/", {
            "status": "P",  # O "V" para virtual
        })
