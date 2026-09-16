import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
RACES = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin"]

def audit():
    print("=== AUDIT 0-ART9 / 0-ART11 ACROSS ALL 9 RACES ===")
    results = {}
    
    for r in RACES:
        base_dir = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{r}"
        chassis_dir = f"{base_dir}/chassis"
        comp_file = f"{base_dir}/proof_paperdoll_{r}_composite.png"
        
        print(f"\n--- Checking {r} ---")
        if not os.path.exists(comp_file):
            print(f"  ❌ Composite missing: {comp_file}")
            results[r] = "MISSING_COMPOSITE"
            continue
            
        comp_im = Image.open(comp_file).convert("RGBA")
        print(f"  ✓ Composite exists: size={comp_im.size}, bbox={comp_im.getbbox()}")
        
        # Check chassis files
        if os.path.exists(chassis_dir):
            for cfile in sorted(os.listdir(chassis_dir)):
                if cfile.endswith(".png"):
                    cp = f"{chassis_dir}/{cfile}"
                    c_im = Image.open(cp).convert("RGBA")
                    print(f"  ✓ Chassis: {cfile} size={c_im.size}, bbox={c_im.getbbox()}")
        else:
            print(f"  ❌ Chassis dir missing: {chassis_dir}")

if __name__ == "__main__":
    audit()
