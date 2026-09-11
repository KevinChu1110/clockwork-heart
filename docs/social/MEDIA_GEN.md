> 2026-09-11 自 Hermes 移入 repo；工具在 pdc-hermes /root/gen_media.py（走 hermes 的 xai-oauth 憑證）。

# 產圖、產影片、產音樂、查趨勢

## ⭐ 2026-09-07 起：產圖與產影片預設走 Grok

`gen_media.py` 的 `--backend` **預設是 `grok`**（走 Kevin 的 SuperGrok 訂閱，
`hermes auth` 的 `xai-oauth` 憑證）。要用 Gemini 得明寫 `--backend gemini`。

為什麼換：同一組 `art_direction.md` §6.2 提示詞兩邊對跑，Grok 對
「破舊機械玩具」的質感理解明顯更準——刮痕與掉漆層次、螺絲鉚釘的分件、
胡桃鉗配色的飽和度、角色表情都比較到位。Gemini 留著當備援與比對用。

### 影像

```bash
python3 /root/gen_media.py image "<提示詞>" out.png            # 預設 grok-imagine-image
python3 /root/gen_media.py image "<提示詞>" out.png --model grok-imagine-image-quality   # 要品質
python3 /root/gen_media.py image "<提示詞>" out.png --backend gemini --aspect 4:5        # 要指定比例
```

⚠️ **xAI 沒有 aspectRatio 參數**，比例只能寫進提示詞（`vertical 9:16 composition`）。
要精確控制比例就用 Gemini。

### 影片

```bash
python3 /root/gen_media.py video "<提示詞>" out.mp4 --seconds 15 --image 首幀.png
```

- **時長 1～15 秒**（Veo 只有 8 秒）。15 秒代表**整支預告可以一鏡生成**，
  不必再做「取末幀 → 接龍 → xfade」那套，美術也就不會在接縫處漂移。
- 首幀走 `--image`，構圖不會跑掉。
- 產出 848×480 24fps 含 AAC 音軌。**480p 做短影音夠，做官網主視覺不夠**。
- ⚠️ **影片維持一週一部的量**。Kevin 說計費不用擔心是建立在這個量上，
  要大量產之前先問他。

### 模型分層（2026-09-07）

| 誰 | 模型 | 為什麼 |
|---|---|---|
| `sideworker`（做事的） | `grok-4.6` | 實作與轉譯吃判斷力 |
| `side-producer` / `side-review` / `side-ideas` / `marketing-round` | `grok-4.6` | 決策與審稿吃判斷力 |
| `side-live`（每 3 分鐘）/ `side-progress` / `fb-post` | Gemini flash | 高頻回報，要便宜 |

⛔ 不要把 `side-live` 改成 Grok，它一天跑 480 次。


## 現況一覽（不要假設沒列出來的東西能用）

| 能力 | 狀態 | 怎麼用 |
|------|------|--------|
| 產圖（Gemini） | ✅ 可用 | `/root/gen_media.py image` |
| 產影片（Veo） | ✅ 可用但**要先問 Kevin** | `/root/gen_media.py video` |
| 產圖（fal） | ❌ **不用**（Kevin 決定不儲值） | 帳號無餘額，呼叫必定 403。⛔ 不要嘗試 |
| 產音樂（Suno） | ❌ 沒有 | Suno 無公開 API，fal 也不用了。需要音樂先問 Kevin |
| 網頁設計（Lovable） | ❌ 不接 | 沒有 API。而且你本來就會寫 HTML/CSS，直接改比較快 |
| 發 Facebook 貼文 | ❌ 沒有權限 | 只能**準備內容**，Kevin 自己發 |
| 查熱門風格 | ✅ 免金鑰 | `web_search` |

## 產圖與產影片：`/root/gen_media.py`

Hermes 內建的 `image_gen` 外掛沒有 Google provider，所以走這支自寫的 CLI（直接打 Gemini API）：

```bash
python3 /root/gen_media.py models                                    # 這把金鑰能用哪些影像／影片模型
python3 /root/gen_media.py image "<提示詞>" 輸出.png --ref 參考圖.png  # 產圖
python3 /root/gen_media.py video "<提示詞>" 輸出.mp4 --seconds 8       # 產影片（Veo，非同步）
```

- 影像預設 `gemini-3.1-flash-image`；要更好的品質用 `gemini-3-pro-image`
- **`--ref` 帶參考圖可以延續既有風格** —— 做遊戲宣傳素材時務必帶一張現有畫面，
  不然產出來的東西跟遊戲長得不像，做出來也不能用
- 影片是 Veo，送出後輪詢，通常一到數分鐘

## ⛔ 用量規矩

- **圖片**：一次任務最多 3 張，且只在任務明確需要素材時才產
- **影片（Veo）一律先問 Kevin 再產** —— 貴，而且一次要好幾分鐘
- 產出的素材放 `/tmp` 或任務工作區，**不要 commit 進 repo**，除非任務明講要入庫
- 沿用專案憲章「付費 API 先問 Kevin」的精神：圖片有上述配額所以可自行判斷，超出配額就用 clarify 問

## 查熱門風格：`web_search`

免金鑰可用（Hermes 走免費輪替），做行銷或美術方向提案前可以先查再提。

但**查到的趨勢要落回我們自己的證據**：對照 12 週短影音表排到哪、最近 commit 做出了什麼畫面、
現有美術方向是什麼。⛔ 不要直接照抄別人的做法當提案 —— 沒有扣回自己專案的趨勢報告沒有價值。

## 行銷素材的交付方式

我們**沒有 Facebook 粉專的發文權限**，所以行銷任務的產出一律是「Kevin 可以直接複製貼上就發」的東西：
完整文案（不是綱要）、指定用哪張現有素材、建議發文時段。不要寫成「建議可以考慮…」。
