"""
scripts/render_projects_svg.py
Renders the architectural Featured Projects Matrix SVG (project-matrix.svg)
highlighting Devanshu's top Cyber Security & Full-Stack engineering repositories.
Fully supports light/dark themes, reduced-motion, and vector iconography.
"""

import os
import json
import xml.sax.saxutils as saxutils

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(BASE_DIR, "project-matrix.svg")


def escape(text):
    return saxutils.escape(str(text)) if text is not None else ""


def build_projects_svg():
    repos_path = os.path.join(DATA_DIR, "repos.json")
    with open(repos_path, "r", encoding="utf-8") as f:
        repos_data = json.load(f)

    # Dictionary of curated highlighted projects with their specific engineering details
    FEATURED = [
        {
            "name": "LockItPDF",
            "tag": "CRYPTOGRAPHY // SEC-OPS",
            "desc": "Full-stack Dockerized PDF encryption engine with granular access control & password shielding.",
            "stack": ["Python", "Docker", "JS/CSS", "Security"],
            "status": "CONTAINERIZED",
            "icon_color": "#00f2fe",
            "icon_type": "shield",
            "url": "https://github.com/devcodes2108/LockItPDF"
        },
        {
            "name": "SecurePDF-BatchEncryptor",
            "tag": "SECURITY PIPELINE",
            "desc": "High-throughput batch cryptographic encryption pipeline for automated document safeguarding.",
            "stack": ["Python", "Jupyter", "Cryptography", "Batch"],
            "status": "PIPELINE",
            "icon_color": "#10b981",
            "icon_type": "lock",
            "url": "https://github.com/devcodes2108/SecurePDF-BatchEncryptor"
        },
        {
            "name": "devanshu-portfolio",
            "tag": "FULL-STACK PRODUCTION",
            "desc": "Type-safe modern developer showcase highlighting engineering projects, speaking, and articles.",
            "stack": ["TypeScript", "React", "TailwindCSS", "Responsive"],
            "status": "DEPLOYED",
            "icon_color": "#38bdf8",
            "icon_type": "globe",
            "url": "https://github.com/devcodes2108/devanshu-portfolio"
        },
        {
            "name": "quick-push",
            "tag": "DEVELOPER ACCELERATOR",
            "desc": "Streamlined developer automation engine for accelerated Git commits, staging, and sync workflows.",
            "stack": ["TypeScript", "Git Ops", "Automation", "CLI"],
            "status": "TOOLING",
            "icon_color": "#f59e0b",
            "icon_type": "terminal",
            "url": "https://github.com/devcodes2108/quick-push"
        }
    ]

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 260" width="860" height="260">
  <defs>
    <style>
      :root {
        --bg-panel: #0d1117;
        --border-panel: #30363d;
        --border-focus: #00f2fe;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --card-inner: #161b22;
        --badge-bg: rgba(0, 242, 254, 0.08);
        --accent-cyan: #00f2fe;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
      }

      @media (prefers-color-scheme: light) {
        :root {
          --bg-panel: #ffffff;
          --border-panel: #d0d7de;
          --border-focus: #0969da;
          --text-primary: #1f2328;
          --text-secondary: #656d76;
          --text-muted: #8c959f;
          --card-inner: #f6f8fa;
          --badge-bg: rgba(9, 105, 218, 0.08);
          --accent-cyan: #0969da;
          --accent-green: #1a7f37;
          --accent-amber: #9a6700;
        }
      }

      .hud-text {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      }
      .mono-text {
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      }

      @keyframes cardSlide {
        0% {
          opacity: 0;
          transform: translateY(12px);
        }
        100% {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .card-item {
        animation: cardSlide 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }

      @media (prefers-reduced-motion: reduce) {
        .card-item {
          animation: none !important;
          opacity: 1 !important;
        }
      }
    </style>
  </defs>

  <!-- 2x2 Grid Layout: Card size 420 x 120 -->
"""

    card_coords = [
        (0, 0, 0.05),
        (440, 0, 0.15),
        (0, 135, 0.25),
        (440, 135, 0.35)
    ]

    for idx, (x, y, delay) in enumerate(card_coords):
        p = FEATURED[idx]
        card_name = escape(p["name"])
        card_tag = escape(p["tag"])
        card_desc = escape(p["desc"])
        card_status = escape(p["status"])
        card_color = p["icon_color"]

        # Icon SVG Paths
        if p["icon_type"] == "shield":
            icon_markup = f"""<path d="M14 6 L22 10 C22 18 14 24 14 26 C14 24 6 18 6 10 Z" fill="none" stroke="{card_color}" stroke-width="1.8" stroke-linejoin="round" />
            <circle cx="14" cy="15" r="2.5" fill="{card_color}" />"""
        elif p["icon_type"] == "lock":
            icon_markup = f"""<rect x="7" y="11" width="14" height="12" rx="2" fill="none" stroke="{card_color}" stroke-width="1.8" />
            <path d="M10 11 V7 A4 4 0 0 1 18 7 V11" fill="none" stroke="{card_color}" stroke-width="1.8" />
            <circle cx="14" cy="17" r="1.5" fill="{card_color}" />"""
        elif p["icon_type"] == "globe":
            icon_markup = f"""<circle cx="14" cy="14" r="9" fill="none" stroke="{card_color}" stroke-width="1.8" />
            <ellipse cx="14" cy="14" rx="4.5" ry="9" fill="none" stroke="{card_color}" stroke-width="1.5" />
            <line x1="5" y1="14" x2="23" y2="14" stroke="{card_color}" stroke-width="1.5" />"""
        else: # terminal
            icon_markup = f"""<rect x="5" y="6" width="18" height="16" rx="3" fill="none" stroke="{card_color}" stroke-width="1.8" />
            <path d="M9 11 L12 14 L9 17" fill="none" stroke="{card_color}" stroke-width="1.5" stroke-linecap="round" />
            <line x1="14" y1="17" x2="18" y2="17" stroke="{card_color}" stroke-width="1.5" stroke-linecap="round" />"""

        svg += f"""  <g class="card-item" transform="translate({x}, {y})" style="animation-delay: {delay}s;">
    <!-- Outer Card Frame -->
    <rect x="0" y="0" width="420" height="125" rx="10" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="1.2" />

    <!-- Corner Indicator -->
    <line x1="0" y1="16" x2="0" y2="36" stroke="{card_color}" stroke-width="3" />

    <!-- Icon Pod -->
    <g transform="translate(14, 12)">
      <rect x="0" y="0" width="28" height="28" rx="6" fill="var(--bg-panel)" stroke="var(--border-panel)" stroke-width="1" />
      {icon_markup}
    </g>

    <!-- Project Name & Tag -->
    <text x="52" y="24" fill="var(--text-primary)" font-size="14.5" font-weight="700" class="hud-text">{card_name}</text>
    <text x="52" y="37" fill="{card_color}" font-size="9" font-weight="600" class="mono-text" letter-spacing="0.75">{card_tag}</text>

    <!-- Status Badge -->
    <g transform="translate(320, 14)">
      <rect x="0" y="0" width="86" height="18" rx="4" fill="var(--bg-panel)" stroke="var(--border-panel)" stroke-width="0.75" />
      <text x="43" y="12" text-anchor="middle" fill="var(--text-secondary)" font-size="8.5" font-weight="600" class="mono-text">{card_status}</text>
    </g>

    <!-- Description -->
    <text x="14" y="60" fill="var(--text-secondary)" font-size="11" class="hud-text">
      <tspan x="14" dy="0">{card_desc[:58]}</tspan>
      <tspan x="14" dy="16">{card_desc[58:120]}</tspan>
    </text>

    <!-- Tech Stack Badges -->
    <g transform="translate(14, 98)">
"""
        tag_x = 0
        for tag in p["stack"]:
            tag_text = escape(tag)
            pill_w = len(tag_text) * 6.5 + 14
            svg += f"""      <rect x="{tag_x}" y="0" width="{pill_w:.1f}" height="18" rx="4" fill="var(--badge-bg)" stroke="var(--border-panel)" stroke-width="0.75" />
      <text x="{tag_x + pill_w / 2:.1f}" y="12" text-anchor="middle" fill="var(--text-primary)" font-size="9" font-weight="500" class="mono-text">{tag_text}</text>
"""
            tag_x += pill_w + 6

        svg += """    </g>
  </g>
"""

    svg += "</svg>"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[+] Successfully generated {OUTPUT_PATH}")


if __name__ == "__main__":
    build_projects_svg()

