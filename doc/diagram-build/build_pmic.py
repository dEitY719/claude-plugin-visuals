"""Generate PMIC system architecture .excalidraw file.

Layout:
- Top center: External Vref source
- Top half: MAIN PMIC (large container) with EX→SAR ADC and NTC→DSM ADC paths,
  plus internal SPMI master block
- Bottom: 5 SUB-PMIC chips (each with 16:1 MUX → SAR ADC, Vref + SPMI inputs)

ADC and MUX shapes are drawn as trapezoid polygons (input wide, output narrow),
matching the conventional schematic symbol for an analog block.
"""

import json
import itertools

_id_counter = itertools.count(1)
_seed_counter = itertools.count(10000)


def _id(prefix: str = "el") -> str:
    return f"{prefix}_{next(_id_counter)}"


def _seed() -> int:
    return next(_seed_counter)


# ---------------------------------------------------------------------------
# Color palette (from references/color-palette.md)
# ---------------------------------------------------------------------------
COLORS = {
    "primary_fill": "#3b82f6",
    "primary_stroke": "#1e3a5f",
    "secondary_fill": "#60a5fa",
    "tertiary_fill": "#93c5fd",
    "trigger_fill": "#fed7aa",
    "trigger_stroke": "#c2410c",
    "success_fill": "#a7f3d0",
    "success_stroke": "#047857",
    "decision_fill": "#fef3c7",
    "decision_stroke": "#b45309",
    "ai_fill": "#ddd6fe",
    "ai_stroke": "#6d28d9",
    "inactive_fill": "#dbeafe",
    "inactive_stroke": "#1e40af",
    "title": "#1e40af",
    "subtitle": "#3b82f6",
    "body": "#64748b",
    "on_light": "#374151",
}


# ---------------------------------------------------------------------------
# Element factories
# ---------------------------------------------------------------------------
def rect(x, y, w, h, *, fill="transparent", stroke=None, stroke_width=2,
         stroke_style="solid", rounded=True, eid=None):
    return {
        "type": "rectangle",
        "id": eid or _id("rect"),
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke or COLORS["primary_stroke"],
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "roundness": {"type": 3} if rounded else None,
    }


