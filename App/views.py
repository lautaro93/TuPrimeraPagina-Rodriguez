from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Receta, Animal, Avatar
from .forms import RegistroUsuarioForm, ActualizarPerfilForm, AvatarForm
class IndexView(TemplateView):
    template_name = 'App/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_recetas'] = Receta.objects.count()
        context['total_usuarios'] = User.objects.count()
        return context

class AboutView(TemplateView):
    template_name = 'App/about.html'
class IniciarSesionView(View):
    template_name = 'App/iniciarSesion.html'
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}!')
                return redirect('mostrar_recetas')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, self.template_name, {'form': form})
class RegistrarseView(View):
    template_name = 'App/registrarse.html'
    form_class = RegistroUsuarioForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'formulario': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente!')
            return redirect('iniciar_sesion')
        return render(request, self.template_name, {'formulario': form})
class CerrarSesionView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada exitosamente.')
        return redirect('iniciar_sesion')
    
class PerfilUsuarioView(LoginRequiredMixin, View):
    login_url = 'iniciar_sesion'
    template_name = 'App/perfil_usuario.html'
    
    def get(self, request):
        context = {
            'user': request.user,
            'total_recetas': Receta.objects.filter(autor=request.user).count()
        }
        return render(request, self.template_name, context)
    
class EditarPerfilView(LoginRequiredMixin, View):
    login_url = 'iniciar_sesion'
    template_name = 'App/editar_perfil.html'
    
    def get(self, request):
        perfil_form = ActualizarPerfilForm(instance=request.user)
        avatar, created = Avatar.objects.get_or_create(user=request.user)
        avatar_form = AvatarForm(instance=avatar)
        context = {
            'perfil_form': perfil_form,
            'avatar_form': avatar_form,
            'user': request.user
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        avatar, created = Avatar.objects.get_or_create(user=request.user)

        perfil_form = ActualizarPerfilForm(request.POST, instance=request.user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        
        perfil_valido = perfil_form.is_valid()
        avatar_valido = avatar_form.is_valid()
        
        if perfil_valido and avatar_valido:
            perfil_form.save()
            avatar_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_usuario')
        else:
            context = {
                'perfil_form': perfil_form,
                'avatar_form': avatar_form,
                'user': request.user
            }
            return render(request, self.template_name, context)
class CambiarPasswordView(LoginRequiredMixin, View):
    login_url = 'iniciar_sesion'
    template_name = 'App/cambiar_password.html'
    
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('perfil_usuario')
        return render(request, self.template_name, {'form': form})
class CrearRecetaView(LoginRequiredMixin, View):
    login_url = 'iniciar_sesion'
    template_name = 'App/crear_receta.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        nombre = request.POST.get('nombre')
        imagen = request.POST.get('imagen')
        ingredientes = request.POST.get('ingredientes')
        instrucciones = request.POST.get('instrucciones')
        
        Receta.objects.create(
            nombre=nombre,
            imagen=imagen,
            ingredientes=ingredientes,
            instrucciones=instrucciones,
            autor=request.user
        )
        return redirect('mostrar_recetas')
class MostrarRecetasView(ListView):
    model = Receta
    template_name = 'App/mostrar_recetas.html'
    context_object_name = 'recetas'
    
    def get_queryset(self):
        usuario_id = self.request.GET.get('usuario')
        if usuario_id:
            return Receta.objects.filter(autor_id=usuario_id)
        return Receta.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_id = self.request.GET.get('usuario')
        if usuario_id:
            try:
                context['usuario_filtrado'] = User.objects.get(id=usuario_id)
            except User.DoesNotExist:
                context['usuario_filtrado'] = None
        else:
            context['usuario_filtrado'] = None
        context['usuarios_con_recetas'] = User.objects.filter(receta__isnull=False).distinct()
        return context
class MisRecetasView(LoginRequiredMixin, ListView):
    login_url = 'iniciar_sesion'
    model = Receta
    template_name = 'App/mis_recetas.html'
    context_object_name = 'recetas'
    
    def get_queryset(self):
        return Receta.objects.filter(autor=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Mis Recetas - {self.request.user.username}'
        return context
class EditarRecetaView(LoginRequiredMixin, UpdateView):
    model = Receta
    fields = ['nombre', 'imagen', 'ingredientes', 'instrucciones']
    template_name = 'App/editar_receta.html'
    success_url = reverse_lazy('mis_recetas')
    pk_url_kwarg = 'receta_id'
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(Receta, id=self.kwargs['receta_id'], autor=self.request.user)
        return obj
    
    def form_valid(self, form):
        messages.success(self.request, 'Receta actualizada exitosamente.')
        return super().form_valid(form)
class EliminarRecetaView(LoginRequiredMixin, DeleteView):
    model = Receta
    template_name = 'App/eliminar_receta.html'
    success_url = reverse_lazy('mis_recetas')
    pk_url_kwarg = 'receta_id'
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(Receta, id=self.kwargs['receta_id'], autor=self.request.user)
        return obj
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Receta eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

class BuscarRecetaView(View):
    template_name = 'App/buscar_receta.html'
    
    def get(self, request):
        receta = None
        searched = False
        if 'nombre' in request.GET:
            nombre = request.GET.get('nombre')
            searched = True
            try:
                receta = Receta.objects.get(nombre__iexact=nombre)
            except Receta.DoesNotExist:
                receta = None
        return render(request, self.template_name, {'receta': receta, 'searched': searched})

@login_required(login_url='iniciar_sesion')
def animales(request):
    if request.method == 'POST':
        if 'crear' in request.POST:
            return _crear_animal(request)
        elif 'buscar' in request.POST:
            return _buscar_animal(request)
    animales = Animal.objects.all()
    return render(request, 'App/animal.html', {'animales': animales})

def _crear_animal(request):
    """Función auxiliar para crear un animal"""
    nombre = request.POST.get('nombre')
    edad = request.POST.get('edad')
    especie = request.POST.get('especie')
    if nombre and edad and especie:
        try:
            Animal.objects.create(nombre=nombre, edad=int(edad), especie=especie)
            messages.success(request, f'Animal "{nombre}" creado exitosamente.')
        except ValueError:
            messages.error(request, 'La edad debe ser un número válido.')
    else:
        messages.error(request, 'Todos los campos son obligatorios.')
    
    return redirect('animales')

def _buscar_animal(request):
    nombre = request.POST.get('nombre_buscar')
    animales = Animal.objects.all()
    animal = None
    if nombre:
        animales = animales.filter(nombre__icontains=nombre)
        animal = animales.first()
        if not animales.exists():
            messages.info(request, f'No se encontraron animales con el nombre "{nombre}".')
    
    return render(request, 'App/animal.html', {'animales': animales, 'animal': animal})

