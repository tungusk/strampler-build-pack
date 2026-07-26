# AliExpress cart — verified listings, 2026-07-25 session

Companion to `COMPLETION-SHOPPING-5UNITS.md`. Every listing below was opened
and photo/SKU-checked in-browser this session (Claude + Arlo). Prices are the
**signed-out "welcome deal"** numbers — expect the regular price after login
(regular shown in parens where seen). Welcome deals also carry "max 1 per
shopper" caps that may lift or vanish once signed in.

**Outcome vs the plan: everything sourced on Ali except the Eurorack power
cables. No Thonk order needed** — the SD sniffer and the dual-gang pot (the
two flagged risks) both found verified listings.

## The cart

| # | Part | Listing | SKU to pick | Qty | ~Price |
|---|---|---|---|---|---|
| 1 | Jacks (Thonkiconn/PJ-301M, mono + knurled nuts) | aliexpress.us/item/2251832766984352.html (Shenzhen NingSheng, 5.0★/60 sold) | 200-pc lot | **1 lot = 200 pcs** | $39.83 ($42.25) |
| 2 | B10k pots, RV09 vertical, knurled 18mm shaft | aliexpress.us/item/3256806764561680.html (Jinboli, 4.9★/137 sold) | **B10K B103** | **3 lots × 10 = 30** | $2.39/lot ($2.93) |
| 3 | Dual-gang B100k, Taiwan Alpha RD902F | aliexpress.us/item/3256811723023981.html (Franchise Switch, 5★/417 sold) | RD902F-B100K, D-shaft 15mm | **2 lots × 5 = 10** | $18.50/lot |
| 4 | EC12 encoder w/ push switch, 24 det | aliexpress.us/item/3256807315397735.html (Tongxuan, 4.8★/323 sold) | **20mm** (knurled) | **4 lots × 2 = 8** | $0.99/lot ($2.68) |
| 5 | 2.2" ILI9341 TFT (MSP2202) — ORIGINAL BOM link, still alive | aliexpress.us/item/2251832421426963.html (EQV Official, 5★) | — | **6** | $5.99 + $4.80 ship |
| 6 | 2.4GHz antenna + u.FL pigtail set | aliexpress.us/item/3256807801327960.html (XYANT, 4.9★/900+ sold) | **"SMA Male to IPEX1"** (antenna+pigtail set) | **4 lots × 2 = 8** | $0.99/lot ($2.58) |
| 7 | microSD sniffer breakout (SparkFun clone) | aliexpress.us/item/3256809057269319.html (Great IT, 4.9★/600+ sold) | **10PCS** pack | **1 × 10** | ~$2/10 welcome ($4.92/5 reg) |
| 8 | Knobs, Davies 1900h clone, SET SCREW | aliexpress.com/item/1005006890019684.html (DAIERBUMP, 4.8★/600+ sold) | 6mm bore | **3 lots × 10 = 30** | $1.33/lot ($14.26?) |
| 9 | M3 10mm F-F standoffs ×30 + M3 6mm screws ×60 | any assortment kit — search "M3 brass standoff kit" | — | 1 kit | ~$5-8 |

Rough total: **$85–110** signed-in, well under the doc's $110–140 estimate.

## Verification notes (what was actually checked)

