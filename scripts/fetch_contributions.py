#!/usr/bin/env python3
"""Fetch devcodes2108's public GitHub contribution calendar without a token."""
import json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "devcodes2108"
OUT = Path(__file__).resolve().parents[1] / "data/contributions.json"

def main():
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, headers={"User-Agent": "devcodes2108-profile-art/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        raw = cell.get("data-count") or cell.get("aria-label", "")
        match = re.search(r"\d[\d,]*", str(raw))
        count = int(match.group().replace(",", "")) if match else 0
        level = int(cell.get("data-level", "0"))
        days.append({"date": cell["data-date"], "count": count, "level": level})
    if not days:
        raise RuntimeError("No contribution cells found; GitHub markup may have changed.")
    days.sort(key=lambda item: item["date"])
    longest = current = 0
    streak = 0
    best_day = max(days, key=lambda item: item["count"])
    for item in days:
        if item["count"]:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 0
    for item in reversed(days):
        if item["count"]: current += 1
        else: break
    monthly = {}
    for item in days:
        key = item["date"][:7]
        monthly[key] = monthly.get(key, 0) + item["count"]
    payload = {"username": USERNAME, "updated_at": date.today().isoformat(), "days": days[-371:], "stats": {"total": sum(x["count"] for x in days[-371:]), "current_streak": current, "longest_streak": longest, "best_day": best_day, "monthly": monthly}}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {len(payload['days'])} days to {OUT}")

if __name__ == "__main__": main()


def _unused_reference():
    return timedelta(days=1)

_UNUSED = _unused_reference
