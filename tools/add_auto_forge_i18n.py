#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

new_entries = {
    '一鍵鍛造': {
        'zh_TW': '一鍵鍛造',
        'zh_CN': '一键锻造',
        'en': 'Auto Forge',
        'ja': '一括鍛造',
        'ko': '일괄 단조',
        'es': 'Forja Automática',
    },
    '一鍵鍛造完成！成功 %d 次（嘗試 %d 次）· 攻擊力 +%d · 消耗 %d 金幣、%d 鐵屑': {
        'zh_TW': '一鍵鍛造完成！成功 %d 次（嘗試 %d 次）· 攻擊力 +%d · 消耗 %d 金幣、%d 鐵屑',
        'zh_CN': '一键锻造完成！成功 %d 次（尝试 %d 次）· 攻击力 +%d · 消耗 %d 金币、%d 铁屑',
        'en': 'Auto Forge done! Succeeded %d times (%d tries) · ATK +%d · Cost %d Gold, %d Iron Scrap',
        'ja': '一括鍛造完了！成功 %d 回（試行 %d 回）· 攻撃力 +%d · 消費 %d ゴールド、%d 鉄くず',
        'ko': '일괄 단조 완료! 성공 %d회(시도 %d회) · 공격력 +%d · 소모 %d 골드, %d 고철',
        'es': '¡Forja automática completa! Éxito %d veces (%d intentos) · ATQ +%d · Coste %d Oro, %d Chatarra',
    },
    '一鍵鍛造結束：嘗試 %d 次全數失敗 · 消耗 %d 金幣、%d 鐵屑': {
        'zh_TW': '一鍵鍛造結束：嘗試 %d 次全數失敗 · 消耗 %d 金幣、%d 鐵屑',
        'zh_CN': '一键锻造结束：尝试 %d 次全数失败 · 消耗 %d 金币、%d 铁屑',
        'en': 'Auto Forge ended: %d tries all failed · Cost %d Gold, %d Iron Scrap',
        'ja': '一括鍛造終了：%d 回試行すべて失敗 · 消費 %d ゴールド、%d 鉄くず',
        'ko': '일괄 단조 종료: %d회 시도 모두 실패 · 소모 %d 골드, %d 고철',
        'es': 'Forja automática finalizada: %d intentos fallidos · Coste %d Oro, %d Chatarra',
    },
    '鐵屑不足！一鍵鍛造需要鐵屑穩火。': {
        'zh_TW': '鐵屑不足！一鍵鍛造需要鐵屑穩火。',
        'zh_CN': '铁屑不足！一键锻造需要铁屑稳火。',
        'en': 'Not enough Iron Scrap! Auto Forge requires scrap to steady heat.',
        'ja': '鉄くず不足！一括鍛造には火力を安定させる鉄くずが必要です。',
        'ko': '고철 부족! 일괄 단조에는 화력을 안정시킬 고철이 필요합니다.',
        'es': '¡Chatarra de hierro insuficiente! La forja automática requiere chatarra para templar el fuego.',
    },
    '金幣不足！無法進行一鍵鍛造。': {
        'zh_TW': '金幣不足！無法進行一鍵鍛造。',
        'zh_CN': '金币不足！无法进行一键锻造。',
        'en': 'Not enough gold! Cannot perform Auto Forge.',
        'ja': 'ゴールド不足！一括鍛造を実行できません。',
        'ko': '골드 부족! 일괄 단조를 진행할 수 없습니다.',
        'es': '¡Oro insuficiente! No se puede realizar la forja automática.',
    },
    '目前條件無法進行一鍵鍛造。': {
        'zh_TW': '目前條件無法進行一鍵鍛造。',
        'zh_CN': '当前条件无法进行一键锻造。',
        'en': 'Cannot perform Auto Forge under current conditions.',
        'ja': '現在の条件では一括鍛造を実行できません。',
        'ko': '현재 조건에서는 일괄 단조를 진행할 수 없습니다.',
        'es': 'No se puede realizar la forja automática en las condiciones actuales.',
    },
}

for loc in locales:
    p = os.path.join('/opt/side/bravesoul-game/game/data/i18n/content', loc, 'ui.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
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
        for k, v in new_entries.items():
            d[k] = v[loc]
        with open(p_root, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Updated {p_root}')

print('All i18n updated successfully!')
