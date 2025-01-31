from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PersonaListaView

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),  # Página principal que lista los proyectos
    path('project/<int:pk>/', views.project_detail, name='project_detail'),  # Detalle del proyecto
    path('project/<int:pk>/comment/', views.add_comment, name='add_comment'),  # Agregar comentario
    path('project/<int:pk>/vote/', views.add_vote, name='add_vote'),  # Agregar voto
    path('register/', views.user_register, name='user_register'),  # Registro de usuario
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='user_login'),
    path('bienvenido/', views.bienvenido, name='bienvenido'),  # Nueva ruta
    path('index/', views.index, name='index'),  # Nueva ruta
    path('logout/', views.user_logout, name='logout'),  # Cierre de sesión
    path('profile/', views.user_profile, name='profile'),  # Perfil del usuario
    path('proyectos/', views.proyectos, name='proyectos'),  # Página de proyectos
    path('resultados/', views.resultados, name='resultados'),  # Resultados de votaciones
    path('pal2024-2026/', views.pal_2024_2026, name='pal_2024_2026'),
    path('cajamarcaga/', views.cajamarcaga, name='cajamarcaga'),
    path('nosc-caj/', views.nosc_caj, name='nosc_caj'),  # NOSC Cajamarca
    path('repositorio/', views.repositorio_view, name='repositorio'),  # Repositorio de documentos
    path('contacto/', views.contacto, name='contacto'),  # Página de contacto
    path('terms_and_conditions/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
    path('politicaprivacidad/', views.politicaprivacidad, name='politicaprivacidad'),
    path('introduccion/', views.introducción, name='introduccion'),

    path('registrar_organizacion/', views.registrar_organizacion, name='registrar_organizacion'),
    path('registrar_persona/', views.registrar_persona, name='registrar_persona'),
    path('persona_list/', PersonaListaView.as_view(), name='persona_list'),
    path('editar_persona/<int:id>/', views.editar_persona, name='editar_persona'),
    path('eliminar_persona/<int:id>/', views.eliminar_persona, name='eliminar_persona'),
    path('confirmar_eliminar_persona/<int:id>/', views.confirmar_eliminar_persona, name='confirmar_eliminar_persona'),

    path('organizacion_lista/', views.organizacion_lista, name='organizacion_lista'),
    path('organizaciones/editar/<int:pk>/', views.editar_organizacion, name='editar_organizacion'),
    path('organizaciones/eliminar/<int:pk>/', views.eliminar_organizacion, name='eliminar_organizacion'),
    path('confirmar_eliminar_organizacion/<int:id>/', views.confirmar_eliminar_organizacion, name='confirmar_eliminar_organizacion'),
    path('configuracion/', views.configuracion, name='configuracion'),

    path('miembros/', views.miembros_view, name='miembros'),
    path('foro_multiactor/', views.foro_multiactor, name='foro_multiactor'),
    path('documentos_list/', views.documentos_list, name='documentos_list'),
    path('registrar_documento/', views.registrar_documento, name='registrar_documento'),
    path('editar_documento/<int:pk>/', views.editar_documento, name='editar_documento'),
    path('eliminar_documento/<int:pk>/', views.eliminar_documento, name='eliminar_documento'),
    path('confirmar_eliminar_documento/<int:id>/', views.confirmar_eliminar_documento, name='confirmar_eliminar_documento'),

    path('usuarios_list/', views.usuarios_list, name='usuarios_list'),
    path('editar_user/<int:pk>/', views.editar_user, name='editar_user'),
    path('confirmar_eliminar_user/<int:id>/', views.confirmar_eliminar_user, name='confirmar_eliminar_user'),

    path('ejes_list/', views.ejes_list, name='ejes_list'),
    path('lista_compromisos/', views.lista_compromisos, name='lista_compromisos'),
    path('no_autorizado/', views.no_autorizado, name='no_autorizado'),
    path('eventos/', views.eventos_lista, name='eventos_lista'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('editar_evento/<int:id>/', views.editar_evento, name='editar_evento'),
    path('calendario/', views.calendario, name='calendario'),

    path('introduccionpal/', views.introduccionpal, name='introduccionpal'),
    path('tablero/', views.tablero, name='tablero'),
    path('metodologia/', views.metodologia, name='metodologia'),
    path('hitos_lista/', views.hitos_lista, name='hitos_lista'),
    path('agregar_hito/', views.agregar_hito, name='agregar_hito'),
    path('eliminar_hito/<int:pk>/', views.eliminar_hito, name='eliminar_hito'),
    path('crear_compromiso/', views.crear_compromiso, name='crear_compromiso'),
    path('detalle_compromiso/<int:pk>/', views.detalle_compromiso, name='detalle_compromiso'),
    path('detalle-compromiso/<int:pk>/', views.detalle__compromiso, name='detalle-compromiso'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)