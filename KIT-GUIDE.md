# Strämpler DIY kit pack — bare boards + parts, NO assembly (2026-07-06)

For putting together **build kits** of the Antumbra CTAG Strämpler: bare
PCBs + panel + a complete parts kit per build. All SMD is hand-solderable
(0603 passives, SOIC/TSSOP/SSOP ICs, one QFN — the CP2102N — and the
castellated ESP32 module). See "Licensing & selling" at the bottom before
selling anything.

## 0. Board formats — Eagle AND KiCad

`boards/` holds the original Eagle 7.3 files; `boards-kicad/` holds KiCad 10
conversions (made with `kicad-cli pcb import --format eagle`, KiCad 10.0.4,
2026-07-07) plus verification renders. **Eagle was sunset by Autodesk in
2026** — the KiCad files are the living, forkable format; the Eagle files
remain the designer's originals. Statistics from the import: main board 174
footprints / 2001 tracks / 263 vias / 4 zones; panel 32 footprints / 38210
art zones. The schematic (`.sch`) imports via the KiCad GUI:
File → Import Non-KiCad Project → EAGLE (kicad-cli cannot do schematics).

## 1. Boards (any fab; PCBWay shown since it takes Eagle natively)

pcbway.com → PCB Instant Quote:
- `boards/Strampler_redesign_v2_2.brd` — main board, 91.3 x 108 mm, 2-layer,
  1.6 mm, HASL fine for hand-soldering (ENIG easier for the QFN). Qty 5 or 10.
- `boards/strampler_panel_v2_2.brd` — panel, 93.9 x 130.1 mm, 2-layer, 1.6 mm,
  matte black + ENIG for the classic Antumbra look. Same qty.
- No assembly service on either. ~$25–35 per design per 5 pcs + shipping.
- (JLCPCB is a few dollars cheaper but needs gerbers converted from the
  Eagle files first — PCBWay quotes the .brd directly.)

## 2. Mouser parts — one cart per kit

Upload `mouser-bom-ONE-KIT.csv` at mouser.com → BOM Tool. Quantities are for
ONE kit — set the multiplier to your kit count in the BOM tool. 43 lines,
~$45–60 per kit at qty-1 pricing. Notes:
- IC5 is entered by MPN `ESP32-WROVER-IE-N8R8` — verify the tool matches the
  **-IE (IPEX antenna)** variant, NOT the plain -E; the module lives behind a
  metal panel and needs the external antenna.
- Some 2019 Mouser SKUs may be superseded — accept the tool's suggested
  equivalents for passives (1% resistors, X5R/X7R ceramics).
- The designer's original cart also exists (may be stale):
  https://www.mouser.com/ProjectManager/ProjectDetail.aspx?AccessID=9c1a090daf

## 3. Parts NOT at Mouser — `parts-NOT-from-mouser.csv`

Per kit:
- **Thonk** (thonk.co.uk): 14x Thonkiconn PJ398SM, 4x B10k pot, 1x B100k
  dual-gang pot, uSD breakout, knobs — ~£45–55.
- **AliExpress**: 2.2" 240x320 SPI TFT (ILI9341) ~$8; IPEX WiFi antenna ~$3.
- **Rotary encoder** (Bourns PEC11-style w/ switch), 2x5 male header,
  M3 10mm F-F standoffs x5 + M3 6mm screws x10 — any supplier.
- **WM8731SEDS/V x1 (+ spare recommended)** — obsolete. Rochester
  Electronics for genuine EOL stock (~$6–12); UTSource/eBay cheaper with
  fake risk. THE critical part: without it there is no audio.

## 4. Per-kit cost, roughly

| | |
|---|---|
| Boards (main + panel, amortised at qty 5) | $12–18 |
| Mouser cart | $45–60 |
| Thonk | £45–55 (~$60–70) |
| TFT + antenna + encoder + misc hardware | ~$25 |
| WM8731 (+spare) | $12–25 |
| **Per kit** | **≈ $160–195** |

## 5. Kit contents checklist (what goes in each bag)

1 main PCB, 1 panel, the Mouser bag, the Thonk bag, TFT, antenna, encoder,
WM8731, hardware (standoffs/screws/header). Builder needs: firmware from
github.com/ctag-fh-kiel/ctag-straempler (or the tungusk fork for the
machines build), flashed over USB with `--flash_size detect`; an SD card
(FAT32, <=2GB files) with the CONFIG.JSN from the repo.

Build order: SMD (ICs first, WM8731 SSOP28 with flux+drag), then power-up
smoke test (3.3V rails), then through-hole loosely, panel on, align, solder.

## 6. Licensing & selling (checked 2026-07-06 — not legal advice)

Two licenses apply (LICENSE file in the firmware repo):
- **Firmware: GPL 3.0** — commercial use allowed; you must provide source to
  buyers (the public repo/fork satisfies this; forks must stay GPL).
- **Hardware: CC BY-NC-SA 4.0** — the **NonCommercial** clause means building
  boards from the design files **to sell** is NOT permitted without separate
  permission from the rights holders: CTAG (Robert Manzke, Phillip Lamp,
  Niklas Wantrupp — creative-technologies.de) and Antumbra (antumbra.eu /
  @antumbra_modular) for the redesign layout.

Practical gradations as commonly understood:
- Selling YOUR OWN existing module secondhand: fine (personal property).
- Kits/builds for friends at cost: the gray zone NC tolerates in practice;
  keep it small-scale and non-profit.
- Building to sell at a profit: squarely prohibited without a yes from both
  CTAG and Antumbra first.

Permission looks gettable: CTAG's README asks people to "help build and
spread the hardware module", and Pusherman openly sold panel/PCB sets. A
short email describing what you'd sell is the way in.

Also: **ShareAlike** — any board/panel modifications you distribute must be
published under the same license. Freesound access is per-user (each owner
needs their own API key); that's not something you can license to buyers.
