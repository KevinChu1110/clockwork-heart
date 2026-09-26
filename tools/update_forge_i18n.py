#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    # ── 鐵匠鋪鍛造彈窗主標題 ──
    "天宮鐵匠 · 裝備鍛造": {
        "zh_TW": "天宮鐵匠 · 裝備鍛造",
        "zh_CN": "天宫铁匠 · 装备锻造",
        "en": "Celestial Blacksmith · Equipment Forge",
        "ja": "天宮の鍛冶屋 · 装備鍛造",
        "ko": "천궁 대장장이 · 장비 단조",
        "es": "Herrero Celestial · Forja de Equipo",
    },

    # ── 當前裝備與數值 ──
    "當前裝備：%s（第 %d 階）": {
        "zh_TW": "當前裝備：%s（第 %d 階）",
        "zh_CN": "当前装备：%s（第 %d 阶）",
        "en": "Equipped: %s (Tier %d)",
        "ja": "現在の装備：%s（第 %d 階）",
        "ko": "현재 장비: %s (제 %d 단계)",
        "es": "Equipo actual: %s (Rango %d)",
    },
    "武器攻擊：+%d": {
        "zh_TW": "武器攻擊：+%d",
        "zh_CN": "武器攻击：+%d",
        "en": "Weapon ATK: +%d",
        "ja": "武器攻撃：+%d",
        "ko": "무기 공격력: +%d",
        "es": "Ataque de arma: +%d",
    },
    "持有金幣：%d": {
        "zh_TW": "持有金幣：%d",
        "zh_CN": "持有金币：%d",
        "en": "Gold: %d",
        "ja": "所持ゴールド：%d",
        "ko": "보유 골드: %d",
        "es": "Oro en posesión: %d",
    },

    # ── 升階花費與成功率 ──
    "升階花費：已達上限": {
        "zh_TW": "升階花費：已達上限",
        "zh_CN": "升阶花费：已达上限",
        "en": "Forge Cost: Max Tier",
        "ja": "昇階コスト：上限到達",
        "ko": "승급 비용: 최대 달성",
        "es": "Coste de subida: Nivel máx.",
    },
    "升階花費：%d 金幣": {
        "zh_TW": "升階花費：%d 金幣",
        "zh_CN": "升阶花费：%d 金币",
        "en": "Forge Cost: %d Gold",
        "ja": "昇階コスト：%d ゴールド",
        "ko": "승급 비용: %d 골드",
        "es": "Coste de subida: %d de oro",
    },
    "成功率：已封頂": {
        "zh_TW": "成功率：已封頂",
        "zh_CN": "成功率：已封顶",
        "en": "Success Rate: Maxed",
        "ja": "成功率：上限到達",
        "ko": "성공률: 최대 달성",
        "es": "Prob. de éxito: Máxima",
    },
    "基礎成功率：%d%%": {
        "zh_TW": "基礎成功率：%d%%",
        "zh_CN": "基础成功率：%d%%",
        "en": "Base Success Rate: %d%%",
        "ja": "基本成功率：%d%%",
        "ko": "기본 성공률: %d%%",
        "es": "Prob. base de éxito: %d%%",
    },

    # ── 魂槽開放 ──
    "魂槽開放：%d/%d 槽（下一槽需器階 %d）": {
        "zh_TW": "魂槽開放：%d/%d 槽（下一槽需器階 %d）",
        "zh_CN": "魂槽开放：%d/%d 槽（下一槽需器阶 %d）",
        "en": "Soul Slots: %d/%d (Next slot at Tier %d)",
        "ja": "魂スロット解放：%d/%d 枠（次回解放は階位 %d）",
        "ko": "소울 슬롯 개방: %d/%d 슬롯 (다음 슬롯은 제 %d 단계 필요)",
        "es": "Ranuras de alma: %d/%d (Siguiente en Rango %d)",
    },
    "魂槽開放：%d/%d 槽（已全數開放）": {
        "zh_TW": "魂槽開放：%d/%d 槽（已全數開放）",
        "zh_CN": "魂槽开放：%d/%d 槽（已全部开放）",
        "en": "Soul Slots: %d/%d (All Unlocked)",
        "ja": "魂スロット解放：%d/%d 枠（すべて解放済み）",
        "ko": "소울 슬롯 개방: %d/%d 슬롯 (전체 개방 완료)",
        "es": "Ranuras de alma: %d/%d (Todas desbloqueadas)",
    },

    # ── 保底進度條標題與說明 ──
    "器階已達上限 · 鍛造已封頂": {
        "zh_TW": "器階已達上限 · 鍛造已封頂",
        "zh_CN": "器阶已达上限 · 锻造已封顶",
        "en": "Gear Tier Maxed · Forging Capped",
        "ja": "器階上限到達 · 鍛造上限到達",
        "ko": "장비 단계 최대치 달성 · 단조 상한 도달",
        "es": "Nivel de equipo máx. · Forja al tope",
    },
    "所有階級均已鍛造完成": {
        "zh_TW": "所有階級均已鍛造完成",
        "zh_CN": "所有阶级均已锻造完成",
        "en": "All tiers have been forged",
        "ja": "すべての階位の鍛造が完了しました",
        "ko": "모든 단계의 단조가 완료되었습니다",
        "es": "Todos los rangos han sido forjados",
    },
    "鍛造連敗保底 %d/3 · 滿 3 格釘釘摔錘必成功": {
        "zh_TW": "鍛造連敗保底 %d/3 · 滿 3 格釘釘摔錘必成功",
        "zh_CN": "锻造连败保底 %d/3 · 满 3 格钉钉摔锤必成功",
        "en": "Forge Loss Pity %d/3 · At 3 bars Ding's hammer throw guarantees success",
        "ja": "鍛造連敗保証 %d/3 · 3マス満タンで釘釘が錘を投げて必ず成功",
        "ko": "제작 연패 보장 %d/3 · 3칸 달성 시 딩딩 망치 던지기 확정 성공",
        "es": "Garantía de forja %d/3 · Con 3 barras Ding lanza el martillo con éxito asegurado",
    },
    "保底已滿 3/3 · 本次升階釘釘摔錘必成功！": {
        "zh_TW": "保底已滿 3/3 · 本次升階釘釘摔錘必成功！",
        "zh_CN": "保底已满 3/3 · 本次升阶钉钉摔锤必成功！",
        "en": "Pity Full 3/3 · Ding's hammer throw guarantees tier-up this time!",
        "ja": "保証満タン 3/3 · 今回の昇階は釘釘が錘を投げて必ず成功！",
        "ko": "보장 완료 3/3 · 이번 승급은 딩딩 망치 던지기 확정 성공!",
        "es": "¡Garantía 3/3 · Esta subida Ding lanza el martillo con éxito asegurado!",
    },
    "再失敗 1 次將觸發第 3 格摔錘保底": {
        "zh_TW": "再失敗 1 次將觸發第 3 格摔錘保底",
        "zh_CN": "再失败 1 次将触发第 3 格摔锤保底",
        "en": "1 more failure will trigger 3rd bar hammer-throw pity",
        "ja": "あと1回失敗すると第3マスの錘投げ保証が発動します",
        "ko": "1회 더 실패 시 제 3칸 망치 던지기 보장이 발동합니다",
        "es": "1 fallo más activará la garantía de lanzamiento de martillo",
    },
    "升階失敗累積 1 格 · 升階成功清空進度": {
        "zh_TW": "升階失敗累積 1 格 · 升階成功清空進度",
        "zh_CN": "升阶失败累计 1 格 · 升阶成功清空进度",
        "en": "Tier-up failure adds 1 bar · Tier-up success resets progress",
        "ja": "昇階失敗で1マス累積 · 昇階成功で進行度リセット",
        "ko": "승급 실패 시 1칸 누적 · 승급 성공 시 진행도 초기화",
        "es": "Fallo de subida suma 1 barra · Éxito reinicia el progreso",
    },
    "累積 3 次升階失敗將啟動必成功保底機制": {
        "zh_TW": "累積 3 次升階失敗將啟動必成功保底機制",
        "zh_CN": "累计 3 次升阶失败将启动必成功保底机制",
        "en": "Accumulate 3 forge failures to activate guaranteed success pity",
        "ja": "鍛造失敗が3回累積すると確定成功保証が発動します",
        "ko": "승급 실패가 3회 누적되면 확정 성공 보장 메커니즘이 활성화됩니다",
        "es": "Acumular 3 fallos de subida activará la garantía de éxito asegurado",
    },
    "保底已觸發 · 釘釘發脾氣必定升階": {
        "zh_TW": "保底已觸發 · 釘釘發脾氣必定升階",
        "zh_CN": "保底已触发 · 钉钉发脾气必定升阶",
        "en": "Pity triggered · Ding's tantrum guarantees tier-up",
        "ja": "保証発動 · 釘釘の癇癪で必ず昇階",
        "ko": "보장 발동 · 딩딩의 성화로 확정 승급",
        "es": "Garantía activada · El berrinche de Ding asegura la subida",
    },

    # ── 操作按鈕 ──
    "鍛造已封頂": {
        "zh_TW": "鍛造已封頂",
        "zh_CN": "锻造已封顶",
        "en": "Forging Maxed",
        "ja": "鍛造上限到達",
        "ko": "단조 상한 도달",
        "es": "Forja al máximo",
    },
    "強化升階（消耗 %d 金幣）": {
        "zh_TW": "強化升階（消耗 %d 金幣）",
        "zh_CN": "强化升阶（消耗 %d 金币）",
        "en": "Forge Tier-Up (Costs %d Gold)",
        "ja": "強化昇階（%d ゴールド消費）",
        "ko": "강화 승급 (%d 골드 소모)",
        "es": "Mejorar rango (Coste %d de oro)",
    },
    "離開鐵匠鋪": {
        "zh_TW": "離開鐵匠鋪",
        "zh_CN": "离开铁匠铺",
        "en": "Leave Smithy",
        "ja": "鍛冶屋を出る",
        "ko": "대장간 나가기",
        "es": "Salir de la herrería",
    },

    # ── 操作提示回饋 (_msg_label) ──
    "器階已達上限，無法再進行鍛造！": {
        "zh_TW": "器階已達上限，無法再進行鍛造！",
        "zh_CN": "器阶已达上限，无法再进行锻造！",
        "en": "Gear tier maxed, cannot forge any further!",
        "ja": "器階が上限に達しているため、これ以上鍛造できません！",
        "ko": "장비 단계가 최대치에 도달하여 더 이상 단조할 수 없습니다!",
        "es": "¡El equipo ya está en su nivel máximo, no se puede forjar más!",
    },
    "金幣不足！升階需要 %d 金幣。": {
        "zh_TW": "金幣不足！升階需要 %d 金幣。",
        "zh_CN": "金币不足！升阶需要 %d 金币。",
        "en": "Not enough gold! Tier-up requires %d Gold.",
        "ja": "ゴールドが不足しています！昇階には %d ゴールド必要です。",
        "ko": "골드가 부족합니다! 승급에는 %d 골드가 필요합니다.",
        "es": "¡Oro insuficiente! Subir de nivel requiere %d de oro.",
    },
    "（消耗鐵屑穩火）": {
        "zh_TW": "（消耗鐵屑穩火）",
        "zh_CN": "（消耗铁屑稳火）",
        "en": " (Used iron scrap to steady flame)",
        "ja": "（鉄屑を消費して火力を安定）",
        "ko": " (쇠부스러기를 소모하여 화력 안정)",
        "es": " (Hierro residual usado para avivar el fuego)",
    },
    "鍛造成功！升階至第 %d 階，攻擊力上升！%s": {
        "zh_TW": "鍛造成功！升階至第 %d 階，攻擊力上升！%s",
        "zh_CN": "锻造成功！升阶至第 %d 阶，攻击力上升！%s",
        "en": "Forge successful! Upgraded to Tier %d, ATK increased!%s",
        "ja": "鍛造成功！第 %d 階へ昇階し、攻撃力が上昇しました！%s",
        "ko": "단조 성공! 제 %d 단계로 승급하여 공격력이 상승했습니다!%s",
        "es": "¡Forja exitosa! ¡Subido a Rango %d, ataque aumentado!%s",
    },
    "鍛造失敗！釘釘摔錘了，吃塊消氣餅回復體力！": {
        "zh_TW": "鍛造失敗！釘釘摔錘了，吃塊消氣餅回復體力！",
        "zh_CN": "锻造失败！钉钉摔锤了，吃块消气饼回复体力！",
        "en": "Forge failed! Ding slammed his hammer; eat a chill-out cookie to recover energy!",
        "ja": "鍛造失敗！釘釘が錘を叩きつけました、機嫌直しの餅を食べて体力を回復！",
        "ko": "단조 실패! 딩딩이 망치를 내리쳤습니다. 화풀이 떡을 먹고 기력을 회복하세요!",
        "es": "¡Forja fallida! Ding ha estampado el martillo, ¡come una galleta de calmar ánimos para reponer energía!",
    },
    "鍛造失敗！累積 1 格保底進度（目前 %d/3 格）。": {
        "zh_TW": "鍛造失敗！累積 1 格保底進度（目前 %d/3 格）。",
        "zh_CN": "锻造失败！累计 1 格保底进度（目前 %d/3 格）。",
        "en": "Forge failed! Accumulated 1 pity bar (%d/3 bars currently).",
        "ja": "鍛造失敗！保証が1マス累積しました（現在 %d/3 マス）。",
        "ko": "단조 실패! 보장 진행도 1칸 누적 (현재 %d/3칸).",
        "es": "¡Forja fallida! Acumulada 1 barra de garantía (actualmente %d/3 barras).",
    },
}

# 1. 更新 game/data/i18n/content/<loc>/ui.json
content_dir = 'game/data/i18n/content'
for loc in locales:
    p = os.path.join(content_dir, loc, 'ui.json')
    if os.path.exists(p):
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

print('Forge i18n files updated successfully!')
