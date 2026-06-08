# Interposer Plate - README

A thin custom interposer plate (0.74 mm thick) with complex outer shape, two window cutouts, and four mounting holes.  
Designed using **build123d** in Python.

## Model Specifications
- Thickness: **0.74 mm**
- Fillet on all vertical edges: **0.50 mm**
- Units: Millimeters (mm)
- Four circular holes of diameter **3.5 mm**

## Design Approach (Step-by-Step)

The model is built following a clean and efficient CAD workflow:

1. **Define Geometry Data**  
   All coordinates and hole positions are stored at the top for easy modification and clarity.

2. **Create 2D Sketch**  
   - Draw the outer profile using `Polyline`.
   - Convert it into a face using `make_face()`.
   - Subtract the two irregular windows using `Mode.SUBTRACT`.
   - Subtract the four circular holes using `Circle` with `Mode.SUBTRACT`.

3. **Extrude the Sketch**  
   Extrude the final 2D sketch by **0.74 mm** to create the 3D thin plate.

4. **Apply Fillets**  
   Select all vertical edges (parallel to Z-axis) and apply **0.50 mm** fillet for smooth corners.

5. **Export & Output**  
   - Export the model as `Interposer.step`
   - Print the final volume for reference
   - Display the model in the viewer (if `ocp-vscode` is installed)

This approach keeps all boolean operations in 2D (which is faster and more stable) before going to 3D.

## How to Generate the Model

### Requirements
```bash
pip install build123d ocp-vscode
