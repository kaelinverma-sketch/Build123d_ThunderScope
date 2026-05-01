#  ThunderScope project

Assembly

This repository contains the parametric source code for the ThunderScope mechanical enclosure. The project utilizes a code-driven CAD approach to define, transform, and assemble high-precision mechanical components using the `build123d` framework.

## Methodology

### 1. Parametric Foundation
The assembly is built upon a **Master Dimension Block**. Every feature—from the 120mm vertical height of the case to the specific 0.38mm radius of the side grooves—is defined as a variable. This allows for rapid iteration and ensures that downstream transformations (like mirroring or offsetting) maintain perfect tolerances across the entire model.

### 2. Functional Component Logic
Parts are generated through functional creation functions (`create_case_body_mbs`, `create_l_bezel`, etc.). Each component follows a "Clean Room" construction logic:
* **Case Body:** Utilizes boolean subtraction and internal rail logic to define structural support and heat dissipation ribs.
* **Front Panel:** Features dual-radius fillets and cylindrical cutouts for interface components.
* **L-Bezel & End Plate:** Constructed at the origin (Y=0) to serve as master templates before being moved into final assembly positions.

### 3. The "Algebraic Flip" Assembly Pattern
To avoid the common pitfalls of the standard `mirror()` operation—which can invert the "handedness" of parts and break vertex-indexing or hole orientation—this assembly uses a **Rotation-Translation Pattern**:
* **Rotation Logic:** Flipped components (like the bottom bezel) are created using a `Rotation(180, 0, 0)` transformation. This preserves the geometric orientation while rotating the part 180 degrees around the X-axis.
* **Algebraic Transformation:** The assembly utilizes the `*` operator and the `.moved(Location())` method to create transformed copies of master parts without mutating the original geometry.

### 4. Precision Exploded View
The script is configured for an **Exploded Visualization** state, providing clear visibility of internal mating surfaces:
* **Y-Axis Explosion:** Symmetrical 3mm gaps are applied at the top (Y=123) and bottom (Y=-3) planes.
* **Z-Axis Explosion:** The rear assembly features a precision 3.10mm longitudinal shift (Z = 104.60).
* **Component Nesting:** The End Plate is seated deeper into the bezel (Z = 103.10) to simulate actual seated depth while remaining exploded from the main case.

### 5. Multi-Mode Exporting
The workflow includes a robust STEP export pipeline featuring:
* **GUI-First Interaction:** Utilizing `tkinter` for a native system "Save As" dialog.
* **CLI Fallback:** A console-based path input system ensures the script remains functional in environments where graphical libraries are not configured (common in some Homebrew or virtual environment setups).
* **Compound Aggregation:** Individual bodies are wrapped into a single `Compound` object during export to preserve the assembly structure when imported into other CAD platforms (Fusion 360, SolidWorks, etc.).

## Dependencies
* **Python 3.11+**
* **build123d:** Core CAD engine.
* **ocp_vscode:** For real-time visualization.
* **python-tk:** (Optional) Required for the graphical save dialog.
