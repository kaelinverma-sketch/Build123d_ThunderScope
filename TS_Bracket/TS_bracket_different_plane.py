import os
from build123d import *

# ── 1. Base Bracket (Modified Tab Length & Slot Removed) ────────────────────
with BuildPart() as bracket_3d:
    with BuildSketch() as bracket_sketch:
        with BuildLine() as outline:
            p_start = (1.0, 0.0)
            CenterArc(center=(1.0, 1.1), radius=1.1, start_angle=270, arc_size=90)
            Line((2.1, 1.1), (2.1, 7.7))
            CenterArc(center=(2.7, 7.7), radius=0.6, start_angle=180, arc_size=-180)
            Line((3.3, 7.7), (3.3, 6.1))
            Line((3.3, 6.1), (9.4, 6.1))
            Line((9.4, 6.1), (9.4, 7.7))
            CenterArc(center=(10.0, 7.7), radius=0.6, start_angle=180, arc_size=-180)
            Line((10.6, 7.7), (10.6, 4.5)) 
            CenterArc(center=(11.9, 4.5), radius=1.3, start_angle=180, arc_size=90)
            Line((11.9, 3.2), (108.7, 3.2))
            Line((108.7, 3.2), (112.8, 7.3))
            
            # --- MODIFIED TAB SECTION (Length = 7.25mm) ---
            # X target: 112.8 + 7.25 = 120.05
            Line((112.8, 7.3), (120.05, 7.3))   
            Line((120.05, 7.3), (120.05, 17.5)) 
            Line((120.05, 17.5), (112.8, 17.5)) 
            # ----------------------------------------------

            Line((112.8, 17.5), (108.7, 21.6))
            Line((108.7, 21.6), (6.5, 21.6))
            Line((6.5, 21.6), (3.9, 19.1))
            Line((3.9, 19.1), (1.0, 19.1))
            Line((1.0, 19.1), (0.0, 19.1))
            Line((0.0, 19.1), (0.0, 0.0))
            Line((0.0, 0.0), p_start)
        make_face()
        
        # Subtractions (Circular holes only)
        with Locations([(24.7, 13.4), (46.3, 13.4), (68.0, 13.4), (89.6, 13.4)]):
            Circle(radius=5.1, mode=Mode.SUBTRACT)
        with Locations([(12.3, 13.4), (12.3, 10.9), (57.2, 10.1)]):
            Circle(radius=0.8, mode=Mode.SUBTRACT)
        with Locations([(107.0, 12.4)]):
            Circle(radius=2.4, mode=Mode.SUBTRACT)
        
        # Slot at (118.1, 12.4) removed as requested.
        
    extrude(amount=0.787)

# ── 2. Side Piece (TS_bracket_2) ─────────────────────────────────────────────
with BuildPart() as side_piece_left_3d:
    left_plane = Plane(origin=(0, 0, 0.787), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    with BuildSketch(left_plane) as side_sketch:
        with BuildLine() as side_outline:
            Line((0.0,  0.0), (19.1, 0.0))
            Line((19.1, 0.0), (19.0, 8.5))
            CenterArc(center=(17.1, 8.5), radius=1.9, start_angle=0, arc_size=90)
            Line((17.1, 10.4), (13.1, 10.4))
            Line((13.1, 10.4), (13.1, 6.2))
            Line((13.1, 6.2), (10.7, 6.2))
            Line((10.7, 6.2), (10.7, 10.4))
            Line((10.7, 10.4), (1.9, 10.4))
            CenterArc(center=(1.9, 8.5), radius=1.9, start_angle=90, arc_size=90)
            Line((0.0, 8.5), (0.0, 6.3))
            Line((0.0, 6.3), (3.2, 6.3))
            CenterArc(center=(3.2, 4.1), radius=2.2, start_angle=90, arc_size=-180)
            Line((3.2, 1.9), (0.0, 1.9))
            Line((0.0, 1.9), (0.0, 0.0))
        make_face()
    extrude(amount=0.787)

# ── 3. Target Edge Side Piece & Concentric Cylinder (TS_bracket_3) ──────────
with BuildPart() as side_tab_in_notch_3d:
    edge_plane = Plane(origin=(10.6-7.3, 19.148-13.048, 0), x_dir=(1, 0, 0), z_dir=(0, 1, 0))
    with BuildSketch(edge_plane):
        with BuildLine():
            l1 = Line((0.0, 0.0), (6.096, 0.0))
            l2 = Line(l1 @ 1, (6.096, 7.0104))
            a1 = CenterArc(center=(4.826, 7.0104), radius=1.27, start_angle=0, arc_size=90)
            l3 = Line(a1 @ 1, (1.27, 8.2804))
            a2 = CenterArc(center=(1.27, 7.0104), radius=1.27, start_angle=90, arc_size=90)
            l4 = Line(a2 @ 1, (0.0, 0.0))
        make_face()
        with Locations([(3.048, 5.2832)]):
            Circle(radius=3.175/2, mode=Mode.SUBTRACT)
    extrude(amount=0.787)

    with BuildPart(edge_plane):
        with Locations([(3.048, 5.2832)]):
            Cylinder(radius=3.886/2, height=1.118+0.787, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(radius=3.175/2, height=1.118+0.787, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

# ── 4. Final Combination ───────────────────────────────────────────────────
final_body = bracket_3d.part + side_piece_left_3d.part + side_tab_in_notch_3d.part

# ── 5. EXPORT AND SHOW ──────────────────────────────────────────────────────
try:
    from ocp_vscode import show
    show(final_body, names=["ThunderScope Bracket"])
except ImportError:
    pass

export_step(final_body, "TS_Bracket_NoSlot.step")

# --- 1. Load the Original Model ---
original_path = "/Users/softage/ThunderScope/Original models/TS PCIe Bracket.step"

if os.path.exists(original_path):
    original_part = import_step(original_path)
    # The original file might be a single part or a compound
    vol_original = sum(s.volume for s in original_part.solids())
else:
    vol_original = 0.0
    print(f"Warning: File not found at {original_path}")

# --- 2. Calculate Volume of Your New Model ---
# final_body is the Compound created in the previous step
vol_new = sum(s.volume for s in final_body.solids())

# --- 3. Comparison and Output ---
diff = vol_new - vol_original

print("--- Volumetric Comparison ---")
print(f"Original Model Volume: {vol_original:,.3f} mm³")
print(f"New Model Volume:      {vol_new:,.3f} mm³")
print(f"Volumetric Difference: {diff:,.3f} mm³")

if vol_original > 0:
    percent_change = (diff / vol_original) * 100
    print(f"Percentage Change:     {percent_change:+.2f}%")