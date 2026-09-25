#!/usr/bin/env python3
import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']

data_map = {
    # 1. 部件名稱
    "星紋斗篷": {
        "zh_TW": "星紋斗篷",
        "zh_CN": "星纹斗篷",
        "en": "Astral Cape",
        "ja": "星紋のマント",
        "ko": "성문 망토",
        "es": "Capa Astral",
    },
    "無外裝 (裸機素體)": {
        "zh_TW": "無外裝 (裸機素體)",
        "zh_CN": "无外装 (裸机素体)",
        "en": "No Costume (Bare Frame)",
        "ja": "外装なし (素体)",
        "ko": "외형 없음 (기본 소체)",
        "es": "Sin Atuendo (Chasis Base)",
    },
    # 2. 彈窗大標題
    "發條衣櫥 · 英雄換裝": {
        "zh_TW": "發條衣櫥 · 英雄換裝",
        "zh_CN": "发条衣橱 · 英雄换装",
        "en": "Clockwork Wardrobe · Hero Outfits",
        "ja": "ゼンマイ衣装棚 · 英雄の着替え",
        "ko": "태엽 옷장 · 영웅 옷 갈아입기",
        "es": "Armario de Cuerda · Atuendos de Héroe",
    },
    "發條衣櫥・英雄換裝": {
        "zh_TW": "發條衣櫥・英雄換裝",
        "zh_CN": "发条衣橱・英雄换装",
        "en": "Clockwork Wardrobe · Hero Outfits",
        "ja": "ゼンマイ衣装棚 · 英雄の着替え",
        "ko": "태엽 옷장 · 영웅 옷 갈아입기",
        "es": "Armario de Cuerda · Atuendos de Héroe",
    },
    # 3. 副標題
    "個人化外觀部件即時切換 · 零數值純視覺展示": {
        "zh_TW": "個人化外觀部件即時切換 · 零數值純視覺展示",
        "zh_CN": "个性化外观部件即时切换 · 零数值纯视觉展示",
        "en": "Real-time appearance swap · Pure visual display without stat impact",
        "ja": "外見パーツのリアルタイム切替 · ステータス変化なしの純粋な外見変更",
        "ko": "실시간 외형 부품 변경 · 능력치 변화 없는 순수 외형 표시",
        "es": "Cambio cosmético en tiempo real · Visualización pura sin impacto en estadísticas",
    },
    # 4. 種族列提示
    "外裝庫": {
        "zh_TW": "外裝庫",
        "zh_CN": "外装库",
        "en": "Wardrobe Vault",
        "ja": "外装庫",
        "ko": "외형 보관함",
        "es": "Armario",
    },
    "點「全部」可跨族穿：騎士／法師／遊俠／格鬥／維京": {
        "zh_TW": "點「全部」可跨族穿：騎士／法師／遊俠／格鬥／維京",
        "zh_CN": "点“全部”可跨族穿：骑士／法师／游侠／格斗／维京",
        "en": "Tap \"All\" for cross-race wear: Knight / Mage / Ranger / Fighter / Viking",
        "ja": "「全部」で種族を超えて着用可能：騎士／法師／遊侠／格闘／ヴァイキング",
        "ko": "「전체」를 누르면 종족 간 교차 착용 가능: 기사／법사／레인저／격투／바이킹",
        "es": "Toca \"Todo\" para atuendos entre razas: Caballero / Mago / Explorador / Luchador / Vikingo",
    },
    # 5. 底部操作按鈕
    "還原預設": {
        "zh_TW": "還原預設",
        "zh_CN": "还原预设",
        "en": "Reset",
        "ja": "デフォルトに戻す",
        "ko": "기본값 복원",
        "es": "Restablecer",
    },
    "隨機": {
        "zh_TW": "隨機",
        "zh_CN": "随机",
        "en": "Random",
        "ja": "ランダム",
        "ko": "무작위",
        "es": "Aleatorio",
    },
    "確認換裝 · 套用新外觀": {
        "zh_TW": "確認換裝 · 套用新外觀",
        "zh_CN": "确认换装 · 套用新外观",
        "en": "Confirm Outfit · Apply New Look",
        "ja": "着替え確認 · 新しい外見を適用",
        "ko": "착용 확인 · 새 외형 적용",
        "es": "Confirmar Atuendo · Aplicar Nuevo Aspecto",
    },
    # 6. 部件區塊標題與提示
    "外裝服飾 (Costume)": {
        "zh_TW": "外裝服飾 (Costume)",
        "zh_CN": "外装服饰 (Costume)",
        "en": "Outfits (Costume)",
        "ja": "衣装 (Costume)",
        "ko": "의상 (Costume)",
        "es": "Atuendos (Costume)",
    },
    "機體塗裝 (Chassis / Paint)": {
        "zh_TW": "機體塗裝 (Chassis / Paint)",
        "zh_CN": "机体涂装 (Chassis / Paint)",
        "en": "Paint Finish (Chassis / Paint)",
        "ja": "機体塗装 (Chassis / Paint)",
        "ko": "기체 도장 (Chassis / Paint)",
        "es": "Pintura de Chasis (Chassis / Paint)",
    },
    "點擊卡片即時預覽": {
        "zh_TW": "點擊卡片即時預覽",
        "zh_CN": "点击卡片即时预览",
        "en": "Tap card to preview",
        "ja": "カードをタップしてプレビュー",
        "ko": "카드를 탭하여 미리보기",
        "es": "Toca una tarjeta para previsualizar",
    },
    # 7. 狀態標籤
    "✓ 已選用": {
        "zh_TW": "✓ 已選用",
        "zh_CN": "✓ 已选用",
        "en": "✓ Selected",
        "ja": "✓ 選択中",
        "ko": "✓ 선택됨",
        "es": "✓ Seleccionado",
    },
    # 8. 種族 chip 標籤
    "全部": {
        "zh_TW": "全部",
        "zh_CN": "全部",
        "en": "All",
        "ja": "全部",
        "ko": "전체",
        "es": "Todo",
    },
    "兔": {
        "zh_TW": "兔",
        "zh_CN": "兔",
        "en": "Rabbit",
        "ja": "兎",
        "ko": "토끼",
        "es": "Conejo",
    },
    "狐": {
        "zh_TW": "狐",
        "zh_CN": "狐",
        "en": "Fox",
        "ja": "狐",
        "ko": "여우",
        "es": "Zorro",
    },
    "獅": {
        "zh_TW": "獅",
        "zh_CN": "狮",
        "en": "Lion",
        "ja": "獅子",
        "ko": "사자",
        "es": "León",
    },
    "野豬": {
        "zh_TW": "野豬",
        "zh_CN": "野猪",
        "en": "Boar",
        "ja": "猪",
        "ko": "멧돼지",
        "es": "Jabalí",
    },
    "猴": {
        "zh_TW": "猴",
        "zh_CN": "猴",
        "en": "Monkey",
        "ja": "猿",
        "ko": "원숭이",
        "es": "Mono",
    },
    "虎": {
        "zh_TW": "虎",
        "zh_CN": "虎",
        "en": "Tiger",
        "ja": "虎",
        "ko": "호랑이",
        "es": "Tigre",
    },
    "熊": {
        "zh_TW": "熊",
        "zh_CN": "熊",
        "en": "Bear",
        "ja": "熊",
        "ko": "곰",
        "es": "Oso",
    },
    "鶴": {
        "zh_TW": "鶴",
        "zh_CN": "鹤",
        "en": "Crane",
        "ja": "鶴",
        "ko": "두루미",
        "es": "Grulla",
    },
    "企鵝": {
        "zh_TW": "企鵝",
        "zh_CN": "企鹅",
        "en": "Penguin",
        "ja": "ペンギン",
        "ko": "펭귄",
        "es": "Pingüino",
    },
    "龜": {
        "zh_TW": "龜",
        "zh_CN": "龟",
        "en": "Tortoise",
        "ja": "亀",
        "ko": "거북",
        "es": "Tortuga",
    },
    "象": {
        "zh_TW": "象",
        "zh_CN": "象",
        "en": "Elephant",
        "ja": "象",
        "ko": "코끼리",
        "es": "Elefante",
    },
    "蛙": {
        "zh_TW": "蛙",
        "zh_CN": "蛙",
        "en": "Frog",
        "ja": "蛙",
        "ko": "개구리",
        "es": "Rana",
    },
    "貓": {
        "zh_TW": "貓",
        "zh_CN": "猫",
        "en": "Panda",
        "ja": "パンダ",
        "ko": "판다",
        "es": "Panda",
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
