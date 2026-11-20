#!/usr/bin/env python3
"""Gera um story 9:16 (1080x1920) no estilo da @jonas_maciel_worship.

Uso: python3 -I tools/make_story.py SAIDA.jpg "Texto principal" ["Referência"] ["RÓTULO"]
- Texto principal: use \\n para forçar quebra de linha (opcional).
- Referência: ex. "Salmos 46:10" (omita ou deixe vazio para mensagens sem versículo).
- RÓTULO: pequeno texto acima da cruz, ex. "VERSÍCULO DO DIA" (opcional).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
# Áreas seguras de story: evita ~250px no topo e ~340px na base.
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GOLD = (255, 226, 170, 255)
HANDLE = "@jonas_maciel_worship"


def gradient():
    img = Image.new("RGB", (W, H))
    px = img.load()
    top, bot = (14, 22, 48), (120, 72, 38)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return img


def wrap(d, text, font, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            test = (cur + " " + word).strip()
            if d.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def main():
    out = sys.argv[1]
    text = sys.argv[2].replace("\\n", "\n")
    ref = sys.argv[3] if len(sys.argv) > 3 else ""
    label = sys.argv[4] if len(sys.argv) > 4 else ""

    img = gradient()
    d = ImageDraw.Draw(img, "RGBA")

    # brilho suave atrás da cruz
    cy = 640
    for r in range(620, 0, -8):
        d.ellipse((W / 2 - r, cy - r, W / 2 + r, cy + r), fill=(255, 214, 140, int(26 * (1 - r / 620))))

    def center(t, y, font, fill):
        w = d.textlength(t, font=font)
        d.text(((W - w) / 2, y), t, font=font, fill=fill)

    # rótulo
    if label:
        center(label, 330, ImageFont.truetype(SANS_B, 32), (255, 226, 170, 230))

    # cruz branca com sombra
    def cross(fill, off=0):
        d.rectangle((W / 2 - 11 + off, 460 + off, W / 2 + 11 + off, 760 + off), fill=fill)
        d.rectangle((W / 2 - 90 + off, 545 + off, W / 2 + 90 + off, 567 + off), fill=fill)
    cross((0, 0, 0, 110), 7)
    cross((255, 255, 255, 255))

    # texto principal: reduz a fonte até caber em no máximo 5 linhas
    manual = text.count("\n") + 1  # respeita as quebras manuais: encolhe a fonte até caberem
    size = 84
    while True:
        f = ImageFont.truetype(SERIF_B, size)
        lines = wrap(d, text, f, W - 160)
        if (len(lines) <= max(manual, 1) if manual > 1 else len(lines) <= 5) or size <= 52:
            break
        size -= 4
    lh = int(size * 1.35)
    y = 900
    for ln in lines:
        center(ln, y, f, (255, 255, 255, 255))
        y += lh

    if ref:
        d.line((W / 2 - 90, y + 30, W / 2 + 90, y + 30), fill=GOLD, width=3)
        center(ref, y + 62, ImageFont.truetype(SERIF, 48), GOLD)

    center(HANDLE, 1500, ImageFont.truetype(SANS, 32), (255, 255, 255, 200))
    img.save(out, "JPEG", quality=92)


if __name__ == "__main__":
    main()
