# 發條之心 · Facebook 粉專門面（簡介／封面／Graph 欄位）

粉專：**發條之心 Clockwork Heart**（id `1335191403004011`）  
https://www.facebook.com/1335191403004011

本文件只準備文案與圖檔，**不擅自改線上門面**（換簡介／封面／頭像要 Kevin 在後台按）。對齊 `docs/world/CANON.md`：發條玩具兔小白、玩具世界停擺、官網、#開發中。

⛔ 已作廢、不要再貼回粉專：五色葫蘆、傭兵團最弱新人、魔王敗後二十年、Q 萌像素／浮空島糖果大廳當門面定調。

---

## 現況（2026-09-07 Graph 實測）

| 欄位 | 現值 |
|---|---|
| name | 發條之心 Clockwork Heart |
| category | Game Publisher |
| about / description / cover | **空**（無簡介、無封面） |
| picture | 預設剪影（未設頭像） |
| website | `https://kevinchu1110.github.io/bravesoul-game`（舊路徑，需改） |
| fan_count / followers_count | 0 / 0 |
| 貼文 | 0 |

---

## 一、簡介（About）· 125 字

給粉專首頁「簡介」欄。100–150 字，含官網與 #開發中。

```
《發條之心》開發中。玩具世界停了：大鐘不走，發條玩具僵在原地。米白金屬發條兔「小白」胸口那顆發條之心還在轉，拿著齒輪短劍走進被遺忘的玩具堆。官網 https://kevinchu1110.github.io/clockwork-heart/ #開發中
```

字數：含空白 125、去空白 123。不承諾上架日、不放商店連結。

---

## 二、封面橫幅

| 項目 | 值 |
|---|---|
| 檔案 | `web/media/social/fb_cover_toy.png` |
| 規格 | 1640×624（Facebook 封面 @2x） |
| 來源 | 自 `branding/key_visual_main.png`（1376×768）全寬裁切，y=244 起取 524px 高再放大 |
| 畫面 | 四隻發條英雄（獅槍／兔劍／狐杖／豬錘）＋中央發條核心；切掉原圖頂部字標殘邊 |
| 上傳 | Meta Business Suite → 粉專封面。**不要用 API 直接換。** |

舊檔 `web/media/social/fb_cover.png`、`fb_cover_alt.png`、`web/media/hero/fb_cover_1.png` 是上一輪候選，門面改用 `fb_cover_toy.png`。

頭像此次不換（現成 `fb_avatar.png` 未必是發條定調）。要換另開任務給 Kevin 挑。

---

## 三、Graph API 欄位建議值（給 Kevin 手動填）

只改這三個。權杖不要拿去 PATCH。

| Graph 欄位 | 建議值 | 後台位置 |
|---|---|---|
| `about` | 上面「簡介」全文（125 字） | 粉專設定 → 關於 |
| `website` | `https://kevinchu1110.github.io/clockwork-heart/` | 關於 → 網站（覆蓋現在的 bravesoul-game） |
| cover photo | 上傳 `web/media/social/fb_cover_toy.png` | 粉專封面 |
| 行動呼籲 | 「了解更多」→ 同上官網 | 粉專按鈕 |

可選（不一定有欄位）：

| 欄位 | 建議值 |
|---|---|
| `description` / 詳細介紹 | 玩具世界停擺。主角是米白金屬發條兔「小白」。遊戲開發中，進度看官網。#開發中 |
| category | 維持 Game Publisher |

核對：改完後 `about` 非空、`website` 指向 clockwork-heart、封面非空。可用：

```
python3 /root/fb_post.py whoami
```

再 vis 粉專頁確認封面有圖。

---

*整理：2026-09-07 · 對齊 CANON，舊勇者之魂門面文案作廢*
