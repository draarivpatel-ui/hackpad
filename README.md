# AarivPad - 3x3 Mechanical Macropad + EC11 Rotary Encoder + OLED

A custom 3x3 mechanical macropad powered by a **Seeed Studio XIAO RP2040**, an **Alps EC11 rotary encoder** with push switch, a **0.91" 128x32 SSD1306 I2C OLED display**, and four **SK6812 MINI-E reverse-mount RGB underglow LEDs**, built for the Hack Club Stardance **Hackpad** mission.

![AarivPad Interactive Workbench and Hardware Inspector](screenshot.png)

Live Interactive Workbench & 3D Hardware Inspector: https://aariv.me/hackpad/

## Repository Structure

- `pcb/aarivpad.kicad_pro`, `pcb/aarivpad.kicad_sch`, `pcb/aarivpad.kicad_pcb`: Complete KiCad 8 project, schematic, and routed 2-layer PCB (68.0mm x 84.0mm, 19.05mm MX switch spacing, M2 mounting holes, `F.Cu` and `B.Cu` ground pours).
- `pcb/gerbers/aarivpad-gerbers.zip`: Fabrication-ready Gerber RS-274X layers (`F_Cu.gtl`, `B_Cu.gbl`, `F_Mask.gts`, `B_Mask.gbs`, `F_SilkS.gto`, `B_SilkS.gbo`, `Edge_Cuts.gm1`) and Excellon drill file (`aarivpad.drl`) ready for JLCPCB.
- `pcb/bom.csv`: Complete Bill of Materials matching the official Hackpad kit components.
- `cad/aarivpad_case.scad`, `cad/bottom_case.stl`, `cad/switch_plate.stl`, `cad/encoder_knob.stl`: Parametric OpenSCAD enclosure source and triangulated STL meshes (~58g PLA total, well under the 300g Printing Legion limit).
- `firmware/code.py`: CircuitPython + KMK firmware implementing a 3-layer keymap (Git/Terminal workflow, Media/RGB control, and KiCad/CAD viewport navigation), rotary encoder acceleration, and live 128x32 SSD1306 OLED status rendering.
- `index.html`: Zero-dependency browser simulator and hardware inspector featuring an interactive 3D exploded CAD view, 2-layer PCB viewer, and playable 9-key + EC11 KMK simulator with Web Audio switch clicks.

## XIAO RP2040 Pinout & Matrix Wiring

| Seeed XIAO RP2040 Pin | Net Name | Connected Hardware |
| --- | --- | --- |
| `D0 / GPIO26` | `COL0` | Column 0 Switch Bus (`SW1`, `SW4`, `SW7`) |
| `D1 / GPIO27` | `COL1` | Column 1 Switch Bus (`SW2`, `SW5`, `SW8`) |
| `D2 / GPIO28` | `COL2` | Column 2 Switch Bus (`SW3`, `SW6`, `SW9`) |
| `D3 / GPIO29` | `ROW0` | Row 0 Diode Bus (`D1`, `D2`, `D3` cathodes) |
| `D6 / GPIO0` | `ROW1` | Row 1 Diode Bus (`D4`, `D5`, `D6` cathodes) |
| `D7 / GPIO1` | `ROW2` | Row 2 Diode Bus (`D7`, `D8`, `D9` cathodes) |
| `D4 / GPIO6 (SDA)` | `I2C_SDA` | 0.91" 128x32 SSD1306 OLED Display (`SDA`) |
| `D5 / GPIO7 (SCL)` | `I2C_SCL` | 0.91" 128x32 SSD1306 OLED Display (`SCL`) |
| `D8 / GPIO2` | `ENC_A` | EC11 Rotary Encoder Phase A |
| `D9 / GPIO4` | `ENC_B` | EC11 Rotary Encoder Phase B |
| `D10 / GPIO3` | `ENC_SW` | EC11 Push Switch + SK6812 RGB Underglow Chain |
| `3V3 / 5V / GND` | Power | OLED `VCC` (`3V3`), SK6812 `VDD` (`5V`), Common Ground |

## Bill of Materials (Hackpad Kit Compatible)

| Ref | Qty | Component | Footprint / Package |
| --- | --- | --- | --- |
| `U1` | 1 | Seeed Studio XIAO RP2040 | Through-hole / SMD 14-pin Module |
| `SW1-SW9` | 9 | Cherry MX / Gateron 5-Pin Mechanical Switches | `SW_Cherry_MX_1.00u_PCB` |
| `D1-D9` | 9 | 1N4148W / 1N4148 Switching Diodes | `D_SOD-123` (THT compatible pads) |
| `SW10` | 1 | Alps EC11 Rotary Encoder with Push Switch | `RotaryEncoder_Alps_EC11E-Switch` |
| `U2` | 1 | 0.91" 128x32 SSD1306 I2C OLED Display | 4-Pin 2.54mm Header (`GND/VCC/SCL/SDA`) |
| `LED1-LED4` | 4 | SK6812 MINI-E Addressable RGB LEDs | Reverse-Mount `PLCC4 3.2x2.8mm` |
| `K1-K9` | 9 | 1u Blank DSA PBT Keycaps | Standard MX Stem |
| `H1-H4` | 4 | M2x8mm Screws + M2x5mm Brass Heat-Set Inserts | 2.2mm Mounting Holes |

## Why I built this

When switching between terminal Git sessions, KiCad PCB layout, and media playback, I kept reaching for multi-finger chord shortcuts (`git status`, `git diff --stat`, `git log --oneline`, tmux panes, and KiCad layer/track hotkeys). Designing `AarivPad` around a 3x3 matrix with a dedicated EC11 encoder and a 128x32 OLED status bar puts all nine single-tap macros and a tactile rotary dial right next to my mouse, while keeping the entire PCB on a clean two-layer 68mm x 84mm footprint.

## Honest AI note

Built by AI coding agents (ZCode) under Aariv Patel's direction for the Hack Club Stardance Hackpad mission: Aariv defined the 3x3 + EC11 + OLED hardware architecture and macro layers and reviewed the resulting design files and interactive workbench.

## License

MIT.
