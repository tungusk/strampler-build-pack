# Price estimate — PCBWay turnkey order (2026-07-06)

Assembled option: 2 assembled main boards (SMD only, WM8731 DNP), 5 bare
main PCBs total, 5 panels. Boards measured from the Eagle files:
main 91.3 x 108.0 mm, panel 93.9 x 130.1 mm (18 HP).

| Item | Estimate (USD) |
|---|---|
| Main PCB, 2-layer, qty 5 (assemble 2) | 25–35 |
| Assembly setup + stencil + labour (2 boards, ~144 SMD each, one side) | 70–90 |
| Turnkey parts, 2 board sets (incl. ~15% sourcing markup) | 85–100 |
| Panel, qty 5, matte black + ENIG | 40–60 |
| DHL shipping | 25–35 |
| **PCBWay total** | **≈ 250–320** |

Parts cost is dominated by: R-78E3.3 regulator (~$10/board), MCP3208 (~$4),
ESP32-WROVER-IE (~$4), CP2102N (~$2.50). Plain green HASL panel saves ~$25.
Assembling 1 instead of 2 saves only ~$50 (setup dominates).

## Not covered by PCBWay (per finished module)

| Item | Estimate |
|---|---|
| Thonk: 14x Thonkiconn, 5 pots, SD breakout, knobs | £45–55 |
| AliExpress: ILI9341 2.2" TFT + IPEX antenna | ~$11 |
| Encoder, USB-B, tact switches, LED, headers, standoffs | ~$15 |
| WM8731 x2 (broker: Rochester genuine ~$6–12 ea; UTSource/eBay cheaper, fake risk) | $12–25 |

**All-in, one finished module + one spare assembled board: ~$350–420.**

Exact turnkey numbers come from PCBWay's human BOM review, usually <24 h
after upload (see ORDER-GUIDE.md).
