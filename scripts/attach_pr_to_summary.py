#!/usr/bin/env python3
"""Augment the monthly run summary with PR metadata."""

from __future__ import annotations

import json
import os
from pathlib import Path

SUMMARY = Path(__file__).resolve().parents[1] / ".github" / "last-monthly-run.json"


def main() -> None:
    if not SUMMARY.exists():
        return

    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    pr_url = os.environ.get("PR_URL", "").strip()
    if pr_url:
        data["pull_request_url"] = pr_url
        data["published_via"] = "pull_request"
    else:
        data["published_via"] = "no_pull_request"
    data["publish_step"] = os.environ.get("PUSH_STATUS", "unknown")
    SUMMARY.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
