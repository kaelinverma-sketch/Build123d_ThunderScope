from build123d import *

# --- Build the Front Endcap Part ---
with BuildPart() as front_endcap_part:
    with BuildSketch() as front_sketch:
        # 1. Outer Perimeter (103 x 30.5)
        with BuildLine() as outline:
            p1, p2, p3, p4 = (-103.0, 0.0), (0.0, 0.0), (0.0, -30.5), (-103.0, -30.5)
            Polyline(p1, p2, p3, p4, close=True)
            fillet(outline.vertices(), radius=4.0)
        make_face()

        # 2. Corner Mounting Holes (R=2.1)
        with Locations((-4.0, -4.0), (-99.0, -4.0), (-4.0, -26.5), (-99.0, -26.5)):
            Circle(radius=2.1, mode=Mode.SUBTRACT)

        # 3. Four Collinear Notched Holes (Y = -10.455)
        y_bnc = -10.455
        x_bnc_locations = [-20.6, -40.6, -62.4, -82.4]

        for x_loc in x_bnc_locations:
            with Locations((x_loc, y_bnc)):
                Circle(radius=5.1, mode=Mode.SUBTRACT)
                with Locations((0, 5.1), (0, -5.1)):
                    Rectangle(3.0, 1.5, mode=Mode.SUBTRACT)

        # 4. Three Rectangular Slots at the Top (5.0x2.5)
        y_top_slot_center = -3.99
        slot_x_positions = [
            (x_bnc_locations[0] + x_bnc_locations[1]) / 2,
            (x_bnc_locations[1] + x_bnc_locations[2]) / 2,
            (x_bnc_locations[2] + x_bnc_locations[3]) / 2
        ]
        with Locations(*[(x, y_top_slot_center) for x in slot_x_positions]):
            Rectangle(5.0, 2.5, mode=Mode.SUBTRACT)

        # 5. Bottom Horizontal Slots (12x3, 2.74mm from bottom)
        # Slot 1 Left Edge 36.675 -> Center -64.825 (if 3 wide)
        # Correcting for 12.0 width: Left Edge -103 + 36.675 = -66.325. Center = -66.325 + 6.0 = -60.325
        x_horiz_positions = [-60.325, -39.675]
        y_bottom_slot_center = -26.26 # (-30.5 + 2.74 + 1.5)
        with Locations(*[(x, y_bottom_slot_center) for x in x_horiz_positions]):
            Rectangle(12.0, 3.0, mode=Mode.SUBTRACT)

        # 6. Three Alignment Holes (Radius 1.3mm)
        # Positioned based on previous drawings: (-77.6, -9.1), (-77.6, -25.3), (-93.8, -9.1)
        with Locations((-77.6, -9.1), (-77.6, -25.3), (-93.8, -9.1)):
            Circle(radius=1.3, mode=Mode.SUBTRACT)

    # --- Extrude to 1.51mm depth ---
    extrude(amount=1.51)

# --- Metadata & Export ---
print(f"Front Endcap Volume: {front_endcap_part.part.volume:.3f} mm³")
export_step(front_endcap_part.part, "Generated_TS_Front_Endcap_3D.step")

try:
    from ocp_vscode import show_object
    show_object(front_endcap_part.part, name="TS_Front_Endcap_Final")
except ImportError:
    pass
