#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新背包物品欄六語系詞條至 game/data/i18n/content/<locale>/ui.json
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
I18N_DIR = BASE_DIR / "game" / "data" / "i18n" / "content"

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

ENTRIES = {
    "物品欄": {
        "zh_TW": "物品欄",
        "zh_CN": "物品栏",
        "en": "Inventory",
        "ja": "インベントリ",
        "ko": "소지품",
        "es": "Inventario",
    },
    "冒險者背包 · 點選格子查看詳情": {
        "zh_TW": "冒險者背包 · 點選格子查看詳情",
        "zh_CN": "冒险者背包 · 点击格子查看详情",
        "en": "Adventurer's Bag · Tap slot to view details",
        "ja": "冒険者のバッグ · マスをタップして詳細確認",
        "ko": "모험가의 배낭 · 슬롯을 눌러 상세 확인",
        "es": "Bolsa de aventurero · Toca una casilla para ver detalles",
    },
    "冒險者背包": {
        "zh_TW": "冒險者背包",
        "zh_CN": "冒险者背包",
        "en": "Adventurer's Bag",
        "ja": "冒険者のバッグ",
        "ko": "모험가의 배낭",
        "es": "Bolsa de aventurero",
    },
    "使用 / 賣出": {
        "zh_TW": "使用 / 賣出",
        "zh_CN": "使用 / 出售",
        "en": "Use / Sell",
        "ja": "使う / 売却",
        "ko": "사용 / 판매",
        "es": "Usar / Vender",
    },
    "放到快捷欄": {
        "zh_TW": "放到快捷欄",
        "zh_CN": "放入快捷栏",
        "en": "Assign to Hotbar",
        "ja": "ショートカットに登録",
        "ko": "단축칸에 등록",
        "es": "Asignar a acceso rápido",
    },
    "左鍵點選查看 · 雙擊或右鍵快速使用": {
        "zh_TW": "左鍵點選查看 · 雙擊或右鍵快速使用",
        "zh_CN": "左键点击查看 · 双击或右键快速使用",
        "en": "Click to view · Double-click or right-click to quick use",
        "ja": "クリックで確認 · ダブルクリックか右クリックで即時使用",
        "ko": "클릭하여 확인 · 더블 클릭 또는 우클릭으로 빠른 사용",
        "es": "Clic para ver · Doble clic o clic derecho para uso rápido",
    },
    "請點選左側格子查看道具詳情。": {
        "zh_TW": "請點選左側格子查看道具詳情。",
        "zh_CN": "请点击左侧格子查看道具详情。",
        "en": "Please select a slot on the left to view item details.",
        "ja": "左側のマスを選択して道具の詳細を確認してください。",
        "ko": "왼쪽 슬롯을 선택하여 아이템 상세를 확인하세요.",
        "es": "Selecciona una casilla de la izquierda para ver los detalles del objeto.",
    },
    "消耗品：使用回復狀態": {
        "zh_TW": "消耗品：使用回復狀態",
        "zh_CN": "消耗品：使用恢复状态",
        "en": "Consumable: Use to restore stats",
        "ja": "消耗品：使用して状態を回復",
        "ko": "소모품: 사용하여 상태 회복",
        "es": "Consumible: Usar para recuperar estado",
    },
    "素材：點擊使用可賣出金幣": {
        "zh_TW": "素材：點擊使用可賣出金幣",
        "zh_CN": "素材：点击使用可出售金币",
        "en": "Material: Click use to sell for gold",
        "ja": "素材：使うをクリックしてゴールドで売却",
        "ko": "재료: 사용을 눌러 골드로 판매",
        "es": "Material: Pulsa usar para vender por oro",
    },
    "重要物：劇情關鍵道具": {
        "zh_TW": "重要物：劇情關鍵道具",
        "zh_CN": "重要物：剧情关键道具",
        "en": "Key Item: Story-critical item",
        "ja": "重要品：ストーリー重要アイテム",
        "ko": "중요 아이템: 스토리 핵심 아이템",
        "es": "Objeto clave: Objeto crucial para la historia",
    },
    "消耗品": {
        "zh_TW": "消耗品",
        "zh_CN": "消耗品",
        "en": "Consumable",
        "ja": "消耗品",
        "ko": "소모품",
        "es": "Consumible",
    },
    "素材（點擊使用可賣出）": {
        "zh_TW": "素材（點擊使用可賣出）",
        "zh_CN": "素材（点击使用可出售）",
        "en": "Material (Click Use to Sell)",
        "ja": "素材（使うをクリックで売却）",
        "ko": "재료 (사용 클릭 시 판매)",
        "es": "Material (Pulsa usar para vender)",
    },
    "重要道具": {
        "zh_TW": "重要道具",
        "zh_CN": "重要道具",
        "en": "Key Item",
        "ja": "重要アイテム",
        "ko": "중요 아이템",
        "es": "Objeto clave",
    },
    "類型：%s": {
        "zh_TW": "類型：%s",
        "zh_CN": "类型：%s",
        "en": "Type: %s",
        "ja": "タイプ：%s",
        "ko": "유형: %s",
        "es": "Tipo: %s",
    },
}

def main():
    for loc in LOCALES:
        json_path = I18N_DIR / loc / "ui.json"
        if not json_path.exists():
            print(f"[警告] 找不到語系檔: {json_path}")
            continue
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        added = 0
        updated = 0
        for src, trans_dict in ENTRIES.items():
            val = trans_dict.get(loc, src)
            if src not in data:
                data[src] = val
                added += 1
            elif data[src] != val:
                data[src] = val
                updated += 1

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")

        print(f"[{loc}] ui.json 已更新: 新增 {added} 筆, 更新 {updated} 筆 (總計 {len(data)} 筆)")

if __name__ == "__main__":
    main()
