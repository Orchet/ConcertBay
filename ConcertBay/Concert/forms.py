from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from Concert.models import Cliente


class RegistroForm(UserCreationForm):
 nombre = forms.CharField(max_length=30)
 apellido = forms.CharField(max_length=30)
 cedula = forms.CharField(max_length=10)
 correo = forms.CharField(max_length=50)
 telefono = forms.CharField(max_length=30)

 class Meta:
   model = User
   fields = ('username', 'nombre', 'apellido', 'email', 'cedula', 'telefono','password1', 'password2')

 def __init__(self, *args, **kwargs):
   super(RegistroForm, self).__init__(*args, **kwargs)
   for key in self.fields.keys():
     self.fields[key].widget.attrs['class'] = 'general'

 def save(self, commit=True):
   user = super(RegistroForm, self).save(commit=False)
   user.email = self.cleaned_data['email']
   # Creación de persona
   c_nombre = self.cleaned_data['nombre']
   c_apellido = self.cleaned_data['apellido']
   c_cedula = self.cleaned_data['cedula']
   c_telefono = self.cleaned_data['telefono']
   if commit:
     user.save()
     new_cliente = Cliente(nombre=c_nombre,apellido=c_apellido,cedula=c_cedula,telefono=c_telefono,
                           correo=user.email ,user=user)
     new_cliente.save()
   return user
 
class LoginForm(AuthenticationForm):
 def __init__(self, *args, **kwargs):
   super(LoginForm, self).__init__(*args, **kwargs)
   for key in self.fields.keys():
     self.fields[key].widget.attrs['class'] = 'general'


class CompraForm(forms.Form):
  cantidad = forms.CharField(max_length=2)
  
  
  