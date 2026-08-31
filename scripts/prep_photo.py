#!/usr/bin/env python3
"""Prepare a face photo for ASCII conversion. Optional local-only pipeline."""
import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

def main():
    if len(sys.argv) != 2: raise SystemExit('Usage: python scripts/prep_photo.py path/to/photo.jpg')
    source = Path(sys.argv[1])
    image = Image.open(source).convert('L')
    image = ImageOps.fit(image, (100, 53), method=Image.Resampling.LANCZOS)
    image = ImageOps.autocontrast(image, cutoff=2)
    image = ImageEnhance.Contrast(image).enhance(1.35)
    image.save(Path(__file__).resolve().parents[1] / 'source-prepped.png')

if __name__ == '__main__': main()