- **Jacks (#1):** photos show the WQP mono profile — box body, threaded
  collar, knurled nuts included, 2 signal pins + wide ground tab. Thonk's own
  page confirms PJ301M-12 / PJ398SM / WQP518MA are all interchangeable
  Thonkiconns (tab material differs only). $0.20/pc vs Thonk £0.38.
  Residual risk: photos can't prove sub-mm footprint; 200-lot leaves margin.
- **Dual pot (#3):** exact Alpha MPN **RD902F-B100K** in title, green Taiwan
  Alpha body "0B100K" visible. Gallery's other shots are recycled stock
  photos — pin rows NOT visually confirmed; MPN + genuine-Alpha look is the
  evidence. D-shaft ("half-axle") → use set-screw knobs (#8 covers this).
- **Encoder (#4):** 5 pins + push, EC12 = ALPS EC12E pattern; a review
  confirms correct quadrature phasing. 20mm SKU photo = knurled shaft.
- **SD sniffer (#7):** zoomed photo shows the 8 **staggered** card-edge
  fingers + DAT/CLK/CMD/CD labels = SparkFun sniffer clone geometry the
  KiCad footprint expects (1.1mm pitch stagger). The doc's ⚠️ item — PASSED.
- **B10k pots (#2):** 18mm shaft vs Alpha 15mm — knobs sit ~3mm prouder,
  cosmetic only. Pin/mount layout is standard RV09 vertical.
- **Antenna (#6):** set = folded rod (SMA male) + u.FL(IPEX-1)→SMA-female
  bulkhead pigtail 15cm. Plugs into the WROVER-IE's u.FL; rod can
  panel/case-mount on the bulkhead.

## NOT on AliExpress

- **Eurorack power cables 10-pin→16-pin ×5** — two searches found nothing
  eurorack-specific. Get from Thonk/Tayda/Amazon, or existing case spares,
  or DIY (2×5 + 2×8 IDC + ribbon).

## Unchanged from the main doc

- **LCSC add-on** still as written in `COMPLETION-SHOPPING-5UNITS.md`:
  D6R00F1LFS tacts ×12, Molex 105017-0001 USB-B ×6, 5mm red LED ×10,
  2×5 shrouded header ×10, WM8731SEDS/RV spares ×2-3.
- WM8731 main stock: already populated on the PCBWay boards.

## CART SIGNED OFF 2026-07-25 — est. $197.95, awaiting Arlo's checkout click

Arlo accepted the jack-lot risk explicitly; duals bumped back to 2 lots
(10 pcs) as the one insurance line. Claude: comfortable with every line as
carted. On arrival: test-fit ONE jack + ONE dual on a bare board with
calipers BEFORE soldering the run (both risks resolve in 10 minutes;
90-day free returns cover a miss).

Revised per Arlo mid-session: spares trimmed to lean, and the hinged XYANT
antennas swapped for **straight slim antennas** (Arlo: "I like the straight
stubby antennas better than the giant ones with the hinge").

Final 10 lines:
jacks 200pc ×1 $41.83 · RV09 B10K ×2 (20, exact) $2.49 ·
RD902F-B100K ×2 (10 = 5+5, deliberate insurance on the MPN-only line) $18.50 · EC12 20mm ×3 (6 = 5+1) $2.68 ·
TFT ×6 (5+1, fragile in transit) $5.99 ·
**MGCKTD straight 3dBi antenna + U.FL→RP-SMA pigtail, 5-SET pack ×1 $6.65**
(aliexpress.us/item/3256805483874281.html, 5★/316 sold — replaces XYANT;
kept mainly for its 5 U.FL→RP-SMA bulkhead pigtails, whips = spares) ·
**2.4G mini STRAIGHT stub antennas RP-SMA ×3 packs = 6 pcs $1.47/2pc**
(aliexpress.us/item/3256807938705105.html, 4.9★/500+ — Arlo prefers the
stubby look; screw onto the MGCKTD pigtail bulkheads. NOTE: the 915MHz
LoRa lookalike Arlo first found is the WRONG BAND — always check 2.4GHz) ·
~~SD sniffer 10PCS~~ **REMOVED — WRONG PART** (see below) ·
knobs BLACK ×3 (30; 25 needed) $4.49 ·
M3×10 F-F standoffs 60pc ×1 $6.61 · **M3×6 screws 304SS 50pc ×1 $1.88**
(aliexpress.us/item/2251832785290389.html, SKU M3 50pcs + 6mm).
**Subtotal $150.85 + $19.36 ship − $2 = est. $168.21.**
Knobs are 6.35mm-bore set-screw — grub screw clamps 6mm shafts fine.

## ✅ ORDER PLACED 2026-07-26 — AliExpress 11 lines, $186.02

(Mouser's companion order, 6 lines / $57.04, placed the same day — see
`COMPLETION-SHOPPING-5UNITS.md`.) Encoder caps went out at **1 lot**
(10 caps) after Arlo trimmed from 4. Everything below is the sourcing
record for reference / reorders.

## Ali cart as verified = 11 lines, est. total $190.82 (pre-trim)

(Was 10 lines / $184.42 before the encoder-cap addition below.)

**+ ENCODER CAP (added 07-25):** "10PCS For KY-040 … ABS D Half Shaft
Hole Caps Knob 6mm", item 3256806101256136, $1.60/10 × **4 lots = 40
caps, $6.40** (4 = the seller's whole remaining stock). Hard ABS, true
6mm **D-bore**, **no indicator line**, flat top for the push switch —
see `COMPLETION-SHOPPING-5UNITS.md` for why the encoder gets its own cap
and which candidates were rejected. Knock-on: the 30 Davies knobs now
cover only 25 pot positions, restoring a +5 spare there.

## Earlier verified state — 10 lines, $184.42

Re-read line by line 2026-07-25 after Arlo asked "does that make both
carts ready?": antenna stubs **Straight-2pcs-RP SMA** ×3 (=6) · TFT ×6 ·
RD902F-B100K ×2 (=10) · RV09 **B10K B103** ×2 (=20) · PJ-301M jacks ×1
(=200) · MGCKTD antenna **5set** ×1 · M3×6 screws 50pc ×1 · M3×10
standoffs 60pc ×1 · knobs **Black** ×3 (=30) · EC12 **20mm** ×3 (=6).
All 10 lines selected/checked.

⚠️ **The SD-sniffer removal had to be done TWICE.** The first delete
(earlier the same day) silently did not apply — the line was still in the
cart at re-check, and only a second attempt with the confirm dialog took.
Total fell $197.37 → $184.42, exactly the $12.95. **Both AliExpress and
Mouser cart deletes need a confirm dialog and can silently no-op —
always re-read the cart to verify a removal.**

**SD CORRECTION (later 07-25): the Ali sniffer 10-pack was REMOVED — wrong
part.** Arlo caught it against his test unit (vertical slot). Correct P1 =
**Yamaichi PJS008U-3000 vertical microSD holder**.

**SOURCE IT FROM MOUSER, NOT THONK** (checked 07-25): Mouser
945-PJS008U-3000-0, **$1.17 ea @qty10, 10,877 in stock**, authorized
Yamaichi distributor, parametrics confirm 8-contact / 1.10 mm / through-hole
/ "Ver Dip Mnt". Thonk is £3.59 incl VAT (~$4.55) — 3x the price. Digi-Key
has ZERO stock (marketplace, no backorders). Full table in
`COMPLETION-SHOPPING-5UNITS.md`.

## THONK — ABANDONED 2026-07-25 (Arlo's call)

A cart was staged (6 Yamaichi + 5 power cables, £31.49) then dropped:
SD holders go to Mouser at 1/3 the price, and Arlo sources power cables
separately ("nice but not actually part of the module"). Nothing to buy
from Thonk. Cable reference if ever needed: Thonk "Eurorack Power Cables",
**10-16 Pin** variants (module end = the 2×5 P4 header, bus end = 16-pin),
Micro 8cm £1.50 / Short 15cm £1.66 / Long 25cm £1.91 / XL 0.5m £2.52,
volume discount from 5 up.

## MOUSER ORDER (the second order — see COMPLETION-SHOPPING-5UNITS.md)

SD holders + tacts + Molex micro-USB + LED + 2×5 header. WM8731 spares
DROPPED (PCBWay already populated all 5 codecs — see that doc). Rough
parts total ~$40 before shipping/tariffs.

**NOT moved to Mouser: everything already in the Ali cart.** Mouser would
be 5–10× on jacks/pots/encoders/knobs/TFT (e.g. jacks $0.20 ea on Ali vs
$2–3 at Mouser), and the Ali cart is already verified and signed off.
Reversible if Arlo ever wants single-vendor sourcing at that premium.

## Process notes
- Avoid listings tagged "FREE GIFT / with any purchase" — they open promo
  funnels, not product pages.
- AliExpress search is part-number-blind for PJ398SM/WQP518MA; the winning
  queries were "PJ301M-12 3.5mm jack", "RD902F B100K", "EC12 rotary encoder
  push switch 20mm", "microSD sniffer TF card extender adapter board".
