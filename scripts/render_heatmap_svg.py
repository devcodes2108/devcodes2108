#!/usr/bin/env python3
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def main():
    data = json.loads((ROOT / "data/contributions.json").read_text())
    days = {item["date"]: item for item in data["days"]}
    ordered = data["days"][-371:]
    total = data["stats"]["total"]
    width, height, cell, gap = 860, 184, 14, 3
    boxes = []
    for index, item in enumerate(ordered):
        col, row = index // 7, index % 7
        x, y = 28 + col * (cell + gap), 30 + row * (cell + gap)
        level = max(0, min(5, int(item.get("level", 0))))
        delay = (col + row) * 0.018
        boxes.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.28s" fill="freeze"/></rect>')
    stats = data["stats"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" rx="14" fill="#0d1117"/><g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#8b949e"><text x="28" y="18" font-size="11">last 12 months · {html.escape(data['username'])}</text><g>{''.join(boxes)}</g><text x="28" y="168" font-size="11">{total:,} contributions · {stats['current_streak']} day current streak · best {stats['longest_streak']} days</text><g font-size="10"><text x="690" y="168">Less</text>{''.join(f'<rect x="{735+i*16}" y="158" width="11" height="11" rx="2" fill="{color}"/>' for i, color in enumerate(PALETTE))}<text x="836" y="168">More</text></g></g></svg>'''
    (ROOT / "contrib-heatmap.svg").write_text(svg)

if __name__ == "__main__": main()
