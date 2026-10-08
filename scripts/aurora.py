"""Design B — Aurora: animated aurora hero, glowing skill tiles, 3D isometric contribution city."""
from lib import P, SANS, MONO, STATIC, esc, data_uri, icon, brand, contributions, anim, svg_open, write

W = 860
BG = "#070b1a"
TXT, MUTED = "#f8fafc", "#94a3b8"
AUR = ["#22d3ee", "#a855f7", "#ec4899", "#34d399"]

# ---------------------------------------------------------------- HERO
H = 300
roles = P["roles"]
per = 3.0  # seconds per role
n = len(roles)
css = (".f{opacity:0;animation:fi .9s ease-out forwards}@keyframes fi{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
       ".b1{animation:m1 14s ease-in-out infinite alternate}@keyframes m1{to{transform:translate(220px,60px)}}"
       ".b2{animation:m2 17s ease-in-out infinite alternate}@keyframes m2{to{transform:translate(-200px,-40px)}}"
       ".b3{animation:m3 12s ease-in-out infinite alternate}@keyframes m3{to{transform:translate(120px,-70px)}}"
       ".ring{animation:spin 6s linear infinite;transform-origin:700px 140px}@keyframes spin{to{transform:rotate(360deg)}}"
       ".cur{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}")
for i in range(n):
    a, b = i / n * 100, (i + 1) / n * 100
    # each role: typed in, held, erased within its slot of the cycle
    css += (f".r{i}{{clip-path:inset(0 100% 0 0);animation:t{i} {per*n}s linear infinite}}"
            f"@keyframes t{i}{{0%,{a:.2f}%{{clip-path:inset(0 100% 0 0)}}{a + (b-a)*.35:.2f}%,{a + (b-a)*.8:.2f}%"
            f"{{clip-path:inset(0 0 0 0)}}{b - .01:.2f}%,100%{{clip-path:inset(0 100% 0 0)}}}}")

p = [svg_open(W, H, css), "<defs>",
     '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>',
     '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">' +
     "".join(f'<stop offset="{i/3:.2f}" stop-color="{c}"/>' for i, c in enumerate(AUR)) + "</linearGradient>",
     f'<clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>',
     '<clipPath id="av"><circle cx="700" cy="140" r="78"/></clipPath>',
     "</defs>",
     f'<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{BG}"/>',
     f'<g filter="url(#blur)" opacity=".75">'
     f'<circle class="{"" if STATIC else "b1"}" cx="140" cy="70" r="120" fill="{AUR[0]}" opacity=".55"/>'
     f'<circle class="{"" if STATIC else "b2"}" cx="560" cy="240" r="140" fill="{AUR[1]}" opacity=".6"/>'
     f'<circle class="{"" if STATIC else "b3"}" cx="330" cy="260" r="110" fill="{AUR[2]}" opacity=".45"/></g>',
     # subtle grid
     "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#ffffff" stroke-opacity=".035"/>' for x in range(0, W, 40)),
     "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#ffffff" stroke-opacity=".035"/>' for y in range(0, H, 40)),
     "</g>",
     f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="#ffffff22"/>',
     f'<g{anim("f", .1)}><text x="48" y="78" font-family="{MONO}" font-size="14" fill="{AUR[0]}">&lt;hello world /&gt;</text></g>',
     f'<g{anim("f", .3)}><text x="46" y="134" font-family="{SANS}" font-size="46" font-weight="800" fill="{TXT}">'
     f'{esc(P["name"])}</text></g>',
     f'<g{anim("f", .5)}><text x="48" y="172" font-family="{SANS}" font-size="20" font-weight="600" fill="{MUTED}">I\'m a</text>']
for i, r in enumerate(roles):
    if STATIC and i:
        continue
    p.append(f'<text class="{"" if STATIC else f"r{i}"}" x="104" y="172" font-family="{SANS}" font-size="20" '
             f'font-weight="800" fill="url(#g)">{esc(r)}</text>')
p.append("</g>")
p.append(f'<g{anim("f", .7)}><text x="48" y="214" font-family="{SANS}" font-size="15" fill="#cbd5e1">'
         f'{esc(P["bio"].replace("|", " "))}</text>')
# pills
px = 48
for t, c in ((f'@ {P["company"]}', AUR[1]), (f'📍 {P["location"]}', AUR[0]), ("✦ Open to collabs", AUR[3])):
    w = len(t) * 7.6 + 28
    p.append(f'<rect x="{px}" y="236" width="{w:.0f}" height="30" rx="15" fill="#ffffff0f" stroke="{c}" stroke-opacity=".55"/>'
             f'<text x="{px + w/2:.0f}" y="256" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{TXT}">{esc(t)}</text>')
    px += w + 10
