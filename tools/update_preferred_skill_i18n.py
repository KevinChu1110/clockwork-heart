#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
new_entries = {
    '設為首發': {
        'zh_TW': '設為首發',
        'zh_CN': '设为首发',
        'en': 'Set as Opener',
        'ja': '初手に設定',
        'ko': '선발 설정',
        'es': 'Fijar inicial',
    },
    '【設為首發】': {
        'zh_TW': '【設為首發】',
        'zh_CN': '【设为首发】',
        'en': '[Set as Opener]',
        'ja': '【初手に設定】',
        'ko': '【선발 설정】',
        'es': '[Fijar inicial]',
    },
    '已設首發': {
        'zh_TW': '已設首發',
        'zh_CN': '已设首发',
        'en': '已设首发',
        'ja': '初手設定済',
        'ko': '선발 지정됨',
        'es': 'Inicial fijado',
    },
    '【已設首發】': {
        'zh_TW': '【已設首發】',
        'zh_CN': '【已设首发】',
        'en': '[Opener Set]',
        'ja': '【初手設定済】',
        'ko': '【선발 지정됨】',
        'es': '[Inicial fijado]',
    },
    '取消首發': {
        'zh_TW': '取消首發',
        'zh_CN': '取消首发',
        'en': 'Unset Opener',
        'ja': '初手を解除',
        'ko': '선발 해제',
        'es': 'Quitar inicial',
    },
    '【取消首發】': {
        'zh_TW': '【取消首發】',
        'zh_CN': '【取消首发】',
        'en': '[Unset Opener]',
        'ja': '【初手を解除】',
        'ko': '【선발 해제】',
        'es': '[Quitar inicial]',
    },
}
# Correction for English
new_entries['已設首發']['en'] = 'Opener Set'

for loc in locales:
    p = os.path.join('/opt/side/bravesoul-game/game/data/i18n/content', loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p}')

    p_root = os.path.join('/opt/side/bravesoul-game/game/data/i18n', f'{loc}.json')
    if os.path.exists(p_root):
        with open(p_root, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p_root, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p_root}')
