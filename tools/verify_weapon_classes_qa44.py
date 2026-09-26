import json
import re

def check_emoji(text):
    for ch in text:
        cp = ord(ch)
        if ((0x2600 <= cp <= 0x27BF and cp not in (0x2715, 0x2713)) or
            (0x1F300 <= cp <= 0x1FAFF)):
            return True
    return False

def main():
    base_table = json.load(open("game/data/tables/weapon_classes.json", encoding="utf-8"))
    classes = base_table["classes"]

    locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
    loc_data = {}
    for loc in locales:
        loc_data[loc] = json.load(open(f"game/data/i18n/content/{loc}/weapon_class.json", encoding="utf-8"))

    print(f"Total weapon classes: {len(classes)}")
    all_ok = True

    for c in classes:
        cid = c["id"]
        print(f"\n--- Checking Class: {cid} (atk:{c.get('atk')} def:{c.get('def')} hp:{c.get('hp')} crit:{c.get('crit')}) ---")
        for loc in locales:
            d = loc_data[loc].get(cid, {})
            name = d.get("name", "")
            title = d.get("title", "")
            play = d.get("play", "")
            pros = d.get("pros", [])
            pro0 = pros[0] if pros else ""

            if not name or not title or not play or not pro0:
                print(f"  [ERROR] {loc} missing required fields in {cid}: {d}")
                all_ok = False

            if loc == "en" and name == "S":
                print(f"  [ERROR] en name is 'S' for {cid}!")
                all_ok = False

            sep = " · " if loc in ["en", "es"] else ("・" if loc == "ja" else "·")
            btn = f"{name}{sep}{title}"

            for field_name, text in [("name", name), ("title", title), ("play", play), ("pro0", pro0)]:
                if check_emoji(text):
                    print(f"  [ERROR] {loc} {cid} {field_name} contains emoji: {text}")
                    all_ok = False

            print(f"  [{loc}] Btn: \"{btn}\" | Play: \"{play[:25]}...\" | Pro0: \"{pro0[:20]}...\"")

    # Verify dialogLines for forge.path_chosen across locales
    print("\n--- Verifying forge.path_chosen across locales ---")
    for loc in ["zh_TW", "en", "ja"]:
        dlg_path = f"game/data/dialogues/{loc}/craft.json" if loc != "zh_TW" else "game/data/dialogues/craft.json"
        dlg_data = json.load(open(dlg_path, encoding="utf-8"))
        chosen_lines = dlg_data.get("forge.path_chosen", [])
        print(f"[{loc}] forge.path_chosen lines count: {len(chosen_lines)}")
        for line in chosen_lines:
            spk = line.get("speaker")
            txt = line.get("text")
            print(f"  Speaker: {spk} | Text: {txt}")

    if all_ok:
        print("\n>>> ALL CHECKS PASSED SUCCESSFULLY! <<<")
    else:
        print("\n>>> SOME CHECKS FAILED! <<<")

if __name__ == "__main__":
    main()
