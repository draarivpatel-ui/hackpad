# AarivPad build log

## 2026-10-25 - Schematic, 2-layer PCB routing, OpenSCAD case, and KMK firmware

1. **Schematic and matrix pinout (`pcb/aarivpad.kicad_sch`)**:
   - Wired a 3x3 Cherry MX mechanical switch matrix (`SW1`..`SW9`) with nine `1N4148W` SOD-123 anti-ghosting diodes (`D1`..`D9`) in `COL2ROW` orientation to a Seeed Studio XIAO RP2040 (`U1`).
   - Assigned `COL0`..`COL2` to `D0`..`D2` (`GPIO26`..`GPIO28`), `ROW0`..`ROW2` to `D3`, `D6`, `D7` (`GPIO29`, `GPIO0`, `GPIO1`), the 0.91" 128x32 SSD1306 I2C OLED (`U2`) to hardware I2C on `D4`/`D5` (`SDA`/`SCL`), and the Alps EC11 rotary encoder (`SW10`) to `D8`/`D9` (quadrature A/B) and `D10` (push switch).
   - Added four reverse-mount `SK6812 MINI-E` addressable RGB LEDs (`LED1`..`LED4`) around the perimeter for underglow illumination.
2. **2-layer PCB layout and Gerbers (`pcb/aarivpad.kicad_pcb`, `pcb/gerbers/aarivpad-gerbers.zip`)**:
   - Placed the 3x3 switch matrix on standard 19.05mm (0.75") key spacing inside a compact 68.0mm x 84.0mm board outline with four M2 mounting holes at 4.0mm corner offsets.
   - Routed row buses and I2C signals on `F.Cu`, column buses and encoder switch return on `B.Cu`, and poured stitched `GND` copper zones across both layers.
   - Plotted JLCPCB-ready Gerber layers (`F_Cu.gtl`, `B_Cu.gbl`, `F_Mask.gts`, `B_Mask.gbs`, `F_SilkS.gto`, `B_SilkS.gbo`, `Edge_Cuts.gm1`) and Excellon drill file (`aarivpad.drl`), archived into `pcb/gerbers/aarivpad-gerbers.zip`.
3. **3D-printable enclosure (`cad/aarivpad_case.scad`, `cad/*.stl`)**:
   - Modeled the M2 heat-set bottom tray (`bottom_case.stl`), 3.0mm clip-in MX switch plate with OLED viewport and encoder cutout (`switch_plate.stl`), and 6mm D-shaft knurled rotary knob (`encoder_knob.stl`). Total print weight is ~58g PLA, well under the 300g Printing Legion allowance.
4. **KMK firmware and interactive browser workbench (`firmware/code.py`, `index.html`)**:
   - Wrote the CircuitPython KMK firmware with three layers (Layer 0: Git and Terminal shortcuts; Layer 1: Media and RGB underglow controls; Layer 2: KiCad and 3D CAD navigation), rotary encoder scrubbing, and live SSD1306 128x32 OLED status updates.
   - Built `index.html` so reviewers can test all 9 keys across all 3 layers, turn the EC11 encoder, watch the simulated 128x32 OLED update, orbit the 3D exploded CAD assembly, and toggle the 2-layer KiCad PCB copper/silkscreen layers in the browser.
