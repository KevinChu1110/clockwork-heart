#!/usr/bin/env python3
"""
更新四區出征關卡名稱、型別與敵方稱號六語系字典
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_TRANSLATIONS = {
    # 1. 關卡型別
    "前哨哨衛": {
        "zh_TW": "前哨哨衛",
        "zh_CN": "前哨哨卫",
        "en": "Outpost Sentry",
        "ja": "前哨の哨兵",
        "ko": "전초 척후병",
        "es": "Centinela de Avanzada",
    },
    "精英機關": {
        "zh_TW": "精英機關",
        "zh_CN": "精英机关",
        "en": "Elite Mechanism",
        "ja": "精鋭からくり",
        "ko": "정예 기계장치",
        "es": "Mecanismo Élite",
    },
    "首領部位破壞": {
        "zh_TW": "首領部位破壞",
        "zh_CN": "首领部位破坏",
        "en": "Boss Part Break",
        "ja": "首領の部位破壊",
        "ko": "보스 부위 파괴",
        "es": "Destrucción de Partes de Jefe",
    },
    # 2. 16 道主線關卡名稱
    "荒路哨站 · 停擺發條鼠": {
        "zh_TW": "荒路哨站 · 停擺發條鼠",
        "zh_CN": "荒路哨站 · 停摆发条鼠",
        "en": "Wasteland Outpost · Stagnant Clockwork Rat",
        "ja": "荒路の哨所 · 停止ぜんまい鼠",
        "ko": "황로 초소 · 멈춰선 태엽 쥐",
        "es": "Puesto del Páramo · Rata de Cuerda Inerte",
    },
    "堡外野原 · 鉚兵哨衛": {
        "zh_TW": "堡外野原 · 鉚兵哨衛",
        "zh_CN": "堡外野原 · 铆兵哨卫",
        "en": "Outer Castle Plain · Riveted Sentry",
        "ja": "城外の野原 · 鋲留め哨兵",
        "ko": "성 밖 들판 · 리벳 척후병",
        "es": "Planicie del Fuerte · Centinela Remachado",
    },
    "堡壘廣場 · 發條機關偶": {
        "zh_TW": "堡壘廣場 · 發條機關偶",
        "zh_CN": "堡垒广场 · 发条机关偶",
        "en": "Fortress Plaza · Clockwork Automaton",
        "ja": "要塞広場 · ぜんまいからくり人形",
        "ko": "요새 광장 · 태엽 기계 인형",
        "es": "Plaza de la Fortaleza · Autómata de Cuerda",
    },
    "閣樓大門 · 重裝發條衛": {
        "zh_TW": "閣樓大門 · 重裝發條衛",
        "zh_CN": "阁楼大门 · 重装发条卫",
        "en": "Attic Gate · Heavy Clockwork Guard",
        "ja": "屋根裏の大門 · 重装ぜんまい衛兵",
        "ko": "다락방 정문 · 중장갑 태엽 경비",
        "es": "Puerta del Ático · Guardia de Cuerda Pesado",
    },
    "白霧外緣 · 守望機關衛": {
        "zh_TW": "白霧外緣 · 守望機關衛",
        "zh_CN": "白雾外缘 · 守望机关卫",
        "en": "White Mist Border · Watch Mechanism Guard",
        "ja": "白霧の外縁 · 見張り機関衛兵",
        "ko": "하얀 안개 변두리 · 망루 기계 경비",
        "es": "Borde de Niebla Blanca · Guardia Mecánico Vigía",
    },
    "市集街道 · 潛伏機關偶": {
        "zh_TW": "市集街道 · 潛伏機關偶",
        "zh_CN": "市集街道 · 潜伏机关偶",
        "en": "Market Street · Lurking Automaton",
        "ja": "市場通り · 潜伏からくり人形",
        "ko": "시장 거리 · 잠복 기계 인형",
        "es": "Calle del Mercado · Autómata Acechante",
    },
    "排水管道 · 黑鏽機關偶": {
        "zh_TW": "排水管道 · 黑鏽機關偶",
        "zh_CN": "排水管道 · 黑锈机关偶",
        "en": "Drainage Conduit · Blight Rust Automaton",
        "ja": "排水管路 · 黒錆からくり人形",
        "ko": "배수관 수로 · 검은 녹 기계 인형",
        "es": "Conducto de Drenaje · Autómata de Óxido Negro",
    },
    "聖獅內殿 · 守衛泰坦雷歐": {
        "zh_TW": "聖獅內殿 · 守衛泰坦雷歐",
        "zh_CN": "圣狮内殿 · 守卫泰坦雷欧",
        "en": "Inner Lion Sanctum · Titan Guardian Leo",
        "ja": "聖獅の内殿 · 守護タイタン・レオ",
        "ko": "성사자 내전 · 수호 타이탄 레오",
        "es": "Santuario del León · Titán Guardián Leo",
    },
    "西林外緣 · 霧影機關偶": {
        "zh_TW": "西林外緣 · 霧影機關偶",
        "zh_CN": "西林外缘 · 雾影机关偶",
        "en": "West Grove Edge · Mist Shadow Automaton",
        "ja": "西林の外縁 · 霧影からくり人形",
        "ko": "서쪽 숲 변두리 · 안개 그림자 기계 인형",
        "es": "Borde del Bosque Oeste · Autómata Sombra de Niebla",
    },
    "霧崖小徑 · 旋風發條偶": {
        "zh_TW": "霧崖小徑 · 旋風發條偶",
        "zh_CN": "雾崖小径 · 旋风发条偶",
        "en": "Mist Cliff Trail · Whirlwind Clockwork Doll",
        "ja": "霧崖の小道 · 旋風ぜんまい人形",
        "ko": "안개 절벽 오솔길 · 회오리 태엽 인형",
        "es": "Sendero del Risco Nublado · Muñeco de Cuerda Torbellino",
    },
    "鏡廊入口 · 鐘擺守衛": {
        "zh_TW": "鏡廊入口 · 鐘擺守衛",
        "zh_CN": "镜廊入口 · 钟摆守卫",
        "en": "Mirror Hall Gate · Pendulum Guardian",
        "ja": "鏡廊の入口 · 振り子守護者",
        "ko": "거울 회랑 입구 · 진자 수호자",
        "es": "Entrada de la Galería de Espejos · Guardián del Péndulo",
    },
    "白霧核心 · 守衛泰坦白狐": {
        "zh_TW": "白霧核心 · 守衛泰坦白狐",
        "zh_CN": "白雾核心 · 守卫泰坦白狐",
        "en": "White Mist Core · Titan Guardian White Fox",
        "ja": "白霧の核心 · 守護タイタン白狐",
        "ko": "하얀 안개 핵 · 수호 타이탄 백호",
        "es": "Núcleo de Niebla Blanca · Titán Guardián Zorro Blanco",
    },
    "石岸潮線 · 破浪哨衛": {
        "zh_TW": "石岸潮線 · 破浪哨衛",
        "zh_CN": "石岸潮线 · 破浪哨卫",
        "en": "Stone Coast Tide Line · Wave-Breaker Sentry",
        "ja": "石岸の潮線 · 破浪の哨兵",
        "ko": "돌 해안 조수선 · 파도 가르기 척후병",
        "es": "Línea de Marea de la Costa Rocosa · Centinela Rompeolas",
    },
    "潮岸沉船 · 舵輪機關衛": {
        "zh_TW": "潮岸沉船 · 舵輪機關衛",
        "zh_CN": "潮岸沉船 · 舵轮机关卫",
        "en": "Tidal Shipwreck · Helm Mechanism Guard",
        "ja": "潮岸の沈船 · 操舵輪機関衛兵",
        "ko": "파도 난파선 · 타륜 기계 경비",
        "es": "Naufragio de la Marea · Guardia Mecánico del Timón",
    },
    "疤地焰徑 · 熔火發條偶": {
        "zh_TW": "疤地焰徑 · 熔火發條偶",
        "zh_CN": "疤地焰径 · 熔火发条偶",
        "en": "Scarland Flame Trail · Molten Clockwork Doll",
        "ja": "傷跡の炎路 · 溶火ぜんまい人形",
        "ko": "흉터 화염길 · 용암 태엽 인형",
        "es": "Sendero de Fuego de la Cicatriz · Muñeco de Cuerda Fundido",
    },
    "通天塔底 · 終境停擺核": {
        "zh_TW": "通天塔底 · 終境停擺核",
        "zh_CN": "通天塔底 · 终境停摆核",
        "en": "Sky-Piercing Tower Base · End-Stasis Core",
        "ja": "通天の塔の底 · 終境の停止核",
        "ko": "통천탑 기슭 · 종경의 정지핵",
        "es": "Base de la Torre Celeste · Núcleo del Éxtasis Final",
    },
    # 3. 16 個敵方稱號（單獨查詢）
    "停擺發條鼠": {
        "zh_TW": "停擺發條鼠",
        "zh_CN": "停摆发条鼠",
        "en": "Stagnant Clockwork Rat",
        "ja": "停止ぜんまい鼠",
        "ko": "멈춰선 태엽 쥐",
        "es": "Rata de Cuerda Inerte",
    },
    "鉚兵哨衛": {
        "zh_TW": "鉚兵哨衛",
        "zh_CN": "铆兵哨卫",
        "en": "Riveted Sentry",
        "ja": "鋲留め哨兵",
        "ko": "리벳 척후병",
        "es": "Centinela Remachado",
    },
    "發條機關偶": {
        "zh_TW": "發條機關偶",
        "zh_CN": "发条机关偶",
        "en": "Clockwork Automaton",
        "ja": "ぜんまいからくり人形",
        "ko": "태엽 기계 인형",
        "es": "Autómata de Cuerda",
    },
    "重裝發條衛": {
        "zh_TW": "重裝發條衛",
        "zh_CN": "重装发条卫",
        "en": "Heavy Clockwork Guard",
        "ja": "重装ぜんまい衛兵",
        "ko": "중장갑 태엽 경비",
        "es": "Guardia de Cuerda Pesado",
    },
    "守望機關衛": {
        "zh_TW": "守望機關衛",
        "zh_CN": "守望机关卫",
        "en": "Watch Mechanism Guard",
        "ja": "見張り機関衛兵",
        "ko": "망루 기계 경비",
        "es": "Guardia Mecánico Vigía",
    },
    "潛伏機關偶": {
        "zh_TW": "潛伏機關偶",
        "zh_CN": "潜伏机关偶",
        "en": "Lurking Automaton",
        "ja": "潜伏からくり人形",
        "ko": "잠복 기계 인형",
        "es": "Autómata Acechante",
    },
    "黑鏽機關偶": {
        "zh_TW": "黑鏽機關偶",
        "zh_CN": "黑锈机关偶",
        "en": "Blight Rust Automaton",
        "ja": "黒錆からくり人形",
        "ko": "검은 녹 기계 인형",
        "es": "Autómata de Óxido Negro",
    },
    "守衛泰坦雷歐": {
        "zh_TW": "守衛泰坦雷歐",
        "zh_CN": "守卫泰坦雷欧",
        "en": "Titan Guardian Leo",
        "ja": "守護タイタン・レオ",
        "ko": "수호 타이탄 레오",
        "es": "Titán Guardián Leo",
    },
    "霧影機關偶": {
        "zh_TW": "霧影機關偶",
        "zh_CN": "雾影机关偶",
        "en": "Mist Shadow Automaton",
        "ja": "霧影からくり人形",
        "ko": "안개 그림자 기계 인형",
        "es": "Autómata Sombra de Niebla",
    },
    "旋風發條偶": {
        "zh_TW": "旋風發條偶",
        "zh_CN": "旋风发条偶",
        "en": "Whirlwind Clockwork Doll",
        "ja": "旋風ぜんまい人形",
        "ko": "회오리 태엽 인형",
        "es": "Muñeco de Cuerda Torbellino",
    },
    "鐘擺守衛": {
        "zh_TW": "鐘擺守衛",
        "zh_CN": "钟摆守卫",
        "en": "Pendulum Guardian",
        "ja": "振り子守護者",
        "ko": "진자 수호자",
        "es": "Guardián del Péndulo",
    },
    "守衛泰坦白狐": {
        "zh_TW": "守衛泰坦白狐",
        "zh_CN": "守卫泰坦白狐",
        "en": "Titan Guardian White Fox",
        "ja": "守護タイタン白狐",
        "ko": "수호 타이탄 백호",
        "es": "Titán Guardián Zorro Blanco",
    },
    "破浪哨衛": {
        "zh_TW": "破浪哨衛",
        "zh_CN": "破浪哨卫",
        "en": "Wave-Breaker Sentry",
        "ja": "破浪の哨兵",
        "ko": "파도 가르기 척후병",
        "es": "Centinela Rompeolas",
    },
    "舵輪機關衛": {
        "zh_TW": "舵輪機關衛",
        "zh_CN": "舵轮机关卫",
        "en": "Helm Mechanism Guard",
        "ja": "操舵輪機関衛兵",
        "ko": "타륜 기계 경비",
        "es": "Guardia Mecánico del Timón",
    },
    "熔火發條偶": {
        "zh_TW": "熔火發條偶",
        "zh_CN": "熔火发条偶",
        "en": "Molten Clockwork Doll",
        "ja": "溶火ぜんまい人形",
        "ko": "용암 태엽 인형",
        "es": "Muñeco de Cuerda Fundido",
    },
    "終境停擺核": {
        "zh_TW": "終境停擺核",
        "zh_CN": "终境停摆核",
        "en": "End-Stasis Core",
        "ja": "終境の停止核",
        "ko": "종경의 정지핵",
        "es": "Núcleo del Éxtasis Final",
    },
}

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

def update_ui_content_json():
    for loc in LOCALES:
        p = os.path.join(BASE_DIR, "game", "data", "i18n", "content", loc, "ui.json")
        data = {}
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        for key, trans in NEW_TRANSLATIONS.items():
            data[key] = trans[loc]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {p} ({len(data)} keys)")

def update_top_level_i18n_json():
    for loc in LOCALES:
        p = os.path.join(BASE_DIR, "game", "data", "i18n", f"{loc}.json")
        data = {}
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        for key, trans in NEW_TRANSLATIONS.items():
            data[key] = trans[loc]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Updated {p} ({len(data)} keys)")

if __name__ == "__main__":
    update_ui_content_json()
    update_top_level_i18n_json()
    print("Done!")
