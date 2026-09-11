import json

with open("/root/.hermes/profiles/sideart/cache/spillover/call_536465.txt") as f:
    d = json.load(f)

for c in d.get("comments", []):
    if "第 4b" in c.get("body", ""):
        print("=== COMMENT ===")
        print(c.get("body"))
