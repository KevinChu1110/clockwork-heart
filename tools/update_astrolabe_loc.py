#!/usr/bin/env python3
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "game/data/i18n/content")
LOCALES = ("zh_CN", "en", "ja", "ko", "es")

STALE_KEYS = [
    "星盤偏了一角，像在等傭兵團最弱的那個。",
    "暴擊 ",
    "木人樁身上全是橫痕。啄木鳥式的戳，一刀都沒留下。",
]

TRANSLATIONS = {
    # 木人樁
    "[color=#6f6]木人試招完成！[/color]": {
        "zh_CN": "[color=#6f6]木人试招完成！[/color]",
        "en": "[color=#6f6]Training Dummy Trial Complete![/color]",
        "ja": "[color=#6f6]木人試技完了！[/color]",
        "ko": "[color=#6f6]목인 연습 완료![/color]",
        "es": "[color=#6f6]¡Prueba de muñeco completada![/color]",
    },
    "[color=#fc8]試招結束。[/color]": {
        "zh_CN": "[color=#fc8]试招结束。[/color]",
        "en": "[color=#fc8]Trial ended.[/color]",
        "ja": "[color=#fc8]試技終了。[/color]",
        "ko": "[color=#fc8]연습 종료.[/color]",
        "es": "[color=#fc8]Prueba finalizada.[/color]",
    },
    "手遊大廳 (Lobby)": {
        "zh_CN": "手游大厅 (Lobby)",
        "en": "Mobile Lobby",
        "ja": "ロビー (Lobby)",
        "ko": "모바일 로비 (Lobby)",
        "es": "Lobby Móvil",
    },
    "木人樁": {
        "zh_CN": "木人桩",
        "en": "Training Dummy",
        "ja": "木人",
        "ko": "목인",
        "es": "Muñeco de entrenamiento",
    },
    "木人樁不反擊 · 自由試刀 · 右上可結束": {
        "zh_CN": "木人桩不反击 · 自由试刀 · 右上可结束",
        "en": "Dummy does not counter · Free practice · Exit via top-right",
        "ja": "木人は反撃しない · 自由試技 · 右上で終了可能",
        "ko": "목인은 반격하지 않음 · 자유 연습 · 우측 상단에서 종료",
        "es": "El muñeco no contraataca · Práctica libre · Salir arriba a la derecha",
    },
    "木人樁立在場中，木質堅實。正好用來試試招式與身手。": {
        "zh_CN": "木人桩立在场中，木质坚实。正好用来试试招式与身手。",
        "en": "A sturdy wooden dummy stands in the center, perfect for honing skills.",
        "ja": "広場に立つ堅牢な木人。技や身のこなしを試すのに打って付けだ。",
        "ko": "마당에 단단한 목인이 서 있다. 기술과 솜씨를 시험하기에 제격이다.",
        "es": "Un robusto muñeco de madera en el centro, ideal para probar técnicas.",
    },
    "木人樁：靜止不動，供武者試招。": {
        "zh_CN": "木人桩：静止不动，供武者试招。",
        "en": "Training Dummy: Stands still for martial practice.",
        "ja": "木人：静止したまま武者の試技を受ける。",
        "ko": "목인: 움직이지 않고 무사의 연습을 받는다.",
        "es": "Muñeco de madera: Inmóvil, para que los guerreros practiquen.",
    },
    "木人試招：木人不會還手 · 測試出招節奏與技能傷害 · 隨時可按右上結束": {
        "zh_CN": "木人试招：木人不会还手 · 测试出招节奏与技能伤害 · 随时可按右上结束",
        "en": "Dummy Trial: Dummy won't fight back · Test rhythm and skill damage · Exit anytime top-right",
        "ja": "木人試技：反撃なし · 攻撃リズムと技威力の検証 · 右上でいつでも終了",
        "ko": "목인 연습: 반격 없음 · 공격 리듬과 스킬 피해 시험 · 언제든 우상단에서 종료",
        "es": "Prueba de muñeco: Sin contraataques · Prueba ritmo y daño · Sal arriba a la derecha",
    },
    "結束試招": {
        "zh_CN": "结束试招",
        "en": "End Trial",
        "ja": "試技終了",
        "ko": "연습 종료",
        "es": "Terminar prueba",
    },
    "試招完成": {
        "zh_CN": "试招完成",
        "en": "Trial Complete",
        "ja": "試技完了",
        "ko": "연습 완료",
        "es": "Prueba completada",
    },
    "試招結束": {
        "zh_CN": "试招结束",
        "en": "Trial Ended",
        "ja": "試技終了",
        "ko": "연습 종료",
        "es": "Prueba terminada",
    },

    # 星盤調查
    "[color=#a0a8c0]「星盤偏了一角，像在等傭兵團最弱的那個。」[/color]": {
        "zh_CN": "[color=#a0a8c0]「星盘偏了一角，像在等佣兵团最弱的那个。」[/color]",
        "en": "[color=#a0a8c0]\"The star chart tilts a corner, as if waiting for the company's weakest.\"[/color]",
        "ja": "[color=#a0a8c0]「星盤が一角傾いている。傭兵団で一番弱い者を待つように。」[/color]",
        "ko": "[color=#a0a8c0]「성반이 한쪽으로 기울었다. 용병단 제일 약한 놈을 기다리듯.」[/color]",
        "es": "[color=#a0a8c0]\"La carta estelar se inclina en una esquina, como esperando al más débil de la compañía.\"[/color]",
    },
    "[b]聚魂殿 · 周天星盤[/b]": {
        "zh_CN": "[b]聚魂殿 · 周天星盘[/b]",
        "en": "[b]Soul Hall · Celestial Astrolabe[/b]",
        "ja": "[b]聚魂殿 · 周天星盤[/b]",
        "ko": "[b]취혼전 · 주천성반[/b]",
        "es": "[b]Salón del Alma · Astrolabio Celestial[/b]",
    },
    "聚魂殿 · 周天星盤": {
        "zh_CN": "聚魂殿 · 周天星盘",
        "en": "Soul Hall · Celestial Astrolabe",
        "ja": "聚魂殿 · 周天星盤",
        "ko": "취혼전 · 주천성반",
        "es": "Salón del Alma · Astrolabio Celestial",
    },
    "周天星盤": {
        "zh_CN": "周天星盘",
        "en": "Celestial Astrolabe",
        "ja": "周天星盤",
        "ko": "주천성반",
        "es": "Astrolabio Celestial",
    },
    "聚魂儀式": {
        "zh_CN": "聚魂仪式",
        "en": "Soul Ritual",
        "ja": "聚魂の儀",
        "ko": "취혼 의식",
        "es": "Ritual de Alma",
    },
    "重整星象": {
        "zh_CN": "重整星象",
        "en": "Refresh Chart",
        "ja": "星象更新",
        "ko": "성상 갱신",
        "es": "Actualizar Carta",
    },
    "離開星盤": {
        "zh_CN": "离开星盘",
        "en": "Leave Astrolabe",
        "ja": "星盤を離れる",
        "ko": "성반 떠나기",
        "es": "Dejar Astrolabio",
    },
    "星盤點亮：%d / %d 主星 · 持有戰魂 %d 顆（入魂 %d，背包 %d）": {
        "zh_CN": "星盘点亮：%d / %d 主星 · 持有战魂 %d 颗（入魂 %d，背包 %d）",
        "en": "Astrolabe Lit: %d / %d Stars · Souls Held: %d (Equipped %d, Bag %d)",
        "ja": "星盤点灯：%d / %d 主星 · 所持戦魂 %d 個（装備 %d、鞄 %d）",
        "ko": "성반 점등: %d / %d 주성 · 보유 전혼 %d 개（장착 %d, 가방 %d）",
        "es": "Astrolabio Iluminado: %d / %d Estrellas · Almas: %d (Equipadas %d, Mochila %d)",
    },
    "[b]數值傾向分布[/b]": {
        "zh_CN": "[b]数值倾向分布[/b]",
        "en": "[b]Stat Inclination Distribution[/b]",
        "ja": "[b]能力傾向分布[/b]",
        "ko": "[b]능력치 경향 분포[/b]",
        "es": "[b]Distribución de Inclinación de Estadísticas[/b]",
    },
    "  全能均衡：%d / %d 星點亮（紫微）": {
        "zh_CN": "  全能均衡：%d / %d 星点亮（紫微）",
        "en": "  Balanced: %d / %d Stars Lit (Polaris)",
        "ja": "  全能均衡：%d / %d 星点灯（紫微）",
        "ko": "  만능 균형: %d / %d 성 점등 (자미)",
        "es": "  Equilibrado: %d / %d Estrellas Iluminadas (Polaris)",
    },
    "  攻擊偏向：%d / %d 星點亮（天機、太陽、武曲、廉貞、巨門、七殺、破軍）": {
        "zh_CN": "  攻击偏向：%d / %d 星点亮（天机、太阳、武曲、廉贞、巨门、七杀、破军）",
        "en": "  Attack Bias: %d / %d Stars Lit (Tianji, Sun, Wuqu, Lianzhen, Jumen, Qisha, Pojun)",
        "ja": "  攻撃傾向：%d / %d 星点灯（天機、太陽、武曲、廉貞、巨門、七殺、破軍）",
        "ko": "  공격 경향: %d / %d 성 점등 (천기, 태양, 무곡, 염정, 거문, 칠살, 파군)",
        "es": "  Sesgo Ataque: %d / %d Estrellas Iluminadas (Tianji, Sol, Wuqu, Lianzhen, Jumen, Qisha, Pojun)",
    },
    "  防禦偏向：%d / %d 星點亮（天府、天相、天梁）": {
        "zh_CN": "  防御偏向：%d / %d 星点亮（天府、天相、天梁）",
        "en": "  Defense Bias: %d / %d Stars Lit (Tianfu, Tianxiang, Tianliang)",
        "ja": "  防御傾向：%d / %d 星点灯（天府、天相、天梁）",
        "ko": "  방어 경향: %d / %d 성 점등 (천부, 천상, 천량)",
        "es": "  Sesgo Defensa: %d / %d Estrellas Iluminadas (Tianfu, Tianxiang, Tianliang)",
    },
    "  氣血偏向：%d / %d 星點亮（天同、太陰、貪狼）": {
        "zh_CN": "  气血偏向：%d / %d 星点亮（天同、太阴、贪狼）",
        "en": "  HP Bias: %d / %d Stars Lit (Tiantong, Moon, Tanlang)",
        "ja": "  気血傾向：%d / %d 星点灯（天同、太陰、貪狼）",
        "ko": "  생명 경향: %d / %d 성 점등 (천동, 태음, 탐랑)",
        "es": "  Sesgo Vitalidad: %d / %d Estrellas Iluminadas (Tiantong, Luna, Tanlang)",
    },
    "[b]紫微十四主星盤點[/b]": {
        "zh_CN": "[b]紫微十四主星盘点[/b]",
        "en": "[b]Ziwei 14 Main Stars Survey[/b]",
        "ja": "[b]紫微十四主星総覧[/b]",
        "ko": "[b]자미 14 주성 목록[/b]",
        "es": "[b]Inventario de las 14 Estrellas Principales de Ziwei[/b]",
    },
    "[已點亮]": {
        "zh_CN": "[已点亮]",
        "en": "[Lit]",
        "ja": "[点灯]",
        "ko": "[점등]",
        "es": "[Iluminada]",
    },
    "[未點亮]": {
        "zh_CN": "[未点亮]",
        "en": "[Dim]",
        "ja": "[消灯]",
        "ko": "[소등]",
        "es": "[Apagada]",
    },
    "全能均衡": {
        "zh_CN": "全能均衡",
        "en": "Balanced",
        "ja": "全能均衡",
        "ko": "만능 균형",
        "es": "Equilibrado",
    },
    "攻擊偏向": {
        "zh_CN": "攻击偏向",
        "en": "Attack Bias",
        "ja": "攻撃傾向",
        "ko": "공격 경향",
        "es": "Sesgo Ataque",
    },
    "防禦偏向": {
        "zh_CN": "防御偏向",
        "en": "Defense Bias",
        "ja": "防御傾向",
        "ko": "방어 경향",
        "es": "Sesgo Defensa",
    },
    "氣血偏向": {
        "zh_CN": "气血偏向",
        "en": "HP Bias",
        "ja": "気血傾向",
        "ko": "생명 경향",
        "es": "Sesgo Vitalidad",
    },
    "（持有 %d 顆 · 最高 %s %s）": {
        "zh_CN": "（持有 %d 颗 · 最高 %s %s）",
        "en": "(Held: %d · Highest: %s %s)",
        "ja": "（所持 %d 個 · 最高 %s %s）",
        "ko": "（보유 %d 개 · 최고 %s %s）",
        "es": "(Posee %d · Máx: %s %s)",
    },
    "（未感應）": {
        "zh_CN": "（未感应）",
        "en": "(Unattuned)",
        "ja": "（未感応）",
        "ko": "（미감응）",
        "es": "(Sin sintonizar)",
    },
    "[b]秘境異曜[/b]": {
        "zh_CN": "[b]秘境异曜[/b]",
        "en": "[b]Secret Relic Stars[/b]",
        "ja": "[b]秘境異曜[/b]",
        "ko": "[b]비경 이요[/b]",
        "es": "[b]Estrellas de Reliquia Secreta[/b]",
    },
}

for loc in LOCALES:
    path = os.path.join(CONTENT, loc, "ui.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Remove stale keys
    for sk in STALE_KEYS:
        data.pop(sk, None)

    # Add translations
    for src_k, trans_map in TRANSLATIONS.items():
        if loc in trans_map:
            data[src_k] = trans_map[loc]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("Updated ui.json across all 5 locales successfully!")
