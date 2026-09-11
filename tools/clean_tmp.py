import os
import shutil

dirs_to_clean = [
    "/tmp/test_cf",
    "/tmp/macaque_all_frames",
    "/tmp/test_frames",
    "/tmp/inspect_raw_macaque",
    "/tmp/dense",
    "/tmp/director_verify_new_rec05",
    "/tmp/side_exact_verify",
    "/tmp/inspect_dir_rec05",
    "/tmp/macaque_frames"
]

for d in dirs_to_clean:
    if os.path.isdir(d):
        shutil.rmtree(d, ignore_errors=True)
        print("Removed dir:", d)

for item in os.listdir("/tmp"):
    if item.startswith("frames_test_"):
        p = os.path.join("/tmp", item)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
            print("Removed:", p)
