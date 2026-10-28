"""Scrape the public contribution calendar (no token needed) into data/contributions.json."""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "maxguillemin-dev"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.select("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        m = re.match(r"(\d+)", tips.get(td.get("id"), ""))
        days.append({
            "date": td["data-date"],
            "level": int(td.get("data-level", 0)),
            "count": int(m.group(1)) if m else 0,
        })
    return sorted(days, key=lambda d: d["date"])


def stats(days: list[dict]) -> dict:
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    today = date.today().isoformat()
    past = [d for d in days if d["date"] <= today]
    current = 0
    for d in reversed(past):
        if d["count"]:
            current += 1
        elif d["date"] != today:  # today may still be empty
            break
    best = max(days, key=lambda d: d["count"], default={"date": None, "count": 0})
    months: dict[str, int] = {}
    for d in days:
        key = d["date"][:7]
        months[key] = months.get(key, 0) + d["count"]
    return {
        "total": sum(d["count"] for d in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "months": months,
    }


def main() -> None:
    r = requests.get(f"https://github.com/users/{USER}/contributions", timeout=30,
                     headers={"User-Agent": "profile-readme-bot"})
    r.raise_for_status()
    days = parse(r.text)
    if not days:
        sys.exit("no contribution cells found - markup changed?")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"user": USER, "updated": datetime.utcnow().isoformat() + "Z",
                               "days": days, **stats(days)}, indent=1))
    print(f"{len(days)} days, {sum(d['count'] for d in days)} contributions")


if __name__ == "__main__":
    main()
