import json

locales = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
keys_to_check = [
    "機體外觀 · 發條紙娃娃",
    "更衣 · 發條衣櫥",
    "武器輪替配置",
    "點擊切換輪替順位 · 三段作戰序列",
    "首選武器", "副手武器", "絕技武器",
    "鐵劍", "獵弓", "拳套",
    "4 次打擊", "5 連擊",
    "首選武器 · 鐵劍：近身迅捷連續 4 次斬擊，戰鬥開局起手輪替順位",
    "副手武器 · 獵弓：中距離精準連續 4 次射擊，壓制敵陣並牽制推進",
    "絕技武器 · 拳套：重裝近身蓄力 5 連擊，滿怒時超頻運轉爆發絕技",
    "機體戰鬥屬性",
    "有效戰力 %d",
    "生命力 (HP)", "機體核心",
    "物理攻擊", "打擊破壞",
    "物理防禦", "減傷防護",
    "暴擊率", "弱點致命",
    "怒氣量表", "滿怒超頻運轉 +25% 性能",
    "20 點"
]

for loc in locales:
    p = f"/opt/side/bravesoul-game/game/data/i18n/content/{loc}/ui.json"
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    found = [k for k in keys_to_check if k in data]
    print(f"{loc}: {len(found)}/{len(keys_to_check)} found -> {found}")
