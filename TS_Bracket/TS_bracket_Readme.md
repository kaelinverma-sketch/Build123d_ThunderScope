# ThunderScope PCIe Bracket CAD Design Approach

This document outlines the procedural workflow and logic used to generate the ThunderScope PCIe bracket using `build123d`.

## 1. Geometric Strategy
The design follows a **Parametric Sketching** approach. Instead of using a traditional GUI, the part was constructed via code to ensure exact mathematical alignment of the PCIe standard mounting holes and the custom ThunderScope interface notches.

## 2. Structural Modules
The model is built as a `Compound` of three logical components to ensure high stability and zero geometric distortion:

### A. The Main Plate
- **Origin logic:** Sketched on the XY plane.
- **Key Modifications:** - The side tab (right-hand flange) was extended to a length of **7.25mm**. 
  - The extension was calculated by shifting the X-coordinates from the shoulder point (112.8mm) to **120.05mm**.
  - All mounting holes (radius 5.1mm and 0.8mm) were maintained at their original industrial positions.
  - The slot on the right tab was explicitly removed per the final design requirement.

### B. The Left Side Piece
- **Plane Orientation:** Sketched on a vertical plane using `Plane(origin=(0, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))`.
- **Complexity:** Contains custom rounded notches and arcs (radii 1.9mm and 2.2mm) to match the PCIe slot interface.

### C. The Notched Pin Assembly
- **Geometry:** A precision sub-assembly featuring a cylinder of radius 3.886/2mm and a hollow core for alignment.
- **Placement:** Positioned relative to the primary notch at $(10.6-7.3, 19.148-13.048)$.

## 3. Handling the 90-Degree Bend
After testing multiple iterations (3D Fillets and 2D Sketch Fillets), a **Sharp 90° Join** was selected. 
- **Reasoning:** A 1.778mm radius fillet was found to collide with the adjacent $X=11.9$ geometry and existing mounting holes, causing `BRep_API` failures.
- **Reference Match:** The final output matches the sharp-cornered grey reference model provided in the design brief.

## 4. Volumetric Analysis
The script includes a validation module to compare the material volume of the generated model against the original manufacturer's STEP file:
- **Command:** `sum(s.volume for s in final_body.solids())`
- **Goal:** To ensure the volumetric difference reflects only the intended additions (like the tab extension) and not unintended geometric artifacts.

## 5. Viewer and Export
- **Rendering:** Integrated with `ocp_vscode` for real-time visual feedback.
- **Export:** The final body is exported as a STEP file using `export_step(final_body, "TS_Bracket_NoSlot.step")`.
