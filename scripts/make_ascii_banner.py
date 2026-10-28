"""ASCII name banner that prints itself row by row -> ascii-banner.svg (SMIL, plays once)."""
from pathlib import Path
from xml.sax.saxutils import escape

import pyfiglet

from theme import *

ROOT = Path(__file__).resolve().parent.parent
FS, CW, LH = 14, 8.4, 17


def main() -> None:
    lines = []
    for word in ("MAXIME", "GUILLEMIN"):
        lines += pyfiglet.figlet_format(word, font="standard", width=200).rstrip("\n").split("\n") + [""]
    lines = [l.rstrip() for l in lines]
    cols = max(len(l) for l in lines)
    W, H = int(cols * CW) + 40, len(lines) * LH + 90
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
           f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
           f'<text x="20" y="28" font-size="12" fill="{MUTED}">$ <tspan fill="{GREEN}">figlet</tspan> -f standard "Maxime Guillemin"</text>', "<defs>"]
    for i in range(len(lines)):
        t = 0.6 + i * 0.12
        out.append(f'<clipPath id="c{i}"><rect x="20" y="{44 + i * LH}" height="{LH}" width="0">'
                   f'<animate attributeName="width" from="0" to="{W}" begin="{t:.2f}s" dur="0.5s" fill="freeze"/></rect></clipPath>')
    out.append("</defs>")
    for i, l in enumerate(lines):
        out.append(f'<text xml:space="preserve" x="20" y="{44 + i * LH + 13}" font-size="{FS}" fill="{BLUE}" '
                   f'style="white-space:pre" clip-path="url(#c{i})">{escape(l)}</text>')
    ty = H - 22
    out.append(f'<text x="20" y="{ty}" font-size="13" fill="{FG}" opacity="0">full stack <tspan fill="{MUTED}">x</tspan> <tspan fill="{PURPLE}">AI-augmented</tspan> <tspan fill="{GREEN}">_</tspan>'
               f'<animate attributeName="opacity" from="0" to="1" begin="{0.6 + len(lines) * 0.12:.2f}s" dur="0.4s" fill="freeze"/></text>')
    out.append("</svg>")
    (ROOT / "ascii-banner.svg").write_text("\n".join(out))
    print("wrote ascii-banner.svg", W, H)


if __name__ == "__main__":
    main()
