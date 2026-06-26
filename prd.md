# Product Requirement Document (PRD) - Gimnasio Web App

## 1. Introducción y Objetivos
Este proyecto consiste en el desarrollo de una aplicación web para la gestión y promoción de un gimnasio, inspirada en la estructura y estética de `energytime.cl`. El objetivo es ofrecer una plataforma informativa para visitantes y un sistema de gestión interna para usuarios registrados y administradores.

### Objetivos Clave:
* **Público General:** Visualizar entrenamientos, planes de precios y registrarse/iniciar sesión.
* **Usuarios (Clientes):** Gestionar su perfil y registrar/visualizar su avance físico.
* **Administrador:** Gestionar usuarios y un CRUD completo de rutinas de entrenamiento.

---

## 2. Arquitectura Tecnológica
* **Backend Framework:** Django 6.0
* **Base de Datos:** SQLite (Entorno de desarrollo y producción simplificado)
* **Frontend:** Django Templates + Tailwind CSS (vía CDN)
* **Arquitectura de Vistas:** Vistas Basadas en Funciones (FBVs)
* **Despliegue:** Render

---

## 3. Requisitos Funcionales (Por Rol)

### 3.1. Usuario Anónimo (Landing Page)
* **Carrusel de Entrenamientos:** Sección interactiva que muestra las disciplinas del gimnasio (funcional, HIIT, fuerza, etc.).
* **Cards de Planes:** Tabla de precios y beneficios por plan (Mensual, Semestral, Anual).
* **Autenticación:** Registro de usuarios, Inicio de sesión (Login) y Cierre de sesión (Logout).

### 3.2. Usuario Registrado (Cliente)
* **Dashboard/Perfil:** Vista privada con sus datos personales.
* **Historial de Avance:** Formulario para registrar peso, porcentaje de grasa o medidas, y una tabla/lista para ver su evolución en el tiempo.
* **Visualización de Rutinas:** Sección para ver las rutinas asignadas por el administrador.

### 3.3. Administrador (Staff)
* **Panel de Control:** Acceso a la gestión global.
* **CRUD de Rutinas:** * Crear nuevas rutinas (Nombre, descripción, series, repeticiones, nivel).
    * Leer/Listar rutinas existentes.
    * Actualizar/Editar rutinas.
    * Eliminar rutinas.
* **Gestión de Usuarios:** Ver la lista de clientes registrados y sus avances.

---

## 4. Estructura del Proyecto y Base de Datos (Modelos)

Se definen los siguientes modelos principales en Django:

### Modelo `PerfilUsuario` (Extensión del usuario de Django)
* `user`: OneToOneField(User)
* `telefono`: CharField
* `fecha_nacimiento`: DateField

### Modelo `AvanceFisico`
* `usuario`: ForeignKey(User)
* `fecha`: DateField (auto_now_add=True)
* `peso`: DecimalField
* `porcentaje_grasa`: DecimalField
* `notas`: TextField

### Modelo `Rutina`
* `nombre`: CharField
* `descripcion`: TextField
* `nivel`: CharField (Principiante, Intermedio, Avanzado)
* `creado_por`: ForeignKey(User, limit_choices_to={'is_staff': True})
* `fecha_creacion`: DateTimeField(auto_now_add=True)

---

## 5. Mapeo de URLs y Vistas (FBVs)

### Públicas:
* `/` -> `views.home` (Landing, carrusel, planes)
* `/accounts/register/` -> `views.register_view`
* `/accounts/login/` -> `views.login_view`
* `/accounts/logout/` -> `views.logout_view`

### Privadas (Usuario):
* `/dashboard/` -> `views.dashboard_view`
* `/avance/nuevo/` -> `views.crear_avance`

### Privadas (Admin):
* `/admin-gym/rutinas/` -> `views.lista_rutinas`
* `/admin-gym/rutinas/crear/` -> `views.crear_rutina`
* `/admin-gym/rutinas/editar/<int:pk>/` -> `views.editar_rutina`
* `/admin-gym/rutinas/eliminar/<int:pk>/` -> `views.eliminar_rutina`

---

## 6. Plan de Despliegue (Render)
Para desplegar exitosamente en Render con SQLite se requiere:
1.  **`requirements.txt`:** Incluir `Django>=6.0`, `gunicorn`, `whitenoise`.
2.  **`build.sh`:** Script para instalar dependencias, ejecutar `collectstatic` y aplicar `migrate`.
3.  **Configuración de Disco (Opcional pero recomendado):** Al usar SQLite, los datos se borrarán si el contenedor se reinicia, a menos que se monte un "Render Persistent Disk" y se apunte la base de datos a esa ruta (`/data/db.sqlite3`).

---

## 7. Plan de Documentación (`/doc`)
Se mantendrá una carpeta en la raíz llamada `doc/` con los siguientes archivos Markdown para registrar el progreso:

* `doc/01_inicializacion.md`: Configuración del entorno virtual, instalación de Django 6.0 y estructura inicial.
* `doc/02_modelos_y_base_datos.md`: Documentación del esquema de la base de datos y migraciones.
* `doc/03_vistas_y_rutas.md`: Explicación de las funciones de Django (FBVs) y el sistema de autenticación.
* `doc/04_interfaz_tailwind.md`: Detalles del diseño del carrusel, las cards y la integración de Tailwind CDN.
* `doc/05_despliegue_render.md`: Bitácora de pasos y errores solucionados durante el despliegue.
* `doc/futuras_implementaciones.md`: Roadmap (Pasarelas de pago, gráficos de avance, reserva de horas/clases).