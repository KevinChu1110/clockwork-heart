import os, shutil

tmp_entries = os.listdir("/tmp")
for e in tmp_entries:
    if e.startswith("five_races") or e.startswith("check_") or e.startswith("mc_frames") or e.endswith(".log") or e.endswith(".flag") or e.startswith("godot"):
        p = os.path.join("/tmp", e)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            try:
                os.remove(p)
            except Exception:
                pass

print("CLEANUP_DONE")
