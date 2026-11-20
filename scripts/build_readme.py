"""Write README.md from the section data, so links and alt text never drift.

Every graphic is a <picture> with a dark and a light version; GitHub serves the
one that matches the visitor's theme.

Usage: python scripts/build_readme.py
"""

import hashlib
from pathlib import Path

from make_sections import CONTACT, HISTORY, PROJECTS, STACK


VDIR = Path("assets/v")
_used: set[str] = set()


def v(path: str) -> str:
    """Copy the SVG to assets/v/<name>-<hash>.svg and link that copy.

    A new image always gets a new file name, so no browser, CDN or camo cache
    can keep showing an old version. Copies nothing links to are removed.
    """
    data = Path(path).read_bytes().replace(b"\r\n", b"\n")   # same name on Windows and Linux
    name = f"{Path(path).stem}-{hashlib.md5(data).hexdigest()[:8]}.svg"
    VDIR.mkdir(parents=True, exist_ok=True)
    (VDIR / name).write_bytes(data)
    _used.add(name)
    return f"./{VDIR.as_posix()}/{name}"


def pic(name: str, alt: str, width: str) -> str:
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{v(name + "-dark.svg")}">'
            f'<img src="{v(name + "-light.svg")}" width="{width}" alt="{alt}"></picture>')


def prompt(cmd: str) -> str:
    return f"<h3><code>faizan@github ~ $ {cmd}</code></h3>"


def main():
    p = []
    p.append('<div align="center">\n')
    p.append(pic("assets/city", "Muhammad Faizan — GitHub contributions over the last year as an animated isometric city", "100%"))
    p.append('\n\n<b>Full stack developer</b> shipping web and mobile apps with React, Next.js, '
             'React Native and Node.js — from Supabase backends to a live app on Google Play.<br>'
             'Full Stack Developer at BitzSol · Rawalpindi, Pakistan.\n')
    p.append("</div>\n\n<br>\n")

    p.append(prompt("whoami") + "\n")
    p.append('<p align="center">'
             + pic("assets/portrait", "ASCII portrait of Muhammad Faizan", "42.5%") + "\n"
             + pic("assets/card", "Neofetch-style card: Full Stack Developer at BitzSol, "
                   "shipped Lovebirds on Google Play, React, Next.js, React Native, Supabase", "56.5%")
             + "</p>\n\n")

    p.append(prompt("./contact.sh") + "\n<p align=\"center\">\n")
    for label, value, url, _ in CONTACT:
        p.append(f'<a href="{url}">' + pic(f"assets/contact-{label}", f"{label}: {value}", f"{96 // len(CONTACT)}%") + "</a>\n")
    p.append("</p>\n\n<br>\n\n")

    p.append(prompt("ls ./projects") + "\n<p align=\"center\">\n")
    for slug, title, stack, desc, url, _, _ in PROJECTS:
        p.append(f'<a href="{url}">' + pic(f"assets/project-{slug}", f"{title}: {desc}. Built with {stack}.", "49%")
                 + "</a>\n")
    p.append("</p>\n\n<br>\n\n")

    p.append(prompt("cat stack.txt") + "\n<p align=\"center\">"
             + pic("assets/stack", "Tech stack — " + "; ".join(f"{n}: {', '.join(i)}" for n, i, _ in STACK), "100%")
             + "</p>\n\n<br>\n\n")

    p.append(prompt("history") + "\n<p align=\"center\">"
             + pic("assets/history", "Career — " + "; ".join(f"{pl} ({r}), {y}" for y, m, pl, r, _ in HISTORY), "100%")
             + "</p>\n\n")

    p.append('<div align="center">\n\n<code>faizan@github ~ $ exit</code><br>\n'
             "<sub>Open to roles in Pakistan and to relocation · "
             '<a href="https://www.linkedin.com/in/muhammad-faizanmk">LinkedIn</a> · '
             "the city above rebuilds itself every day from my real contributions</sub>\n\n</div>\n")

    open("README.md", "w", encoding="utf-8").write("".join(p))
    for f in VDIR.glob("*.svg"):
        if f.name not in _used:
            f.unlink()
    print("wrote README.md")


if __name__ == "__main__":
    main()
