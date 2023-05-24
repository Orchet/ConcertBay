from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse
from .models import Artista, Cliente, Localidad, Concierto, Reserva
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import RegistroForm, LoginForm
from django.db.models import Sum

class MainView(TemplateView):
    template_name = "main.html"


def registro_request(request):
 if request.method == 'POST':
   form = RegistroForm(request.POST)
   if form.is_valid():
     user = form.save()
     login(request, user)
     messages.success(request, 'Se ha registrado exitosamente')
     return redirect("landing")
   messages.error(request, 'Información no válida')
 # Método no válido, retorna formulario vacío
 
 form = RegistroForm()
 return render(request=request,        
               template_name='registro.html', 
               context={'registro_form': form})

 
def login_request(request):
 if request.method == 'POST':
   form = LoginForm(request, data=request.POST)
   if form.is_valid():
     username = form.cleaned_data.get('username')
     password = form.cleaned_data.get('password')
     user = authenticate(username=username, password=password)
     if user is not None:
       login(request, user)
       messages.info(request, f'Ha iniciado sesión como: {username}')
       return redirect("landing")
     messages.error(request, 'Credenciales incorrectas')
   messages.error(request, 'Credenciales incorrectas')
 # Método no válido, retorna formulario vacío
 form = LoginForm()
 return render(request=request,
               template_name='login.html',
               context={'login_form': form})


def logout_request(request):
 logout(request)
 messages.info(request, "Has cerrado sesión")
 return redirect("login")



def getListadoConciertos(request):
    conciertos = Concierto.objects.all()
    nombre_conciertos = []
    for concierto in conciertos:        
        artista = Artista.objects.get(id=concierto.id)    
        nro_localidad = Localidad.objects.filter(concierto_id=concierto.id).aggregate(disp=Sum('nro_disponibles'))
        nombre_conciertos.append((concierto.id, concierto.nombre, artista.nombre, concierto.fecha, "Entradas disponibles: " + str(nro_localidad['disp'])))
    return render(request, "conciertos.html", {'listado': nombre_conciertos})
  
  

def getInfoConciertoById(request, id_concierto):
 concierto = Concierto.objects.get(id=id_concierto)
 artista = Artista.objects.get(id=concierto.artista_id)
 nro_localidad = Localidad.objects.filter(concierto_id=concierto.id).aggregate(disp=Sum('nro_disponibles'))
 precios = Localidad.objects.filter(concierto_id=concierto.id)
 sitio_precio = []
 for precio in precios:
      sitio_precio.append((precio.id, precio.nombre, "$ " + str(precio.precio))) 
 return render(request, "concierto.html", {'concierto': concierto.nombre, 'fecha': concierto.fecha, 'artista': artista.nombre, 
                                           'descripcion': artista.descripcion, 'nro_disponibles': str(nro_localidad['disp']),
                                           'lista_precios': sitio_precio})



def getInfoTicketById(request, id_localidad):
 localidad = Localidad.objects.get(id=id_localidad)
 concierto = Concierto.objects.get(id=localidad.concierto_id) 
 return render(request, "compra.html", {'concierto': concierto.nombre, 
                                        'localidad_id': localidad.id, 'localidad': localidad.nombre,
                                        'precio': "$ " + str(localidad.precio)})
                                           
                                           
def compraTicket(request, id_localidad, nro_tickets):      
  if request.method == 'POST':   
   user = request.user.id
   cliente = Cliente.objects.get(user__id=user)
   localidad = Localidad.objects.get(id=id_localidad)
   concierto = Concierto.objects.get(id=localidad.concierto_id)
   total = localidad.precio * nro_tickets
   new_reserva = Reserva(cliente = cliente, concierto = concierto, 
                        localidad = localidad, total_compra = total, nro_tickets = nro_tickets)
   new_reserva.save()
   #print (user)
   #print (new_reserva)
   localidad.nro_disponibles = localidad.nro_disponibles - nro_tickets
   localidad.save()
   messages.info(request, 'Se ha realizado su compra')
   return redirect(f'/getInfoConciertoById/{localidad.concierto.id}')



def getInfoComprasByCliente(request):
  compras = Reserva.objects.filter(cliente_id=1)
  lista_compras = []
  for compra in compras:        
    concierto = Concierto.objects.get(id=compra.concierto_id)
    localidad = Localidad.objects.get(id=compra.localidad_id)
    lista_compras.append((concierto.nombre, localidad.nombre, "$ " + str(localidad.precio), compra.nro_tickets,
                          "$ " + str(compra.total_compra), compra.fecha_creacion))    
  return render(request, "consulta.html", {'listado_compras': lista_compras})  
    
    
    
    
    
    