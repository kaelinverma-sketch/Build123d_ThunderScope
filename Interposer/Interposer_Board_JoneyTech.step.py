from build123d import *

try:
    from ocp_vscode import show_object
except ImportError:
    def show_object(obj, name=None):
        pass

# --- Geometry Data (2 Decimal Places) ---
outer_pts = [(0.0, 0.0), (-123.0, 0.0), (-123.0, -74.5), (-109.5, -74.5), (-109.5, -99.5), (0.0, -99.5)]
window1_pts = [(-107.43, -25.53), (-107.43, -21.53), (-104.2, -21.53), (-103.0, -21.53), (-87.53, -21.53), (-87.53, -25.53), (-85.97, -25.53), (-85.97, -13.03), (-109.02, -13.03), (-109.02, -25.53)]
window2_pts = [(-28.18, -51.03), (-28.18, -27.97), (-40.67, -27.97), (-40.67, -29.53), (-36.67, -29.53), (-36.67, -49.42), (-40.68, -49.42), (-40.68, -51.03)]
holes = [(-10.00, -28.10, 1.75), (-116.68, -39.53, 1.75), (-9.98, -71.40, 1.75), (-97.48, -77.53, 1.75)]

with BuildPart() as interpose:
    with BuildSketch() as s:
        # Create main body
        with BuildLine():
            Polyline(outer_pts, close=True)
        make_face()
        
        # Subtract Windows
        for pts in [window1_pts, window2_pts]:
            with BuildLine(mode=Mode.SUBTRACT):
                Polyline(pts, close=True)
            make_face(mode=Mode.SUBTRACT)
        
        # Subtract Holes
        for x, y, r in holes:
            with Locations((x, y)):
                Circle(radius=r, mode=Mode.SUBTRACT)
                
    # Extrude to thickness
    extrude(amount=0.74)
    
    # Apply 0.50mm fillets to all vertical edges
    fillet(interpose.edges().filter_by(Axis.Z), radius=0.50)

# 1. Print Volume
print(f"\nFinal Volume: {interpose.part.volume:.2f} mm^3")

# 2. Export STEP file (Corrected syntax)
export_step(interpose.part, "Interposer.step")
print("File exported as 'Interposer.step'")

# 3. Show in OCP Viewer
show_object(interpose, name="Interposer")
