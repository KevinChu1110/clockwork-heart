#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "彩喙巨嘴鳥": "彩喙巨嘴鳥",
        "巨嘴鳥": "巨嘴鳥",
        "林冠輕量化合金素體底盤": "林冠輕量化合金素體底盤",
        "彩晶折光巨嘴面罩": "彩晶折光巨嘴面罩",
        "翡翠石英瞄準目鏡": "翡翠石英瞄準目鏡",
        "蔓谷探險巡林獵裝": "蔓谷探險巡林獵裝",
        "多節沖壓銅片導航尾翼": "多節沖壓銅片導航尾翼",
        "三葉林冠旋翼黃銅發條鑰匙": "三葉林冠旋翼黃銅發條鑰匙",
        "林冠聚能氣動銃": "林冠聚能氣動銃",
    },
    "zh_CN": {
        "彩喙巨嘴鳥": "彩喙巨嘴鸟",
        "巨嘴鳥": "巨嘴鸟",
        "林冠輕量化合金素體底盤": "林冠轻量化合金素体底盘",
        "彩晶折光巨嘴面罩": "彩晶折光巨嘴面罩",
        "翡翠石英瞄準目鏡": "翡翠石英瞄准目镜",
        "蔓谷探險巡林獵裝": "蔓谷探险巡林猎装",
        "多節沖壓銅片導航尾翼": "多节冲压铜片导航尾翼",
        "三葉林冠旋翼黃銅發條鑰匙": "三叶林冠旋翼黄铜发条钥匙",
        "林冠聚能氣動銃": "林冠聚能气动铳",
    },
    "en": {
        "彩喙巨嘴鳥": "The Prism-Bill Toucan",
        "巨嘴鳥": "Toucan",
        "林冠輕量化合金素體底盤": "Canopy Lightweight Alloy Chibi Chassis",
        "彩晶折光巨嘴面罩": "Prism-Bill Brass Visor Cowl",
        "翡翠石英瞄準目鏡": "Emerald Quartz Aiming Monocle",
        "蔓谷探險巡林獵裝": "Vine Valley Scout Workwear Harness",
        "多節沖壓銅片導航尾翼": "Segmented Copper Rudder Navigation Tail",
        "三葉林冠旋翼黃銅發條鑰匙": "Tri-Vane Canopy Rotor Brass Winding Key",
        "林冠聚能氣動銃": "Canopy Prism Pneumatic Arquebus",
    },
    "ja": {
        "彩喙巨嘴鳥": "彩嘴巨嘴鳥 (プリズム・オオハシ)",
        "巨嘴鳥": "オオハシ",
        "林冠輕量化合金素體底盤": "林冠軽量合金矮萌素体",
        "彩晶折光巨嘴面罩": "彩晶折光巨嘴バイザー兜",
        "翡翠石英瞄準目鏡": "翡翠石英照準レンズ面甲",
        "蔓谷探險巡林獵裝": "蔓谷探検巡林ハンターベスト",
        "多節沖壓銅片導航尾翼": "多節プレス銅板ナビゲーション尾羽",
        "三葉林冠旋翼黃銅發條鑰匙": "三葉林冠ローター黄銅ぜんまい鍵",
        "林冠聚能氣動銃": "林冠集能空気動銃",
    },
    "ko": {
        "彩喙巨嘴鳥": "무지개부리 왕부리새 (프리즘 투칸)",
        "巨嘴鳥": "왕부리새",
        "林冠輕量化合金素體底盤": "림관 경량 합금 꼬마 소체 하판",
        "彩晶折光巨嘴面罩": "채정 굴절 왕부리 바이저 두건",
        "翡翠石英瞄準目鏡": "비취 석영 조준 렌즈 면갑",
        "蔓谷探險巡林獵裝": "넝쿨골 탐험 순림 사냥 조끼",
        "多節沖壓銅片導航尾翼": "다절 프레스 동판 내비게이션 미익",
        "三葉林冠旋翼黃銅發條鑰匙": "3엽 림관 로터 황동 태엽 열쇠",
        "林冠聚能氣動銃": "림관 집능 공기압 총",
    },
    "es": {
        "彩喙巨嘴鳥": "El Tucán Pico Iris",
        "巨嘴鳥": "Tucán",
        "林冠輕量化合金素體底盤": "Chasis Chibi de Aleación Ligera del Dosel",
        "彩晶折光巨嘴面罩": "Capucha de Visera de Latón con Pico Prisma",
        "翡翠石英瞄準目鏡": "Monóculo de Puntería de Cuarzo Esmeralda",
        "蔓谷探險巡林獵裝": "Arnés de Explorador del Valle de Enredaderas",
        "多節沖壓銅片導航尾翼": "Cola de Timón de Navegación de Cobre Segmentado",
        "三葉林冠旋翼黃銅發條鑰匙": "Llave de Cuerda de Latón con Rotor del Dosel de Tres Palas",
        "林冠聚能氣動銃": "Arcabuz Neumático de Prisma del Dosel",
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
