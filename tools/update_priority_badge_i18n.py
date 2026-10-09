#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
new_entries = {
    '平常首發': {
        'zh_TW': '平常首發',
        'zh_CN': '平时首发',
        'en': 'Normal Opener',
        'ja': '通常初手',
        'ko': '통상 선공',
        'es': 'Apertura normal',
    },
    '【平常首發】': {
        'zh_TW': '【平常首發】',
        'zh_CN': '【平时首发】',
        'en': '[Normal Opener]',
        'ja': '【通常初手】',
        'ko': '【통상 선공】',
        'es': '[Apertura normal]',
    },
    '危急應急': {
        'zh_TW': '危急應急',
        'zh_CN': '危急应急',
        'en': 'Crisis Emergency',
        'ja': '緊急応急',
        'ko': '위급 대처',
        'es': 'Respuesta de crisis',
    },
    '【危急應急】': {
        'zh_TW': '【危急應急】',
        'zh_CN': '【危急应急】',
        'en': '[Crisis Emergency]',
        'ja': '【緊急応急】',
        'ko': '【위급 대처】',
        'es': '[Respuesta de crisis]',
    },
}

for loc in locales:
    p = os.path.join('game/data/i18n/content', loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p}')

    p_root = os.path.join('game/data/i18n', f'{loc}.json')
    if os.path.exists(p_root):
        with open(p_root, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p_root, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p_root}')
