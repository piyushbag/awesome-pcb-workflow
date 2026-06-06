#!/usr/bin/env python3
"""POST the monthly update summary to a Cursor Automation webhook."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / ".github" / "last-monthly-run.json"


def main() -> int:
    webhook_url = os.environ.get("CURSOR_AUTOMATION_WEBHOOK_URL", "").strip()
    webhook_key = os.environ.get("CURSOR_AUTOMATION_WEBHOOK_KEY", "").strip()

    if not webhook_url:
        print("CURSOR_AUTOMATION_WEBHOOK_URL not set — skipping Cursor notification.")
        return 0

    if not SUMMARY.exists():
        print(f"Missing summary file: {SUMMARY}", file=sys.stderr)
        return 1

    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))

    repo = os.environ.get("GITHUB_REPOSITORY", payload.get("repo", ""))
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    sha = os.environ.get("GITHUB_SHA", "")

    if run_id and repo:
        payload["workflow_run_url"] = f"{server}/{repo}/actions/runs/{run_id}"
    if sha and repo:
        payload["commit_url"] = f"{server}/{repo}/commit/{sha}"

    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "awesome-pcb-workflow-monthly-bot",
    }
    if webhook_key:
        token = webhook_key if webhook_key.lower().startswith("bearer ") else f"Bearer {webhook_key}"
        headers["Authorization"] = token

    request = urllib.request.Request(webhook_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            print(f"Cursor webhook accepted ({response.status}).")
    except urllib.error.HTTPError as exc:
        print(f"Cursor webhook failed: HTTP {exc.code}", file=sys.stderr)
        print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
