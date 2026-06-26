from django.contrib import admin
from .models import PerfilUsuario, AvanceFisico, Rutina

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'fecha_nacimiento']
    search_fields = ['user__username', 'user__email']

@admin.register(AvanceFisico)
class AvanceFisicoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha', 'peso', 'porcentaje_grasa']
    list_filter = ['fecha']

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'creado_por', 'fecha_creacion']
    list_filter = ['nivel', 'fecha_creacion']
    filter_horizontal = ['asignada_a']
