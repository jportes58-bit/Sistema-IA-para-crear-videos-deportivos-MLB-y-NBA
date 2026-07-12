from __future__ import annotations
import os, requests

API = "https://open.tiktokapis.com/v2"

def configured() -> bool:
    return bool(os.getenv("TIKTOK_ACCESS_TOKEN", "").strip())

def creator_info() -> dict:
    token = os.environ["TIKTOK_ACCESS_TOKEN"]
    r = requests.post(
        f"{API}/post/publish/creator_info/query/",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        timeout=30
    )
    r.raise_for_status()
    return r.json()

def init_direct_post(video_url: str, title: str, privacy_level: str = "SELF_ONLY") -> dict:
    """Inicializa Direct Post usando PULL_FROM_URL.
    La URL debe pertenecer a un dominio o prefijo verificado en TikTok Developers.
    """
    token = os.environ["TIKTOK_ACCESS_TOKEN"]
    payload = {
        "post_info": {
            "title": title[:2200],
            "privacy_level": privacy_level,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url
        }
    }
    r = requests.post(
        f"{API}/post/publish/video/init/",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"},
        json=payload, timeout=30
    )
    r.raise_for_status()
    return r.json()
