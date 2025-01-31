from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView

from .models import Eje, Compromiso, Comentario, Voto, RedSocial, Persona, Organizacion, Categoria, Documento, Evento, \
    Hito, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, UserLoginForm, EventoForm, ProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import OrganizacionForm, PersonaForm, DocumentoForm
from django.views import View

def superuser_check(user):
    return user.is_superuser
def home(request):
    compromisos = Compromiso.objects.all()
    return render(request, 'core/home.html', {'projects': compromisos})

def project_detail(request, pk):
    project = get_object_or_404(Compromiso, pk=pk)
    comments = project.comments.all()
    votes_count = project.votes.count()
    return render(request, 'core/project_detail.html', {
        'project': project,
        'comments': comments,
        'votes_count': votes_count,
    })

@login_required
def add_comment(request, pk):
    project = get_object_or_404(Compromiso, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comentario.objects.create(user=request.user, project=project, content=content)
    return redirect('core:project_detail', pk=pk)

@login_required
def add_vote(request, pk):
    project = get_object_or_404(Compromiso, pk=pk)
    try:
        Voto.objects.create(user=request.user, project=project)
    except:
        pass  # El usuario ya votó
    return JsonResponse({'votes_count': project.votes.count()})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('core:user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Obtiene el usuario autenticado
            login(request, user)  # Inicia la sesión del usuario
            messages.success(request, f"¡Bienvenido, {user.username}!")

            # Verifica si el usuario es superusuario
            if user.is_superuser:
                return redirect('core:bienvenido')  # Superusuarios
            else:
                return redirect('core:index')  # Usuarios normales
        else:
            messages.error(request, "Credenciales inválidas. Por favor, verifica e intenta nuevamente.")
    else:
        form = UserLoginForm()

    return render(request, 'core/login.html', {'form': form})



@login_required
@user_passes_test(superuser_check, login_url='/no_autorizado/')
def bienvenido(request):
    return render(request, 'core/bienvenido.html')

@login_required
def index(request):
    return render(request, 'core/index.html')

def proyectos(request):
    return render(request, 'core/proyectos.html')

def no_autorizado(request):
    return render(request, 'core/no_autorizado.html')

def resultados(request):
    return render(request, 'core/resultados.html')
@login_required
def user_profile(request):
    return render(request, 'core/profile.html')

def user_logout(request):
    logout(request)
    return redirect('core:home')


def pal_2024_2026(request):
    return render(request, 'core/pal_2024_2026.html')

def cajamarcaga(request):
    return render(request, 'core/cajamarcaga.html')

def nosc_caj(request):
    return render(request, 'core/nosc_caj.html')

def repositorio_view(request):
    categorias = Categoria.objects.prefetch_related('documentos').all()
    context = {'categorias': categorias}
    return render(request, 'core/repositorio.html', context)

def contacto(request):
    redes = RedSocial.objects.all()
    return render(request, 'core/contacto.html', {'redes': redes})

def terminos_y_condiciones(request):
    return render(request, 'core/terms_and_conditions.html')

def politicaprivacidad(request):
    return render(request, 'core/politicaprivacidad.html')

def introducción(request):
    return render(request, 'core/introduccion.html')

def miembros(request):
    return render(request, 'core/miembros.html')

# Función para verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser


# Vista para crear una nueva organizacion
@user_passes_test(superuser_check, login_url='/no_autorizado/')
def registrar_organizacion(request):
    if request.method == 'POST':
        form = OrganizacionForm(request.POST, request.FILES)  # Incluye request.FILES para manejar archivos
        if form.is_valid():
            form.save()
            return redirect('core:organizacion_lista')  # Cambia según tu nombre de URL
    else:
        form = OrganizacionForm()
    return render(request, 'core/registrar_organizacion.html', {'form': form})


# Vista para crear una nueva persona
@user_passes_test(superuser_check, login_url='/no_autorizado/')
def registrar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:persona_list')  # Puedes redirigir a una lista de personas
    else:
        form = PersonaForm()
    return render(request, 'core/registrar_persona.html', {'form': form})

# Vista para editar una persona
@user_passes_test(superuser_check, login_url='/no_autorizado/')
def editar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)

    if request.method == "POST":
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('core:persona_list')  # Redirige a la lista de personas
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'core/editar_persona.html', {'form': form, 'persona': persona})


