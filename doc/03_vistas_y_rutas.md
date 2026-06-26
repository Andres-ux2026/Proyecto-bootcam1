# Vistas y Rutas (FBVs)

## Vistas Públicas
- `home` - Landing page con carrusel, planes y disciplinas
- `register_view` - Registro de usuarios con formulario personalizado
- `login_view` - Inicio de sesión
- `logout_view` - Cierre de sesión

## Vistas Privadas (Requieren Login)
- `dashboard_view` - Perfil, historial de avance con Chart.js, rutinas asignadas
- `crear_avance` - Formulario para registrar peso, %grasa y notas

## Vistas Admin (Requieren Staff)
- `lista_rutinas` - CRUD listar rutinas
- `crear_rutina` - Crear nueva rutina
- `editar_rutina` - Editar rutina existente
- `eliminar_rutina` - Eliminar rutina
- `lista_usuarios` - Listar clientes registrados
- `detalle_usuario` - Ver avances de un usuario

## Mapeo de URLs
Todas las rutas siguen la estructura definida en el PRD sección 5.
