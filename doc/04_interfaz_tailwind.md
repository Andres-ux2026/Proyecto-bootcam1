# Interfaz con Tailwind CSS

## Diseño General
- Tailwind CSS vía CDN
- Paleta de colores personalizada `akela` (azul corporativo)
- Diseño responsivo (mobile-first)
- Navegación adaptativa según rol (anónimo, usuario, admin)

## Componentes Principales
- **Carrusel**: Hero slider con imágenes reales (Pexels), transiciones CSS, dots indicadores, auto-play cada 5s
- **Cards de Planes**: 3 columnas (Mensual, Semestral, Anual), card destacada con borde azul y badge "MÁS POPULAR"
- **Grid de Entrenamientos**: 3 disciplinas con imagen hover zoom y overlay gradiente
- **Dashboard**: Layout de 2 columnas (perfil + rutinas | avance con Chart.js)
- **Formularios**: Inputs con bordes redondeados, focus ring azul, estilos consistentes
- **Tablas**: Diseño limpio con hover en filas y badges de nivel

## Chart.js
- Gráfico lineal de evolución de peso y %grasa
- Integrado vía CDN en el dashboard del usuario
- Dos datasets con colores diferenciados y relleno suave
