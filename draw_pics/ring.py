"""
python /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/ring.py --json /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/flux_style_categories.json \
    --out style_ring \
    --inner_n 4 --ring_w 0.24 --gap  0.05
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import argparse
from pathlib import Path
import os 
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

WARM = ["#D7443D", "#E85D4A", "#F07C5E", "#F4A261", "#E9C46A", "#C95C6A", "#B93E3A", "#F7C6C4"]
COOL = ["#2E2D86", "#4B46B8", "#6A63D8", "#8B7EEA", "#B54BA5"]

def wrap_label(s: str, max_len: int) -> str:
    if len(s) <= max_len:
        return s
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_len:
            cur += " " + w
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    if len(lines) > 2:
        lines = lines[:2]
        lines[-1] = lines[-1][: max(0, max_len - 1)] + "…"
    return "\n".join(lines)

def readable_rotation(deg: float) -> float:
    rot = deg - 90
    if rot < -90:
        rot += 180
    if rot > 90:
        rot -= 180
    return rot

def load_pairs(json_path: Path):
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pairs = [(k, len(v) if isinstance(v, list) else 0) for k, v in data.items()]
    pairs = [(k, v) for k, v in pairs if v > 0]
    if not pairs:
        raise ValueError("All categories have zero length.")
    return pairs

def draw_ring(ax, labels, values, radius, width, colors, start=90.0, label_max_len=18):
    total = sum(values)
    angles = [v / total * 360 for v in values]
    cur = start

    for lab, ang, col in zip(labels, angles, colors):
        theta1 = cur
        theta2 = cur - ang  # clockwise
        mid = (theta1 + theta2) / 2.0
        cur = theta2

        ax.add_patch(Wedge(
            (0, 0),
            r=radius,
            theta1=theta2, theta2=theta1,   # swap to emulate clockwise
            width=width,
            facecolor=col,
            edgecolor="white",
            linewidth=2.2
        ))

        mid_rad = math.radians(mid)
        text_r = radius - width / 2
        x, y = text_r * math.cos(mid_rad), text_r * math.sin(mid_rad)

        lab2 = wrap_label(lab, label_max_len)
        fs = max(7, min(16, 0.20 * ang + 7))
        if "\n" in lab2:
            fs = max(7, fs - 1)

        ax.text(
            x, y, lab2,
            ha="center", va="center",
            color="white",
            fontsize=fs, fontweight="bold",
            rotation=readable_rotation(mid),
            rotation_mode="anchor",
            linespacing=0.9
        )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", default="style_two_ring_clean")
    ap.add_argument("--center", default="Style")
    ap.add_argument("--inner_n", type=int, default=4, help="How many smallest categories go to inner ring (3 or 4 recommended)")
    ap.add_argument("--ring_w", type=float, default=0.24, help="Ring thickness (outer_w=inner_w=ring_w)")
    ap.add_argument("--gap", type=float, default=0.05, help="Gap between outer & inner rings")
    ap.add_argument("--outer_r", type=float, default=1.0, help="Outer ring outer radius")
    args = ap.parse_args()

    pairs = load_pairs(Path(args.json))
    pairs_sorted = sorted(pairs, key=lambda x: x[1])  # small -> large

    inner_n = max(1, min(args.inner_n, len(pairs_sorted) - 1))  # ensure outer ring not empty
    inner = pairs_sorted[:inner_n]
    outer = pairs_sorted[inner_n:]

    inner_labels = [k for k, _ in inner]
    inner_values = [v for _, v in inner]
    outer_labels = [k for k, _ in outer]
    outer_values = [v for _, v in outer]

    # 关键：内外环厚度一致
    outer_w = inner_w = args.ring_w
    outer_r = args.outer_r
    inner_r = outer_r - outer_w - args.gap
    hole_r  = max(0.25, inner_r - inner_w - 0.05)

    outer_colors = [WARM[i % len(WARM)] for i in range(len(outer_labels))]
    inner_colors = [COOL[i % len(COOL)] for i in range(len(inner_labels))]

    fig, ax = plt.subplots(figsize=(7.6, 7.6), dpi=260)
    ax.set_aspect("equal")
    ax.axis("off")

    draw_ring(ax, outer_labels, outer_values, outer_r, outer_w, outer_colors, label_max_len=22)
    draw_ring(ax, inner_labels, inner_values, inner_r, inner_w, inner_colors, label_max_len=18)

    ax.add_artist(plt.Circle((0, 0), hole_r, color="white", zorder=10))
    ax.text(0, 0, args.center, ha="center", va="center",
            fontsize=25, fontweight="bold", color="#111111", zorder=11)

    # 防止“残缺”：固定显示范围，整圆必定完整
    pad = 0.12
    ax.set_xlim(-(outer_r + pad), outer_r + pad)
    ax.set_ylim(-(outer_r + pad), outer_r + pad)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../figures")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    save_path_svg = os.path.join(output_dir, f"{args.out}.svg")
    save_path_png = os.path.join(output_dir, f"{args.out}.png")
    # out = Path(args.out)
    fig.savefig(save_path_png, bbox_inches="tight", facecolor="white")
    fig.savefig(save_path_svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    main()