# AarivPad - 3x3 Mechanical Macropad + EC11 Rotary Encoder + 128x32 OLED + SK6812 Underglow
# Target MCU: Seeed Studio XIAO RP2040 (CircuitPython + KMK Firmware)
# Pinout matches pcb/aarivpad.kicad_pcb:
#   Columns: COL0=D0 (GPIO26), COL1=D1 (GPIO27), COL2=D2 (GPIO28)
#   Rows:    ROW0=D3 (GPIO29), ROW1=D6 (GPIO0),  ROW2=D7 (GPIO1)
#   I2C OLED (SSD1306 128x32): SDA=D4 (GPIO6), SCL=D5 (GPIO7)
#   EC11 Encoder: A=D8 (GPIO2), B=D9 (GPIO4), SW=D10 (GPIO3)
#   SK6812 RGB Underglow (4 pixels): NEOPIXEL / Status LED chain

import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes

keyboard = KMKKeyboard()

# Matrix configuration (3 columns x 3 rows, 1N4148W SOD-123 diodes COL2ROW)
keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D6, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Load KMK modules & extensions
layers = Layers()
encoder_handler = EncoderHandler()
media_keys = MediaKeys()

# 4x SK6812 MINI-E Reverse-Mount Underglow LEDs
rgb = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=4,
    val_limit=120,
    hue_default=145,
    sat_default=255,
    val_default=90,
    animation_mode=AnimationModes.BREATHING_RAINBOW,
)

keyboard.modules = [layers, encoder_handler]
keyboard.extensions = [media_keys, rgb]

# Configure EC11 Rotary Encoder (Pin A = D8, Pin B = D9, Push Switch = D10)
encoder_handler.pins = ((board.D8, board.D9, board.D10, False),)

# Useful composite shortcuts for Git, Terminal, and CAD workflows
GIT_ST  = KC.MACRO("git status\n")
GIT_DF  = KC.MACRO("git diff --stat\n")
GIT_LG  = KC.MACRO("git log --oneline -n 8\n")
GIT_PL  = KC.MACRO("git pull --rebase\n")
GIT_CM  = KC.MACRO('git commit -m ""')
GIT_PS  = KC.MACRO("git push\n")
TMUX_SP = KC.LCTL(KC.B)
TERM_CL = KC.LCTL(KC.L)

# 3 Layers:
# Layer 0: DEV / GIT (Git status, diff, log, pull, commit, push, tmux prefix, clear, cycle layer)
# Layer 1: MEDIA / STREAM (Mute, Play/Pause, Next, Prev, Vol-, Vol+, RGB Toggle, Hue+, cycle layer)
# Layer 2: CAD / KICAD (Home view, Top view, Front view, DRC check, Route track, Add via, 3D viewer, Zoom fit, cycle layer)
keyboard.keymap = [
    # Layer 0: Git & Terminal Workflow
    [
        GIT_ST,   GIT_DF,   GIT_LG,
        GIT_PL,   GIT_CM,   GIT_PS,
        TMUX_SP,  TERM_CL,  KC.TO(1),
    ],
    # Layer 1: Media & Underglow Control
    [
        KC.MPRV,    KC.MPLY,    KC.MNXT,
        KC.VOLD,    KC.MUTE,    KC.VOLU,
        KC.RGB_TOG, KC.RGB_HUI, KC.TO(2),
    ],
    # Layer 2: KiCad & 3D CAD Navigation
    [
        KC.HOME,       KC.KP_7,       KC.KP_1,
        KC.X,          KC.V,          KC.B,
        KC.LALT(KC.N3), KC.F1,        KC.TO(0),
    ],
]

# Rotary Encoder per-layer mapping: (CCW, CW, Push)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.MUTE),),           # Layer 0: System Volume & Mute
    ((KC.RGB_VAD, KC.RGB_VAI, KC.RGB_M_BR),), # Layer 1: Underglow Brightness & Mode
    ((KC.MW_DN, KC.MW_UP, KC.MB_MMB),),       # Layer 2: CAD Canvas Zoom & Pan Click
]

# Initialize 0.91" 128x32 SSD1306 I2C OLED on D4 (SDA) and D5 (SCL)
displayio.release_displays()
OLED_NAMES = {
    0: "L0: GIT / TERM",
    1: "L1: MEDIA / RGB",
    2: "L2: KICAD / CAD",
}

try:
    i2c = busio.I2C(board.D5, board.D4)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

    splash = displayio.Group()
    title_lbl = label.Label(terminalio.FONT, text="AARIVPAD v1.0", color=0xFFFFFF, x=2, y=6)
    layer_lbl = label.Label(terminalio.FONT, text=OLED_NAMES[0], color=0xFFFFFF, x=2, y=18)
    status_lbl = label.Label(terminalio.FONT, text="ENC:VOL  RGB:ON", color=0xFFFFFF, x=2, y=28)
    splash.append(title_lbl)
    splash.append(layer_lbl)
    splash.append(status_lbl)
    oled.root_group = splash

    class OLEDLayerStatus(Layers):
        def after_hid_send(self, keyboard):
            super().after_hid_send(keyboard)
            active = keyboard.active_layers[0]
            layer_lbl.text = OLED_NAMES.get(active, "L0: GIT / TERM")

    keyboard.modules[0] = OLEDLayerStatus()
except Exception:
    # Allow keyboard operation even if OLED is disconnected during bench testing
    pass

if __name__ == "__main__":
    keyboard.go()
