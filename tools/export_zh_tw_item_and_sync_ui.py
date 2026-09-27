import json, os, re

ROOT = "/opt/side/bravesoul-game"
cat_path = f"{ROOT}/game/scripts/systems/inventory_system.gd"
with open(cat_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 抓出 22 個道具的繁中 name 與 desc
zh_tw_items = {}
pattern = re.compile(r'^\t"(\w+)":\s*\{(.*?extraneous|.*?^\t\},)', re.MULTILINE | re.DOTALL)
for m in re.finditer(r'^\t"(\w+)":\s*\{(.*?^\t\},)', text, re.MULTILINE | re.DOTALL):
    iid = m.group(1)
    body = m.group(2)
    name_m = re.search(r'"name":\s*"([^"]+)"', body)
    desc_m = re.search(r'"desc":\s*"([^"]+)"', body)
    if name_m and desc_m:
        zh_tw_items[iid] = {
            "name": name_m.group(1),
            "desc": desc_m.group(1)
        }

print("zh_TW items found:", len(zh_tw_items))

# 寫入 zh_TW/item.json
tw_path = f"{ROOT}/game/data/i18n/content/zh_TW/item.json"
with open(tw_path, 'w', encoding='utf-8') as f:
    json.dump(zh_tw_items, f, ensure_ascii=False, indent=2, sort_keys=True)
print("Wrote zh_TW/item.json successfully")

# 另外，為了讓 ContentLoc.text("ui", 繁中) 也能直接對照（對齊 skill 和 title 的做法）：
# 我們把 繁中 name -> 譯文 name, 繁中 desc -> 譯文 desc 加到各語系的 ui.json 中
LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
for loc in LOCALES:
    ui_path = f"{ROOT}/game/data/i18n/content/{loc}/ui.json"
    item_loc_path = f"{ROOT}/game/data/i18n/content/{loc}/item.json"
    if not os.path.exists(item_loc_path):
        continue
    with open(item_loc_path, 'r', encoding='utf-8') as f:
        loc_data = json.load(f)
    with open(ui_path, 'r', encoding='utf-8') as f:
        ui_data = json.load(f)
    
    added = 0
    for iid, tw_val in zh_tw_items.items():
        tw_name = tw_val["name"]
        tw_desc = tw_val["desc"]
        tr_name = loc_data.get(iid, {}).get("name", tw_name)
        tr_desc = loc_data.get(iid, {}).get("desc", tw_desc)
        if tw_name not in ui_data or ui_data[tw_name] != tr_name:
            ui_data[tw_name] = tr_name
            added += 1
        if tw_desc not in ui_data or ui_data[tw_desc] != tr_desc:
            ui_data[tw_desc] = tr_desc
            added += 1
    
    with open(ui_path, 'w', encoding='utf-8') as f:
        json.dump(ui_data, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[{loc}] Added/updated {added} keys in ui.json")
