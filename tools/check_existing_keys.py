import json

proposed_keys = [
    "星紋斗篷",
    "無外裝 (裸機素體)",
    "發條衣櫥 · 英雄換裝",
    "發條衣櫥・英雄換裝",
    "個人化外觀部件即時切換 · 零數值純視覺展示",
    "外裝庫",
    "點「全部」可跨族穿：騎士／法師／遊俠／格鬥／維京",
    "還原預設",
    "隨機",
    "確認換裝 · 套用新外觀",
    "外裝服飾 (Costume)",
    "機體塗裝 (Chassis / Paint)",
    "點擊卡片即時預覽",
    "✓ 已選用",
    "全部",
    "兔", "狐", "獅", "野豬", "猴", "虎", "熊", "鶴", "企鵝", "龜", "象", "蛙", "貓"
]

with open('/opt/side/bravesoul-game/game/data/i18n/content/en/ui.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for k in proposed_keys:
    if k in d:
        print(f"ALREADY EXISTS: {k} -> {d[k]}")
    else:
        print(f"NEW KEY: {k}")
