import json
import os

base = '/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_f800a6fa/bravesoul-game/game/data/i18n/content'
translations = {
    'zh_TW': {
        '機芯五槽配置': '機芯五槽配置',
        '點擊更換裝備 · 強化核心機芯': '點擊更換裝備 · 強化核心機芯',
        '背包暫無此部位可替換機芯': '背包暫無此部位可替換機芯',
        '更換裝備': '更換裝備',
    },
    'zh_CN': {
        '機芯五槽配置': '机芯五槽配置',
        '點擊更換裝備 · 強化核心機芯': '点击更换装备 · 强化核心机芯',
        '背包暫無此部位可替換機芯': '背包暂无此部位可替换机芯',
        '更換裝備': '更换装备',
    },
    'en': {
        '機芯五槽配置': '5 Core Slots Configuration',
        '點擊更換裝備 · 強化核心機芯': 'Tap to swap · Enhance core mechanisms',
        '背包暫無此部位可替換機芯': 'No replaceable core parts for this slot in bag',
        '更換裝備': 'Change Equipment',
    },
    'ja': {
        '機芯五槽配置': '五大コアスロット配置',
        '點擊更換裝備 · 強化核心機芯': 'タップで装備変更 · コアを強化',
        '背包暫無此部位可替換機芯': 'バッグに該当部位の交換用コアパーツがありません',
        '更換裝備': '装備変更',
    },
    'ko': {
        '機芯五槽配置': '코어 5슬롯 구성',
        '點擊更換裝備 · 強化核心機芯': '터치하여 장비 교체 · 코어 강화',
        '背包暫無此部位可替換機芯': '가방에 해당 부위의 교체 가능한 코어 부품이 없습니다',
        '更換裝備': '장비 교체',
    },
    'es': {
        '機芯五槽配置': 'Configuración de 5 Ranuras de Núcleo',
        '點擊更換裝備 · 強化核心機芯': 'Toca para cambiar equipo · Mejorar núcleos',
        '背包暫無此部位可替換機芯': 'Sin piezas de núcleo reemplazables para esta ranura en la mochila',
        '更換裝備': 'Cambiar equipo',
    }
}

for lang, items in translations.items():
    p = os.path.join(base, lang, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for k, v in items.items():
            d[k] = v
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        print(f'Updated {lang}/ui.json')
