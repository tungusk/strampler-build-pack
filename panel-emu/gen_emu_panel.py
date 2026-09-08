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
BOARD_ORIGIN = (54.75, 18.0)        # board footprint at the RIGHT, raised so a jack row fits under the PCB (PCB spans y 10.25..118.25 of the region)
JACK_HOLE = 9.6                     # 3/8"-32 bushing (Switchcraft 11/111/112): 9.53 nominal
JACK_COLS = (15.4, 39.4)            # x of the two 1/4" jack columns (LEFT side)
JACK_PITCH = 24.0                   # row pitch, 5 rows on the left (was 1"; tightened to make room for the bus toggles)
JACK_ROW0 = 17.0                    # y of the bottom row (shared by the left field and the CV 5-8 row)
MOUNT_HOLES = [(6.35, 6.35), (W-6.35, 6.35), (6.35, H-6.35), (W-6.35, H-6.35)]
MOUNT_DIA = 4.2                     # cabinet has WOOD rails (Arlo 09-07): clearance for #6 wood screws; 3.6 for #4. Match the neighbours' inset by eye.
LED_HOLE = 3.2                      # 3 mm light pipe / bare 3 mm LED behind
INCLUDE_SD_SLOT = True              # kept "just in case" (Arlo 2026-09-07)
BLUE = "#2456A6"                    # E-mu accent blue
FONT = "Helvetica, Arial, sans-serif"

# left jack field: rows top-to-bottom, each row = (left jack, right jack) as (label, board ref)
JACK_ROWS = [
    (("TR1", "J5"), ("TR2", "J6")),
    (("1  V/OCT", "J7"), ("2  V/OCT", "J8")),
    (("3  ±5V", "J11"), ("4  ±5V", "J12")),
    (("IN L", "J2"),  ("IN R", "J1")),
    (("OUT L", "J4"), ("OUT R", "J3")),
]
# bus-select toggles (E-mu keyboard / trigger buses), in the padding above the top row.
# 3-position ON-OFF-ON: up = bus A, centre = off (jack un-normalled), down = bus B.
# Feeds the SWITCHING jacks listed in NORMALLED via their tip-shunt (normal) lug.
TOGGLE_HOLE = 6.5                   # 1/4"-40 bushing (C&K 7203 DPDT ON-OFF-ON / generic MTS-203)
# ONE ganged E-mu-style KYBD switch (up = keyboard 1, centre = off, down = keyboard 2), 2 poles:
#   pole A: VOICE 1/2 -> jack 1 normal lug, pole B: GATE 1/2 -> TR1.  TR2 stays plain (Arlo 09-07:
#   TR1/TR2 are independent trigger inputs to the firmware, so driving both from one key is redundant).
# targets: (jack ref, route) where route = "down" (straight down between the columns) or ("side", x_run)
TOGGLES = [(27.4, 131.5, "KYBD: 1 · TR1", [])]   # targets named in the label; no indicator lines (Arlo 09-07)
NORMALLED = {"J7": "VOICE 1/2 (kbd CV)", "J5": "GATE 1/2"}   # Switchcraft 12A/112A; TR2 plain

# bottom row under the PCB, one jack directly below each CV knob (x = knob x)
BOTTOM_JACKS = [("5", "J9", 13.903), ("6", "J10", 35.117), ("7", "J13", 56.33), ("8", "J14", 77.544)]

# ------------------------------------------------ board-locked geometry (v2_3)
bx, by = BOARD_ORIGIN
def B(x, y): return (bx + x, by + y)

