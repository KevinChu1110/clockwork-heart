with open("/root/.hermes/profiles/sideworker/skills/creative/bravesoul/references/review.md", "r") as f:
    text = f.read()

import re
m = re.search(r"## 0-QA21.*?(?=\n## 0-|\Z)", text, re.DOTALL)
if m:
    print(m.group(0)[:2000])
