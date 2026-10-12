import json

locales = {
    "zh_TW": {
        "ui_hotbar_slot_capsule": "快捷欄 %d",
        "快捷欄 %d": "快捷欄 %d",
        "快捷欄 1": "快捷欄 1",
        "快捷欄 2": "快捷欄 2",
        "ui_remove_hotbar": "從快捷欄卸下",
        "從快捷欄卸下": "從快捷欄卸下",
        "已從快捷欄卸下：%s": "已從快捷欄卸下：%s",
    },
    "zh_CN": {
        "ui_hotbar_slot_capsule": "快捷栏 %d",
        "快捷欄 %d": "快捷栏 %d",
        "快捷欄 1": "快捷栏 1",
        "快捷欄 2": "快捷栏 2",
        "ui_remove_hotbar": "从快捷栏卸下",
        "從快捷欄卸下": "从快捷栏卸下",
        "已從快捷欄卸下：%s": "已从快捷栏卸下：%s",
    },
    "en": {
        "ui_hotbar_slot_capsule": "Hotbar %d",
        "快捷欄 %d": "Hotbar %d",
        "快捷欄 1": "Hotbar 1",
        "快捷欄 2": "Hotbar 2",
        "ui_remove_hotbar": "Remove from Hotbar",
        "從快捷欄卸下": "Remove from Hotbar",
        "已從快捷欄卸下：%s": "Removed from Hotbar: %s",
    },
    "ja": {
        "ui_hotbar_slot_capsule": "ショートカット %d",
        "快捷欄 %d": "ショートカット %d",
        "快捷欄 1": "ショートカット 1",
        "快捷欄 2": "ショートカット 2",
        "ui_remove_hotbar": "ショートカットから解除",
        "從快捷欄卸下": "ショートカットから解除",
        "已從快捷欄卸下：%s": "ショートカットから解除しました：%s",
    },
    "ko": {
        "ui_hotbar_slot_capsule": "단축칸 %d",
        "快捷欄 %d": "단축칸 %d",
        "快捷欄 1": "단축칸 1",
        "快捷欄 2": "단축칸 2",
        "ui_remove_hotbar": "단축칸에서 해제",
        "從快捷欄卸下": "단축칸에서 해제",
        "已從快捷欄卸下：%s": "단축칸에서 해제됨: %s",
    },
    "es": {
        "ui_hotbar_slot_capsule": "Acceso rápido %d",
        "快捷欄 %d": "Acceso rápido %d",
        "快捷欄 1": "Acceso rápido 1",
        "快捷欄 2": "Acceso rápido 2",
        "ui_remove_hotbar": "Quitar de acceso rápido",
        "從快捷欄卸下": "Quitar de acceso rápido",
        "已從快捷欄卸下：%s": "Quitado del acceso rápido: %s",
    },
}

for loc, entries in locales.items():
    ui_path = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(ui_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in entries.items():
        data[k] = v
    with open(ui_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    root_path = f"/opt/side/bravesoul-game/game/data/i18n/{loc}.json"
    with open(root_path, "r", encoding="utf-8") as f:
        data2 = json.load(f)
    for k, v in entries.items():
        data2[k] = v
    with open(root_path, "w", encoding="utf-8") as f:
        json.dump(data2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("Updated hotbar capsule i18n files for all 6 locales successfully!")
