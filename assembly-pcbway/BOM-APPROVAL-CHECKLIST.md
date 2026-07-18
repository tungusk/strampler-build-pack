# PCBWay BOM approval checklist — pre-payment gate

Quote **T-1N8W1065663A**, revised **$370.65 / 5 units** (component $284.44 +
assembly $29.00 + PCB $57.21), all 5 boards assembled, codec populated.
**BOM rev 2 confirmed 2026-07-16** — full-file diff vs rev 1 showed exactly
one cell changed (IC4 "DO NOT POPULATE" note removed). Remaining step:
Arlo's final engineer pass, then approve/pay on the order page.

## Why no CSV is needed

PCBWay assembles from the BOM revision *you approve*, not from the email
thread. The rep edits their working copy and sends it back for confirmation —
an unambiguous email line is as good as an attached file. The one thing that
actually gates production is which document carries your approval.

## Resolved (verified 2026-07-16, BOM rev 2)

- [x] **IC4 populate landed.** Line item 40: designator IC4, MPN
      **WM8731SEDS/RV** @ $17.44/pc ($87.20/5), sourced by PCBWay from LCSC,
      DNP note removed, qty ×5 — all boards get the codec.
- [x] **Revised quote went UP by a plausible amount.** +$107.02 vs the 07-08
      quote = codec $87.20 + the two previously-unpriced cap lines $19.82.
      No suspicious "free codec" line.
- [x] **Cap substitutions landed with correct 16V MPNs:**
      - C38/C39/C42 → AVX **TAJA226M016RNJ** (22µF 16V 1206, our named sub;
        `016` = 16V)
      - C36 → Panasonic **EEE-FK1C102SV** (verified 1000µF 16V,
        10.0×10.8mm — AEC-Q200 sibling of the FK1C102P we named; 10mm can
        fits case-G pads, 0.6mm taller is a non-issue)
- [x] **WROVER sub correct:** ESP32-WROVER-IE-N8R8, **IPEX variant**
      re-confirmed in the approval reply, accepted @ $7.47.
- [x] **Codec authenticity decision made:** boards get LCSC-sourced
      WM8731SEDS/RV (the best real source — Rochester has NO stock, see
      SOURCING-NOTES). Optional hedge: order a few spare /RV from LCSC
      directly with the sidecar orders.

## Final engineer pass (Arlo, on the order page, before paying)

Package = the fixed KiCad-plotted gerber zips (`gerbers/` — the
`--check-zones` ones), BOM rev 2 as returned by PCBWay, and
`SOURCING-NOTES.md`.

- [ ] Order page shows the **rev 2** BOM (IC4 populate, no DNP note) — not
      an earlier revision.
- [ ] Total on the payment page is **$370.65** — the quote UI had a
      price-ratchet bug before; if the number moved, re-quote clean, don't
      pay a drifted figure.
- [ ] Gerber zips attached to the order are the FIXED KiCad-plotted ones
      (main board B.Cu ~959KB with GND pours, not the 126KB unfilled plot).
- [ ] Panel order: matte black, ENIG.
- [ ] Assembly side = SMD bottom side; CPL is `CPL-Strampler_redesign_v2_2.csv`.
- [ ] Ship-to address + shipping tier sanity check.

## Final gate

- [ ] Pay against the rev 2 BOM / $370.65 quote. Then fire the sidecar
      orders: Thonk (jacks/pots/SD/knobs ~£50) or Qingpu direct,
      AliExpress ILI9341 TFT + IPEX antenna, encoder/USB-B/switches,
      optionally spare WM8731SEDS/RV from LCSC.
