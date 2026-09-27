with open("/root/.hermes/profiles/sideworker/skills/creative/bravesoul/references/review.md", "r") as f:
    text = f.read()

import re
matches = re.findall(r"^## 0-QA\d+.*$", text, re.MULTILINE)
for m in matches:
    print(m)
