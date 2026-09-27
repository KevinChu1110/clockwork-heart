import json

keys_to_check = [
    "長遠任務（完成後可領獎）\n\n",
    "領獎：%s",
    "（暫無待領任務）",
    "\n戰力 %d · Lv%d",
    "演武場（剩 %d）",
    "演武場（練習）",
    "野外獵場（剩 %d）",
    "野外獵場（練習）",
    "齒輪深淵（飾品 · 剩 %d）",
    "收貨！",
    "剩 %d",
    "護送 · 攔截（%s）",
    "靈寵（花 %d）",
    "旅人留言石",
    "通關燭火",
    "長遠任務",
    "每日發條",
    "今天，誰需要上發條？",
    "今天已上過發條",
    "金 %d · 星屑 %d · 經驗 %d",
    "委託「%s」：金 %d · 星屑 %d · 經驗 %d%s · 鐵屑×1",
    "此委託今日已領。",
    "尚未完成：%s",
    "找不到委託。",
    " · 升級！",
    "今日獎勵已領過。明天再來。",
    "每日補給：金 %d · 星屑 %d · 上發條累計 %d 次%s",
    "已領過此任務獎勵。",
    "條件尚未達成。",
    "任務「%s」完成：金 %d · 星屑 %d · 經驗 %d%s",
    "找不到任務。",
    "[b]今日委託[/b]（每日輪替）",
    "[b]演武場[/b]  有獎剩 %d · 最佳 %d 分",
    "[b]演武場[/b]  （進堡壘後解鎖）",
    "[b]野外獵場[/b]  有獎剩 %d",
    "[b]野外獵場[/b]  （進堡壘後解鎖）",
    "[b]旅人足跡[/b]  地圖上的半透明旅人＝殘影；留言石可留字",
    "[color=#8a8070]可領 %d · 今日待辦約 %d[/color]",
]

for lc in ["en", "ja", "zh_CN", "ko", "es"]:
    path = f"/opt/side/bravesoul-game/game/data/i18n/content/{lc}/ui.json"
    data = json.load(open(path, encoding="utf-8"))
    present = [k for k in keys_to_check if k in data]
    print(f"[{lc}] present: {len(present)} / {len(keys_to_check)}")
