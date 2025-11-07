from django.db import models

# Create your models here.

class Relacion(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.nombre


class Contacto(models.Model):
	nombre = models.CharField(max_length=100)
	primer_apellido = models.CharField(max_length=100)
	segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
	alias = models.CharField(max_length=100, blank=True, null=True)
	relacion = models.ForeignKey(Relacion, on_delete=models.PROTECT)
	telefono = models.CharField(max_length=30)
	correo = models.EmailField(blank=True, null=True)

	def __str__(self):
		return self.nombre