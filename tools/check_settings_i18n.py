import json
import os

locales = ['zh_TW', 'zh_CN', 'en', 'ja', 'ko', 'es']
words = [
    "音量調節與聲效開關",
    "背景音樂 (BGM)",
    "戰鬥音效 (SFX)",
    "顯示模式與渲染設定",
    "全螢幕沉浸模式",
    "切換顯示模式",
    "已切換顯示模式！",
    "雲端與本機存檔備份",
    "匯出存檔備份檔 (JSON)",
    "從外部備份還原存檔",
    "存檔備份已成功匯出至本機！",
    "請選擇要還原的備份存檔...",
    "✓ 已選用",
    "語言切換",
    "聲音音效",
    "畫面顯示",
    "存檔備份",
    "系統設定",
    "請選擇您偏好的顯示語系 (即時生效)：",
    "語言已成功切換！",
    "加值權限與功能測試",
    "移除廣告（測試用開關）",
    "· 已啟用",
    "· 未啟用",
    "已啟用移除廣告功能！",
    "已重置移除廣告狀態！"
]

all_ok = True
for loc in locales:
    p = f"game/data/i18n/content/{loc}/ui.json"
    with open(p, 'r', encoding='utf-8') as f:
        d = json.load(f)
    missing = [w for w in words if w not in d and loc != 'zh_TW']
    if missing:
        print(f"[{loc}] Still missing: {missing}")
        all_ok = False
    else:
        print(f"[{loc}] All {len(words)} keys OK")

if all_ok:
    print("ALL LOCALES PASSED!")
