from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap, subprocess, tempfile, os

W, H = 1080, 1920

def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def _wrap(text: str, width: int):
    return textwrap.wrap(text, width=width, break_long_words=False)

def make_card(text: str, subtitle: str, output: Path, accent=(255, 255, 255)):
    img = Image.new("RGB", (W, H), (10, 12, 18))
    d = ImageDraw.Draw(img)
    # fondo geométrico original, sin clips protegidos
    for y in range(0, H, 80):
        shade = 18 + (y // 80) % 3 * 5
        d.rectangle((0, y, W, y + 80), fill=(shade, shade + 2, shade + 8))
    d.rounded_rectangle((70, 120, W-70, H-120), radius=45, outline=accent, width=8)
    d.text((90, 165), "PORTES AI SPORTS", font=_font(44, True), fill=accent)
    lines = _wrap(text, 22)
    y = 430
    for line in lines[:7]:
        bbox = d.textbbox((0,0), line, font=_font(78, True))
        x = (W - (bbox[2]-bbox[0]))/2
        d.text((x, y), line, font=_font(78, True), fill=(245,245,245))
        y += 105
    sub_lines = _wrap(subtitle, 36)
    y = 1370
    for line in sub_lines[:4]:
        bbox = d.textbbox((0,0), line, font=_font(42))
        x = (W - (bbox[2]-bbox[0]))/2
        d.text((x, y), line, font=_font(42), fill=(205,210,220))
        y += 58
    d.text((W/2-220, H-220), "Síguenos para más MLB y NBA", font=_font(38, True), fill=accent)
    img.save(output, quality=94)

def render_video(script: dict, output_path: str | Path, seconds: int = 18) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cards = [
            (script["hook"], "La historia deportiva que debes conocer"),
            (script["body"][:180], "Datos y contexto en pocos segundos"),
            (script["close"], "@PortesAISports")
        ]
        images = []
        for i, (main, sub) in enumerate(cards):
            p = td / f"card_{i}.png"
            make_card(main, sub, p)
            images.append(p)
        concat = td / "concat.txt"
        duration = seconds / len(images)
        concat.write_text("".join(
            f"file '{p.as_posix()}'\nduration {duration}\n" for p in images
        ) + f"file '{images[-1].as_posix()}'\n", encoding="utf-8")
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-vf", "scale=1080:1920,format=yuv420p",
            "-r", "30", "-c:v", "libx264", "-preset", "veryfast",
            "-movflags", "+faststart", str(output_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path
