# PORTES AI SPORTS 1.0

Asistente local para crear contenido vertical de MLB y NBA.

## Funciones incluidas

- Consulta de programación/resultados MLB.
- Consulta de scoreboard NBA vigente, con entrada manual de respaldo.
- Puntuación de potencial de interés.
- Generación de guion local; mejora automática si añades una clave de OpenAI.
- Creación de video MP4 vertical 1080 × 1920.
- Títulos, descripción y hashtags.
- Módulo preparado para TikTok Content Posting API.
- Aprobación manual antes de publicar.

## Instalación rápida en Windows

1. Instala Python 3.11 o superior y FFmpeg.
2. Descomprime el proyecto.
3. Ejecuta `INSTALAR_WINDOWS.bat`.
4. Ejecuta `INICIAR_WINDOWS.bat`.
5. El navegador abrirá el panel.

## Activar IA

Copia `.env.example` como `.env` y coloca:

```env
OPENAI_API_KEY=tu_clave
```

Sin clave, el sistema sigue funcionando con el generador local.

## Vincular TikTok después

La integración exige una aplicación de TikTok Developers, OAuth, el producto Content Posting API y las aprobaciones aplicables. No compartas tu contraseña. Se conectará mediante autorización oficial y token.

## Uso responsable de contenido deportivo

El proyecto crea gráficos originales. No descarga ni reutiliza transmisiones, highlights, logotipos o material protegido. Para añadir imágenes o clips debes tener derechos o una licencia válida.

## Meta de vistas

El sistema optimiza estructura y consistencia, pero ninguna herramienta puede garantizar que TikTok entregue una cifra específica de vistas.
