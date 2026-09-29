#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "星岩鼴鼠": "星岩鼴鼠",
        "鼴鼠": "鼴鼠",
        "星穹高頻等離子重鎚": "星穹高頻等離子重鎚",
        "四葉微型發條天線鑰匙": "四葉微型發條天線鑰匙",
        "圓筒微型冷氣反推噴嘴短尾": "圓筒微型冷氣反推噴嘴短尾",
        "乳白工程塑料合金採礦爪矮萌底盤": "乳白工程塑料合金採礦爪矮萌底盤",
        "防爆聚碳酸酯採礦護目兜帽": "防爆聚碳酸酯採礦護目兜帽",
        "軌道高抗衝擊防護工裝背帶褲": "軌道高抗衝擊防護工裝背帶褲",
        "琥珀點陣LED採礦護目目鏡": "琥珀點陣LED採礦護目目鏡",
    },
    "zh_CN": {
        "星岩鼴鼠": "星岩鼹鼠",
        "鼴鼠": "鼹鼠",
        "星穹高頻等離子重鎚": "星穹高频等离子重锤",
        "四葉微型發條天線鑰匙": "四叶微型发条天线钥匙",
        "圓筒微型冷氣反推噴嘴短尾": "圆筒微型冷气反推喷嘴短尾",
        "乳白工程塑料合金採礦爪矮萌底盤": "乳白工程塑料合金采矿爪矮萌底盘",
        "防爆聚碳酸酯採礦護目兜帽": "防爆聚碳酸酯采矿护目兜帽",
        "軌道高抗衝擊防護工裝背帶褲": "轨道高抗冲击防护工装背带裤",
        "琥珀點陣LED採礦護目目鏡": "琥珀点阵LED采矿护目目镜",
    },
    "en": {
        "星岩鼴鼠": "The Asteroid Mole",
        "鼴鼠": "Mole",
        "星穹高頻等離子重鎚": "Orbital High-Frequency Plasma Sledgehammer",
        "四葉微型發條天線鑰匙": "Four-Vane Antenna Brass Winding Key",
        "圓筒微型冷氣反推噴嘴短尾": "Cylindrical Cold-Gas Reaction Thruster Tail",
        "乳白工程塑料合金採礦爪矮萌底盤": "Milky Polymer Digging Claw Mole Chassis",
        "防爆聚碳酸酯採礦護目兜帽": "Blast-Proof Polycarbonate Mining Visor Cowl",
        "軌道高抗衝擊防護工裝背帶褲": "Orbital Heavy-Duty Sapper Dungarees",
        "琥珀點陣LED採礦護目目鏡": "Amber Dot-Matrix LED Mining Visor Lenses",
    },
    "ja": {
        "星岩鼴鼠": "星岩の土竜 (セイガンのモグラ)",
        "鼴鼠": "モグラ",
        "星穹高頻等離子重鎚": "星穹高周波プラズマスレッジハンマー",
        "四葉微型發條天線鑰匙": "四葉アンテナ黄銅ぜんまい鍵",
        "圓筒微型冷氣反推噴嘴短尾": "円筒微型冷気反推ノズル短尾",
        "乳白工程塑料合金採礦爪矮萌底盤": "乳白エンジニアリングプラスチック採掘爪矮萌素体",
        "防爆聚碳酸酯採礦護目兜帽": "防爆ポリカーボネート採掘バイザーフード",
        "軌道高抗衝擊防護工裝背帶褲": "軌道高耐衝撃サッパーオーバーオール",
        "琥珀點陣LED採礦護目目鏡": "琥珀ドットマトリクスLED採掘バイザーレンズ",
    },
    "ko": {
        "星岩鼴鼠": "성암 두더지",
        "鼴鼠": "두더지",
        "星穹高頻等離子重鎚": "성궁 고주파 플라스마 슬레지해머",
        "四葉微型發條天線鑰匙": "4엽 안테나 황동 태엽 열쇠",
        "圓筒微型冷氣反推噴嘴短尾": "원통형 미세 냉기 역추진 노즐 꼬리",
        "乳白工程塑料合金採礦爪矮萌底盤": "유백색 엔지니어링 플라스틱 채굴 발톱 소체 하판",
        "防爆聚碳酸酯採礦護目兜帽": "방폭 폴리카보네이트 채굴 바이저 두건",
        "軌道高抗衝擊防護工裝背帶褲": "궤도 고충격 방호 멜빵 작업복 바지",
        "琥珀點陣LED採礦護目目鏡": "호박 도트 매트릭스 LED 채굴 바이저 렌즈",
    },
    "es": {
        "星岩鼴鼠": "El Topo Asteroide",
        "鼴鼠": "Topo",
        "星穹高頻等離子重鎚": "Mazo Pesado de Plasma de Alta Frecuencia Orbital",
        "四葉微型發條天線鑰匙": "Llave de Cuerda de Latón con Antena de Cuatro Aspas",
        "圓筒微型冷氣反推噴嘴短尾": "Cola de Boquilla Propulsora de Gas Frío Cilíndrica",
        "乳白工程塑料合金採礦爪矮萌底盤": "Chasis de Topo de Polímero Lechoso con Garras de Minería",
        "防爆聚碳酸酯採礦護目兜帽": "Capucha con Visor de Minería de Policarbonato Antiexplosiones",
        "軌道高抗衝擊防護工裝背帶褲": "Peto de Trabajo de Zapador Orbital de Alto Impacto",
        "琥珀點陣LED採礦護目目鏡": "Lentes con Visor de Minería LED de Matriz de Puntos de Ámbar",
    },
}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_i18n = os.path.join(repo_root, "game/data/i18n/content")

for loc, entries in locales.items():
    ui_path = os.path.join(base_i18n, loc, "ui.json")
    if not os.path.exists(ui_path):
        print(f"File not found: {ui_path}")
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
    print(f"成功更新 {loc}/ui.json，新增 {added} 條目")
