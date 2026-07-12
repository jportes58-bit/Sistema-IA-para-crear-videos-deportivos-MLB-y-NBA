from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio.v2 as imageio
import numpy as np
import textwrap

WIDTH, HEIGHT = 720, 1280

def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

def _frame(main: str, subtitle: str) -> np.ndarray:
    image = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    draw = ImageDraw.Draw(image)

    for y in range(0, HEIGHT, 70):
        shade = 18 + ((y // 70) % 3) * 5
        draw.rectangle((0, y, WIDTH, y + 70), fill=(shade, shade + 2, shade + 9))

    draw.rounded_rectangle(
        (45, 75, WIDTH - 45, HEIGHT - 75),
        radius=30,
        outline=(242, 201, 76),
        width=5,
    )
    draw.text(
        (65, 110),
        "PORTES AI SPORTS PRO",
        font=_font(29, True),
        fill=(242, 201, 76),
    )

    y = 285
    for line in textwrap.wrap(main, width=21, break_long_words=False)[:7]:
        font = _font(49, True)
        box = draw.textbbox((0, 0), line, font=font)
        x = (WIDTH - (box[2] - box[0])) / 2
        draw.text((x, y), line, font=font, fill=(248, 248, 248))
        y += 68

    y = 940
    for line in textwrap.wrap(subtitle, width=35, break_long_words=False)[:4]:
        font = _font(27)
        box = draw.textbbox((0, 0), line, font=font)
        x = (WIDTH - (box[2] - box[0])) / 2
        draw.text((x, y), line, font=font, fill=(210, 216, 228))
        y += 40

    draw.text(
        (145, HEIGHT - 145),
        "Síguenos para más deportes",
        font=_font(25, True),
        fill=(242, 201, 76),
    )
    return np.asarray(image)

def render_video(
    script: dict,
    output_path: str | Path,
    seconds: int = 15,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    sections = [
        (script["hook"], "La historia deportiva que debes conocer"),
        (script["body"][:190], "Datos y contexto en pocos segundos"),
        (script["close"], "@PortesAISports"),
    ]

    fps = 12
    frames_per_section = max(1, int(seconds * fps / len(sections)))
    frames: list[np.ndarray] = []

    for main, subtitle in sections:
        frame = _frame(main, subtitle)
        frames.extend([frame] * frames_per_section)

    imageio.mimsave(
        output,
        frames,
        fps=fps,
        codec="libx264",
        quality=7,
        macro_block_size=None,
    )
    return output
