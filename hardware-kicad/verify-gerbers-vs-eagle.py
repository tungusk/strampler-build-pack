#!/usr/bin/env python3
"""Compare Eagle .brd geometry against KiCad-plotted gerbers/drills, independent of KiCad."""
import math, re, sys, xml.etree.ElementTree as ET
from collections import defaultdict

# ---------------- Eagle parsing ----------------

def rot_parse(rot):
    """Eagle rot attr like 'R90', 'MR180', 'SR0' -> (mirror, angle_deg)."""
    if not rot:
        return False, 0.0
    m = re.match(r'^([SM]*)R([0-9.]+)$', rot)
    if not m:
        raise ValueError(f"rot {rot}")
    return ('M' in m.group(1)), float(m.group(2))

def xform(px, py, mirror, angle, ox, oy):
    """Transform package-local point into board coords.
    Eagle applies rotation FIRST, then mirrors about the Y axis (verified against
    routed-track endpoints landing exactly on transformed pad centers)."""
    a = math.radians(angle)
    c, s = math.cos(a), math.sin(a)
    rx, ry = px * c - py * s, px * s + py * c
    if mirror:
        rx = -rx
    return (ox + rx, oy + ry)

class Eagle:
    def __init__(self, path):
        self.root = ET.parse(path).getroot()
        self.packages = {}  # (lib, pkg) -> element
        for lib in self.root.iter('library'):
            ln = lib.get('name')
            for pkg in lib.iter('package'):
                self.packages[(ln, pkg.get('name'))] = pkg
        brd = self.root.find('.//board')
        self.plain = brd.find('plain')
        self.elements = list(brd.find('elements')) if brd.find('elements') is not None else []
        self.signals = list(brd.find('signals')) if brd.find('signals') is not None else []

    def holes(self):
        """Return (pth, npth) lists of (x, y, drill_dia).
        PTH: pads (in packages, transformed) + vias. NPTH: <hole> in plain and packages."""
        pth, npth = [], []
        for el in self.elements:
            pkg = self.packages[(el.get('library'), el.get('package'))]
            mirror, angle = rot_parse(el.get('rot'))
            ox, oy = float(el.get('x')), float(el.get('y'))
            for pad in pkg.iter('pad'):
                x, y = xform(float(pad.get('x')), float(pad.get('y')), mirror, angle, ox, oy)
                pth.append((x, y, float(pad.get('drill'))))
            for h in pkg.iter('hole'):
                x, y = xform(float(h.get('x')), float(h.get('y')), mirror, angle, ox, oy)
                npth.append((x, y, float(h.get('drill'))))
        for sig in self.signals:
            for via in sig.iter('via'):
                pth.append((float(via.get('x')), float(via.get('y')), float(via.get('drill'))))
        if self.plain is not None:
            for h in self.plain.iter('hole'):
                npth.append((float(h.get('x')), float(h.get('y')), float(h.get('drill'))))
        return pth, npth

    def wires(self, layers):
        """All signal+plain wires on given Eagle layer numbers -> list of (x1,y1,x2,y2,width,curve)."""
        out = []
        for sig in self.signals:
            for w in sig.iter('wire'):
                if int(w.get('layer')) in layers:
                    out.append(tuple(float(w.get(k)) for k in ('x1', 'y1', 'x2', 'y2', 'width')) + (float(w.get('curve') or 0),))
        if self.plain is not None:
            for w in self.plain.iter('wire'):
                if int(w.get('layer')) in layers:
                    out.append(tuple(float(w.get(k)) for k in ('x1', 'y1', 'x2', 'y2', 'width')) + (float(w.get('curve') or 0),))
        return out

    def smds(self, layer):
        """SMD pads landing on Eagle layer (1 top/16 bottom) -> (x, y, dx, dy, total_rot%180)."""
        out = []
        for el in self.elements:
            pkg = self.packages[(el.get('library'), el.get('package'))]
            emir, eang = rot_parse(el.get('rot'))
            ox, oy = float(el.get('x')), float(el.get('y'))
            for smd in pkg.iter('smd'):
                slayer = int(smd.get('layer'))
                eff_layer = ({1: 16, 16: 1}.get(slayer, slayer)) if emir else slayer
                if eff_layer != layer:
                    continue
                smir, sang = rot_parse(smd.get('rot'))
                x, y = xform(float(smd.get('x')), float(smd.get('y')), emir, eang, ox, oy)
                ang = (sang * (-1 if emir else 1) + eang * (-1 if emir else 1)) % 180
                out.append((x, y, float(smd.get('dx')), float(smd.get('dy')), ang))
        return out

    def polygons(self, layers):
        """Copper polygons on layers -> list of (layer, [pts], width)."""
        out = []
        for sig in self.signals:
            for p in sig.iter('polygon'):
                if int(p.get('layer')) in layers:
                    pts = [(float(v.get('x')), float(v.get('y'))) for v in p.iter('vertex')]
                    out.append((int(p.get('layer')), pts, float(p.get('width'))))
        return out

# ---------------- Excellon parsing ----------------

