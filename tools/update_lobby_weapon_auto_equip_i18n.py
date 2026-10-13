#!/usr/bin/env python3
import json
import os

repo = '/opt/side/bravesoul-game'
loc_content = os.path.join(repo, 'game/data/i18n/content')
loc_root = os.path.join(repo, 'game/data/i18n')

translations = {
    'zh_TW': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': '戰力提升 +%d！已一鍵配置最高戰力武器。',
        '已一鍵配置最高戰力武器。': '已一鍵配置最高戰力武器。',
        '目前已是最佳武器配置！': '目前已是最佳武器配置！'
    },
    'zh_CN': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': '战力提升 +%d！已一键配置最高战力武器。',
        '已一鍵配置最高戰力武器。': '已一键配置最高战力武器。',
        '目前已是最佳武器配置！': '当前已是最佳武器配置！'
    },
    'en': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': 'Power +%d! Equipped highest power weapons.',
        '已一鍵配置最高戰力武器。': 'Equipped highest power weapons.',
        '目前已是最佳武器配置！': 'Already at optimal weapon configuration!'
    },
    'ja': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': '戦力 +%d！最高戦力の武器を一括装着しました。',
        '已一鍵配置最高戰力武器。': '最高戦力の武器を一括装着しました。',
        '目前已是最佳武器配置！': '現在は最適な武器配置です！'
    },
    'ko': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': '전투력 +%d! 최고 전투력 무기를 일괄 장착했습니다.',
        '已一鍵配置最高戰力武器。': '최고 전투력 무기를 일괄 장착했습니다.',
        '目前已是最佳武器配置！': '현재 최적의 무기 배치입니다!'
    },
    'es': {
        '戰力提升 +%d！已一鍵配置最高戰力武器。': '¡Poder +%d! Armas de mayor poder equipadas.',
        '已一鍵配置最高戰力武器。': 'Armas de mayor poder equipadas.',
        '目前已是最佳武器配置！': '¡Ya está en la configuración óptima de armas!'
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
