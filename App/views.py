from django.shortcuts import render, redirect
from .models import Receta, Usuario, Animal

# Create your views here.
def index(request):
    context = {
        'message': 'This is the index page.'
    }
    return render(request, 'App/index.html', context)

def crear_receta(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        imagen = request.POST.get('imagen')
        ingredientes = request.POST.get('ingredientes')
        instrucciones = request.POST.get('instrucciones')
        receta = Receta(nombre=nombre, imagen=imagen, ingredientes=ingredientes, instrucciones=instrucciones)
        receta.save()
        return redirect('mostrar_recetas')
    return render(request, 'App/crear_receta.html')

def mostrar_recetas(request):
    recetas = Receta.objects.all()
    context = {
        'recetas': recetas
    }
    return render(request, 'App/mostrar_recetas.html', context)

def buscar_receta(request):
    receta = None
    searched = False
    if 'nombre' in request.GET:
        nombre = request.GET.get('nombre')
        searched = True
        try:
            receta = Receta.objects.get(nombre__iexact=nombre)
        except Receta.DoesNotExist:
            receta = None
    return render(request, 'App/buscar_receta.html', {'receta': receta, 'searched': searched})

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido', '')
        edad = request.POST.get('edad', 18)
        email = request.POST.get('email')
        password = request.POST.get('password')

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            email=email,
            password=password
        )
        usuario.save()
        return redirect('mostrar_usuarios')
    return render(request, 'App/crear_usuario.html')

def mostrar_usuarios(request):
    usuarios = Usuario.objects.all()
    context = {
        'usuarios': usuarios
    }
    return render(request, 'App/mostrar_usuarios.html', context)

def buscar_usuario(request):
    usuario = None
    if request.method == 'POST':
        email = request.POST.get('email')
        usuario = Usuario.objects.filter(email=email).first()
    return render(request, 'App/buscar_usuario.html', {'usuario': usuario})

def crear_animal(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        especie = request.POST.get('especie')
        animal = Animal(nombre=nombre, edad=edad, especie=especie)
        animal.save()
        return redirect('mostrar_animales')
    return render(request, 'App/crear_animal.html')

def mostrar_animales(request):
    animales = Animal.objects.all()
    context = {
        'animales': animales
    }
    return render(request, 'App/mostrar_animales.html', context)

def buscar_animal(request):
    animal = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        animal = Animal.objects.filter(nombre=nombre).first()
    return render(request, 'App/buscar_animal.html', {'animal': animal})
