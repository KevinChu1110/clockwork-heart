#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    # ── 手藝工坊彈窗主標題與分頁 ──
    "手藝工坊 · 寶石熔煉與寶石櫃": {
        "zh_TW": "手藝工坊 · 寶石熔煉與寶石櫃",
        "zh_CN": "手艺工坊 · 宝石熔炼与宝石柜",
        "en": "Gem Workshop · Smelting & Gem Case",
        "ja": "細工工房 · 宝石製錬と宝石棚",
        "ko": "세공 공방 · 보석 제련과 보석함",
        "es": "Taller de Gemas · Fundición y Alijo de Gemas",
    },
    "寶石熔煉與合成": {
        "zh_TW": "寶石熔煉與合成",
        "zh_CN": "宝石熔炼与合成",
        "en": "Gem Smelting & Fusion",
        "ja": "宝石製錬と合成",
        "ko": "보석 제련과 합성",
        "es": "Fundición y Fusión de Gemas",
    },
    "寶石櫃盤點檢視": {
        "zh_TW": "寶石櫃盤點檢視",
        "zh_CN": "宝石柜盘点检视",
        "en": "Gem Case Inventory",
        "ja": "宝石棚の確認",
        "ko": "보석함 재고 점검",
        "es": "Inventario de Gemas",
    },

    # ── 熔煉產線頂部橫幅與規則 ──
    "今日熔煉產線：%d / %d 線": {
        "zh_TW": "今日熔煉產線：%d / %d 線",
        "zh_CN": "今日熔炼产线：%d / %d 线",
        "en": "Today's Smelt Lines: %d / %d",
        "ja": "本日の製錬ライン：%d / %d",
        "ko": "오늘의 제련 라인: %d / %d",
        "es": "Líneas de Fundición de Hoy: %d / %d",
    },
    "· 熔爐已點燃（雙線並行）": {
        "zh_TW": "· 熔爐已點燃（雙線並行）",
        "zh_CN": "· 熔炉已点燃（双线并行）",
        "en": "· Furnace Lit (Dual Line Active)",
        "ja": "· 溶鉱炉点火中（二重ライン稼働）",
        "ko": "· 용광로 점화됨 (듀얼 라인 가동)",
        "es": "· Horno Encendido (Línea Doble Activa)",
    },
    "點燃熔爐": {
        "zh_TW": "點燃熔爐",
        "zh_CN": "点燃熔炉",
        "en": "Light Furnace",
        "ja": "溶鉱炉点火",
        "ko": "용광로 점화",
        "es": "Encender Horno",
    },
    "3碎片→1級 · 3顆同級可合成": {
        "zh_TW": "3碎片→1級 · 3顆同級可合成",
        "zh_CN": "3碎片→1级 · 3颗同级可合成",
        "en": "3 Shards → Lv.1 · 3 Same-Level Can Fuse",
        "ja": "破片3個→1階 · 同階3個で合成可能",
        "ko": "조각 3개→1급 · 동급 3개 합성 가능",
        "es": "3 Frag. → Niv.1 · 3 de Mismo Nivel Fusionan",
    },

    # ── 寶石顏色名 ──
    "紅寶石": {
        "zh_TW": "紅寶石",
        "zh_CN": "红宝石",
        "en": "Ruby",
        "ja": "ルビー",
        "ko": "루비",
        "es": "Rubí",
    },
    "黃寶石": {
        "zh_TW": "黃寶石",
        "zh_CN": "黄宝石",
        "en": "Topaz",
        "ja": "トパーズ",
        "ko": "토파즈",
        "es": "Topacio",
    },
    "藍寶石": {
        "zh_TW": "藍寶石",
        "zh_CN": "蓝宝石",
        "en": "Sapphire",
        "ja": "サファイア",
        "ko": "사파이어",
        "es": "Zafiro",
    },

    # ── 寶石特性 ──
    "暴擊·生命": {
        "zh_TW": "暴擊·生命",
        "zh_CN": "暴击·生命",
        "en": "Crit · HP",
        "ja": "会心・生命",
        "ko": "치명타·생명",
        "es": "Crítico · Vida",
    },
    "攻擊·防禦": {
        "zh_TW": "攻擊·防禦",
        "zh_CN": "攻击·防御",
        "en": "ATK · DEF",
        "ja": "攻撃・防御",
        "ko": "공격·방어",
        "es": "ATQ · DEF",
    },
    "命中·迴避": {
        "zh_TW": "命中·迴避",
        "zh_CN": "命中·回避",
        "en": "Hit · Evasion",
        "ja": "命中・回避",
        "ko": "명중·회피",
        "es": "Acierto · Evasión",
    },

    # ── 碎片與各階存量 ──
    "碎片儲備": {
        "zh_TW": "碎片儲備",
        "zh_CN": "碎片储备",
        "en": "Shard Stock",
        "ja": "破片備蓄",
        "ko": "조각 비축",
        "es": "Reserva de Fragmentos",
    },
    "%d階:%d": {
        "zh_TW": "%d階:%d",
        "zh_CN": "%d阶:%d",
        "en": "Lv.%d:%d",
        "ja": "%d階:%d",
        "ko": "%d급:%d",
        "es": "Niv.%d:%d",
    },

    # ── 熔煉與合成按鈕與反饋 ──
    "熔煉 1 級寶石": {
        "zh_TW": "熔煉 1 級寶石",
        "zh_CN": "熔炼 1 级宝石",
        "en": "Smelt Lv.1 Gem",
        "ja": "1階の宝石を製錬",
        "ko": "1급 보석 제련",
        "es": "Fundir Gema Niv.1",
    },
    "今日產線已盡": {
        "zh_TW": "今日產線已盡",
        "zh_CN": "今日产线已尽",
        "en": "No Lines Left Today",
        "ja": "本日のライン上限",
        "ko": "오늘 생산 라인 소진",
        "es": "Líneas de Hoy Agotadas",
    },
    "碎片不足(需3)": {
        "zh_TW": "碎片不足(需3)",
        "zh_CN": "碎片不足(需3)",
        "en": "Need 3 Shards",
        "ja": "破片不足(必要:3)",
        "ko": "조각 부족(3개 필요)",
        "es": "Faltan Fragmentos (3 Req.)",
    },
    "熔煉完成！": {
        "zh_TW": "熔煉完成！",
        "zh_CN": "熔炼完成！",
        "en": "Smelting Complete!",
        "ja": "製錬完了！",
        "ko": "제련 완료!",
        "es": "¡Fundición Completada!",
    },
    "合成 %d 級 → %d 級": {
        "zh_TW": "合成 %d 級 → %d 級",
        "zh_CN": "合成 %d 级 → %d 级",
        "en": "Fuse Lv.%d → Lv.%d",
        "ja": "合成 %d階 → %d階",
        "ko": "합성 %d급 → %d급",
        "es": "Fusionar Niv.%d → Niv.%d",
    },
    "合成(需3同級)": {
        "zh_TW": "合成(需3同級)",
        "zh_CN": "合成(需3同级)",
        "en": "Need 3 of Same Lv.",
        "ja": "同階3個必要",
        "ko": "동급 3개 필요",
        "es": "Req. 3 del Mismo Nivel",
    },
    "合成完成！": {
        "zh_TW": "合成完成！",
        "zh_CN": "合成完成！",
        "en": "Fusion Complete!",
        "ja": "合成完了！",
        "ko": "합성 완료!",
        "es": "¡Fusión Completada!",
    },

    # ── 寶石櫃分頁 ──
    "倉庫寶石儲備盤點（各階數量）": {
        "zh_TW": "倉庫寶石儲備盤點（各階數量）",
        "zh_CN": "仓库宝石储备盘点（各阶数量）",
        "en": "Warehouse Gem Reserves (By Level)",
        "ja": "倉庫の宝石備蓄確認（階層別）",
        "ko": "창고 보석 비축 점검 (등급별 수량)",
        "es": "Reservas de Gemas en Almacén (Por Nivel)",
    },
    "重新盤點": {
        "zh_TW": "重新盤點",
        "zh_CN": "重新盘点",
        "en": "Re-Inventory",
        "ja": "再確認",
        "ko": "다시 점검",
        "es": "Recontar",
    },
    "一鍵鑲嵌": {
        "zh_TW": "一鍵鑲嵌",
        "zh_CN": "一键镶嵌",
        "en": "Quick Socket",
        "ja": "一括装着",
        "ko": "일괄 장착",
        "es": "Engarzar Todo",
    },
    "離開工坊": {
        "zh_TW": "離開工坊",
        "zh_CN": "离开工坊",
        "en": "Leave Workshop",
        "ja": "工房を出る",
        "ko": "공방 나가기",
        "es": "Salir del Taller",
    },
    "全身穿戴寶石六維總加成": {
        "zh_TW": "全身穿戴寶石六維總加成",
        "zh_CN": "全身穿戴宝石六维总加成",
        "en": "Total 6-Stat Gem Socket Bonuses",
        "ja": "装備宝石の全ステータス合計加算",
        "ko": "착용 보석 6대 능력치 총합 보너스",
        "es": "Bonif. Total de Gemas Engarzadas",
    },

    # ── 六維加成項目 ──
    "暴擊：+%.1f": {
        "zh_TW": "暴擊：+%.1f",
        "zh_CN": "暴击：+%.1f",
        "en": "Crit: +%.1f",
        "ja": "会心：+%.1f",
        "ko": "치명타: +%.1f",
        "es": "Crítico: +%.1f",
    },
    "攻擊加成：+%.1f%%": {
        "zh_TW": "攻擊加成：+%.1f%%",
        "zh_CN": "攻击加成：+%.1f%%",
        "en": "ATK Bonus: +%.1f%%",
        "ja": "攻撃力加算：+%.1f%%",
        "ko": "공격력 보너스: +%.1f%%",
        "es": "Bonif. ATQ: +%.1f%%",
    },
    "命中：+%.1f": {
        "zh_TW": "命中：+%.1f",
        "zh_CN": "命中：+%.1f",
        "en": "Hit: +%.1f",
        "ja": "命中：+%.1f",
        "ko": "명중: +%.1f",
        "es": "Acierto: +%.1f",
    },
    "生命加成：+%.1f%%": {
        "zh_TW": "生命加成：+%.1f%%",
        "zh_CN": "生命加成：+%.1f%%",
        "en": "HP Bonus: +%.1f%%",
        "ja": "生命力加算：+%.1f%%",
        "ko": "생명력 보너스: +%.1f%%",
        "es": "Bonif. Vida: +%.1f%%",
    },
    "防禦加成：+%.1f%%": {
        "zh_TW": "防禦加成：+%.1f%%",
        "zh_CN": "防御加成：+%.1f%%",
        "en": "DEF Bonus: +%.1f%%",
        "ja": "防御力加算：+%.1f%%",
        "ko": "방어력 보너스: +%.1f%%",
        "es": "Bonif. DEF: +%.1f%%",
    },
    "迴避：+%.1f": {
        "zh_TW": "迴避：+%.1f",
        "zh_CN": "回避：+%.1f",
        "en": "Evasion: +%.1f",
        "ja": "回避：+%.1f",
        "ko": "회피: +%.1f",
        "es": "Evasión: +%.1f",
    },

    # ── 孔位卡片與庫存小卡 ──
    "%s孔位": {
        "zh_TW": "%s孔位",
        "zh_CN": "%s孔位",
        "en": "%s Socket",
        "ja": "%sスロット",
        "ko": "%s 소켓",
        "es": "Ranura de %s",
    },
    "未穿戴裝備": {
        "zh_TW": "未穿戴裝備",
        "zh_CN": "未穿戴装备",
        "en": "No Gear Equipped",
        "ja": "装備未装着",
        "ko": "장비 미착용",
        "es": "Sin Equipo Equipado",
    },
    "孔位閒置 · 未鑲嵌寶石": {
        "zh_TW": "孔位閒置 · 未鑲嵌寶石",
        "zh_CN": "孔位闲置 · 未镶嵌宝石",
        "en": "Socket Empty · No Gem Socketed",
        "ja": "スロット空き · 宝石未装着",
        "ko": "소켓 비어있음 · 보석 미장착",
        "es": "Ranura Vacía · Sin Gema Engarzada",
    },
    "已鑲嵌：%s (%s) · %s %s": {
        "zh_TW": "已鑲嵌：%s (%s) · %s %s",
        "zh_CN": "已镶嵌：%s (%s) · %s %s",
        "en": "Socketed: %s (%s) · %s %s",
        "ja": "装着中：%s (%s) · %s %s",
        "ko": "장착됨: %s (%s) · %s %s",
        "es": "Engarzada: %s (%s) · %s %s",
    },
    "%s %d級": {
        "zh_TW": "%s %d級",
        "zh_CN": "%s %d级",
        "en": "%s Lv.%d",
        "ja": "%s %d階",
        "ko": "%s %d급",
        "es": "%s Niv.%d",
    },
    "持有 %d 顆": {
        "zh_TW": "持有 %d 顆",
        "zh_CN": "持有 %d 颗",
        "en": "%d Owned",
        "ja": "%d個所持",
        "ko": "%d개 보유",
        "es": "%d Poseído",
    },
    "0 顆": {
        "zh_TW": "0 顆",
        "zh_CN": "0 颗",
        "en": "0 Owned",
        "ja": "0個",
        "ko": "0개",
        "es": "0",
    },
    "%s · %d 級": {
        "zh_TW": "%s · %d 級",
        "zh_CN": "%s · %d 级",
        "en": "%s · Lv.%d",
        "ja": "%s · %d階",
        "ko": "%s · %d급",
        "es": "%s · Niv.%d",
    },

    # ── 品階 ──
    "凡": {
        "zh_TW": "凡",
        "zh_CN": "凡",
        "en": "Common",
        "ja": "凡",
        "ko": "일반",
        "es": "Común",
    },
    "良": {
        "zh_TW": "良",
        "zh_CN": "良",
        "en": "Fine",
        "ja": "良",
        "ko": "우수",
        "es": "Bueno",
    },
    "優": {
        "zh_TW": "優",
        "zh_CN": "优",
        "en": "Rare",
        "ja": "優",
        "ko": "희귀",
        "es": "Raro",
    },
    "精": {
        "zh_TW": "精",
        "zh_CN": "精",
        "en": "Epic",
        "ja": "精",
        "ko": "영웅",
        "es": "Épico",
    },
    "極": {
        "zh_TW": "極",
        "zh_CN": "极",
        "en": "Mythic",
        "ja": "極",
        "ko": "전설",
        "es": "Mítico",
    },
}

# 1. 更新 game/data/i18n/content/<loc>/ui.json
content_dir = 'game/data/i18n/content'
for loc in locales:
    p = os.path.join(content_dir, loc, 'ui.json')
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    before_len = len(d)
    for k, v in data_map.items():
        d[k] = v[loc]
    after_len = len(d)
    print(f'[content/ui.json] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

# 2. 同步更新 game/data/i18n/<loc>.json（滿足 Loc.t 根層查找）
root_i18n_dir = 'game/data/i18n'
for loc in locales:
    p = os.path.join(root_i18n_dir, f'{loc}.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        before_len = len(d)
        for k, v in data_map.items():
            d[k] = v[loc]
        after_len = len(d)
        print(f'[root i18n] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')

print('Gem Workshop i18n files updated successfully!')
