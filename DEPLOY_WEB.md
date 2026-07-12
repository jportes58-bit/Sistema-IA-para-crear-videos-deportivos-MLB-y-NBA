# Publicar PORTES AI SPORTS en la web

La forma más sencilla es Streamlit Community Cloud.

1. Crea una cuenta de GitHub.
2. Crea un repositorio nuevo.
3. Sube todos los archivos de esta carpeta.
4. Entra a Streamlit Community Cloud.
5. Pulsa **Create app**.
6. Selecciona el repositorio y `app.py`.
7. Pulsa **Deploy**.

La aplicación abrirá en una dirección web y no tendrás que instalar Python.

## Para activar IA

En Streamlit, abre **App settings > Secrets** y agrega:

```toml
OPENAI_API_KEY="tu_clave"
OPENAI_MODEL="gpt-4.1-mini"
```

## Para TikTok

No compartas la contraseña de tu cuenta. La conexión se hará con OAuth y la aplicación oficial de TikTok Developers. El botón Publicar permanecerá bloqueado hasta completar esa configuración y los permisos exigidos por TikTok.