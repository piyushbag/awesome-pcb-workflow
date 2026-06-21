# Awesome PCB Workflow [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

<div align="center">

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="banner" width="100%">

<em>Open-source tools for the complete PCB design workflow.</em><br>
<strong>AI-assisted EDA · Schematic Capture · SPICE Simulation · Signal Integrity · Layout Automation · DFM · Fabrication CI/CD · Hardware Testing Agents</strong>

[![GitHub Stars](https://badgen.net/github/stars/piyushbag/awesome-pcb-workflow?label=stars&icon=github&color=gold)](https://github.com/piyushbag/awesome-pcb-workflow/stargazers)
[![GitHub Forks](https://badgen.net/github/forks/piyushbag/awesome-pcb-workflow?label=forks&icon=github)](https://github.com/piyushbag/awesome-pcb-workflow/forks)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0--1.0-lightgrey.svg?style=flat-square)](LICENSE)
[![Works with OrCAD](https://img.shields.io/badge/Works%20with-OrCAD-red?style=flat-square)](https://www.orcad.com)
[![Works with KiCad](https://img.shields.io/badge/Works%20with-KiCad-blue?style=flat-square)](https://www.kicad.org)

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="banner" width="100%">

</div>

## Contents

- [💡 Why This Exists](#-why-this-exists)
- [🚀 Quick Start](#-quick-start)
- [🔥 Featured This Month](#-featured-this-month)
- [🗺 Workflow Map](#-workflow-map)
- [📂 Tools by Stage](#-tools-by-stage)
  - [📋 Requirements & Specification](#-requirements--specification)
  - [📐 Schematic Capture](#-schematic-capture)
  - [📦 Component Libraries & BOM Management](#-component-libraries--bom-management)
  - [⚡ SPICE & Circuit Simulation](#-spice--circuit-simulation)
  - [📡 Signal Integrity & EMC Analysis](#-signal-integrity--emc-analysis)
  - [🖥 PCB Layout & EDA](#-pcb-layout--eda)
  - [🏭 Fabrication & Gerber Tooling](#-fabrication--gerber-tooling)
  - [🔩 DFM & Panelization](#-dfm--panelization)
  - [🧪 Testing & Verification](#-testing--verification)
  - [🤖 AI & Automation](#-ai--automation)
  - [📚 Documentation & Collaboration](#-documentation--collaboration)
  - [🎓 Learning Resources](#-learning-resources)
- [🔌 OrCAD Integration Cheatsheet](#-orcad-integration-cheatsheet)
- [⭐ Star History](#-star-history)

---

## 💡 Why This Exists

Most "awesome" PCB lists stop at schematic capture. Real hardware engineering is a **12-stage pipeline**, and broken toolchains in any stage kill productivity. This repo covers **everything** — from design intent to tested board — with open-source tools that plug into your existing OrCAD-based flow or replace proprietary stages entirely.

- 🏭 **Full pipeline coverage** — requirements, schematic, simulation, layout, DFM, fabrication, test, and documentation.
- 🔧 **OrCAD-first integration notes** — every tool documents how it connects to OrCAD Capture, PSpice, and Allegro.
- 🤖 **AI-augmented** — modern scripting and AI tools that eliminate repetitive manual design tasks.
- 📦 **Curated, not dumped** — each entry is verified, actively maintained, with a one-line "why use it" note.
- 🆓 **100% open source** — no EDA vendor lock-in, no paywalls, no telemetry.

---

## 🚀 Quick Start

**Get a complete open-source PCB environment running in under 5 minutes:**

```bash
# 1. Install KiCad — the open EDA that reads/writes OrCAD netlists
brew install --cask kicad          # macOS
sudo apt install kicad             # Ubuntu/Debian
winget install KiCad.KiCad        # Windows

# 2. Install ngspice for SPICE simulation
brew install ngspice               # macOS
sudo apt install ngspice           # Ubuntu/Debian

# 3. Clone this repo for workflow scripts and templates
git clone https://github.com/piyushbag/awesome-pcb-workflow.git
cd awesome-pcb-workflow

# 4. Install Python toolchain helpers
pip install -r requirements.txt    # kibot, kibom, kicost, skidl, pymeasure
```

---

## 🔥 Featured This Month

| Tool               | What it does                                                                         | Stage                                          |
| ------------------ | ------------------------------------------------------------------------------------ | ---------------------------------------------- |
| ⚡ SKiDL | Describe schematics in pure Python — generate netlists programmatically, version-controllable. | [Schematic](#-schematic-capture) |
| 📐 Qucs-S | Qt GUI for ngspice/Xyce with RF S-parameter and harmonic balance support. | [Simulation](#-signal-integrity--emc-analysis) |
| 📊 KiBOM | Configurable BOM export from KiCad schematics to CSV, HTML, Excel. | [BOM](#-component-libraries--bom-management) |
| 📋 KiBot | CI/CD automation: Gerbers, drill, BOM, PDF docs, 3D models — one YAML config. | [Fabrication](#-fabrication--gerber-tooling) |
| 🌐 Kitspace | Git for hardware — public PCB project hosting with 3D preview and BOM pricing. | [Testing](#-testing--verification) |

> 📬 **Watch this repo** to get notified when new tools are added each month.

---

## 🗺 Workflow Map

```text
┌─────────────────────────────────────────────────────────────────┐
│                    PCB DESIGN WORKFLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 Requirements & Specification                                │
│       │                                                         │
│       ▼                                                         │
│  📐 Schematic Capture ──── 📦 Component Library                 │
│       │                         │                               │
│       ▼                         ▼                               │
│  ⚡ SPICE Simulation       💰 BOM Management                     │
│       │                                                         │
│       ▼                                                         │
│  📡 Signal Integrity & EMC Analysis                             │
│       │                                                         │
│       ▼                                                         │
│  🖥️  PCB Layout / EDA ──── 🧊 3D Visualization                  │
│       │                                                         │
│       ▼                                                         │
│  ✅  Design Rule Check (DRC) & DFM Analysis                     │
│       │                                                         │
│       ▼                                                         │
│  🏭  Fabrication Prep ──── 🔩 Panelization ──── 👁️ Gerber QA    │
│       │                                                         │
│       ▼                                                         │
│  🧪  Test & Verification ──── 🔍 Debug                          │
│       │                                                         │
│       ▼                                                         │
│  📚  Documentation ──── 🌐 Version Control ──── 🚀 Release      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 Tools by Stage

### 📋 Requirements & Specification

_Capture and manage design requirements before a single wire is drawn._

| Tool                                                              | Description                                                                                       | License    |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------- |
| [📝 Doorstop](https://github.com/jacebrowning/doorstop)           | Git-native requirements management — trace requirements to schematic notes and design properties. | MIT        |
| [🗂️ Obsidian](https://obsidian.md)                                | Free-form engineering notebook: decisions, constraints, block diagrams, links.                    | Free       |
| [📊 draw.io / diagrams.net](https://github.com/jgraph/drawio)     | Open-source block diagram and architecture drawing tool.                                          | Apache-2.0 |
| [📋 OSHW Checklist](https://certification.oshwa.org/process.html) | Open hardware compliance and requirements checklist from OSHWA.                                   | —          |
| [🏗️ Mermaid](https://github.com/mermaid-js/mermaid)               | Markdown-based diagram-as-code for system architecture in docs.                                   | MIT        |

---

### 📐 Schematic Capture

_Draw, annotate, and export schematics. Every tool documents its OrCAD interoperability._

| Tool                                                     | Description                                                                                    | OrCAD Integration                          | License |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------ | ------- |
| [🟦 KiCad](https://www.kicad.org)                        | Industry-leading open EDA — schematic + PCB in one suite. 50k+ community symbols.              | Import OrCAD `.dsn` via netlist converter. | GPL-3.0 |
| [🟩 LibrePCB](https://librepcb.org)                      | Modern, clean EDA with strict library management and real-time ERC.                            | Netlist import via KiCad bridge.           | GPL-3.0 |
| [⚡ SKiDL](https://github.com/devbisme/skidl)            | Describe schematics in pure Python — generate netlists programmatically, version-controllable. | Export to OrCAD-compatible `.net`.         | MIT     |
| [🔶 atopile](https://github.com/atopile/atopile)         | Code-driven schematic design with type safety, reuse, and auto part selection.                 | Exports to KiCad / Gerber.                 | MIT     |
| [🟫 gEDA/gschem](http://www.geda-project.org)            | Veteran open-source EDA with deep Scheme scripting and netlist flexibility.                    | Netlist export compatible.                 | GPL-2.0 |
| [🌐 Horizon EDA](https://github.com/horizon-eda/horizon) | Constraint-based EDA with real-time DRC, pooled parts library.                                 | —                                          | GPL-3.0 |
| [🐍 faebryk](https://github.com/faebryk/faebryk)         | Graph-based schematic design in Python — AI-assisted part selection and constraint solving.    | Netlist export.                            | MIT     |
| [🖥 PcbDraw](https://github.com/yaqwsx/PcbDraw) | Convert your KiCAD board into a nicely looking 2D drawing suitable for pinout diagrams. | — | MIT |
| [🟦 kicanvas](https://github.com/theacodes/kicanvas) | The KiCAD web viewer. | — | NOASSERTION |
| [⚡ CircuitPro](https://github.com/CircuitProApp/CircuitPro) | Circuit Pro — a Mac-native PCB design tool. Free for personal and commercial use. | — | NOASSERTION |

> **OrCAD Users:** See our full guide → [docs/orcad-to-kicad.md](docs/orcad-to-kicad.md)

---

### 📦 Component Libraries & BOM Management

_Keep component data clean, costs low, and inventory tracked._

#### Component Libraries

| Tool                                                                  | Description                                                        | License      |
| --------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------ |
| [📚 KiCad Official Libraries](https://github.com/KiCad/kicad-symbols) | 50,000+ verified symbols and footprints, community-maintained.     | CC-BY-SA-4.0 |
| [🔍 Component Search Engine](https://componentsearchengine.com)       | Free EDA models for 35M+ parts — OrCAD, KiCad, Altium formats.     | Free         |
| [⚡ SnapEDA](https://www.snapeda.com)                                 | Industry-standard free component library with verified footprints. | Free         |
| [📦 Ultra Librarian](https://www.ultralibrarian.com)                  | 13M+ free CAD models for all major EDA tools including OrCAD.      | Free         |
| [🗄️ KiCad Library Convention](https://klc.kicad.org)                  | Standards guide for building clean, standardized libraries.        | —            |
| [🔬 Octopart](https://octopart.com)                                   | Multi-distributor component search with parametric filtering.      | Free         |

#### BOM Management & Costing

| Tool                                                                            | Description                                                        | OrCAD Integration          | License  |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------- | -------- |
| [📊 KiBOM](https://github.com/SchrodingersGat/KiBOM)                            | Configurable BOM export from KiCad schematics to CSV, HTML, Excel. | —                          | MIT      |
| [💰 KiCost](https://github.com/hildogjr/KiCost)                                 | Real-time pricing from Mouser, Digi-Key, Arrow, LCSC.              | Works with OrCAD netlists. | MIT      |
| [📋 InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) | Interactive BOM with visual component highlighting on PCB image.   | OrCAD BOM CSV → ibom.      | MIT      |
| [🏭 InvenTree](https://github.com/inventree/InvenTree)                          | Full inventory + BOM management system (self-hosted, API-driven).  | REST API integration.      | MIT      |
| [📦 Partkeepr](https://github.com/partkeepr/PartKeepr)                          | Open-source parts management with stock tracking and datasheets.   | CSV import.                | AGPL-3.0 |
| [🌐 Kitspace BOM Builder](https://github.com/kitspace/bom-builder)              | Web-based BOM building with multi-distributor price lookup.        | —                          | AGPL-3.0 |

---

### ⚡ SPICE & Circuit Simulation

_Simulate before you spin a board. Catch topology mistakes for free._

| Tool                                                     | Description                                                               | Best For                        | License |
| -------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------- | ------- |
| [🔬 ngspice](http://ngspice.sourceforge.net)             | The open-source SPICE standard — transient, AC, DC, noise, Monte Carlo.   | All-purpose circuit simulation. | BSD     |
| [📐 Qucs-S](https://github.com/ra3xdh/qucs_s)            | Qt GUI for ngspice/Xyce with RF S-parameter and harmonic balance support. | RF circuits with GUI.           | GPL-2.0 |
| [🐍 PySpice](https://github.com/FabriceSalvaire/PySpice) | Python API to ngspice — scriptable parametric and sweep simulation.       | Design space exploration.       | GPL-3.0 |
| [⚡ Xyce](https://xyce.sandia.gov)                       | High-performance parallel SPICE by Sandia National Labs.                  | Large mixed-signal circuits.    | GPL-3.0 |
| [🌐 Qucs](http://qucs.sourceforge.net)                   | Circuit simulator with S-parameters, Verilog-A, and harmonic balance.     | RF/microwave, S-param.          | GPL-2.0 |
| [📊 SchemDraw](https://schemdraw.readthedocs.io)         | Draw and annotate schematics in Python, pair with PySpice.                | Quick topology docs.            | MIT     |
| [⚡ ahkab](https://github.com/ahkab/ahkab) | a SPICE-like electronic circuit simulator written in Python. | Circuit simulation. | GPL-2.0 |
| [⚡ SpiceSharp](https://github.com/SpiceSharp/SpiceSharp) | Spice# is a cross-platform electronic circuit simulator based on Berkeley Spice - the mother of commercial... | Circuit simulation. | MIT |

> **OrCAD PSpice Users:** `.cir` netlists from PSpice are directly compatible with ngspice. See our migration guide → [docs/pspice-to-ngspice.md](docs/pspice-to-ngspice.md)

---

### 📡 Signal Integrity & EMC Analysis

_Catch SI/EMC problems before fab — boards are expensive, simulation is free._

| Tool                                                                                                 | Description                                                                           | License  |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------- |
| [🌊 openEMS](https://openems.de)                                                                     | Open-source 3D EM field simulator using FDTD — free alternative to HFSS/CST.          | GPL-3.0  |
| [📡 atlc](http://atlc.sourceforge.net)                                                               | Arbitrary transmission line calculator — 2D cross-section impedance from geometry.    | GPL-2.0  |
| [🐍 scikit-rf](https://github.com/scikit-rf/scikit-rf)                                               | Python RF/microwave analysis: S-params, network analysis, de-embedding, calibration.  | BSD      |
| [🔧 Saturn PCB Toolkit](https://saturnpcb.com/saturn-pcb-toolkit/)                                   | Free Windows app: impedance, via current, trace width, differential pair calculators. | Freeware |
| [🌐 MMTL](https://sourceforge.net/projects/mmtl/)                                                    | Multiconductor transmission-line solver for complex trace geometries.                 | GPL-2.0  |
| [📊 KiCad Impedance Calculator](https://docs.kicad.org/master/en/pcb_calculator/pcb_calculator.html) | Built-in PCB trace and via impedance calculator inside KiCad.                         | GPL-3.0  |
| [🔬 Sonnet Lite](https://www.sonnetsoftware.com/products/lite/)                                      | Free tier of Sonnet EM planar 3D EM simulator.                                        | Freeware |
| [⚡ AppCAD](https://www.broadcom.com/info/wireless/appcad)                                           | Free RF design and impedance tool from Broadcom/Avago.                                | Freeware |

---

### 🖥 PCB Layout & EDA

_Place, route, and verify your board geometry._

| Tool                                                            | Description                                                             | OrCAD Integration                     | License  |
| --------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------- | -------- |
| [🟦 KiCad pcbnew](https://www.kicad.org/discover/pcb-design/)   | World-class open PCB layout with interactive router, DRC, and 3D view.  | Import via IPC-2581 or KiCad netlist. | GPL-3.0  |
| [🌐 Horizon EDA layout](https://github.com/horizon-eda/horizon) | Real-time DRC, constraint-driven routing, pooled library.               | —                                     | GPL-3.0  |
| [🐍 pcbnew Python API](https://docs.kicad.org/doxygen-python/)  | Full PCB manipulation and automation via Python scripting inside KiCad. | —                                     | GPL-3.0  |
| [📐 LibrePCB layout](https://librepcb.org/features/)            | Beginner-friendly with strict design rule enforcement, clean UI.        | —                                     | GPL-3.0  |
| [🎨 FreeRouting](https://github.com/freerouting/freerouting)    | Java-based autorouter that plugs into KiCad and accepts DSN files.      | DSN netlist import.                   | GPL-3.0  |
| [🟩 TopoR Lite](http://www.eremex.com/products/topor/)          | Topological autorouter with topology-preserving rerouting (free lite).  | Netlist import.                       | Freeware |

#### 3D Visualization & Mechanical Co-Design

| Tool                                                             | Description                                                        | License  |
| ---------------------------------------------------------------- | ------------------------------------------------------------------ | -------- |
| [🧊 KiCad 3D Viewer](https://www.kicad.org/discover/3d-viewer/)  | Real-time 3D PCB viewer with STEP, VRML, and IDF export.           | GPL-3.0  |
| [🔩 FreeCAD KiCad StepUp](https://github.com/easyw/kicad-StepUp) | Bi-directional mechanical/PCB co-design — changes sync both ways.  | LGPL-2.0 |
| [📐 OpenSCAD](https://openscad.org)                              | Parametric enclosure design from PCB dimensions via script.        | GPL-2.0  |
| [🌐 Diode.io](https://www.withdiode.com)                         | Browser-based 3D PCB viewer for sharing designs with stakeholders. | Free     |

---

### 🏭 Fabrication & Gerber Tooling

_Generate, verify, and send fab-ready files._

| Tool                                                                    | Description                                                                   | License |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------- |
| [📋 KiBot](https://github.com/INTI-CMNB/KiBot)                          | CI/CD automation: Gerbers, drill, BOM, PDF docs, 3D models — one YAML config. | GPL-3.0 |
| [👁️ Gerbv](http://gerbv.geda-project.org)                               | The open-source Gerber/Excellon viewer — battle-tested and reliable.          | GPL-2.0 |
| [🌐 Tracespace](https://tracespace.io)                                  | Web-based Gerber viewer with layer compositing and drill visualization.       | MIT     |
| [🐍 pcb-tools](https://github.com/curtacircuitos/pcb-tools)             | Python library for reading, writing, and transforming Gerber files.           | MIT     |
| [🐍 pygerber](https://github.com/Argmaster/pygerber)                    | Modern Python Gerber renderer with DFM checking.                              | MIT     |
| [📦 jlcpcb-tools](https://github.com/Bouni/kicad-jlcpcb-tools)          | KiCad plugin: one-click JLCPCB order with LCSC BOM generation.                | MIT     |
| [🔍 OpenBoardView](https://github.com/openboardview/OpenBoardView)      | View `.brd` / `.bvr` board files for repair and reverse engineering.          | MIT     |
| [📊 GerberTools](https://github.com/ThisIsNotRocketScience/GerberTools) | Gerber file manipulation, panelization, and merging utility.                  | MIT     |
| [🌐 Salitronic Gerber Analyzer](https://salitronic.com/gerber_analyzer) | Browser-based Gerber / ODB++ / IPC-2581 viewer with DRC, layer diff, pick-and-place, plus thermal, EMI and impedance analysis. | Free |

---

### 🔩 DFM & Panelization

_Make your board manufacturable at scale._

| Tool                                                                         | Description                                                                                 | License  |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | -------- |
| [🏭 KiKit](https://github.com/yaqwsx/KiKit)                                  | CLI panelization: mouse-bites, V-cuts, fiducials, automated tab placement from JSON config. | MIT      |
| [📏 DFMNow](https://www.numericalinnovations.com/pages/dfm-now)              | Free DFM analysis for Gerber files — checks clearances, annular rings, min trace.           | Freeware |
| [🌐 JLCPCB DFM Checker](https://dfm.nexpcb.com)                              | Web-based DFM checker targeting JLCPCB design rules.                                        | Free     |
| [🐍 gerber-panelizer](https://github.com/ThisIsNotRocketScience/GerberTools) | Script-driven Gerber panelization with configurable spacing.                                | MIT      |
| [🔧 PCB Shopper](https://pcbshopper.com)                                     | Compare Gerber specs across 30+ PCB manufacturers — price and lead time.                    | Free     |

---

### 🧪 Testing & Verification

_Verify the board works before it goes to production._

#### Automated Test Frameworks

| Tool                                                     | Description                                                                     | License  |
| -------------------------------------------------------- | ------------------------------------------------------------------------------- | -------- |
| [🐍 PyMeasure](https://github.com/pymeasure/pymeasure)   | Python instrument control: Keysight, Tektronix, R&S, Stanford Research, Fluke.  | MIT      |
| [🔬 OpenTAP](https://github.com/opentap/opentap)         | Industrial test automation platform — write test steps in C# or Python plugins. | MPL-2.0  |
| [📡 sigrok / PulseView](https://sigrok.org)              | Open-source logic analyzer frontend: 100+ protocol decoders, scope integration. | GPL-3.0  |
| [🔌 OpenOCD](https://openocd.org)                        | Open On-Chip Debugger — JTAG/SWD for firmware-level test on hardware.           | GPL-2.0  |
| [🐍 cocotb](https://github.com/cocotb/cocotb)            | Python-based HDL co-simulation for FPGA/ASIC co-verification.                   | BSD      |
| [🧪 labgrid](https://github.com/labgrid-project/labgrid) | Lab automation framework: coordinate power, serial, JTAG across a test farm.    | LGPL-2.1 |

#### Boundary Scan & JTAG

| Tool                                         | Description                                                      | License |
| -------------------------------------------- | ---------------------------------------------------------------- | ------- |
| [🔍 UrJTAG](http://urjtag.org)               | Universal JTAG boundary scan — supports 1000+ device BSDL files. | GPL-2.0 |
| [🔬 pyBSL](https://github.com/nwidger/pyBSL) | Python boundary scan library for board-level testing.            | MIT     |

---

### 🤖 AI & Automation

_Let code do the repetitive design work._

| Tool                                                                | Description                                                                    | License                 |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------- |
| [⚡ atopile](https://github.com/atopile/atopile)                    | Code-first hardware design — generate schematics from typed, reusable modules. | MIT                     |
| [🐍 SKiDL](https://github.com/devbisme/skidl)                       | Describe PCB schematics in Python — parametric, versionable, testable in CI.   | MIT                     |
| [🤖 KiBot](https://github.com/INTI-CMNB/KiBot)                      | CI/CD pipeline for PCB: fab outputs, docs, and checks on every Git push.       | GPL-3.0                 |
| [🧠 faebryk](https://github.com/faebryk/faebryk)                    | Graph-based PCB design framework with AI-assisted part selection.              | MIT                     |
| [🐍 KiCad Python Scripting](https://docs.kicad.org/doxygen-python/) | Full pcbnew Python API — automate placement, routing, and export.              | GPL-3.0                 |
| [🔬 spade](https://gitlab.com/spade-lang/spade)                     | Hardware description language for PCB-level digital design.                    | EUPL-1.2                |
| [🌐 JITX](https://www.jitx.com)                                     | Design-intent language for PCB automation (free tier available).               | Proprietary (free tier) |
| [🐍 gdsfactory](https://github.com/gdsfactory/gdsfactory)           | Python-driven photonic / mixed PCB chip layout with automated DRC.             | MIT                     |
| [🔧 pcbflow](https://github.com/michaelgale/pcbflow)                | Python scripting layer over KiCad pcbnew for programmatic board generation.    | MIT                     |

---

### 📚 Documentation & Collaboration

_Document designs so every engineer on the team can understand them._

| Tool                                                      | Description                                                                    | License  |
| --------------------------------------------------------- | ------------------------------------------------------------------------------ | -------- |
| [🌐 Kitspace](https://kitspace.org)                       | Git for hardware — public PCB project hosting with 3D preview and BOM pricing. | AGPL-3.0 |
| [📦 Aisler](https://aisler.net)                           | Shareable PCB project pages with fabrication integration.                      | Free     |
| [📖 KiBot PDF Export](https://github.com/INTI-CMNB/KiBot) | Auto-generate schematic PDFs and assembly drawings in CI.                      | GPL-3.0  |
| [🏷️ IPC-2581](https://www.ipc.org/ipc-2581)               | Open fab data format replacing Gerber/ODB++ — KiCad exports natively.          | Standard |
| [📝 Git for Hardware](docs/git-for-hardware.md)           | Git workflow for PCB: what to commit, binary handling, CI integration.         | —        |

---

### 🎓 Learning Resources

#### Standards & Reference

| Resource                                                                   | Description                                                                            |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [📏 IPC Standards](https://www.ipc.org)                                    | IPC-2221 (design), IPC-7711 (rework), IPC-A-610 (acceptance criteria) — free previews. |
| [📡 Henry Ott EMC Tech Tips](http://www.hottconsultants.com/techtips.html) | Free EMC design reference from the author of the industry bible.                       |
| [🔬 Eric Bogatin SI Resources](https://www.betheresignal.com)              | Free signal integrity resources, webinars, and rule-of-thumb guides.                   |

#### Courses & Community

| Resource                                                             | Description                                                                       |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [🎓 Phil's Lab (YouTube)](https://www.youtube.com/@PhilsLab)         | Best free KiCad + hardware engineering YouTube channel — end-to-end board builds. |
| [🏫 Contextual Electronics](https://contextualelectronics.com)       | Project-based PCB design courses from beginner to advanced.                       |
| [💬 r/PrintedCircuitBoard](https://reddit.com/r/PrintedCircuitBoard) | Design reviews, community Q&A, and tool recommendations.                          |
| [🌐 EEVblog Forum](https://www.eevblog.com/forum/)                   | Veteran electronics engineering community — SI, EMC, test, production.            |
| [📖 Hackaday.io](https://hackaday.io)                                | Open hardware project hosting with community feedback.                            |

---

## 🔌 OrCAD Integration Cheatsheet

Quick reference for plugging OrCAD into the open-source ecosystem:

```text
OrCAD Capture  ──(netlist .net export)──▶  KiCad pcbnew / SKiDL / KiBOM
OrCAD PSpice   ──(.cir netlist)─────────▶  ngspice / PySpice / Xyce
OrCAD Allegro  ──(IPC-2581 export)──────▶  KiKit panelization / KiBot CI / FreeCAD
OrCAD BOM      ──(CSV export)───────────▶  KiCost / InvenTree / InteractiveHtmlBom
OrCAD 3D       ──(STEP export)──────────▶  FreeCAD / OpenSCAD
```

| OrCAD Tool    | Open-Source Equivalent      | Migration Guide                                        |
| ------------- | --------------------------- | ------------------------------------------------------ |
| OrCAD Capture | KiCad Eeschema / SKiDL      | [docs/orcad-to-kicad.md](docs/orcad-to-kicad.md)       |
| OrCAD PSpice  | ngspice / PySpice           | [docs/pspice-to-ngspice.md](docs/pspice-to-ngspice.md) |
| OrCAD Allegro | KiCad pcbnew                | [docs/orcad-integration/](docs/orcad-integration/)     |
| OrCAD BOM     | KiCost + InteractiveHtmlBom | [docs/orcad-integration/](docs/orcad-integration/)     |

> Full integration guides → [`docs/orcad-integration/`](docs/orcad-integration/)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=piyushbag/awesome-pcb-workflow&type=Date)](https://star-history.com/#piyushbag/awesome-pcb-workflow&Date)

> Star the repo to get notified when new tools are added, and to help other engineers find this resource.

---

<div align="center">

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" alt="banner" width="100%">

Built with ❤️ for hardware engineers, by hardware engineers.

[⭐ Star](https://github.com/piyushbag/awesome-pcb-workflow/stargazers) &nbsp;·&nbsp;
[🍴 Fork](https://github.com/piyushbag/awesome-pcb-workflow/fork) &nbsp;·&nbsp;
[🐛 Report an Issue](https://github.com/piyushbag/awesome-pcb-workflow/issues/new/choose) &nbsp;·&nbsp;
[📬 Submit a Tool](https://github.com/piyushbag/awesome-pcb-workflow/issues/new?template=add-tool.md)

</div>
