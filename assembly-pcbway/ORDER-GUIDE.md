# PCBWay order guide — Antumbra CTAG Strämpler (2026-07-06)

Two items to order: the **main board (PCB + turnkey SMD assembly, 2 assembled)**
and the **panel (bare PCB, no assembly)**. Hardware license CC BY-NC-SA 4.0 —
personal/non-commercial build.

## 1. Main board — PCB + assembly

Go to pcbway.com → *PCB Instant Quote* → *Quick-order PCB*.

- Upload **`gerbers-main-Strampler_redesign_v2_2.zip`** (RS-274X gerbers +
  Excellon drills, plotted from the KiCad conversion — PCBWay's uploader
  rejects raw Eagle .brd files).
- PCB specs: 2 layers, 1.6 mm FR4, HASL or ENIG (ENIG nicer under the QFN/SSOP),
  any solder-mask colour. Quantity: 5 (their PCB minimum — assemble 2, 3 spares).
- Tick **Assembly Service**: Turnkey, **Assemble 2**, ONE side (all SMD is on
  the BOTTOM side — 144 bottom / 30 top placements in the CPL; the top-side
  refs are through-hole and NOT for assembly).
- Upload `BOM-PCBWay-assembly.csv` (40 SMD lines) and
  **`CPL-kicad-origin.csv`** when the assembly form asks (this position file
  is exported from the same KiCad board as the gerbers, so origins match;
  `CPL-Strampler_redesign_v2_2.csv` is the older Eagle-coordinate version).

### BOM notes PCBWay must see (paste into the order remarks)
- **IC4 / WM8731: DO NOT POPULATE.** Obsolete part; customer hand-solders later.
- **IC5: ESP32-WROVER-IE-N8R8** substitutes the discontinued WROVER-IB.
  The **IPEX/-I (external antenna) variant is required** — the module sits
  behind a metal panel; the PCB-antenna variant (non-I) will not work.
- All other Supplier P/Ns are Mouser references from the designer's BOM
  (2019) — approve reasonable equivalents for passives if any ref is stale,
  1% tolerance on resistors, X7R/X5R on ceramics.
- The CPL lists ALL footprints incl. through-hole (jacks/pots/encoder);
  assemble only the designators present in the BOM.

## 2. Panel — bare PCB

Separate quick-order: upload **`gerbers-panel-strampler_panel_v2_2.zip`**.
- 2 layers (it's just FR4 with plating/art), 1.6 mm, **matte black + ENIG**
  is the classic Antumbra look. Qty 5 (minimum).
- No assembly.

## 3. Parts the fab does NOT supply (order alongside)

From **Thonk**: 14× Thonkiconn PJ398SM jacks, 4× B10k pot, 1× B100k dual-gang
pot, SD card reader (μSD breakout per BOM), knobs. From **AliExpress**:
2.2" 240×320 SPI TFT (ILI9341), IPEX WiFi antenna. Elsewhere: rotary encoder,
USB-B (Mouser 538-105017-0001), 2× D6R00F1LFS tactile switches, 5 mm red LED,
2x5 male header, screen connector (Mouser 798-MDF79S254DSA55), M3 standoffs
+ screws. **WM8731SEDS/V ×2** from a broker (Rochester Electronics is the
legit-stock route; UTSource/eBay cheaper but inspect for fakes).

## 4. After delivery

Hand-solder order: WM8731 (SSOP28, flux + drag), then TH parts loosely, fit
the panel, align, then solder. Flash firmware per the repo README/CLAUDE.md
(`--flash_size detect`; a WROVER-E with 8 MB flash matches the current unit).
