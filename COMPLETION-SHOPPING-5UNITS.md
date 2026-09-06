# Completion shopping list — 5 units

## ✅ BOTH ORDERS PLACED 2026-07-26

- **AliExpress — 11 lines, $186.02** (jacks, pots, dual-gang, encoders,
  TFTs, antennas + stubs, knobs, encoder caps, standoffs, screws)
- **Mouser — 6 lines, $57.04** (SD holders, tact switches, micro-USB,
  LED, power header, screen connector) — single shipment, all ship-now

Total ≈ **$243** — that's the two module-parts orders. Power cables and
SD cards are still outstanding (see below); neither appears in any BOM.

**Power cables: ORDERED** (ExcelValley 5-pack, 10→16 pin, Amazon).
**SD cards: NOT ordered** — deliberately deferred to nearer final
assembly. Neither item appears in any BOM. Card spec + purchasing notes
below; **brand matters far less than FAT32 and the seller** — Lexar at
~40% under SanDisk is a sound buy for this duty cycle.

## ✅ FIRST MODULE BUILT — 2026-08-28 (soldering lab)

**Result: PASS — boots and makes sound.** Unit #1 of 5, PCBWay-assembled main
board + hand-soldered through-hole. Remaining adjustments are cosmetic /
ergonomic; the electrical build is proven.

What happened, for units 2–5:
- **Flashed from a bare Mac** (no ESP-IDF): `pip install esptool` in a venv,
  micro-USB to the on-board CP2102 (`/dev/cu.usbserial-*`), module on
  **rack +12 V** (USB VBUS does not power the board), then
  `bin/keys-multisample-v1/flash.sh` offsets with `--flash_size detect`
  (chip is 8 MB). Boot log: PSRAM 64 Mbit OK, display init, I2S up, WiFi up.
  Procedure is in the firmware repo `HANDOFF.md` (2026-08-29 entry).
- **White screen on first power-up** — panel got no init. Fixed by
  **reseating the TFT in the Hirose P3 receptacle**; root cause not
  isolated (seating vs. a marginal header pin). Check the 9-pin header is
  fully home before suspecting anything else. Orientation was correct
  (backlight on = VCC/GND/LED right).
- **Jacks**: Ali lot fits, nuts included (audit rows 4).
- **POT1 (GAIN) not fitted** — Ali sent the wrong part; Mouser substitute
  carted (see POT1 section). Audio **input** path is untested until it's in;
  output verified by ear.
- **Panel**: LED light window is copper on this run (see Panel defect
  section) — module works, LED just doesn't show through. Re-fab pending.
- **SJ1 (bottom, IO19↔TFT SDO)** is open, as on the test unit. Not needed
  for operation; bridge it if TFT readback is wanted (firmware `/tftread`).
- No SD card was in for the first boot — firmware tolerates that (logs
  `Failed to initialize the card (263)`, continues). A blank FAT32 card
  self-populates on first boot.

## Power cables & SD cards — sourcing notes (for reorders / kit runs)

