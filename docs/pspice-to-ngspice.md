# OrCAD PSpice → ngspice Migration Guide

ngspice is the open-source SPICE simulator and is directly compatible with PSpice netlist syntax. Most `.cir` files exported from OrCAD PSpice run in ngspice with zero or minimal changes. This guide covers the differences, gotchas, and Python automation patterns.

---

## Why Move to ngspice?

| | OrCAD PSpice | ngspice |
|---|---|---|
| License | Commercial | BSD (free, open-source) |
| CI/CD integration | Manual | Full scripting via CLI |
| Python API | Limited | PySpice, native API |
| Batch / parametric sweeps | GUI-only | Script-driven |
| Model library | OrCAD-specific `.lib` | `.lib` files compatible |
| Community models | Limited | ngspice-compatible `.lib` from vendors |

---

## Compatibility: What Works Out of the Box

The following PSpice features are natively supported in ngspice:

| Feature | ngspice Support |
|---|---|
| R, L, C, V, I, E, F, G, H sources | ✅ Full |
| MOSFET (Level 1, 2, 3, BSIM) models | ✅ Full |
| BJT, JFET, Diode models | ✅ Full |
| Behavioral sources (ABM/E source) | ✅ Full (use `B` source) |
| `.AC`, `.DC`, `.TRAN` analyses | ✅ Full |
| `.PARAM` and parametric sweeps | ✅ Full |
| `.PROBE` → `.PRINT` | ⚠️ Rename required |
| `.STEP` parameter sweeps | ⚠️ Syntax differs slightly |
| Stimulus files (`.STIM`) | ⚠️ Must convert to `PULSE()`/`PWL()` |
| Monte Carlo (`.MC`) | ⚠️ Use ngspice `.measure` + shell loop |
| Worst-case analysis | ❌ Not native — implement via parameter sweep |
| Behavioral models (`.SUBCKT`) | ✅ Full |
| Vendor `.lib` files | ✅ Most work directly |

---

## Step-by-Step Migration

### Step 1: Export netlist from OrCAD PSpice

1. Open your schematic in OrCAD Capture
2. Go to **PSpice → Create Netlist**
3. Select **PSpice** format → outputs a `.cir` file
4. Also export model libraries: **PSpice → Model Editor → Export**

### Step 2: Install ngspice

```bash
brew install ngspice          # macOS
sudo apt install ngspice      # Ubuntu/Debian
winget install ngspice.ngspice  # Windows (via winget)
```

### Step 3: Fix common syntax differences

Open the `.cir` file in a text editor and apply these substitutions:

```bash
# Rename .PROBE to .PRINT (or just delete — ngspice outputs to terminal)
sed -i 's/\.PROBE/\.PRINT TRAN/' design.cir

# Convert PSpice .STEP to ngspice .step syntax
# PSpice:   .STEP PARAM Rval LIST 1k 10k 100k
# ngspice:  .step param Rval list 1k 10k 100k
# (ngspice is case-insensitive — this usually works as-is)

# PSpice behavioral ABM sources use E source with VALUE={}
# ngspice uses B (behavioral) source:
# PSpice:   EOUT OUT GND VALUE = {V(IN)*2}
# ngspice:  BOUT OUT GND V = V(IN)*2
```

### Step 4: Run the simulation

```bash
ngspice design.cir
```

Or in batch mode (no GUI):

```bash
ngspice -b design.cir -o output.log
```

### Step 5: View results

ngspice outputs to `ngspice.out` or via its interactive terminal. For waveform viewing:

```bash
# Launch ngspice interactive with plot capability
ngspice design.cir
ngspice → plot V(out)
ngspice → plot I(R1)
```

Or use **Qucs-S** as a GUI front-end that can load ngspice raw output files:

```bash
# Load ngspice raw output in Qucs-S
qucs-s --rawfile output.raw
```

---

## Python Automation with PySpice

