#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
new_entries = {
    '連轉——抽十格': {
        'zh_TW': '連轉——抽十格',
        'zh_CN': '连转——抽十格',
        'en': 'Wind Up — Draw 10',
        'ja': '連続巻き——十回引く',
        'ko': '연속 감기——10칸 뽑기',
        'es': 'Dar Cuerda — Extraer 10',
    },
    'soul.btn_pull_ten': {
        'zh_TW': '連轉——抽十格',
        'zh_CN': '连转——抽十格',
        'en': 'Wind Up — Draw 10',
        'ja': '連続巻き——十回引く',
        'ko': '연속 감기——10칸 뽑기',
        'es': 'Dar Cuerda — Extraer 10',
    },
    '封靈連轉結果': {
        'zh_TW': '封靈連轉結果',
        'zh_CN': '封灵连转结果',
        'en': 'Ten Pull Results',
        'ja': '連続召喚結果',
        'ko': '10연속 소환 결과',
        'es': 'Resultados de 10 Extracciones',
    },
    'soul.ten_pull_title': {
        'zh_TW': '封靈連轉結果',
        'zh_CN': '封灵连转结果',
        'en': 'Ten Pull Results',
        'ja': '連続召喚結果',
        'ko': '10연속 소환 결과',
        'es': 'Resultados de 10 Extracciones',
    },
    '收入行囊': {
        'zh_TW': '收入行囊',
        'zh_CN': '收入行囊',
        'en': 'Collect All',
        'ja': '回収する',
        'ko': '모두 수령',
        'es': 'Recoger Todo',
    },
    'soul.btn_collect': {
        'zh_TW': '收入行囊',
        'zh_CN': '收入行囊',
        'en': 'Collect All',
        'ja': '回収する',
        'ko': '모두 수령',
        'es': 'Recoger Todo',
    },
    '再連轉一次': {
        'zh_TW': '再連轉一次',
        'zh_CN': '再连转一次',
        'en': 'Draw 10 Again',
        'ja': 'もう一度十回引く',
        'ko': '다시 10칸 뽑기',
        'es': 'Extraer 10 Otra Vez',
    },
    'soul.btn_pull_ten_again': {
        'zh_TW': '再連轉一次',
        'zh_CN': '再连转一次',
        'en': 'Draw 10 Again',
        'ja': 'もう一度十回引く',
        'ko': '다시 10칸 뽑기',
        'es': 'Extraer 10 Otra Vez',
    },
    '跳過': {
        'zh_TW': '跳過',
        'zh_CN': '跳过',
        'en': 'Skip',
        'ja': 'スキップ',
        'ko': '건너뛰기',
        'es': 'Saltar',
    },
    'soul.btn_skip': {
        'zh_TW': '跳過',
        'zh_CN': '跳过',
        'en': 'Skip',
        'ja': 'スキップ',
        'ko': '건너뛰기',
        'es': 'Saltar',
    }
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
print('Done!')
