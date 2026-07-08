#!/bin/bash
# Regenerate all fab outputs from the KiCad boards after editing.
# Usage: ./make-fab-files.sh   (writes into ../gerbers/)
set -e
cd "$(dirname "$0")"
CLI="${KICAD_CLI:-$HOME/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}"
MAIN=project/Strampler_redesign_v2_2.kicad_pcb
PANEL=strampler_panel_v2_2.kicad_pcb
OUT=../gerbers

TMP=$(mktemp -d)
# --- main board: gerbers + drills + centroid ---
"$CLI" pcb export gerbers -o "$TMP/main/" --check-zones \
  -l F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts "$MAIN"
"$CLI" pcb export drill -o "$TMP/main/" --format excellon --excellon-separate-th "$MAIN"
"$CLI" pcb export pos --format csv --units mm --side both -o "$OUT/CPL-kicad-origin.csv" "$MAIN"
rm -f "$OUT/gerbers-main-Strampler_redesign_v2_2.zip"
(cd "$TMP/main" && zip -jq "$OLDPWD/$OUT/gerbers-main-Strampler_redesign_v2_2.zip" ./*)

# --- panel: gerbers + drills ---
# NOTE: if you re-import the panel from Eagle, remember the importer creates
# UNFILLED zones (empty plots!) and puts restrict layers on "UNDEFINED" —
# this repo's panel .kicad_pcb is already fixed; edit THAT, not a re-import.
"$CLI" pcb export gerbers -o "$TMP/panel/" --check-zones \
  -l F.Cu,B.Cu,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts "$PANEL"
"$CLI" pcb export drill -o "$TMP/panel/" --format excellon "$PANEL"
rm -f "$OUT/gerbers-panel-strampler_panel_v2_2.zip"
(cd "$TMP/panel" && zip -jq "$OLDPWD/$OUT/gerbers-panel-strampler_panel_v2_2.zip" ./*)

rm -rf "$TMP"
echo "Done: $OUT/"
ls -la "$OUT"
