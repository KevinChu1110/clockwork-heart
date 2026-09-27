import hashlib
import os

proof_dir = "/opt/side/bravesoul-game/proofs/soul-result-card-i18n"
for root, dirs, files in os.walk(proof_dir):
    for f in sorted(files):
        p = os.path.join(root, f)
        with open(p, "rb") as fp:
            data = fp.read()
            md5 = hashlib.md5(data).hexdigest()
        rel = os.path.relpath(p, proof_dir)
        print(f"{rel}: {len(data)} bytes, md5: {md5}")
