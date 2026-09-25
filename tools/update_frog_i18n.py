#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
data_map = {
    '碧箸蛙': {
        'zh_TW': '碧箸蛙',
        'zh_CN': '碧箸蛙',
        'en': 'The Spring-Leg Frog',
        'ja': '碧箸蛙',
        'ko': '벽저와',
        'es': 'Rana de Resorte de Jade'
    },
    '碧簧蛙': {
        'zh_TW': '碧簧蛙',
        'zh_CN': '碧簧蛙',
        'en': 'The Spring-Leg Frog',
        'ja': '碧箸蛙',
        'ko': '벽저와',
        'es': 'Rana de Resorte de Jade'
    },
    '忍者': {
        'zh_TW': '忍者',
        'zh_CN': '忍者',
        'en': 'Ninja',
        'ja': '忍者',
        'ko': '닌자',
        'es': 'Ninja'
    },
    '碧箸巡林客工裝': {
        'zh_TW': '碧箸巡林客工裝',
        'zh_CN': '碧箸巡林客工装',
        'en': 'Spring Forest Courier Overalls',
        'ja': '碧箸巡林客作業着',
        'ko': '벽저 순림객 작업복',
        'es': 'Mono de Guardabosques de Jade'
    },
    '碧簧巡林客工裝': {
        'zh_TW': '碧簧巡林客工裝',
        'zh_CN': '碧簧巡林客工装',
        'en': 'Spring Forest Courier Overalls',
        'ja': '碧箸巡林客作業着',
        'ko': '벽저 순림객 작업복',
        'es': 'Mono de Guardabosques de Jade'
    },
    '原廠薄荷翡翠綠': {
        'zh_TW': '原廠薄荷翡翠綠',
        'zh_CN': '原厂薄荷翡翠绿',
        'en': 'Stock Mint Emerald Green',
        'ja': '純正ミントエメラルドグリーン',
        'ko': '순정 민트 에메랄드 그린',
        'es': 'Verde Esmeralda Menta Original'
    },
    '原廠薄荷翡翠綠琺瑯烤漆': {
        'zh_TW': '原廠薄荷翡翠綠琺瑯烤漆',
        'zh_CN': '原厂薄荷翡翠绿珐琅烤漆',
        'en': 'Stock Mint Emerald Green Enamel Lacquer',
        'ja': '純正ミントエメラルドグリーンエナメル塗装',
        'ko': '순정 민트 에메랄드 그린 에나멜 칠',
        'es': 'Pintura de Esmalte Verde Esmeralda Menta Original'
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
