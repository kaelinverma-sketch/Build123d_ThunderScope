# Generated_TS_Back_Endcap_3D Design Approach

This document outlines the methodology and geometric constraints used to generate the 3D model for the ThunderScope Back Endcap using the `build123d` python library.

## 1. Shared Base Geometry
The Back Endcap shares the standard enclosure profile used across the project:
- **Dimensions:** 103.0 mm (Width) x 30.5 mm (Height).
- **Fillets:** 4.0 mm radius on all four corners.
- **Mounting:** Four 2.1 mm radius holes located 4.0 mm from the adjacent edges (centers at (-4,-4), (-99,-4), (-4,-26.5), and (-99,-26.5)).
- **Thickness:** Extruded to a depth of 1.51 mm.

## 2. Back Endcap Specific Features

### A. Ventilation System (Fan Vents)
- **Design:** Spoke-supported arc slots surrounding a solid central hub.
- **Placement:** Centered at (-85.7, -17.2).
- **Slots:** Four SlotArcs distributed at 45°, 135°, 225°, and 315° angles with a radius of 8.2 mm and a height of 2.0 mm.

### B. Notched Interface Holes
- **Quantity:** 2 holes.
- **Radius:** 5.1 mm.
- **X-Positions:** Located at -33.5 mm and -69.6 mm.
- **Y-Position:** -20.0 mm.
- **Keyway Notches:** Two $3.0 \times 1.5$ mm rectangular notches per hole, placed diametrically opposite (top and bottom).

### C. Data & Power Cutouts
- **Large Rectangular Cutout:** $20.5 \times 2.0$ mm centered at (-51.5, -17.3).
- **Small Rectangular Cutout:** $10.5 \times 3.5$ mm centered at (-51.5, -5.6).

### D. Side Alignment & Secondary Holes
- **Alignment Holes:** Three 1.3 mm radius holes located at (-77.6, -9.1), (-77.6, -25.3), and (-93.8, -9.1).
- **Side Port:** One 2.3 mm radius circular cutout at (-15.2, -20.6).

## 3. Technical Implementation
- **Library:** `build123d`.
- **Coordinate System:** Derived from the original DXF origin point to ensure 1:1 hardware fitment.
- **Export Format:** STEP file named `Generated_TS_Back_Endcap_3D.step`.
