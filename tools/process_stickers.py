#!/usr/bin/env python3
"""
Processa uma imagem com várias "figurinhas" em um fundo quadriculado,
remove o fundo e separa em arquivos PNG individuais com fundo transparente.

Uso:
  python tools/process_stickers.py ../images/source.png

Saída:
  ../images/sticker1.png, sticker2.png, ...

Dependências: rembg, pillow, numpy, opencv-python
Instalar: pip install -r tools/requirements.txt
"""
import sys
from pathlib import Path
from io import BytesIO
from rembg import remove
from PIL import Image
import numpy as np
import cv2


def remove_background_pil(img: Image.Image) -> Image.Image:
    """Remove fundo usando rembg (U2Net) e retorna PIL RGBA image."""
    buf = BytesIO()
    img.save(buf, format='PNG')
    in_bytes = buf.getvalue()
    out_bytes = remove(in_bytes)
    out_img = Image.open(BytesIO(out_bytes)).convert('RGBA')
    return out_img


def find_components(img: Image.Image, min_area=500):
    """Encontra componentes conectados na máscara alpha e retorna bounding boxes."""
    a = np.array(img.split()[-1])  # alpha channel
    # binarize
    _, th = cv2.threshold(a, 10, 255, cv2.THRESH_BINARY)
    # find contours
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area >= min_area:
            boxes.append((x, y, w, h))
    # sort left-to-right, top-to-bottom
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    return boxes


def crop_and_save(img: Image.Image, box, out_path: Path, pad=8):
    x, y, w, h = box
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(img.width, x + w + pad)
    y1 = min(img.height, y + h + pad)
    crop = img.crop((x0, y0, x1, y1))
    # optionally resize if too large
    max_dim = 1024
    if max(crop.width, crop.height) > max_dim:
        scale = max_dim / max(crop.width, crop.height)
        new_size = (int(crop.width * scale), int(crop.height * scale))
        crop = crop.resize(new_size, Image.LANCZOS)
    crop.save(out_path, format='PNG')


def main():
    if len(sys.argv) < 2:
        print("Uso: python tools/process_stickers.py PATH/TO/source.png")
        sys.exit(1)

    src = Path(sys.argv[1])
    if not src.exists():
        print("Arquivo não encontrado:", src)
        sys.exit(1)

    out_dir = src.parent
    print("Carregando imagem:", src)
    img = Image.open(src).convert('RGBA')

    print("Removendo fundo (rembg)...")
    try:
        img_nobg = remove_background_pil(img)
    except Exception as e:
        print("Erro ao rodar rembg:", e)
        sys.exit(1)

    print("Detectando componentes...")
    boxes = find_components(img_nobg)
    if not boxes:
        print("Nenhum componente detectado. Salvando imagem processada como 'sticker1.png'")
        out = out_dir / 'sticker1.png'
        img_nobg.save(out)
        print("Salvo:", out)
        return

    print(f"{len(boxes)} componentes detectados. Salvando...")
    for i, box in enumerate(boxes, start=1):
        out = out_dir / f'sticker{i}.png'
        crop_and_save(img_nobg, box, out)
        print("Salvo:", out)


if __name__ == '__main__':
    main()
