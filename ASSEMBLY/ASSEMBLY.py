from build123d import *
import math
try:
    from ocp_vscode import show
except ImportError:
    show = None

# =============================================================================
# 1. GENERATE CASE TOP (FULL DETAIL)
# =============================================================================
with BuildPart() as top_body:
    # --- 1. Dimensions ---
    length, width, height = 12.9, 30.8, 51.6
    wall_thickness = 2.0

    # A. Base Solid
    Box(length, width, height)
    
    # B. Styling Fillet (Top X-axis edges)
    styling_r = 6.4 
    x_edges = edges().filter_by(Axis.X)
    top_x_edges = x_edges.group_by(Axis.Z)[-1]
    fillet(top_x_edges, radius=styling_r)
    
    # C. Shelling
    yz_face_opening = faces().filter_by(Axis.X).sort_by(Axis.X)[0]
    bottom_face_opening = faces().filter_by(Axis.Z).sort_by(Axis.Z)[0]
    offset(amount=-wall_thickness, openings=[yz_face_opening, bottom_face_opening])
    
    # --- 3. Internal Side Wall Extrusions (Lips) ---
    rect_w, rect_l = 2.0, 11.5
    rect_y = -13.4 + 2.4 + (rect_w / 2)
    rect_z = 23.8 - 5.9 - (rect_l / 2)
    inner_wall_plane = Plane.YZ.offset(4.45)
    with BuildSketch(inner_wall_plane):
        with Locations((rect_y, rect_z), (-rect_y, rect_z)):
            Rectangle(rect_w, rect_l)
    extrude(amount=-3.8)

    # --- 4. Base Features & Vertical Slots ---
    bottom_plane = Plane.XY.offset(-height / 2)
    with BuildSketch(bottom_plane):
        with Locations((-length / 2, 0)):
            Rectangle(10.9, 26.8, align=(Align.MIN, Align.CENTER))
    extrude(amount=8.2)
    
    front_yz_plane = Plane.YZ.offset(-length / 2) 
    with BuildSketch(front_yz_plane):
        with Locations((0, -height / 2)):
            Rectangle(26.8, 8.2, align=(Align.CENTER, Align.MIN))
        with Locations((-13.4, -25.8)):
            Rectangle(2.4, 8.2, align=(Align.MIN, Align.MIN))
        with Locations((13.4, -25.8)):
            Rectangle(2.4, 8.2, align=(Align.MAX, Align.MIN))
    extrude(amount=9.7, mode=Mode.SUBTRACT)

    # Vertical Corner Slots
    with BuildSketch(front_yz_plane):
        for z_offset in [6.05, 6.05 + 22.1]:
            with Locations((-width / 2, -height / 2 + z_offset)):
                Rectangle(1, 10, align=(Align.MIN, Align.MIN))
    extrude(amount=4.5, mode=Mode.SUBTRACT)

    # --- 4.5. Right View Cutout & Chamfer Softening ---
    right_yz_plane = Plane.YZ.offset(length / 2)
    with BuildSketch(right_yz_plane):
        with Locations((-12.34, 21.0)):
            Rectangle(4.6, 3.11, align=(Align.MIN, Align.MAX))
    extrude(amount=-wall_thickness, mode=Mode.SUBTRACT)

    cutout_outer_edges = edges().filter_by(lambda e: 
        math.isclose(e.center().X, length/2, abs_tol=1e-3) and
        -12.5 < e.center().Y < -7.5 and 17.5 < e.center().Z < 21.5
    )
    if cutout_outer_edges:
        chamfer(cutout_outer_edges, length=1.5)

    chamfer_edges = edges().filter_by(lambda e: 
        4.9 <= e.center().X <= 6.5 and
        -13.0 < e.center().Y < -7.0 and 
        17.0 < e.center().Z < 22.0
    )
    if chamfer_edges:
        fillet(chamfer_edges, radius=0.2)

    # --- 5. Internal Vertical Rib ---
    inner_edge_x = 4.45
    with BuildSketch(bottom_plane):
        with Locations((inner_edge_x, 0)):
            Rectangle(3.8, 22.0, align=(Align.MAX, Align.CENTER))
    extrude(amount=8.2)

    # --- 6. Vertical Triangular Notches ---
    tri_base, tri_side = 1.57, 1.11
    tri_height = math.sqrt(tri_side**2 - (tri_base/2)**2)
    pos_x, pos_y_abs = -6.45 + 3.12, 13.4
    z_original, z_copy = -25.8 + 6.85 + 22.1, (-25.8 + 6.85 + 22.1) - 22.5
    
    for z_pos in [z_original, z_copy]:
        with BuildSketch(Plane.XY.offset(z_pos)):
            with Locations((pos_x, pos_y_abs)):
                Polygon([(0, 0), (tri_base, 0), (tri_base / 2, tri_height)], align=(Align.MIN, Align.MIN))
            with Locations((pos_x, -pos_y_abs)):
                Polygon([(0, 0), (tri_base, 0), (tri_base / 2, -tri_height)], align=(Align.MIN, Align.MAX))
        extrude(amount=8.4, mode=Mode.SUBTRACT)

    # --- 7. Final Finishing Fillets ---
    bottom_outer = edges().filter_by(lambda e: math.isclose(e.center().Z, -height/2, abs_tol=0.2))
    bottom_outer = bottom_outer.filter_by(
        lambda e: (math.isclose(e.center().X, length/2, abs_tol=0.5) or 
                   math.isclose(abs(e.center().Y), width/2, abs_tol=0.5)) 
                   and e.center().X > (-length/2 + 0.1)
    )
    if bottom_outer:
        fillet(bottom_outer, radius=0.9)

    vertical_corners = edges().filter_by(Axis.Z).filter_by(
        lambda e: math.isclose(e.center().X, length/2, abs_tol=0.2) and 
                  math.isclose(abs(e.center().Y), width/2, abs_tol=0.2)
    ).filter_by(lambda e: e.center().Z > -height/2 + 1.0)
    if vertical_corners:
        fillet(vertical_corners, radius=0.5)

