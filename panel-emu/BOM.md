# E-mu panel build — BOM for the 1/4" jack version

What to buy **on top of, or instead of**, the standard Strämpler kit to build
the E-mu format panel described in `README.md`. Prices are Digi-Key, qty 1,
checked **2026-09-14** unless marked ≈ (not checked — cheap commodity parts).
`BOM-digikey.csv` in this folder is the same list for Digi-Key's BOM tool
(it matches on manufacturer part number).

## Leave out of the standard kit

| qty | part | why |
|---|---|---|
| 14 | Thonkiconn PJ398SM 3.5 mm jacks (J1–J14) | replaced by 1/4" jacks on flying leads; the board pads stay empty |
| 1 | Eurorack front panel | replaced by the 6" × 6" E-mu panel |

Everything else in the kit is still used: pots, encoder, buttons, LED, SMA,
display, and the five M3 × 10 mm F-F panel standoffs. Knobs are unchanged —
the PTN09 pots pass through the new panel just as they did the old one
(≤ 2 mm panel, see README "Panel thickness").

## 1/4" jacks — 16 (14 + 2 spares)

| qty | part | Digi-Key | each | notes |
|---|---|---|---|---|
| 11 | **Switchcraft 11** — mono, 2-lug, open frame | [11](https://www.digikey.com/en/products/detail/switchcraft-inc/11/109515) | $4.71 | the 10 plain jacks + 1 spare. 3/8"-32 bushing, nut + washer included. 9,863 in stock |
| 5 | **Switchcraft 12A** — mono, tip shunt (switching) | [12A](https://www.digikey.com/en/products/detail/switchcraft-inc/12A/109527) | $5.00 | the 4 bus-normalled jacks (CV 1, CV 2, TR1, TR2) + 1 spare. 0.375" hole, nut + washer included. 1,186 in stock |

Both are the period-correct 1970s American-modular jack. Same 3/8"-32
bushing, so one hole size (Ø9.6 in the cut file) serves both. Enclosed
equivalents if dust matters: Switchcraft 111X / 112AX.

## BUS switches — 2

| qty | part | Digi-Key | each | notes |
|---|---|---|---|---|
| 2 | **E-Switch 100DP3T1B1M1QEH** — DPDT ON-OFF-ON, bat handle, solder lug | [100DP3T1B1M1QEH](https://www.digikey.com/en/products/detail/100DP3T1B1M1QEH/EG2413-ND/378882) | $5.16 | pick. 1/4-40 bushing, Ø6.35 hole (the cut file's 6.5 clears it) |
| (2) | C&K **7203SYZQE** — same function, epoxy-sealed | [7203SYZQE](https://www.digikey.com/en/products/detail/c-k/7203SYZQE/6979) | $18.45 | premium alternative, same bushing and hole |

Avoid C&K **7203J1ZQE2**, which turns up first in searches: its handle is a
flat paddle, not a bat. The NKK M2023SS1W01 is obsolete.

## Bus pickup

| qty | part | Digi-Key | each | notes |
|---|---|---|---|---|
| 2 | **Aries 16-600-10** — 16-pin DIP header plug, solder tails, 0.300" rows | [16-600-10](https://www.digikey.com/en/products/detail/aries-electronics/16-600-10/4260) | $2.85 | plugs into the cabinet's DIP socket. 1 + spare |

Solder tails rather than an IDC ribbon plug on purpose: only **seven** bus
lines are used (GND, +15, −15, VOICE 1/2, GATE 1/2), so plain wire does the
job and the power pair can be heavier than 28 AWG ribbon. The 3M IDC DIP plug
(7816-0006PR) is obsolete; if you want ribbon anyway, the Assmann AWLP 16/3,2-G
or TE 1-746610-4 are Digi-Key's suggested replacements (not checked for gauge),
and 3M 3801/16 ribbon is sold by the foot ($1.58/ft).

**Meter the cabinet's socket before wiring** — the pin map came from a 1974
drawing (README "Bus normalling" and research section).

## ±15 V → ±12 V regulator sub-board

The E-mu bus is ±15 V and the board's rail caps are 16 V parts, so the module
carries its own regulators on a scrap of perfboard behind the PCB (README
"Power conversion"). Skip this whole section if the module gets its own ±12 V
brick instead.

| qty | part | Digi-Key | each | notes |
|---|---|---|---|---|
| 1 | **ST L7812CV** — +12 V, 1.5 A, TO-220 | [L7812CV](https://www.digikey.com/en/products/detail/stmicroelectronics/L7812CV/585973) | $1.21 | active, 17k in stock |
| 1 | **ST L7912CV** — −12 V, 1.5 A, TO-220 | [L7912CV](https://www.digikey.com/en/products/detail/stmicroelectronics/L7912CV/585997) | $1.16 | active. **Its tab is the −15 V INPUT** — keep it off ground, no heatsink needed |
| 1 | **Boyd/Aavid 574502B00000G** — clip-on TO-220 heatsink, 21 °C/W | [574502B00000G](https://www.digikey.com/en/products/detail/boyd-laconia-llc/574502B00000G/240992) | $0.50 | on the 7812 only (~1.5 W → ~30 °C rise) |
| 2 | **KEMET C322C105K5R5TA** — 1 µF 50 V X7R, radial | [C322C105K5R5TA](https://www.digikey.com/en/products/detail/kemet/C322C105K5R5TA/6873900) | ≈ $0.50 | regulator inputs, close to the pins |
| 2 | **Panasonic ECA-1EM100** — 10 µF 25 V electrolytic | [ECA-1EM100](https://www.digikey.com/en/products/detail/panasonic-electronic-components/ECA-1EM100/245007) | ≈ $0.25 | regulator outputs |
| 2 | 1N4007 | any | ≈ $0.15 | reverse diode output→input across each regulator |
| 1 | perfboard, ~40 × 25 mm | any | — | |
| 4 | M3 M/F standoffs (length = PCB rear clearance, ~10 mm) + M3 nuts | any | — | the sub-board on the PCB's standoff holes |
| 1 | 0.5 A fuse + inline holder (optional) | any | — | in the +15 lead, for a vintage 2900/2910 supply |

**Sub-board → board power header (P4):** reuse one of the 10→16 pin Eurorack
power cables from the kit order — cut off the 16-pin end and solder it to the
sub-board, keeping the red stripe (−12) orientation. Or build one: 3M
89110-0101 10-pin IDC socket ([Digi-Key](https://www.digikey.com/en/products/detail/3m/89110-0101/229690), $1.01)
on a short 10-way ribbon.

## Wire and small parts

| qty | part | notes |
|---|---|---|
| ~4 m | 24 AWG stranded hookup wire, two colours | jack flying leads: 14 tip/sleeve pairs at ~40–145 mm (README lead table) plus slack |
| ~1 m | 22 AWG stranded hookup wire, three colours | bus plug → sub-board: GND, +15, −15 |
| ~1 m | 24 AWG stranded | VOICE 1/2, GATE 1/2 from the bus plug to the BUS switches |
| — | heat-shrink, assorted small | every solder joint on a flying lead |

## Panel and fixing

| qty | part | each | notes |
|---|---|---|---|
| 1 | E-mu panel, 2 mm natural anodized aluminium, UV-printed | $89.72 | Front Panel Express quote 2026-09-08, file `emu_panel_fpe.fpd` ready to upload. $63.08 bare |
| 5 | M3 × 6 mm countersunk (90° flat head) screws | — | panel → the kit's M3 standoffs. Countersink the five M3 holes |
| 4 | #6 × 3/4" wood screws + finishing washers | — | panel → the cabinet's wood rails. Match the neighbouring modules' head style |

## Rough total

| | |
|---|---|
| jacks (16) | $76.81 |
| BUS switches (2, E-Switch) | $10.32 |
| DIP plugs (2) | $5.70 |
| regulator sub-board parts | ≈ $5 |
| panel (printed) | $89.72 |
| **total, before wire, screws, tax and shipping** | **≈ $188** |

Digi-Key's own quantity breaks at 10+ bring the jacks down a little. Cheapest
route on jacks: generic open-frame 1/4" TS jacks from AliExpress at under $1
each — check the bushing is 3/8"-32 and that four of them have the switch lug.
