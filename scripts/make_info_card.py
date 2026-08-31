#!/usr/bin/env python3
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANIMATION = '' if os.getenv('STATIC') else '<style>@keyframes reveal{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}</style>'
ROWS = [('now', 'Frontend Engineer · Full-Stack'), ('prev', 'Open source contributor'), ('stack', 'React · Next.js · TypeScript · Node'), ('focus', 'Interfaces that feel inevitable'), ('links', 'github.com/devcodes2108')]
lines = []
for i, (key, value) in enumerate(ROWS):
    y = 74 + i * 42
    style = f'opacity:0;animation:reveal .45s ease {i*0.12:.2f}s forwards' if ANIMATION else ''
    lines.append(f'<g style="{style}"><text x="28" y="{y}" fill="#69f0a0" font-size="12">{key}</text><text x="108" y="{y}" fill="#c9d1d9" font-size="12">{value}</text></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="250" viewBox="0 0 490 250"><rect width="490" height="250" rx="14" fill="#0d1117" stroke="#30363d"/><circle cx="24" cy="22" r="5" fill="#ff7b72"/><circle cx="42" cy="22" r="5" fill="#d29922"/><circle cx="60" cy="22" r="5" fill="#3fb950"/><text x="82" y="27" fill="#8b949e" font-family="ui-monospace,monospace" font-size="12">devcodes2108@github — neofetch</text><text x="28" y="52" fill="#c9d1d9" font-family="ui-monospace,monospace" font-size="15">DevCodes / profile</text><g font-family="ui-monospace,monospace">{''.join(lines)}</g>{ANIMATION}</svg>'''
(ROOT / 'info-card.svg').write_text(svg)
