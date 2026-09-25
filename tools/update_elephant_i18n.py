#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    '鋼岳象': {
        'zh_TW': '鋼岳象',
        'zh_CN': '钢岳象',
        'en': 'The Colossus Elephant',
        'ja': '鋼岳象',
        'ko': '강악상',
        'es': 'El Elefante Colosal'
    },
    '戰士': {
        'zh_TW': '戰士',
        'zh_CN': '战士',
        'en': 'Warrior',
        'ja': '戦士',
        'ko': '전사',
        'es': 'Guerrero'
    },
    '巨輪工坊厚鋼工裝': {
        'zh_TW': '巨輪工坊厚鋼工裝',
        'zh_CN': '巨轮工坊厚钢工装',
        'en': 'Great Cog Foundry Heavy Steel Overalls',
        'ja': '巨輪工房厚鋼作業着',
        'ko': '거륜공방 후강 작업복',
        'es': 'Mono de Acero Pesado del Gran Taller de Engranajes'
    },
    '巨輪工坊先鋒吊帶甲': {
        'zh_TW': '巨輪工坊先鋒吊帶甲',
        'zh_CN': '巨轮工坊先锋吊带甲',
        'en': 'Great Cog Foundry Pioneer Harness-Plates',
        'ja': '巨輪工房先鋒吊帯甲',
        'ko': '거륜공방 선봉 멜빵갑',
        'es': 'Armadura de Tirantes Pionera del Taller de Engranajes'
    },
    '原廠巨輪工坊黃銅原金': {
        'zh_TW': '原廠巨輪工坊黃銅原金',
        'zh_CN': '原厂巨轮工坊黄铜原金',
        'en': 'Stock Great Cog Foundry Brass Gold',
        'ja': '純正巨輪工房黄銅原金',
        'ko': '순정 거륜공방 황동원금',
        'es': 'Latón Dorado Original del Gran Taller de Engranajes'
    },
    '原廠黃銅原金': {
        'zh_TW': '原廠黃銅原金',
        'zh_CN': '原厂黄铜原金',
        'en': 'Stock Brass Gold',
        'ja': '純正黄銅原金',
        'ko': '순정 황동원금',
        'es': 'Latón Dorado Original'
    }
}

base_dir = '/opt/side/bravesoul-game/game/data/i18n/content'
for loc in locales:
    p = os.path.join(base_dir, loc, 'ui.json')
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    before_len = len(d)
    for k, v in data_map.items():
        d[k] = v[loc]
    after_len = len(d)
    print(f'{loc}: {before_len} -> {after_len} keys')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

print('All ui.json files updated successfully!')
