"""Render data/contributions.json as an animated 53x7 heatmap -> contrib-heatmap.svg."""
import json
from datetime import date
from pathlib import Path

from theme import *

ROOT = Path(__file__).resolve().parent.parent
CELL, GAP, LEFT, TOP = 12, 3, 40, 62
STEP = CELL + GAP


def main() -> None:
    data = json.loads((ROOT / "data" / "contributions.json").read_text())
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    cols = (offset + len(days) + 6) // 7
    width = LEFT + cols * STEP + 20
    height = TOP + 7 * STEP + 70
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">',
           "<style>",
           f".t{{fill:{MUTED};font-size:10px}} .h{{fill:{FG};font-size:13px}} .s{{fill:{FG};font-size:12px}}",
           "@keyframes in{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}",
           ".c{opacity:0;animation:in .45s ease-out forwards}",
           "</style>",
           f'<rect width="{width}" height="{height}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
           f'<text x="20" y="28" class="h"><tspan fill="{GREEN}">max</tspan><tspan fill="{MUTED}">@github</tspan> <tspan fill="{BLUE}">~ $</tspan> ./contributions.sh</text>']
    last_month = None
    last_col = -9
    for i, d in enumerate(days):
        pos = offset + i
        col, row = divmod(pos, 7)
        dt = date.fromisoformat(d["date"])
        if row == 0 and dt.month != last_month:
            last_month = dt.month
            if col - last_col >= 3:  # skip a label that would overlap the previous one
                last_col = col
                out.append(f'<text x="{LEFT + col * STEP}" y="{TOP - 8}" class="t">{dt.strftime("%b")}</text>')
        delay = (col + row) * 0.012
        title = f'{d["count"]} contribution(s) on {d["date"]}'
        out.append(f'<rect class="c" style="animation-delay:{delay:.3f}s" x="{LEFT + col * STEP}" y="{TOP + row * STEP}" '
                   f'width="{CELL}" height="{CELL}" rx="3" fill="{HEAT[min(d["level"], 5)]}"><title>{title}</title></rect>')
    for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="14" y="{TOP + r * STEP + 10}" class="t">{label}</text>')
    fy = TOP + 7 * STEP + 28
    best = data["best_day"]
    out.append(f'<text x="20" y="{fy}" class="s"><tspan fill="{GREEN}">{data["total"]:,}</tspan> contributions in the last year'
               f' <tspan fill="{MUTED}">|</tspan> streak <tspan fill="{ORANGE}">{data["current_streak"]}d</tspan>'
               f' <tspan fill="{MUTED}">|</tspan> longest <tspan fill="{PURPLE}">{data["longest_streak"]}d</tspan>'
               f' <tspan fill="{MUTED}">|</tspan> best <tspan fill="{CYAN}">{best["count"]}</tspan></text>')
    lx = width - 20 - 6 * STEP - 70
    out.append(f'<text x="{lx}" y="{fy + 26}" class="t">Less</text>')
    for i, c in enumerate(HEAT):
        out.append(f'<rect x="{lx + 32 + i * STEP}" y="{fy + 16}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    out.append(f'<text x="{lx + 38 + 6 * STEP}" y="{fy + 26}" class="t">More</text>')
    out.append("</svg>")
    (ROOT / "contrib-heatmap.svg").write_text("\n".join(out))
    print("wrote contrib-heatmap.svg", width, "x", height)


if __name__ == "__main__":
    main()
