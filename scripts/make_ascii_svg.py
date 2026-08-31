#!/usr/bin/env python3
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = Path(__file__).resolve().parents[1]
RAMP = ' .`:-=+*cs#%@'

def fallback():
    return [''.join(' @'[(x+y*3)%2] if ((x-50)/38)**2 + ((y-26)/24)**2 < 1 else ' ' for x in range(100)) for y in range(53)]

def main():
    source = ROOT / 'source-prepped.png'
    rows = []
    if source.exists():
        image = Image.open(source).convert('L').resize((100, 53))
        for y in range(53): rows.append(''.join(RAMP[min(len(RAMP)-1, p * len(RAMP)//256)] for p in [image.getpixel((x,y)) for x in range(100)]))
    else: rows = fallback()
    text = []
    for y, row in enumerate(rows):
        chars = ''.join(f'<tspan x="18" dy="0">{row.replace("&", "&amp;").replace("<", "&lt;")}</tspan>')
        text.append(f'<text y="{24+y*8}" style="animation-delay:{y*0.045:.2f}s">{chars}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="490" viewBox="0 0 370 490"><rect width="370" height="490" rx="14" fill="#0d1117" stroke="#30363d"/><style>text{{font:7px ui-monospace,SFMono-Regular,Menlo,monospace;fill:#c9d1d9;opacity:0;animation:print .45s ease forwards}}@keyframes print{{to{{opacity:1}}}}</style><text x="18" y="18" fill="#69f0a0" font-family="ui-monospace,monospace" font-size="10">portrait.render()</text>{''.join(text)}</svg>'''
    (ROOT / 'avi-ascii.svg').write_text(svg)

if __name__ == '__main__': main()
