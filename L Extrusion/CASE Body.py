from build123d import *
from ocp_vscode import show

# ==========================================
# MASTER DIMENSIONS (MBS)
# ==========================================
height = 120.0
casing_length = 103.0
casing_width = 30.51
wall_thickness = 0.75 # Derived from (30.51 - 29.01) / 2

# Fillet Radii
global_fillet = 0.3 
corner_fillet = 3.0  
inner_corner_fillet = corner_fillet - wall_thickness # Maintains wall thickness

# Side Wall Slot Dimensions
cut_w, cut_d = 1.83, 4.0
cut_x, cut_z = 2.55, 4.77

# Internal Rail Support Dimensions
inner_w, inner_d = 1.5, 2.5
inner_x, inner_z = 9.32, 1.5
separation = 2.0
total_features = 4 

# Rotated Corner Cut Dimensions
rot_cut_w = 6.0    
rot_cut_d = 1.88
pivot_x, pivot_z = 26.51, 4.0

# Edge Groove Array Dimensions
bead_dia = 0.76
bead_radius = bead_dia / 2
bead_start_x = 5.84
bead_z = 0.0
bead_gap = 6.11
total_beads = 4

# Side Wall Groove Dimensions
side_groove_dia = 0.76
side_groove_radius = side_groove_dia / 2
side_groove_x = 30.51
side_groove_z = 6.35

def create_case_body_mbs():
    # 1. CREATE THE ROUNDED SHELL FIRST
    # This prevents the "covered front" and "ruined features" issues
    with BuildPart() as main_shell:
        # Outer Box
        Box(casing_width, height, casing_length, align=(Align.MIN, Align.MIN, Align.MIN))
        # Fillet Outer Corners
        outer_edges = main_shell.edges().filter_by(Axis.Y).sort_by(SortBy.DISTANCE, (casing_width/2, 0, casing_length/2))[-4:]
        fillet(outer_edges, radius=corner_fillet)
        
        # Inner Cutout
        with BuildPart(mode=Mode.SUBTRACT) as inner_cut:
            Box(29.01, height, 100, align=(Align.MIN, Align.MIN, Align.MIN))
            inner_cut.part = inner_cut.part.moved(Pos(wall_thickness, 0, 1.5))
            # Fillet Inner Corners to maintain wall thickness
            inner_edges = inner_cut.edges().filter_by(Axis.Y).sort_by(SortBy.DISTANCE, (casing_width/2, 0, casing_length/2))[-4:]
            fillet(inner_edges, radius=inner_corner_fillet)

    # 2. CREATE THE RIBS (Applied to the rounded shell)
    with BuildPart() as ribs:
        rib_int = Box(7.32, height, 7.79, align=(Align.MIN, Align.MIN, Align.MIN))
        add(rib_int)
        add(mirror(rib_int, about=Plane.XY.offset(casing_length / 2)))
        
        rib_ext = Box(7.19, height, 7.32, align=(Align.MIN, Align.MIN, Align.MIN))
        rib_ext.move(Pos(23.32, 0, 0))
        add(rib_ext)
        add(mirror(rib_ext, about=Plane.XY.offset(casing_length / 2)))

    # 3. INTERNAL RAIL ARRAY
    with BuildPart() as internal_rails:
        with BuildSketch(Plane.XZ):
            for i in range(total_features):
                x_pos = inner_x + i * (inner_w + separation)
                with Locations((x_pos, inner_z)):
                    Rectangle(inner_w, inner_d, align=(Align.MIN, Align.MIN))
        extrude(amount=-height)
        add(mirror(internal_rails.part, about=Plane.XY.offset(casing_length / 2)))

    # 4. SUBTRACTION TOOLS (Slots and Grooves)
    with BuildPart() as tools:
        # Side wall slots
        with BuildSketch(Plane.XZ):
            with Locations((cut_x, cut_z)):
                Rectangle(cut_w, cut_d, align=(Align.MIN, Align.MIN))
        extrude(amount=-height)
        
        # Rotated cuts
        with BuildPart() as rot_tool:
            with BuildSketch(Plane.XZ):
                with Locations((pivot_x, pivot_z - (rot_cut_d / 2))):
                    Rectangle(rot_cut_w, rot_cut_d, align=(Align.MIN, Align.MIN))
            extrude(amount=-height)
            rot_tool.part = rot_tool.part.rotate(Axis((pivot_x, 0, pivot_z), (0, 1, 0)), 225)
        add(rot_tool)

        # Edge beads
        with BuildPart() as beads:
            with BuildSketch(Plane.XZ):
                for i in range(total_beads):
                    x_pos = bead_start_x + i * (bead_dia + bead_gap)
                    with Locations((x_pos, bead_z)):
                        Circle(radius=bead_radius)
            extrude(amount=-height)
        add(beads)
        
        # Side grooves
        with BuildPart() as side_g:
            with BuildSketch(Plane.XZ):
                with Locations((side_groove_x, side_groove_z)):
                    Circle(radius=side_groove_radius)
            extrude(amount=-height)
        add(side_g)

        # Mirror all tools to the other side
        tools.part = tools.part + mirror(tools.part, about=Plane.XY.offset(casing_length / 2))

    # 5. FINAL ASSEMBLY
    # Combine the shell and ribs, then subtract the tools, then add rails
    case_body = (main_shell.part + ribs.part) - tools.part + internal_rails.part
    
    # 6. FINAL GLOBAL FILLET (0.3mm)
    # Target only linear vertical edges to avoid touching the 3mm curves
    linear_y_edges = case_body.edges().filter_by(Axis.Y).filter_by(GeomType.LINE)
    case_body = fillet(linear_y_edges, radius=global_fillet)
    
    return case_body

if __name__ == "__main__":
    final_solid = create_case_body_mbs()
    show(final_solid, names=["Clean 3mm Corner Case"])