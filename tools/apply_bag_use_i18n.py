import json
import os

TRANSLATIONS = {
    "zh_TW": {
        "使用【%s】· %s": "使用【%s】· %s",
        "使用【%s】%s": "使用【%s】%s",
        "使用【%s】": "使用【%s】",
        "賣出【%s】· 金 +%d": "賣出【%s】· 金 +%d",
        "【%s】是重要物品，不能消耗。": "【%s】是重要物品，不能消耗。",
        "使用失敗。": "使用失敗。",
        "使用失敗": "使用失敗",
        "賣出失敗。": "賣出失敗。",
        "賣出失敗": "賣出失敗",
        "沒有這個道具。": "沒有這個道具。",
        "無法使用。": "無法使用。",
        "第 %d 格是空的。開 I 背包指派道具。": "第 %d 格是空的。開 I 背包指派道具。",
        "沒有可賣的材料。": "沒有可賣的材料。",
        "賣出材料 %d 件 · 金 +%d": "賣出材料 %d 件 · 金 +%d",
        "星屑 +%d": "星屑 +%d",
        "HP +%d": "HP +%d",
    },
    "zh_CN": {
        "使用【%s】· %s": "使用【%s】· %s",
        "使用【%s】%s": "使用【%s】%s",
        "使用【%s】": "使用【%s】",
        "賣出【%s】· 金 +%d": "出售【%s】· 金 +%d",
        "【%s】是重要物品，不能消耗。": "【%s】是重要物品，不能消耗。",
        "使用失敗。": "使用失败。",
        "使用失敗": "使用失败",
        "賣出失敗。": "出售失败。",
        "賣出失敗": "出售失败",
        "沒有這個道具。": "没有这个道具。",
        "無法使用。": "无法使用。",
        "第 %d 格是空的。開 I 背包指派道具。": "第 %d 格是空的。按 I 打开背包指定道具。",
        "沒有可賣的材料。": "没有可出售的材料。",
        "賣出材料 %d 件 · 金 +%d": "出售材料 %d 件 · 金 +%d",
        "星屑 +%d": "星屑 +%d",
        "HP +%d": "HP +%d",
    },
    "en": {
        "使用【%s】· %s": "Used [%s] · %s",
        "使用【%s】%s": "Used [%s]%s",
        "使用【%s】": "Used [%s]",
        "賣出【%s】· 金 +%d": "Sold [%s] · gold +%d",
        "【%s】是重要物品，不能消耗。": "[%s] is a key item and cannot be consumed.",
        "使用失敗。": "Failed to use.",
        "使用失敗": "Failed to use",
        "賣出失敗。": "Failed to sell.",
        "賣出失敗": "Failed to sell",
        "沒有這個道具。": "Item not found.",
        "無法使用。": "Cannot be used.",
        "第 %d 格是空的。開 I 背包指派道具。": "Slot %d is empty. Open bag (I) to assign items.",
        "沒有可賣的材料。": "No sellable materials.",
        "賣出材料 %d 件 · 金 +%d": "Sold %d materials · gold +%d",
        "星屑 +%d": "Stardust +%d",
        "HP +%d": "HP +%d",
    },
    "ja": {
        "使用【%s】· %s": "【%s】を使用 · %s",
        "使用【%s】%s": "【%s】を使用%s",
        "使用【%s】": "【%s】を使用",
        "賣出【%s】· 金 +%d": "【%s】を売却 · 金 +%d",
        "【%s】是重要物品，不能消耗。": "【%s】は重要アイテムのため消費できません。",
        "使用失敗。": "使用に失敗しました。",
        "使用失敗": "使用に失敗しました",
        "賣出失敗。": "売却に失敗しました。",
        "賣出失敗": "売却に失敗しました",
        "沒有這個道具。": "該当のアイテムがありません。",
        "無法使用。": "使用できません。",
        "第 %d 格是空的。開 I 背包指派道具。": "スロット %d は空です。I キーでバッグを開いて道具を登録してください。",
        "沒有可賣的材料。": "売却できる素材がありません。",
        "賣出材料 %d 件 · 金 +%d": "素材を %d 個売却 · 金 +%d",
        "星屑 +%d": "星屑 +%d",
        "HP +%d": "HP +%d",
    },
    "ko": {
        "使用【%s】· %s": "【%s】 사용 · %s",
        "使用【%s】%s": "【%s】 사용%s",
        "使用【%s】": "【%s】 사용",
        "賣出【%s】· 金 +%d": "【%s】 판매 · 골드 +%d",
        "【%s】是重要物品，不能消耗。": "【%s】(은)는 중요 아이템이므로 소모할 수 없습니다.",
        "使用失敗。": "사용에 실패했습니다.",
        "使用失敗": "사용에 실패했습니다",
        "賣出失敗。": "판매에 실패했습니다.",
        "賣出失敗": "판매에 실패했습니다",
        "沒有這個道具。": "해당 아이템이 없습니다.",
        "無法使用。": "사용할 수 없습니다.",
        "第 %d 格是空的。開 I 背包指派道具。": "슬롯 %d이(가) 비어 있습니다. I 키로 배낭을 열어 아이템을 등록하세요.",
        "沒有可賣的材料。": "판매할 수 있는 재료가 없습니다.",
        "賣出材料 %d 件 · 金 +%d": "재료 %d개 판매 · 골드 +%d",
        "星屑 +%d": "별가루 +%d",
        "HP +%d": "HP +%d",
    },
    "es": {
        "使用【%s】· %s": "Usaste [%s] · %s",
        "使用【%s】%s": "Usaste [%s]%s",
        "使用【%s】": "Usaste [%s]",
        "賣出【%s】· 金 +%d": "Vendiste [%s] · oro +%d",
        "【%s】是重要物品，不能消耗。": "[%s] es un objeto clave y no se puede consumir.",
        "使用失敗。": "Error al usar.",
        "使用失敗": "Error al usar",
        "賣出失敗。": "Error al vender.",
        "賣出失敗": "Error al vender",
        "沒有這個道具。": "El objeto no existe.",
        "無法使用。": "No se puede usar.",
        "第 %d 格是空的。開 I 背包指派道具。": "La casilla %d está vacía. Abre la bolsa (I) para asignar un objeto.",
        "沒有可賣的材料。": "No hay materiales para vender.",
        "賣出材料 %d 件 · 金 +%d": "Vendiste %d materiales · oro +%d",
        "星屑 +%d": "Polvo estelar +%d",
        "HP +%d": "HP +%d",
    }
}

base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"
for loc, items in TRANSLATIONS.items():
    file_path = os.path.join(base_dir, loc, "ui.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in items.items():
        data[k] = v
    # sort keys for clean git diff
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Updated {loc}/ui.json with {len(items)} keys.")
