# Knob cap options — browsing notes, 2026-09-11

Shopping for **looks**, not a commit. Nothing ordered. This file exists so the
research does not have to be redone.

---

## What is on the panel now

| Position | Qty/unit | Shaft | Cap fitted |
|---|---|---|---|
| POT1 GAIN (dual-gang) | 1 | 6 mm **knurled T18** | Davies 1900h clone, set screw |
| POT2–5 = CV 5–8 (Same Sky PTN091) | 4 | 6 mm **knurled 18T** | same |
| SW1 DATA (EC12 encoder) | 1 | 6 mm **D-shaft** | separate push-on D-bore cap |

Both bought on AliExpress, order placed 2026-07-26 (see `ORDER-CART-ALI-20260725.md`):

- **Knobs** — item `1005006890019684` → redirects to `3256806703704932`
  (DAIERBUMP, "1900 Davies Style 6.35MM Knob Metal Insert"). **6.35 mm bore,
  brass insert, set screw.** 30 on hand, black. 6 colours offered: white, red,
  green, blue, black, cream. ~$1.09–1.50 per 10.
- **Encoder cap** — item `3256806101256136`, KY-040 style, true 6 mm **D-bore**,
  hard ABS, **no indicator line**, flat top for the push switch. 40 on hand.

> **The set screw is the important part.** A 6.35 mm round bore with a grub
> screw clamps ANY 6 mm shaft — T18 knurled and D alike — so one part can serve
> all six positions. Splined (T18) and D-bore push-on caps cannot: each fits
> only its own shaft profile. When screening alternatives, set-screw parts are
> the flexible ones.

---

## The panel decides what fits

Parsed from `hardware-kicad/strampler_panel_v2_3.kicad_pcb` (do not eyeball this
— parse it):

- **CV 5–8 row** (y −45.83): x = 13.90 / 35.12 / 56.33 / 77.54, drill 7.2 mm
- **Control row** (y −65.10): GAIN (7.2), TR1 (9.5), TR2 (9.5), encoder (8.2)
- **Horizontal pitch: 21.22 mm** (both rows)
- **Row-to-row gap: 19.27 mm**  ← **the binding constraint**

Two adjacent knobs touch when the **sum of their radii** reaches the gap:

- Same knob everywhere → max **19.27 mm** diameter touching, **≈17 mm** for a
  ~2 mm visual gap.
- **Mixed sizes are the escape hatch.** Small knobs on the control row (GAIN +
  DATA) let the four CV knobs grow to **~19 mm**: 2.2 mm clearance horizontally
  at the 21.22 mm pitch, 3.8 mm to the row above. This also restores DATA's
  by-feel distinction (see the 07-25 reasoning in `COMPLETION-SHOPPING-5UNITS.md`)
  through size contrast instead of a different part family.

Standing rules from earlier rounds: **plastic, not aluminium**; **not
soft-touch**; the **encoder wants no indicator line** (an encoder has no
absolute position, so a pointer points at nothing).

---

## Thonk — thonk.co.uk (UK, ships worldwide, prices ex-VAT)

Worth using as the **spec sheet** even if buying elsewhere: every product lists
diameter and height, which Ali listings almost never do.

### The direct equivalent of what is fitted
**Davies 1900h Clone – 6.35 mm Round Shaft** — `/shop/1900h-round/` — £1.30
"High quality brass insert with set screw, 6.4 mm shaft, ABS, 12 mm diameter at
the base and 16 mm tall." **20 colours**: black, dark red, chocolate, green,
white, transparent, orange, light blue, natural, cream, mustard, forest, yellow,
dark blue, pink, violet, light grey, dark grey, red, blue + black NO-LINE.

Same family, other fittings (push-on, so each fits only its own shaft):
- `/shop/1900h-t18/` £0.75 — T18 splined, **pots only**, ~20 colours,
  + Black and Transparent **NO-LINE** at £0.68
- `/shop/1900h-d/` £0.75 — D-bore, **encoder only**, 20 colours,
  + **NO-LINE in black, white, light grey, dark grey, cream** at £0.68
  (red no-line was out of stock)

> **Note for the encoder:** the D-shaft no-line variants would let DATA use the
> same mould family and colour stock as the pots while still having no pointer.
> The listing's warning that "the pointer is on the curved side of the D … not
> suitable for all D-shaft pots" is irrelevant on a no-line knob — there is no
> pointer to misalign. Trade-off: same 12 mm body as the pots, so the by-feel
> distinction is lost unless sizes are mixed.

Bulk on all of the above: 10+ −5%, 25+ −7%, 100+ −10%, 500+ −20%.

### 6.35 mm set-screw alternatives that FIT (≤ ~17 mm)

