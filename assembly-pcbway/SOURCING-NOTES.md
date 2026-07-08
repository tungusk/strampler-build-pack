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

## Per-unit completion cost (if PCBWay populates the codec)

Assembled board (amortized) + jacks/pots direct + TFT + antenna + misc
hardware ≈ **$70–80 per unit** on top of the PCBWay order. Boards keep
forever; buy completion parts only for the units you actually build.
