# Sourcing notes — codec + panel components (2026-07-07)

## WM8731 codec (IC4) — the critical part

Stock reality (checked 2026-07-07 via OEMsTrade aggregation):
- **Rochester Electronics: NO stock listed** (despite being the usual
  genuine-EOL route — don't count on them for this part).
- **LCSC: 592 x WM8731SEDS/RV @ $8.38–13.31** — the best real source.
  LCSC is JLCPCB's sister distributor, reputable, same ecosystem as the
  Chinese fabs. `/RV` = tape-and-reel packaging of the SAME SSOP28 chip
  as `/V` (tube). Fully interchangeable.
- HK brokers (IC Components, YIC) list `/RV` at ~$1.53 — **fake-risk tier**,
  a $1.50 obsolete Wolfson codec is usually a remarked blank. Avoid.
- Mouser: /V discontinued, /RV backorder with long lead. Not practical.

**Preferred plan:** ask PCBWay (during BOM review) to source the codec from
LCSC and populate IC4 — see message template below. Boards then arrive
fully SMD-complete, no SSOP28 hand-soldering, and every board carries its
own irreplaceable codec.

**Fallback:** order 7 pcs WM8731SEDS/RV from lcsc.com yourself (~$70 for 5
units + spares) and hand-solder (flux + drag, SSOP28 is very doable).

## Message template for PCBWay BOM review (paste into the order chat)

> Regarding BOM item IC4 (WM8731, currently marked DO NOT POPULATE):
> please quote sourcing **WM8731SEDS/RV** from **LCSC** (approx. 590 pcs
> in stock as of July 2026, ~$8–13/pc) and populate IC4 on all assembled
> boards. Note: WM8731SEDS/RV is the tape-and-reel packaging of
> WM8731SEDS/V — same die, same SSOP28 package, fully interchangeable.
> If you can source it, please remove the DNP flag for IC4 and update the
> quote. If LCSC stock is gone, keep IC4 as DNP.

Where to send it: PCBWay account → Orders → the assembly order → order
message thread / online chat with your service rep (BOM review questions
arrive there or by email — reply in the same thread).

## Jacks & pots — Thonk vs direct

"Thonkiconn" is Thonk's nickname for the **Qingpu WQP-PJ398SM** vertical
mono 3.5 mm jack (~GBP 0.62 at Thonk, ~$0.25–0.35 from Qingpu's own
AliExpress storefront — same manufacturer, same part). For 5 units you
need 70 jacks (order ~80): ~GBP 43 at Thonk vs ~$25 direct, slower ship.

**Footprint warning:** the board is laid out for the PJ398SM pattern
(2 signal pins + wide ground lug). The visually similar PJ301M-12 style
has a DIFFERENT footprint and will not fit. Only buy listings explicitly
marked PJ398SM / WQP-PJ398SM with clear photos.

Pots are standard Alpha 9mm verticals (RD901F style): B10k x4 + B100k
dual-gang x1 per unit — Thonk, Tayda, or Ali all carry them.

## PCBWay quote response (2026-07-08) — quote T-1N8W1065663A, 5 units

Quote received: **$263.63 / 5 units** (component $177.42 + assembly $29.00 +
PCB $57.21), codec EXCLUDED (IC4 still DNP in this quote). ESP32-WROVER-IE-
N8R8 accepted & populated ($7.47) with the IPEX-required note honored.

**Two parts PCBWay flagged out of stock** — subs decided (both 16V, ratings
decoded from the original MPNs since the value column omits voltage):

- **C38 C39 C42 (qty 3) — 22µF 16V tantalum, 1206 (case A).** Original AVX
  TCTAL1C226M8R (`1C`=16V). Subs given: **KEMET T491A226M016AT** or **AVX
  TAJA226M016RNJ** (or any in-stock low-ESR polymer, same size/rating).
  These positions are rail decoupling — MnO2 tant is fine.
- **C36 (qty 1) — 1000µF 16V SMD electrolytic, case "Panasonic G"
  (10×10.2mm).** Original Chemi-Con APXG160ARA102MJA0G (`160`=16V). Subs:
  **Panasonic EEE-FK1C102P** or **Nichicon UWT1C102MNL1GS**. MUST stay 16V +
  10×10.2mm — 25V pushes to a taller/wider can that won't fit case G pads.

**Reply sent to PCBWay:** substitute-your-choice-equivalent for both caps
(named parts as acceptable) + the codec-populate request from the template
above (source WM8731SEDS/RV from LCSC, populate IC4, remove DNP; keep DNP if
LCSC stock gone). Expect the revised total to rise ~$40–65 if they populate
the codec. Awaiting revised quote.

## Per-unit completion cost (if PCBWay populates the codec)

Assembled board (amortized) + jacks/pots direct + TFT + antenna + misc
hardware ≈ **$70–80 per unit** on top of the PCBWay order. Boards keep
forever; buy completion parts only for the units you actually build.

## Revised quote (2026-07-16) — APPROVED at $370.65 / 5 units

Component $284.44 + assembly $29.00 + PCB $57.21 = **$370.65** (+$107 vs the
07-08 quote: WM8731 $87.20 + the two previously-unpriced cap lines $19.82).

- **IC4**: sourced as **WM8731SEDS/RV** @ $17.44/pc ($87.20/5). ⚠️ The BOM
  still carried the old "DO NOT POPULATE" instruction on item 40 — reply told
  PCBWay to populate IC4 on all 5 boards and remove the note.
- **C38/C39/C42**: purchased as **TAJA226M016RNJ** (our named AVX sub, 16V
  case A). Accepted.
- **C36**: purchased as **EEE-FK1C102SV** — verified 1000µF 16V,
  10.0mm dia × 10.8mm (DigiKey). Same 10mm can as case G (0.6mm taller,
  clearance non-issue); it's the current AEC-Q200 sibling of the
  EEE-FK1C102P we named. Accepted. Rep (Remi) couldn't string-match
  "APXG160A102MJA0G" — that's the ORIGINAL Chemi-Con part C36 replaces;
  told them to ignore.
- ESP32-WROVER-IE-N8R8 IPEX-variant note re-confirmed in the reply.
- All BOM quantities are ×5 → **all 5 boards fully assembled**.

Quote approved in the order thread; awaiting production start.

## Confirmed BOM (2026-07-16, rev 2) — READY TO ORDER

PCBWay returned the corrected BOM: full-file diff vs rev 1 shows EXACTLY ONE
cell changed — IC4's "DO NOT POPULATE" note removed. WM8731SEDS/RV stays
sourced/priced ($17.44/pc), all subs and the IPEX note intact, total still
**$370.65 / 5 units, all assembled, codec populated**. Nothing else moved.

Status: Arlo may run one final engineer pass, then approve/pay on the PCBWay
order page. Engineer-pass package = the fixed KiCad-plotted gerber zips (the
--check-zones ones), this BOM rev 2, and this notes file.
