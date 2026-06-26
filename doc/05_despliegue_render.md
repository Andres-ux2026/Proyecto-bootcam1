# Despliegue en Render

## Requisitos
- `requirements.txt` con Django>=6.0, gunicorn, whitenoise
- `build.sh` script de build
- `runtime.txt` (opcional, Python 3.12+)

## Configuración
1. Crear servicio Web en Render
2. Conectar repositorio de Git
3. Configurar:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn akelagym.wsgi`
4. (Opcional) Montar Render Persistent Disk en `/data` y configurar `RENDER_PERSISTENT_DISK_PATH` para persistencia SQLite

## Archivos de Configuración
- `build.sh`: Instala dependencias, corre collectstatic y migrate
- `settings.py`: Whitenoise para estáticos, soporte para Persistent Disk
