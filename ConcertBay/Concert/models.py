from django.db import models
from django.utils import timezone
from datetime import date


class Artista (models.Model):
    nombre = models.CharField(max_length=100)
    genero_musical = models.CharField(max_length=50)
    correo_contacto = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)
    
class Cliente (models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=10)
    correo = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    user = models.OneToOneField('auth.user', on_delete=models.PROTECT, related_name='user', default=None)
        
class Escenario (models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField(default=0)
    
class Concierto (models.Model):
    nombre = models.CharField(max_length=50)   
    fecha = models.DateTimeField(default=timezone.now)
    artista = models.ForeignKey('Artista', on_delete=models.PROTECT, related_name='artista')
    escenario = models.ForeignKey('Escenario', on_delete=models.PROTECT, related_name='escenario') 
    descripcion = models.CharField(max_length=300, null=True, blank=True)
    estado = models.BooleanField(default=True)

class Localidad (models.Model):
    nombre = models.CharField(max_length=50)
    nro_disponibles = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    concierto = models.ForeignKey('Concierto', on_delete=models.PROTECT, related_name='localidad_concierto')
    estado = models.BooleanField(default=True)

class Reserva (models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT, related_name='cliente')
    concierto = models.ForeignKey('Concierto', on_delete=models.PROTECT, related_name='concierto')
    localidad = models.ForeignKey('Localidad', on_delete=models.PROTECT, related_name='localidad')
    nro_tickets = models.SmallIntegerField(default=0)
    total_compra = models.FloatField(default=0)
    estado = models.BooleanField(default=True)

class Pago (models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    reserva = models.ForeignKey('Reserva', on_delete=models.PROTECT, related_name='reserva')
    total = models.FloatField(default=0)
        
    