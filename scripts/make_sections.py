"""Render every README section graphic in the city theme, light and dark.

Edit the data blocks below (CONTACT, PROJECTS, STACK, HISTORY) and re-run.

Usage: python scripts/make_sections.py
Writes: assets/<name>-dark.svg and assets/<name>-light.svg
"""
from datetime import date, timedelta
from html import escape
from pathlib import Path
from textwrap import wrap

from theme import FONT_MONO, FONT_SANS, THEMES, iso_box, shade

OUT = Path("assets")

PORTFOLIO = "https://faizan.click"
PLAY = "https://play.google.com/store/apps/details?id=com.rishtaandrang.app"
GH = "https://github.com/Faizan-mk/"

# label, shown value, link, accent
CONTACT = [
    ("portfolio", "faizan.click", PORTFOLIO, False),
    ("linkedin", "in/muhammad-faizanmk", "https://www.linkedin.com/in/muhammad-faizanmk", False),
    ("email", "faizannaizi007@gmail.com", "mailto:faizannaizi007@gmail.com", False),
    ("resume", "view pdf", "https://drive.google.com/file/d/1gvfkw35DghDp4BdIwe0AmLJlogmfWNlx/view?usp=sharing", True),
]

# slug, title, stack, description, link, building height, featured
PROJECTS = [
    ("lovebirds", "Lovebirds", "React Native · Expo · TypeScript · Supabase",
     "28-screen matrimonial app live on Google Play: selfie and CNIC checks, realtime chat, Urdu UI, subscriptions",
     PLAY, 54, True),
    ("coffee", "Coffee Shop Website", "React 19 · Vite · Tailwind · Supabase",
     "Multi-page site with a categorized menu and a store locator for 21 outlets across 7 cities",
     "https://cblt-cofee-website.vercel.app", 44, False),
    ("hostel", "Hostel Management System", "React · Node.js · Express · MySQL · JWT",
     "Admin and student dashboards: rooms, fees and invoicing, complaints and a notice board",
     GH + "Hostal_Mangment-system", 40, False),
    ("travel", "AI Travel Planner", "React · Node.js · Express · MySQL",
     "AI chatbot, budget planner, expense tracker, live weather and an SOS emergency module",
     GH + "travel-planner-frontend", 36, False),
    ("admin", "Lovebirds Admin", "Next.js · Tailwind · Supabase · AWS Amplify",
     "Moderation dashboard for the live app: reports, bans, story review, update popups and push announcements",
     PLAY, 32, False),
    ("auth", "MERN Auth System", "React · Node.js · Express · MongoDB · JWT",
     "Registration and login from scratch with bcrypt hashing, protected routes and Context API state",
     GH + "User-Authentication-System-MERN-Stack-", 28, False),
]

STACK = [
    ("frontend", ["React", "Next.js", "TypeScript", "JavaScript", "Tailwind", "Vite", "React Router"], False),
    ("backend", ["Node.js", "Express", "REST APIs", "JWT · RBAC", "Python", "Sequelize"], False),
    ("data · cloud", ["Supabase", "PostgreSQL", "MongoDB", "MySQL", "AWS", "Vercel", "Git"], False),
    ("ai · llm", ["Gemini API", "LangChain", "RAG", "Generative AI"], False),
    ("mobile", ["React Native", "Expo", "EAS Build", "Google Play", "RevenueCat"], True),
]

# (year, month, place, role, above_road)
HISTORY = [
    (2022, 9, "University of Mianwali", "BS Computer Science", True),
    (2025, 4, "CodeAlpha", "Frontend Developer Intern", False),
    (2026, 3, "DevelopersHub", "Backend Developer Intern", True),
    (2026, 8, "BitzSol", "Full Stack Developer", False),
]
WHEN = {"University of Mianwali": "2022 – 2026 · CGPA 3.44"}   # label instead of the month
CURRENT = "BitzSol"

STYLE = (
    "<style>.t{font-family:" + FONT_SANS + "}.m{font-family:" + FONT_MONO + "}"
    ".fade{opacity:0;animation:f .6s ease-out forwards}"
    "@keyframes f{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}</style>"
)


def svg(w: int, h: int, label: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label)}">{STYLE}{body}</svg>')


def rise(inner: str, delay: float, dur: float = .5) -> str:
    """Wrap content so it grows up from its own baseline (origin must be the base)."""
    return (f'<g transform="scale(1,0)"><animateTransform attributeName="transform" type="scale" '
            f'from="1 0" to="1 1" begin="{delay:.2f}s" dur="{dur}s" fill="freeze"/>{inner}</g>')


