import json
import os

repo = "/opt/side/bravesoul-game"
locs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

translations = {
    "已裝備無法拆解": {
        "zh_TW": "已裝備無法拆解",
        "zh_CN": "已装备无法拆解",
        "en": "Equipped (Cannot Dismantle)",
        "ja": "装備中（分解不可）",
        "ko": "장착 중（분해 불가）",
        "es": "Equipado (No Desmantelar)"
    },
    "拆解【%s】：獲得鐵屑 ×%d": {
        "zh_TW": "拆解【%s】：獲得鐵屑 ×%d",
        "zh_CN": "拆解【%s】：获得铁屑 ×%d",
        "en": "Dismantled [%s]: Iron Scrap x%d",
        "ja": "【%s】を分解：鉄屑 ×%d を獲得",
        "ko": "【%s】 분해: 고철 ×%d 획득",
        "es": "Desmantelado [%s]: Chatarra de hierro x%d"
    },
    "拆解機芯回收鐵屑": {
        "zh_TW": "拆解機芯回收鐵屑",
        "zh_CN": "拆解机芯回收铁屑",
        "en": "Dismantle Core for Scrap Iron",
        "ja": "コアパーツを分解して鉄屑を回収",
        "ko": "코어를 분해하여 고철 회수",
        "es": "Desmantelar núcleo para recuperar chatarra"
    },
    "非裝備或機芯物品無法拆解。": {
        "zh_TW": "非裝備或機芯物品無法拆解。",
        "zh_CN": "非装备或机芯物品无法拆解。",
        "en": "Cannot dismantle items other than equipment or cores.",
        "ja": "装備またはコアパーツ以外のアイテムは分解できません。",
        "ko": "장비 또는 코어 아이템 외에는 분해할 수 없습니다.",
        "es": "No se pueden desmantelar objetos que no sean equipo o núcleos."
    },
    "機芯部件 · 強化發條動力核心": {
        "zh_TW": "機芯部件 · 強化發條動力核心",
        "zh_CN": "机芯部件 · 强化发条动力核心",
        "en": "Core Part · Enhances Clockwork Power Core",
        "ja": "コアパーツ · 発条動力コアを強化",
        "ko": "코어 파츠 · 태엽 동력 코어 강화",
        "es": "Pieza de núcleo · Mejora el núcleo cinético"
    },
    "機芯部件 · 部位：%s · 色階：%s": {
        "zh_TW": "機芯部件 · 部位：%s · 色階：%s",
        "zh_CN": "机芯部件 · 部位：%s · 色阶：%s",
        "en": "Core Part · Slot: %s · %s",
        "ja": "コアパーツ · スロット：%s · %s",
        "ko": "코어 파츠 · 슬롯: %s · %s",
        "es": "Pieza de núcleo · Ranura: %s · %s"
    }
}

for loc in locs:
    ui_path = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in translations.items():
            data[k] = v[loc]
        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {ui_path}")

    root_path = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(root_path):
        with open(root_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in translations.items():
            data[k] = v[loc]
        with open(root_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {root_path}")
