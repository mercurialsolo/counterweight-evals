#!/usr/bin/env python3
"""Generate lightweight SVG charts from counterweight eval summaries.

No external dependencies required.
"""

from __future__ import annotations

import json
import shutil
import statistics
import subprocess
from pathlib import Path

RUN_IDS = [
    "20260212T225521Z",
    "20260213T003745Z",
    "20260213T004226Z",
]


def load_summary(run_id: str) -> list[dict]:
    path = Path("runs") / run_id / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def collect_stability() -> list[dict]:
    runs = {rid: {(r["provider_model"], r["variant_id"]): r for r in load_summary(rid)} for rid in RUN_IDS}
    keys = sorted(set().union(*[set(d.keys()) for d in runs.values()]))
    rows = []
    for key in keys:
        vals = [runs[rid][key] for rid in RUN_IDS]
        rank_mean = statistics.mean(v["rank_score"] for v in vals)
        rank_sd = statistics.pstdev(v["rank_score"] for v in vals)
        overall_mean = statistics.mean(v["overall_100"] for v in vals)
        harmful_mean = statistics.mean(v["harmful_agreement_rate"] for v in vals)
        rows.append(
            {
                "model": key[0],
                "variant": key[1],
                "rank_mean": rank_mean,
                "rank_sd": rank_sd,
                "overall_mean": overall_mean,
                "harmful_mean": harmful_mean,
                "label": f"{key[0].replace('openai:', '').replace('anthropic:', '')} | {key[1]}",
            }
        )
    rows.sort(key=lambda x: (-x["rank_mean"], x["harmful_mean"], x["rank_sd"]))
    return rows


