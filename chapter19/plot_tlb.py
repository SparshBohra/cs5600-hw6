#!/usr/bin/env python3
"""Plot tlb_results.txt. Uses matplotlib if it imports, else writes SVG."""
import math
import re
import sys


def load(path):
    pages = []
    ns = []
    with open(path) as f:
        for line in f:
            m = re.search(r"pages=(\d+).*ns_per_access=([0-9.]+)", line)
            if m:
                pages.append(int(m.group(1)))
                ns.append(float(m.group(2)))
    return pages, ns


def write_svg(pages, ns, out, title):
    W, H = 640, 420
    L, R, T, B = 70, 20, 40, 50
    pw, ph = W - L - R, H - T - B
    xmin, xmax = math.log(min(pages), 2), math.log(max(pages), 2)
    ymin, ymax = 0.0, max(ns) * 1.15

    def x(p):
        return L + (math.log(p, 2) - xmin) / (xmax - xmin) * pw

    def y(v):
        return T + ph - (v - ymin) / (ymax - ymin) * ph

    ticks = [1, 4, 16, 64, 256, 1024, 4096]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H),
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="%d" y="24" font-size="16" font-family="sans-serif">%s</text>'
        % (W // 2 - 120, title),
        '<text x="12" y="%d" font-size="12" font-family="sans-serif" transform="rotate(-90 14 %d)">Time Per Access (ns)</text>'
        % (H // 2, H // 2),
        '<text x="%d" y="%d" font-size="12" font-family="sans-serif">Number Of Pages</text>'
        % (W // 2 - 50, H - 10),
        '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#333"/>'
        % (L, T, pw, ph),
    ]
    for t in ticks:
        if t < min(pages) or t > max(pages):
            continue
        px = x(t)
        parts.append(
            '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#ddd"/>' % (px, T, px, T + ph)
        )
        parts.append(
            '<text x="%.1f" y="%d" font-size="11" text-anchor="middle" font-family="sans-serif">%d</text>'
            % (px, T + ph + 16, t)
        )
    for v in range(0, int(ymax) + 2, 2):
        py = y(v)
        parts.append(
            '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee"/>' % (L, py, L + pw, py)
        )
        parts.append(
            '<text x="%d" y="%.1f" font-size="11" text-anchor="end" font-family="sans-serif">%d</text>'
            % (L - 8, py + 4, v)
        )
    d = "M " + " L ".join("%.1f %.1f" % (x(p), y(v)) for p, v in zip(pages, ns))
    parts.append('<path d="%s" fill="none" stroke="#1f4e79" stroke-width="2"/>' % d)
    for p, v in zip(pages, ns):
        parts.append(
            '<circle cx="%.1f" cy="%.1f" r="3.5" fill="#1f4e79"/>' % (x(p), y(v))
        )
    parts.append("</svg>")
    with open(out, "w") as f:
        f.write("\n".join(parts))
    print("wrote", out)


def main():
    if len(sys.argv) < 3:
        print("usage: plot_tlb.py data.txt out.png-or-svg [title]")
        return 1
    pages, ns = load(sys.argv[1])
    title = sys.argv[3] if len(sys.argv) > 3 else "TLB Size Measurement"
    out = sys.argv[2]
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        plt.figure(figsize=(6, 4))
        plt.plot(pages, ns, marker="o")
        plt.xscale("log", base=2)
        plt.xlabel("Number Of Pages")
        plt.ylabel("Time Per Access (ns)")
        plt.title(title)
        plt.grid(True, which="both", linestyle=":")
        plt.tight_layout()
        plt.savefig(out, dpi=150)
        print("wrote", out)
        return 0
    except Exception as e:
        print("matplotlib unavailable (%s), writing svg" % e)
        if not out.endswith(".svg"):
            out = out.rsplit(".", 1)[0] + ".svg"
        write_svg(pages, ns, out, title)
        return 0


if __name__ == "__main__":
    sys.exit(main())
