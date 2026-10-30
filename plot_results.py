"""Create dependency-free SVG charts from policy_summary.csv."""
from pathlib import Path
import csv
import html

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"


def read_summary():
    with (OUT / "policy_summary.csv").open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bar_chart(rows, field, title, filename, maximum=1.0, suffix="%"):
    width, height = 900, 480
    left, right, top, bottom = 230, 35, 70, 75
    plot_w = width - left - right
    plot_h = height - top - bottom
    bar_h = 48
    gap = 25
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}">'.format(width, height, width, height),
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="{}" y="38" font-size="23" font-family="Arial" font-weight="bold">{}</text>'.format(left, html.escape(title)),
    ]
    for tick in range(0, 6):
        value = maximum * tick / 5
        x = left + plot_w * tick / 5
        parts.append('<line x1="{:.1f}" y1="{}" x2="{:.1f}" y2="{}" stroke="#dddddd"/>'.format(x, top, x, top + plot_h))
        parts.append('<text x="{:.1f}" y="{}" text-anchor="middle" font-size="13" font-family="Arial">{:.0f}{}</text>'.format(x, top + plot_h + 24, value * 100 if suffix == "%" else value, suffix))
    for index, row in enumerate(rows):
        value = float(row[field])
        y = top + index * (bar_h + gap) + 8
        bar_w = plot_w * min(max(value, 0.0), maximum) / maximum
        label = row["policy"]
        parts.append('<text x="{}" y="{}" text-anchor="end" font-size="14" font-family="Arial">{}</text>'.format(left - 12, y + 30, html.escape(label)))
        parts.append('<rect x="{}" y="{}" width="{:.1f}" height="{}" fill="#4c78a8"/>'.format(left, y, bar_w, bar_h))
        display = "{:.1f}{}".format(value * 100, "%") if suffix == "%" else "{:.2f}".format(value)
        parts.append('<text x="{:.1f}" y="{}" font-size="14" font-family="Arial">{}</text>'.format(left + bar_w + 8, y + 30, display))
    parts.append("</svg>")
    (OUT / filename).write_text("\n".join(parts), encoding="utf-8")


def main():
    rows = read_summary()
    bar_chart(rows, "attack_success_rate", "Attack success rate (lower is better)", "attack_success_rate.svg")
    bar_chart(rows, "primary_task_completion_rate", "Primary task completion (higher is better)", "task_completion_rate.svg")
    bar_chart(rows, "metadata_operations_per_episode", "Abstract metadata operations per episode", "metadata_operations.svg", maximum=max(1.0, max(float(r["metadata_operations_per_episode"]) for r in rows)), suffix="ops")


if __name__ == "__main__":
    main()
