
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class Curso(models.Model):
    CODE_CHOICES = [
        ("1SMR", "1º SMR"),
        ("2SMR", "2º SMR"),
        ("1ASIR", "1º ASIR"),
        ("2ASIR", "2º ASIR"),
    ]
    code = models.CharField(max_length=10, choices=CODE_CHOICES, unique=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.nombre

class Empresa(models.Model):
    class Estado(models.TextChoices):
        VERDE = "verde", "Colabora"
        NARANJA = "naranja", "En contacto"
        ROJO = "rojo", "No colabora"

    cif = models.CharField(max_length=16, unique=True)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=255, blank=True)
    localidad = models.CharField(max_length=120, blank=True)
    nif_responsable = models.CharField(max_length=16, blank=True)
    nombre_responsable = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.VERDE)
    cursos = models.ManyToManyField(Curso, blank=True, related_name="empresas")

    # Nota: los alumnos se obtienen desde LDAP, no se persisten aquí.
    # Podemos opcionalmente almacenar un criterio de búsqueda configurable.
    
    class Meta:
        ordering = ["-estado", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.cif})"


class ContactoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="historial")
    profesor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="contactos_empresas")
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.empresa.nombre} - {self.profesor} @ {self.fecha:%Y-%m-%d %H:%M}"

class AlumnoEmpresa(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, related_name="alumnos")
    uid = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100, blank=True)
    curso = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre or self.uid} ({self.curso})"

class PersonaContacto(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, related_name="contactos")
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.telefono or self.email or 'sin contacto'})"


class HistorialContacto(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, related_name="historial_contactos")
    profesor_username = models.CharField(max_length=150)
    profesor_nombre = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    texto = models.TextField()

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.empresa.nombre} - {self.profesor_username} ({self.fecha:%d/%m/%Y %H:%M})"