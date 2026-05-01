from build123d import *
from ocp_vscode import show

with BuildPart() as adaptor_body:
    with BuildSketch() as adaptor_sketch:
        with BuildLine() as adaptor_outline:
            # Segment 1 to 32
            Line((-62.54, 58.27), (-62.70, 57.96))
            # Sagitta signs flipped to bulge inside (concave fillets)
            SagittaArc((-62.70, 57.96), (-63.37, 57.74), 0.15)
            Line((-63.37, 57.74), (-66.32, 59.21))
            SagittaArc((-66.32, 59.21), (-66.59, 59.12), -0.06)
            Line((-66.59, 59.12), (-67.94, 56.42))
            Line((-67.94, 56.42), (-65.35, 55.12))
            SagittaArc((-65.35, 55.12), (-65.89, 54.05), 0.60)
            Line((-65.89, 54.05), (-68.48, 55.34))
            Line((-68.48, 55.34), (-75.31, 41.68))
            SagittaArc((-75.31, 41.68), (-75.22, 41.41), -0.06)
            Line((-75.22, 41.41), (-72.27, 39.94))
            SagittaArc((-72.27, 39.94), (-72.05, 39.27), 0.15)
            Line((-72.05, 39.27), (-72.20, 38.95))
            SagittaArc((-72.20, 38.95), (-72.11, 38.68), -0.06)
            Line((-72.11, 38.68), (-52.79, 29.02))
            SagittaArc((-52.79, 29.02), (-52.53, 29.11), -0.06)
            Line((-52.53, 29.11), (-52.37, 29.43))
            SagittaArc((-52.37, 29.43), (-51.70, 29.65), 0.15)
            Line((-51.70, 29.65), (-48.75, 28.17))
            SagittaArc((-48.75, 28.17), (-48.48, 28.26), -0.06)
            Line((-48.48, 28.26), (-41.65, 41.93))
            Line((-41.65, 41.93), (-44.24, 43.22))
            SagittaArc((-44.24, 43.22), (-43.70, 44.30), 0.60)
            Line((-43.70, 44.30), (-41.11, 43.00))
            Line((-41.11, 43.00), (-39.76, 45.71))
            SagittaArc((-39.76, 45.71), (-39.85, 45.97), -0.06)
            Line((-39.85, 45.97), (-42.80, 47.45))
            SagittaArc((-42.80, 47.45), (-43.02, 48.12), 0.15)
            Line((-43.02, 48.12), (-42.87, 48.43))
            SagittaArc((-42.87, 48.43), (-42.95, 48.70), -0.06)
            Line((-42.95, 48.70), (-62.27, 58.36))
            SagittaArc((-62.27, 58.36), (-62.54, 58.27), -0.06)
        make_face()
    # Extrude the sketch by 0.781 mm
    extrude(amount=0.781)

show(adaptor_body)
# Export the adaptor body to a STEP file
export_step(adaptor_body.part, "adaptor_board.step")

# Optional: Print the volume to verify the geometry
print(f"Adaptor Board Volume: {adaptor_body.part.volume:.4f} mm³")