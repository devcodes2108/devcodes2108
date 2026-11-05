"""
scripts/render_matrix_svg.py
Renders the 53-week contribution telemetry calendar SVG (contrib-matrix.svg)
using real data from data/contributions.json with diagonal cascade animation,
adaptive light/dark theme, and zero third-party dependencies.
"""

import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(BASE_DIR, "contrib-matrix.svg")


def build_matrix_svg():
    contrib_path = os.path.join(DATA_DIR, "contributions.json")
    with open(contrib_path, "r", encoding="utf-8") as f:
        contrib_data = json.load(f)

    days = contrib_data.get("days", [])
    total_contribs = contrib_data.get("total_contributions", 92)
    longest_streak = contrib_data.get("longest_streak", 4)
    current_streak = contrib_data.get("current_streak", 0)

    # Calculate grid layout
    # 53 columns x 7 rows
    # Cell size 10x10, gap 3.5
    cell_size = 10.5
    gap = 3.5
    start_x = 42
    start_y = 48

    # Month label tracking
    # Determine the date of the first day to align day of week
    month_positions = []
    last_month = None

    # Organize days into 7xN columns
    # In GitHub contributions, day 0 in calendar is Sunday (row 0)
    grid_cells = []
    col = 0
    row = 0

    # GitHub provides days chronologically starting on a Sunday
    if days:
        first_date_str = days[0]["date"]
        # Find weekday of first day (0=Monday, 6=Sunday in Python datetime)
        first_dt = datetime.strptime(first_date_str, "%Y-%m-%d")
        # In GitHub calendar, Sunday is row 0, Saturday is row 6
        gh_weekday = (first_dt.weekday() + 1) % 7
        row = gh_weekday

    for idx, day_info in enumerate(days):
        date_str = day_info["date"]
        level = day_info["level"]
        count = day_info["count"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")

        # Track month labels
        month_abbr = dt.strftime("%b")
        if month_abbr != last_month and row == 0 and col < 52:
            month_positions.append((month_abbr, start_x + col * (cell_size + gap)))
            last_month = month_abbr

        cx = start_x + col * (cell_size + gap)
        cy = start_y + row * (cell_size + gap)

        # Staggered animation delay based on diagonal wave
        delay = (col * 0.012 + row * 0.025)

        grid_cells.append({
            "x": cx,
            "y": cy,
            "level": level,
            "count": count,
            "date": date_str,
            "delay": delay
        })

        row += 1
        if row > 6:
            row = 0
            col += 1

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 185" width="860" height="185">
  <defs>
    <style>
      :root {{
        --bg-panel: #0d1117;
        --border-panel: #30363d;
        --border-focus: #00f2fe;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --card-inner: #161b22;
        --accent-cyan: #00f2fe;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;

        /* Day level dark colors */
        --lvl-0: #161b22;
        --lvl-1: #0e4429;
        --lvl-2: #006d32;
        --lvl-3: #26a641;
        --lvl-4: #00f2fe; /* Cyber highlight for peak contributions */
      }}

      @media (prefers-color-scheme: light) {{
        :root {{
          --bg-panel: #ffffff;
          --border-panel: #d0d7de;
          --border-focus: #0969da;
          --text-primary: #1f2328;
          --text-secondary: #656d76;
          --text-muted: #8c959f;
          --card-inner: #f6f8fa;
          --accent-cyan: #0969da;
          --accent-green: #1a7f37;
          --accent-amber: #9a6700;

          --lvl-0: #ebedf0;
          --lvl-1: #9be9a8;
          --lvl-2: #40c463;
          --lvl-3: #30a14e;
          --lvl-4: #0969da;
        }}
      }}

      .hud-text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      }}
      .mono-text {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      }}

      /* Diagonal wave reveal animation */
      @keyframes cellCascade {{
        0% {{
          opacity: 0;
          transform: scale(0.3);
        }}
        70% {{
          transform: scale(1.15);
        }}
        100% {{
          opacity: 1;
          transform: scale(1);
        }}
      }}

      .cell {{
        transform-box: fill-box;
        transform-origin: center;
        animation: cellCascade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }}

      @media (prefers-reduced-motion: reduce) {{
        .cell {{
          animation: none !important;
          opacity: 1 !important;
        }}
      }}
    </style>

    <clipPath id="matrixClip">
      <rect x="0" y="0" width="860" height="185" rx="14" ry="14" />
    </clipPath>
  </defs>

  <g clip-path="url(#matrixClip)">
    <!-- Container background -->
    <rect x="0" y="0" width="860" height="185" fill="var(--bg-panel)" rx="14" stroke="var(--border-panel)" stroke-width="1.5" />

    <!-- Header bar inside matrix -->
    <text x="24" y="26" fill="var(--text-muted)" font-size="11" font-weight="600" class="mono-text" letter-spacing="1">ACTIVITY TELEMETRY // 53-WEEK COMMIT CADENCE</text>
    <text x="836" y="26" text-anchor="end" fill="var(--accent-cyan)" font-size="11" font-weight="600" class="mono-text">{total_contribs} COMMITS IN PAST YEAR</text>

    <!-- Month Labels -->
