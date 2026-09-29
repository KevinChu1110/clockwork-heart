#!/usr/bin/env python3
import json
import os

locales = {
    "zh_TW": {
        "破竹羚牛": "破竹羚牛",
        "羚牛": "羚牛",
        "青古銅鑄鐵重裝底盤": "青古銅鑄鐵重裝底盤",
        "黃銅反曲扭角重盔": "黃銅反曲扭角重盔",
        "三葉天元雕花黃銅發條鑰匙": "三葉天元雕花黃銅發條鑰匙",
        "天元拓荒道袍重肩甲": "天元拓荒道袍重肩甲",
        "翡翠石英耐震雙目鏡": "翡翠石英耐震雙目鏡",
        "天元破竹開山巨斧": "天元破竹開山巨斧",
        "雙聯竹露油壺減震閥": "雙聯竹露油壺減震閥",
    },
    "zh_CN": {
        "破竹羚牛": "破竹羚牛",
        "羚牛": "羚牛",
        "青古銅鑄鐵重裝底盤": "青古铜铸铁重装底盘",
        "黃銅反曲扭角重盔": "黄铜反曲扭角重盔",
        "三葉天元雕花黃銅發條鑰匙": "三叶天元雕花黄铜发条钥匙",
        "天元拓荒道袍重肩甲": "天元拓荒道袍重肩甲",
        "翡翠石英耐震雙目鏡": "翡翠石英耐震双目镜",
        "天元破竹開山巨斧": "天元破竹开山巨斧",
        "雙聯竹露油壺減震閥": "双联竹露油壶减震阀",
    },
    "en": {
        "破竹羚牛": "The Bamboo-Cleaving Takin",
        "羚牛": "Takin",
        "青古銅鑄鐵重裝底盤": "Antique Bronze Cast Iron Heavy Chassis",
        "黃銅反曲扭角重盔": "Brass Recurve Twisted Horn Cowl",
        "三葉天元雕花黃銅發條鑰匙": "Tri-Leaf Zen Carved Brass Winding Key",
        "天元拓荒道袍重肩甲": "Zen Pioneer Heavy Robe Pauldrons",
        "翡翠石英耐震雙目鏡": "Emerald Quartz Shock-Resistant Visors",
        "天元破竹開山巨斧": "Zen Bamboo-Cleaving Great Axe",
        "雙聯竹露油壺減震閥": "Dual Bamboo Dew Oil Flask Shock Valve",
    },
    "ja": {
        "破竹羚牛": "破竹羚牛 (バンブークリーヴィング・ターキン)",
        "羚牛": "ターキン",
        "青古銅鑄鐵重裝底盤": "青古銅鋳鉄重装シャーシ",
        "黃銅反曲扭角重盔": "黄銅反曲ねじれ角重兜",
        "三葉天元雕花黃銅發條鑰匙": "三葉天元彫刻黄銅ぜんまい鍵",
        "天元拓荒道袍重肩甲": "天元開拓道服重肩甲",
        "翡翠石英耐震雙目鏡": "翡翠石英耐震バイザー",
        "天元破竹開山巨斧": "天元破竹開山巨斧",
        "雙聯竹露油壺減震閥": "連装竹露油壺減震バルブ",
    },
    "ko": {
        "破竹羚牛": "파죽 영양 (뱀부 클리빙 타킨)",
        "羚牛": "타킨",
        "青古銅鑄鐵重裝底盤": "청고동 주철 중장갑 하판",
        "黃銅反曲扭角重盔": "황동 반곡 뒤틀린 뿔 투구",
        "三葉天元雕花黃銅發條鑰匙": "3엽 천원 조각 황동 태엽 열쇠",
        "天元拓荒道袍重肩甲": "천원 개척 도포 중견갑",
        "翡翠石英耐震雙目鏡": "비취 석영 내진 안경",
        "天元破竹開山巨斧": "천원 파죽 개산 거대도끼",
        "雙聯竹露油壺減震閥": "2연장 죽로 기름병 감진 밸브",
    },
    "es": {
        "破竹羚牛": "El Takín Rompebambú",
        "羚牛": "Takín",
        "青古銅鑄鐵重裝底盤": "Chasis Pesado de Fundición de Bronce Antiguo",
        "黃銅反曲扭角重盔": "Caperuza Pesada de Cuernos Retorcidos Recurvados de Latón",
        "三葉天元雕花黃銅發條鑰匙": "Llave de Cuerda de Latón Tallada Zen de Tres Palas",
        "天元拓荒道袍重肩甲": "Hombreras Pesadas de Túnica de Pionero Zen",
        "翡翠石英耐震雙目鏡": "Visores Antivibración de Cuarzo Esmeralda",
        "天元破竹開山巨斧": "Gran Hacha Rompebambú Zen",
        "雙聯竹露油壺減震閥": "Válvula Amortiguadora de Frasco de Aceite de Rocío de Bambú Doble",
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
