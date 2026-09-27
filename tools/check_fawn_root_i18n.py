#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
base = '/opt/side/bravesoul-game/game/data/i18n'

fawn_keys = [
    '翠角鹿',
    '鹿',
    '遊俠',
    '翡翠林緣巡守工裝',
    '翡翠林緣巡守背帶工裝',
    '雙色沖壓原木紋金屬板',
    '沖壓雙色象牙米白與淺褐原木紋金屬板',
    '翠木角尺複合機關弓'
]

for loc in locales:
    p = os.path.join(base, f'{loc}.json')
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    print(f'=== root {loc} ({len(d)} keys) ===')
    for k in fawn_keys:
        if k in d:
            print(f'  [FOUND] {k} -> {d[k]}')
        else:
            print(f'  [MISSING] {k}')