def parse_drl(path):
    tools, cur, out = {}, None, []
    for line in open(path):
        line = line.strip()
        m = re.match(r'^T(\d+)C([0-9.]+)$', line)
        if m:
            tools[m.group(1)] = float(m.group(2)); continue
        m = re.match(r'^T(\d+)$', line)
        if m:
            cur = m.group(1); continue
        m = re.match(r'^X(-?[0-9.]+)Y(-?[0-9.]+)$', line)
        if m and cur in tools:
            out.append((float(m.group(1)), float(m.group(2)), tools[cur]))
    return out

# ---------------- Gerber (RS-274X) parsing ----------------

class Gerber:
    """Minimal KiCad-output parser: apertures, flashes, draws, regions."""
    def __init__(self, path):
        self.apertures = {}   # dcode -> (shape, params)
        self.flashes = []     # (x, y, dcode)
        self.draws = []       # (x1,y1,x2,y2,dcode,interp)  interp: 1 lin, 2/3 arc
        self.arcs = []        # (x1,y1,x2,y2,i,j,dcode,dir)
        self.regions = []     # list of [pts]
        self._parse(path)

    def _parse(self, path):
        text = open(path).read()
        cx = cy = 0.0
        dcode = None
        interp = 1
        in_region = False
        region_pts = []
        scale = 1e-6
        for raw in re.split(r'\*', text):
            cmd = raw.strip(' \t\r\n%')
            if not cmd:
                continue
            m = re.match(r'^ADD(\d+)([A-Za-z_][\w]*),([0-9.X]+)$', cmd)
            if m:
                self.apertures[int(m.group(1))] = (m.group(2), [float(v) for v in m.group(3).split('X')])
                continue
            if cmd.startswith(('TF', 'TA', 'TO', 'TD', 'G04', 'FSLA', 'MOMM', 'LPD', 'LPC', 'IPPOS')):
                continue
            if cmd == 'G36':
                in_region, region_pts = True, [(cx, cy)]
                continue
            if cmd == 'G37':
                in_region = False
                if len(region_pts) > 2:
                    self.regions.append(region_pts)
                region_pts = []
                continue
            m = re.match(r'^G0*([123])$', cmd)
            if m:
                interp = int(m.group(1)); continue
            m = re.match(r'^D(\d+)$', cmd)
            if m:
                d = int(m.group(1))
                if d >= 10:
                    dcode = d
                continue
            m = re.match(r'^(?:G0*([123]))?(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?D0*([123])$', cmd)
            if m:
                if m.group(1):
                    interp = int(m.group(1))
                nx = cx if m.group(2) is None else float(m.group(2)) * scale
                ny = cy if m.group(3) is None else float(m.group(3)) * scale
                i = 0.0 if m.group(4) is None else float(m.group(4)) * scale
                j = 0.0 if m.group(5) is None else float(m.group(5)) * scale
                op = int(m.group(6))
                if op == 3:
                    self.flashes.append((nx, ny, dcode))
                elif op == 1:
                    if in_region:
                        region_pts.append((nx, ny))
                    elif interp == 1:
                        self.draws.append((cx, cy, nx, ny, dcode, 1))
                    else:
                        self.arcs.append((cx, cy, nx, ny, i, j, dcode, interp))
                elif op == 2 and in_region:
                    if len(region_pts) > 2:
                        self.regions.append(region_pts)
                    region_pts = [(nx, ny)]
                cx, cy = nx, ny
                continue
            if cmd in ('M02', 'M00', 'G75', 'G74'):
                continue
            # unrecognized -> surface it
            print(f"  [gerber-parse] UNRECOGNIZED: {cmd[:60]!r} in {path.split('/')[-1]}", file=sys.stderr)

# ---------------- matching helpers ----------------

def find_translation(a, b, tol=0.01):
    """a, b: lists of (x, y, size). Find translation t such that a+t == b. Try centroid; fall back to voting."""
    if len(a) != len(b):
        return None
    ax = sum(p[0] for p in a) / len(a); ay = sum(p[1] for p in a) / len(a)
    bx = sum(p[0] for p in b) / len(b); by = sum(p[1] for p in b) / len(b)
    return (bx - ax, by - ay)

def match_sets(a, b, t, pos_tol=0.002, size_tol=0.006):
    """Greedy nearest match of a (+t) onto b. Returns (matched, unmatched_a, unmatched_b, max_pos_err, max_size_err)."""
    bleft = list(b)
    un_a, max_pe, max_se = [], 0.0, 0.0
    for (x, y, s) in a:
        tx, ty = x + t[0], y + t[1]
        best, bi = None, None
        for i, (bx2, by2, bs) in enumerate(bleft):
            d = math.hypot(bx2 - tx, by2 - ty)
            if d <= pos_tol and abs(bs - s) <= size_tol and (best is None or d < best):
                best, bi = d, i
        if bi is None:
            un_a.append((x, y, s))
        else:
            max_pe = max(max_pe, best)
            max_se = max(max_se, abs(bleft[bi][2] - s))
            bleft.pop(bi)
    return len(a) - len(un_a), un_a, bleft, max_pe, max_se