| Design | Ø | H | £ | character |
|---|---|---|---|---|
| Davies 1900h clone | 12 | 16 | 1.30 | *current* — tall, fluted, skirted |
| **Small Fluted** `/shop/knobs-small-fluted/` | 15 | 10.5 | **0.74** | ribbed barrel, no skirt, much lower |
| **Small Ridged Pointer** `/shop/small-ridged-pointer/` | 13 (14.5 at tip) | 13 | 1.30 | ridged, pointed nose; black/white/lt-grey only |
| **Synth Pointer – Mini** `/shop/synth-pointer-knobs/` | 14 | 11 | 1.05 | Synth Tech / Pittsburgh / L-1 look, same brass insert as the 1900h |
| **Synth Pointer – Small** | 16 | 11 | ~1.2 | same family; 3.3 mm clearance, tight but legal |
| Rogan RB `/shop/rogan-buchla/` | **not stated** | — | 0.22–4.50 | Buchla / Verbos look, USA made — **measure before buying** |

### Ruled out on size

| | Ø | why |
|---|---|---|
| Erica Synths small `/shop/erica-knobs-6-35mm-shaft/` | 19 | 0.27 mm to the row below |
| Small Fluted **Skirt** | 19 | same |
| 'Mini MXR' `/shop/mini-mxr/` (T18 only) | 19 | same — a shame, Thonk colour-match it to the 1900h |
| 'MXR' small / large `/shop/mxr-style-knobs/` | 20 / 25 | **exceeds** the 19.27 gap — would collide |
| Erica medium / large | 24 / 28 | too big |
| Synth Pointer medium / large | 27 / 33 | too big |
| Davies Fine XL Skirted 1600BM `/shop/1600bm/` | **38.1** | genuine Davies, way out |

Ruled out on the standing rules: **Bastl aluminium**, **Sifam Soft Touch encoder
knobs**, **Spectrum soft-touch D-shaft set**.

---

## AliExpress — far more variety, roughly 1/10 the price

Your knob is really a **guitar-pedal knob**, and that category is enormous.
Search that lands well: `6.35mm knob set screw guitar pedal`. Same test applies
— 6.35 mm bore + set screw fits all six positions.

**Pulled up and eyeballed 2026-09-11:**

| Design | Item | Price | Notes |
|---|---|---|---|
| **Smooth barrel cap, 13 × 16 mm** | `3256805934267586` | **$1.09/10 = $0.11 ea** | **Dimensions actually stated.** 13 mm Ø × 16 mm tall ≈ the 1900h footprint (12 × 16), so clearance is a non-question. Smooth, no skirt, no flutes, **no indicator line**. 7 colours: black, green, orange, purple, red, white, yellow. Cleanest and cheapest of the lot. |
| **Davies 1510** | `3256812318817007` | $4.56 / 5–10 pc | NOT a smaller skirted knob as assumed — it is a **duckbill pointer**: flat top, protruding nose, no fluting. ABS, black only in this listing. |
| **Skirted "jazz bass"** | `3256806512237215` | $1.09/5 = $0.22 ea | Wide skirt, fluted cap, dot-and-line indicator. Closest in spirit to the 1900h but broader and flatter. 9 colours incl. red, cream, green, grey, yellow, purple. |
| **Chicken head, clear** | `3256807642556410` | $7.72/16 | Translucent body, black pointer, brass insert. Biggest visual statement. **No dimensions given** — chicken heads run long nose-to-tail and the row gap is 19.27 mm, so measure before buying. |

**Seen in search, not opened:**
- `3256806897372581` — 15× Davies 1510 **style pointer**, 1/4" 6.4 mm
- `3256812045540311` — Davies 1510 **duckbill**, listing says **19 × 1x mm**
- `3256807826974915` — 100 pc **18T** 1900H style — splined, **pots only**
- `3256807544573411` — 10 pc "silver top" (plastic body, metal cap)
- `3256807512572484` / `3256807505096421` — KN-19-14 knurled pedal knob
- `3256806065523459` — Davies 1900 style **aluminium** — fails the no-metal rule
- `3256812885747807` — chrome dome, all metal — same

DAIERBUMP and DaierTek are the same seller family already used, so a re-order
consolidates shipping.

---

## Conclusions

1. **Spec at Thonk, buy on Ali.** Thonk publishes Ø and height on everything;
   Ali mostly gives a photo. With 19.27 mm between rows that spec is the one
   thing that cannot be guessed. Identify the archetype and its real dimensions
   where they are published, then find the same thing for a tenth the price —
   which is exactly the story of the 1900h already fitted.
2. **If one thing gets ordered for looks**, the smooth 13 × 16 barrel
   (`3256805934267586`) is the pick: published dimensions that clear the panel,
   $0.11, and no indicator line — which suits the encoder as well as the pots.
3. **If the pointer stays**, the skirted jazz-bass is the silhouette change.
4. **Mixing sizes is unexplored and cheap** — small on GAIN + DATA, ~19 mm on
   the four CVs. Nothing on the panel forbids it and it solves DATA-by-feel.
