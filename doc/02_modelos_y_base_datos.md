# Modelos y Base de Datos

## Modelos Definidos

### PerfilUsuario
- `user`: OneToOneField(User) - Relación uno a uno con usuario Django
- `telefono`: CharField - Teléfono del usuario
- `fecha_nacimiento`: DateField - Fecha de nacimiento
- Señal `post_save` crea automáticamente el perfil al registrar usuario

### AvanceFisico
- `usuario`: ForeignKey(User) - Usuario que registra el avance
- `fecha`: DateField(auto_now_add) - Fecha del registro
- `peso`: DecimalField - Peso en kg
- `porcentaje_grasa`: DecimalField - Porcentaje de grasa corporal
- `notas`: TextField - Notas adicionales

### Rutina
- `nombre`: CharField - Nombre de la rutina
- `descripcion`: TextField - Descripción detallada
- `nivel`: CharField(choices) - Principiante, Intermedio, Avanzado
- `creado_por`: ForeignKey(User, staff only) - Admin que creó la rutina
- `fecha_creacion`: DateTimeField(auto_now_add)
- `asignada_a`: ManyToManyField(User) - Usuarios asignados

## Migraciones
Ejecutadas con `makemigrations` y `migrate`.
