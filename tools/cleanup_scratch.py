import os, glob

# Remove temporary png and py in tools
for p in glob.glob('tools/check_*.py') + glob.glob('tools/inspect_*.py') + glob.glob('tools/diff_*.py') + glob.glob('tools/find_*.py') + glob.glob('tools/crop_*.py') + glob.glob('tools/*.png'):
    try:
        os.remove(p)
    except Exception as e:
        print(f"Error {p}: {e}")
print("Cleanup done")
