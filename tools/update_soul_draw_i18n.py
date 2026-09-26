#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    # ── 抽魂主畫面標題 ──
    "抽魂 · 封靈罐": {
        "zh_TW": "抽魂 · 封靈罐",
        "zh_CN": "抽魂 · 封灵罐",
        "en": "Soul Draw · Soul Canister",
        "ja": "抽魂 · 封霊缶",
        "ko": "추혼 · 봉령캔",
        "es": "Extracción de Almas · Recipiente de Almas",
    },
    "soul.draw_title": {
        "zh_TW": "抽魂 · 封靈罐",
        "zh_CN": "抽魂 · 封灵罐",
        "en": "Soul Draw · Soul Canister",
        "ja": "抽魂 · 封霊缶",
        "ko": "추혼 · 봉령캔",
        "es": "Extracción de Almas · Recipiente de Almas",
    },

    # ── 抽一格主按鈕 ──
    "上緊——抽一格": {
        "zh_TW": "上緊——抽一格",
        "zh_CN": "上紧——抽一格",
        "en": "Wind Up — Draw 1",
        "ja": "巻き上げ——一回引く",
        "ko": "태엽 감기——1칸 뽑기",
        "es": "Dar Cuerda — Extraer 1",
    },
    "soul.btn_pull": {
        "zh_TW": "上緊——抽一格",
        "zh_CN": "上紧——抽一格",
        "en": "Wind Up — Draw 1",
        "ja": "巻き上げ——一回引く",
        "ko": "태엽 감기——1칸 뽑기",
        "es": "Dar Cuerda — Extraer 1",
    },

    # ── 次按鈕（去玩具堆邊緣） ──
    "去玩具堆邊緣": {
        "zh_TW": "去玩具堆邊緣",
        "zh_CN": "去玩具堆边缘",
        "en": "To the Toy-pile Edge",
        "ja": "玩具の山の縁へ",
        "ko": "장난감 더미 가장자리로",
        "es": "Ir a la orilla del montón",
    },
    "soul.btn_continue": {
        "zh_TW": "去玩具堆邊緣",
        "zh_CN": "去玩具堆边缘",
        "en": "To the Toy-pile Edge",
        "ja": "玩具の山の縁へ",
        "ko": "장난감 더미 가장자리로",
        "es": "Ir a la orilla del montón",
    },

    # ── 票數資訊 ──
    "封靈票 ×%d · 今日已抽 %d": {
        "zh_TW": "封靈票 ×%d · 今日已抽 %d",
        "zh_CN": "封灵票 ×%d · 今日已抽 %d",
        "en": "Soul Tickets ×%d · Pulled Today: %d",
        "ja": "封霊券 ×%d · 本日抽選 %d",
        "ko": "봉령 티켓 ×%d · 오늘 뽑기 %d",
        "es": "Boletos de Alma ×%d · Extraídas Hoy: %d",
    },
    "soul.tickets_status": {
        "zh_TW": "封靈票 ×%d · 今日已抽 %d",
        "zh_CN": "封灵票 ×%d · 今日已抽 %d",
        "en": "Soul Tickets ×%d · Pulled Today: %d",
        "ja": "封霊券 ×%d · 本日抽選 %d",
        "ko": "봉령 티켓 ×%d · 오늘 뽑기 %d",
        "es": "Boletos de Alma ×%d · Extraídas Hoy: %d",
    },

    # ── 錯誤提示 ──
    "封靈票不足": {
        "zh_TW": "封靈票不足",
        "zh_CN": "封灵票不足",
        "en": "Not enough Soul Tickets",
        "ja": "封霊券が不足しています",
        "ko": "봉령 티켓 부족",
        "es": "Boletos de alma insuficientes",
    },
    "soul.err_tickets": {
        "zh_TW": "封靈票不足",
        "zh_CN": "封灵票不足",
        "en": "Not enough Soul Tickets",
        "ja": "封霊券が不足しています",
        "ko": "봉령 티켓 부족",
        "es": "Boletos de alma insuficientes",
    },
    "今天抽魂次數滿了，明天再轉": {
        "zh_TW": "今天抽魂次數滿了，明天再轉",
        "zh_CN": "今天抽魂次数满了，明天再转",
        "en": "Daily soul pulls are full — come back tomorrow",
        "ja": "本日の抽魂上限に達しました。明日また回してください",
        "ko": "오늘의 혼 뽑기 횟수가 가득 찼습니다. 내일 다시 돌려주세요",
        "es": "Límite diario de invocaciones alcanzado, vuelve mañana",
    },
    "err.daily_cap_pull": {
        "zh_TW": "今天抽魂次數滿了，明天再轉",
        "zh_CN": "今天抽魂次数满了，明天再转",
        "en": "Daily soul pulls are full — come back tomorrow",
        "ja": "本日の抽魂上限に達しました。明日また回してください",
        "ko": "오늘의 혼 뽑기 횟수가 가득 찼습니다. 내일 다시 돌려주세요",
        "es": "Límite diario de invocaciones alcanzado, vuelve mañana",
    },
}

# 1. 更新 game/data/i18n/content/<loc>/ui.json
content_dir = 'game/data/i18n/content'
for loc in locales:
    p = os.path.join(content_dir, loc, 'ui.json')
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    before_len = len(d)
    for k, v in data_map.items():
        d[k] = v[loc]
    after_len = len(d)
    print(f'[content/ui.json] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write('\n')

# 2. 同步更新 game/data/i18n/<loc>.json（滿足 Loc.t 根層查找）
root_i18n_dir = 'game/data/i18n'
for loc in locales:
    p = os.path.join(root_i18n_dir, f'{loc}.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        before_len = len(d)
        for k, v in data_map.items():
            d[k] = v[loc]
        after_len = len(d)
        print(f'[root i18n] {loc}: {before_len} -> {after_len} keys (+{after_len - before_len})')
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')

print('Soul Draw i18n files updated successfully!')
