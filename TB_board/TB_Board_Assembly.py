import sys
import os
import importlib.util
import build123d
from ocp_vscode import show, set_port

# Check if Assembly exists in the library
if hasattr(build123d, "Assembly"):
    from build123d import Assembly
else:
    # Fallback for older versions or specific installs
    print("Warning: 'Assembly' not found in build123d. Using Compound fallback.")
    Assembly = None

from build123d import Part, Compound, Solid, import_step

set_port(3939)

# 1. ABSOLUTE PATH SETUP
BASE_DIR = "/Users/softage/ThunderScope/Generated models/TB_board/"
STEP_PATH = os.path.join(BASE_DIR, "TB_Board.step")

# 2. LOAD GENERATED PARTS
def load_part(file_name):
    full_path = os.path.join(BASE_DIR, file_name)
    if not os.path.exists(full_path):
        return None
    spec = importlib.util.spec_from_file_location("mod", full_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        for attr in ['adaptor_body', 'base_body', 'fpc_body', 'result']:
            if hasattr(module, attr): return getattr(module, attr)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, (Part, Compound, Solid)): return obj
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
    return None

gen_base = load_part("base_board.py")
gen_adaptor = load_part("adaptor_board.py")
gen_fpc = load_part("fpc_final.py")

# 3. LOAD STEP REFERENCE
step_solids = []
ref_step = None
if os.path.exists(STEP_PATH):
    ref_step = import_step(STEP_PATH)
    step_solids = list(ref_step.solids())
    print(f"Found {len(step_solids)} solids in STEP.")

# 4. BUILD THE ASSEMBLY (OR COMPOUND)
final_parts = []

parts_list = [(gen_base, "Base"), (gen_adaptor, "Adaptor"), (gen_fpc, "FPC")]

for part, label in parts_list:
    if part is not None:
        # Match volume
        match_loc = None
        v = part.volume
        for s in step_solids:
            if abs(s.volume - v) / v < 0.20:
                match_loc = s.location
                break
        
        # Apply location and add to list
        moved_part = part.move(match_loc) if match_loc else part
        final_parts.append(moved_part)
        print(f"{'✓' if match_loc else '!'} Processed {label}")

# 5. SHOW RESULTS
if final_parts:
    # Use Assembly if available, otherwise just show a list of parts
    if Assembly:
        ts_asm = Assembly(name="ThunderScope")
        for i, p in enumerate(final_parts):
            ts_asm.add(p, name=f"Part_{i}")
        show(ts_asm, ref_step, names=["Assembly", "Ref"])
    else:
        show(*final_parts, ref_step, names=["Parts", "Ref"])
else:
    print("No parts found to display.")