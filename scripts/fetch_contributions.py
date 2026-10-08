"""Scrape the public contribution calendar (no token) -> data/contributions.json"""
import datetime as dt, json, os, re
import requests
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
user = json.load(open(os.path.join(ROOT, "profile.json"), encoding="utf-8"))["username"]
html = requests.get(f"https://github.com/users/{user}/contributions",
                    headers={"User-Agent": "profile-readme-bot"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")
tips = {t.get("for"): t.get_text(strip=True) for t in soup.select("tool-tip")}
days = []
for td in soup.select("td[data-date]"):
    m = re.match(r"^(\d+|No) contribution", tips.get(td.get("id"), ""))
    days.append({"date": td["data-date"], "count": 0 if not m or m.group(1) == "No" else int(m.group(1))})
days.sort(key=lambda d: d["date"])
longest = run = 0
for d in days:
    run = run + 1 if d["count"] else 0
    longest = max(longest, run)
current = 0
for d in reversed(days):
    if d["count"]:
        current += 1
    elif d["date"] == dt.date.today().isoformat():
        continue
    else:
        break
best = max(days, key=lambda d: d["count"])
json.dump({"user": user, "total": sum(d["count"] for d in days), "current_streak": current,
           "longest_streak": longest, "best_day": best, "days": days},
          open(os.path.join(ROOT, "data", "contributions.json"), "w"), indent=1)
print(user, sum(d["count"] for d in days), "contributions")
