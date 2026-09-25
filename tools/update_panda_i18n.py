#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    '瓷韻熊貓': {
        'zh_TW': '瓷韻熊貓',
        'zh_CN': '瓷韵熊猫',
        'en': 'The Porcelain Panda',
        'ja': '磁韻パンダ',
        'ko': '도운 판다',
        'es': 'Panda de Porcelana'
    },
    '武術家': {
        'zh_TW': '武術家',
        'zh_CN': '武术家',
        'en': 'Monk',
        'ja': '武術家',
        'ko': '무술가',
        'es': 'Monje'
    },
    '禪道學徒生漆長袍': {
        'zh_TW': '禪道學徒生漆長袍',
        'zh_CN': '禅道学徒生漆长袍',
        'en': 'Zen Apprentice Lacquer Robe',
        'ja': '禅道見習い生漆長袍',
        'ko': '선도 견습생 옻칠 도포',
        'es': 'Túnica de Laca de Aprendiz Zen'
    },
    '羊脂白瓷生漆塗裝': {
        'zh_TW': '羊脂白瓷生漆塗裝',
        'zh_CN': '羊脂白瓷生漆涂装',
        'en': 'Mutton-Fat White Porcelain Lacquer',
        'ja': '羊脂白磁生漆塗装',
        'ko': '양지백자 옻칠 도장',
        'es': 'Pintura de Laca de Porcelana Blanca'
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
