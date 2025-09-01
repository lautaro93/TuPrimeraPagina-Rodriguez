"""
URL configuration for Entrega3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.crear_receta, name='crear_receta'),
    path('recetas/mostrar', views.mostrar_recetas, name='mostrar_recetas'),
    path('usuarios/crear', views.crear_usuario, name='crear_usuario'),
    path('usuarios/mostrar', views.mostrar_usuarios, name='mostrar_usuarios'),
    path('recetas/buscar', views.buscar_receta, name='buscar_receta'),
    path('usuarios/buscar', views.buscar_usuario, name='buscar_usuario'),
    path('animales/crear', views.crear_animal, name='crear_animal'),
    path('animales/mostrar', views.mostrar_animales, name='mostrar_animales'),
    path('animales/buscar', views.buscar_animal, name='buscar_animal'),
]
