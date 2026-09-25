#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    "首發": {
        "zh_TW": "首發",
        "zh_CN": "首发",
        "en": "Launch",
        "ja": "初期",
        "ko": "초기",
        "es": "Lanzamiento",
    },
    "擴充": {
        "zh_TW": "擴充",
        "zh_CN": "扩充",
        "en": "Expansion",
        "ja": "拡張",
        "ko": "확장",
        "es": "Expansión",
    },
    "確認選擇 · 踏上旅途": {
        "zh_TW": "確認選擇 · 踏上旅途",
        "zh_CN": "确认选择 · 踏上旅途",
        "en": "Confirm Selection · Begin Journey",
        "ja": "選択確認 · 旅立ち",
        "ko": "선택 확인 · 여정 시작",
        "es": "Confirmar Selección · Emprender el Viaje",
    },
    "返回": {
        "zh_TW": "返回",
        "zh_CN": "返回",
        "en": "Back",
        "ja": "戻る",
        "ko": "돌아가기",
        "es": "Volver",
    },
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
    print(f'{loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

print('All ui.json files updated successfully!')
