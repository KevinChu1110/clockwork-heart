#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

entries_to_remove = [
    '✦ 封靈連轉結果 ✦',
]

new_entries = {
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
    '發條解鎖 · 聚魂召喚': {
        'zh_TW': '發條解鎖 · 聚魂召喚',
        'zh_CN': '发条解锁 · 聚魂召唤',
        'en': 'Clockwork Unlock · Soul Summon',
        'ja': 'ゼンマイ解錠・魂集め召喚',
        'ko': '태엽 해제 · 집혼 소환',
        'es': 'Desbloqueo de Cuerda · Invocación de Almas',
    },
    'soul.summon_hint': {
        'zh_TW': '發條解鎖 · 聚魂召喚',
        'zh_CN': '发条解锁 · 聚魂召唤',
        'en': 'Clockwork Unlock · Soul Summon',
        'ja': 'ゼンマイ解錠・魂集め召喚',
        'ko': '태엽 해제 · 집혼 소환',
        'es': 'Desbloqueo de Cuerda · Invocación de Almas',
    },
    '普通': {
        'zh_TW': '普通',
        'zh_CN': '普通',
        'en': 'Common',
        'ja': '普通',
        'ko': '일반',
        'es': 'Común',
    },
    '優良': {
        'zh_TW': '優良',
        'zh_CN': '优良',
        'en': 'Fine',
        'ja': '上質',
        'ko': '우수',
        'es': 'Bueno',
    },
    '稀有': {
        'zh_TW': '稀有',
        'zh_CN': '稀有',
        'en': 'Rare',
        'ja': 'レア',
        'ko': '희귀',
        'es': 'Raro',
    },
    '史詩': {
        'zh_TW': '史詩',
        'zh_CN': '史诗',
        'en': 'Epic',
        'ja': 'エピック',
        'ko': '에픽',
        'es': 'Épico',
    },
    '傳奇': {
        'zh_TW': '傳奇',
        'zh_CN': '传奇',
        'en': 'Legendary',
        'ja': 'レジェンド',
        'ko': '전설',
        'es': 'Legendario',
    },
    '神話': {
        'zh_TW': '神話',
        'zh_CN': '神话',
        'en': 'Mythic',
        'ja': '神話',
        'ko': '신화',
        'es': 'Mítico',
    },
}

for loc in locales:
    p = os.path.join('/opt/side/bravesoul-game/game/data/i18n/content', loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for rk in entries_to_remove:
            if rk in d:
                del d[rk]
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
        for rk in entries_to_remove:
            if rk in d:
                del d[rk]
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p_root, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p_root}')

print('All i18n clean & updated!')
