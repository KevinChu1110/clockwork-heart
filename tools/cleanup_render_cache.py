import os, shutil

dirs_to_clean = [
    "/opt/side/bravesoul-game/proofs/render_18s",
    "/opt/side/bravesoul-game/proofs/five_races_frames",
    "/tmp/contact_sheet_samples"
]

for d in dirs_to_clean:
    if os.path.exists(d):
        shutil.rmtree(d, ignore_errors=True)
        print("Cleaned:", d)

print("CLEANUP_DONE")
