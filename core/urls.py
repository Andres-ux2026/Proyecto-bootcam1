from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('avance/nuevo/', views.crear_avance, name='crear_avance'),
    path('admin-gym/rutinas/', views.lista_rutinas, name='lista_rutinas'),
    path('admin-gym/rutinas/crear/', views.crear_rutina, name='crear_rutina'),
    path('admin-gym/rutinas/editar/<int:pk>/', views.editar_rutina, name='editar_rutina'),
    path('admin-gym/rutinas/eliminar/<int:pk>/', views.eliminar_rutina, name='eliminar_rutina'),
    path('admin-gym/usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('admin-gym/usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
]