PySpice lets you describe circuits in Python and run ngspice programmatically — ideal for design space exploration and CI/CD.

```python
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

circuit = Circuit('RC Low-Pass Filter')

circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd,
                                 amplitude=1@u_V, frequency=1@u_kHz)
circuit.R(1, 'in', 'out', 1@u_kΩ)
circuit.C(1, 'out', circuit.gnd, 1@u_uF)

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(variation='dec', number_of_points=100,
                        start_frequency=100@u_Hz, stop_frequency=1@u_MHz)

import numpy as np
import matplotlib.pyplot as plt

frequency = np.array(analysis.frequency)
gain = 20 * np.log10(np.abs(np.array(analysis['out'])))

plt.semilogx(frequency, gain)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('RC Filter Frequency Response')
plt.grid(True)
plt.savefig('filter_response.png')
```

Run parametric sweeps across component values in a loop — something PSpice makes painful:

```python
results = {}
for r_value in [100, 1000, 10000]:
    circuit.R(1, 'in', 'out', r_value@u_Ω)
    analysis = simulator.ac(...)
    results[r_value] = analysis
```

---

## Loading Vendor SPICE Models

Most vendors publish PSpice-compatible `.lib` files. These work directly in ngspice:

```spice
* In your .cir file:
.LIB "vendor_model.lib"

* Or include a specific subcircuit:
.INCLUDE "TL072.lib"
```

Common sources for ngspice-compatible models:

- [SpiceModel.com](https://www.spicemodel.com) — aggregator
- Texas Instruments: `ti.com/design-resources/software/spice-models.html`
- Analog Devices: `analog.com/en/design-center/simulation-models.html`
- Microchip/Atmel: Device-specific `.lib` on product pages

---

## Replacing PSpice-Specific Features

### Worst-Case Analysis

PSpice has built-in worst-case. In ngspice, use parameter sweeps:

```spice
.param Rtol = 0.05
.param Rnom = 1000

* Sweep ±5% tolerance
.step param Rtol_val list -0.05 0 0.05
.param Rval = {Rnom * (1 + Rtol_val)}
R1 in out {Rval}
```

### Monte Carlo

Use ngspice with a shell script:

```bash
#!/bin/bash
for i in $(seq 1 1000); do
    # Generate random parameter file
    python generate_random_params.py > params.inc
    ngspice -b design.cir >> monte_carlo_results.txt
done
python analyze_results.py monte_carlo_results.txt
```

### Stimulus Files (`.STIM`)

PSpice `.STIM` converts to ngspice `PWL` (piecewise linear) or `PULSE`:

```spice
* PSpice:
VSTIM IN GND STIMULUS {CLK_1MHz}
.STIMULUS CLK_1MHz PWL REPEAT FOREVER (0,0) (500n,0) (500n,5) (1u,5) ENDREPEAT

* ngspice equivalent:
VCLK IN GND PULSE(0 5 0 1n 1n 500n 1u)
```

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `unknown device type` | PSpice-specific source type | Check compatibility table above |
| `no such node` | Floating net from `.PROBE` statement | Remove or replace `.PROBE` |
| `timestep too small` | Stiff circuit | Add `.options reltol=1e-3 abstol=1e-9` |
| Model not found | `.lib` path difference | Use absolute path or copy lib to working dir |
| `singular matrix` | Floating node or unsupported topology | Add small resistors to ground on floating nets |
| `SFW` behavioral source | PSpice-only construct | Rewrite as ngspice `B` source |

---

## Further Reading

- [ngspice User Manual](http://ngspice.sourceforge.net/docs/ngspice-html-manual/manual.xhtml)
- [PySpice Documentation](https://pyspice.fabrice-salvaire.fr)
- [Qucs-S with ngspice backend](https://github.com/ra3xdh/qucs_s)
- [ngspice vs PSpice syntax comparison (comprehensive)](http://ngspice.sourceforge.net/ngspice-vs-pspice.html)
