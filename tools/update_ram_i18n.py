#!/usr/bin/env python3
"""為第二十九族星盤靈羊 (The Astral Ram, ram) 於六語系 ui.json 建立名稱與頭銜佔位詞條。
依據 docs/design/ASTRAL_RAM_DESIGN_PROPOSAL.md 第九節六語系在地化對照表。
"""

import json
import os

locales = {
    "zh_TW": {
        "星盤靈羊": "星盤靈羊",
        "靈羊": "靈羊",
        "星軌漫步者引力法袍": "星軌漫步者引力法袍",
        "星軌游絲共鳴杖": "星軌游絲共鳴杖",
        "星盤三叉星芒發條鑰匙": "星盤三叉星芒發條鑰匙",
        "雙螺旋發條游絲盤角面甲": "雙螺旋發條游絲盤角面甲",
        "星光琥珀金色點陣LED目鏡": "星光琥珀金色點陣LED目鏡",
        "懸浮反重力星環儀": "懸浮反重力星環儀",
    },
    "zh_CN": {
        "星盤靈羊": "星盘灵羊",
        "靈羊": "灵羊",
        "星軌漫步者引力法袍": "星轨漫步者引力法袍",
        "星軌游絲共鳴杖": "星轨游丝共鸣杖",
        "星盤三叉星芒發條鑰匙": "星盘三叉星芒发条钥匙",
        "雙螺旋發條游絲盤角面甲": "双螺旋发条游丝盘角面甲",
        "星光琥珀金色點陣LED目鏡": "星光琥珀金色点阵LED目镜",
        "懸浮反重力星環儀": "悬浮反重力星环仪",
    },
    "en": {
        "星盤靈羊": "The Astral Ram",
        "靈羊": "Ram",
        "星軌漫步者引力法袍": "Astro-Starlight Gravity Robe",
        "星軌游絲共鳴杖": "Astral Spiral Resonance Staff",
        "星盤三叉星芒發條鑰匙": "Astrolabe Tri-Star Winding Key",
        "雙螺旋發條游絲盤角面甲": "Spiral Balance Spring Horn Visor",
        "星光琥珀金色點陣LED目鏡": "Starlight Amber Dot-Matrix LED Optics",
        "懸浮反重力星環儀": "Floating Gravitational Orbit Rings",
    },
    "ja": {
        "星盤靈羊": "アストラル・ラム (霊羊)",
        "靈羊": "霊羊",
        "星軌漫步者引力法袍": "星軌の引力法衣",
        "星軌游絲共鳴杖": "星軌のヒゲゼンマイ共鳴杖",
        "星盤三叉星芒發條鑰匙": "アストロラーベ三叉星のぜんまい鍵",
        "雙螺旋發條游絲盤角面甲": "二重渦巻ヒゲゼンマイ角面甲",
        "星光琥珀金色點陣LED目鏡": "星光琥珀ドットマトリクスLEDアイ",
        "懸浮反重力星環儀": "浮遊反重力オービットリング",
    },
    "ko": {
        "星盤靈羊": "아스트랄 램 (성반영양)",
        "靈羊": "영양",
        "星軌漫步者引力法袍": "성궤 중력 법의",
        "星軌游絲共鳴杖": "성궤 헤어스프링 공명 지팡이",
        "星盤三叉星芒發條鑰匙": "아스트롤라베 삼차 성망의 태엽 열쇠",
        "雙螺旋發條游絲盤角面甲": "이중 나선 헤어스프링 뿔 면갑",
        "星光琥珀金色點陣LED目鏡": "별빛 호박색 도트 매트릭스 LED 눈",
        "懸浮反重力星環儀": "부유 반중력 궤도 링",
    },
    "es": {
        "星盤靈羊": "El Carnero Astral",
        "靈羊": "Carnero",
        "星軌漫步者引力法袍": "Túnica de Gravedad Astral",
        "星軌游絲共鳴杖": "Bastón de Resonancia Espiral Astral",
        "星盤三叉星芒發條鑰匙": "Llave de Cuerda Tri-Estrella del Astrolabio",
        "雙螺旋發條游絲盤角面甲": "Visera de Cuernos de Espiral de Balance",
        "星光琥珀金色點陣LED目鏡": "Óptica LED de Matriz de Puntos Ámbar Luz Estelar",
        "懸浮反重力星環儀": "Anillos Orbitales Antigravitatorios Flotantes",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"檔案不存在: {ui_path}")
        continue
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, v in entries.items():
        if k not in data:
            data[k] = v
            added += 1
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[{loc}] 更新 {ui_path} (新增 {added} 條)")
