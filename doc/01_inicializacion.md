# Configuración Inicial

## Entorno Virtual
Se creó un entorno virtual con `python3 -m venv venv` y se activó.

## Dependencias
- Django 6.0.6
- gunicorn
- whitenoise

## Proyecto
Se ejecutó `django-admin startproject akelagym .` y se creó la app `core`.

## Configuración (`settings.py`)
- SQLite como base de datos
- Whitenoise para archivos estáticos
- Tailwind CSS vía CDN
- Español (`es-cl`) y zona horaria `America/Santiago`
- LOGIN_URL y LOGIN_REDIRECT_URL configurados
- Soporte para Render Persistent Disk
