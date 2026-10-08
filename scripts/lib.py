"""Shared helpers: profile data, brand icons, embedded photos, contribution data."""
import base64
import datetime as dt
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
STATIC = os.environ.get("STATIC") == "1"  # frozen frame (no animation) for previews

P = json.load(open("profile.json", encoding="utf-8"))
ICONS = json.load(open("assets/icons.json"))
SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def data_uri(path):
    mime = {"jpg": "image/jpeg", "png": "image/png", "webp": "image/webp"}[path.rsplit(".", 1)[1]]
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def icon(name, x, y, size, color=None):
    """Simple Icons glyph (24x24 viewBox) placed at x,y with given size."""
    i = ICONS[name]
    s = size / 24
    return (f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" '
            f'd="{i["path"]}" fill="{color or "#" + i["hex"]}"/>')


def brand(name):
    return "#" + ICONS[name]["hex"]


def contributions():
    d = json.load(open("data/contributions.json"))
    days = d["days"]
    mx = max([x["count"] for x in days] + [1])
    for x in days:
        c = x["count"]
        x["lv"] = 0 if c <= 0 else min(4, 1 + int(c / mx * 3.999))
    first = dt.date.fromisoformat(days[0]["date"])
    d["offset"] = (first.weekday() + 1) % 7  # Sunday = row 0
    d["weeks"] = (d["offset"] + len(days) + 6) // 7
    return d


def anim(cls, delay):
    return "" if STATIC else f' class="{cls}" style="animation-delay:{delay:.2f}s"'


def svg_open(w, h, style=""):
    st = "" if STATIC or not style else f"<style>{style}</style>"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{st}'


def write(name, parts):
    os.makedirs("assets/out", exist_ok=True) if False else None
    open(name, "w", encoding="utf-8").write("\n".join(parts) + "\n</svg>")
    print("wrote", name)
