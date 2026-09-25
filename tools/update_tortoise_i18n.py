#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    '玄機龜': {
        'zh_TW': '玄機龜',
        'zh_CN': '玄机龟',
        'en': 'The Xuanji Tortoise',
        'ja': '玄機龜',
        'ko': '현기귀',
        'es': 'La Tortuga Xuanji'
    },
    '法師': {
        'zh_TW': '法師',
        'zh_CN': '法师',
        'en': 'Mage',
        'ja': '法師',
        'ko': '법사',
        'es': 'Mago'
    },
    '天元道場玄機護甲': {
        'zh_TW': '天元道場玄機護甲',
        'zh_CN': '天元道场玄机护甲',
        'en': 'Zen Dojo Xuanji Harness',
        'ja': '天元道場玄機護甲',
        'ko': '천원도장 현기호갑',
        'es': 'Armadura Xuanji del Dojo Zen'
    },
    '原廠青銅古翠綠': {
        'zh_TW': '原廠青銅古翠綠',
        'zh_CN': '原厂青铜古翠绿',
        'en': 'Stock Antique Bronze Emerald Green',
        'ja': '純正青銅古翠緑',
        'ko': '순정 청동 고취록',
        'es': 'Verde Esmeralda Bronce Antiguo Original'
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
