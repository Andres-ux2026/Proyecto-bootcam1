from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

class AvanceFisico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avances')
    fecha = models.DateField(auto_now_add=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)')
    porcentaje_grasa = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='% Grasa')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha}'

    class Meta:
        verbose_name = 'Avance físico'
        verbose_name_plural = 'Avances físicos'
        ordering = ['-fecha']

class Rutina(models.Model):
    NIVELES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES)
    creado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rutinas_creadas',
        limit_choices_to={'is_staff': True}
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignada_a = models.ManyToManyField(
        User, related_name='rutinas_asignadas', blank=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['-fecha_creacion']