"""

    for m_abbr, m_x in month_positions:
        svg += f'    <text x="{m_x:.1f}" y="42" fill="var(--text-muted)" font-size="9" class="mono-text">{m_abbr}</text>\n'

    svg += """
    <!-- Day Labels (Mon, Wed, Fri) -->
    <text x="20" y="66" fill="var(--text-muted)" font-size="8.5" class="mono-text">Mon</text>
    <text x="20" y="94" fill="var(--text-muted)" font-size="8.5" class="mono-text">Wed</text>
    <text x="20" y="122" fill="var(--text-muted)" font-size="8.5" class="mono-text">Fri</text>

    <!-- Calendar Grid Cells -->
    <g id="heatmap-cells">
"""

    for c in grid_cells:
        lvl = c["level"]
        svg += f'      <rect class="cell" x="{c["x"]:.1f}" y="{c["y"]:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="var(--lvl-{lvl})" style="animation-delay: {c["delay"]:.3f}s;" />\n'

    svg += f"""    </g>

    <!-- Footer Bar: Summary & Legend -->
    <line x1="20" y1="152" x2="840" y2="152" stroke="var(--border-panel)" stroke-width="0.75" />

    <!-- Left Stats -->
    <g transform="translate(24, 170)">
      <circle cx="4" cy="-4" r="3" fill="var(--accent-green)" />
      <text x="14" y="0" fill="var(--text-primary)" font-size="10.5" font-weight="600" class="hud-text">Active Days: {contrib_data.get('active_days_count', 24)}</text>
      <text x="120" y="0" fill="var(--text-muted)" font-size="10.5" class="mono-text">|</text>
      <text x="135" y="0" fill="var(--text-secondary)" font-size="10.5" class="hud-text">Longest Streak: <tspan fill="var(--accent-amber)" font-weight="600" class="mono-text">{longest_streak} days</tspan></text>
      <text x="275" y="0" fill="var(--text-muted)" font-size="10.5" class="mono-text">|</text>
      <text x="290" y="0" fill="var(--text-secondary)" font-size="10.5" class="hud-text">Velocity: <tspan fill="var(--accent-cyan)" font-weight="600" class="mono-text">{(total_contribs / 52):.1f} commits/wk</tspan></text>
    </g>

    <!-- Right Legend -->
    <g transform="translate(715, 170)">
      <text x="0" y="0" fill="var(--text-muted)" font-size="10" class="mono-text">Less</text>
      <rect x="32" y="-9" width="10" height="10" rx="2" fill="var(--lvl-0)" />
      <rect x="46" y="-9" width="10" height="10" rx="2" fill="var(--lvl-1)" />
      <rect x="60" y="-9" width="10" height="10" rx="2" fill="var(--lvl-2)" />
      <rect x="74" y="-9" width="10" height="10" rx="2" fill="var(--lvl-3)" />
      <rect x="88" y="-9" width="10" height="10" rx="2" fill="var(--lvl-4)" />
      <text x="105" y="0" fill="var(--text-muted)" font-size="10" class="mono-text">More</text>
    </g>
  </g>
</svg>"""

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[+] Successfully generated {OUTPUT_PATH}")


if __name__ == "__main__":
    build_matrix_svg()

