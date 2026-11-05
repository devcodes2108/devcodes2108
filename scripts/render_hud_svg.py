"""
scripts/render_hud_svg.py
Generates the Cyber-Engineering Telemetry HUD SVG (cyber-hud.svg).
Displays profile identity, specialization, system status, language DNA telemetry,
and high-level metrics with light/dark theme adaptation and reduced-motion support.
"""

import os
import json
import xml.sax.saxutils as saxutils
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(BASE_DIR, "cyber-hud.svg")


def escape(text):
    return saxutils.escape(str(text)) if text is not None else ""


def build_hud_svg():
    # Load profile data
    profile_path = os.path.join(DATA_DIR, "profile.json")
    repos_path = os.path.join(DATA_DIR, "repos.json")
    contrib_path = os.path.join(DATA_DIR, "contributions.json")

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)
    with open(repos_path, "r", encoding="utf-8") as f:
        repos_data = json.load(f)
    with open(contrib_path, "r", encoding="utf-8") as f:
        contrib = json.load(f)

    name = profile.get("name", "Devanshu Singh")
    login = profile.get("login", "devcodes2108")
    public_repos = profile.get("public_repos", len(repos_data.get("repos", [])))
    total_contribs = contrib.get("total_contributions", 92)
    longest_streak = contrib.get("longest_streak", 4)
    active_days = contrib.get("active_days_count", 24)

    # Calculate language breakdown
    lang_totals = repos_data.get("language_totals", {})
    total_bytes = sum(lang_totals.values()) or 1

    # Filter and group languages
    sorted_langs = sorted(lang_totals.items(), key=lambda x: x[1], reverse=True)
    top_langs = []
    other_bytes = 0

    lang_colors = {
        "TypeScript": "#3178c6",
        "Python": "#3572A5",
        "Jupyter Notebook": "#DA5B0B",
        "HTML": "#e34c26",
        "CSS": "#563d7c",
        "JavaScript": "#f1e05a",
        "Dockerfile": "#384d54",
        "PowerShell": "#012456"
    }

    # Group Jupyter Notebook into Python/Notebooks or display directly
    for l_name, b_count in sorted_langs[:5]:
        pct = (b_count / total_bytes) * 100
        top_langs.append({
            "name": l_name,
            "bytes": b_count,
            "pct": pct,
            "color": lang_colors.get(l_name, "#58a6ff")
        })

    # Total code size in KB
    total_code_kb = total_bytes // 1024

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 280" width="860" height="280">
  <defs>
    <style>
      /* Base Theme (Dark by default on GitHub dark mode) */
      :root {{
        --bg-panel: #0d1117;
        --border-panel: #30363d;
        --border-focus: #00f2fe;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --accent-cyan: #00f2fe;
        --accent-teal: #4facfe;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --badge-bg: rgba(0, 242, 254, 0.08);
        --card-inner: #161b22;
        --grid-line: rgba(48, 54, 61, 0.4);
      }}

      /* Light Theme override */
      @media (prefers-color-scheme: light) {{
        :root {{
          --bg-panel: #ffffff;
          --border-panel: #d0d7de;
          --border-focus: #0969da;
          --text-primary: #1f2328;
          --text-secondary: #656d76;
          --text-muted: #8c959f;
          --accent-cyan: #0969da;
          --accent-teal: #0550ae;
          --accent-green: #1a7f37;
          --accent-amber: #9a6700;
          --badge-bg: rgba(9, 105, 218, 0.08);
          --card-inner: #f6f8fa;
          --grid-line: rgba(208, 215, 222, 0.5);
        }}
      }}

      .hud-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      }}
      .mono-text {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      }}

      /* Scanline and glowing animations */
      @keyframes pulseStatus {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.92); }}
      }}

      @keyframes radarSweep {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
      }}

      @keyframes scanlineAnim {{
        0% {{ transform: translateY(0); opacity: 0.15; }}
        50% {{ opacity: 0.35; }}
        100% {{ transform: translateY(270px); opacity: 0.15; }}
      }}

      @keyframes barGrow {{
        0% {{ width: 0; }}
      }}

      .status-pulse {{
        transform-origin: 792px 35px;
        animation: pulseStatus 2.4s ease-in-out infinite;
      }}

      .radar-arm {{
        transform-origin: 52px 52px;
        animation: radarSweep 6s linear infinite;
      }}

      .scan-line {{
        animation: scanlineAnim 4s ease-in-out infinite alternate;
      }}

      /* Reduced motion support */
      @media (prefers-reduced-motion: reduce) {{
        .status-pulse, .radar-arm, .scan-line {{
          animation: none !important;
        }}
      }}
    </style>

    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="100%" stop-color="#4facfe" />
    </linearGradient>

    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.05" />
    </linearGradient>

    <linearGradient id="radarGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#00f2fe" stop-opacity="0" />
    </linearGradient>

    <!-- Clip path for panel frame -->
    <clipPath id="panelClip">
      <rect x="0" y="0" width="860" height="280" rx="14" ry="14" />
    </clipPath>
  </defs>

  <!-- Outer Terminal HUD Frame -->
  <g clip-path="url(#panelClip)">
    <rect x="0" y="0" width="860" height="280" fill="var(--bg-panel)" rx="14" stroke="var(--border-panel)" stroke-width="1.5" />

    <!-- Subtle Background Circuit / Grid Pattern -->
    <path d="M0 45 L860 45 M0 175 L860 175 M540 45 L540 175 M280 175 L280 280 M570 175 L570 280" stroke="var(--grid-line)" stroke-width="1" stroke-dasharray="3 3" />

    <!-- Moving Scanner Line across the HUD -->
    <line x1="10" y1="0" x2="850" y2="0" stroke="url(#cyanGrad)" stroke-width="1.5" opacity="0.25" class="scan-line" />

    <!-- ==================== HEADER BAR ==================== -->
    <!-- Top HUD Coordinates and Breadcrumb -->
    <text x="24" y="28" fill="var(--text-muted)" font-size="11" class="mono-text" letter-spacing="1.5">SEC-OPS // SYSTEM TELEMETRY HUD // v2.6</text>
    
    <!-- Online Heartbeat Status -->
    <g transform="translate(685, 18)">
      <rect x="0" y="0" width="150" height="24" rx="12" fill="var(--badge-bg)" stroke="var(--border-focus)" stroke-width="0.75" />
      <circle cx="15" cy="12" r="4.5" fill="var(--accent-green)" class="status-pulse" />
      <text x="28" y="15.5" fill="var(--text-primary)" font-size="10.5" font-weight="600" class="mono-text" letter-spacing="0.5">STATUS: ACTIVE</text>
    </g>

    <!-- ==================== LEFT: IDENTITY & SPECIALIZATION ==================== -->
    <!-- Stylized Cyber Shield / Radar Glyph -->
    <g transform="translate(24, 60)">
      <!-- Outer Hex/Radar boundary -->
      <circle cx="45" cy="45" r="42" fill="url(#shieldGrad)" stroke="var(--border-panel)" stroke-width="1.5" />
      <circle cx="45" cy="45" r="28" fill="none" stroke="var(--border-panel)" stroke-width="1" stroke-dasharray="2 4" />
      
      <!-- Rotating Radar Beam -->
      <g class="radar-arm" style="transform-origin: 45px 45px;">
        <line x1="45" y1="45" x2="45" y2="4" stroke="url(#radarGrad)" stroke-width="2" stroke-linecap="round" />
        <polygon points="45,45 35,8 45,4" fill="url(#radarGrad)" opacity="0.4" />
      </g>

      <!-- Center Security Shield Icon -->
      <path d="M45 28 L57 33 C57 44 45 54 45 57 C45 54 33 44 33 33 Z" fill="none" stroke="var(--accent-cyan)" stroke-width="2.2" stroke-linejoin="round" />
      <circle cx="45" cy="41" r="3" fill="var(--accent-cyan)" />
    </g>

    <!-- Identity & Bio Metadata -->
    <text x="130" y="80" fill="var(--text-primary)" font-size="22" font-weight="700" class="hud-text" letter-spacing="-0.3">{escape(name)}</text>
    <text x="310" y="80" fill="var(--accent-cyan)" font-size="13" class="mono-text">@{escape(login)}</text>
    
    <text x="130" y="103" fill="var(--accent-green)" font-size="12.5" font-weight="600" class="mono-text" letter-spacing="0.5">CYBER SECURITY SPECIALIST // CSE '26</text>
    <text x="130" y="123" fill="var(--text-secondary)" font-size="12" class="hud-text">Institute of Technical Education and Research (ITER) • Bhubaneswar, IN</text>
    
    <!-- Focus Badges -->
    <g transform="translate(130, 137)">
      <rect x="0" y="0" width="100" height="20" rx="4" fill="var(--badge-bg)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="8" y="13.5" fill="var(--text-primary)" font-size="10" font-weight="600" class="mono-text">🔐 Cryptography</text>

      <rect x="108" y="0" width="105" height="20" rx="4" fill="var(--badge-bg)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="116" y="13.5" fill="var(--text-primary)" font-size="10" font-weight="600" class="mono-text">⚡ Full-Stack TS</text>

      <rect x="221" y="0" width="95" height="20" rx="4" fill="var(--badge-bg)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="229" y="13.5" fill="var(--text-primary)" font-size="10" font-weight="600" class="mono-text">🐍 Python/OOP</text>

      <rect x="324" y="0" width="70" height="20" rx="4" fill="var(--badge-bg)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="332" y="13.5" fill="var(--text-primary)" font-size="10" font-weight="600" class="mono-text">🐳 Docker</text>
    </g>

    <!-- ==================== RIGHT: TELEMETRY METRIC PODS ==================== -->
    <!-- Metric 1: Total Contributions -->
    <g transform="translate(560, 62)">
      <rect x="0" y="0" width="135" height="48" rx="8" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="14" y="20" fill="var(--text-muted)" font-size="9.5" font-weight="600" class="mono-text">ANNUAL COMMITS</text>
      <text x="14" y="39" fill="var(--accent-cyan)" font-size="18" font-weight="700" class="mono-text">{total_contribs}</text>
      <path d="M105 18 L112 14 L119 22 L125 15" fill="none" stroke="var(--accent-cyan)" stroke-width="1.5" stroke-linecap="round" />
    </g>

    <!-- Metric 2: Repositories -->
    <g transform="translate(705, 62)">
      <rect x="0" y="0" width="130" height="48" rx="8" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="14" y="20" fill="var(--text-muted)" font-size="9.5" font-weight="600" class="mono-text">PUBLIC REPOS</text>
      <text x="14" y="39" fill="var(--text-primary)" font-size="18" font-weight="700" class="mono-text">{public_repos}</text>
      <circle cx="112" cy="24" r="5" fill="none" stroke="var(--accent-green)" stroke-width="1.5" />
    </g>

    <!-- Metric 3: Active Days -->
    <g transform="translate(560, 118)">
      <rect x="0" y="0" width="135" height="46" rx="8" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="14" y="18" fill="var(--text-muted)" font-size="9.5" font-weight="600" class="mono-text">ACTIVE SESSIONS</text>
      <text x="14" y="37" fill="var(--text-primary)" font-size="17" font-weight="700" class="mono-text">{active_days} days</text>
    </g>

    <!-- Metric 4: Max Streak -->
    <g transform="translate(705, 118)">
      <rect x="0" y="0" width="130" height="46" rx="8" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="1" />
      <text x="14" y="18" fill="var(--text-muted)" font-size="9.5" font-weight="600" class="mono-text">STREAK VELOCITY</text>
      <text x="14" y="37" fill="var(--accent-amber)" font-size="17" font-weight="700" class="mono-text">{longest_streak} d streak</text>
    </g>

    <!-- ==================== FOOTER: LANGUAGE DNA DISTRIBUTION ==================== -->
    <text x="24" y="202" fill="var(--text-secondary)" font-size="11" font-weight="600" class="mono-text" letter-spacing="1">LANGUAGE DNA // CODE DISTRIBUTION ({total_code_kb} KB)</text>
    
    <!-- Multi-segment Language Progress Bar -->
    <g transform="translate(24, 212)">
      <!-- Background container -->
      <rect x="0" y="0" width="812" height="10" rx="5" fill="var(--card-inner)" stroke="var(--border-panel)" stroke-width="0.75" />
      
      <!-- Segment clips -->
      <g clip-path="url(#barClip)">
