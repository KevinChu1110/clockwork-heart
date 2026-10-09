import json, os

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
base_dir = "/opt/side/bravesoul-game/game/data/i18n/content"

new_entries = {
    "武器庫 · 更換裝備": {
        "zh_TW": "武器庫 · 更換裝備",
        "zh_CN": "武器库 · 更换装备",
        "en": "Armory · Change Equipment",
        "ja": "武器庫 · 装備変更",
        "ko": "무기고 · 장비 교체",
        "es": "Armería · Cambiar equipo"
    },
    "選擇要裝備至【%s】的武器 · 即時連動紙娃娃與屬性": {
        "zh_TW": "選擇要裝備至【%s】的武器 · 即時連動紙娃娃與屬性",
        "zh_CN": "选择要装备至【%s】的武器 · 实时连动纸娃娃与属性",
        "en": "Select weapon for [%s] · Live paperdoll & stat sync",
        "ja": "【%s】に装備する武器を選択 · 着せ替えとステータス即時連動",
        "ko": "[%s]에 장착할 무기 선택 · 외형 및 능력치 즉시 연동",
        "es": "Selecciona arma para [%s] · Sincronización en vivo"
    },
    "背包與庫存尚無可替換武器": {
        "zh_TW": "背包與庫存尚無可替換武器",
        "zh_CN": "背包与库存尚无可替换武器",
        "en": "No alternative weapons in inventory",
        "ja": "バッグとインベントリに交換可能な武器がありません",
        "ko": "가방과 보관함에 교체 가능한 무기가 없습니다",
        "es": "No hay armas alternativas en el inventario"
    },
    "可前往冒險出征獲取或在鍛造殿堂打造新武器": {
        "zh_TW": "可前往冒險出征獲取或在鍛造殿堂打造新武器",
        "zh_CN": "可前往冒险出征获取或在锻造殿堂打造新武器",
        "en": "Acquire from adventure sorties or forge in the Hall",
        "ja": "冒険の出征で入手するか鍛冶の殿堂で作成できます",
        "ko": "모험 출정에서 획득하거나 대장간에서 제작할 수 있습니다",
        "es": "Consíguelas en expediciones o forja en la Sala"
    },
    "卸下武器": {
        "zh_TW": "卸下武器",
        "zh_CN": "卸下武器",
        "en": "Unequip",
        "ja": "武器を外す",
        "ko": "무기 해제",
        "es": "Desequipar"
    },
    "使用中": {
        "zh_TW": "使用中",
        "zh_CN": "使用中",
        "en": "In Use",
        "ja": "使用中",
        "ko": "사용 중",
        "es": "En uso"
    },
    "裝備": {
        "zh_TW": "裝備",
        "zh_CN": "装备",
        "en": "Equip",
        "ja": "装備",
        "ko": "장착",
        "es": "Equipar"
    },
    "調換至此欄": {
        "zh_TW": "調換至此欄",
        "zh_CN": "调换至此栏",
        "en": "Swap to this slot",
        "ja": "この欄に付け替え",
        "ko": "이 슬롯으로 변경",
        "es": "Cambiar a esta ranura"
    },
    "其他欄位使用中": {
        "zh_TW": "其他欄位使用中",
        "zh_CN": "其他栏位使用中",
        "en": "In other slot",
        "ja": "他のスロットで使用中",
        "ko": "다른 슬롯에서 사용 중",
        "es": "En otra casilla"
    },
    "當前槽位裝備中": {
        "zh_TW": "當前槽位裝備中",
        "zh_CN": "当前槽位装备中",
        "en": "Equipped in slot",
        "ja": "現在のスロットに装備中",
        "ko": "현재 슬롯 장착 중",
        "es": "Equipado aquí"
    },
    "需達 Lv%d 解鎖": {
        "zh_TW": "需達 Lv%d 解鎖",
        "zh_CN": "需达 Lv%d 解锁",
        "en": "Requires Lv%d",
        "ja": "Lv%d で解放",
        "ko": "Lv%d 시 해금",
        "es": "Requiere Nv.%d"
    },
    "當前槽位尚未裝備武器": {
        "zh_TW": "當前槽位尚未裝備武器",
        "zh_CN": "当前槽位尚未装备武器",
        "en": "No weapon equipped in this slot",
        "ja": "現在スロットに武器が装備されていません",
        "ko": "현재 슬롯에 무기가 장착되지 않았습니다",
        "es": "No hay arma equipada en esta ranura"
    },
    "點擊武器卡片即可立即更換，即時更新戰鬥屬性與外觀紙娃娃": {
        "zh_TW": "點擊武器卡片即可立即更換，即時更新戰鬥屬性與外觀紙娃娃",
        "zh_CN": "点击武器卡片即可立即更换，实时更新战斗属性与外观纸娃娃",
        "en": "Click a weapon to equip immediately · Live stat and appearance update",
        "ja": "武器カードをクリックすると即座に変更され、能力値と外見が更新されます",
        "ko": "무기 카드를 클릭하면 즉시 교체되며 전투 능력치와 종이인형이 갱신됩니다",
        "es": "Toca un arma para equiparla al instante · Actualiza atributos y aspecto"
    }
}

for loc in locales:
    p = os.path.join(base_dir, loc, "ui.json")
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    added = 0
    for k, trans in new_entries.items():
        if k not in data:
            data[k] = trans[loc]
            added += 1
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[{loc}] added {added} entries to {p}")
