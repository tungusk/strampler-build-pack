# Completion shopping list — 5 units, AliExpress-first (no Thonk)

For the 5 PCBWay-assembled boards (ordered 2026-07-17, all SMD done, codec
populated). Everything below is through-hole / bolt-on. Quantities include
spares. Footprint data verified against the KiCad board
(`hardware-kicad/project/Strampler_redesign_v2_2.kicad_pcb`).

## AliExpress cart

| Part | Need | Order | Notes |
|---|---|---|---|
| **WQP-PJ398SM jack** (J1–J14) | 70 | 80 | Qingpu's own AliExpress storefront, ~$0.25–0.35 ea. Listing MUST say PJ398SM / WQP-PJ398SM with clear photos — the PJ301M-12 lookalike has a different footprint and will not fit. |
| **B10k pot, Alpha 9mm vertical** (POT2–5) | 20 | 24 | RD901F style / "RV09" clones. 6mm knurled T18 shaft (match knobs). |
| **B100k DUAL-gang pot, 9mm vertical** (POT1) | 5 | 8 | ⚠️ Footprint check: two 3-pin rows, 2.5mm pin pitch, rows 2.5mm apart, mount legs at ±4.4mm. Standard Alpha RD902F dual pattern — compare listing photo before buying. |
| **EC12E rotary encoder w/ push switch** (SW1) | 5 | 8 | Footprint `ALPS_EC12E_SW`: A/B/C at 2.5mm pitch one side, D/E switch pins opposite (5mm apart), tabs at ±6.1mm — standard EC12. Pick shaft (knurled T18 or D) to match your knob choice + panel clearance. |
| **2.2" 240×320 SPI TFT, ILI9341** (P3, MSP2202) | 5 | 6 | Original link: aliexpress.com/item/32607741715.html — MSP2202 module, footprint verified on board. |
| **IPEX/u.FL WiFi antenna** | 5 | 8 | Original link: aliexpress.com/item/4001275208954.html. Cheap — spares. |
| **microSD breakout** (P1) | 5 | 6+ | ⚠️ THE risky one — see section below before ordering. |
| **Knobs** | 25 | 30 | For 6mm knurled T18 shafts (4 pots + encoder per unit; dual-gang = 1 knob). Davies 1900h clones etc. |
| **M3 10mm F-F standoffs** | 25 | 30 | Assortment kits fine. |
| **M3 6mm screws** | 50 | 60 | |
| **Eurorack power cables 10-pin→16-pin** | 5 | 5 | Not in any BOM — don't forget. |

Rough Ali total: **$110–140** for all five units.

## LCSC add-on (ride along with the spare-codec order)

| Part | Need | Order | Notes |
|---|---|---|---|
| **C&K D6R00F1LFS tactile switch** (SW2, SW3) | 10 | 12 | Confirmed MPN from the Mouser kit BOM. Footprint is a 5.0×5.0mm pin square — generic 6×6mm tacts (4.5×6.5mm pins) will NOT fit. D6R clones exist on Ali but are hit-or-miss; LCSC/Mouser is the safe route. |
| **Molex 105017-0001 USB-B** (P2) | 5 | 6 | Right-angle THT USB-B. Footprint has Molex-specific SMD pads alongside the TH legs — buy the real MPN, not a generic USB-B. |
| **5mm red LED** (L1) | 5 | 10 | Original: INL-5AR30. Any 5mm red works; pad A/K at 2.54mm. |
| **2×5 shrouded male header** (P4) | 5 | 10 | Eurorack power, 2.54mm. |
| **WM8731SEDS/RV spares** (hedge) | — | 2–3 | ~$10 ea. The reason this order exists. |

## The SD breakout (P1) — footprint truth

`SD-CARD-THONK` footprint: **8 staggered pads at 1.1mm x-pitch** (rows
offset 1.1mm) + 2 mechanical pads at ±4.3mm. 1.1mm is exactly microSD
card-edge contact pitch — the board takes the Thonk-style castellated
uSD breakout (Radio Music style), NOT the common 2.54mm-header
"LC Studio" SD module.

Options, best first:
1. **Ali "microSD sniffer" / "TF card extender adapter board"** — clones of
   the SparkFun sniffer with the same card-edge finger geometry. Compare
   the listing photo against the pad map above (8 fingers, 1.1mm pitch,
   staggered) before buying.
2. **Thonk fallback:** the genuine uSD breakout is ~£1.50 ea — a £10
   mini-order if no Ali listing checks out. Dodges the big Thonk cart
   either way.

## Pad-map quick reference (from the KiCad board)

- P1 SD: 8 pads, x = -3.85…+3.85 @ 1.1mm pitch, alternating y (-0.47/-1.57); mounts ±4.3
- POT1 dual: rows y=10.0 & y=7.5, pins x = -2.5/0/+2.5; mounts ±4.4
- SW1 encoder: ABC @ y=7.5 (2.5mm pitch), D/E @ y=-7.0 (±2.5), tabs ±6.1
- SW2/3 tact: pins at (±2.5, ±2.5) — 5.0×5.0mm square
- P2 USB-B: TH legs (±2.5,0)+(±3.5,-2.7), Molex SMD signal pads center
- P4 power: 2×5 @ 2.54mm
- L1 LED: A/K @ 2.54mm
