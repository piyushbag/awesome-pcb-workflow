# Contributing to Awesome PCB Workflow

Thank you for helping make this the most comprehensive PCB workflow resource on the internet. Every contribution — whether it's a new tool, a correction, or an integration guide — improves the experience for thousands of hardware engineers.

---

## What We're Looking For

This list covers the **complete PCB design workflow**, not just EDA schematic/layout tools. We especially value contributions that:

- Cover underserved workflow stages (requirements, simulation, test automation, DFM, documentation)
- Include **OrCAD integration notes** — how the tool connects to OrCAD Capture, PSpice, or Allegro
- Serve **professional hardware engineers**, not only hobbyists
- Are backed by active maintenance or significant community adoption

---

## How to Add a Tool

### Step 1 — Check if it already exists

Search the README before opening a PR:

```bash
grep -i "tool-name" README.md
```

### Step 2 — Fork and clone

```bash
git clone https://github.com/YOUR-USERNAME/awesome-pcb-workflow.git
cd awesome-pcb-workflow
git checkout -b add/tool-name
```

### Step 3 — Add your entry

Find the correct workflow stage section in `README.md` and add a table row. Follow the exact format:

```markdown
| [🔧 Tool Name](https://github.com/org/repo) | One sentence: what it does and why it matters | OrCAD note or — | MIT |
```

**Rules for the entry:**

- Name: include a relevant emoji, then the tool name, linked to the canonical URL
- Description: one sentence, active voice, says what the tool *does* and *why an engineer would use it*
- OrCAD Integration: how the tool connects to OrCAD (netlist format, API, export method) — or `—` if not applicable
- License: the SPDX license identifier (e.g., `MIT`, `GPL-3.0`, `Apache-2.0`, `Freeware`)

### Step 4 — Commit and open a PR

```bash
git add README.md
git commit -m "Add [Tool Name] to [Stage]"
git push origin add/tool-name
```

Then open a pull request with:

- **Title:** `Add [Tool Name] to [Stage]`
- **Description:** What the tool does, why it belongs here, and any OrCAD integration details

---

## Inclusion Criteria

### ✅ A tool is included

- It is **open-source** (Apache, MIT, GPL, BSD, or equivalent) *or* free-to-use with clearly documented terms
- It is **actively maintained** — at least one commit in the last 18 months — *or* is historically significant (e.g., ngspice, gerbv)
- It is **relevant to professional hardware design** — not just hobbyist breadboard projects
- It **solves a real workflow problem** in schematic, simulation, layout, fab prep, test, or documentation
- It has **working documentation** — a README or docs site that a new user can actually follow

### ❌ A tool is excluded

- It is purely commercial with no meaningful free tier
- It is unmaintained with known breaking bugs and no active fork
- It is a duplicate of an already-listed tool without a clear differentiation
- It is a personal project without any external adoption or documentation
- The submission reads as self-promotion rather than a community recommendation

---

## Updating an Existing Entry

If a tool has changed — new name, new URL, new license, or a better description — open a PR with:

- **Title:** `Update [Tool Name] — [what changed]`
- **Description:** Brief explanation of what changed and why

---

## Adding a Documentation Guide

The `docs/` folder is open for integration guides. If you have hands-on experience with:

- Connecting a specific tool to OrCAD
- A CI/CD workflow for PCB projects
- A test automation setup for hardware
- A migration guide from one tool to another

Add a `.md` file under `docs/` and link it from the relevant section in the README.

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By contributing, you agree to uphold a welcoming, harassment-free environment.

In practice: be constructive in reviews, assume good intent, and focus on the content — not the contributor.

---

## Review Process

All PRs are reviewed by maintainers. Expect a response within **7 days**. PRs that follow the format above and meet inclusion criteria are typically merged quickly. If you don't hear back, feel free to ping with a comment.

---

## Questions?

Open an issue with the label `question` — we're happy to help before you spend time on a PR.
