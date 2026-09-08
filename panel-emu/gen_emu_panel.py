#!/usr/bin/env python3
"""
E-mu Modular style front panel for the Strämpler main board — one-off,
6" x 6" (two 3" E-mu units), 1/4" Switchcraft jacks wired to the board's
3.5 mm jack pads with flying leads.

Outputs (all in mm, panel origin = bottom-left corner, Y up):
  emu_panel.svg   layered: CUT (red, 0.1 mm stroke) + ART (black text, blue lines)
  emu_panel_cut.dxf   cut layer only (outline + holes) for a mill / laser
  emu_panel_art.dxf   artwork only (text + lines) for engraving / marking
  emu_panel.png   preview render

Board-locked cutouts come from strampler_panel_v2_3.kicad_pcb (Antumbra 18 HP
panel, 91.3 x 128.5 mm) and are only translated by BOARD_ORIGIN. Everything
else is parametric — edit the CONFIG block.
"""
import math, os, sys

# ----------------------------------------------------------------- CONFIG
W, H = 152.4, 152.4                 # 6" x 6"
BOARD_ORIGIN = (6.35, 11.95)        # where the 91.3x128.5 board footprint sits
JACK_HOLE = 9.6                     # 3/8"-32 bushing (Switchcraft 11/111/112): 9.53 nominal
JACK_COLS = (113.0, 137.0)          # x of the two 1/4" jack columns
JACK_PITCH = 19.05                  # 3/4" row pitch, 7 rows
JACK_ROW0 = 19.05                   # y of the bottom row
MOUNT_HOLES = [(6.35, 6.35), (W-6.35, 6.35), (6.35, H-6.35), (W-6.35, H-6.35)]
MOUNT_DIA = 4.2                     # PLACEHOLDER — measure the cabinet rails
LED_HOLE = 3.2                      # 3 mm light pipe / bare 3 mm LED behind
INCLUDE_SD_SLOT = True              # kept "just in case" (Arlo 2026-09-07)
BLUE = "#2456A6"                    # E-mu accent blue
FONT = "Helvetica, Arial, sans-serif"

# jack field: (label, board ref, sublabel) top-to-bottom per column
JACKS = {
    0: [("IN L", "J2", ""), ("IN R", "J1", ""),
        ("CV 1  V/OCT", "J7", ""), ("CV 2  V/OCT", "J8", ""),
        ("CV 3  ±5V", "J11", ""), ("CV 4  ±5V", "J12", ""),
        ("TRIG 1", "J5", "")],
    1: [("CV 5", "J9", ""), ("CV 6", "J10", ""),
        ("CV 7", "J13", ""), ("CV 8", "J14", ""),
        ("TRIG 2", "J6", ""),
        ("OUT L", "J4", ""), ("OUT R", "J3", "")],
}

# ------------------------------------------------ board-locked geometry (v2_3)
bx, by = BOARD_ORIGIN
def B(x, y): return (bx + x, by + y)

POTS = [  # (x, y, dia, label)
    (13.903, 45.834, 7.2, "CV 5"), (35.117, 45.834, 7.2, "CV 6"),
    (56.33, 45.834, 7.2, "CV 7"), (77.544, 45.834, 7.2, "CV 8"),
    (13.903, 65.096, 7.2, "GAIN"),
    (77.544, 65.096, 8.2, "SELECT"),            # encoder SW1
]
BUTTONS = [(35.117, 65.096, 9.5, "1"), (56.33, 65.096, 9.5, "2")]   # SW2/SW3
LED = (45.65, 65.04)
ANT = (83.901, 97.693, 7.2)
SCREWS = [(4.741, 80.224), (86.723, 80.224), (4.741, 114.565), (86.723, 114.565), (45.65, 73.479)]
SCREW_DIA = 3.2
DISPLAY = (24.132, 80.405, 67.308, 112.981, 1.0)   # x0 y0 x1 y1 r
SD_SLOT = (3.488, 91.222, 5.995, 104.207)
# vacated 3.5 mm jack pads (for the flying-lead table only)
PADS = {"J2": (7.539, 29.346), "J5": (20.268, 29.346), "J7": (32.993, 29.346), "J8": (45.65, 29.346),
        "J11": (58.449, 29.346), "J12": (71.176, 29.346), "J4": (83.901, 29.346),
        "J1": (7.539, 16.646), "J6": (20.268, 16.646), "J9": (32.993, 16.646), "J10": (45.65, 16.646),
        "J13": (58.449, 16.646), "J14": (71.176, 16.646), "J3": (83.901, 16.646)}

