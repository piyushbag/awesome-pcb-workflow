# OrCAD Integration Guide Index

This directory documents how to connect OrCAD's suite of tools to the open-source PCB ecosystem. Each guide is written for practicing hardware engineers who use OrCAD daily and want to augment or partially replace it with open-source tooling.

---

## Guides

| Guide | OrCAD Tool | Open-Source Target | What It Covers |
|---|---|---|---|
| [orcad-to-kicad.md](../orcad-to-kicad.md) | OrCAD Capture | KiCad Eeschema / pcbnew | Netlist bridge, full migration, footprint mapping |
| [pspice-to-ngspice.md](../pspice-to-ngspice.md) | OrCAD PSpice | ngspice / PySpice | `.cir` compatibility, syntax differences, Python automation |

---

## Quick Reference: OrCAD Export Formats

| Export Format | Available In | Use With |
|---|---|---|
| KiCad netlist `.net` | OrCAD Capture 17.4+ | KiCad pcbnew, SKiDL |
| Cadence netlist `.cdl` | OrCAD Capture | Various EDA tools |
| EDIF 2.0.0 | OrCAD Capture | orcad2kicad converter |
| PSpice netlist `.cir` | OrCAD PSpice | ngspice, Xyce, PySpice |
| IPC-2581 | OrCAD Allegro 17.2+ | KiKit, FreeCAD StepUp |
| ODB++ | OrCAD Allegro | KiCad, most fab portals |
| BOM CSV | OrCAD Capture | KiCost, InvenTree, ibom |
| STEP 3D model | OrCAD Allegro | FreeCAD, KiCad 3D viewer |
| Gerber RS-274X | OrCAD Allegro | Gerbv, Tracespace, KiBot |

---

## OrCAD Suite → Open-Source Equivalent Map

```text
OrCAD Capture (Schematic)
    │
    ├── Full replacement  →  KiCad Eeschema / SKiDL / atopile
    └── Netlist bridge   →  KiCad pcbnew (layout only open-source)

OrCAD PSpice (Simulation)
    │
    ├── Full replacement  →  ngspice + PySpice + Qucs-S
    └── Partial          →  ngspice for .cir netlists, PSpice GUI retained

OrCAD Allegro (PCB Layout)
    │
    ├── Full replacement  →  KiCad pcbnew + FreeRouting
    └── Netlist bridge   →  IPC-2581 export → KiCad

OrCAD SigXplorer (Signal Integrity)
    │
    └── Open alternative  →  openEMS + scikit-rf + Saturn PCB Toolkit

OrCAD Constraint Manager
    │
    └── Open alternative  →  KiCad constraint system + Horizon EDA

OrCAD Part Manager / CIS (Component Data)
    │
    └── Open alternatives →  InvenTree + Component Search Engine + SnapEDA
```

---

## Integration Philosophy

You do not have to choose between OrCAD and open-source. The most pragmatic approach for most teams:

1. **Keep OrCAD Capture** for schematic capture (your team knows it, your libraries are built for it)
2. **Add KiBot** for CI/CD — auto-generate Gerbers, BOM, and docs on every git push
3. **Add ngspice + PySpice** alongside PSpice for scripted, parametric simulation
4. **Add KiCost + InteractiveHtmlBom** for BOM management
5. **Replace PSpice with full ngspice** only when the team has bandwidth for the learning curve
6. **Replace Allegro with KiCad pcbnew** as a long-term project for new board spins

This incremental approach delivers immediate ROI (CI/CD, BOM automation) without disrupting existing design flows.

---

## Contributing an Integration Guide

If you have hands-on experience connecting OrCAD to an open-source tool not covered here, please add a guide:

1. Create a `.md` file in `docs/orcad-integration/`
2. Cover: what you're connecting, the export format used, step-by-step instructions, troubleshooting
3. Add a row to the table above
4. Submit a PR with title: `Add OrCAD integration guide for [Tool]`
