"""Shared palette: grey everywhere, purple only where it means something."""

FONT_SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
FONT_MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "panel": "#0d1117",
        "sky": "#0a0716",          # city background (night)
        "border": "#30363d",
        "text": "#e6edf3",
        "body": "#c9d1d9",
        "muted": "#8b949e",
        "faint": "#6e7681",
        "accent": "#a855f7",
        "accent_dim": "#7e22ce",
        "accent_deep": "#4c1d95",
        "block": "#484f58",        # grey building faces: top / left / right
        "block_l": "#30363d",
        "block_r": "#21262d",
        "ground": "#0d1117",
        "road": "#1c2128",
        "levels": ["#161b22", "#3b1d6e", "#6d28d9", "#9333ea", "#c084fc"],
        "window": "#f2cc60",
        "car_a": "#f2cc60",
        "car_b": "#f85149",
        "flag": "#a855f7",
    },
    "light": {
        "panel": "#ffffff",
        "sky": "#f6f0ff",          # city background (day)
        "border": "#d0d7de",
        "text": "#1f2328",
        "body": "#3d444d",
        "muted": "#656d76",
        "faint": "#8c959f",
        "accent": "#7e22ce",
        "accent_dim": "#9333ea",
        "accent_deep": "#581c87",
        "block": "#afb8c1",
        "block_l": "#d0d7de",
        "block_r": "#e6eaef",
        "ground": "#f6f8fa",
        "road": "#d8dee4",
        "levels": ["#ebedf0", "#e9d5ff", "#c084fc", "#9333ea", "#6b21a8"],
        "window": "#ffffff",
        "car_a": "#1f6feb",
        "car_b": "#cf222e",
        "flag": "#7e22ce",
    },
}


def iso_box(x, y, half_w, height, top, left, right, extra=""):
    """An isometric box whose base centre sits at (x, y)."""
    w, h = half_w, height
    return (
        f'<g transform="translate({x:.1f},{y:.1f})"{extra}>'
        f'<polygon points="0,{-h - w * .5:.1f} {w:.1f},{-h:.1f} 0,{-h + w * .5:.1f} {-w:.1f},{-h:.1f}" fill="{top}"/>'
        f'<polygon points="{-w:.1f},{-h:.1f} 0,{-h + w * .5:.1f} 0,{w * .5:.1f} {-w:.1f},0" fill="{left}"/>'
        f'<polygon points="{w:.1f},{-h:.1f} 0,{-h + w * .5:.1f} 0,{w * .5:.1f} {w:.1f},0" fill="{right}"/>'
        "</g>"
    )


def shade(hex_color: str, factor: float) -> str:
    """Darken (factor < 1) or lighten (factor > 1) a hex colour."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if factor < 1:
        r, g, b = (int(c * factor) for c in (r, g, b))
    else:
        r, g, b = (int(c + (255 - c) * (factor - 1)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"
