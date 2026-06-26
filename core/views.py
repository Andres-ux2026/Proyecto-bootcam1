from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistroForm, AvanceFisicoForm, RutinaForm
from .models import AvanceFisico, Rutina, PerfilUsuario

def es_admin(user):
    return user.is_staff

def home(request):
    slides = [
        {
            'image': 'https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg',
            'title': 'Transforma tu Cuerpo',
            'description': 'Entrenamientos diseñados para todos los niveles con instructores certificados.',
        },
        {
            'image': 'https://images.pexels.com/photos/6550839/pexels-photo-6550839.jpeg',
            'title': 'Supera tus Límites',
            'description': 'HIIT, fuerza, funcional y más. Encuentra la disciplina que te apasiona.',
        },
        {
            'image': 'https://images.pexels.com/photos/6455874/pexels-photo-6455874.jpeg',
            'title': 'Resultados Reales',
            'description': 'Seguimiento personalizado de tu avance físico con métricas detalladas.',
        },
    ]
    planes = [
        {
            'nombre': 'Mensual',
            'precio': '29.990',
            'periodo': 'mes',
            'descripcion': 'Perfecto para empezar y probar nuestras instalaciones.',
            'destacado': False,
            'beneficios': ['Acceso ilimitado al gimnasio', 'Clases grupales incluidas', 'Evaluación física inicial', 'App de seguimiento', 'Sin permanencia mínima'],
        },
        {
            'nombre': 'Semestral',
            'precio': '19.990',
            'periodo': 'mes',
            'descripcion': 'Nuestro plan más elegido. Entrena sin preocupaciones.',
            'destacado': True,
            'beneficios': ['Todo lo del plan Mensual', '2 meses gratis', 'Nutricionista incluido', 'Acceso a eventos exclusivos', 'Plan personalizado'],
        },
        {
            'nombre': 'Anual',
            'precio': '14.990',
            'periodo': 'mes',
            'descripcion': 'Para los que entrenan en serio. Mayor beneficio económico.',
            'destacado': False,
            'beneficios': ['Todo lo del plan Semestral', '6 meses gratis', 'Sesiones con entrenador personal', 'Parking gratis', 'Acceso 24/7'],
        },
    ]
    disciplinas = [
        {'nombre': 'Funcional', 'descripcion': 'Entrenamiento completo que mejora tu día a día.', 'image': 'https://images.pexels.com/photos/3289711/pexels-photo-3289711.jpeg'},
        {'nombre': 'HIIT', 'descripcion': 'Alta intensidad para quemar calorías en tiempo récord.', 'image': 'https://images.pexels.com/photos/6455874/pexels-photo-6455874.jpeg'},
        {'nombre': 'Fuerza', 'descripcion': 'Desarrolla músculo y aumenta tu potencia.', 'image': 'https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg'},
    ]
    return render(request, 'core/home.html', {
        'slides': slides,
        'planes': planes,
        'disciplinas': disciplinas,
    })

def register_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a AkelaGym.')
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    avances = AvanceFisico.objects.filter(usuario=request.user)
    rutinas = Rutina.objects.filter(asignada_a=request.user)
    return render(request, 'core/dashboard.html', {
        'avances': avances,
        'rutinas': rutinas,
    })

@login_required
def crear_avance(request):
    if request.method == 'POST':
        form = AvanceFisicoForm(request.POST)
        if form.is_valid():
            avance = form.save(commit=False)
            avance.usuario = request.user
            avance.save()
            messages.success(request, 'Avance registrado correctamente.')
            return redirect('dashboard')
    else:
        form = AvanceFisicoForm()
    return render(request, 'core/crear_avance.html', {'form': form})

@user_passes_test(es_admin)
def lista_rutinas(request):
    rutinas = Rutina.objects.all()
    return render(request, 'core/lista_rutinas.html', {'rutinas': rutinas})

@user_passes_test(es_admin)
def crear_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.creado_por = request.user
            rutina.save()
            form.save_m2m()
            messages.success(request, 'Rutina creada exitosamente.')
            return redirect('lista_rutinas')
    else:
        form = RutinaForm()
    return render(request, 'core/rutina_form.html', {'form': form, 'titulo': 'Crear Rutina'})

@user_passes_test(es_admin)
def editar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualizada exitosamente.')
            return redirect('lista_rutinas')
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'core/rutina_form.html', {'form': form, 'titulo': 'Editar Rutina'})

@user_passes_test(es_admin)
def eliminar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        rutina.delete()
        messages.success(request, 'Rutina eliminada exitosamente.')
        return redirect('lista_rutinas')
    return render(request, 'core/confirmar_eliminar.html', {'rutina': rutina})

@user_passes_test(es_admin)
def lista_usuarios(request):
    from django.contrib.auth.models import User
    usuarios = User.objects.filter(is_staff=False)
    return render(request, 'core/lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(es_admin)
def detalle_usuario(request, pk):
    from django.contrib.auth.models import User
    usuario = get_object_or_404(User, pk=pk)
    avances = AvanceFisico.objects.filter(usuario=usuario)
    return render(request, 'core/detalle_usuario.html', {
        'usuario': usuario,
        'avances': avances,
    })