class PersonaListaView(View):
    def get(self, request):
        personas = Persona.objects.all()  # Obtener todas las personas
        paginator = Paginator(personas, 5)  # Dividir en páginas, 5 personas por página
        page_number = request.GET.get('page')  # Número de página actual
        page_obj = paginator.get_page(page_number)  # Obtener el objeto de la página actual
        return render(request, 'core/persona_list.html', {'page_obj': page_obj})

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('core:persona_list')

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def confirmar_eliminar_persona(request, id):
    persona = get_object_or_404(Persona, id=id)

    if request.method == 'POST':
        persona.delete()
        return redirect('core:persona_list')  # Redirige a la lista de personas
    return render(request, 'core/confirmar_eliminar_persona.html', {'persona': persona})

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def organizacion_lista(request):
    organizaciones = Organizacion.objects.prefetch_related('provincias').all()

    # Paginación: 10 elementos por página
    paginator = Paginator(organizaciones, 5)
    page_number = request.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene los elementos de la página actual

    context = {
        'page_obj': page_obj  # Enviamos el objeto de la página al contexto
    }
    return render(request, 'core/organizacion_lista.html', context)

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def eliminar_organizacion(request, pk):
    # Intenta obtener la organización o lanza un error 404 si no existe
    organizacion = get_object_or_404(Organizacion, pk=pk)

    if request.method == "POST":
        # Elimina la organización si se envió una solicitud POST
        organizacion.delete()
        return redirect('core:organizacion_lista')

    return render(request, 'core/eliminar_organizacion.html', {'organizacion': organizacion})

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def editar_organizacion(request, pk):
    organizacion = get_object_or_404(Organizacion, pk=pk)

    if request.method == 'POST':
        form = OrganizacionForm(request.POST, instance=organizacion)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('core:organizacion_lista')  # Redirigir a la lista
    else:
        # Prellenar el formulario con los datos de la organización
        form = OrganizacionForm(instance=organizacion)

    return render(request, 'core/editar_organizacion.html', {'form': form, 'organizacion': organizacion})

@user_passes_test(superuser_check, login_url='/no_autorizado/')
def confirmar_eliminar_organizacion(request, id):
    organizacion = get_object_or_404(Organizacion, id=id)

    if request.method == 'POST':
        organizacion.delete()
        return redirect('core:organizacion_lista')
    return render(request, 'core/confirmar_eliminar_organizacion.html', {'organizacion': organizacion})

def configuracion(request):
    return render(request, 'core/configuracion.html')

def miembros_view(request):
    personas = Persona.objects.all()
    context = {'personas': personas}
    return render(request, 'core/miembros.html', context)

def foro_multiactor(request):
    return render(request, 'core/foro_multiactor.html')

def documentos_list(request):
    documentos = Documento.objects.select_related('categoria').all()
    paginator = Paginator(documentos, 10)  # Muestra 10 documentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/documentos_list.html', {'page_obj': page_obj})

def registrar_documento(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        categoria_id = request.POST['categoria']
        url = request.POST['url']
        categoria = Categoria.objects.get(id=categoria_id)
        Documento.objects.create(nombre=nombre, categoria=categoria, url=url)
        return redirect('core:documentos_list')  # Cambia el nombre si es diferente
    return render(request, 'core/registrar_documento.html', {'categorias': categorias})

def editar_documento(request, pk):
    documento = get_object_or_404(Documento, id=pk)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect('core:documentos_list')
    else:
        form = DocumentoForm(instance=documento)
    return render(request, 'core/editar_documento.html', {'form': form})

def eliminar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    documento.delete()
    return redirect('core:documentos_list')

def confirmar_eliminar_documento(request, id):
    documento = get_object_or_404(Documento, id=id)

    if request.method == 'POST':
        documento.delete()
        return redirect('core:documentos_list')  # Redirige a la lista de personas
    return render(request, 'core/confirmar_eliminar_documento.html', {'documento': documento})

def usuarios_list(request):
    usuarios = User.objects.all()

    # Paginación: 10 elementos por página
    paginator = Paginator(usuarios, 5)
    page_number = request.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene los elementos de la página actual

    context = {
        'page_obj': page_obj  # Enviamos el objeto de la página al contexto
    }
    return render(request, 'core/usuarios_list.html', context)

@login_required
def editar_user(request, pk):
    user_to_edit = get_object_or_404(User, pk=pk)

    # Verifica que el usuario actual sea un superusuario
    if not request.user.is_superuser:
        return redirect('core:usuarios_list')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            # Guarda al usuario editado sin afectar la sesión
            form.save()
            return redirect('core:usuarios_list')
    else:
        form = UserRegistrationForm(instance=user_to_edit)

    return render(request, 'core/editar_user.html', {
        'form': form,
        'user_to_edit': user_to_edit,  # Cambia la variable para evitar confusiones
    })

def confirmar_eliminar_user(request, id):  # o pk si prefieres usar pk
    user = get_object_or_404(User, id=id)  # Aquí usamos id para obtener el usuario
    if request.method == 'POST':
        user.delete()  # Eliminar el usuario
        return redirect('core:usuarios_list')  # Redirigir a la lista de usuarios después de eliminar
    return render(request, 'core/confirmar_eliminar_user.html', {'user': user})

def ejes_list(request):
    ejes = Eje.objects.all()

    # Paginación: 10 elementos por página
    paginator = Paginator(ejes, 5)
    page_number = request.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene los elementos de la página actual

    context = {
        'page_obj': page_obj  # Enviamos el objeto de la página al contexto
    }
    return render(request, 'core/ejes_list.html', context)

def compromisos_list(request):
    compromisos = Compromiso.objects.all()

    # Paginación: 10 elementos por página
    paginator = Paginator(compromisos,10)
    page_number = request.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene los elementos de la página actual

    context = {
        'page_obj': page_obj  # Enviamos el objeto de la página al contexto
    }
    return render(request, 'core/compromisos_list.html', context)


@user_passes_test(is_superuser)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:eventos_lista')
    else:
        form = EventoForm()
    return render(request, 'core/crear_evento.html', {'form': form})




@user_passes_test(is_superuser)
def eventos_lista(request):
    eventos = Evento.objects.all()
    paginator = Paginator(eventos, 10)  # Cambia 10 por el número de eventos por página que prefieras
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/eventos_lista.html', {'page_obj': page_obj})

def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)  # Busca el evento con el ID o devuelve un 404
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('core:eventos_lista')  # Redirige a la lista de eventos
    else:
        form = EventoForm(instance=evento)
    return render(request, 'core/editar_evento.html', {'form': form})