def text(x, y, w, h, content, *, color=None, size=16, align="center",
         valign="middle", container=None, eid=None):
    return {
        "type": "text",
        "id": eid or _id("text"),
        "x": x, "y": y, "width": w, "height": h,
        "text": content,
        "originalText": content,
        "fontSize": size,
        "fontFamily": 3,
        "textAlign": align,
        "verticalAlign": valign,
        "strokeColor": color or COLORS["on_light"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "containerId": container,
        "lineHeight": 1.25,
    }


def line(x, y, points, *, stroke=None, stroke_width=2, stroke_style="solid",
         fill="transparent", fill_style="solid", eid=None):
    pts = [list(p) for p in points]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return {
        "type": "line",
        "id": eid or _id("line"),
        "x": x, "y": y,
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "strokeColor": stroke or COLORS["body"],
        "backgroundColor": fill,
        "fillStyle": fill_style,
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "points": pts,
    }


def arrow(x, y, points, *, stroke=None, stroke_width=2, stroke_style="solid",
          end_arrow="arrow", start_arrow=None, eid=None):
    pts = [list(p) for p in points]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return {
        "type": "arrow",
        "id": eid or _id("arr"),
        "x": x, "y": y,
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "strokeColor": stroke or COLORS["primary_stroke"],
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(),
        "version": 1,
        "versionNonce": _seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "points": pts,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": start_arrow,
        "endArrowhead": end_arrow,
    }


def trapezoid(x, y, w, h, *, fill, stroke, eid=None, inset_ratio=0.22,
              direction="right"):
    """Closed trapezoid polygon (input wide, narrow output).

    direction='right'  -> wide on left, narrow on right (typical ADC/MUX symbol)
    """
    inset = h * inset_ratio
    if direction == "right":
        pts = [(0, 0), (w, inset), (w, h - inset), (0, h), (0, 0)]
    else:
        pts = [(0, inset), (w, 0), (w, h), (0, h - inset), (0, inset)]
    return line(x, y, pts, stroke=stroke, stroke_width=2,
                fill=fill, fill_style="solid", eid=eid)


# ---------------------------------------------------------------------------
# Build elements
# ---------------------------------------------------------------------------
elements = []


# ====== TITLE ======
elements.append(text(80, 20, 1100, 36,
                     "PMIC System Architecture  —  1 Main PMIC + 5 Sub PMICs",
                     color=COLORS["title"], size=26, align="left"))
elements.append(text(80, 60, 1100, 24,
                     "ADCs draw Vref from off-chip; MAIN ↔ SUBs communicate over SPMI",
                     color=COLORS["body"], size=14, align="left"))


# ====== EXTERNAL Vref SOURCE ======
VREF_X, VREF_Y, VREF_W, VREF_H = 1850, 30, 220, 70
elements.append(rect(VREF_X, VREF_Y, VREF_W, VREF_H,
                     fill=COLORS["trigger_fill"],
                     stroke=COLORS["trigger_stroke"], stroke_width=2))
elements.append(text(VREF_X + 10, VREF_Y + 12, VREF_W - 20, 22,
                     "External Vref Source",
                     color=COLORS["trigger_stroke"], size=16, align="center",
                     valign="top"))
elements.append(text(VREF_X + 10, VREF_Y + 38, VREF_W - 20, 20,
                     "(off-chip reference)",
                     color=COLORS["body"], size=12, align="center", valign="top"))


# ====== MAIN PMIC OUTLINE ======
M_X, M_Y, M_W, M_H = 80, 130, 1700, 690
elements.append(rect(M_X, M_Y, M_W, M_H,
                     fill="transparent",
                     stroke=COLORS["primary_stroke"], stroke_width=3))

# Title bar inside main
elements.append(rect(M_X, M_Y, M_W, 38,
                     fill=COLORS["primary_fill"],
                     stroke=COLORS["primary_stroke"], stroke_width=2,
                     rounded=False))
elements.append(text(M_X + 16, M_Y + 6, 360, 26,
                     "MAIN  PMIC",
                     color="#ffffff", size=20, align="left", valign="top"))
elements.append(text(M_X + M_W - 380, M_Y + 8, 364, 24,
                     "DSM ADC + SAR ADC + 8 EX + 10 NTC",
                     color="#ffffff", size=13, align="right", valign="top"))


# ====== EX CHANNELS (8 sources, drawn as 16-wide block with ...) ======
EX_LEFT_X = M_X + 30           # 110
EX_RIGHT_X = 530               # where lines terminate (mux input)
EX_TOP_Y = M_Y + 80             # 210
EX_LINE_GAP = 22

elements.append(text(EX_LEFT_X, EX_TOP_Y - 36, 360, 24,
                     "EX Sources  (8 channels — shown as 16 inputs)",
                     color=COLORS["title"], size=15, align="left", valign="top"))

# Pin labels + lines.  We draw EX1, EX2, EX3 + ... + EX16 (rows of horizontal lines)
ex_rows = [
    ("EX 1", EX_TOP_Y),
    ("EX 2", EX_TOP_Y + EX_LINE_GAP),
    ("EX 3", EX_TOP_Y + 2 * EX_LINE_GAP),
]
ex_dot_y = EX_TOP_Y + 3 * EX_LINE_GAP + 4
ex_last_y = EX_TOP_Y + 5 * EX_LINE_GAP + 4
ex_rows_after = [
    ("EX 16", ex_last_y),
]

# horizontal lines for visible rows
for label, y in ex_rows:
    elements.append(text(EX_LEFT_X, y - 9, 56, 18, label,
                          color=COLORS["on_light"], size=12, align="left",
                          valign="top"))
    elements.append(line(EX_LEFT_X + 60, y, [(0, 0), (EX_RIGHT_X - (EX_LEFT_X + 60), 0)],
                         stroke=COLORS["body"], stroke_width=1))

# vertical "..." marker
elements.append(text(EX_LEFT_X + 4, ex_dot_y - 4, 80, 32, "⋮",
                     color=COLORS["body"], size=24, align="left", valign="top"))
elements.append(text(EX_LEFT_X + 80 + 200, ex_dot_y - 4, 60, 28, "⋯",
                     color=COLORS["body"], size=22, align="left", valign="top"))

for label, y in ex_rows_after:
    elements.append(text(EX_LEFT_X, y - 9, 56, 18, label,
                          color=COLORS["on_light"], size=12, align="left",
                          valign="top"))
    elements.append(line(EX_LEFT_X + 60, y, [(0, 0), (EX_RIGHT_X - (EX_LEFT_X + 60), 0)],
                         stroke=COLORS["body"], stroke_width=1))


# ====== MUX 16:1 (EX → SAR ADC) ======
MUX_EX_X, MUX_EX_Y, MUX_EX_W, MUX_EX_H = 530, EX_TOP_Y - 18, 110, 180
elements.append(trapezoid(MUX_EX_X, MUX_EX_Y, MUX_EX_W, MUX_EX_H,
                          fill=COLORS["tertiary_fill"],
                          stroke=COLORS["primary_stroke"]))
elements.append(text(MUX_EX_X + 6, MUX_EX_Y + MUX_EX_H/2 - 24, MUX_EX_W - 12, 22,
                     "MUX",
                     color=COLORS["primary_stroke"], size=16, align="center",
                     valign="top"))
elements.append(text(MUX_EX_X + 6, MUX_EX_Y + MUX_EX_H/2, MUX_EX_W - 12, 22,
                     "16 : 1",
                     color=COLORS["primary_stroke"], size=14, align="center",
                     valign="top"))


# ====== SAR ADC (Main) trapezoid ======
SAR_X, SAR_Y, SAR_W, SAR_H = 700, MUX_EX_Y + 12, 200, 156
elements.append(trapezoid(SAR_X, SAR_Y, SAR_W, SAR_H,
                          fill=COLORS["secondary_fill"],
                          stroke=COLORS["primary_stroke"]))
elements.append(text(SAR_X + 14, SAR_Y + 30, SAR_W - 28, 26, "SAR ADC",
                     color=COLORS["primary_stroke"], size=18, align="center",
                     valign="top"))
elements.append(text(SAR_X + 14, SAR_Y + 60, SAR_W - 28, 22, "(Main)",
                     color=COLORS["primary_stroke"], size=12, align="center",
                     valign="top"))

# MUX_EX output → SAR ADC input
mux_ex_out_y = MUX_EX_Y + MUX_EX_H / 2
sar_in_y = SAR_Y + SAR_H / 2
elements.append(line(MUX_EX_X + MUX_EX_W, mux_ex_out_y,
                     [(0, 0), (SAR_X - (MUX_EX_X + MUX_EX_W), sar_in_y - mux_ex_out_y)],
                     stroke=COLORS["primary_stroke"], stroke_width=2))


# ====== NTC CHANNELS (10) ======
NTC_TOP_Y = M_Y + 380
NTC_LINE_GAP = 22

elements.append(text(EX_LEFT_X, NTC_TOP_Y - 36, 320, 24,
                     "NTC Channels  (10 thermistors)",
                     color=COLORS["title"], size=15, align="left", valign="top"))

ntc_rows = [
    ("NTC 1", NTC_TOP_Y),
    ("NTC 2", NTC_TOP_Y + NTC_LINE_GAP),
    ("NTC 3", NTC_TOP_Y + 2 * NTC_LINE_GAP),
]
ntc_dot_y = NTC_TOP_Y + 3 * NTC_LINE_GAP + 4
ntc_last_y = NTC_TOP_Y + 5 * NTC_LINE_GAP + 4
ntc_rows_after = [
    ("NTC 10", ntc_last_y),
]

for label, y in ntc_rows:
    elements.append(text(EX_LEFT_X, y - 9, 56, 18, label,
                          color=COLORS["on_light"], size=12, align="left",
                          valign="top"))
    elements.append(line(EX_LEFT_X + 60, y, [(0, 0), (EX_RIGHT_X - (EX_LEFT_X + 60), 0)],
                         stroke=COLORS["body"], stroke_width=1))

elements.append(text(EX_LEFT_X + 4, ntc_dot_y - 4, 80, 32, "⋮",
                     color=COLORS["body"], size=24, align="left", valign="top"))
elements.append(text(EX_LEFT_X + 80 + 200, ntc_dot_y - 4, 60, 28, "⋯",
                     color=COLORS["body"], size=22, align="left", valign="top"))

for label, y in ntc_rows_after:
    elements.append(text(EX_LEFT_X, y - 9, 56, 18, label,
                          color=COLORS["on_light"], size=12, align="left",
                          valign="top"))
    elements.append(line(EX_LEFT_X + 60, y, [(0, 0), (EX_RIGHT_X - (EX_LEFT_X + 60), 0)],
                         stroke=COLORS["body"], stroke_width=1))


# ====== MUX 10:1 for NTC ======
MUX_NTC_X, MUX_NTC_Y, MUX_NTC_W, MUX_NTC_H = 530, NTC_TOP_Y - 18, 110, 180
elements.append(trapezoid(MUX_NTC_X, MUX_NTC_Y, MUX_NTC_W, MUX_NTC_H,
                          fill=COLORS["tertiary_fill"],
                          stroke=COLORS["primary_stroke"]))
elements.append(text(MUX_NTC_X + 6, MUX_NTC_Y + MUX_NTC_H/2 - 24, MUX_NTC_W - 12, 22,
                     "MUX",
                     color=COLORS["primary_stroke"], size=16, align="center",
                     valign="top"))
elements.append(text(MUX_NTC_X + 6, MUX_NTC_Y + MUX_NTC_H/2, MUX_NTC_W - 12, 22,
                     "10 : 1",
                     color=COLORS["primary_stroke"], size=14, align="center",
                     valign="top"))


# ====== DSM ADC trapezoid ======
DSM_X, DSM_Y, DSM_W, DSM_H = 700, MUX_NTC_Y + 12, 200, 156
elements.append(trapezoid(DSM_X, DSM_Y, DSM_W, DSM_H,
                          fill=COLORS["ai_fill"],
                          stroke=COLORS["ai_stroke"]))
elements.append(text(DSM_X + 14, DSM_Y + 30, DSM_W - 28, 26, "DSM ADC",
                     color=COLORS["ai_stroke"], size=18, align="center",
                     valign="top"))
elements.append(text(DSM_X + 14, DSM_Y + 60, DSM_W - 28, 22, "(Main)",
                     color=COLORS["ai_stroke"], size=12, align="center",
                     valign="top"))

mux_ntc_out_y = MUX_NTC_Y + MUX_NTC_H / 2
dsm_in_y = DSM_Y + DSM_H / 2
elements.append(line(MUX_NTC_X + MUX_NTC_W, mux_ntc_out_y,
                     [(0, 0), (DSM_X - (MUX_NTC_X + MUX_NTC_W), dsm_in_y - mux_ntc_out_y)],
                     stroke=COLORS["ai_stroke"], stroke_width=2))


# ====== Internal SPMI Master / Digital block ======
DIG_X, DIG_Y, DIG_W, DIG_H = 1050, M_Y + 230, 380, 300
elements.append(rect(DIG_X, DIG_Y, DIG_W, DIG_H,
                     fill=COLORS["inactive_fill"],
                     stroke=COLORS["inactive_stroke"], stroke_width=2))
elements.append(text(DIG_X + 14, DIG_Y + 14, DIG_W - 28, 26,
                     "SPMI Master  /  Digital Core",
                     color=COLORS["inactive_stroke"], size=16, align="center",
                     valign="top"))
elements.append(text(DIG_X + 14, DIG_Y + 50, DIG_W - 28, 22,
                     "ADC sample buffer • register map • SPMI Tx/Rx",
                     color=COLORS["body"], size=11, align="center", valign="top"))

# SAR ADC -> Digital
sar_out_x = SAR_X + SAR_W
sar_out_y = SAR_Y + SAR_H / 2
elements.append(arrow(sar_out_x, sar_out_y,
                      [(0, 0), (DIG_X - sar_out_x, 0),
                       (DIG_X - sar_out_x, (DIG_Y + 80) - sar_out_y)],
                      stroke=COLORS["primary_stroke"], stroke_width=2))
elements.append(text(sar_out_x + 12, sar_out_y - 24, 110, 18,
                     "12-bit data", color=COLORS["body"], size=11, align="left",
                     valign="top"))

# DSM ADC -> Digital
dsm_out_x = DSM_X + DSM_W
dsm_out_y = DSM_Y + DSM_H / 2
elements.append(arrow(dsm_out_x, dsm_out_y,
                      [(0, 0), (DIG_X - dsm_out_x, 0),
                       (DIG_X - dsm_out_x, (DIG_Y + DIG_H - 80) - dsm_out_y)],
                      stroke=COLORS["ai_stroke"], stroke_width=2))
elements.append(text(dsm_out_x + 12, dsm_out_y + 8, 110, 18,
                     "16-bit data", color=COLORS["body"], size=11, align="left",
                     valign="top"))


# ====== SPMI output pin (right side of Main chip) ======
SPMI_PIN_X = M_X + M_W
SPMI_PIN_Y = M_Y + M_H / 2 - 6
# arrow from digital block to right edge
elements.append(arrow(DIG_X + DIG_W, DIG_Y + DIG_H / 2,
                      [(0, 0), (SPMI_PIN_X - (DIG_X + DIG_W) + 60, 0)],
                      stroke=COLORS["success_stroke"], stroke_width=3))
elements.append(text(SPMI_PIN_X - 80, SPMI_PIN_Y - 28, 140, 22,
                     "SPMI Bus",
                     color=COLORS["success_stroke"], size=14, align="center",
                     valign="top"))


# ====== Vref distribution into Main chip ======
# External Vref center at (VREF_X + VREF_W/2, VREF_Y + VREF_H)
vref_src_x = VREF_X + VREF_W / 2
vref_src_y = VREF_Y + VREF_H

# trunk going down to a horizontal bus at y = main_top - 18
TRUNK_Y = M_Y - 18
elements.append(line(vref_src_x, vref_src_y,
                     [(0, 0), (0, TRUNK_Y - vref_src_y)],
                     stroke=COLORS["trigger_stroke"], stroke_width=2))

# Horizontal bus across the width above all chips (Main + Subs)
BUS_LEFT = 200
BUS_RIGHT = 2300
elements.append(line(BUS_LEFT, TRUNK_Y,
                     [(0, 0), (BUS_RIGHT - BUS_LEFT, 0)],
                     stroke=COLORS["trigger_stroke"], stroke_width=2,
                     stroke_style="dashed"))
elements.append(text(BUS_LEFT + 20, TRUNK_Y - 22, 200, 18,
                     "Vref distribution bus",
                     color=COLORS["trigger_stroke"], size=12, align="left",
                     valign="top"))

# Vref drop into Main chip (entering between title bar and content row, so it
# does not visually cut through the "MAIN PMIC" title)
main_vref_x = SAR_X + SAR_W / 2 + 80   # chosen between SAR and digital
# vertical drop stops at top of chip outline (M_Y), then a small label,
# then continues *below* the title bar (M_Y + 38)
elements.append(line(main_vref_x, TRUNK_Y,
                     [(0, 0), (0, M_Y - TRUNK_Y)],
                     stroke=COLORS["trigger_stroke"], stroke_width=2))
# small "Vref-in" pin marker at chip boundary
elements.append(line(main_vref_x, M_Y + 38,
                     [(0, 0), (0, (M_Y + 70) - (M_Y + 38))],
                     stroke=COLORS["trigger_stroke"], stroke_width=2))
# small "Vref" pin label entering the chip
elements.append(text(main_vref_x + 6, TRUNK_Y + 4, 60, 18, "Vref",
                     color=COLORS["trigger_stroke"], size=12, align="left",
                     valign="top"))

# Internal Vref split: from (main_vref_x, M_Y+70) -> SAR ADC top, DSM ADC top
internal_split_y = M_Y + 70
elements.append(line(main_vref_x, internal_split_y,
                     [(0, 0), (0, 24)],
                     stroke=COLORS["trigger_stroke"], stroke_width=1,
                     stroke_style="dashed"))
elements.append(line(SAR_X + SAR_W * 0.5, internal_split_y + 24,
                     [(0, 0), ((main_vref_x) - (SAR_X + SAR_W * 0.5), 0)],
                     stroke=COLORS["trigger_stroke"], stroke_width=1,
                     stroke_style="dashed"))
elements.append(line(SAR_X + SAR_W * 0.5, internal_split_y + 24,
                     [(0, 0), (0, (SAR_Y) - (internal_split_y + 24))],
                     stroke=COLORS["trigger_stroke"], stroke_width=1,
                     stroke_style="dashed"))
# DSM Vref drop from the same horizontal stub
elements.append(line(DSM_X + DSM_W * 0.5, internal_split_y + 24,
                     [(0, 0), ((main_vref_x) - (DSM_X + DSM_W * 0.5), 0)],
                     stroke=COLORS["trigger_stroke"], stroke_width=1,
                     stroke_style="dashed"))
elements.append(line(DSM_X + DSM_W * 0.5, internal_split_y + 24,
                     [(0, 0), (0, (DSM_Y) - (internal_split_y + 24))],
                     stroke=COLORS["trigger_stroke"], stroke_width=1,
                     stroke_style="dashed"))


# ====== SUB-PMICs (5) ======
SUB_Y = 950
SUB_W = 420
SUB_H = 470
SUB_GAP = 40
SUB_X_START = 80

# SPMI bus from main right side -> down -> across to all subs
# Main SPMI exit at (M_X + M_W + 60, SPMI_PIN_Y) approximately
spmi_exit_x = M_X + M_W + 60
spmi_exit_y = DIG_Y + DIG_H / 2
spmi_bus_y = SUB_Y - 60
spmi_bus_left = SUB_X_START + 60

# Down from main chip exit to bus
elements.append(line(spmi_exit_x, spmi_exit_y,
                     [(0, 0), (0, spmi_bus_y - spmi_exit_y)],
                     stroke=COLORS["success_stroke"], stroke_width=3))
# Horizontal bus across all subs
elements.append(line(spmi_bus_left, spmi_bus_y,
                     [(0, 0), (spmi_exit_x - spmi_bus_left, 0)],
                     stroke=COLORS["success_stroke"], stroke_width=3))
elements.append(text(spmi_bus_left + 8, spmi_bus_y - 24, 200, 20,
                     "SPMI Bus  (Main ↔ Subs)",
                     color=COLORS["success_stroke"], size=13, align="left",
                     valign="top"))


def build_sub(idx, x, y, w, h):
    """Build a single Sub-PMIC chip. idx is 1-based."""
    out = []
    # Chip outline
    out.append(rect(x, y, w, h,
                    fill="transparent",
                    stroke=COLORS["primary_stroke"], stroke_width=2))
    # Title bar
    out.append(rect(x, y, w, 32,
                    fill=COLORS["secondary_fill"],
                    stroke=COLORS["primary_stroke"], stroke_width=2,
                    rounded=False))
    out.append(text(x + 12, y + 5, 200, 22, f"SUB-PMIC  #{idx}",
                    color="#ffffff", size=15, align="left", valign="top"))
    out.append(text(x + w - 132, y + 7, 120, 20, "1 × SAR ADC",
                    color="#ffffff", size=11, align="right", valign="top"))

    # Input channels area (left): 16 channels shown as 3 + ... + 1
    ch_x = x + 14
    ch_x_end = x + 150
    ch_top = y + 80
    gap = 22
    rows_top = [("CH 1", ch_top), ("CH 2", ch_top + gap), ("CH 3", ch_top + 2 * gap)]
    dot_y = ch_top + 3 * gap + 2
    last_y = ch_top + 5 * gap + 4
    rows_bot = [("CH 16", last_y)]

    out.append(text(ch_x, ch_top - 26, 200, 18, "16 inputs",
                    color=COLORS["title"], size=12, align="left", valign="top"))

    for label, ly in rows_top:
        out.append(text(ch_x, ly - 9, 50, 18, label,
                        color=COLORS["on_light"], size=11, align="left",
                        valign="top"))
        out.append(line(ch_x + 50, ly,
                        [(0, 0), (ch_x_end - (ch_x + 50), 0)],
                        stroke=COLORS["body"], stroke_width=1))

    out.append(text(ch_x, dot_y - 4, 60, 28, "⋮",
                    color=COLORS["body"], size=20, align="left", valign="top"))
    out.append(text(ch_x + 80, dot_y - 4, 60, 28, "⋯",
                    color=COLORS["body"], size=18, align="left", valign="top"))

    for label, ly in rows_bot:
        out.append(text(ch_x, ly - 9, 50, 18, label,
                        color=COLORS["on_light"], size=11, align="left",
                        valign="top"))
        out.append(line(ch_x + 50, ly,
                        [(0, 0), (ch_x_end - (ch_x + 50), 0)],
                        stroke=COLORS["body"], stroke_width=1))

    # MUX 16:1
    mux_x, mux_w, mux_h = ch_x_end + 6, 80, 170
    mux_y = ch_top - 14
    out.append(trapezoid(mux_x, mux_y, mux_w, mux_h,
                         fill=COLORS["tertiary_fill"],
                         stroke=COLORS["primary_stroke"]))
    out.append(text(mux_x, mux_y + mux_h/2 - 22, mux_w, 20,
                    "MUX",
                    color=COLORS["primary_stroke"], size=13, align="center",
                    valign="top"))
    out.append(text(mux_x, mux_y + mux_h/2, mux_w, 20,
                    "16 : 1",
                    color=COLORS["primary_stroke"], size=12, align="center",
                    valign="top"))

    # SAR ADC (sub)
    sar_x = mux_x + mux_w + 30
    sar_w = 160
    sar_h = 130
    sar_y = mux_y + 16
    out.append(trapezoid(sar_x, sar_y, sar_w, sar_h,
                         fill=COLORS["secondary_fill"],
                         stroke=COLORS["primary_stroke"]))
    out.append(text(sar_x, sar_y + sar_h/2 - 22, sar_w, 22,
                    "SAR ADC",
                    color=COLORS["primary_stroke"], size=14, align="center",
                    valign="top"))
    out.append(text(sar_x, sar_y + sar_h/2 + 4, sar_w, 18,
                    f"Sub #{idx}",
                    color=COLORS["primary_stroke"], size=11, align="center",
                    valign="top"))

    # MUX -> SAR connection
    mux_out_y = mux_y + mux_h / 2
    sar_in_y = sar_y + sar_h / 2
    out.append(line(mux_x + mux_w, mux_out_y,
                    [(0, 0), (sar_x - (mux_x + mux_w), sar_in_y - mux_out_y)],
                    stroke=COLORS["primary_stroke"], stroke_width=2))

    # SPMI input from top (entering chip)
    spmi_in_x = x + w * 0.30
    out.append(arrow(spmi_in_x, y - 36,
                     [(0, 0), (0, 36)],
                     stroke=COLORS["success_stroke"], stroke_width=2))
    out.append(text(spmi_in_x + 8, y - 32, 60, 18, "SPMI",
                    color=COLORS["success_stroke"], size=11, align="left",
                    valign="top"))

    # Vref drop into chip (from top global bus)
    vref_in_x = x + w * 0.72
    # tap line from global bus down to sub top
    out.append(line(vref_in_x, TRUNK_Y,
                    [(0, 0), (0, y - TRUNK_Y)],
                    stroke=COLORS["trigger_stroke"], stroke_width=2))
    out.append(text(vref_in_x + 6, y - 18, 60, 18, "Vref",
                    color=COLORS["trigger_stroke"], size=11, align="left",
                    valign="top"))
    # internal Vref into ADC top
    out.append(line(vref_in_x, y + 32,
                    [(0, 0), (0, (sar_y) - (y + 32) - 4)],
                    stroke=COLORS["trigger_stroke"], stroke_width=1,
                    stroke_style="dashed"))
    # horizontal stub to top-mid of SAR
    out.append(line(sar_x + sar_w * 0.5, sar_y - 4,
                    [(0, 0), (vref_in_x - (sar_x + sar_w * 0.5), 0)],
                    stroke=COLORS["trigger_stroke"], stroke_width=1,
                    stroke_style="dashed"))

    # SPMI bus tap from spmi_bus_y down into sub at spmi_in_x
    out.append(line(spmi_in_x, spmi_bus_y,
                    [(0, 0), (0, (y - 36) - spmi_bus_y)],
                    stroke=COLORS["success_stroke"], stroke_width=2))

    return out


for i in range(5):
    sx = SUB_X_START + i * (SUB_W + SUB_GAP)
    elements.extend(build_sub(i + 1, sx, SUB_Y, SUB_W, SUB_H))


# ====== Legend (bottom-left) ======
LEG_X, LEG_Y = 80, 1470
elements.append(text(LEG_X, LEG_Y, 200, 22, "Legend",
                     color=COLORS["title"], size=15, align="left", valign="top"))
legend_items = [
    ("Trapezoid block  =  ADC / MUX", COLORS["secondary_fill"], COLORS["primary_stroke"]),
    ("Solid line  =  signal path", None, COLORS["body"]),
    ("Dashed orange  =  Vref distribution", None, COLORS["trigger_stroke"]),
    ("Solid green  =  SPMI bus", None, COLORS["success_stroke"]),
    ("⋮  ⋯  =  more channels (omitted)", None, COLORS["body"]),
]
for i, (label, fill, stroke) in enumerate(legend_items):
    yy = LEG_Y + 30 + i * 22
    if fill:
        elements.append(rect(LEG_X, yy, 24, 14, fill=fill, stroke=stroke,
                              stroke_width=1, rounded=False))
    else:
        elements.append(line(LEG_X, yy + 7, [(0, 0), (24, 0)],
                             stroke=stroke, stroke_width=2,
                             stroke_style=("dashed" if "Dashed" in label else "solid")))
    elements.append(text(LEG_X + 32, yy - 2, 400, 20, label,
                         color=COLORS["on_light"], size=12, align="left",
                         valign="top"))


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "viewBackgroundColor": "#ffffff",
        "gridSize": 20,
    },
    "files": {},
}

import os
out_path = os.path.join(os.path.dirname(__file__), "..", "pmic-system.excalidraw")
out_path = os.path.abspath(out_path)
with open(out_path, "w") as f:
    json.dump(doc, f, indent=2)
print(f"Wrote {len(elements)} elements to {out_path}")
