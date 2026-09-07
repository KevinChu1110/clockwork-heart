# 發條之心 · Facebook 當週發文檔期（冷啟動第一週 · 3 則）

一次只排一週。本週粉專 0 貼文、0 讚、0 追蹤（`fb_insights.py` 無數據可對），前兩週不拿數據退稿。

廢止上一版 W4 幽靈檔：`web/media/shorts/w04_touch_break_20s.mp4`、`w04_play_mechanism_14s.mp4`、紫微星盤長文、七殺 vs 紫微投票——那些檔不存在，也不再排。

三則都標 `#開發中`。⛔ 不上架日、⛔ 不放未上線商店連結。官網可以放：https://kevinchu1110.github.io/clockwork-heart/

發文前提：文案已在本檔；門面簡介／封面見 `docs/social/FB_PROFILE.md`（Kevin 手動換）。**未審過不要發。**

---

## 當週 3 則

| 序 | 建議時段 | Persona | 形式 | 素材（必須存在） | 追蹤 |
|---|---|---|---|---|---|
| Day 1 | 週二 20:00 | 阿哲 | 世界觀開場長文 | `branding/key_visual_main.png` | 分享／長文停留 |
| Day 2 | 週四 20:00 | 小魚 | 20 秒真機 | `web/media/hero/fb_lobby.mp4` | 完播／重播 |
| Day 3 | 週六 12:00 | Ken | 四英雄二選一 | `branding/key_visual_main.png` | 留言／觸及 |

素材自檢（發文前記得再跑一次）：

```
test -f branding/key_visual_main.png
test -f web/media/hero/fb_lobby.mp4
test -f web/media/social/fb_cover_toy.png
```

---

### Day 1 · 阿哲（內容行銷）· 374 字

- **圖**：`branding/key_visual_main.png`
- **發法**（審過後）：`python3 /root/fb_post.py photo "<文案>" branding/key_visual_main.png`

```
世界停了。不是天崩地裂，是秒針不跳了。

發條玩具一隻隻僵在最後一個姿勢：眼珠裡的光熄掉，關節鎖死。對牠們來說，停一百年和停一秒沒有差別——只要有人再轉一次鑰匙。

問題是：誰來轉？

《發條之心》的起點，是一隻米白金屬打造的發條兔。牠叫小白。胸口有一顆孤品級的發條之心，還在轉。背後的黃銅鑰匙不知被誰上過弦。在一個灑滿晨光的閣樓角落，有人在牠耳邊說過一句話：「動起來吧，小傢伙，去看看這個停下來的世界。」

大鐘在雲海頂端。修好它，停擺的同胞才會再動。小白不是來拯救人類大陸的勇者——牠是玩具堆裡第一隻還醒著的秒針。

遊戲還在開發。這則只講世界從哪裡開始，不講什麼時候能玩。

官網 https://kevinchu1110.github.io/clockwork-heart/

#發條之心 #ClockworkHeart #開發中 #世界觀
```

---

### Day 2 · 小魚（短影音）· 107 字

- **片**：`web/media/hero/fb_lobby.mp4`（1280×720、20s、H.264、真機）
- **發法**（審過後）：`python3 /root/fb_post.py video "<文案>" web/media/hero/fb_lobby.mp4 "大廳 20 秒"`
- **誠實**：這支是舊大廳實機（糖果風、角色名 Capoo），**不是**發條定調後的畫面。文案必須講「不是最終長相」，不准寫成現況預告片。

```
20 秒，真機，不是概念圖。

點大廳裡的角色：姿勢會換，對話會冒出來。這支是目前能公開的實機畫面——美術還在換成發條玩具定調，所以你看到的大廳不是最終長相。

#發條之心 #ClockworkHeart #開發中
```

下一週若有發條定調的 20 秒實機，再換掉這支。

---

### Day 3 · Ken（社群互動）· 123 字

- **圖**：`branding/key_visual_main.png`（四英雄現成視覺）
- **發法**（審過後）：`python3 /root/fb_post.py photo "<文案>" branding/key_visual_main.png`

```
圖上四隻都是發條玩具：獅拿槍、兔拿劍、狐拿杖、豬拿錘。

第一場只能帶一隻。你站誰旁邊？

A 小白（劍）——聽齒輪異音、拆零件
B 雷歐（槍）——正面硬剛

留言只回一個字母：A 或 B。

#發條之心 #ClockworkHeart #開發中
```

---

## 主管自檢

1. **差異度**：長文世界觀／真機短片／二選一投票，三則切口不同。
2. **素材**：三條路徑 `test -f` 都在。W4 短影音已刪出檔期。
3. **誠實**：無上架日、無商店；Day 2 不拿舊大廳冒充發條定調。
4. **數據**：粉專零基礎，本週不對照上輪數字。

週日用 `python3 /root/fb_insights.py summary` 收一次，當下一週唯一依據。