# =============================================================================
# 2. GENERATE CASE BOTTOM (FULL DETAIL)
# =============================================================================
with BuildPart() as bottom_body:
    # --- Configuration ---
    BASE_L, BASE_W, BASE_H = 30.8, 51.6, 2.0
    CUB_L, CUB_W, CUB_H = 26.4, 49.4, 8.6
    CUB_SHIFT_X, CUB_FILLET_R, BASE_FILLET_R = 2.0, 5.2, 7.4
    CENTER_X = CUB_SHIFT_X + (CUB_L / 2)
    TOP_Z = BASE_H + CUB_H

    # A. MAIN ADDITIVE STRUCTURE
    Box(BASE_L, BASE_W, BASE_H, align=(Align.MIN, Align.MIN, Align.MIN))
    with Locations(Location((CUB_SHIFT_X, 0.0, BASE_H))):
        Box(CUB_L, CUB_W, CUB_H, align=(Align.MIN, Align.MIN, Align.MIN))

    # B. VERTICAL CORNER FILLETS
    upper_edges = bottom_body.edges().filter_by(Axis.Z).filter_by(lambda e: e.center().Z > BASE_H).sort_by(Axis.Y)[-2:]
    fillet(upper_edges, radius=CUB_FILLET_R)
    lower_edges = bottom_body.edges().filter_by(Axis.Z).filter_by(lambda e: e.center().Z < BASE_H).sort_by(Axis.Y)[-2:]
    fillet(lower_edges, radius=BASE_FILLET_R)

    # C. SUBTRACTIVE VOIDS
    with Locations(Location((4.0, 8.2, BASE_H))):
        Box(22.4, 30.0, 8.6, align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
    with Locations(Location((4.0, 38.2, BASE_H))):
        Box(22.4, 6.0, 8.6, align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
    with Locations(Location((4.0, 0.0, TOP_Z - 3.3))):
        Box(22.4, 8.2, 3.3, align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)
    with Locations(Location((CENTER_X - 4.5, 3.2, 2.0))):
        Box(9.0, 5.0, 5.3, align=(Align.MIN, Align.MIN, Align.MIN), mode=Mode.SUBTRACT)

    with BuildPart(mode=Mode.PRIVATE) as rear_profile:
        with Locations(Location((4.0, 44.2, TOP_Z - 3.3))):
            Box(22.4, 3.2, 3.3, align=(Align.MIN, Align.MIN, Align.MIN))
            fillet(rear_profile.edges().filter_by(Axis.Z).sort_by(Axis.Y)[-2:], radius=3.19)
    add(rear_profile, mode=Mode.SUBTRACT)

    # D. ADDITIVE FEATURES
    with Locations(Location((8.4, 6.2, 8.1)), Location((22.0, 6.2, 8.1))):
        Cylinder(radius=2.43/2, height=1.6, align=(Align.CENTER, Align.CENTER, Align.CENTER))

    # Notches
    with BuildPart(mode=Mode.PRIVATE) as ext_notches:
        for y_pos in [-15.05, -37.15]:
            with BuildSketch(Plane.XZ.offset(y_pos)):
                with Locations(Location((2.0, 6.8)) * Rot(0, 0, 180)):
                    Polygon([(0, 0), (0, 1.4), (0.7, 0.7)])
            extrude(amount=8.0)
        mirror(about=Plane.YZ.offset(CENTER_X))
    add(ext_notches, mode=Mode.ADD)

    with BuildPart(mode=Mode.PRIVATE) as int_notches:
        with BuildSketch(Plane.XZ.offset(-27.1)):
            with Locations(Location((4.0, 9.1))):
                Polygon([(0, 0), (0, 1.0), (0.5, 0.5)])
        extrude(amount=10.0)
        mirror(about=Plane.YZ.offset(CENTER_X))
    add(int_notches, mode=Mode.ADD)

# =============================================================================
# 3. ALIGNMENT & MATING
# =============================================================================

# Orientation: Rotated 180 around Y axis
case_top = top_body.part.rotate(Axis.Y, 90).rotate(Axis.Z, 90).rotate(Axis.Y, 180)

# Move: Original(17.05) - Move1(15.05) - Move2(8.55) = -6.55
case_top.move(Location((15.4, 25.8, -6.55))) 

# Optional: Exploded view
exploded_top = case_top.moved(Location((0, 0, 15)))

# =============================================================================
# 4. VIEW
# =============================================================================
if show:
    show(bottom_body.part, exploded_top, names=["Bottom Part", "Top Part (Exploded)"])