# ----------------------------------------------------------------- build
cut, art = [], []          # SVG fragments
dxf_cut, dxf_art = [], []  # ezdxf ops as callables

def Y(y): return H - y     # SVG y-down

def circle(x, y, d, layer="cut"):
    (cut if layer == "cut" else art).append(f'<circle cx="{x:.3f}" cy="{Y(y):.3f}" r="{d/2:.3f}"/>')
    (dxf_cut if layer == "cut" else dxf_art).append(("circle", (x, y), d/2))

def rrect(x0, y0, x1, y1, r):
    cut.append(f'<rect x="{x0:.3f}" y="{Y(y1):.3f}" width="{x1-x0:.3f}" height="{y1-y0:.3f}" rx="{r:.3f}"/>')
    dxf_cut.append(("rrect", (x0, y0, x1, y1), r))

def line(x0, y0, x1, y1, w=0.5, color=BLUE):
    art.append(f'<line x1="{x0:.3f}" y1="{Y(y0):.3f}" x2="{x1:.3f}" y2="{Y(y1):.3f}" stroke="{color}" stroke-width="{w}"/>')
    dxf_art.append(("line", (x0, y0), (x1, y1)))

def text(x, y, s, size=2.6, anchor="middle", weight="bold", color="#000"):
    art.append(f'<text x="{x:.3f}" y="{Y(y):.3f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
               f'text-anchor="{anchor}" fill="{color}">{s}</text>')
    dxf_art.append(("text", (x, y), s, size, anchor))

# outline
cut.append(f'<rect x="0" y="0" width="{W}" height="{H}"/>')
dxf_cut.append(("rect", (0, 0, W, H)))
for (x, y) in MOUNT_HOLES: circle(x, y, MOUNT_DIA)

# board-locked
for (x, y, d, lab) in POTS:
    px, py = B(x, y); circle(px, py, d); text(px, py + d/2 + 5.5, lab, 2.6)
for (x, y, d, lab) in BUTTONS:
    px, py = B(x, y); circle(px, py, d); text(px, py + d/2 + 2.2, lab, 2.4)
lx, ly = B(*LED); circle(lx, ly, LED_HOLE)
ax, ay, ad = ANT; px, py = B(ax, ay); circle(px, py, ad); text(px, py - ad/2 - 3.2, "ANT", 2.2)
for (x, y) in SCREWS:
    px, py = B(x, y); circle(px, py, SCREW_DIA)
x0, y0, x1, y1, r = DISPLAY
rrect(bx + x0, by + y0, bx + x1, by + y1, r)
if INCLUDE_SD_SLOT:
    sx0, sy0, sx1, sy1 = SD_SLOT; rrect(bx + sx0, by + sy0, bx + sx1, by + sy1, 0.3)

# 1/4" jack field
for col, xs in enumerate(JACK_COLS):
    rows = JACKS[col]
    for i, (lab, ref, sub) in enumerate(rows):
        y = JACK_ROW0 + (len(rows) - 1 - i) * JACK_PITCH
        circle(xs, y, JACK_HOLE)
        text(xs, y + JACK_HOLE/2 + 2.4, lab, 2.6 if len(lab) <= 6 else 2.2)