from datetime import date

def calendario(request):
        eventos = Evento.objects.all()
        today = date.today()

        for evento in eventos:
            # Validación segura de las fechas
            if evento.fechainicio and evento.fechafin:
                if evento.fechainicio > today:
                    evento.estado = 'futura'
                elif evento.fechainicio <= today <= evento.fechafin:
                    evento.estado = 'en_curso'
                else:
                    evento.estado = 'pasada'
            else:
                evento.estado = 'sin_fecha'  # Estado para eventos sin fechas válidas

        return render(request, 'core/calendario.html', {'eventos': eventos, 'today': today})

from .models import Compromiso
from .forms import CompromisoForm, HitoForm

def lista_compromisos(request):
    compromisos = Compromiso.objects.all()
    return render(request, 'core/lista_compromisos.html', {'compromisos': compromisos})

def detalle_compromiso(request, pk):
    compromiso = get_object_or_404(Compromiso, pk=pk)
    hitos = compromiso.hitos.all()
    return render(request, 'core/detalle_compromiso.html', {'compromiso': compromiso, 'hitos': hitos})

def crear_compromiso(request):
    if request.method == 'POST':
        form = CompromisoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:lista_compromisos')
    else:
        form = CompromisoForm()
    return render(request, 'core/crear_compromiso.html', {'form': form})

def editar_compromiso(request, pk):
    compromiso = get_object_or_404(Compromiso, pk=pk)
    if request.method == 'POST':
        form = CompromisoForm(request.POST, instance=compromiso)
        if form.is_valid():
            form.save()
            return redirect('detalle_compromiso', pk=pk)
    else:
        form = CompromisoForm(instance=compromiso)
    return render(request, 'core/editar_compromiso.html', {'form': form})

def eliminar_compromiso(request, pk):
    compromiso = get_object_or_404(Compromiso, pk=pk)
    compromiso.delete()
    return redirect('lista_compromisos')


# Vista para crear un nuevo hito
@user_passes_test(superuser_check, login_url='/no_autorizado/')
def agregar_hito(request):
    if request.method == 'POST':
        form = HitoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:hitos_lista')  # Puedes redirigir a una lista de personas
    else:
        form = HitoForm()
    return render(request, 'core/agregar_hito.html', {'form': form})


def introduccionpal(request):
    return render(request, 'core/introduccionpal.html')

def tablero(request):
    compromisos = Compromiso.objects.all()  # Obtiene todos los compromisos
    return render(request, 'core/tablero.html', {'compromisos': compromisos})

def metodologia(request):
    return render(request, 'core/metodologia.html')


def hitos_lista(request):
    hitos = Hito.objects.all()  # Recupera todos los hitos
    paginator = Paginator(hitos, 10)  # Dividir los hitos en páginas de 10 registros
    page_number = request.GET.get('page')  # Obtiene el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtiene la página correspondiente
    return render(request, 'core/hitos_lista.html', {'page_obj': page_obj})

def detalle_compromiso(request, pk):
    compromiso = get_object_or_404(Compromiso, pk=pk)
    return render(request, 'core/detalle_compromiso.html', {'compromiso': compromiso})

def eliminar_hito(request, pk):
    hito = get_object_or_404(Hito, pk=pk)
    compromiso = hito.compromiso  # Suponiendo que 'compromiso' es la ForeignKey en Hito
    hito.delete()
    messages.success(request, "El hito ha sido eliminado correctamente.")
    return redirect('core:detalle_compromiso', pk=compromiso.id)

def detalle__compromiso(request, pk):
    from django.db.models import Count, Q

    compromiso = get_object_or_404(Compromiso, pk=pk)

    # Total de hitos
    total_hitos = compromiso.hitos.count()

    # Total de hitos completados
    hitos_terminados = compromiso.hitos.filter(estado="Terminado").count()

    # Calcula el porcentaje de avance
    porcentaje = 0 if total_hitos == 0 else int((hitos_terminados / total_hitos) * 100)

    return render(request, 'core/detalle-compromiso.html', {
        'compromiso': compromiso,
        'porcentaje': porcentaje
    })

@login_required
def editar_perfil(request):
    perfil, created = Profile.objects.get_or_create(user=request.user)  # Obtener o crear perfil

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('core:profile')  # Redirige a la página de perfil
    else:
        form = ProfileForm(instance=perfil)

    return render(request, 'core/editar_perfil.html', {'form': form})