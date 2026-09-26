#!/usr/bin/env python3
import json
import os

data_enemy = {
    "zh_TW": {
        "colossus_lion": {"name": "失控發條獅"},
        "colossus_puppet": {"name": "霧鐘提線人偶"},
        "colossus_elephant": {"name": "黑鏽蒸氣巨象"}
    },
    "zh_CN": {
        "colossus_lion": {"name": "失控发条狮"},
        "colossus_puppet": {"name": "雾钟提线人偶"},
        "colossus_elephant": {"name": "黑锈蒸气巨象"}
    },
    "en": {
        "colossus_lion": {"name": "Rampant Clockwork Lion"},
        "colossus_puppet": {"name": "Mistbell Marionette"},
        "colossus_elephant": {"name": "Black-Rust Steam Colossus"}
    },
    "ja": {
        "colossus_lion": {"name": "暴走のぜんまい獅子"},
        "colossus_puppet": {"name": "霧鐘の操り人形"},
        "colossus_elephant": {"name": "黒錆の蒸気巨象"}
    },
    "ko": {
        "colossus_lion": {"name": "폭주 태엽 사자"},
        "colossus_puppet": {"name": "안개종 꼭두각시 인형"},
        "colossus_elephant": {"name": "검은녹 증기 거상"}
    },
    "es": {
        "colossus_lion": {"name": "León de Cuerda Desbocado"},
        "colossus_puppet": {"name": "Marioneta de Reloj de Niebla"},
        "colossus_elephant": {"name": "Coloso de Vapor de Óxido Negro"}
    }
}

translations_ui = {
    "zh_TW": {
        "失控發條獅": "失控發條獅",
        "霧鐘提線人偶": "霧鐘提線人偶",
        "黑鏽蒸氣巨象": "黑鏽蒸氣巨象",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。",
    },
    "zh_CN": {
        "失控發條獅": "失控发条狮",
        "霧鐘提線人偶": "雾钟提线人偶",
        "黑鏽蒸氣巨象": "黑锈蒸气巨象",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "胸膛主簧卡死的黄铜巡游发条狮，板件咬合剧烈震颤，等待卸下过载零件重归平静。",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "白银铰链与黄铜牵引线组装的报时人偶，大钟停摆后齿轮错位，悬空悬臂正狂乱摆动。",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "冷轧钢板与双活塞驱动的重工金属巨象，身嵌黑锈管柱，背部发条嘶鸣着滚烫蒸气。",
    },
    "en": {
        "失控發條獅": "Rampant Clockwork Lion",
        "霧鐘提線人偶": "Mistbell Marionette",
        "黑鏽蒸氣巨象": "Black-Rust Steam Colossus",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "A brass parade clockwork lion with a jammed mainspring; shuddering plates await relief from overloaded parts.",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "A timekeeping marionette of silver hinges and brass cables; gear misalignment flails its hanging arms wildly.",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "A heavy metal elephant driven by rolled steel and dual pistons, fitted with black-rust pipes venting scalding steam.",
    },
    "ja": {
        "失控發條獅": "暴走のぜんまい獅子",
        "霧鐘提線人偶": "霧鐘の操り人形",
        "黑鏽蒸氣巨象": "黒錆の蒸気巨象",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "主ぜんまいが噛み込んだ真鍮の巡行獅子。過負荷パーツを外され静寂を取り戻すのを待っている。",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "銀の蝶番と真鍮ワイヤーで組まれた時報人形。大鐘の停止で歯車が狂い、吊られた腕が乱舞する。",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "冷間圧延鋼板と二連ピストンで動く重工巨象。黒錆のパイプを帯び、背面のぜんまいから熱い蒸気を噴き上げる。",
    },
    "ko": {
        "失控發條獅": "폭주 태엽 사자",
        "霧鐘提線人偶": "안개종 꼭두각시 인형",
        "黑鏽蒸氣巨象": "검은녹 증기 거상",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "메인 태엽이 걸려 멈춘 황동 순회 사자. 과부하 부품을 분해해 평온을 되찾길 기다립니다.",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "은색 힌지와 황동 와이어로 조립된 시보 인형. 대종이 멈춘 후 어긋난 톱니로 매달린 팔이 날뜁니다.",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "압연 강판과 듀얼 피스톤으로 구동되는 중공업 거상. 검은녹 파이프를 두르고 등 뒤의 태엽에서 뜨거운 증기를 뿜어냅니다.",
    },
    "es": {
        "失控發條獅": "León de Cuerda Desbocado",
        "霧鐘提線人偶": "Marioneta de Reloj de Niebla",
        "黑鏽蒸氣巨象": "Coloso de Vapor de Óxido Negro",
        "胸膛主簧卡死的黃銅巡遊發條獅，板件咬合劇烈震顫，等待卸下過載零件重歸平靜。": "Un león de cuerda de latón con el muelle atascado; sus placas vibran esperando retirar piezas sobrecargadas.",
        "白銀鉸鏈與黃銅牽引線組裝的報時人偶，大鐘停擺後齒輪錯位，懸空懸臂正狂亂擺動。": "Una marioneta con bisagras de plata y cables de latón; con el gran reloj parado, sus brazos oscilan sin control.",
        "冷軋鋼板與雙活塞驅動的重工金屬巨象，身嵌黑鏽管柱，背部發條嘶鳴著滾燙蒸氣。": "Un elefante de metal pesado con placas de acero y doble pistón, con tubos de óxido negro que silban vapor ardiente.",
    }
}

# Old keys to clean up
old_keys = [
    "黑鐧蒸汽巨象",
    "冷軋鋼板與雙活塞驅動的重工金屬巨象，手握黑鐧管柱，背部發條嘶鳴著滾燙蒸汽。"
]

# 1. Update enemy.json
for lang, entries in data_enemy.items():
    p = f"game/data/i18n/content/{lang}/enemy.json"
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    for k, v in entries.items():
        d[k] = v
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated enemy: {p}")

# 2. Update content/{loc}/ui.json and {loc}.json
for loc, kv in translations_ui.items():
    p_content = f"game/data/i18n/content/{loc}/ui.json"
    if os.path.exists(p_content):
        with open(p_content, "r", encoding="utf-8") as f:
            d = json.load(f)
        for ok in old_keys:
            d.pop(ok, None)
        for k, v in kv.items():
            d[k] = v
        with open(p_content, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated ui.json: {p_content}")

    p_root = f"game/data/i18n/{loc}.json"
    if os.path.exists(p_root):
        with open(p_root, "r", encoding="utf-8") as f:
            d = json.load(f)
        for ok in old_keys:
            d.pop(ok, None)
        for k, v in kv.items():
            d[k] = v
        with open(p_root, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"Updated root i18n: {p_root}")

print("Sync completed successfully.")
