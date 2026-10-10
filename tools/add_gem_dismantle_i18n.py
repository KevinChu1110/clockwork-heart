import json
import os

BASE = "/opt/side/bravesoul-game/game/data/i18n"
LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

ENTRIES = {
    "已鑲寶石：": {
        "zh_TW": "已鑲寶石：",
        "zh_CN": "已镶宝石：",
        "en": "Socketed Gem: ",
        "ja": "装着宝石：",
        "ko": "장착 보석: ",
        "es": "Gema engarzada: ",
    },
    "已鑲寶石：%s · %d 星（%s） · %s %s": {
        "zh_TW": "已鑲寶石：%s · %d 星（%s） · %s %s",
        "zh_CN": "已镶宝石：%s · %d 星（%s） · %s %s",
        "en": "Socketed Gem: %s · %d Star (%s) · %s %s",
        "ja": "装着宝石：%s · %d 星（%s） · %s %s",
        "ko": "장착 보석: %s · %d성(%s) · %s %s",
        "es": "Gema engarzada: %s · %d Estrella (%s) · %s %s",
    },
    "類型：%s（已鑲寶石）": {
        "zh_TW": "類型：%s（已鑲寶石）",
        "zh_CN": "类型：%s（已镶宝石）",
        "en": "Type: %s (Socketed)",
        "ja": "タイプ：%s（宝石装着）",
        "ko": "유형: %s (보석 장착)",
        "es": "Tipo: %s (Engarzada)",
    },
    "拆解【%s】：獲得鐵屑 ×%d、金幣 +%d、返還寶石【%s】": {
        "zh_TW": "拆解【%s】：獲得鐵屑 ×%d、金幣 +%d、返還寶石【%s】",
        "zh_CN": "拆解【%s】：获得铁屑 ×%d、金币 +%d、返还宝石【%s】",
        "en": "Dismantled [%s]: Iron Scrap x%d, Gold +%d, Returned Gem [%s]",
        "ja": "【%s】を分解：鉄くず ×%d、ゴールド +%d、宝石返還【%s】",
        "ko": "【%s】 분해: 고철 ×%d, 골드 +%d, 보석 반환【%s】",
        "es": "Desmantelado [%s]: Chatarra de hierro x%d, Oro +%d, Gema devuelta [%s]",
    },
    "拆解【%s】，獲得鐵屑×%d、金幣+%d，返還寶石【%s】": {
        "zh_TW": "拆解【%s】，獲得鐵屑×%d、金幣+%d，返還寶石【%s】",
        "zh_CN": "拆解【%s】，获得铁屑×%d、金币+%d，返还宝石【%s】",
        "en": "Dismantled [%s], received Iron Scrap x%d, Gold +%d, returned Gem [%s]",
        "ja": "【%s】を分解、鉄くず×%d、ゴールド+%dを獲得、宝石返還【%s】",
        "ko": "【%s】 분해, 고철×%d, 골드+%d 획득, 보석 반환【%s】",
        "es": "Desmantelado [%s], chatarra de hierro x%d, oro +%d, gema devuelta [%s]",
    },
    "返還寶石": {
        "zh_TW": "返還寶石",
        "zh_CN": "返还宝石",
        "en": "Returned Gem",
        "ja": "宝石返還",
        "ko": "보석 반환",
        "es": "Gema devuelta",
    },
    "返還寶石【%s】": {
        "zh_TW": "返還寶石【%s】",
        "zh_CN": "返还宝石【%s】",
        "en": "Returned Gem [%s]",
        "ja": "宝石返還【%s】",
        "ko": "보석 반환【%s】",
        "es": "Gema devuelta [%s]",
    },
}

def update_file(path, locale):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    changed = False
    for key, trans in ENTRIES.items():
        val = trans[locale]
        if key not in data or data[key] != val:
            data[key] = val
            changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {path}")
    else:
        print(f"No changes for {path}")

def main():
    p_extra = "/opt/side/bravesoul-game/proofs/t_2d2436f1/proof_05_gem_safe_in_gem_bag.png"
    if os.path.exists(p_extra):
        os.remove(p_extra)
    for loc in LOCALES:
        p_content = os.path.join(BASE, "content", loc, "ui.json")
        p_root = os.path.join(BASE, f"{loc}.json")
        update_file(p_content, loc)
        update_file(p_root, loc)

if __name__ == "__main__":
    main()
