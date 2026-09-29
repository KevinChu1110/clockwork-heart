#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "星環狐猴": "星環狐猴",
        "狐猴": "狐猴",
        "星穹輕量聚合物高機動底盤": "星穹輕量聚合物高機動底盤",
        "星軌冷光雷達耳罩面甲": "星軌冷光雷達耳罩面甲",
        "三環軌道星環黃銅發條鑰匙": "三環軌道星環黃銅發條鑰匙",
        "宇航匿蹤輕量安全吊帶胸甲": "宇航匿蹤輕量安全吊帶胸甲",
        "琥珀脈衝星穹雙目鏡": "琥珀脈衝星穹雙目鏡",
        "星軌脈衝雙鋒短匕": "星軌脈衝雙鋒短匕",
        "多節霓光光纖星環天線尾": "多節霓光光纖星環天線尾",
    },
    "zh_CN": {
        "星環狐猴": "星环狐猴",
        "狐猴": "狐猴",
        "星穹輕量聚合物高機動底盤": "星穹轻量聚合物高机动底盘",
        "星軌冷光雷達耳罩面甲": "星轨冷光雷达耳罩面甲",
        "三環軌道星環黃銅發條鑰匙": "三环轨道星环黄铜发条钥匙",
        "宇航匿蹤輕量安全吊帶胸甲": "宇航匿踪轻量安全吊带胸甲",
        "琥珀脈衝星穹雙目鏡": "琥珀脉冲星穹双目镜",
        "星軌脈衝雙鋒短匕": "星轨脉冲双锋短匕",
        "多節霓光光纖星環天線尾": "多节霓光光纤星环天线尾",
    },
    "en": {
        "星環狐猴": "The Star-Ring Lemur",
        "狐猴": "Lemur",
        "星穹輕量聚合物高機動底盤": "Starfall Lightweight Polymer High-Mobility Chassis",
        "星軌冷光雷達耳罩面甲": "Orbital Luminescent Radar Cowl Mask",
        "三環軌道星環黃銅發條鑰匙": "Tri-Ring Orbit Star-Ring Brass Winding Key",
        "宇航匿蹤輕量安全吊帶胸甲": "Astronaut Stealth Lightweight Safety Harness Cuirass",
        "琥珀脈衝星穹雙目鏡": "Amber Pulsar Starfall Dual Visors",
        "星軌脈衝雙鋒短匕": "Orbital Pulse Twin Daggers",
        "多節霓光光纖星環天線尾": "Segmented Neon Optical Fiber Star-Ring Antenna Tail",
    },
    "ja": {
        "星環狐猴": "星環狐猴 (スターリング・キツネザル)",
        "狐猴": "キツネザル",
        "星穹輕量聚合物高機動底盤": "星穹軽量ポリマー高機動シャーシ",
        "星軌冷光雷達耳罩面甲": "星軌冷光レーダーイヤーマフ面甲",
        "三環軌道星環黃銅發條鑰匙": "三環軌道星環黄銅ぜんまい鍵",
        "宇航匿蹤輕量安全吊帶胸甲": "宇宙潜行軽量安全ハーネス胸甲",
        "琥珀脈衝星穹雙目鏡": "琥珀パルス星穹バイザー",
        "星軌脈衝雙鋒短匕": "星軌パルス双鋒短剣",
        "多節霓光光纖星環天線尾": "多節ネオン光ファイバー星環アンテナ尾",
    },
    "ko": {
        "星環狐猴": "성환 여우원숭이 (스타링 리머)",
        "狐猴": "여우원숭이",
        "星穹輕量聚合物高機動底盤": "성궁 경량 폴리머 고기동 하판",
        "星軌冷光雷達耳罩面甲": "성궤 냉광 레이더 이어머프 면갑",
        "三環軌道星環黃銅發條鑰匙": "3환 궤도 성환 황동 태엽 열쇠",
        "宇航匿蹤輕量安全吊帶胸甲": "우주 은닉 경량 안전 하네스 흉갑",
        "琥珀脈衝星穹雙目鏡": "호박 펄스 성궁 쌍안경",
        "星軌脈衝雙鋒短匕": "성궤 펄스 쌍봉 단검",
        "多節霓光光纖星環天線尾": "다절 네온 광섬유 성환 안테나 꼬리",
    },
    "es": {
        "星環狐猴": "El Lémur de Anillo Estelar",
        "狐猴": "Lémur",
        "星穹輕量聚合物高機動底盤": "Chasis de Alta Movilidad de Polímero Ligero Starfall",
        "星軌冷光雷達耳罩面甲": "Caperuza de Máscara con Orejeras de Radar Luminiscente Orbital",
        "三環軌道星環黃銅發條鑰匙": "Llave de Cuerda de Latón de Anillo Estelar de Órbita de Tres Anillos",
        "宇航匿蹤輕量安全吊帶胸甲": "Peto con Arnés de Seguridad Ligero y Sigiloso de Astronauta",
        "琥珀脈衝星穹雙目鏡": "Visores Dobles de Púlsar de Ámbar de Starfall",
        "星軌脈衝雙鋒短匕": "Dagas Gemelas de Pulso Orbital",
        "多節霓光光纖星環天線尾": "Cola de Antena de Anillo Estelar de Fibra Óptica de Neón Segmentada",
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
