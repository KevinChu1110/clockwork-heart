#!/usr/bin/env python3
import json
import os

repo = '/opt/side/bravesoul-game'
loc_content = os.path.join(repo, 'game/data/i18n/content')
loc_root = os.path.join(repo, 'game/data/i18n')

translations = {
    'zh_TW': {
        '已卸下所有戰魂': '已卸下所有戰魂',
        '未裝備任何戰魂': '未裝備任何戰魂',
        '已一鍵配置最高戰力戰魂': '已一鍵配置最高戰力戰魂',
        '目前已是最佳戰魂配置！': '目前已是最佳戰魂配置！',
        '一鍵卸下全部戰魂': '一鍵卸下全部戰魂'
    },
    'zh_CN': {
        '已卸下所有戰魂': '已卸下所有战魂',
        '未裝備任何戰魂': '未装备任何战魂',
        '已一鍵配置最高戰力戰魂': '已一键配置最高战力战魂',
        '目前已是最佳戰魂配置！': '目前已是最佳战魂配置！',
        '一鍵卸下全部戰魂': '一键卸下全部战魂'
    },
    'en': {
        '已卸下所有戰魂': 'All souls unequipped',
        '未裝備任何戰魂': 'No souls equipped',
        '已一鍵配置最高戰力戰魂': 'Auto-equipped best souls',
        '目前已是最佳戰魂配置！': 'Already optimal soul loadout!',
        '一鍵卸下全部戰魂': 'Unequip All Souls'
    },
    'ja': {
        '已卸下所有戰魂': 'すべての戦魂を解除しました',
        '未裝備任何戰魂': '戦魂が装備されていません',
        '已一鍵配置最高戰力戰魂': '最高戦力の戦魂を一括装着しました',
        '目前已是最佳戰魂配置！': '現在はすでに最適な戦魂配置です！',
        '一鍵卸下全部戰魂': 'すべての戦魂を一括解除'
    },
    'ko': {
        '已卸下所有戰魂': '모든 전혼을 해제했습니다',
        '未裝備任何戰魂': '장착된 전혼이 없습니다',
        '已一鍵配置最高戰力戰魂': '최고 전투력 전혼을 일괄 장착했습니다',
        '目前已是最佳戰魂配置！': '현재 이미 최적의 전혼 배치입니다!',
        '一鍵卸下全部戰魂': '모든 전혼 일괄 해제'
    },
    'es': {
        '已卸下所有戰魂': 'Todas las almas desequipadas',
        '未裝備任何戰魂': 'No hay almas equipadas',
        '已一鍵配置最高戰力戰魂': 'Almas más fuertes autoequipadas',
        '目前已是最佳戰魂配置！': '¡Ya es la mejor configuración de almas!',
        '一鍵卸下全部戰魂': 'Desequipar todas las almas'
    }
}

for lang, kv in translations.items():
    p1 = os.path.join(loc_content, lang, 'ui.json')
    if os.path.exists(p1):
        with open(p1, 'r', encoding='utf-8') as f:
            d1 = json.load(f)
        for k, v in kv.items():
            d1[k] = v
        with open(p1, 'w', encoding='utf-8') as f:
            json.dump(d1, f, ensure_ascii=False, indent=2)
        print(f'Updated {p1}')

    p2 = os.path.join(loc_root, f'{lang}.json')
    if os.path.exists(p2):
        with open(p2, 'r', encoding='utf-8') as f:
            d2 = json.load(f)
        for k, v in kv.items():
            d2[k] = v
        with open(p2, 'w', encoding='utf-8') as f:
            json.dump(d2, f, ensure_ascii=False, indent=2)
        print(f'Updated {p2}')

clean_p = os.path.join(repo, 'tools/clean_old_proofs.py')
if os.path.exists(clean_p):
    os.remove(clean_p)
