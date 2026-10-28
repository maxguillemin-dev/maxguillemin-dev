"""Neofetch-style info card -> info-card.svg (STATIC=1 for a frozen frame)."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

from theme import *

ROOT = Path(__file__).resolve().parent.parent
STATIC = os.environ.get("STATIC") == "1"
W, LH = 490, 22

ROWS = [
    ("Role", "Full Stack Developer, AI-augmented", GREEN),
    ("Location", "Clermont-Ferrand, France", FG),
    ("Status", "Open to work: CDI, immediately", ORANGE),
    None,
    ("Now", "MCP server in TypeScript", CYAN),
    ("Prev", "2y alternance @ Les Biens en Commun", FG),
    ("Edu", "Master Epitech + RNCP niveau 6", FG),
    None,
    ("Frontend", "TypeScript React Next.js Tailwind Zustand", BLUE),
    ("Backend", "NestJS Node.js PostgreSQL pgvector", BLUE),
    ("DevOps", "Docker AWS Vercel Git", BLUE),
    ("AI", "Claude API, Claude Code, OpenAI API", PURPLE),
    None,
    ("Langs", "Francais (natif), English (B1 -> B2)", FG),
    ("Hobbies", "Japon, jeux video, TCG, dev perso", FG),
]


def main() -> None:
    h = 70 + len(ROWS) * LH + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" font-family="{FONT}" font-size="13">',
           "<style>@keyframes l{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
           + (".r{opacity:1}" if STATIC else ".r{opacity:0;animation:l .4s ease-out forwards}") + "</style>",
           f'<rect width="{W}" height="{h}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
           f'<rect width="{W}" height="32" rx="10" fill="{PANEL}"/><rect y="22" width="{W}" height="10" fill="{PANEL}"/>',
           '<circle cx="20" cy="16" r="5" fill="#ff5f56"/><circle cx="38" cy="16" r="5" fill="#ffbd2e"/><circle cx="56" cy="16" r="5" fill="#27c93f"/>',
           f'<text x="{W // 2}" y="20" fill="{MUTED}" font-size="11" text-anchor="middle">maxime@github: ~</text>',
           f'<text x="20" y="58" fill="{GREEN}">maxime</text><text x="68" y="58" fill="{MUTED}">@</text><text x="78" y="58" fill="{BLUE}">maxguillemin-dev</text>',
           f'<text x="20" y="74" fill="{BORDER}">{"-" * 40}</text>']
    y, i = 98, 0
    for row in ROWS:
        if row is None:
            y += LH // 2
            continue
        k, v, c = row
        d = 0 if STATIC else 0.25 + i * 0.12
        out.append(f'<g class="r" style="animation-delay:{d:.2f}s"><text x="20" y="{y}" fill="{ORANGE}" font-weight="bold">{k}</text>'
                   f'<text x="110" y="{y}" fill="{c}">{escape(v)}</text></g>')
        y += LH
        i += 1
    for j, col in enumerate(["#f7768e", "#ff9e64", "#e0af68", "#9ece6a", "#7dcfff", "#7aa2f7", "#bb9af7", "#c0caf5"]):
        out.append(f'<rect x="{20 + j * 22}" y="{h - 34}" width="22" height="14" fill="{col}"/>')
    out.append("</svg>")
    (ROOT / "info-card.svg").write_text("\n".join(out))
    print("wrote info-card.svg")


if __name__ == "__main__":
    main()
