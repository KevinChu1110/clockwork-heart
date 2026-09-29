#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "提線猞猁": "提線猞猁",
        "猞猁": "猞猁",
        "晨曦提線裂空機關爪": "晨曦提線裂空機關爪",
        "雙環八音風鈴黃銅發條鑰匙": "雙環八音風鈴黃銅發條鑰匙",
        "雙節同軸鐘擺平衡配重短尾": "雙節同軸鐘擺平衡配重短尾",
        "提線木偶精雕胡桃木矮萌底盤": "提線木偶精雕胡桃木矮萌底盤",
        "歐風提線雙天線金耳兜帽": "歐風提線雙天線金耳兜帽",
        "晨曦小鎮提線雜技工裝背心": "晨曦小鎮提線雜技工裝背心",
        "雙色翡翠寶石目鏡彩釉面甲": "雙色翡翠寶石目鏡彩釉面甲",
    },
    "zh_CN": {
        "提線猞猁": "提线猞猁",
        "猞猁": "猞猁",
        "晨曦提線裂空機關爪": "晨曦提线裂空机关爪",
        "雙環八音風鈴黃銅發條鑰匙": "双环八音风铃黄铜发条钥匙",
        "雙節同軸鐘擺平衡配重短尾": "双节同轴钟摆平衡配重短尾",
        "提線木偶精雕胡桃木矮萌底盤": "提线木偶精雕胡桃木矮萌底盘",
        "歐風提線雙天線金耳兜帽": "欧风提线双天线金耳兜帽",
        "晨曦小鎮提線雜技工裝背心": "晨曦小镇提线杂技工装背心",
        "雙色翡翠寶石目鏡彩釉面甲": "双色翡翠宝石目镜彩釉面甲",
    },
    "en": {
        "提線猞猁": "The Marionette Lynx",
        "猞猁": "Lynx",
        "晨曦提線裂空機關爪": "Dawn Marionette Steel Claws",
        "雙環八音風鈴黃銅發條鑰匙": "Twin-Ring Chime Brass Winding Key",
        "雙節同軸鐘擺平衡配重短尾": "Twin-Segment Pendulum Bobtail Balance",
        "提線木偶精雕胡桃木矮萌底盤": "Marionette Carved Walnut Chibi Chassis",
        "歐風提線雙天線金耳兜帽": "Euro Marionette Twin-Antenna Golden Ear Cowl",
        "晨曦小鎮提線雜技工裝背心": "Dawn Town Marionette Acrobat Workwear Vest",
        "雙色翡翠寶石目鏡彩釉面甲": "Bicolor Emerald Quartz Eyepiece Glazed Mask",
    },
    "ja": {
        "提線猞猁": "操り人形のオオヤマネコ (マリオネット・オオヤマネコ)",
        "猞猁": "オオヤマネコ",
        "晨曦提線裂空機關爪": "晨曦の糸裂きからくり鉤爪",
        "雙環八音風鈴黃銅發條鑰匙": "二連オルゴール黄銅ぜんまい鍵",
        "雙節同軸鐘擺平衡配重短尾": "二節同軸振り子バランス短尾",
        "提線木偶精雕胡桃木矮萌底盤": "マリオネット彫刻胡桃木矮萌素体",
        "歐風提線雙天線金耳兜帽": "欧風糸操りアンテナ金耳フード",
        "晨曦小鎮提線雜技工裝背心": "晨曦の町マリオネット軽業ベスト",
        "雙色翡翠寶石目鏡彩釉面甲": "双色翡翠水晶レンズ色釉面甲",
    },
    "ko": {
        "提線猞猁": "마리오네트 스라소니",
        "猞猁": "스라소니",
        "晨曦提線裂空機關爪": "새벽 조종실 공파 기믹 클로",
        "雙環八音風鈴黃銅發條鑰匙": "쌍환 오르골 풍경 황동 태엽 열쇠",
        "雙節同軸鐘擺平衡配重短尾": "2절 동축 진자 균형 단미",
        "提線木偶精雕胡桃木矮萌底盤": "마리오네트 정조 호두나무 소체 하판",
        "歐風提線雙天線金耳兜帽": "유럽풍 마리오네트 트윈안테나 금귀 두건",
        "晨曦小鎮提線雜技工裝背心": "새벽마을 마리오네트 곡예 작업 조끼",
        "雙色翡翠寶石目鏡彩釉面甲": "이색 비취 보석 렌즈 채유 면갑",
    },
    "es": {
        "提線猞猁": "El Lince Marioneta",
        "猞猁": "Lince",
        "晨曦提線裂空機關爪": "Garras Mecánicas de Acero de la Marioneta del Alba",
        "雙環八音風鈴黃銅發條鑰匙": "Llave de Cuerda de Latón con Carillón de Doble Anillo",
        "雙節同軸鐘擺平衡配重短尾": "Cola Corta de Péndulo Coaxial de Equilibrio",
        "提線木偶精雕胡桃木矮萌底盤": "Chasis Chibi de Nogal Tallado de Marioneta",
        "歐風提線雙天線金耳兜帽": "Capucha con Orejas Doradas y Doble Antena de Marioneta Europea",
        "晨曦小鎮提線雜技工裝背心": "Chaleco de Trabajo Acróbata de la Marioneta de Villa Alba",
        "雙色翡翠寶石目鏡彩釉面甲": "Máscara Esmaltada con Ocular de Cuarzo Esmeralda Bicolor",
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