def faces(t: dict, green: bool) -> tuple[str, str, str]:
    if green:
        return t["accent"], t["accent_dim"], t["accent_deep"]
    return t["block"], t["block_l"], t["block_r"]


# ---------------------------------------------------------------- contact
def contact(t, label, value, accent):
    w, h = 205, 48
    col = t["accent"] if accent else t["border"]
    txt = t["accent"] if accent else t["text"]
    body = (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="{t["panel"]}" stroke="{col}"/>'
            f'<text x="16" y="20" class="m" font-size="11" fill="{t["muted"]}">'
            f'<tspan fill="{t["accent"]}">$</tspan> open {label}</text>'
            f'<text x="16" y="37" class="t" font-size="{12 if len(value) > 20 else 13}" font-weight="600" fill="{txt}">{escape(value)}</text>'
            f'<text x="{w - 16}" y="31" text-anchor="end" class="t" font-size="15" fill="{t["muted"]}">↗</text>')
    return svg(w, h, f"{label}: {value}", body)


# ---------------------------------------------------------------- projects
def project(t, i, title, stack, desc, height, featured):
    w, h = 420, 132
    top, left, right = faces(t, featured)
    lines = wrap(desc, 44)[:3]
    stroke = t["accent"] if featured else t["border"]
    body = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t["panel"]}" stroke="{stroke}"/>']
    # little ground tile + building on the right
    bx, by = 362, 104
    body.append(f'<polygon points="{bx},{by - 17} {bx + 34},{by} {bx},{by + 17} {bx - 34},{by}" fill="none" '
                f'stroke="{t["border"]}" stroke-dasharray="3 3"/>')
    building = iso_box(0, 0, 20, height, top, left, right)
    # windows on the front faces
    win = "".join(
        f'<rect x="{fx}" y="{-height + 10 + k * 8}" width="2.4" height="2.4" fill="{t["window"] if featured else t["panel"]}" '
        f'opacity="{.9 if featured else .55}"/>'
        for k in range(max(0, int((height - 12) / 8))) for fx in (-13, -7, 6, 12)
        if (k * 7 + fx + i) % 3)
    body.append(f'<g transform="translate({bx},{by})">{rise(building + win, .3 + i * .08, .6)}</g>')
    tag = "featured" if featured else None
    y = 34
    body.append(f'<g class="fade" style="animation-delay:{.1 + i * .08:.2f}s">')
    body.append(f'<text x="20" y="{y}" class="t" font-size="16" font-weight="600" fill="{t["text"]}">{escape(title)}</text>')
    if tag:
        tw = len(title) * 8.6 + 28
        body.append(f'<rect x="{tw}" y="{y - 13}" width="62" height="18" rx="9" fill="none" stroke="{t["accent"]}"/>'
                    f'<text x="{tw + 31}" y="{y}" text-anchor="middle" class="m" font-size="10" fill="{t["accent"]}">{tag}</text>')
    body.append(f'<text x="20" y="{y + 20}" class="m" font-size="10.5" fill="{t["accent"] if featured else t["muted"]}">'
                f'{escape(stack)}</text>')
    for k, line in enumerate(lines):
        body.append(f'<text x="20" y="{y + 48 + k * 18}" class="t" font-size="12.5" fill="{t["body"]}">{escape(line)}</text>')
    body.append("</g>")
    return svg(w, h, f"{title} — {desc}. Built with {stack}.", "".join(body))


# ---------------------------------------------------------------- stack
def stack(t):
    w = 860
    col_w = w / len(STACK)
    rows = max(len(items) for _, items, _ in STACK)
    h = 150 + rows * 22 + 20
    body = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>']
    base_y = 104
    for gi, (name, items, green) in enumerate(STACK):
        cx = col_w * gi + col_w / 2
        top, left, right = faces(t, green)
        if gi:
            body.append(f'<line x1="{col_w * gi:.0f}" y1="24" x2="{col_w * gi:.0f}" y2="{h - 24}" stroke="{t["border"]}"/>')
        # one voxel per tool, stacked; each appears in turn
        for k in range(len(items)):
            y = base_y - k * 8
            blk = iso_box(0, 0, 16, 8, top, left, right)
            body.append(f'<g transform="translate({cx:.1f},{y})" opacity="0">'
                        f'<animate attributeName="opacity" to="1" begin="{.2 + gi * .15 + k * .07:.2f}s" dur=".2s" fill="freeze"/>'
                        f'{blk}</g>')
        body.append(f'<text x="{cx:.1f}" y="{base_y + 34}" text-anchor="middle" class="m" font-size="12" '
                    f'fill="{t["accent"] if green else t["muted"]}">{escape(name)} · {len(items)}</text>')
        body.append(f'<g class="fade" style="animation-delay:{.4 + gi * .15:.2f}s">')
        for k, item in enumerate(items):
            body.append(f'<text x="{cx:.1f}" y="{base_y + 64 + k * 22}" text-anchor="middle" class="t" font-size="13.5" '
                        f'fill="{t["text"] if green else t["body"]}">{escape(item)}</text>')
        body.append("</g>")
    label = "Tech stack. " + " ".join(f"{n}: {', '.join(i)}." for n, i, _ in STACK)
    return svg(w, int(h), label, "".join(body))


