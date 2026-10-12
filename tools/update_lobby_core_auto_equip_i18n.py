#!/usr/bin/env python3
import json
import os

repo = '/opt/side/bravesoul-game'
loc_content = os.path.join(repo, 'game/data/i18n/content')
loc_root = os.path.join(repo, 'game/data/i18n')

translations = {
    'zh_TW': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': '戰力提升 +%d！已一鍵配置最高戰力機芯。',
        '目前已是最佳機芯配置！': '目前已是最佳機芯配置！'
    },
    'zh_CN': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': '战力提升 +%d！已一键配置最高战力机芯。',
        '目前已是最佳機芯配置！': '当前已是最佳机芯配置！'
    },
    'en': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': 'Power +%d! Equipped highest power cores.',
        '目前已是最佳機芯配置！': 'Already at optimal core configuration!'
    },
    'ja': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': '戦力 +%d！最高戦力のコアを一括装着しました。',
        '目前已是最佳機芯配置！': '現在は最適なコア配置です！'
    },
    'ko': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': '전투력 +%d! 최고 전투력 코어를 일괄 장착했습니다.',
        '目前已是最佳機芯配置！': '현재 최적의 코어 배치입니다!'
    },
    'es': {
        '戰力提升 +%d！已一鍵配置最高戰力機芯。': '¡Poder +%d! Núcleos de mayor poder equipados.',
        '目前已是最佳機芯配置！': '¡Ya está en la configuración óptima de núcleos!'
    }
}

for lang, kv in translations.items():
    # 1. content/{lang}/ui.json
    p1 = os.path.join(loc_content, lang, 'ui.json')
    if os.path.exists(p1):
        with open(p1, 'r', encoding='utf-8') as f:
            d1 = json.load(f)
        for k, v in kv.items():
            d1[k] = v
        with open(p1, 'w', encoding='utf-8') as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
        print(f'Updated {p1}')

    # 2. {lang}.json
    p2 = os.path.join(loc_root, f'{lang}.json')
    if os.path.exists(p2):
        with open(p2, 'r', encoding='utf-8') as f:
            d2 = json.load(f)
        for k, v in kv.items():
            d2[k] = v
        with open(p2, 'w', encoding='utf-8') as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
        print(f'Updated {p2}')
