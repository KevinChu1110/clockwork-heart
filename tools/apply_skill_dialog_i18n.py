import json
import os

root = "/opt/side/bravesoul-game"

translations = {
    "zh_TW": {
        "旅途 · 招式心法": "旅途 · 招式心法",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉",
        "戰鬥優先": "戰鬥優先",
        "平常出招：%s": "平常出招：%s",
        "危急治療：%s": "危急治療：%s",
        "可體悟": "可體悟",
        "未解鎖": "未解鎖",
        "熟練 %d/%d": "熟練 %d/%d",
        "下級預覽：%s": "下級預覽：%s",
        "解鎖條件：%s": "解鎖條件：%s",
        "關閉": "關閉",
        "Lv.%d · 極階": "Lv.%d · 極階",
    },
    "zh_CN": {
        "旅途 · 招式心法": "旅途 · 招式心法",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "铁匠养器 · 星途养魂 · 旅途养招 · 出招随装备武器流转",
        "戰鬥優先": "战斗优先",
        "平常出招：%s": "平时出招：%s",
        "危急治療：%s": "危急治疗：%s",
        "可體悟": "可体悟",
        "未解鎖": "未解锁",
        "熟練 %d/%d": "熟练 %d/%d",
        "下級預覽：%s": "下级预览：%s",
        "解鎖條件：%s": "解锁条件：%s",
        "關閉": "关闭",
        "Lv.%d · 極階": "Lv.%d · 极阶",
    },
    "en": {
        "旅途 · 招式心法": "Journey · Skill Disciplines",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "Forge gear · Nurture souls · Hone skills with your weapon",
        "戰鬥優先": "Battle Priority",
        "平常出招：%s": "Normal: %s",
        "危急治療：%s": "Emergency: %s",
        "可體悟": "Attainable",
        "未解鎖": "Locked",
        "熟練 %d/%d": "Mastery %d/%d",
        "下級預覽：%s": "Next Level: %s",
        "解鎖條件：%s": "Unlock: %s",
        "關閉": "Close",
        "Lv.%d · 極階": "Lv.%d · Mastered",
    },
    "ja": {
        "旅途 · 招式心法": "旅路 · 技の心法",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "鍛冶で器を · 星路で魂を · 旅路で技を磨く",
        "戰鬥優先": "戦闘優先",
        "平常出招：%s": "通常発動：%s",
        "危急治療：%s": "緊急回復：%s",
        "可體悟": "体悟可能",
        "未解鎖": "未解放",
        "熟練 %d/%d": "熟練 %d/%d",
        "下級預覽：%s": "次級予告：%s",
        "解鎖條件：%s": "解放条件：%s",
        "關閉": "閉じる",
        "Lv.%d · 極階": "Lv.%d · 極階",
    },
    "ko": {
        "旅途 · 招式心法": "여정 · 기술 심법",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "대장간에서 장비를 · 별길에서 혼을 · 여정에서 기술을 연마한다",
        "戰鬥優先": "전투 우선",
        "平常出招：%s": "통상 발동: %s",
        "危急治療：%s": "위급 회복: %s",
        "可體悟": "체득 가능",
        "未解鎖": "미해금",
        "熟練 %d/%d": "숙련 %d/%d",
        "下級預覽：%s": "다음 등급 미리보기: %s",
        "解鎖條件：%s": "해금 조건: %s",
        "關閉": "닫기",
        "Lv.%d · 極階": "Lv.%d · 극계",
    },
    "es": {
        "旅途 · 招式心法": "Viaje · Disciplinas de Habilidad",
        "鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉": "Forja equipo · Cultiva almas · Perfecciona habilidades en el camino",
        "戰鬥優先": "Prioridad en combate",
        "平常出招：%s": "Ataque regular: %s",
        "危急治療：%s": "Emergencia: %s",
        "可體悟": "Disponible",
        "未解鎖": "Bloqueado",
        "熟練 %d/%d": "Maestría %d/%d",
        "下級預覽：%s": "Siguiente nivel: %s",
        "解鎖條件：%s": "Desbloqueo: %s",
        "關閉": "Cerrar",
        "Lv.%d · 極階": "Nv.%d · Maestro",
    },
}

for loc, kv in translations.items():
    p = f"{root}/game/data/i18n/content/{loc}/ui.json"
    data = {}
    if os.path.exists(p):
        data = json.load(open(p, encoding="utf-8"))
    for k, v in kv.items():
        data[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(f"Updated {loc}/ui.json with {len(kv)} keys")