### Eurorack power cable, 10-pin (module P4) → 16-pin (bus board)
**Leading pick (in Amazon cart, not yet ordered): [ExcelValley 5-pack,
10→16 pin, 25 cm](https://www.amazon.com/ExcelValley-5-Pack-Eurorack-Modular-Synthesizer/dp/B07N8H544N)**.

Alternatives, cheapest-per-cable last:
| Source | Detail |
|---|---|
| [Arcus Audio](https://arcusaudio.com/product/10-pack-10-eurorack-power-cable-10pin-16pin-with-strain-relief-connectors/) | **10-pack**, 10″, 28AWG, strain relief. US. Best pre-made bulk. |
| [Etsy custom](https://www.etsy.com/listing/477371413/eurorack-power-cable-ribbon-cable-10) | packs of 3/5/10/15/20, choose length, bulk discounts |
| [AI Synthesis](https://aisynthesis.com/product/eurorack-power-cable/) | $5.00 ea, 254 mm, "5+ bulk discount" |
| [Thonk](https://www.thonk.co.uk/shop/eurorack-power-cables/) | £1.66 (15 cm) — cheapest each, but UK→US shipping. Bulk quotes >500. |
| **DIY** | **~$0.50/cable** in parts (ribbon ~$0.50/m, 16-pin IDC ~$0.10, 10-pin ~$0.20) + a **$15–40 IDC crimp tool**. Pays back around **30–50 cables** — i.e. only if kits happen, not for one build. [refs](https://modwiggler.com/forum/viewtopic.php?t=78071) |

⚠️ Red stripe → **-12V**. Our P4 is a shrouded keyed header so a keyed
cable can't reverse; only matters if you ever buy unkeyed.

### microSD card — SPEC (verified against firmware 2026-07-26)

Source of truth: `components/drivers/storage.c` + `sdkconfig.defaults` in
the firmware repo.

| Spec | Requirement | Why |
|---|---|---|
| **Filesystem** | **FAT32 — mandatory** | `CONFIG_FATFS_LFN_NONE=y` and **no exFAT option is enabled**, so FatFS can mount FAT12/16/32 only. An exFAT card will simply fail to mount. |
| **Pre-formatted** | **Yes — the firmware will NOT format it** | `format_if_mount_failed = false`. A blank/exFAT card gives "Failed to mount filesystem", not a rescue. |
| **Capacity** | **32 GB recommended. No hard maximum.** | FAT32 is the only real constraint — *not* capacity. 4–32 GB (SDHC) is FAT32 out of the packet; 64 GB+ (SDXC) ships exFAT and must be reformatted, which is fine if you don't mind doing it. See the note below on why bigger still isn't better. |
| **Filenames** | **8.3 only** | LFN is compiled out. This is *why* every sample id in the system is ≤8 chars. |
| **Max file size** | FAT32 ceiling is 4 GB; repo documents **≤2 GB** | Moot in practice — samples are megabytes. |
| **Speed class** | **Any Class 10 / UHS-I** | Bus is **1-bit SDMMC** at `SDMMC_FREQ_HIGHSPEED`; the audio path needs ~**176 KB/s**. Even 1-bit mode has enormous headroom. Paying for V30/A2 buys nothing. |
| **Contents** | `CONFIG.JSN` from the repo, before first boot | |

**Is there a max size?** No hard limit in the firmware, and none in FAT32
at any capacity you can buy (its ceiling is ~2 TB at these cluster sizes).
A 64/128/256 GB card reformatted to FAT32 should mount fine.

**But bigger is still not better here, for two concrete reasons:**
1. **Nothing above 32 GB has been tested on this hardware.** The only
   proven configuration is what's in the test unit.
2. **Directory walks are a known performance hazard in this firmware.**
   Bench-caught previously: per-index stat probing with a missing
   extension walks the entire FAT directory per call and starved the
   capture queue — *1804 dropped chunks*. Browsers already cap at
   224/512 entries. A bigger volume invites a bigger pool, and the cost
   lands on the audio path, not on idle time.

And there's nothing to gain: 32 GB ≈ **50 hours** of 44.1 k stereo audio.

### microSD card — purchasing
**Not yet ordered.** Lexar sits in an Amazon cart; **B&H is the better
buy** — see the supplier note at the end of this section.

**BUY 32 GB, and the reason is the SD spec, not preference:** 4–32 GB is
**SDHC, which the SD Association defines as FAT32** — exactly what the
firmware wants, straight out of the packet. **64 GB and up is SDXC =
exFAT**, so every card needs reformatting first, and Windows won't make a
FAT32 volume >32 GB without a third-party tool (guiformat / SD Card
Formatter / `mkfs.vfat`). Hold this even if 64 GB is a dollar cheaper.

Everything else is irrelevant here: the machine streams ~**176 KB/s**, so
Class 10 / UHS-I is already ~50× more than it can use — don't pay for
V30/A2. 32 GB ≈ 50 hours of 44.1 k stereo audio.

Brand barely matters at this duty cycle (gentle, read-mostly, rarely
reinserted). **Counterfeits are the only real risk** and they're
brand-independent — buy from a real retailer, not a marketplace
"mixed-brand tested lot". Lexar is legitimate (Micron sold it to Longsys
in 2017); photography forums report more early failures than SanDisk, but
that's sustained-burst camera use, not this. SanDisk Ultra 32 GB
`SDSQUA4-032G-GN6MA` is the belt-and-braces pick if reordering.

### Where to buy cards — B&H, and the reason is counterfeits
**[B&H Photo](https://www.bhphotovideo.com/)** (or [Adorama](https://www.adorama.com/)) — **authorized dealers** buying
direct from the manufacturer, so a counterfeit has no path into their
stock. SanDisk reckons [~1/3 of memory cards on the market are fake](https://www.pocket-lint.com/beware-of-fake-sd-cards/).

⚠️ **"Sold by Amazon" is NOT the safeguard it looks like** — Amazon
**commingles inventory** across every seller of an ASIN, so a third-party
counterfeit [can reach you even buying direct from Amazon](https://www.dpreview.com/forums/threads/buying-sd-cards-from-amazon.4468446/).

⚠️ **Skip "bulk memory card" sites** — checked
[bulkmemorycards.com](https://bulkmemorycards.com/product-category/microsd-cards/microsd-32gb/):
SanDisk Ultra 32 GB runs **$12.65–$15.50**, *above* normal retail, and the
bulk tiers shave only a few percent. No wholesale advantage at our volume.

**Setup:** copy `CONFIG.JSN` from the repo onto each card before first
boot. **If the cards are 64 GB+, reformat to FAT32 first.**

**Test every card on arrival, whatever the source.** A fake reports full
capacity but has less real flash and fails *silently* — you'd discover it
as corrupted samples months in. On macOS:
`brew install f3` then `f3write /Volumes/CARD && f3read /Volumes/CARD`.
~10 min per card, before you commit a library to them.

**⚠️ ON ARRIVAL — do this before soldering the run:** test-fit ONE
Thonkiconn jack and ONE RD902F dual-gang pot on a bare board with
calipers. Those are the only two lines whose footprint could not be
fully proven from listing photos. Both listings carry 90-day free
returns.

## COMPLETENESS AUDIT 2026-07-25 — every part accounted for

Method: kit BOM + `parts-NOT-from-mouser.csv` minus what PCBWay built.

| # | Part | Desig. | Per unit | Source | Status |
|---|---|---|---|---|---|
| 1 | Main PCB + panel | — | 1+1 | PCBWay | ✅ main ×5 OK · ❌ **panels ×5 DEFECTIVE** — LED light window is copper instead of bare FR4 (conversion bug, fixed 2026-08-28; see [Panel defect](#panel-defect--led-light-window-is-copper-2026-08-28)). Re-fab from the regenerated `gerbers-panel-*.zip`. |
| 2 | All SMD passives & ICs | many | — | PCBWay | ✅ assembled |
| 3 | WM8731 codec | IC4 | 1 | PCBWay | ✅ **populated** (not DNP — see below) |
| 4 | Thonkiconn jacks | J1–J14 | 14 | Ali | ✅ 200-pc lot — **received 2026-08-28, knurled nuts included** (confirmed in the bag; no separate nut order needed). **Test-fit on board OK 2026-08-28** — footprint matches. |
| 5 | B10k pots | POT2–5 | 4 | ~~Ali~~ → **Mouser** | ⬆ **UPGRADED 2026-08-29**: Same Sky PTN091-V10115K1B ×25 ordered (metal shaft, M7 bushing — see [POT2–5 section](#pot25-cv-pots--upgrade-to-metal-shaft--threaded-bushing-2026-08-29)); ✅ panel v2_3 has 7.2 mm holes (order re-fab from the v2_3 zip). Ali RV09 ×20 on hand = fallback for 9.2 mm panels. |
| 6 | B100k dual-gang | POT1 | 1 | ~~Ali~~ → **Mouser** | ❌ **WRONG PART received** (right-angle, mono) → reorder, see [POT1 section](#pot1-dual-gang-gain-pot--wrong-part-substitute-2026-08-28) |
| 7 | Encoder | SW1 | 1 | Ali | ✅ 6 |
| 8 | 2.2" ILI9341 TFT | P3 | 1 | Ali | ✅ 6 |
| 9 | Antenna + u.FL pigtail | — | 1 | Ali | ✅ 5 sets + stubs |
| 10 | Knobs, pots (Davies set-screw) | POT1–5 | **5** | Ali | ✅ 30 (25 needed → +5 spare) |
| 10b | **Encoder cap** (separate, see below) | SW1 | 1 | Ali | ✅ 40 |
| 11 | M3×10 F-F standoffs | — | 5 | Ali | ✅ 60 |
| 12 | M3×6 screws | — | 10 | Ali | ✅ 50 |
| 13 | Yamaichi microSD holder | P1 | 1 | Mouser | ✅ 6 |
| 14 | D6R tactile switches | SW2, SW3 | 2 | Mouser | ✅ 12 |
| 15 | Molex micro-USB | P2 | 1 | Mouser | ✅ 6 |
| 16 | 5mm red LED | L1 | 1 | Mouser | ✅ 10 |
| 17 | 2×5 shrouded power header | P4 | 1 | Mouser | ✅ 10 |
| 18 | Hirose screen connector | (TFT) | 1 | Mouser | ✅ 6 — **nearly missed** |
| 19 | Eurorack power cable | — | 1 | **Arlo sources separately** | ⬜ |
| 20 | microSD card (FAT32, ≤2 GB files) | — | 1 | **user-supplied, in no BOM** | ⬜ |

⚠️ **Knob count**: 5 pots (POT1 dual + POT2–5) **plus** the encoder = **6
shafts per unit**. The doc's old "25 needed" line undercounted by missing
the encoder.

**Resolved 2026-07-25 by giving the encoder its own cap** (Arlo's call).
So the 30 Davies set-screw knobs now cover only the 25 pot positions,
which conveniently restores a +5 spare margin on that line.

### Encoder cap (SW1) — separate part, deliberately distinct
**AliExpress "10PCS For KY-040 … ABS D Half Shaft Hole Caps Knob 6mm"**,
item 3256806101256136, $1.60/10, 4.9★/370 sold. **4 lots = 40 caps
$6.40** (4 was the seller's entire remaining stock — the + control greys
out there).

Why a different cap, not another Davies:
- **The EC12 encoder shaft is a D-shaft** (verified from the listing
  photo — smooth with a flat, NOT knurled). These caps are a true
  **D-bore**, so they key to the flat and need no set screw.
- **No indicator line.** A pointer is meaningless on an encoder — it has
  no absolute position, so a Davies pointer would spin and point at
  nothing. Arlo's requirement, and it's the functionally correct choice.
- **Hard ABS, not soft-touch** (Arlo: "not soft touch eew").
- Flat top suits the encoder's **push switch**; smaller diameter than the
  ~18 mm Davies makes DATA findable by feel among six knobs.

Rejected along the way: aluminum (Arlo wants plastic); WISINVI 10.5×17 mm
and KAIHCHIP 11×13.5 mm D-bore plastics (both have indicator lines); the
WISINVI 10×12 mm knurled aluminum (**"Flower Shaft"** = splined bore,
would wobble on a D-shaft).

Everything else on this page is background/history.

---

## Panel defect — LED light window is copper (2026-08-28)

Found at first-module assembly: the wavy line between TR1/TR2 that lines
up with the LED (L1) is a **copper trace** on the fabbed panels. On the
original Antumbra panel it is a **gap in the solder mask over bare FR4**
so the LED shines through the board.

**Cause:** the Eagle→KiCad conversion parked the Eagle `tRestrict`/
`bRestrict` copper keep-outs on KiCad's non-copper `User.1` layer, so the
mask window was plotted correctly but the copper pours filled underneath
it. Details in `hardware-kicad/README.md` (pitfall 2).

**Fix (committed):** keep-outs merged into one F.Cu+B.Cu rule area,
zones refilled, `gerbers/gerbers-panel-strampler_panel_v2_2.zip`
regenerated and verified (copper ∩ window = 0 on both layers).

**Action: ✅ ORDERED 2026-08-30 — at JLCPCB, not PCBWay** (5× panels from
`gerbers-panel-strampler_panel_v2_3.zip`, ~$19 shipped: $9.70 boards +
$9.08 Global Standard Direct Line, 8–13 business days). This is a
**solder-mask shade trial**: the PCBWay run was confirmed matte black but
reads lighter than the Pusherman reference; JLCPCB's current "Black" is a
proprietary semi-matte hybrid (they discontinued pure matte black as
scratch-prone), so it may land between. Spec: 1.6 mm, black mask, white
silk, HASL (finish is invisible — no exposed copper anywhere on the
panel), no order-number mark (JLC's free default). **On arrival: compare
shade vs the PCBWay matte panels and the Pusherman panel — the winner
prints the production run; Pusherman remains the known-good fallback for
the exact reference look.** The 5 defective panels are
usable only as-is with no LED show-through (or scrape the copper off the
window by hand — it's exposed, ~8 mm², both sides).

---

## POT1 dual-gang (GAIN pot) — WRONG PART, substitute (2026-08-28)

**The Ali "RD902F-B100K" lot (order 2026-07-25, #3) delivered a
right-angle MONO pot.** Caught at first-module assembly. The listing's
pin rows were never photo-confirmed (noted at the time) — that was the gap.

**What the board needs** (`POT_DUAL_THONK`, verified against KiCad + the
Alpha RD902F-40 factory drawing): 9 mm **vertical** (shaft ⟂ board),
**2 gangs**, two rows of 3 pins, **2.5 mm pin pitch**, rows at **7.5 and
10.0 mm** from the mount line, 6 mm shaft, M7 bushing.

⚠️ **Correction to the footprint note below:** the board's two Ø2.2 mm
holes at ±4.4 mm are **not** an Alpha feature. Alpha's own drawings (dual
RD902F-40 *and* single RD901F-40) show flat anti-rotation tabs ~11.3 mm
apart. No 9 mm pot's tabs land in those holes — **clip the tabs and let
the panel nut hold the pot.** Same for POT2–5. Select pots by pin grid
only; ignore the mount holes.

### Mouser substitute — ORDER THIS

| Mouser # | MPN | Mfr | Price | Stock (08-28) |
|---|---|---|---|---|
| **179-PTN092V100115K1A** | PTN092-V100115K1A | Same Sky (ex-CUI) | $2.45 / $1.97 @10 | 135 |

9.5 mm vertical, 2-gang, 100 kΩ, 15 mm 6 mm **knurled T18** shaft (fits
the Davies set-screw knobs), M7×0.75. PCB layout is pin-for-pin the Alpha
RD902F pattern (2.5 mm grid, rows 7.5/10). Tabs at 11.5 mm → clip.
Need 5 → **order 8** (spares).

**Caveat — taper is A (log), not B (linear).** Mouser and Digi-Key have
no stock of the linear `PTN092-V100115K1B`. Acceptable: the schematic
wires POT1 as a rheostat (wiper tied to one end, in series with R8/R9
into the codec input), so taper only changes knob feel, and log is the
natural feel for a gain control. If linear is a must, buy the exact part
from Thonk instead: **Alpha 9mm Vertical T18 Dual Gang, B100K**
(RD902F-40-15R1-B100K), £1.99 ex-VAT —
https://www.thonk.co.uk/shop/alpha-9mm-pots-vert-t18-dual-gang/

### Ruled out on Mouser (don't re-check)
- **Bourns PTD902-xxxx-B104** (linear, well stocked, looks perfect): pin
  pitch is **5.0 mm** within each row. Does not fit.
- **Alps RK09L** dual 100k linear: only the *horizontal* variant stocked;
  snap-in type anyway. RK09K / RK097 / Bourns PTV09: single-gang only.
- **Alpha (Taiwan)** on Mouser carries no RD90x at all.

Sources: Bourns PTD90 datasheet · Same Sky PTN09X datasheet (2024-09-12) ·
Alpha RD902F-40 / RD901F-40 drawings hosted by Thonk.

---

## Bench results 2026-09-04 — Mouser pots arrived, SJ1 bridged, input path PASSES

**Mouser order received.** Findings on the first module (the .85 unit):

- **POT1 (PTN092 dual-gang) FITTED and WORKING.** Two adjustments:
  (1) body sits tall in the bottom box — **file off the anti-rotation tab**
  on the bushing face (soft zinc; keep filings out of the pot, shaft down);
  (2) assembly order: **install jacks+pots LOOSE, fit panel, snug nuts,
  THEN solder** — the panel jigs every bushing to true height, so exact
  body height stops mattering. Both belong in KIT-GUIDE for units 2–5.
  Panel v2_4 candidate: add the anti-rotation locating holes (hidden under
  the nuts) so no filing is needed.
- **Audio INPUT path VERIFIED** (was the last untested electrical path):
  signal in, `vu[0]/vu[1]` swept ~1→253 (full range) with the gain pot,
  L/R matched within a count or two the whole sweep (both gangs alive and
  balanced). Ear-level listen still owed (line-in tuner or Tape monitor).
- **SJ1 BRIDGED on this unit → GRAM readback WORKS.** `/tftread`: pixel
  test 4/4 bit-exact at a 10 MHz read clock. **`id_ok` is false and always
  will be on this panel lot** (clone controller ignores 0xD3; RDDID
  nonstandard too) — **the QA criterion for units 2–5 is `pixel_ok`, not
  the overall verdict** (it reads "PARTIAL" because of the ID). Unit 1's
  SJ1 remains open (by choice).
- **PTN091 single-gang (POT2–5): NOT YET TESTED** — look like they fit,
  none installed yet (current panels have 9.2 mm CV holes; the M7 bushing
  wants the v2_3 panels in fab). First install = first test; expect the
  same anti-rotation tab to file unless the tab-hole lands in v2_4.

## POT2–5 CV pots — upgrade to metal shaft + threaded bushing (2026-08-29)

The Ali RV09 clones (row 5) work electrically but feel cheap: plastic
shaft, no bushing, nothing fixing them to the panel (unlike the encoder's
M7 nut). **ORDERED 2026-08-29: Same Sky PTN091-V10115K1B ×25, Mouser
179-PTN091V10115K1B, $1.32 @ 25 = $33 (shipping paid, under the $60
free-ship line).** Need 20 (4 × 5 units) + 5 spares.

Why this part:
- Single-gang sibling of the POT1 sub (PTN092-V100115K1A) — same family,
  same bushing/shaft geometry across the panel, one vendor.
- **Aluminum knurled 18T + slotted shaft** (datasheet materials table),
  15 mm — matches the original Alpha length, existing Davies knobs fit.
- **M7×0.75 zinc threaded bushing + nut** — panel-mounts like the encoder.
  Note: 15 mm shaft carries the 5 mm bushing (7 mm only on 20/25 mm
  shafts) — fine through the 1.6 mm panel, same as the POT1 sub.
- 10 kΩ linear, standard 2.5 mm 3-pin row; clip the mount tabs, panel nut
  holds it (same rule as POT1). Test-fit on arrival as usual.

**✅ PANEL CHANGE DONE 2026-08-29 — panel v2_3.** New
`hardware-kicad/strampler_panel_v2_3.kicad_pcb` (v2_2 kept unchanged as
the pre-M7 version): the four CV pot holes 9.2 → **7.2 mm**, and POT1's
hole 8.2 → **7.2 mm** (hole identification by position match against the
main board: POT1 = the POT_MEDIUM at panel (13.903, −65.096); the OTHER
8.2 at (77.544, −65.096) is the ENCODER — untouched, current encoders
thread it fine; the 2× 9.5 are SW2/SW3). Zones refilled, gerbers
regenerated + verified: drill table has no 9.2 left (7.2 ×6, 8.2 ×1),
edge/silk byte-identical to v2_2, mask differs by exactly the 5 resized
openings, copper diff = zone refill only, LED window still copper-free.
**Order the 5 panels from `gerbers/gerbers-panel-strampler_panel_v2_3.zip`.**
The Ali RV09s (20 on hand) remain the fallback for the 5 defective 9.2 mm
panels if they're ever scraped-and-used.

---

## Pending small hardware (2026-08-31) — display firming + hex jack nuts

### Display corner standoffs (firm up the TFT)
The MSP2202 module hangs off only the Hirose header — the known
white-screen/seating weak point. Main board + module both have 4 corner
mount holes (main board drill 3.1 mm plated ≈3.0 finished; 61.2×34.1 mm
rectangle). The unused card-slot can on the module's back sets a floor on
the gap of a couple of mm. **MEASURE FIRST at a corner hole on the working
unit (calipers or drill-shank gauge), then pick ONE:**
- **M3 nylon hex standoff F-F × <measured>** + M3×6 nylon screws both ends
  — fits our 3.0 mm holes for certain. Qty 30 standoffs + 60 screws
  (6 units incl. retrofit of unit 1 + spares). Ali parametric listing:
  aliexpress.com/item/32996308968.html (pick M3 + length).
- **Dual-lock snap support, 3.2 mm hole class** (barbed both ends,
  tool-free; RS 030-4195 shows the geometry; Ali: search "dual lock PCB
  support 3.2mm") — nicer assembly but our plated 3.0 mm bore is ~0.2 mm
  under nominal; barbs may seat snug or may refuse. Heights come in coarse
  steps (6.4/7.9/9.5) and can't be shimmed. Try-it item; ~$2/100.
  (The common Ali "RC" snap series is 4.0 mm-hole — does NOT fit.)
Both together cost ~$4 — ordering one lot of each and letting the bench
decide is legitimate.

### Non-knurled hex nuts for the jacks (J1–J14)
Arlo wants hex instead of the knurled nuts that shipped with the jack lot;
**silver confirmed** (Bananuts/black ruled out 2026-09-01).
**Thread is M6 × 0.5 (extra-fine)** — standard M6×1.0 and fine M6×0.75 DO
NOT fit; it must be a jack-specific 8mm-across-flats nut (generic DIN439
M6×0.5 exists on Ali but is 10mm AF — barely clears the 12.7mm jack grid,
ruled out on looks/wrenchability).
**DECIDED: Qingpu factory hex nut — SKU WQP-HN (NB: WQP-KN is the KNURLED one!), qty 200, $0.10 ea at Danesi = $20** — matches the full
200-jack stock (84 fitted across 6 units incl. unit 1 retrofit; the rest
keeps every spare jack buildable in the house style, saves a second
shipping later). Source: Danesi Designs (Scott Danesi, Chicago —
danesidesigns.com/products/wqp-kn-qingpu-hexjack-nut-m6-x-0-5mm),
~$0.15–0.25 ea; equal fallback: Amplified Parts / CE Distribution
(same Qingpu part). The Ali jack seller (NingSheng) does NOT carry nuts
(checked 2026-09-01).

## Board rev candidates — HYPOTHETICAL ONLY (no respin planned)

Collected "if we ever respin" ideas. **The 5 assembled main boards in hand
are fine; nothing here is a commitment or a schedule.** A respin has fixed
costs (fab + assembly setup + re-validation), so it should batch everything
below — do not spend one of these ideas alone.

### Main board
- **USB-C replaces micro-B** for the CP2102 flash/serial port. 12-pin
  USB-2.0-only receptacle (TYPE-C-31-M-12 class, ~$0.10), two 5.1 kΩ
  pull-downs on CC, D+/D− unchanged. While in there: check whether the
  CP2102 runs from VBUS or 3.3 V — bus-powering the bridge would allow
  flashing with no rack power (nicer kit-assembly workflow; today rack
  +12 V is required). Assembly note: the current micro-B (Molex
  105017-0001, P2) is a HYBRID footprint — SMD signal pads + 4 TH shield
  legs — which is why PCBWay's reflow-only job skipped it. USB-C offers
  the same choice: hybrid-with-TH-stakes (strong, stays a hand-solder
  step) vs pure-SMD (reflowable at PCBWay, mechanically weaker). For an
  occasional programming port the anchored hybrid is in character.
- **Display mounting holes 3.1 → 4.0 mm** (and unplated) to accept
  dual-lock snap-in PCB supports (RC-style, tool-free) instead of M3
  hardware. Note the TFT module's own ~3 mm corner holes remain the other
  half of the problem — only helps if the module side is solved too.
- **SJ1**: optionally replace with a wired-through trace (bridge is now
  the standard build step anyway; original CTAG wired MISO permanently).
  Or keep the jumper — costs nothing and preserves the isolation option.
- Already fixed in KiCad but absent from the 2026-07 fabbed boards
  (any refab inherits them automatically): SJ1 mask sliver, main-board
  keep-out audit results.

### Kit-ready assembly (process change, not a layout change)
If boards are ever built for OTHER people, add the machine-doable TH parts
to the PCBWay job: micro-USB, SD holder, 2× tact switches, power header,
display socket — ~50 joints/board, est. **$15–40 extra** on the run (2026-07
reference: assembly was only $29.00 of the $370.65 / 5-board order) plus
sourcing markup or consignment handling. Shrinks the kit builder's work to
purely the panel sandwich (jacks/pots/encoder/LED — which MUST stay hand
work for the panel-jig solder order). Not worth it for self-built units:
those six parts are ~10 min in the same soldering session.

### Panel (v2_4 candidates — v2_3 is the current fab)
- **Anti-rotation locating holes for POT1–5** (~1.3 mm at the PTN09X tab
  radius, hidden under the nuts) — eliminates the file-the-tab assembly
  step. Tab angular position is deterministic (pot orientation fixed by
  PCB pins); take the radius/angle from the PTN09X drawing and verify
  against a filed-tab pot in hand before committing.

# Original list — AliExpress-first (no Thonk)

For the 5 PCBWay-assembled boards (ordered 2026-07-17, all SMD done, codec
populated). Everything below is through-hole / bolt-on. Quantities include
spares. Footprint data verified against the KiCad board
(`hardware-kicad/project/Strampler_redesign_v2_2.kicad_pcb`).

## AliExpress cart

| Part | Need | Order | Notes |
|---|---|---|---|
| **WQP-PJ398SM jack** (J1–J14) | 70 | 80 | Qingpu's own AliExpress storefront, ~$0.25–0.35 ea. Listing MUST say PJ398SM / WQP-PJ398SM with clear photos — the PJ301M-12 lookalike has a different footprint and will not fit. |
| **B10k pot, Alpha 9mm vertical** (POT2–5) | 20 | 24 | RD901F style / "RV09" clones. 6mm knurled T18 shaft (match knobs). |
| **B100k DUAL-gang pot, 9mm vertical** (POT1) | 5 | 8 | ⚠️ Footprint check: two 3-pin rows, 2.5mm pin pitch, rows 2.5mm apart. Standard Alpha RD902F dual pattern — compare listing photo before buying. **Ali lot delivered a right-angle mono pot — superseded by Mouser 179-PTN092V100115K1A, see POT1 section above.** (The "mount legs at ±4.4mm" claim was wrong: Alpha tabs are ~11.3mm apart and get clipped.) |
| **EC12E rotary encoder w/ push switch** (SW1) | 5 | 8 | Footprint `ALPS_EC12E_SW`: A/B/C at 2.5mm pitch one side, D/E switch pins opposite (5mm apart), tabs at ±6.1mm — standard EC12. Pick shaft (knurled T18 or D) to match your knob choice + panel clearance. |
| **2.2" 240×320 SPI TFT, ILI9341** (P3, MSP2202) | 5 | 6 | Original link: aliexpress.com/item/32607741715.html — MSP2202 module, footprint verified on board. |
| **IPEX/u.FL WiFi antenna** | 5 | 8 | Original link: aliexpress.com/item/4001275208954.html. Cheap — spares. |
| **microSD breakout** (P1) | 5 | 6+ | ⚠️ THE risky one — see section below before ordering. |
| **Knobs** | 25 | 30 | For 6mm knurled T18 shafts (4 pots + encoder per unit; dual-gang = 1 knob). Davies 1900h clones etc. |
| **M3 10mm F-F standoffs** | 25 | 30 | Assortment kits fine. |
| **M3 6mm screws** | 50 | 60 | |
| **Eurorack power cables 10-pin→16-pin** | 5 | 5 | Not in any BOM — don't forget. |

Rough Ali total: **$110–140** for all five units.

## MOUSER add-on order (was "LCSC add-on") — prices verified 2026-07-25

Everything here is through-hole/bolt-on that the AliExpress order does not
cover. Mouser part numbers checked live; put the **SD holders** (see below)
on this same order.

**CART FINAL 2026-07-25 — subtotal $57.04** ($43.99 parts + $8.49 UPS
Ground + $4.56 est. tariff). **All 6 lines "Ships Now" — no backorder,
ships complete in one box.**

| Part | Need | Order | Spare | Mouser # | Unit | Ext |
|---|---|---|---|---|---|---|
| **Yamaichi PJS008U-3000-0** microSD holder (P1) | 5 | 6 | +1 | **945-PJS008U-3000-0** | $1.38 | $8.28 |
| **C&K D6R00 F1 LFS** tactile switch (SW2, SW3) | 10 | 10 | **0** | **611-D6R00F1LFS** | $1.49 | $14.90 |
| **Molex 105017-0001** micro-USB (P2) | 5 | 6 | +1 | **538-105017-0001** (cut tape) | $0.92 | $5.52 |
| **Kingbright WP7113ID** 5mm red diffused (L1) | 5 | 10 | +5 | **604-WP7113ID** | $0.145 | $1.45 |
| **Würth 61201021621** WR-BHD 2×5 box header (P4) | 5 | 10 | +5 | **710-61201021621** | $0.466 | $4.66 |
| **Hirose MDF7-9S-2.54DSA(55)** screen connector | 5 | 6 | +1 | **798-MDF79S254DSA55** | $1.53 | $9.18 |

**Spare policy here is deliberately the OPPOSITE of the Ali cart's.** On
Ali we trimmed to exact because a spare dual-gang pot cost $18.50. Here
all the spares together cost ~$8, while **re-shipping one forgotten part
from Mouser costs $8.49** — a single reorder equals the whole spare
allowance. These are also the hand-soldered parts (two fine-pitch
connectors), where a lifted pad is a live risk.

⚠️ **D6R is the exception at exactly 10, zero spare.** Ordering 12
triggered "10 Ships Now / **2 Backordered**" — those 2 spares were the
only thing splitting the shipment, despite the product page claiming 399
in stock. Trimmed to 10 so the order ships complete. If a switch dies,
reorder rather than wait on a backorder.

⚠️ **The screen connector was nearly missed** (caught 2026-07-25 when Arlo
asked "is this all of the parts"). It is in the kit BOM as the bare word
"Screen connector" with NO designator, and it is absent from
`parts-NOT-from-mouser.csv`, so it fell through every earlier pass. It's
the 9-pos 2.54 mm receptacle the TFT plugs into.
**How it was caught — reuse this method:** diff the kit BOM against
`assembly-pcbway/BOM-PCBWay-assembly.csv`. PCBWay's BOM is SMD-only, so
*every kit-BOM line absent from it is a part you must buy.* Exactly four
are absent: 538-105017-0001, **798-MDF79S254DSA55**, 743-INL-5AR30,
611-D6R00F1LFS.

**Verified against the original kit BOM** (`bom/mouser-bom-ONE-KIT.csv`):
- D6R: line 44 = `611-D6R00F1LFS`, SW2 SW3 — **exact match** ✓
- LED: line 43 specifies `743-INL-5AR30` (Inolux). **Substituted**
  Kingbright WP7113ID — equivalent 5mm THT diffused red, 2.54mm leads,
  deeper stock, cheaper. Swap back if you want the literal BOM part.
- **P4 header has NO specified MPN** — the kit BOM omits it and
  `KIT-GUIDE.md` says "2x5 male header … any supplier". Final pick:
  **Würth 61201021621** (WR-BHD 2.54mm Box, 10-pin male straight),
  $0.466 @10, 9,619 in stock. Product photo shows a **plain black box
  shroud with the polarity notch and no latches** — exactly the Eurorack
  power header shape. Shrouded matters: Eurorack ribbon connectors are
  keyed, and a bare pin header loses polarity protection.

  ⚠️ **Two wrong picks preceded it — check the PHOTO, not just the
  parametrics.** TE 281740-5 ($2.48) was dropped on price. Amphenol FCI
  71918-110LF ($1.19) was carted and then REMOVED: its parametrics said
  "Type: Shrouded / 2×5 / 2.54 mm", but Arlo spotted that its photo shows
  **ejector-latch arms** on both ends — a latching header, wider at the
  ends, wrong for a dense Eurorack footprint. Mouser's own page carries
  the disclaimer "Images are for reference only", so neither the image
  nor the attribute table is authoritative alone; when they disagree,
  stop and pick a part where they agree.

⚠️ **P2 IS A MICRO-USB, NOT A FULL-SIZE USB-B.** This doc previously said
"Right-angle THT USB-B" — WRONG. Mouser's own description for
105017-0001: "USB Connectors **MICRO USB B** RECPT **BTTM MNT** SMT TH
TABS"; product category "Micro USB Type B Connectors", receptacle/female,
USB 2.0. That matches the pad map (5 SMD signal pads centre + 4 TH
mounting legs) and the RevD board photo. **Order by MPN, never by the old
description.**

⚠️ Mouser flags possible US import tariffs: ~8% on the Yamaichi and the
D6R, **~30% on the Molex**.

### WM8731 spares — NOT NEEDED (resolved 2026-07-25)

**PCBWay populated the codec on all 5 boards.** `BOM-APPROVAL-CHECKLIST.md`
records it: BOM rev 2, line item 40, IC4 = **WM8731SEDS/RV @ $17.44/pc =
$87.20 for 5**, LCSC-sourced by PCBWay, DNP note removed, qty ×5. The
quote rose by a matching amount, so it's real.

**STALE INSTRUCTIONS — DO NOT ACT ON THESE:** `BOM-PCBWay-assembly.csv`
(IC4 row) and `ORDER-GUIDE.md` line 25 still say "DO NOT POPULATE —
customer will hand-solder". Those are the *pre-order* documents; the
approval checklist is what was actually paid for and built.

Spares are therefore optional insurance only, at **~$17.44 ea** (not the
"~$10" this doc used to claim). Sourcing is genuinely hard: **Mouser has
NO bare WM8731** (only $154+ eval boards, all EOL/non-stocked) and
**Rochester has no stock either** — LCSC, as PCBWay used, is the live
source. Arlo's call 07-25: skip them.

## The SD breakout (P1) — footprint truth (CORRECTED 2026-07-25)

**The part is the Yamaichi PJS008U-3000 vertical microSD holder.** The 8
staggered THROUGH-HOLES at 1.1mm pitch + mounts at ±4.3mm are its
staggered DIP solder tails; the card stands VERTICAL off the board
(matches Arlo's test unit). Thonk's description: "vertical Micro SD Card
Reader from Yamaichi, required for Radio Music based projects."

**BUY IT FROM MOUSER — 3x cheaper and deep stock** (verified 2026-07-25):

| Source | Part | Price | Stock |
|---|---|---|---|
| **Mouser (best)** | 945-PJS008U-3000-0 (mfr PJS008U-3000-0) | **$1.38 @1, $1.17 @10, $1.12 @25, $1.05 @100** | **10,877 in stock**, +18,000 due 2026-09-04 |
| Thonk | PJS008U-3000 | £2.99 excl / £3.59 incl VAT ≈ $4.55 | in stock |
| Digi-Key | 2408-PJS008U-3000-0TR-ND | — | **0 in stock**, Marketplace, ships from Yamaichi, "Lead Time Unavailable / No Backorders", tape&reel, non-returnable — NOT a usable source |

Mouser is an **authorized Yamaichi distributor**, and its parametrics
INDEPENDENTLY CONFIRM the footprint match (this is the manufacturer-spec
confirmation the earlier photo-only "verification" lacked): microSD,
**8 contacts, 1 row, 1.10 mm pitch, Through Hole**, PCB mount, 500 mA,
description "MicroSD Card Conn **Ver Dip Mnt** Manual" (Vertical DIP
Mount). Note Mouser flags a possible 8% tariff shipping to the US.
Ignore the other search hit PJS008U-0002 — SMT clam-shell, non-stocked,
MOQ 1200.

Since the kit needs a Mouser order anyway (Molex 538-105017-0001 USB-B,
D6R00F1LFS tacts — see the LCSC/Mouser add-on list), put the SD holders
on that order.

**This section previously recommended SparkFun-sniffer clones — WRONG.**
The sniffer is a flat card-edge-finger board; it neither fits the
through-hole footprint nor mounts vertically. Arlo caught it by
comparing against his test unit ("the slot stands vertical off the
board"). The 1.1mm-pitch coincidence (card-edge pitch ≈ the Yamaichi's
tail pitch) is what made the wrong theory look photo-verified. The
common 2.54mm-header "LC Studio" module remains wrong too.

## Pad-map quick reference (from the KiCad board)

- P1 SD: 8 pads, x = -3.85…+3.85 @ 1.1mm pitch, alternating y (-0.47/-1.57); mounts ±4.3
- POT1 dual: rows y=10.0 & y=7.5, pins x = -2.5/0/+2.5; Ø2.2 holes ±4.4 (unused by Alpha/Same Sky — tabs at ±5.65–5.75 get clipped)
- SW1 encoder: ABC @ y=7.5 (2.5mm pitch), D/E @ y=-7.0 (±2.5), tabs ±6.1
- SW2/3 tact: pins at (±2.5, ±2.5) — 5.0×5.0mm square
- P2 USB-B: TH legs (±2.5,0)+(±3.5,-2.7), Molex SMD signal pads center
- P4 power: 2×5 @ 2.54mm
- L1 LED: A/K @ 2.54mm
