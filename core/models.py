from tabnanny import verbose

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class RedSocial(models.Model):
    nombre = models.CharField(max_length=100)
    enlace = models.URLField()

    def __str__(self):
        return self.nombre


User.add_to_class('photo', models.ImageField(upload_to='user_photos/', blank=True, null=True))

from django.db import models



class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre



class Condicion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre



class Organizacion(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo")
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    rubro = models.CharField(max_length=100, verbose_name="Rubro")
    provincias = models.ManyToManyField(Provincia, related_name="organizaciones")

    def __str__(self):
        return self.razon_social



class Persona(models.Model):
    condicion = models.ForeignKey(Condicion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Condición")


    nombres = models.CharField(max_length=255, verbose_name="Nombre(s)")
    apellidos = models.CharField(max_length=255,verbose_name= "Apellidos")
    correo_electronico = models.EmailField(unique=True, verbose_name="Email")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")


    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, verbose_name="Organización")

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cargo}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="documentos")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Documento")
    url = models.URLField(verbose_name="Enlace de Google Drive")

    def __str__(self):
        return self.nombre


class Medio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    nombre_evento = models.CharField(max_length=255)
    detalle = models.TextField(max_length=80000, verbose_name="Detalle del Evento", default="Escribe el detalle del evento")
    plazo = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin=models.DateField(blank=True, null=True)
    horainicio = models.TimeField(default="00:00:00")
    horafin = models.TimeField(default="00:00:00")
    medio = models.ForeignKey(Medio, on_delete=models.CASCADE, related_name='eventos')
    direccion = models.CharField(max_length=255,blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_evento} - {self.titulo}"

class Eje(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre de eje")

    def __str__(self):
        return self.nombre

class Compromiso(models.Model):
    # Campos principales
    titulo = models.TextField(max_length=255, verbose_name="Título del Compromiso", blank=True, null=True)
    problema = models.TextField(verbose_name="Problema", blank=True, null=True)
    estado_inicial = models.TextField(verbose_name="Estado Inicial", blank=True, null=True)
    accion = models.TextField(verbose_name="Acción", blank=True, null=True)
    relevancia = models.TextField(verbose_name="Relevancia con los valores del Gobierno Abierto", blank=True, null=True)
    otros_actores = models.TextField(verbose_name="Otros Actores", blank=True, null=True)
    eje = models.ForeignKey(Eje, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Eje")

    # Área Responsable
    area_responsable = models.CharField(max_length=255, verbose_name="Área Responsable", blank=True, null=True)
    responsables = models.TextField(verbose_name="Responsables", blank=True, null=True)
    correo_contacto = models.EmailField(verbose_name="Correo Electrónico de Contacto",blank=True, null=True)
    telefono_contacto = models.CharField(max_length=15, verbose_name="Teléfono de Contacto",blank=True, null=True)

    # Avance
    avance = models.FloatField(verbose_name="Porcentaje de Avance", default=0.0)
    estado_avance = models.CharField(max_length=50, verbose_name="Estado del Avance", blank=True, null=True)

    def __str__(self):
        return self.titulo


class Hito(models.Model):
    compromiso = models.ForeignKey(Compromiso, related_name="hitos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, verbose_name="Hito")
    estado = models.CharField(max_length=100, verbose_name="Estado del Compromiso")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_final = models.DateField(verbose_name="Fecha Final")
    avance = models.FloatField(verbose_name="Avance", default=0.0)
    evidencia = models.URLField(null=False, blank=True, verbose_name="Evidencia")


    def __str__(self):
        return f"{self.titulo} - {self.compromiso.titulo}"


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    project = models.ForeignKey(Compromiso, on_delete=models.CASCADE, related_name='comments', verbose_name="Proyecto")
    content = models.TextField(max_length=5000, verbose_name="Comentario")
    created_at = models.DateTimeField(default=now, verbose_name="Fecha")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title}"


class Voto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    project = models.ForeignKey(Compromiso, on_delete=models.CASCADE, related_name='votes', verbose_name="Proyecto")
    created_at = models.DateTimeField(default=now, verbose_name="Fecha")

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"Vote by {self.user.username} on {self.project.title}"









