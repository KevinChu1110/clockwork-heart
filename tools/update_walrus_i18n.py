#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "破冰海象": "破冰海象",
        "海象": "海象",
        "深淵耐壓鍍鈦合金底盤": "深淵耐壓鍍鈦合金底盤",
        "雙聯鎢鋼破冰長牙面罩": "雙聯鎢鋼破冰長牙面罩",
        "雙葉海錨輪轂黃銅發條鑰匙": "雙葉海錨輪轂黃銅發條鑰匙",
        "深淵領航雙排扣水手胸甲": "深淵領航雙排扣水手胸甲",
        "雙聯耐壓石英泡罩目鏡": "雙聯耐壓石英泡罩目鏡",
        "深淵破冰海軍短闊劍": "深淵破冰海軍短闊劍",
        "雙聯減壓壓載氣箱與防鏽油壺": "雙聯減壓壓載氣箱與防鏽油壺",
    },
    "zh_CN": {
        "破冰海象": "破冰海象",
        "海象": "海象",
        "深淵耐壓鍍鈦合金底盤": "深渊耐压镀钛合金底盘",
        "雙聯鎢鋼破冰長牙面罩": "双联钨钢破冰长牙面罩",
        "雙葉海錨輪轂黃銅發條鑰匙": "双叶海锚轮毂黄铜发条钥匙",
        "深淵領航雙排扣水手胸甲": "深渊领航双排扣水手胸甲",
        "雙聯耐壓石英泡罩目鏡": "双联耐压石英泡罩目镜",
        "深淵破冰海軍短闊劍": "深渊破冰海军短阔剑",
        "雙聯減壓壓載氣箱與防鏽油壺": "双联减压压载气箱与防锈油壶",
    },
    "en": {
        "破冰海象": "The Icebreaker Walrus",
        "海象": "Walrus",
        "深淵耐壓鍍鈦合金底盤": "Abyssal Pressure-Resistant Titanium Alloy Chassis",
        "雙聯鎢鋼破冰長牙面罩": "Dual Tungsten Icebreaker Tusk Cowl",
        "雙葉海錨輪轂黃銅發條鑰匙": "Dual-Fluke Anchor Handwheel Brass Key",
        "深淵領航雙排扣水手胸甲": "Abyssal Pilot Double-Breasted Sailor Cuirass",
        "雙聯耐壓石英泡罩目鏡": "Dual Pressure-Resistant Quartz Bubble Eyepieces",
        "深淵破冰海軍短闊劍": "Abyssal Icebreaker Naval Cutlass",
        "雙聯減壓壓載氣箱與防鏽油壺": "Dual Decompression Ballast Tanks & Rust-Proof Oil Flask",
    },
    "ja": {
        "破冰海象": "破氷海象 (アイスブレイカー・ウォルラス)",
        "海象": "セイウチ",
        "深淵耐壓鍍鈦合金底盤": "深淵耐圧チタンメッキ合金シャーシ",
        "雙聯鎢鋼破冰長牙面罩": "連装タングステン破氷牙バイザー",
        "雙葉海錨輪轂黃銅發條鑰匙": "双葉海錨ホイール黄銅ぜんまい鍵",
        "深淵領航雙排扣水手胸甲": "深淵航海ダブルブレスト水兵胸甲",
        "雙聯耐壓石英泡罩目鏡": "連装耐圧石英バブルゴーグル",
        "深淵破冰海軍短闊劍": "深淵破氷海軍短幅広剣",
        "雙聯減壓壓載氣箱與防鏽油壺": "連装減圧バラストタンクと防錆油壺",
    },
    "ko": {
        "破冰海象": "쇄빙 바다코끼리 (아이스브레이커 월러스)",
        "海象": "바다코끼리",
        "深淵耐壓鍍鈦合金底盤": "심연 내압 티타늄 도금 합금 하판",
        "雙聯鎢鋼破冰長牙面罩": "2연장 텅스텐 쇄빙 상아 면갑",
        "雙葉海錨輪轂黃銅發條鑰匙": "쌍엽 해묘 휠 황동 태엽 열쇠",
        "深淵領航雙排扣水手胸甲": "심연 항해 더블버튼 수병 흉갑",
        "雙聯耐壓石英泡罩目鏡": "2연장 내압 석영 버블 안경",
        "深淵破冰海軍短闊劍": "심연 쇄빙 해군 숏 브로드소드",
        "雙聯減壓壓載氣箱與防鏽油壺": "2연장 감압 밸러스트 공기탱크와 방청 기름병",
    },
    "es": {
        "破冰海象": "La Morsa Rompehielos",
        "海象": "Morsa",
        "深淵耐壓鍍鈦合金底盤": "Chasis de Aleación de Titanio Resistente a la Presión Abisal",
        "雙聯鎢鋼破冰長牙面罩": "Caperuza de Colmillos de Tungsteno Rompehielos Doble",
        "雙葉海錨輪轂黃銅發條鑰匙": "Llave de Cuerda de Latón con Rueda de Ancla de Dos Palas",
        "深淵領航雙排扣水手胸甲": "Coraza de Marinero de Doble Botonadura de Navegación Abisal",
        "雙聯耐壓石英泡罩目鏡": "Gafas de Burbuja de Cuarzo Resistentes a la Presión Doble",
        "深淵破冰海軍短闊劍": "Alfanje Naval Rompehielos Abisal",
        "雙聯減壓壓載氣箱與防鏽油壺": "Tanques Dobles de Lastre de Descompresión y Frasco de Aceite Antioxidante",
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
