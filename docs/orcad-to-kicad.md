# OrCAD Capture → KiCad Migration Guide

This guide covers how to move OrCAD Capture schematic data into the KiCad ecosystem for layout, simulation, BOM generation, and CI/CD integration. The two tools can coexist — you do not need to abandon OrCAD to benefit from the open-source toolchain.

---

## When to Use This Guide

- You have an OrCAD Capture project (`.dsn`, `.opj`) and want to run it through KiCad pcbnew for layout
- You want to use open-source BOM or CI/CD tools (KiBot, KiCost, InteractiveHtmlBom) on your OrCAD design
- You are evaluating a full migration from OrCAD to KiCad
- You want to use version control and diff schematic changes across engineers

---

## Option 1 — Netlist Bridge (Easiest, Non-destructive)

This keeps OrCAD Capture as your schematic tool but uses KiCad for everything downstream.

### Step 1: Export netlist from OrCAD Capture

1. Open your project in OrCAD Capture
2. Go to **Tools → Create Netlist**
3. Select the **KiCad** netlist format tab (available in OrCAD 17.4+)
   - If not available, select **PCB2** or **Cadence** format as a fallback
4. Click **Run**
5. The output is a `.net` file

> **Alternative:** Use the **Allegro** netlist format (`.brd`) for import into KiCad pcbnew directly via File → Import → Non-KiCad Board File

### Step 2: Import into KiCad pcbnew

1. Open KiCad, create a new project
2. Open **pcbnew**
3. Go to **File → Import → Netlist**
4. Select your `.net` file
5. Map OrCAD component references to KiCad footprints using the footprint assignment dialog

### Step 3: Assign footprints

OrCAD stores footprint names in its own format. You will need to remap them to KiCad footprint library names. This is a one-time mapping that can be saved as a `.cvpcb` file for reuse.

```text
OrCAD footprint name     →  KiCad footprint library:name
SOIC-8                   →  Package_SO:SOIC-8_3.9x4.9mm_P1.27mm
0402                     →  Capacitor_SMD:C_0402_1005Metric
TO-92                    →  Package_TO_SOT_THT:TO-92_Inline
```

---

## Option 2 — Full Schematic Migration

For teams moving entirely to KiCad.

### Recommended path: Export OrCAD → EDIF → KiCad

OrCAD Capture can export to **EDIF 2.0.0**, which several tools can convert to KiCad format.

```bash
# Using the orcad2kicad Python script
pip install orcad2kicad
orcad2kicad --input design.dsn --output design.kicad_sch
```

Alternatively, use the [EDA Converter](https://www.eda-technologies.com) web tool for complex hierarchical designs.

### What survives migration

| Element | Survival |
|---|---|
| Component references (R1, C2, U1) | ✅ Full |
| Net names and connectivity | ✅ Full |
| Pin connections | ✅ Full |
| Component values | ✅ Full |
| Hierarchical blocks | ⚠️ Partial — verify manually |
| Custom symbols | ⚠️ Needs remapping to KiCad library |
| Simulation models (PSpice) | ❌ Separate step — see [pspice-to-ngspice.md](pspice-to-ngspice.md) |
| Design notes / annotations | ❌ Must be re-entered |

---

## Option 3 — SKiDL Abstraction Layer

If you want to generate netlists programmatically from Python instead of maintaining a GUI schematic:

```python
from skidl import *

# Define components (reusable across projects)
@package
def resistor(a, b):
    pass

r1 = resistor()
r1['a'] += Net('VCC')
r1['b'] += Net('GND')
r1.value = '10k'
r1.footprint = 'Resistor_SMD:R_0402_1005Metric'

# Generate KiCad or OrCAD-compatible netlist
generate_netlist()    # .net file for pcbnew
generate_xml()        # for KiBOM / KiCost
```

This approach makes schematics code-reviewable, parametric, and CI/CD-friendly.

---

## BOM from OrCAD → Open-Source Tools

### Export BOM from OrCAD Capture

1. **Tools → Bill of Materials**
2. Select **CSV** output format
3. Include columns: Reference, Value, Footprint, Quantity, Manufacturer, MPN

### Feed into KiCost (real-time pricing)

```bash
pip install kicost
kicost --input bom.csv --output priced_bom.xlsx --fields "Value,Footprint,Manufacturer,MPN"
```

### Feed into InteractiveHtmlBom

```bash
# Requires a KiCad .kicad_pcb file alongside the BOM
python ibom.py --no-browser --dest-dir ./docs /path/to/board.kicad_pcb
```

---

## Version Control for OrCAD Projects

OrCAD's `.dsn` files are binary by default. To make them diff-able in git:

1. In OrCAD Capture, set **Preferences → Save As** to **ASCII** format
2. Add `.gitignore` entries for OrCAD build artifacts:

```gitignore
# OrCAD build artifacts (do not commit)
*.bak
*.lck
*.DRC
OrCAD_export/
*.log
*.err
allegro/
```

3. Commit ASCII `.dsn` files — they are line-diffable in git
4. See the full workflow: [git-for-hardware.md](git-for-hardware.md)

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Missing footprints after import | OrCAD footprint names don't match KiCad library names | Use pcbnew footprint remapping dialog |
| Net names contain `/` characters | OrCAD hierarchical net naming | Pre-process netlist to replace `/` with `_` |
| Power symbols not recognized | OrCAD power symbols differ from KiCad | Manually add KiCad PWR_FLAG and power symbols |
| Hierarchical sheets not importing | EDIF hierarchy flattening | Use the `--flatten` flag in orcad2kicad |

---

## Further Reading

- [KiCad Netlist Import Documentation](https://docs.kicad.org/master/en/pcbnew/pcbnew.html#netlist_file)
- [SKiDL Documentation](https://devbisme.github.io/skidl/)
- [KiBot CI/CD Configuration](https://github.com/INTI-CMNB/KiBot)
- [OrCAD Export Guide (Cadence)](https://www.orcad.com/resources/orcad-tutorials)
