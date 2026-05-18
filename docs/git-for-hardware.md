# Git for Hardware — PCB Version Control Guide

Software engineers take git for granted. Hardware engineers often don't use it at all, or use it wrong and end up with a repo of opaque binary blobs that can't be diffed, reviewed, or merged. This guide covers the right way to version-control a PCB project — from daily workflow to CI/CD pipeline.

---

## Why Git for PCB?

| Without Git | With Git |
|---|---|
| `design_v3_FINAL_use_this_one.dsn` | Clean commit history with meaningful messages |
| Email attachments for design reviews | Pull request with inline schematic diff |
| No record of why a component changed | Blame shows who changed R47 and why |
| Manual change logs | Automatic changelog from commits |
| One engineer's laptop = source of truth | Every engineer has full history |

---

## What to Commit

### ✅ Always commit

| File type | Why |
|---|---|
| KiCad `.kicad_sch`, `.kicad_pcb` | Main design files — ASCII, line-diffable |
| OrCAD `.dsn` (saved as ASCII) | Schematic source |
| `.kicad_pro` project file | Links schematic to PCB |
| Netlist `.net` | The connectivity bridge |
| BOM `.csv` | Reproducible part lists |
| `kibot.yaml` / `.kibot.yaml` | CI/CD configuration |
| `README.md` | Project overview and setup instructions |
| Fab notes, design notes `.md` | Engineering decisions and constraints |
| `requirements.txt` | Python toolchain versions |

### ⚠️ Commit with care

