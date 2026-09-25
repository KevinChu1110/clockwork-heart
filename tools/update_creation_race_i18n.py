#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    # ── 種族顯示名稱 ──
    "白金兔": {
        "zh_TW": "白金兔",
        "zh_CN": "白金兔",
        "en": "Clockwork Rabbit",
        "ja": "白金兎",
        "ko": "백금토끼",
        "es": "Conejo de Platino",
    },
    "靈尾狐": {
        "zh_TW": "靈尾狐",
        "zh_CN": "灵尾狐",
        "en": "Astral Fox",
        "ja": "霊尾狐",
        "ko": "영미호",
        "es": "Zorro Astral",
    },
    "烈鬃獅": {
        "zh_TW": "烈鬃獅",
        "zh_CN": "烈鬃狮",
        "en": "Gilded Lion",
        "ja": "烈鬃獅子",
        "ko": "열기사자",
        "es": "León Dorado",
    },
    "鋼牙豕": {
        "zh_TW": "鋼牙豕",
        "zh_CN": "钢牙豕",
        "en": "Forge Boar",
        "ja": "鋼牙猪",
        "ko": "강아저",
        "es": "Jabalí de la Forja",
    },
    "靈爪猴": {
        "zh_TW": "靈爪猴",
        "zh_CN": "灵爪猴",
        "en": "Spring Macaque",
        "ja": "霊爪猿",
        "ko": "영조원",
        "es": "Mono Resorte",
    },
    "烈焰虎": {
        "zh_TW": "烈焰虎",
        "zh_CN": "烈焰虎",
        "en": "The Ember Tiger",
        "ja": "烈焔虎",
        "ko": "열염호",
        "es": "El Tigre de Fuego",
    },
    "雲嵐鶴": {
        "zh_TW": "雲嵐鶴",
        "zh_CN": "云岚鹤",
        "en": "The Cloud Crane",
        "ja": "雲嵐鶴",
        "ko": "운람학",
        "es": "La Grulla de las Nubes",
    },
    "玄軸熊": {
        "zh_TW": "玄軸熊",
        "zh_CN": "玄轴熊",
        "en": "The Iron Bear",
        "ja": "玄軸熊",
        "ko": "현축웅",
        "es": "El Oso de Hierro",
    },
    "蒸氣企鵝": {
        "zh_TW": "蒸氣企鵝",
        "zh_CN": "蒸气企鹅",
        "en": "The Steam Penguin",
        "ja": "蒸気ペンギン",
        "ko": "증기 펭귄",
        "es": "El Pingüino de Vapor",
    },
    "玄機龜": {
        "zh_TW": "玄機龜",
        "zh_CN": "玄机龟",
        "en": "The Xuanji Tortoise",
        "ja": "玄機龜",
        "ko": "현기귀",
        "es": "La Tortuga Xuanji",
    },
    "鋼岳象": {
        "zh_TW": "鋼岳象",
        "zh_CN": "钢岳象",
        "en": "The Colossus Elephant",
        "ja": "鋼岳象",
        "ko": "강악상",
        "es": "El Elefante Colosal",
    },
    "碧箸蛙": {
        "zh_TW": "碧箸蛙",
        "zh_CN": "碧箸蛙",
        "en": "The Spring-Leg Frog",
        "ja": "碧箸蛙",
        "ko": "벽저와",
        "es": "Rana de Resorte de Jade",
    },
    "碧簧蛙": {
        "zh_TW": "碧簧蛙",
        "zh_CN": "碧簧蛙",
        "en": "The Spring-Leg Frog",
        "ja": "碧箸蛙",
        "ko": "벽저와",
        "es": "Rana de Resorte de Jade",
    },
    "瓷韻熊貓": {
        "zh_TW": "瓷韻熊貓",
        "zh_CN": "瓷韵熊猫",
        "en": "The Porcelain Panda",
        "ja": "磁韻パンダ",
        "ko": "도운 판다",
        "es": "Panda de Porcelana",
    },
    "翠角鹿": {
        "zh_TW": "翠角鹿",
        "zh_CN": "翠角鹿",
        "en": "The Emerald Fawn",
        "ja": "翠角鹿",
        "ko": "취각록",
        "es": "El Ciervo Esmeralda",
    },

    # ── 右側面板標題與欄位標題 ──
    "即時換裝控制項 · 模組槽位調配": {
        "zh_TW": "即時換裝控制項 · 模組槽位調配",
        "zh_CN": "即时换装控制项 · 模组槽位调配",
        "en": "Live Outfit Controls · Modular Slot Tuning",
        "ja": "リアルタイム着替え操作 · モジュールスロット調整",
        "ko": "실시간 의상 제어 · 모듈 슬롯 배치",
        "es": "Controles de Atuendo en Vivo · Ajuste Modular de Ranuras",
    },
    "• 外裝服飾槽 (Costume Slot - Z:25)": {
        "zh_TW": "• 外裝服飾槽 (Costume Slot - Z:25)",
        "zh_CN": "• 外装服饰槽 (Costume Slot - Z:25)",
        "en": "• Costume Slot (Costume Slot - Z:25)",
        "ja": "• 衣装スロット (Costume Slot - Z:25)",
        "ko": "• 의상 슬롯 (Costume Slot - Z:25)",
        "es": "• Ranura de Atuendo (Costume Slot - Z:25)",
    },
    "• 軀體塗裝槽 (Chassis Shell - Z:10)": {
        "zh_TW": "• 軀體塗裝槽 (Chassis Shell - Z:10)",
        "zh_CN": "• 躯体涂装槽 (Chassis Shell - Z:10)",
        "en": "• Chassis Shell Slot (Chassis Shell - Z:10)",
        "ja": "• 機体塗装スロット (Chassis Shell - Z:10)",
        "ko": "• 기체 도장 슬롯 (Chassis Shell - Z:10)",
        "es": "• Ranura de Pintura (Chassis Shell - Z:10)",
    },
    "• 手持武器槽 (Weapon Slot - Z:40)": {
        "zh_TW": "• 手持武器槽 (Weapon Slot - Z:40)",
        "zh_CN": "• 手持武器槽 (Weapon Slot - Z:40)",
        "en": "• Handheld Weapon Slot (Weapon Slot - Z:40)",
        "ja": "• 手持ち武器スロット (Weapon Slot - Z:40)",
        "ko": "• 무기 슬롯 (Weapon Slot - Z:40)",
        "es": "• Ranura de Arma (Weapon Slot - Z:40)",
    },
    "外裝服飾槽": {
        "zh_TW": "外裝服飾槽",
        "zh_CN": "外装服饰槽",
        "en": "Costume Slot",
        "ja": "衣装スロット",
        "ko": "의상 슬롯",
        "es": "Ranura de Atuendo",
    },
    "軀體塗裝槽": {
        "zh_TW": "軀體塗裝槽",
        "zh_CN": "躯体涂装槽",
        "en": "Chassis Paint Slot",
        "ja": "機体塗装スロット",
        "ko": "기체 도장 슬롯",
        "es": "Ranura de Pintura",
    },
    "手持武器槽": {
        "zh_TW": "手持武器槽",
        "zh_CN": "手持武器槽",
        "en": "Weapon Slot",
        "ja": "手持ち武器スロット",
        "ko": "무기 슬롯",
        "es": "Ranura de Arma",
    },

    # ── 狀態列格式化字串 ──
    "7 大槽位狀態：512 高清合成就緒 (渲染: %d/%d)": {
        "zh_TW": "7 大槽位狀態：512 高清合成就緒 (渲染: %d/%d)",
        "zh_CN": "7 大槽位状态：512 高清合成就绪 (渲染: %d/%d)",
        "en": "7 Slot Status: 512 HD Composite Ready (Rendered: %d/%d)",
        "ja": "7スロット状態：512 HD合成完了 (描画: %d/%d)",
        "ko": "7대 슬롯 상태: 512 HD 합성 준비 완료 (렌더링: %d/%d)",
        "es": "Estado de 7 Ranuras: 512 HD Listo (Renderizado: %d/%d)",
    },
    "7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)": {
        "zh_TW": "7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)",
        "zh_CN": "7 大槽位状态：全部 %d 槽叠合就绪 (载入: %d/%d)",
        "en": "7 Slot Status: All %d Slots Ready (Loaded: %d/%d)",
        "ja": "7スロット状態：全 %d スロット準備完了 (読込: %d/%d)",
        "ko": "7대 슬롯 상태: 전체 %d 슬롯 준비 완료 (로드: %d/%d)",
        "es": "Estado de 7 Ranuras: Las %d Ranuras Listas (Cargadas: %d/%d)",
    },

    # ── 右側操作按鈕 ──
    "重設預設": {
        "zh_TW": "重設預設",
        "zh_CN": "重置默认",
        "en": "Reset Defaults",
        "ja": "デフォルトに戻す",
        "ko": "기본값 복원",
        "es": "Restablecer",
    },
    "儲存驗證截圖": {
        "zh_TW": "儲存驗證截圖",
        "zh_CN": "保存验证截图",
        "en": "Save Verification Proof",
        "ja": "検証スクリーンショット保存",
        "ko": "검증 스크린샷 저장",
        "es": "Guardar Captura de Verificación",
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

print('All i18n files updated successfully!')
