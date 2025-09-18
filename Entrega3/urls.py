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
from django.conf import settings
from django.conf.urls.static import static
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('registrarse/', views.RegistrarseView.as_view(), name='registrarse'),
    path('iniciar-sesion/', views.IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('cerrar-sesion/', views.CerrarSesionView.as_view(), name='cerrar_sesion'),
    path('perfil/', views.PerfilUsuarioView.as_view(), name='perfil_usuario'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),
    path('perfil/cambiar-password/', views.CambiarPasswordView.as_view(), name='cambiar_password'),
    path('recetas/crear/', views.CrearRecetaView.as_view(), name='crear_receta'),
    path('recetas/mostrar/', views.MostrarRecetasView.as_view(), name='mostrar_recetas'),
    path('recetas/mis-recetas/', views.MisRecetasView.as_view(), name='mis_recetas'),
    path('recetas/editar/<int:receta_id>/', views.EditarRecetaView.as_view(), name='editar_receta'),
    path('recetas/eliminar/<int:receta_id>/', views.EliminarRecetaView.as_view(), name='eliminar_receta'),
    path('recetas/buscar/', views.BuscarRecetaView.as_view(), name='buscar_receta'),
    path('animales/', views.animales, name='animales'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
