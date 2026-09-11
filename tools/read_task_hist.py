import json

with open("/root/.hermes/profiles/sideart/cache/spillover/call_536465.txt") as f:
    d = json.load(f)

for r in d.get("runs", []):
    print("RUN:", r.get("id"), r.get("summary"))

for c in d.get("comments", [])[-5:]:
    print("COMMENT:", c.get("body")[:300])