POTS = [  # (x, y, dia, label)
    (13.903, 45.834, 7.2, ""), (35.117, 45.834, 7.2, ""),
    (56.33, 45.834, 7.2, ""), (77.544, 45.834, 7.2, ""),       # attenuator knobs: unlabelled, jack "5".."8" sits directly below
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

def art_box(x0, y0, x1, y1, r=3.0, w=0.6, color=BLUE):
    art.append(f'<rect x="{x0:.3f}" y="{Y(y1):.3f}" width="{x1-x0:.3f}" height="{y1-y0:.3f}" rx="{r:.3f}" '
               f'fill="none" stroke="{color}" stroke-width="{w}"/>')
    dxf_art.append(("rrect", (x0, y0, x1, y1), r))

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
    px, py = B(x, y); circle(px, py, d)
    if lab: text(px, py + d/2 + 5.5, lab, 2.6)
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
def jack_positions():
    for i, row in enumerate(JACK_ROWS):
        y = JACK_ROW0 + (len(JACK_ROWS) - 1 - i) * JACK_PITCH
        for xs, (lab, ref) in zip(JACK_COLS, row):
            yield lab, ref, xs, y
    for lab, ref, kx in BOTTOM_JACKS:
        yield lab, ref, bx + kx, JACK_ROW0
for lab, ref, xs, y in jack_positions():
    circle(xs, y, JACK_HOLE)
    text(xs, y + JACK_HOLE/2 + 2.4, lab, 2.6 if len(lab) <= 6 else 2.2)

# bus toggle + indicator lines to the jacks it normals
def find_jack(ref):
    for lab, r, x, y in jack_positions():
        if r == ref: return x, y
for (tx, ty, lab, targets) in TOGGLES:
    circle(tx, ty, TOGGLE_HOLE)
    text(tx, ty + TOGGLE_HOLE/2 + 2.0, lab, 2.0)
    text(tx + TOGGLE_HOLE/2 + 1.2, ty + 2.2, "1", 1.8, anchor="start", weight="normal")
    text(tx + TOGGLE_HOLE/2 + 1.2, ty - 3.4, "2", 1.8, anchor="start", weight="normal")
    for ref, route in targets:
        jx, jy = find_jack(ref)
        if route == "down":
            pts = [(tx, ty - TOGGLE_HOLE/2), (tx, jy), (jx + (JACK_HOLE/2 + 0.4)*(1 if tx > jx else -1), jy)]
        else:
            rx = route[1]; sgn = 1 if rx > tx else -1
            pts = [(tx + sgn*TOGGLE_HOLE/2, ty), (rx, ty), (rx, jy), (jx + (JACK_HOLE/2 + 0.4)*(1 if rx > jx else -1), jy)]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            line(xa, ya, xb, yb, 0.3)

# ±12 V regulators (7812 / 7912, TO-220) bolted flat to the back of the panel — the panel is the heatsink.
# Tab holes only; bodies lie horizontally in the top strip, pins toward the panel centre.
REG_HOLES = [(60.0, 145.5, "7812"), (120.0, 145.5, "7912 (insulate tab)")]
for (x, y, lab) in REG_HOLES:
    circle(x, y, 3.2)

# E-mu style dress: rounded blue boxes (left field, interface block, bottom row); wordmark plain
art_box(bx + 1.5, by + 38.5, bx + 89.8, by + 121.0, r=3.0)   # display, SD, ANT, pots, buttons, LED
art_box(bx + 1.5, JACK_ROW0 - 7.5, bx + 89.8, JACK_ROW0 + 12.5, r=3.0)   # CV 5-8 row, same width as the interface box
wx = bx + 91.3/2
text(wx, (by + 38.5 + JACK_ROW0 + 12.5)/2 - 6.5*0.35, "CTAG STRÄMPLER", 6.5)   # centred in the band (baseline shifted by ~cap height/2)
fx0, fx1 = JACK_COLS[0] - 10.5, JACK_COLS[1] + 10.5
fy0, fy1 = JACK_ROW0 - 7.5, by + 121.0   # top aligned with the interface box (padding above the top row)
art_box(fx0, fy0, fx1, fy1, r=3.0)

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
for lab, ref, xs, y in jack_positions():
    px, py = B(*PADS[ref])
    print(f"  {ref:>3} {lab:12} pad@({px:6.2f},{py:6.2f}) -> jack@({xs:6.2f},{y:6.2f})  lead ~{math.hypot(xs-px, y-py)+15:.0f} mm")
