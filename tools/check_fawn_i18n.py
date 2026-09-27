#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
base = '/opt/side/bravesoul-game/game/data/i18n/content'

fawn_keys = [
    '翠角鹿',
    '鹿',
    '遊俠',
    '翡翠林緣巡守工裝',
    '翡翠林緣巡守背帶工裝',
    '雙色沖壓原木紋金屬板',
    '沖壓雙色象牙米白與淺褐原木紋金屬板',
    '翠木角尺複合機關弓',
    '墨綠輕布料披肩配黃銅皮扣巡守工裝',
    '沖壓雙色象牙米白與淺褐原木紋金屬板，黃銅鉚釘包邊',
    '自翡翠深林守護巡林的發條小鹿，米白淺褐薄鐵皮板件，精密黃銅游標卡尺角尺天線與減震馬蹄墊。',
    '卸除外裝，呈現米白淺褐原木紋金屬素體',
    '無外裝 (裸機素體)'
]

for loc in locales:
    p = os.path.join(base, loc, 'ui.json')
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    print(f'=== {loc} ({len(d)} keys) ===')
    for k in fawn_keys:
        if k in d:
            print(f'  [FOUND] {k} -> {d[k]}')
        else:
            print(f'  [MISSING] {k}')
