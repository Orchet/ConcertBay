"""ConcertBay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Concert import views

urlpatterns = [
    path("", views.MainView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    path("registro", views.registro_request, name='registro'),
    path("login", views.login_request, name='login'),
    path("logout", views.logout_request, name='logout'),
    path("getInfoConciertoById/<int:id_concierto>", views.getInfoConciertoById, name="getInfoConciertoById"),
    path("conciertos/", views.getListadoConciertos, name="getListadoConciertos"),           
    path("getInfoTicketById/<int:id_localidad>", views.getInfoTicketById, name="getInfoTicketById"),    
    path("compraTicket/<int:id_localidad>/<int:nro_tickets>", views.compraTicket, name="compraTicket"),    
    path("consulta/", views.getInfoComprasByCliente, name="getInfoComprasByCliente"),
]
