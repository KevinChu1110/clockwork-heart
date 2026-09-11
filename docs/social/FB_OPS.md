# 發條之心 · 粉專維運交接（Hermes 阿珊 → Grok Build，2026-09-11）

> 這份是**操作手冊 + 交接狀態**。團隊手法與審稿標準看 `MARKETING_TEAM.md`，
> 素材製作準則看 `BRAND_ASSETS.md`，產圖產影片工具看 `MEDIA_GEN.md`。
> 以上四份原本只存在 Hermes 的 profile 裡，2026-09-11 起以 repo 這份為準。

## 粉專身份

| 項目 | 值 |
|---|---|
| 粉專 | **發條之心 Clockwork Heart**（舊名「勇者之魂 Brave Soul」，腳本註解還沒改） |
| Page ID | `1335191403004011` |
| 網址 | https://www.facebook.com/1335191403004011 |
| 官網（可放） | https://kevinchu1110.github.io/clockwork-heart/ |
| 現況 | 2026-09-11：讚 1、已發 2 則（見下方「已發過」） |
| 權杖 | **永不過期的粉專權杖**，在 pdc-hermes `/root/.fb-page-token`（600 權限）。⛔ 不進 repo、不貼到任何文件或訊息 |
| App | 「粉專自動發文工具」（Graph API v21.0） |

## 工具（都在 pdc-hermes 的 `/root/`，不在 repo）

```bash
python3 /root/fb_post.py whoami                          # 確認接到哪個粉專
python3 /root/fb_post.py recent 5                        # 看最近幾則
python3 /root/fb_post.py draft "<文案>" [圖.png]          # 存未發佈草稿（拿不準就用這個）
python3 /root/fb_post.py text  "<文案>"                   # 純文字
python3 /root/fb_post.py photo "<文案>" a.png [b.png]     # 帶圖（多張＝相簿）
python3 /root/fb_post.py video "<文案>" v.mp4 [標題]      # 影片（FB 排進 Reels 版位）
python3 /root/fb_insights.py summary                     # 真實數據（page + 最近貼文）；沒數字就是沒數字，不准編
/root/gameplay_capture.sh 20 /tmp/play.mp4 [res://scripts/dev/capture_xxx.gd]   # Xvfb 實機錄影，真畫面
python3 /root/discord_send.py docs/social/FB_QUEUE.md    # 把文件貼到 Discord 給 Kevin 看
python3 /root/discord_file.py "<說明>" 檔案...            # 傳圖/影片到 Discord
```

## 發佈規則（Kevin 2026-09-04 定案，交接後不變）

1. **內容必須來自 repo 已寫定的文案**（`FB_QUEUE.md`）。⛔ 不准臨場自編就發。要發新東西：先寫進文件、審過、下一輪再發。
2. **一天最多一則**；同一則不重複發。發完記進 `/root/.fb-warmup-state.json`（`posted[]`：day / persona / topic / output / posted_at / asset）。
3. ⛔ 上架日期、價格、營收數字、與他人合作 → 一律先問 Kevin。
4. 全數標 `#開發中`；不放未上線商店連結。
5. 素材優先序：實機錄影 > `screenshots/` 現有截圖 > `branding/key_visual_main.png` > 產圖（必帶 `--ref` 主視覺）> AI 影片（一週一部，先問）。**不用 AI 畫面冒充實機。**
6. 門面（頭像／封面／簡介）是品牌決策：產好候選 → Kevin 挑 → 他手動換。候選在 `FB_PROFILE.md`。

## 每週流程（原本是 Hermes `marketing-round` 週日 15:00，交接後由 Grok 端執行）

1. `git log --since="7 days ago" --oneline` → 這週真的做出什麼（素材只能用真的存在的畫面）
2. `python3 /root/fb_insights.py summary` → 上週真實反應（前兩週數字沒參考價值，不拿數據退稿）
3. 四位 persona（阿哲／小魚／Ken／小玩）各出一則草案，見 `MARKETING_TEAM.md`
4. 審稿：**四篇必須明顯不同**，至少一則平台機制路線；對照當週素材；誠實；有看數據
5. 過稿寫進 `FB_QUEUE.md`（**只放下一週**，覆蓋上週）；退稿寫明理由
6. 檔期貼到 Discord 給 Kevin 看

## 發文執行：誰按下去

- **Hermes 的 `fb-post` cron 仍在跑**（週四／週五／週日 12:00 與 20:00，profile side）：讀 `FB_QUEUE.md` + 狀態檔，當天有排且沒發過就發，發完回 Discord。
  → 所以 Grok 端只要把 `FB_QUEUE.md` 排好、素材檔存在，發文會自動發生。
- 想手動發：直接 `fb_post.py photo/video`，**發完自己把狀態檔補一筆**，不然 cron 會重發。
- 要停自動發文：`ssh pdc-hermes 'hermes --profile side cron pause 8a4885c16a3f'`（resume 同 id）。

## 已發過（截至 2026-09-11）

| 日期 | Persona | 內容 | 素材 | FB id |
|---|---|---|---|---|
| 09-09 12:28 | 阿哲 | 世界觀開場長文（Day 1） | `branding/key_visual_main.png` | `1335191403004011_122110055883447337` |
| 09-11 12:05 | 小玩 | 部位鎖定暫停挑戰短影音（Day 3） | `web/media/shorts/mk_shorts_soul_battle_polish_30s.mp4` | video `2076963246544696` |

當週檔期還沒發的：Day 2 小魚（30s 實機短影音，週四 20:00）、Day 4 Ken（四英雄二選一投票，週日 12:00）。
⚠️ Day 2 和 Day 3 用同一支影片，Day 3 已經先發了，Day 2 要不要換素材由本週審稿決定。

## 未完成／待 Kevin 的事

- 粉專**簡介空白、沒有封面**：候選在 `FB_PROFILE.md`（兩版簡介、三款 1640×624 封面），等 Kevin 挑
- Hermes side-market 看板 `t_9aeb7b0a`「粉專門面」卡在 blocked，就是等上面這件
- `fb_post.py` 的 docstring 與 `PAGE_ID` 註解還寫「勇者之魂」，改名前先確認 Kevin 要不要保留舊名

## 歷史文件對照

| 檔案 | 狀態 |
|---|---|
| `FB_QUEUE.md` | **當週檔期，唯一有效的發文來源** |
| `FB_QUEUE_R01.md` / `FB_QUEUE_R02.md` | 前幾輪存檔，只供參考 |
| `FB_QUEUE.old-world.md` | 舊世界觀（像素 RPG 時期），作廢 |
| `FB_WARMUP.md` | 最初四週構想，只當素材參考，不照抄 |
| `FACEBOOK.md` | 建粉專步驟 + 第一週 7 則舊稿，作廢大半 |
| `FB_PROFILE.md` | 門面候選，有效 |
