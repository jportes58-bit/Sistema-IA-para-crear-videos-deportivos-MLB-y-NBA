from __future__ import annotations
import os

def is_configured() -> bool:
    return bool(os.getenv("TIKTOK_ACCESS_TOKEN", "").strip())

def publication_status() -> str:
    if is_configured():
        return "Token detectado; falta validar permisos y revisión de TikTok."
    return "TikTok todavía no está vinculado mediante OAuth."
