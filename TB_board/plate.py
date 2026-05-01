from build123d import *
from ocp_vscode import show

# 1. Parameters
thickness = 0.781  # mm
# Note: To flip bulges, we will use -bulge in the sagitta calculation

# 2. Rounded Coordinates and Bulge values from DXF (x, y, bulge)
pts = [
    (-62.54, 58.27, 0.0),
    (-62.7, 57.96, -0.42),
    (-63.37, 57.74, 0.0),
    (-66.32, 59.21, 0.41),
    (-66.59, 59.12, 0.0),
    (-67.94, 56.42, 0.0),
    (-65.35, 55.12, -1.0),
    (-65.89, 54.05, 0.0),
    (-68.48, 55.34, 0.0),
    (-75.31, 41.68, 0.41),
    (-75.22, 41.41, 0.0),
    (-72.27, 39.94, -0.42),
    (-72.05, 39.27, 0.0),
    (-72.2, 38.95, 0.41),
    (-72.11, 38.68, 0.0),
    (-52.79, 29.02, 0.41),
    (-52.53, 29.11, 0.0),
    (-52.37, 29.43, -0.42),
    (-51.7, 29.65, 0.0),
    (-48.75, 28.17, 0.41),
    (-48.48, 28.26, 0.0),
    (-41.65, 41.93, 0.0),
    (-44.24, 43.22, -1.0),
    (-43.7, 44.3, 0.0),
    (-41.11, 43.0, 0.0),
    (-39.76, 45.71, 0.41),
    (-39.85, 45.97, 0.0),
    (-42.8, 47.45, -0.42),
    (-43.02, 48.12, 0.0),
    (-42.87, 48.43, 0.41),
    (-42.95, 48.7, 0.0),
    (-62.27, 58.36, 0.41)
]

with BuildPart() as tb_part_inverted:
    with BuildSketch() as sketch:
        with BuildLine() as outline:
            for i in range(len(pts)):
                start_p = pts[i]
                end_p = pts[(i + 1) % len(pts)]
                
                p1 = (start_p[0], start_p[1])
                p2 = (end_p[0], end_p[1])
                bulge = start_p[2]

                if bulge == 0:
                    Line(p1, p2)
                else:
                    dist = (Vector(p1) - Vector(p2)).length
                    # Flip the bulge by multiplying by -1
                    sagitta = (dist / 2) * (-bulge) 
                    SagittaArc(p1, p2, sagitta)
        
        make_face()
    
    # 3. Extrude to the specified thickness
    extrude(amount=thickness)

# 4. Show the finalized part with inverted arcs
show(tb_part_inverted)