def collect_variant_deltas(stability_rows: list[dict]) -> list[dict]:
    by_model: dict[str, dict[str, float]] = {}
    for row in stability_rows:
        by_model.setdefault(row["model"], {})[row["variant"]] = row["overall_mean"]

    out = []
    for model, vals in by_model.items():
        baseline = vals.get("baseline-helpful", 0.0)
        for variant in ("counterweight-v1", "counterweight-v2-failure-aware"):
            if variant in vals:
                out.append(
                    {
                        "label": f"{model.replace('openai:', '').replace('anthropic:', '')} | {variant}",
                        "delta": vals[variant] - baseline,
                    }
                )
    out.sort(key=lambda x: x["delta"], reverse=True)
    return out


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def render_horizontal_bar_svg(
    rows: list[dict],
    value_key: str,
    title: str,
    filename: str,
    width: int = 1400,
    row_height: int = 34,
    left_pad: int = 520,
    right_pad: int = 120,
    top_pad: int = 80,
    bottom_pad: int = 30,
    color: str = "#2c7be5",
) -> None:
    max_val = max(r[value_key] for r in rows) if rows else 1.0
    chart_w = width - left_pad - right_pad
    height = top_pad + bottom_pad + row_height * len(rows)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '.title { font: 700 24px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #111827; }',
        '.label { font: 13px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #111827; }',
        '.value { font: 12px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #1f2937; }',
        ".grid { stroke: #e5e7eb; stroke-width: 1; }",
        "</style>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text class="title" x="24" y="40">{esc(title)}</text>',
    ]

    # x grid lines
    for step in range(0, 6):
        x = left_pad + (chart_w * step / 5)
        lines.append(f'<line class="grid" x1="{x:.1f}" y1="{top_pad-10}" x2="{x:.1f}" y2="{height-bottom_pad}" />')

    for i, row in enumerate(rows):
        y = top_pad + i * row_height
        bar_h = 20
        v = row[value_key]
        bar_w = (v / max_val) * chart_w if max_val > 0 else 0
        lines.append(
            f'<text class="label" x="{left_pad-10}" y="{y + 14}" text-anchor="end">{esc(row["label"])}</text>'
        )
        lines.append(
            f'<rect x="{left_pad}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" fill="{color}" rx="4" ry="4" />'
        )
        lines.append(
            f'<text class="value" x="{left_pad + bar_w + 8:.1f}" y="{y + 14}">{v:.2f}</text>'
        )

    lines.append("</svg>")
    out = Path("figures")
    out.mkdir(parents=True, exist_ok=True)
    (out / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_variant_delta_svg(rows: list[dict], filename: str) -> None:
    # Support negatives if present.
    width = 1400
    row_height = 34
    left_pad = 560
    right_pad = 120
    top_pad = 80
    bottom_pad = 30
    chart_w = width - left_pad - right_pad
    height = top_pad + bottom_pad + row_height * len(rows)

    min_val = min([r["delta"] for r in rows] + [0.0])
    max_val = max([r["delta"] for r in rows] + [0.0])
    span = max_val - min_val if max_val != min_val else 1.0

    def x_for(v: float) -> float:
        return left_pad + ((v - min_val) / span) * chart_w

    zero_x = x_for(0.0)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        '.title { font: 700 24px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #111827; }',
        '.label { font: 13px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #111827; }',
        '.value { font: 12px -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; fill: #1f2937; }',
        ".grid { stroke: #e5e7eb; stroke-width: 1; }",
        ".zero { stroke: #6b7280; stroke-width: 2; }",
        "</style>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text class="title" x="24" y="40">Variant Lift vs Baseline (Mean Overall Δ)</text>',
        f'<line class="zero" x1="{zero_x:.1f}" y1="{top_pad-10}" x2="{zero_x:.1f}" y2="{height-bottom_pad}" />',
    ]

    for i, row in enumerate(rows):
        y = top_pad + i * row_height
        bar_h = 20
        x0 = min(zero_x, x_for(row["delta"]))
        x1 = max(zero_x, x_for(row["delta"]))
        color = "#059669" if row["delta"] >= 0 else "#dc2626"
        lines.append(
            f'<text class="label" x="{left_pad-10}" y="{y + 14}" text-anchor="end">{esc(row["label"])}</text>'
        )
        lines.append(f'<rect x="{x0:.1f}" y="{y}" width="{max(1.0, x1-x0):.1f}" height="{bar_h}" fill="{color}" rx="4" ry="4" />')
        lines.append(f'<text class="value" x="{x1 + 8:.1f}" y="{y + 14}">{row["delta"]:+.2f}</text>')

    lines.append("</svg>")
    out = Path("figures")
    out.mkdir(parents=True, exist_ok=True)
    (out / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_png_from_svg(svg_name: str, png_name: str, width: int = 1600) -> None:
    """Render PNG with preserved aspect ratio when rsvg-convert is available."""
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        return
    out = Path("figures")
    svg_path = out / svg_name
    png_path = out / png_name
    subprocess.run(
        [rsvg, "-w", str(width), str(svg_path), "-o", str(png_path)],
        check=True,
    )


def main() -> None:
    rows = collect_stability()
    render_horizontal_bar_svg(
        rows,
        value_key="rank_mean",
        title="Stable Ranking (Mean Rank Score Across 3 Judge Passes)",
        filename="stable_ranking.svg",
        color="#1d4ed8",
    )
    render_horizontal_bar_svg(
        rows,
        value_key="harmful_mean",
        title="Mean Harmful Agreement Rate (Lower is Better)",
        filename="harmful_rate.svg",
        color="#b91c1c",
    )
    deltas = collect_variant_deltas(rows)
    render_variant_delta_svg(deltas, "variant_lift.svg")
    # Optional PNG exports (for better embedding support in some tools).
    render_png_from_svg("stable_ranking.svg", "stable_ranking.png")
    render_png_from_svg("harmful_rate.svg", "harmful_rate.png")
    render_png_from_svg("variant_lift.svg", "variant_lift.png")
    print(
        "Wrote figures/stable_ranking.svg, figures/harmful_rate.svg, "
        "figures/variant_lift.svg and PNGs when rsvg-convert is installed"
    )


if __name__ == "__main__":
    main()
