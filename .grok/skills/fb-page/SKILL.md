---
name: fb-page
description: 發條之心 Facebook 粉專維運。要排週檔期、寫貼文、看粉專數據、手動發文或查已發過什麼時用。所有規則與工具路徑在 docs/social/FB_OPS.md。
---

# 粉專維運入口

1. 讀 `docs/social/FB_OPS.md`（身份、工具、規則、已發過、待辦）。
2. 規劃檔期 → 叫 `marketing` subagent（阿珊），產出覆寫 `docs/social/FB_QUEUE.md`。
3. 發文由 Hermes `fb-post` cron 自動照 `FB_QUEUE.md` 發；要手動發用 `/root/fb_post.py`，發完補 `/root/.fb-warmup-state.json`。
4. 數據：`python3 /root/fb_insights.py summary`。

⛔ 權杖在 `/root/.fb-page-token`，不讀出來、不貼到任何地方。
⛔ 上架日／價格／營收／合作 → 問 Kevin。門面（頭像／封面／簡介）→ 產候選給 Kevin 挑，不自己換。
