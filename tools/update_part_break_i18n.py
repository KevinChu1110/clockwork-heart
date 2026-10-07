import json
import os

base_path = "/opt/side/bravesoul-game/game/data/i18n/content"
new_translations = {
    "zh_TW": {
        "核心反應爐": "核心反應爐",
        "動力履帶": "動力履帶",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "部位破壞成就",
        "戰利品已入袋": "戰利品已入袋",
        "背包": "背包"
    },
    "zh_CN": {
        "核心反應爐": "核心反应炉",
        "動力履帶": "动力履带",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "部位破坏成就",
        "戰利品已入袋": "战利品已入袋",
        "背包": "背包"
    },
    "en": {
        "核心反應爐": "Core Reactor",
        "動力履帶": "Power Tread",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "Part Break Achievement",
        "戰利品已入袋": "Loot Stashed in Bag",
        "背包": "Bag"
    },
    "ja": {
        "核心反應爐": "コア反応炉",
        "動力履帶": "動力キャタピラ",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "部位破壊実績",
        "戰利品已入袋": "戦利品獲得",
        "背包": "バッグ"
    },
    "ko": {
        "核心反應爐": "코어 반응로",
        "動力履帶": "동력 무한궤도",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "부위 파괴 업적",
        "戰利品已入袋": "전리품 획득 완료",
        "背包": "가방"
    },
    "es": {
        "核心反應爐": "Reactor del Núcleo",
        "動力履帶": "Oruga de Potencia",
        "PART BREAK": "PART BREAK",
        "部位破壞成就": "Logro de Parte Destruida",
        "戰利品已入袋": "Botín en la mochila",
        "背包": "Mochila"
    }
}

for lang, trans in new_translations.items():
    file_path = os.path.join(base_path, lang, "ui.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in trans.items():
        data[k] = v
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {lang}/ui.json")
