#!/usr/bin/env python3
import json
import os

translations = {
    "zh_TW": {
        "推薦 Lv.%d": "推薦 Lv.%d",
        "未達 Lv.%d 不可出征": "未達 Lv.%d 不可出征",
        "需達 Lv.%d": "需達 Lv.%d",
        "未達標": "未達標",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征",
    },
    "zh_CN": {
        "推薦 Lv.%d": "推荐 Lv.%d",
        "未達 Lv.%d 不可出征": "未达 Lv.%d 不可出征",
        "需達 Lv.%d": "需达 Lv.%d",
        "未達標": "未达标",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "等级未达 Lv.%d，低于推荐等级 10 级以上不可出征！",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "等级未达 Lv.%d，低于推荐等级 10 级以上不可出征",
    },
    "en": {
        "推薦 Lv.%d": "Rec. Lv.%d",
        "未達 Lv.%d 不可出征": "Requires Lv.%d to sortie",
        "需達 Lv.%d": "Requires Lv.%d",
        "未達標": "Locked",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "Requires Lv.%d; cannot sortie if 10+ levels below recommended!",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "Requires Lv.%d; cannot sortie if 10+ levels below recommended",
    },
    "ja": {
        "推薦 Lv.%d": "推奨 Lv.%d",
        "未達 Lv.%d 不可出征": "Lv.%d未満出撃不可",
        "需達 Lv.%d": "Lv.%dで解放",
        "未達標": "未解放",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "Lv.%d未達です。推奨レベルより10以上低い場合は出撃できません！",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "Lv.%d未達です。推奨レベルより10以上低い場合は出撃できません",
    },
    "ko": {
        "推薦 Lv.%d": "추천 Lv.%d",
        "未達 Lv.%d 不可出征": "Lv.%d 미만 출정 불가",
        "需達 Lv.%d": "Lv.%d 필요",
        "未達標": "잠김",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "Lv.%d 미달입니다. 추천 레벨보다 10레벨 이상 낮으면 출정할 수 없습니다!",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "Lv.%d 미달입니다. 추천 레벨보다 10레벨 이상 낮으면 출정할 수 없습니다",
    },
    "es": {
        "推薦 Lv.%d": "Rec. Nv.%d",
        "未達 Lv.%d 不可出征": "Requiere Nv.%d para salir",
        "需達 Lv.%d": "Requiere Nv.%d",
        "未達標": "Bloqueado",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！": "¡Nivel inferior a Nv.%d; no se puede salir con 10+ niveles por debajo del recomendado!",
        "等級未達 Lv.%d，低於推薦等級 10 級以上不可出征": "Nivel inferior a Nv.%d; no se puede salir con 10+ niveles por debajo del recomendado",
    }
}

for loc, kv in translations.items():
    p_content = f"game/data/i18n/content/{loc}/ui.json"
    p_root = f"game/data/i18n/{loc}.json"
    if os.path.exists(p_content):
        with open(p_content, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in kv.items():
            d[k] = v
        with open(p_content, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p_content}")
    if os.path.exists(p_root):
        with open(p_root, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in kv.items():
            d[k] = v
        with open(p_root, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated {p_root}")

print("i18n sync finished.")
