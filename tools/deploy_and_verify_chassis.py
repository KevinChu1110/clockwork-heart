import shutil
import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from tools.build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze
from tools.measure_speckle import interior_speckle

ivory_dest = "game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
bronze_dest = "game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png"

# Deploy clean ivory
shutil.copy('/tmp/perfect_ivory_clean3.png', ivory_dest)
print(f"✓ Deployed clean ivory to {ivory_dest}")

# Build clean bronze from new ivory
create_macaque_paint_bamboo_bronze()
print(f"✓ Built clean bronze to {bronze_dest}")

# Measure speckles for all three
print("\n=== FINAL VERIFIED METRICS ===")
p_iv = interior_speckle(ivory_dest)
p_br = interior_speckle(bronze_dest)
p_rab = interior_speckle("game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png")

print(f"\nTarget threshold: < 12.00% (rabbit 9.37% ± 3%)")
print(f"Macaque Ivory:  {p_iv:.2f}%  -> {'PASS' if p_iv < 12 else 'FAIL'}")
print(f"Macaque Bronze: {p_br:.2f}%  -> {'PASS' if p_br < 12 else 'FAIL'}")
print(f"Rabbit Baseline: {p_rab:.2f}%")
