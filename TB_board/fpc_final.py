from build123d import *
from ocp_vscode import show
import math

# --- Dimensions ---
width_left = 3.00
width_right = 3.50
total_width = width_left + width_right
step_height = 0.28
total_height = 4.05
fillet_radius = 1.00
extrude_length = 21.9

# Subtractive/prot dimensions
cut_width = 0.40; cut_height = 1.56; cut_depth = 0.49; dist_from_top = 0.49
slot_length = 5.50; slot_dist_from_top = 1.30; slot_height = 1.20; slot_depth = 0.412
slot_y_min = total_width - slot_length
spine_w = 0.80; tab_w   = 1.25

z0 = step_height; z1 = z0 + 0.30; z2 = z1 + 0.52; z3 = z2 + 0.40; z4 = z3 + 0.93
prot_pts = [(0,z0),(-spine_w,z0),(-spine_w,z1),(-tab_w,z1),(-tab_w,z2),(-spine_w,z2),(-spine_w,z3),(-tab_w,z3),(-tab_w,z4),(0,z4)]
prot2_depth = 2.345; prot2_x_end = extrude_length - 1.45; prot2_x_start = prot2_x_end - prot2_depth; gap = 1.59
prot1_depth = 14.845; prot1_x_end = prot2_x_start - gap; prot1_x_start = prot1_x_end - prot1_depth

# Sketch dimensions
sketch_x = 0.875; arc_center_z = total_height - fillet_radius; sk_z_top = total_height - 0.15
sk_z_right = sk_z_top - 1.049; sk_z_bot = sk_z_top - 2.001 - 0.647; sk_z_step = sk_z_bot + step_height
sk_y_right = 2.10; sk_y_step = sk_y_right - 1.00; sk_y_left = 0.0
arc_start = (sk_y_left, arc_center_z - fillet_radius)
arc_end_y = math.sqrt(fillet_radius**2 - (sk_z_top - arc_center_z)**2)
arc_end = (arc_end_y, sk_z_top)

# --- L-TAB POSITIONING ANCHORS ---
lsk_y_spine_inner = -0.1            
lsk_z_top = z0 

# --- Main Body Logic ---
with BuildPart() as body:
    with BuildSketch(Plane.YZ) as profile:
        pts = [(0, step_height),(width_left, step_height),(width_left, 0),(total_width, 0),(total_width, total_height),(0, total_height)]
        Polygon(pts); top_left = profile.vertices().sort_by(Axis.Y)[-2:].sort_by(Axis.X)[0]; fillet(top_left, radius=fillet_radius)
    extrude(amount=extrude_length)

main_body = body.part
cut_y_min = total_width - cut_width; cut_z_min = total_height - dist_from_top - cut_height
left_cut = Box(cut_depth, cut_width, cut_height, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((0, cut_y_min, cut_z_min)))
right_cut = Box(cut_depth, cut_width, cut_height, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((extrude_length - cut_depth, cut_y_min, cut_z_min)))
slot_z_min = total_height - slot_dist_from_top - slot_height
left_slot = Box(slot_depth, slot_length, slot_height, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((0, slot_y_min, slot_z_min)))
right_slot = Box(slot_depth, slot_length, slot_height, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((extrude_length - slot_depth, slot_y_min, slot_z_min)))

with BuildSketch(Plane.YZ) as prot_sketch1: Polygon(prot_pts, align=None)
protrusion1 = extrude(prot_sketch1.sketch, amount=prot1_depth).move(Location((prot1_x_start, 0, 0)))
with BuildSketch(Plane.YZ) as prot_sketch2: Polygon(prot_pts, align=None)
protrusion2 = extrude(prot_sketch2.sketch, amount=prot2_depth).move(Location((prot2_x_start, 0, 0)))

result = main_body - left_cut - right_cut - left_slot - right_slot

def make_end_sketch(plane):
    with BuildSketch(plane) as sk:
        with BuildLine():
            Polyline([(sk_y_left, sk_z_bot), (sk_y_right, sk_z_bot), (sk_y_right, sk_z_step), (sk_y_step, sk_z_step), (sk_y_step, sk_z_right), (sk_y_right, sk_z_right), (sk_y_right, sk_z_top), arc_end])
            RadiusArc(arc_end, arc_start, -fillet_radius)
            Polyline([arc_start, (sk_y_left, sk_z_bot)])
        make_face()
    return sk

result = result - extrude(make_end_sketch(Plane.YZ.offset(sketch_x)).sketch, amount=15.56 + 0.09)
result = result - extrude(make_end_sketch(Plane.YZ.offset(sketch_x + 15.56 + 1.19)).sketch, amount=3.4)
result = result - Box(extrude_length, 3.50, 0.28, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((0, 3, 0)))
result = result + Box(extrude_length, 3.50, 0.28, align=(Align.MIN, Align.MIN, Align.MIN)).move(Location((0, 0, 0)))

# --- L-TAB SHARED GEOMETRY ---
vw, vh = 0.15, 0.38
hw, hh = 0.45, 0.15
Ri, Ro = 0.10, 0.25
ocx_local = -(Ri + vw) + Ro
ocy_local = -(Ri + hh) + Ro
tp_vert_local  = (-(Ri + vw), ocy_local)
tp_horiz_local = (ocx_local, -(Ri + hh))

def create_tab(x_pos):
    with BuildPart() as temp:
        with BuildSketch(Plane.YZ.offset(x_pos) * Location((-lsk_y_spine_inner + Ri + vw, lsk_z_top - vh))) as sk:
            with BuildLine():
                Line((-(Ri + vw), vh),  (-Ri, vh))
                Line((-Ri, vh),         (-Ri, 0))
                RadiusArc((-Ri, 0), (0, -Ri), -Ri)
                Line((0, -Ri),          (hw, -Ri))
                Line((hw, -Ri),         (hw, -(Ri + hh)))
                Line((hw, -(Ri + hh)),  tp_horiz_local)
                RadiusArc(tp_horiz_local, tp_vert_local, Ro)
                Line(tp_vert_local,     (-(Ri + vw), vh))
            make_face()
        extrude(amount=0.15)
    return temp.part.mirror(Plane.XZ)

# --- PATTERNING DYNAMICS ---
lsk_plane_offset = 1.875
tab_thickness = 0.15
standard_gap = 0.35
spacing = tab_thickness + standard_gap 
large_offset = 2.35 + 0.5

lsk_all_tabs = []

# Group 1: 29 tabs
for i in range(29):
    lsk_all_tabs.append(create_tab(lsk_plane_offset + (i * spacing)))

# Group 2: 4 more tabs
group1_end_face = lsk_plane_offset + (27 * spacing) + tab_thickness
group2_start_face = group1_end_face + large_offset

for i in range(4):
    lsk_all_tabs.append(create_tab(group2_start_face + (i * spacing)))

# --- NEW OPERATION: MIRROR TO OPPOSITE EDGE ---
# The main body width is total_width (6.50). We mirror across the center Y plane.
mirror_plane = Plane.XZ.offset((-total_width+0.25) / 2)
opposite_tabs = [t.mirror(mirror_plane) for t in lsk_all_tabs]

show(result, protrusion1, protrusion2, *lsk_all_tabs, *opposite_tabs)

export_step(result, "fpc_final.step")
# Combine all parts into one list to calculate volume
all_parts = [result, protrusion1, protrusion2] + lsk_all_tabs + opposite_tabs
total_volume = sum(p.volume for p in all_parts)

print(f"Total Volume: {total_volume:.4f} mm³")