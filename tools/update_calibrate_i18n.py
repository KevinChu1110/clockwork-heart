#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    '鐵屑不足': {
        'zh_TW': '鐵屑不足',
        'zh_CN': '铁屑不足',
        'en': 'Insufficient Scrap',
        'ja': '鉄屑不足',
        'ko': '철 부스러기 부족',
        'es': 'Chatarra insuficiente',
    },
    '鐵屑不足！校準需要 %d 鐵屑。': {
        'zh_TW': '鐵屑不足！校準需要 %d 鐵屑。',
        'zh_CN': '铁屑不足！校准需要 %d 铁屑。',
        'en': 'Not enough scrap iron! Calibration requires %d scrap iron.',
        'ja': '鉄屑が不足しています！校正には %d 個の鉄屑が必要です。',
        'ko': '철 부스러기 부족! 교정에는 철 부스러기 %d개가 필요합니다.',
        'es': '¡Chatarra insuficiente! La calibración requiere %d de chatarra.',
    },
    '鐵屑不足！每次校準需要 %d 鐵屑。': {
        'zh_TW': '鐵屑不足！每次校準需要 %d 鐵屑。',
        'zh_CN': '铁屑不足！每次校准需要 %d 铁屑。',
        'en': 'Not enough scrap iron! Each calibration requires %d scrap iron.',
        'ja': '鉄屑が不足しています！1回の校正には %d 個の鉄屑が必要です。',
        'ko': '철 부스러기 부족! 매 교정마다 철 부스러기 %d개가 필요합니다.',
        'es': '¡Chatarra insuficiente! Cada calibración requiere %d de chatarra.',
    },
    '【%s】%s · 鐵屑不足（持有 %d/%d）· 剩餘校準 %d 次': {
        'zh_TW': '【%s】%s · 鐵屑不足（持有 %d/%d）· 剩餘校準 %d 次',
        'zh_CN': '【%s】%s · 铁屑不足（持有 %d/%d）· 剩余校准 %d 次',
        'en': '[%s] %s · Insufficient Scrap (%d/%d held) · %d Calibrations Left',
        'ja': '【%s】%s · 鉄屑不足（所持 %d/%d）· 残り校正 %d 回',
        'ko': '【%s】%s · 철 부스러기 부족（보유 %d/%d）· 남은 교정 %d회',
        'es': '[%s] %s · Chatarra insuficiente (%d/%d) · %d calibraciones restantes',
    },
    '【%s】%s（目前色階：%s階 · 每次消耗 %d 鐵屑 · 剩餘校準 %d 次）': {
        'zh_TW': '【%s】%s（目前色階：%s階 · 每次消耗 %d 鐵屑 · 剩餘校準 %d 次）',
        'zh_CN': '【%s】%s（目前色阶：%s阶 · 每次消耗 %d 铁屑 · 剩余校准 %d 次）',
        'en': '[%s] %s (Current Tier: %s · Cost: %d Scrap · %d Calibrations Left)',
        'ja': '【%s】%s（現在の階級：%s階 · 1回消費 %d 鉄屑 · 残り校正 %d 回）',
        'ko': '【%s】%s（현재 단계: %s단계 · 1회 소모 %d 철 부스러기 · 남은 교정 %d회）',
        'es': '[%s] %s (Nivel actual: %s · Costo: %d chatarra · %d calibraciones restantes)',
    },
    '【%s】%s · 目前色階：%s階（剩餘 %d 次）': {
        'zh_TW': '【%s】%s · 目前色階：%s階（剩餘 %d 次）',
        'zh_CN': '【%s】%s · 目前色阶：%s阶（剩余 %d 次）',
        'en': '[%s] %s · Current Tier: %s (%d Left)',
        'ja': '【%s】%s · 現在の階級：%s階（残り %d 回）',
        'ko': '【%s】%s · 현재 단계: %s단계（남은 %d회）',
        'es': '[%s] %s · Nivel actual: %s (%d restantes)',
    },
    '【%s】%s（目前色階：%s階 · 剩餘校準：%d 次）': {
        'zh_TW': '【%s】%s（目前色階：%s階 · 剩餘校準：%d 次）',
        'zh_CN': '【%s】%s（目前色阶：%s阶 · 剩余校准：%d 次）',
        'en': '[%s] %s (Current Tier: %s · Calibrations Left: %d)',
        'ja': '【%s】%s（現在の階級：%s階 · 残り校正：%d 回）',
        'ko': '【%s】%s（현재 단계: %s단계 · 남은 교정: %d회）',
        'es': '[%s] %s (Nivel actual: %s · Calibraciones restantes: %d)',
    },
    '【%s】%s（目前色階：%s階 · 剩餘校準 %d 次）': {
        'zh_TW': '【%s】%s（目前色階：%s階 · 剩餘校準 %d 次）',
        'zh_CN': '【%s】%s（目前色阶：%s阶 · 剩余校准 %d 次）',
        'en': '[%s] %s (Current Tier: %s · %d Calibrations Left)',
        'ja': '【%s】%s（現在の階級：%s階 · 残り校正 %d 回）',
        'ko': '【%s】%s（현재 단계: %s단계 · 남은 교정 %d회）',
        'es': '[%s] %s (Nivel actual: %s · %d calibraciones restantes)',
    },
    '【%s】%s（已達最大校準次數上限 7 次）': {
        'zh_TW': '【%s】%s（已達最大校準次數上限 7 次）',
        'zh_CN': '【%s】%s（已达最大校准次数上限 7 次）',
        'en': '[%s] %s (Reached max 7 calibrations)',
        'ja': '【%s】%s（最大校正上限の7回に達しました）',
        'ko': '【%s】%s（최대 교정 횟수 상한 7회 도달）',
        'es': '[%s] %s (Se alcanzó el límite máximo de 7 calibraciones)',
    }
}

content_dir = 'game/data/i18n/content'
for loc in locales:
    p = os.path.join(content_dir, loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in data_map.items():
            d[k] = v[loc]
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p}')

root_i18n_dir = 'game/data/i18n'
for loc in locales:
    p = os.path.join(root_i18n_dir, f'{loc}.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in data_map.items():
            d[k] = v[loc]
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p}')