"""

    # Add bar segments
    bar_width = 812
    current_x = 0
    bar_rects = []
    legend_items = []

    for idx, lang in enumerate(top_langs):
        seg_w = (lang["pct"] / 100.0) * bar_width
        if seg_w < 2:
            seg_w = 2
        bar_rects.append(
            f'        <rect x="{current_x:.1f}" y="0" width="{seg_w:.1f}" height="10" fill="{lang["color"]}" />'
        )
        current_x += seg_w

    svg += "\n".join(bar_rects)
    svg += f"""
      </g>
    </g>

    <clipPath id="barClip">
      <rect x="0" y="0" width="812" height="10" rx="5" />
    </clipPath>

    <!-- Language Legend Below Bar -->
    <g transform="translate(24, 246)">
"""

    leg_x = 0
    for idx, lang in enumerate(top_langs):
        svg += f"""      <circle cx="{leg_x + 5}" cy="-4" r="4.5" fill="{lang['color']}" />
      <text x="{leg_x + 15}" y="0" fill="var(--text-primary)" font-size="11" font-weight="600" class="hud-text">{lang['name']}</text>
      <text x="{leg_x + 15 + len(lang['name']) * 7 + 6}" y="0" fill="var(--text-muted)" font-size="10.5" class="mono-text">{lang['pct']:.1f}%</text>
"""
        leg_x += len(lang['name']) * 7 + 58

    svg += f"""      <!-- Last Synced Telemetry Tag -->
      <text x="812" y="0" text-anchor="end" fill="var(--text-muted)" font-size="10" class="mono-text">SYNCED: {timestamp}</text>
    </g>
  </g>
</svg>"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[+] Successfully generated {OUTPUT_PATH}")


if __name__ == "__main__":
    build_hud_svg()
