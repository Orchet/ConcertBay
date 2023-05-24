from django.contrib import admin

# Register your models here.

from .models import Artista, Cliente, Escenario, Localidad, Concierto, Reserva, Pago

admin.site.register(Artista)
admin.site.register(Cliente)
admin.site.register(Escenario)
admin.site.register(Localidad)
admin.site.register(Concierto)
admin.site.register(Reserva)
admin.site.register(Pago)