| File type | Guidance |
|---|---|
| Gerber files | Commit to a `fab/` folder **tagged to a board revision** only, not on every push |
| STEP / 3D files `.step` | Large binaries — use [Git LFS](https://git-lfs.github.com/) |
| Component library `.kicad_sym` | Commit if custom; use submodule for shared org library |
| Simulation results | Only commit final validated results, not every run |

### ❌ Never commit

```gitignore
# OrCAD build artifacts
*.bak
*.lck
*.DRC
*.log
*.err
allegro/

# KiCad build artifacts
*.000
fp-info-cache
_autosave-*
*.bck
*.kicad_pcb-bak
*.kicad_sch-bak

# Gerber/drill — use tagged releases instead
# (comment this out if your workflow intentionally commits Gerbers)
# *.gbr
# *.drl
# *.gtl *.gbl *.gts *.gbs *.gto *.gbo

# Python
__pycache__/
*.pyc
*.pyo
.env
venv/

# OS cruft
.DS_Store
Thumbs.db
desktop.ini

# Large binaries (use Git LFS for these)
*.step
*.stp
*.wrl
```

Save this as `.gitignore` in the repo root.

---

## Repository Structure

A clean PCB project repository:

```text
project-name/
├── README.md                   # Project overview, specs, fab notes
├── .gitignore
├── requirements.txt            # Python tools
├── kibot.yaml                  # CI/CD configuration (KiBot)
│
├── hardware/                   # All EDA source files
│   ├── project-name.kicad_pro
│   ├── project-name.kicad_sch
│   ├── project-name.kicad_pcb
│   └── libs/                   # Custom component library
│       ├── project-name.kicad_sym
│       └── project-name.pretty/ (footprints)
│
├── simulation/                 # SPICE and SI files
│   ├── power_supply.cir
│   ├── filter_response.cir
│   └── results/
│       └── filter_response.png
│
├── docs/                       # Engineering docs and design decisions
│   ├── design-spec.md
│   ├── bom.csv
│   └── change-log.md
│
├── fab/                        # Fabrication outputs (commit at release only)
│   └── v1.0/
│       ├── gerbers/
│       ├── bom-for-assembly.csv
│       └── fab-notes.md
│
└── test/                       # Test scripts and results
    ├── board-test.py
    └── results/
```

---

## Commit Message Format

Good commit messages make the history useful when you're debugging a hardware issue six months later.

**Format:**

```text
[stage] Short description (what changed)

Why: Reason for the change (design decision, ECO, bug fix)
Impact: What this affects (net, component, layer, etc.)
```

**Examples:**

```text
[schematic] Replace U3 LDO from LM7805 to TPS7A4700

Why: LM7805 has insufficient PSRR for ADC supply — measured 45dB at
     10kHz, need >80dB. TPS7A4700 spec is 82dB at 10kHz.
Impact: VCC_ADC net, C12/C13 bypass capacitors resized to match TPS7A
        recommended values.
```

```text
[layout] Move U3 closer to C12/C13 — reduce bypass cap trace length

Why: Previous placement had 8mm trace to bypass caps, causing
     resonance at ~200MHz visible in spectrum. Moved to <1mm.
Impact: U3, C12, C13 placement, VCC_ADC polygon pour updated.
```

```text
[fab] Tag v2.1 release — ordered from JLCPCB 2026-05-17

Why: ECO-007 incorporated (R47 value corrected to 4.7k)
Impact: Gerbers in fab/v2.1/
```

---

## Branch Strategy for Hardware Teams

```text
main          ← Always reflects the last fabricated, validated board revision
│
├── dev       ← Active development, may not be fab-ready
│   ├── feature/add-usb-c-charging
│   ├── fix/r47-wrong-value
│   └── experiment/rf-matching-network
│
└── release/v2.1   ← Tagged at fab time, frozen
```

**Rules:**

- `main` is only updated when a board revision has been fabricated and validated
- Every fab order gets a `git tag` — `git tag v2.1 && git push origin v2.1`
- Engineers work on `dev` or feature branches, never directly on `main`
- PRs from `dev → main` include a review checklist (DRC passing, BOM correct, fab notes complete)

---

## CI/CD with KiBot

KiBot automatically generates Gerbers, BOM, drill files, schematic PDFs, and 3D renders on every push. Set it up with GitHub Actions:

**`.github/workflows/hardware-ci.yml`:**

```yaml
name: PCB Hardware CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  fabrication-outputs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run KiBot
        uses: INTI-CMNB/KiBot@v2_k8
        with:
          config: kibot.yaml
          schema: hardware/project-name.kicad_sch
          board: hardware/project-name.kicad_pcb

      - name: Upload fab outputs
        uses: actions/upload-artifact@v4
        with:
          name: fab-outputs
          path: fab/

      - name: Upload BOM
        uses: actions/upload-artifact@v4
        with:
          name: bom
          path: docs/bom.*
```

**`kibot.yaml`** (minimal example):

```yaml
kibot:
  version: 1

outputs:
  - name: gerbers
    comment: "Production Gerber files"
    type: gerber
    dir: fab/gerbers
    options:
      use_protel_extensions: true

  - name: drill
    comment: "Excellon drill files"
    type: excellon
    dir: fab/gerbers

  - name: bom
    comment: "Bill of Materials"
    type: bom
    dir: docs
    options:
      format: CSV
      columns:
        - field: Reference
        - field: Value
        - field: Footprint
        - field: Quantity Per PCB

  - name: schematic_pdf
    comment: "Schematic PDF for review"
    type: pdf_schematic
    dir: docs

  - name: ibom
    comment: "Interactive BOM"
    type: ibom
    dir: docs
```

---

## Diffing Schematic Changes

KiCad's `.kicad_sch` files are plain text. You can diff them directly:

```bash
git diff HEAD~1 hardware/project-name.kicad_sch
```

For visual diffs, use the [KiCad-Diff](https://github.com/Gasman2014/KiCad-Diff) tool:

```bash
pip install kidiff
kidiff hardware/project-name.kicad_sch
```

This generates a side-by-side image diff of the schematic — useful in PR reviews.

---

## Release Workflow (When You Order Boards)

```bash
# 1. Ensure DRC passes (zero errors)
# 2. Verify BOM is complete and costed
# 3. Run KiBot to generate fab outputs
kibot -c kibot.yaml

# 4. Copy outputs to versioned fab folder
mkdir -p fab/v2.1
cp -r fab/gerbers fab/v2.1/
cp docs/bom.csv fab/v2.1/bom-assembly.csv

# 5. Commit the release
git add fab/v2.1/ docs/
git commit -m "[fab] Tag v2.1 — ordered JLCPCB 2026-05-17, ECO-007 incorporated"

# 6. Tag the release
git tag -a v2.1 -m "Board revision 2.1 — USB-C charging, R47 corrected to 4.7k"
git push origin main --tags

# 7. Create a GitHub Release with Gerbers as attachment
gh release create v2.1 fab/v2.1/gerbers/*.gbr --title "Board Rev 2.1" --notes "See fab/v2.1/fab-notes.md"
```

---

## Further Reading

- [KiBot CI/CD Documentation](https://github.com/INTI-CMNB/KiBot)
- [Git LFS for large hardware binaries](https://git-lfs.github.com/)
- [KiCad-Diff — visual schematic diffs](https://github.com/Gasman2014/KiCad-Diff)
- [Kitspace — public PCB project hosting](https://kitspace.org)
- [Open Hardware Association guidelines](https://certification.oshwa.org)
