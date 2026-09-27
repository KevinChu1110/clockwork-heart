with open("/root/.hermes/profiles/sideworker/skills/creative/bravesoul/references/review.md", "r") as f:
    text = f.read()

import re
m = re.search(r"## 0-QA16.*?(?=\n## 0-|\Z)", text, re.DOTALL)
if m:
    print(m.group(0)[:2000])
else:
    print("0-QA16 not found")

m2 = re.search(r"## 0-QA31.*?(?=\n## 0-|\Z)", text, re.DOTALL)
if m2:
    print("\n" + "="*50)
    print(m2.group(0)[:2000])
