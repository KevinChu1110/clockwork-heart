import sys
sys.path.insert(0, '/opt/side/bravesoul-game')
from tools.build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze
from tools.measure_speckle import interior_speckle

bronze_out = "/tmp/test_clean_bamboo_bronze.png"
create_macaque_paint_bamboo_bronze(
    src_path="/tmp/perfect_ivory_clean.png",
    out_path=bronze_out
)

print("Measuring clean bronze:")
interior_speckle(bronze_out)