p.append("</g>")
# avatar with spinning gradient ring
p.append(f'<g{anim("f", .4)}>'
         f'<circle class="{"" if STATIC else "ring"}" cx="700" cy="140" r="90" fill="none" stroke="url(#g)" stroke-width="4" '
         f'stroke-dasharray="120 30 60 30" stroke-linecap="round"/>'
         f'<circle cx="700" cy="140" r="82" fill="{BG}"/>'
         f'<image href="{data_uri("assets/avatar.jpg")}" x="622" y="62" width="156" height="156" clip-path="url(#av)" '
         f'preserveAspectRatio="xMidYMid slice"/></g>')
write("aurora-hero.svg", p)

# ---------------------------------------------------------------- SKILLS
cols, tile, gap = 10, 72, 12
rows = (len(P["stack"]) + cols - 1) // cols
SH = 64 + rows * (tile + 30)
css2 = (".t{opacity:0;animation:pop .5s cubic-bezier(.3,1.6,.5,1) forwards;transform-box:fill-box;transform-origin:center}"
        "@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}")
x0 = (W - (cols * tile + (cols - 1) * gap)) / 2
p = [svg_open(W, SH, css2), "<defs>",
     '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter></defs>',
     f'<rect x=".5" y=".5" width="{W-1}" height="{SH-1}" rx="22" fill="{BG}" stroke="#ffffff22"/>',
     f'<text x="{W/2}" y="38" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="3" '
     f'fill="{MUTED}">TECH I BUILD WITH</text>']
for i, nme in enumerate(P["stack"]):
    r, c = divmod(i, cols)
    tx, ty = x0 + c * (tile + gap), 58 + r * (tile + 30)
    col = brand(nme)
    lum = int(col[1:3], 16) * .3 + int(col[3:5], 16) * .59 + int(col[5:7], 16) * .11
    fg = "#f1f5f9" if lum < 70 else col
    glow = "#94a3b8" if lum < 70 else col
    p.append(f'<g{anim("t", .05 * i)}>'
             f'<circle cx="{tx+tile/2:.1f}" cy="{ty+tile/2-6:.1f}" r="18" fill="{glow}" opacity=".35" filter="url(#glow)"/>'
             f'<rect x="{tx:.1f}" y="{ty}" width="{tile}" height="{tile-8}" rx="16" fill="#ffffff08" stroke="#ffffff1c"/>'
             f'{icon(nme, tx + tile/2 - 15, ty + 17, 30, fg)}'
             f'<text x="{tx+tile/2:.1f}" y="{ty+tile+12}" text-anchor="middle" font-family="{SANS}" font-size="11" '
             f'fill="{MUTED}">{esc(nme)}</text></g>')
write("skills.svg", p)

# ---------------------------------------------------------------- 3D CONTRIBUTIONS
d = contributions()
U, V = 6.6, 3.8          # iso half-width / half-height of a tile
K = 9                    # px of height per contribution
ox = 140
oy = 120
CH = 380
css3 = (".bar{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);animation:rise .8s cubic-bezier(.2,.9,.3,1.2) forwards}"
        "@keyframes rise{to{transform:scaleY(1)}}"
        ".f{opacity:0;animation:fi .8s ease-out forwards}@keyframes fi{to{opacity:1}}")
p = [svg_open(W, CH, css3), "<defs>",
     '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">' +
     "".join(f'<stop offset="{i/3:.2f}" stop-color="{c}"/>' for i, c in enumerate(AUR)) + "</linearGradient>",
     "</defs>",
     f'<rect x=".5" y=".5" width="{W-1}" height="{CH-1}" rx="22" fill="{BG}" stroke="#ffffff22"/>',
     f'<text x="34" y="46" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="3" fill="{MUTED}">CONTRIBUTION CITY</text>',
     f'<text x="34" y="86" font-family="{SANS}" font-size="38" font-weight="800" fill="url(#g)">{d["total"]:,}</text>',
     f'<text x="34" y="108" font-family="{SANS}" font-size="13" fill="{MUTED}">contributions in the last year</text>']
stats = [("Longest streak", f'{d["longest_streak"]} days'), ("Current streak", f'{d["current_streak"]} days'),
         ("Best day", f'{d["best_day"]["count"]} commits')]
