"""
scripts/fetch_data.py
Fetches GitHub profile, repositories, languages, and contribution calendar
for devcodes2108 without requiring third-party dependencies or personal access tokens.
Writes output to data/profile.json, data/repos.json, data/contributions.json.
"""

import os
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

USERNAME = os.environ.get("GITHUB_USERNAME", "devcodes2108")
HEADERS = {
    "User-Agent": f"GitHub-Profile-Generator-{USERNAME}",
    "Accept": "application/vnd.github.v3+json"
}

# Optional auth token for GitHub Actions to avoid rate limits
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_profile():
    print(f"[*] Fetching profile for {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}"
    user = fetch_json(url)
    profile_path = os.path.join(DATA_DIR, "profile.json")
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(user, f, indent=2)
    print(f"[+] Saved profile to {profile_path}")
    return user


def fetch_repos():
    print(f"[*] Fetching repos for {USERNAME}...")
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"
    repos = fetch_json(url)

    language_totals = {}
    detailed_repos = []

    for r in repos:
        name = r["name"]
        lang_url = r["languages_url"]
        languages = {}
        try:
            languages = fetch_json(lang_url)
        except Exception as e:
            print(f"[-] Warning: Failed to fetch languages for {name}: {e}")

        for lang, byte_count in languages.items():
            language_totals[lang] = language_totals.get(lang, 0) + byte_count

        detailed_repos.append({
            "name": name,
            "full_name": r.get("full_name"),
            "html_url": r["html_url"],
            "description": r.get("description"),
            "primary_language": r.get("language"),
            "languages": languages,
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "watchers": r.get("watchers_count", 0),
            "open_issues": r.get("open_issues_count", 0),
            "topics": r.get("topics", []),
            "created_at": r.get("created_at"),
            "updated_at": r.get("updated_at"),
            "pushed_at": r.get("pushed_at"),
            "is_fork": r.get("fork", False),
            "size": r.get("size", 0),
            "default_branch": r.get("default_branch", "main")
        })

    repos_payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_repos": len(detailed_repos),
        "language_totals": language_totals,
        "repos": detailed_repos
    }

    repos_path = os.path.join(DATA_DIR, "repos.json")
    with open(repos_path, "w", encoding="utf-8") as f:
        json.dump(repos_payload, f, indent=2)
    print(f"[+] Saved {len(detailed_repos)} repos to {repos_path}")
    return repos_payload


def fetch_contributions():
    print(f"[*] Scraping public contributions calendar for {USERNAME}...")
    url = f"https://github.com/users/{USERNAME}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    # Match each <td ... class="...ContributionCalendar-day...">
    td_matches = re.findall(r'<td[^>]*class="[^"]*ContributionCalendar-day[^"]*"[^>]*>', html)

    # Tooltip pattern matches <tool-tip for="id">text</tool-tip>
    tooltips = {}
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', html, re.DOTALL):
        tip_id = m.group(1)
        tip_text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        tooltips[tip_id] = tip_text

    parsed_days = []
    total_contributions = 0

    for td in td_matches:
        date_match = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', td)
        level_match = re.search(r'data-level="(\d+)"', td)
        id_match = re.search(r'id="([^"]+)"', td)

        if not date_match:
            continue

        date = date_match.group(1)
        level = int(level_match.group(1)) if level_match else 0
        d_id = id_match.group(1) if id_match else ""
        tip = tooltips.get(d_id, "")

        count = 0
        c_search = re.search(r'^([0-9,]+)\s+contribution', tip)
        if c_search:
            count = int(c_search.group(1).replace(",", ""))
        elif level > 0 and count == 0:
            count = level  # fallback estimate if tooltip missing

        total_contributions += count
        parsed_days.append({
            "date": date,
            "level": level,
            "count": count,
            "tooltip": tip
        })

    parsed_days.sort(key=lambda x: x["date"])

    # Compute streaks
    longest_streak = 0
    current_streak = 0
    temp_streak = 0

    for d in parsed_days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Calculate current active streak backwards from the most recent day
    for d in reversed(parsed_days):
        if d["count"] > 0:
            current_streak += 1
        elif current_streak > 0:
            break

    # Monthly breakdown
    monthly_counts = {}
    for d in parsed_days:
        month_key = d["date"][:7]  # YYYY-MM
        monthly_counts[month_key] = monthly_counts.get(month_key, 0) + d["count"]

    contrib_payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "active_days_count": sum(1 for d in parsed_days if d["count"] > 0),
        "monthly_totals": monthly_counts,
        "days": parsed_days
    }

    contrib_path = os.path.join(DATA_DIR, "contributions.json")
    with open(contrib_path, "w", encoding="utf-8") as f:
        json.dump(contrib_payload, f, indent=2)
    print(f"[+] Saved {len(parsed_days)} calendar days to {contrib_path} (Total contributions: {total_contributions})")
    return contrib_payload


if __name__ == "__main__":
    fetch_profile()
    fetch_repos()
    fetch_contributions()
    print("[OK] All data fetched successfully!")
