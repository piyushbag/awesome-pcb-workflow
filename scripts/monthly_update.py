#!/usr/bin/env python3
"""Monthly README updater for awesome-pcb-workflow.

Discovers new open-source PCB workflow tools via the GitHub API, appends
qualifying entries to README.md, rotates the Featured This Month section,
and records featured-tool history for cooldown tracking.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CONFIG = ROOT / ".github" / "discovery-config.json"
HISTORY = ROOT / ".github" / "featured-history.json"

TABLE_ROW = re.compile(
    r"^\|\s*\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)\s*\|\s*(?P<desc>[^|]+)\|"
)
TOOL_NAME = re.compile(
    r"^[\s\W\d_"
    r"\U0001F300-\U0001FAFF"
    r"\U00002600-\U000027BF"
    r"]*(?P<name>.+)$"
)

DENY_NAME_FRAGMENTS = (
    "mirror",
    "awesome-",
    "awesome_",
    "dotfiles",
    "interview",
    "leetcode",
    "bootcamp",
    "tutorial-only",
)

DENY_REPO_NAMES = {
    "kicad-source-mirror",
    "kicad",
    "librepcb",
    "ngspice",
    "horizon",
}
GITHUB_REPO = re.compile(r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/\s)]+)")

EMOJI_KEYWORDS = [
    (("spice", "simulation", "circuit"), "⚡"),
    (("gerber", "fabrication", "fab"), "🏭"),
    (("test", "measure", "instrument"), "🧪"),
    (("rf", "microwave", "signal"), "📡"),
    (("bom", "component", "inventory"), "📦"),
    (("layout", "router", "routing", "pcb"), "🖥"),
    (("ai", "ml", "agent", "automation"), "🤖"),
    (("python",), "🐍"),
    (("kicad",), "🟦"),
]

LICENSE_ALIASES = {
    "MIT": "MIT",
    "Apache-2.0": "Apache-2.0",
    "GPL-3.0": "GPL-3.0",
    "GPL-3.0-only": "GPL-3.0",
    "GPL-2.0": "GPL-2.0",
    "GPL-2.0-only": "GPL-2.0",
    "BSD-3-Clause": "BSD",
    "BSD-2-Clause": "BSD",
    "MPL-2.0": "MPL-2.0",
    "AGPL-3.0": "AGPL-3.0",
    "AGPL-3.0-only": "AGPL-3.0",
    "LGPL-2.1": "LGPL-2.1",
    "LGPL-2.1-only": "LGPL-2.1",
    "EUPL-1.2": "EUPL-1.2",
}


@dataclass
class ToolEntry:
    label: str
    name: str
    url: str
    description: str
    section: str
    emoji: str = "🔧"

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")


def github_request(path: str, token: str) -> dict | list:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "awesome-pcb-workflow-monthly-bot",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def pick_emoji(text: str) -> str:
    lower = text.lower()
    for keywords, emoji in EMOJI_KEYWORDS:
        if any(k in lower for k in keywords):
            return emoji
    return "🔧"


def clean_description(text: str, max_len: int = 120) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return "Open-source tool for hardware design workflows."
    if text[-1] not in ".!?":
        text += "."
    if len(text) > max_len:
        text = text[: max_len - 3].rsplit(" ", 1)[0] + "..."
    return text


def extract_tool_name(label: str) -> str:
    match = TOOL_NAME.match(label.strip())
    return match.group("name").strip() if match else label.strip()


def tool_names_in_readme(content: str) -> set[str]:
    names: set[str] = set()
    for tool in parse_readme_tools(content):
        names.add(tool.name.lower())
        names.add(re.sub(r"[^a-z0-9]+", "", tool.name.lower()))
    return names


def is_name_duplicate(repo_name: str, readme_names: set[str]) -> bool:
    normalized = repo_name.lower().replace("-", "").replace("_", "")
    compact = re.sub(r"[^a-z0-9]+", "", repo_name.lower())
    for existing in readme_names:
        existing_compact = re.sub(r"[^a-z0-9]+", "", existing)
        if (
            repo_name.lower() == existing
            or normalized == existing_compact
            or compact == existing_compact
            or repo_name.lower() in existing
            or existing in repo_name.lower()
        ):
            return True
    return False


def normalize_repo_key(url: str) -> str | None:
    match = GITHUB_REPO.search(url)
    if not match:
        return None
    return f"{match.group('owner').lower()}/{match.group('repo').lower().removesuffix('.git')}"


def parse_readme_tools(content: str) -> list[ToolEntry]:
    tools: list[ToolEntry] = []
    current_section = "Unknown"

    for line in content.splitlines():
        if line.startswith("### "):
            current_section = line.removeprefix("### ").strip()
            continue
        if line.startswith("#### "):
            current_section = line.removeprefix("#### ").strip()
            continue

        match = TABLE_ROW.match(line)
        if not match:
            continue

        label = match.group("label").strip()
        name = extract_tool_name(label)
        emoji = label[: len(label) - len(name)].strip() if name in label else "🔧"
        tools.append(
            ToolEntry(
                label=label,
                name=name,
                url=match.group("url").strip(),
                description=match.group("desc").strip(),
                section=current_section,
                emoji=emoji or "🔧",
            )
        )

    return tools


def existing_repo_keys(content: str) -> set[str]:
    keys: set[str] = set()
    for tool in parse_readme_tools(content):
        key = normalize_repo_key(tool.url)
        if key:
            keys.add(key)
        keys.add(tool.name.lower())
    return keys


def recent_featured_names(history: dict, months: int) -> set[str]:
    featured = history.get("featured", [])
    return {name.lower() for entry in featured[-months:] for name in entry.get("tools", [])}


def search_repositories(query: str, token: str, per_page: int = 15) -> list[dict]:
    params = urllib.parse.urlencode(
        {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    )
    data = github_request(f"/search/repositories?{params}", token)
    return data.get("items", [])


def description_matches_keywords(text: str, search_cfg: dict) -> bool:
    lower = text.lower()
    keywords = search_cfg.get("description_keywords", [])
    required = search_cfg.get("require_any_keywords", [])
    excluded = search_cfg.get("exclude_description_keywords", [])
    if any(keyword in lower for keyword in excluded):
        return False
    groups = search_cfg.get("require_all_keyword_groups", [])
    if groups and not all(any(keyword in lower for keyword in group) for group in groups):
        return False
    if required and not any(keyword in lower for keyword in required):
        return False
    if not keywords:
        return True
    return any(keyword in lower for keyword in keywords)


def repo_qualifies(
    repo: dict,
    min_stars: int,
    known: set[str],
    readme_names: set[str],
    search_cfg: dict,
) -> bool:
    if repo.get("archived") or repo.get("disabled") or repo.get("fork"):
        return False
    if repo.get("stargazers_count", 0) < min_stars:
        return False
    if not repo.get("license"):
        return False
    if not repo.get("description"):
        return False

    repo_name = repo.get("name", "")
    full_name = repo.get("full_name", "").lower()
    description = (repo.get("description") or "").lower()

    if repo_name.lower() in DENY_REPO_NAMES:
        return False
    if any(fragment in repo_name.lower() for fragment in DENY_NAME_FRAGMENTS):
        return False
    if any(fragment in full_name for fragment in DENY_NAME_FRAGMENTS):
        return False
    if "mirror" in description and "source" in description:
        return False
    keywords = search_cfg.get("description_keywords", [])
    if keywords and not description_matches_keywords(description, search_cfg):
        return False
    if is_name_duplicate(repo_name, readme_names):
        return False

    if full_name in known:
        return False
    html_url = repo.get("html_url", "")
    if normalize_repo_key(html_url) in known:
        return False
    return True


def format_license(spdx: str | None) -> str | None:
    if not spdx:
        return None
    return LICENSE_ALIASES.get(spdx, spdx)


def build_row(repo: dict, search_cfg: dict) -> str:
    name = repo["name"]
    if "-" in name and name.islower():
        # Title-case hyphenated repos (kicad-happy -> Kicad-Happy)
        name = "-".join(part.capitalize() for part in name.split("-"))

    emoji = pick_emoji(f"{repo['name']} {repo.get('description', '')}")
    desc = clean_description(repo.get("description", ""))
    license_id = format_license(repo.get("license", {}).get("spdx_id"))
    url = repo["html_url"]
    cols = search_cfg.get("table_columns", 3)

    if cols == 4 and "best_for_default" in search_cfg:
        return f"| [{emoji} {name}]({url}) | {desc} | {search_cfg['best_for_default']} | {license_id} |"
    if cols == 4:
        orcad = search_cfg.get("orcad_default", "—")
        return f"| [{emoji} {name}]({url}) | {desc} | {orcad} | {license_id} |"
    return f"| [{emoji} {name}]({url}) | {desc} | {license_id} |"


def insert_row_in_section(content: str, section_heading: str, row: str) -> str:
    lines = content.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.strip() == section_heading:
            start = i
            break
    if start is None:
        return content

    table_end = None
    in_table = False
    for i in range(start + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("|") and not in_table:
            in_table = True
            continue
        if in_table and not stripped.startswith("|"):
            table_end = i
            break

    if table_end is None:
        return content

    if row.strip() in content:
        return content

    lines.insert(table_end, row + "\n")
    return "".join(lines)


def featured_identity(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower().split()[0])


def select_featured_tools(
    tools: list[ToolEntry],
    config: dict,
    history: dict,
    exclude_names: set[str] | None = None,
) -> list[tuple[ToolEntry, dict]]:
    cooldown = config.get("cooldown_months", 6)
    groups = config.get("featured_stage_groups", {})
    selected: list[tuple[ToolEntry, dict]] = []
    blocked = recent_featured_names(history, cooldown)
    if exclude_names:
        blocked |= {name.lower() for name in exclude_names}
    used_identities: set[str] = set()

    for group_cfg in groups.values():
        keywords = group_cfg.get("section_keywords", [])
        candidates = [
            t
            for t in tools
            if any(kw in t.section for kw in keywords)
            and t.name.lower() not in blocked
            and len(t.name) >= 3
            and len(t.description) >= 20
            and featured_identity(t.name) not in used_identities
            and all(t.name.lower() != s[0].name.lower() for s in selected)
        ]
        if not candidates:
            candidates = [
                t
                for t in tools
                if t.name.lower() not in blocked
                and featured_identity(t.name) not in used_identities
                and all(t.name.lower() != s[0].name.lower() for s in selected)
            ]
        if candidates:
            candidates.sort(
                key=lambda t: (
                    t.name.lower() in blocked,
                    "github.com" not in t.url,
                    -len(t.description),
                )
            )
            pick = candidates[0]
            selected.append((pick, group_cfg))
            blocked.add(pick.name.lower())
            used_identities.add(featured_identity(pick.name))

    return selected[:5]


def featured_description(tool: ToolEntry) -> str:
    desc = tool.description.strip()
    if desc.endswith("."):
        return desc
    return desc + "."


def update_featured_section(content: str, featured: list[tuple[ToolEntry, dict]]) -> str:
    header = "## 🔥 Featured This Month"
    footer = "> 📬 **Watch this repo**"
    start = content.index(header)
    end = content.index(footer, start)

    rows = [
        "| Tool               | What it does                                                                         | Stage                                          |",
        "| ------------------ | ------------------------------------------------------------------------------------ | ---------------------------------------------- |",
    ]
    for tool, group in featured:
        stage_link = f"[{group['label']}]({group['anchor']})"
        label = f"{tool.emoji} {tool.name}".strip()
        desc = featured_description(tool)
        rows.append(f"| {label} | {desc} | {stage_link} |")

    block = header + "\n\n" + "\n".join(rows) + "\n\n"
    return content[:start] + block + content[end:]


def discover_new_tools(content: str, config: dict, token: str) -> tuple[str, list[str]]:
    known = existing_repo_keys(content)
    readme_names = tool_names_in_readme(content)
    min_stars = config.get("min_stars", 25)
    max_new = config.get("max_new_tools_per_month", 5)
    added: list[str] = []

    for search_cfg in config.get("searches", []):
        if len(added) >= max_new:
            break

        queries = [
            f"{search_cfg['query']} NOT mirror in:name NOT awesome in:name",
        ]
        for topic in search_cfg.get("topics", []):
            queries.append(
                f"topic:{topic} stars:>{min_stars} pushed:>2024-01-01 NOT mirror in:name NOT awesome in:name"
            )

        seen_queries: set[str] = set()
        for query in queries:
            if query in seen_queries:
                continue
            seen_queries.add(query)

            try:
                repos = search_repositories(query, token)
            except urllib.error.HTTPError as exc:
                print(f"Search failed for '{query}': {exc}", file=sys.stderr)
                continue

            for repo in repos:
                if len(added) >= max_new:
                    break
                if not repo_qualifies(repo, min_stars, known, readme_names, search_cfg):
                    continue

                row = build_row(repo, search_cfg)
                section = search_cfg["section_heading"]
                updated = insert_row_in_section(content, section, row)
                if updated == content:
                    continue

                content = updated
                full_name = repo["full_name"]
                known.add(full_name.lower())
                known.add(normalize_repo_key(repo["html_url"]) or full_name.lower())
                readme_names.add(repo["name"].lower())
                readme_names.add(re.sub(r"[^a-z0-9]+", "", repo["name"].lower()))
                added.append(full_name)
                print(f"Added {full_name} to {section}")

    return content, added


def run(dry_run: bool = False) -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 1

    config = load_json(CONFIG)
    history = load_json(HISTORY)
    content = README.read_text(encoding="utf-8")
    original = content

    content, added = discover_new_tools(content, config, token)
    tools = parse_readme_tools(content)
    added_names = {a.split("/")[-1] for a in added}
    featured = select_featured_tools(tools, config, history, exclude_names=added_names)
    content = update_featured_section(content, featured)

    now = datetime.now(timezone.utc)
    month_key = now.strftime("%Y-%m")
    history.setdefault("featured", [])
    history["featured"] = [e for e in history["featured"] if e.get("month") != month_key]
    history["featured"].append(
        {
            "month": month_key,
            "tools": [tool.name for tool, _ in featured],
            "added_repos": added,
        }
    )

    if content == original and not added:
        print("No changes needed.")
        return 0

    print("Featured tools:", ", ".join(tool.name for tool, _ in featured))
    if added:
        print("New tools added:", ", ".join(added))

    if dry_run:
        print("\n--- README diff preview (first 80 lines) ---")
        for line in content.splitlines()[:80]:
            print(line)
        return 0

    README.write_text(content, encoding="utf-8")
    save_json(HISTORY, history)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Monthly awesome-pcb-workflow updater")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()
    raise SystemExit(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
