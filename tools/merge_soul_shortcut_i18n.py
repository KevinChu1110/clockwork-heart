import json
import os

repo = "/opt/side/bravesoul-game"

keys = {
    "zh_TW": {
        "戰魂共鳴": "戰魂共鳴",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "戰魂總加成: 攻+%d · 防+%d · 血+%d",
        "未喚醒": "未喚醒",
        "全+%d": "全+%d",
    },
    "zh_CN": {
        "战魂共鸣": "战魂共鸣",
        "战魂总加成: 攻+%d · 防+%d · 血+%d": "战魂总加成: 攻+%d · 防+%d · 血+%d",
        "未唤醒": "未唤醒",
        "全+%d": "全+%d",
        "戰魂共鳴": "战魂共鸣",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "战魂总加成: 攻+%d · 防+%d · 血+%d",
        "未喚醒": "未唤醒",
    },
    "en": {
        "戰魂共鳴": "Soul Resonance",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "Soul Total: ATK+%d · DEF+%d · HP+%d",
        "未喚醒": "Dormant",
        "全+%d": "ALL+%d",
    },
    "ja": {
        "戰魂共鳴": "戦魂共鳴",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "戦魂合計加成: 攻+%d · 防+%d · HP+%d",
        "未喚醒": "未覚醒",
        "全+%d": "全+%d",
    },
    "ko": {
        "戰魂共鳴": "전혼 공명",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "전혼 총 보너스: 공+%d · 방+%d · 체+%d",
        "未喚醒": "미각성",
        "全+%d": "올+%d",
    },
    "es": {
        "戰魂共鳴": "Resonancia de Almas",
        "戰魂總加成: 攻+%d · 防+%d · 血+%d": "Total de Almas: ATQ+%d · DEF+%d · PV+%d",
        "未喚醒": "Inactivo",
        "全+%d": "TOD+%d",
    },
}

for loc, kv in keys.items():
    p1 = os.path.join(repo, "game/data/i18n", f"{loc}.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p1)

    p2 = os.path.join(repo, "game/data/i18n/content", loc, "ui.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.update(kv)
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("Updated", p2)