# E-mu style dress: blue rules + wordmark block in the vacated jack strip
strip_x0, strip_x1 = bx + 2, bx + 89
line(strip_x0, by + 40, strip_x1, by + 40, 0.6)
line(strip_x0, by + 6, strip_x1, by + 6, 0.6)
text((strip_x0 + strip_x1)/2, by + 26, "STRÄMPLER", 7.0)
text((strip_x0 + strip_x1)/2, by + 17.5, "MULTI-MACHINE SAMPLE STREAMER", 2.4, weight="normal")
text((strip_x0 + strip_x1)/2, by + 10.5, "6\" E-mu FORMAT · 1/4\" I/O", 1.9, weight="normal", color=BLUE)
# jack field frame
fx0, fx1 = JACK_COLS[0] - 10.5, JACK_COLS[1] + 10.5
fy0, fy1 = JACK_ROW0 - 9.5, JACK_ROW0 + 6*JACK_PITCH + 9.5
for (xa, ya, xb, yb) in [(fx0, fy0, fx1, fy0), (fx0, fy1, fx1, fy1), (fx0, fy0, fx0, fy1), (fx1, fy0, fx1, fy1)]:
    line(xa, ya, xb, yb, 0.5)
line(bx + 89 + 2, by + 128.5 - 4, bx + 89 + 2, by + 4, 0.5)   # divider board | jacks

# ------------------------------------------------------------ write SVG
out = os.path.dirname(os.path.abspath(__file__))
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" fill="#d9dcdf"/>',   # brushed-aluminum stand-in
       '<g id="ART">', *art, '</g>',
       '<g id="CUT" fill="none" stroke="#e00" stroke-width="0.1">', *cut, '</g>',
       '</svg>']
open(os.path.join(out, "emu_panel.svg"), "w").write("\n".join(svg))

# ------------------------------------------------------------ write DXF
import ezdxf
def write_dxf(path, ops, layer):
    doc = ezdxf.new("R2010"); doc.units = ezdxf.units.MM
    doc.layers.add(layer)
    msp = doc.modelspace(); a = {"layer": layer}
    for op in ops:
        k = op[0]
        if k == "circle": msp.add_circle(op[1], op[2], dxfattribs=a)
        elif k == "rect":
            x0, y0, x1, y1 = op[1]; msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs=a)
        elif k == "rrect":
            (x0, y0, x1, y1), r = op[1], op[2]
            pts = []
            for (cx, cy, a0) in [(x1-r, y1-r, 0), (x0+r, y1-r, 90), (x0+r, y0+r, 180), (x1-r, y0+r, 270)]:
                for t in range(0, 91, 15):
                    ang = math.radians(a0 + t); pts.append((cx + r*math.cos(ang), cy + r*math.sin(ang)))
            msp.add_lwpolyline(pts, close=True, dxfattribs=a)
        elif k == "line": msp.add_line(op[1], op[2], dxfattribs=a)
        elif k == "text":
            (x, y), s, size, anchor = op[1], op[2], op[3], op[4]
            align = {"middle": "MIDDLE_CENTER", "start": "MIDDLE_LEFT", "end": "MIDDLE_RIGHT"}[anchor]
            msp.add_text(s, height=size*0.72, dxfattribs=a).set_placement((x, y + size*0.35), align=getattr(ezdxf.enums.TextEntityAlignment, align))
    doc.saveas(path)
write_dxf(os.path.join(out, "emu_panel_cut.dxf"), dxf_cut, "CUT")
write_dxf(os.path.join(out, "emu_panel_art.dxf"), dxf_art, "ART")

# ------------------------------------------------------------ preview PNG
try:
    import fitz
    d = fitz.open(os.path.join(out, "emu_panel.svg"))
    d[0].get_pixmap(dpi=200).save(os.path.join(out, "emu_panel.png"))
except Exception as e:
    print("preview skipped:", e)

# ------------------------------------------------------------ report
print(f"panel {W} x {H} mm; board footprint at {BOARD_ORIGIN}; {sum(1 for o in dxf_cut if o[0]=='circle')} round holes")
print("flying-lead table (pad on board -> 1/4\" jack):")
for col, xs in enumerate(JACK_COLS):
    rows = JACKS[col]
    for i, (lab, ref, sub) in enumerate(rows):
        y = JACK_ROW0 + (len(rows) - 1 - i) * JACK_PITCH
        px, py = B(*PADS[ref])
        print(f"  {ref:>3} {lab:6} pad@({px:6.2f},{py:6.2f}) -> jack@({xs:6.2f},{y:6.2f})  lead ~{math.hypot(xs-px, y-py)+15:.0f} mm")
