import random
import string
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000"  # Cambia esto al URL de tu aplicación
    csrf_token = None

    def random_string(self, length=10):
        """Genera un string aleatorio de longitud especificada."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_document_id(self):
        """Genera un document ID aleatorio."""
        return ''.join(random.choices(string.digits, k=10))

    def on_start(self):
        # Obtener el token CSRF desde la página de login
        response = self.client.get("/login/")
        if "csrftoken" in response.cookies:
            self.csrf_token = response.cookies['csrftoken']
        else:
            self.csrf_token = None
        # Asegurarse de que el token CSRF se haya obtenido
        assert self.csrf_token is not None, "No se pudo obtener el token CSRF"

        # Registrar un nuevo usuario al iniciar
        self.register()

    def register(self):
        """Registra un nuevo usuario con datos aleatorios."""
        if self.csrf_token:
            # Generar datos aleatorios para el nuevo usuario
            self.document_id = self.random_document_id()
            self.email = f"{self.random_string(5)}@correo.com"
            self.password = "contraseña123"  # Puedes hacer esto también aleatorio si lo deseas

            response = self.client.post("/register/", {
                "full_name": "Usuario Prueba",
                "email": self.email,
                "document_id": self.document_id,
                "country": "1",  # Cambiar según los valores válidos de tu base de datos
                "region": "1",
                "city": "1",
                "password1": self.password,
                "password2": self.password,
                "policy_accept": "S",
                "csrfmiddlewaretoken": self.csrf_token
            }, headers={"X-CSRFToken": self.csrf_token},
               allow_redirects=False)

            # Verificar si el registro fue exitoso
            if response.status_code == 200 or response.status_code == 302:
                print(f"Usuario registrado: {self.document_id}")
            else:
                print(f"Error al registrar usuario: {response.text}")

    @task
    def login(self):
        """Inicia sesión con el usuario recién registrado."""
        if self.csrf_token:
            response = self.client.post("/login/", {
                "document_id": self.document_id,  # Utilizar el document_id registrado
                "password": self.password,
                "csrfmiddlewaretoken": self.csrf_token
            }, headers={"X-CSRFToken": self.csrf_token},
               allow_redirects=False)

            if response.status_code == 200 or response.status_code == 302:
                print(f"Usuario autenticado: {self.document_id}")
            else:
                print(f"Error al iniciar sesión: {response.text}")

    @task
    def mark_attendance(self):
        """Marca asistencia del usuario autenticado."""
        if self.csrf_token:
            response = self.client.post("/mark-attendance/", {
                "status": "P",  # O "V" para virtual
                "csrfmiddlewaretoken": self.csrf_token
            }, headers={"X-CSRFToken": self.csrf_token},
               allow_redirects=False)

            if response.status_code == 200 or response.status_code == 302:
                print(f"Asistencia marcada para: {self.document_id}")
            else:
                print(f"Error al marcar asistencia: {response.text}")

