#!/usr/bin/env python3
"""Build docs/star-history.svg from GitHub stargazer timestamps."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "star-history.svg"
DEFAULT_REPO = "piyushbag/awesome-pcb-workflow"


def fetch_stargazers(owner: str, repo: str, token: str) -> list[datetime]:
    stars: list[datetime] = []
    page = 1

    while True:
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        url = f"https://api.github.com/repos/{owner}/{repo}/stargazers?{query}"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.v3.star+json",
                "User-Agent": "awesome-pcb-workflow-star-history",
            },
        )
        if token:
            request.add_header("Authorization", f"Bearer {token}")

        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.loads(response.read())

        if not batch:
            break

        for item in batch:
            starred_at = datetime.fromisoformat(
                item["starred_at"].replace("Z", "+00:00")
            )
            stars.append(starred_at)

        if len(batch) < 100:
            break
        page += 1

    stars.sort()
    return stars


def _format_date(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d")


def render_svg(repo: str, star_times: list[datetime]) -> str:
    width, height = 800, 420
    margin = {"top": 56, "right": 36, "bottom": 64, "left": 64}
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    if not star_times:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="Star history for {repo}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="50%" y="50%" text-anchor="middle" fill="#666" font-family="sans-serif" font-size="16">No stars yet</text>
</svg>
"""

    points: list[tuple[datetime, int]] = [
        (star_times[0], 1),
        *[(star_time, index + 1) for index, star_time in enumerate(star_times[1:], start=1)],
    ]
    min_time = points[0][0]
    max_time = points[-1][0]
    max_count = points[-1][1]
    y_max = max(max_count, 1)

    def x_pos(value: datetime) -> float:
        if max_time == min_time:
            return margin["left"] + plot_w / 2
        elapsed = (value - min_time).total_seconds()
        total = (max_time - min_time).total_seconds()
        return margin["left"] + (elapsed / total) * plot_w

    def y_pos(count: int) -> float:
        return margin["top"] + plot_h - (count / y_max) * plot_h

    polyline = " ".join(
        f"{x_pos(star_time):.1f},{y_pos(count):.1f}" for star_time, count in points
    )
    area = (
        f"M{margin['left']},{margin['top'] + plot_h} "
        + polyline.replace(" ", " L", 1)
        + f" L{x_pos(max_time):.1f},{margin['top'] + plot_h} Z"
    )

    y_ticks = sorted({1, y_max, max(1, y_max // 2)} if y_max > 2 else {1, y_max})
    y_tick_svg = "\n".join(
        f'  <line x1="{margin["left"]}" y1="{y_pos(tick):.1f}" x2="{margin["left"] + plot_w}" y2="{y_pos(tick):.1f}" stroke="#e5e7eb" stroke-width="1"/>'
        f'\n  <text x="{margin["left"] - 10}" y="{y_pos(tick):.1f}" text-anchor="end" dominant-baseline="middle" fill="#666" font-family="sans-serif" font-size="12">{tick}</text>'
        for tick in y_ticks
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="Star history for {repo}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="50%" y="28" text-anchor="middle" fill="#111827" font-family="sans-serif" font-size="20" font-weight="700">Star History</text>
  <text x="50%" y="48" text-anchor="middle" fill="#6b7280" font-family="sans-serif" font-size="13">{repo} · {_format_date(min_time)} to {_format_date(max_time)}</text>
  <rect x="{margin['left']}" y="{margin['top']}" width="{plot_w}" height="{plot_h}" fill="#fafafa" stroke="#d1d5db" stroke-width="1"/>
{y_tick_svg}
  <path d="{area}" fill="#fee2e2" opacity="0.65"/>
  <polyline points="{polyline}" fill="none" stroke="#dd4528" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="{x_pos(max_time):.1f}" cy="{y_pos(max_count):.1f}" r="4.5" fill="#dd4528"/>
  <text x="{x_pos(max_time):.1f}" y="{y_pos(max_count) - 12:.1f}" text-anchor="middle" fill="#111827" font-family="sans-serif" font-size="12" font-weight="600">{max_count} stars</text>
  <text x="{margin['left'] + plot_w / 2:.1f}" y="{height - 18}" text-anchor="middle" fill="#374151" font-family="sans-serif" font-size="13">Date (UTC)</text>
  <text x="18" y="{margin['top'] + plot_h / 2:.1f}" text-anchor="middle" fill="#374151" font-family="sans-serif" font-size="13" transform="rotate(-90 18 {margin['top'] + plot_h / 2:.1f})">GitHub Stars</text>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if "/" not in args.repo:
        print("Expected --repo in owner/name form.", file=sys.stderr)
        return 1

    owner, repo = args.repo.split("/", 1)
    token = os.environ.get("GITHUB_TOKEN", "")

    try:
        star_times = fetch_stargazers(owner, repo, token)
    except urllib.error.HTTPError as error:
        print(f"GitHub API error: {error.code} {error.reason}", file=sys.stderr)
        return 1

    svg = render_svg(args.repo, star_times)

    if args.dry_run:
        print(svg)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Wrote {args.output} ({len(star_times)} stars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
