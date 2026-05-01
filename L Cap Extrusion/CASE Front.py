from build123d import *
from ocp_vscode import show

# ==========================================
# DIMENSIONS & CONSTANTS
# ==========================================
BOX1_WIDTH, BOX1_HEIGHT = 1.5, 3.8
BOX2_WIDTH, BOX2_HEIGHT = 2.72, 1.5
PLATE_THICKNESS, PLATE_HEIGHT = 1.65, 84.3
CYL_RADIUS = 1.27 / 2  # 0.635mm
EXTRUDE_LENGTH = -120

# Fillet Radii
STANDARD_FILLET = 0.5
SPECIAL_FILLET = 1.0  # New 1mm fillet for Box 1 corner

# Vertical Positioning Logic
BOTTOM_JUNCTION_Z = 3.8
TOTAL_TOP_Z = BOTTOM_JUNCTION_Z + PLATE_HEIGHT  # 88.1mm
MIRROR_Z_CENTER = (BOTTOM_JUNCTION_Z + TOTAL_TOP_Z) / 2  # 45.95mm

# Edge Target Coordinates
BOX1_CORNER_Z_BOTTOM = 3.8
BOX1_CORNER_Z_TOP = 88.1 # Mirrored Z for the top corner
CUT1_XZ = (-2.72, 2.3)
CUT2_XZ = (-2.72, 89.6)

with BuildPart() as mbs_assembly:
    # --- 1. BUILD BOTTOM CLUSTER (WITH CUT) ---
    with BuildPart() as bottom_boxes:
        with BuildSketch(Plane.XZ) as s1:
            Rectangle(BOX1_WIDTH, BOX1_HEIGHT, align=(Align.MIN, Align.MIN))
        extrude(amount=EXTRUDE_LENGTH)
        
        with BuildSketch(Plane.XZ * Location((0, BOTTOM_JUNCTION_Z, 0))) as s2:
            Rectangle(BOX2_WIDTH, BOX2_HEIGHT, align=(Align.MAX, Align.MAX))
        extrude(amount=EXTRUDE_LENGTH)

        with BuildSketch(Plane.XZ * Location(CUT1_XZ)) as cut_sketch:
            Circle(CYL_RADIUS)
        extrude(amount=EXTRUDE_LENGTH, mode=Mode.SUBTRACT)

    add(bottom_boxes.part)

    # --- 2. BUILD CENTRAL PLATE ---
    with BuildSketch(Plane.XZ * Location((-BOX2_WIDTH, BOTTOM_JUNCTION_Z, 0))) as s3:
        Rectangle(PLATE_THICKNESS, PLATE_HEIGHT, align=(Align.MIN, Align.MIN))
    extrude(amount=EXTRUDE_LENGTH)

    # --- 3. APPLY HEIGHT MIRROR ---
    mirror_plane = Plane.XY.offset(MIRROR_Z_CENTER)
    mirror(objects=bottom_boxes.part, about=mirror_plane)

    # --- 4. SELECTIVE FILLETS ---
    all_y_edges = mbs_assembly.edges().filter_by(Axis.Y)
    
    # Selection A: The specific Box 1 corner(s) for the 1.0mm fillet
    # Includes both the bottom (3.8) and mirrored top (88.1) for symmetry
    box1_corner_edges = all_y_edges.filter_by(
        lambda e: abs(e.center().X - 1.5) < 0.05 and 
                  (abs(e.center().Z - BOX1_CORNER_Z_BOTTOM) < 0.05 or 
                   abs(e.center().Z - BOX1_CORNER_Z_TOP) < 0.05)
    )
    
    # Selection B: The sharp cylindrical cut edges to EXCLUDE from everything
    cut_edges = all_y_edges.filter_by(
        lambda e: (Vector(e.center().X, 0, e.center().Z) - Vector(CUT1_XZ[0], 0, CUT1_XZ[1])).length < (CYL_RADIUS + 0.1) or
                  (Vector(e.center().X, 0, e.center().Z) - Vector(CUT2_XZ[0], 0, CUT2_XZ[1])).length < (CYL_RADIUS + 0.1)
    )

    # Selection C: All other Y-edges for the 0.5mm fillet
    standard_target_edges = all_y_edges - box1_corner_edges - cut_edges

    # Apply the Fillets
    if standard_target_edges:
        fillet(standard_target_edges, radius=STANDARD_FILLET)
    
    if box1_corner_edges:
        fillet(box1_corner_edges, radius=SPECIAL_FILLET)

# ==========================================
# VISUALIZATION
# ==========================================
if __name__ == "__main__":
    show(mbs_assembly, names=["MBS Mixed Fillets"])