for i, (k, v) in enumerate(stats):
    p.append(f'<text x="{34 + i*120}" y="{CH-48}" font-family="{SANS}" font-size="12" fill="{MUTED}">{k}</text>'
             f'<text x="{34 + i*120}" y="{CH-28}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TXT}">{v}</text>')

LV = ["#1e293b", "#155e75", "#7e22ce", "#db2777", "#22d3ee"]


def shade(hexc, f):
    r, g, b = int(hexc[1:3], 16), int(hexc[3:5], 16), int(hexc[5:7], 16)
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


WX, WY, DX, DY = 12.0, -3.0, 5.5, 6.0   # week axis (right, slightly up) / day axis (down-right)
S = 0.84                                  # tile size relative to grid step
ox, oy = 96, 278
cells = []
for i, day in enumerate(d["days"]):
    col, row = divmod(d["offset"] + i, 7)
    cells.append((col, row, day))
cells.sort(key=lambda t: (t[1] * DY + t[0] * WY, t[0] * WX))  # painter's order: back to front
for col, row, day in cells:
    x0, y0 = ox + col * WX + row * DX, oy + col * WY + row * DY
    h = 2 + day["count"] * K
    c = LV[day["lv"]]
    P0 = (x0, y0); P1 = (x0 + WX*S, y0 + WY*S); P3 = (x0 + DX*S, y0 + DY*S); P2 = (P1[0] + DX*S, P1[1] + DY*S)
    up = lambda q: (q[0], q[1] - h)
    poly = lambda pts: "M" + "L".join(f"{q[0]:.1f} {q[1]:.1f}" for q in pts) + "z"
    top = poly([up(P0), up(P1), up(P2), up(P3)])
    front = poly([up(P3), up(P2), P2, P3])
    left = poly([up(P0), up(P3), P3, P0])
    cls = "" if STATIC else f' class="bar" style="animation-delay:{(col + row) * 0.02:.2f}s"'
    p.append(f'<g{cls}><path d="{left}" fill="{shade(c, .6)}"/><path d="{front}" fill="{shade(c, .8)}"/>'
             f'<path d="{top}" fill="{c}"/><title>{day["count"]} on {day["date"]}</title></g>')
write("contrib-3d.svg", p)

# ---------------------------------------------------------------- PROJECT CARDS
PW, PH = 424, 150
for k, pr in enumerate(P["projects"], 1):
    acc = AUR[(k - 1) % 4]
    p = [svg_open(PW, PH, ".f{opacity:0;animation:fi .8s ease-out forwards}@keyframes fi{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"),
         '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">' +
         "".join(f'<stop offset="{i/3:.2f}" stop-color="{c}"/>' for i, c in enumerate(AUR)) + "</linearGradient>"
         '<filter id="bl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="30"/></filter>'
         f'<clipPath id="c"><rect width="{PW}" height="{PH}" rx="20"/></clipPath></defs>',
         f'<g{anim("f", .1*k)}><g clip-path="url(#c)"><rect width="{PW}" height="{PH}" fill="{BG}"/>'
         f'<circle cx="{PW-30}" cy="10" r="70" fill="{acc}" opacity=".35" filter="url(#bl)"/></g>',
         f'<rect x="1" y="1" width="{PW-2}" height="{PH-2}" rx="19" fill="none" stroke="url(#g)" stroke-opacity=".7" stroke-width="1.5"/>',
         f'<text x="24" y="44" font-family="{SANS}" font-size="19" font-weight="800" fill="{TXT}">{esc(pr["name"])}</text>',
         f'<text x="{PW-24}" y="44" text-anchor="end" font-family="{SANS}" font-size="12" font-weight="700" fill="{acc}">'
         f'{"LIVE ↗" if pr.get("live") else "CODE ↗"}</text>',
         f'<text x="24" y="76" font-family="{SANS}" font-size="13.5" fill="#cbd5e1">{esc(pr["desc"])}</text>']
    tx = 24
    for t in pr["tags"]:
        col = brand(t)
        lum = int(col[1:3], 16) * .3 + int(col[3:5], 16) * .59 + int(col[5:7], 16) * .11
        p.append(icon(t, tx, 104, 18, "#f1f5f9" if lum < 70 else col))
        tx += 30
    p.append(f'<text x="{tx+4}" y="118" font-family="{MONO}" font-size="12" fill="{MUTED}">{esc(" · ".join(pr["tags"]))}</text></g>')
    write(f"project-{k}.svg", p)