# ---------------------------------------------------------------- history
def history(t):
    w, h = 860, 210
    x0, x1, road_y = 50, 810, 108
    y0, m0 = min((y, m) for y, m, *_ in HISTORY)
    start, end = date(y0 - (m0 <= 4), (m0 - 5) % 12 + 1, 1), date.today() + timedelta(days=70)
    span = (end - start).days

    def xpos(y, m):
        return x0 + (date(y, m, 1) - start).days / span * (x1 - x0)

    body = [f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="{t["panel"]}" stroke="{t["border"]}"/>',
            f'<line x1="{x0}" y1="{road_y}" x2="{x1}" y2="{road_y}" stroke="{t["road"]}" stroke-width="14" stroke-linecap="round"/>',
            f'<line x1="{x0}" y1="{road_y}" x2="{x1}" y2="{road_y}" stroke="{t["faint"]}" stroke-width="1" stroke-dasharray="7 7" opacity=".7"/>']
    for i, (yr, mo, place, role, above) in enumerate(HISTORY):
        x = xpos(yr, mo)
        current = place == CURRENT
        col = t["accent"] if current else t["block"]
        stem_end = road_y - 22 if above else road_y + 22
        ty = road_y - 70 if above else road_y + 46
        d = .3 + i * .25
        body.append(
            f'<g class="fade" style="animation-delay:{d:.2f}s">'
            f'<line x1="{x:.1f}" y1="{road_y}" x2="{x:.1f}" y2="{stem_end}" stroke="{col}" stroke-width="1.2"/>'
            f'<circle cx="{x:.1f}" cy="{road_y}" r="6" fill="{t["panel"]}" stroke="{col}" stroke-width="2.5"/>'
            f'<text x="{x:.1f}" y="{ty}" text-anchor="middle" class="m" font-size="10.5" fill="{t["muted"]}">'
            f'{WHEN.get(place, date(yr, mo, 1).strftime("%b %Y"))}</text>'
            f'<text x="{x:.1f}" y="{ty + 18}" text-anchor="middle" class="t" font-size="14" font-weight="600" '
            f'fill="{t["accent"] if current else t["text"]}">{escape(place)}</text>'
            f'<text x="{x:.1f}" y="{ty + 35}" text-anchor="middle" class="t" font-size="12" fill="{t["body"]}">'
            f'{escape(role)}</text></g>')

    # "now" marker that pulses at the end of the road
    body.append(
        f'<g class="fade" style="animation-delay:1.4s">'
        f'<circle cx="{x1}" cy="{road_y}" r="7" fill="{t["accent"]}"/>'
        f'<circle cx="{x1}" cy="{road_y}" r="7" fill="none" stroke="{t["accent"]}">'
        f'<animate attributeName="r" values="7;16" dur="1.8s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="1.8s" repeatCount="indefinite"/></circle>'
        f'<text x="{x1}" y="{road_y - 22}" text-anchor="middle" class="m" font-size="11" fill="{t["accent"]}">now</text></g>')
    # a car driving the career road
    body.append(f'<rect width="10" height="5" rx="2" y="-2.5" x="-5" fill="{t["car_a"]}">'
                f'<animateMotion dur="7s" repeatCount="indefinite" path="M{x0},{road_y} L{x1},{road_y}"/></rect>')
    label = "Career: " + "; ".join(f"{date(y, m, 1):%b %Y} {p}, {r}" for y, m, p, r, _ in HISTORY) + "."
    return svg(w, h, label, "".join(body))


def main():
    OUT.mkdir(exist_ok=True)
    n = 0
    for mode, t in THEMES.items():
        def save(name, content):
            nonlocal n
            (OUT / f"{name}-{mode}.svg").write_text(content, encoding="utf-8")
            n += 1
        for label, value, _, accent in CONTACT:
            save(f"contact-{label}", contact(t, label, value, accent))
        for i, (slug, title, stk, desc, _, height, featured) in enumerate(PROJECTS):
            save(f"project-{slug}", project(t, i % 2, title, stk, desc, height, featured))
        save("stack", stack(t))
        save("history", history(t))
    print(f"wrote {n} files to {OUT}/")


if __name__ == "__main__":
    main()
