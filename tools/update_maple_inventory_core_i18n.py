#!/usr/bin/env python3
import json
import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
content_base = os.path.join(repo_root, "game/data/i18n/content")
root_i18n_base = os.path.join(repo_root, "game/data/i18n")

translations = {
    "zh_TW": {
        "機芯": "機芯",
        "替換機芯": "替換機芯",
        "已成功替換裝備至【%s】槽位！": "已成功替換裝備至【%s】槽位！",
    },
    "zh_CN": {
        "機芯": "机芯",
        "替換機芯": "替换机芯",
        "已成功替換裝備至【%s】槽位！": "已成功替换装备至【%s】槽位！",
    },
    "en": {
        "機芯": "Core",
        "替換機芯": "Swap Core",
        "已成功替換裝備至【%s】槽位！": "Successfully equipped to slot [%s]!",
    },
    "ja": {
        "機芯": "コア",
        "替換機芯": "コア入替",
        "已成功替換裝備至【%s】槽位！": "【%s】スロットへの装備入替が完了しました！",
    },
    "ko": {
        "機芯": "코어",
        "替換機芯": "코어 교체",
        "已成功替換裝備至【%s】槽位！": "【%s】슬롯에 장비를 성공적으로 교체했습니다!",
    },
    "es": {
        "機芯": "Núcleo",
        "替換機芯": "Cambiar núcleo",
        "已成功替換裝備至【%s】槽位！": "¡Equipo reemplazado con éxito en la ranura [%s]!",
    },
}

for lang, items in translations.items():
    # 1. Update content/<lang>/ui.json
    p_content = os.path.join(content_base, lang, "ui.json")
    if os.path.exists(p_content):
        with open(p_content, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in items.items():
            d[k] = v
        with open(p_content, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Updated {lang}/ui.json")

    # 2. Update <lang>.json
    p_root = os.path.join(root_i18n_base, f"{lang}.json")
    if os.path.exists(p_root):
        with open(p_root, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in items.items():
            d[k] = v
        with open(p_root, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"Updated {lang}.json")
