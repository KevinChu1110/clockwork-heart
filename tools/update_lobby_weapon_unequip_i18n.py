#!/usr/bin/env python3
import json
import os

repo = '/opt/side/bravesoul-game'
loc_content = os.path.join(repo, 'game/data/i18n/content')
loc_root = os.path.join(repo, 'game/data/i18n')

translations = {
    'zh_TW': {
        '已將副武器卸下歸還背包！': '已將副武器卸下歸還背包！',
        '當前無可卸下的武器！': '當前無可卸下的武器！'
    },
    'zh_CN': {
        '已將副武器卸下歸還背包！': '已将副武器卸下归还背包！',
        '當前無可卸下的武器！': '当前无可卸下的武器！'
    },
    'en': {
        '已將副武器卸下歸還背包！': 'Secondary weapons unequipped and returned to bag!',
        '當前無可卸下的武器！': 'No weapons to unequip currently!'
    },
    'ja': {
        '已將副武器卸下歸還背包！': '副武器を外してバッグに戻しました！',
        '當前無可卸下的武器！': '現在外せる武器がありません！'
    },
    'ko': {
        '已將副武器卸下歸還背包！': '보조 무기를 해제하여 가방에 보관했습니다!',
        '當前無可卸下的武器！': '현재 해제할 수 있는 무기가 없습니다!'
    },
    'es': {
        '已將副武器卸下歸還背包！': '¡Armas secundarias desequipadas y devueltas a la bolsa!',
        '當前無可卸下的武器！': '¡No hay armas para desequipar actualmente!'
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
