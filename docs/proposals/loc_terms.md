# 在地化用語提案：品質名、「多巴胺」、保底（Pity）

> **狀態：設計提案，等 KC 確認。** 只有文件，沒改任何翻譯檔或程式。
> 遊戲現有語言：zh_TW（原文）、zh_CN、en、ja、ko、es（`game/data/i18n/content/<語言>/`）。

## 1. 「神品」「秘寶」都翻成 Legendary

### 現況（origin/main）

| 原文 | 出處 | en | es | ko | ja |
|---|---|---|---|---|---|
| 凡品／良品／上品／極品 | 裝備品質（`ui.json`） | Common／Uncommon／Rare／Epic | — | — | — |
| **秘寶** | 裝備品質最高階（`ui.json` 2500 行） | Legendary | Legendario | 전설 | 秘宝 |
| **神品** | 木人樁結算 `dummy_settlement_dialog.gd` 的 `legendary` 品質標籤 | **翻譯檔裡沒有這個 key**，各語言都會直接顯示中文「神品」 | 同左 | 同左 | 同左 |
| 傳奇 | 抽魂卡稀有度（`soul_result_card_view.gd`） | Legendary | Legendario | 전설 | レジェンド |
| 極 | 寶石 Lv5 星級（`gem_system.gd`） | Mythic | Mítico | **전설** | 極 |
| 神 | 戰魂品質（`soul.json`） | Divine | Divino | 신 | 神 |

問題：
1. **同一個品質（裝備 `legendary`）有兩個中文名**：品質表叫「秘寶」，木人樁結算叫「神品」。玩家在兩個畫面看到兩個名字。
2. **神品沒有翻譯**：英韓西日都會顯示中文。
3. **Legendary／전설 撞名**：en／es 的「秘寶」「傳奇」都是 Legendary；ko 的「秘寶」「傳奇」「極」三個都是 전설。抽魂稀有度和裝備品質是不同系統，同名會讓玩家以為是同一階。
4. 「神」（戰魂品質）跟「神品」只差一個字，但不是同一個系統。

### 建議

- **中文統一**：裝備最高品質只用「**秘寶**」，木人樁結算的「神品」改成「秘寶」（由程式改 `_t("神品")` → `_t("秘寶")`）。理由：品質表、拆解、裝備名都已經是秘寶；「神品」容易跟戰魂的「神」混在一起。
- **各語言**：裝備品質沿用通用的 Common→Legendary 階梯；其他系統避開 Legendary／전설。

| 原文（系統） | en | es | ko | ja | zh_CN |
|---|---|---|---|---|---|
| 秘寶（裝備最高品質） | Legendary（不變） | Legendario（不變） | 전설（不變） | 秘宝（不變） | 秘宝（不變） |
| 傳奇（抽魂卡稀有度） | **Fabled** | **Fabuloso** | **설화** | レジェンド（不變） | 传奇（不變） |
| 極（寶石 Lv5） | Mythic（不變） | Mítico（不變） | **신화** | 極（不變） | 极（不變） |

理由：
- 裝備的「Common → Legendary」是玩家最熟的階梯，保留給裝備。
- 抽魂稀有度另取一個字，避免跟裝備撞名。Fabled／설화（說話＝傳說故事）語意接近「傳奇」，但字面不同。
- ko 的「極」改 신화（神話），對齊 en 的 Mythic。
- ja 本來就沒撞名（秘宝／レジェンド／極），不動。

**替代方案**：若 KC 覺得「傳奇」就該叫 Legendary，那改的是裝備品質（秘寶 → en「Treasure」、ko「비보」、es「Tesoro」）。缺點：裝備品質就不再是玩家熟的 Common→Legendary 階梯。

## 2. 「多巴胺」算不算要從玩家文字拿掉的術語

### 現況

- 玩家看得到的只有兩件裝備名（`paperdoll_slots.json` 的 `name`）：「振律多巴胺亮紅散熱冠羽頭盔」「廢土多巴胺暖橘防鏽烤漆鋼板」。zh_TW／zh_CN 原樣顯示「多巴胺」；en／es／ko／ja 翻譯時都已經拿掉了（例：Resonance Scarlet Spring-Crest Cowl）。
- 其他「多巴胺金黃」「多巴胺天藍」都在美術規格欄（`accent`／`primary`／`torso_and_limbs`），玩家看不到。

### 裁定：算，從玩家文字拿掉

- 「多巴胺色系」是 2023 年左右的流行／行銷用語，指高彩度配色，**不是玩具世界觀裡的詞**。放在發條玩具的裝備名裡會出戲，而且「多巴胺」本身是化學名詞，容易讓人聯想到「刺激成癮」，對抽卡類遊戲觀感不好。
- 外文版本來就已經拿掉了，中文版拿掉後各語言就一致了。
- 美術規格欄不是玩家文字，可以保留（那是給畫師的配色描述）。

| 原文 | 建議 zh_TW | zh_CN |
|---|---|---|
| 振律多巴胺亮紅散熱冠羽頭盔 | 振律亮紅散熱冠羽頭盔 | 振律亮红散热冠羽头盔 |
| 廢土多巴胺暖橘防鏽烤漆鋼板 | 廢土暖橘防鏽烤漆鋼板 | 废土暖橘防锈烤漆钢板 |

改名要注意：名字也是翻譯檔的 key，程式改名時要同步搬動六個語言的 key（en／es／ko／ja 的譯文不用改）。

## 3. 保底（英文「Pity」讀起來怪）

### 現況

en 有 9 句用 Pity／pity，而且同一個概念有三種寫法：「Floor」（` 保底：%s`）、「Pity」、「guaranteed success pity」；「Pity Piety」更是兩個詞直譯疊在一起。es 用 Garantía／Mínimo garantizado，但抽魂那句寫成「Piedad asegurada」（直譯「憐憫」）；ko 混用 보장／천장；ja 混用 保証／最低保証／天井。

### 外部參考

- 「Pity」是玩家社群的俗稱，不是官方用語。《原神》官方規則寫的是「4★ drop guarantee」「5★ drop guarantee」，Fandom 維基也註明「pity」「banner」都是非官方用語。來源：Genshin Impact Wiki「Wish」頁（https://genshin-impact.fandom.com/wiki/Wish）、「Wanderlust Invocation」頁（https://genshin-impact.fandom.com/wiki/Wanderlust_Invocation）。
- 抽卡維基也把 pity 當成玩家的通稱，並把「累積換取」另外叫 spark：Gachawiki「Pity system」（https://gachawiki.com/wiki/pity-system.md）。
- 非抽卡的類似機制，有遊戲用「bad luck protection」（《魔獸世界》的稀有掉落），參考：GameDesign.gg 詞彙表「Pity System」（https://gamedesign.gg/glossary/pity-system/）。

> 以上只引用到這些頁面寫的內容；ko／ja 的「천장」「天井」是當地玩家常用說法，這點我沒有找官方來源，僅供參考。

### 建議：玩家文字一律用「保證」，不用 Pity

本作有兩種保底：**鍛造連敗保底**（失敗 3 次必成功）和**抽魂保底**（再 N 抽必得）。建議兩種都用「保證」這個詞，進度條統一叫「保證進度」。

| 原文 | en（現況 → 建議） | es | ko | ja |
|---|---|---|---|---|
| ` 保底：%s` | Floor → **Guarantee: %s** | Garantía: %s | 확정 보장: %s | 確定保証：%s |
| 保底已滿 3/3 · 本次升階釘釘摔錘必成功！ | Pity Full 3/3 → **Guarantee ready 3/3** · Ding's hammer throw can't miss this time! | Garantía lista 3/3 · ¡Esta vez el martillazo de Ding no falla! | 보장 완료 3/3 · 이번 승급은 딩딩 망치로 확정 성공! | 保証たまった 3/3 · 今回は釘釘の錘で必ず成功！ |
| 保底已觸發 · 釘釘發脾氣必定升階 | Pity triggered → **Guarantee used** · Ding's tantrum ensures the tier-up | Garantía usada · El berrinche de Ding asegura la subida | 보장 발동 · 딩딩이 화나서 확정 승급 | 保証発動 · 釘釘の癇癪で必ず昇階 |
| 保底虔誠 [%s] %d/%d · 再 %d 抽得碎片 | Pity Piety → **Devotion [%s] %d/%d** · %d more draws for a shard | Devoción [%s] %d/%d · %d tiradas más para un fragmento | 정성 [%s] %d/%d · %d회 더 뽑으면 조각 확정 | 信心 [%s] %d/%d · あと %d 回で欠片確定 |
| 鍛造連敗保底 %d/3 | Forge Loss Pity → **Forge Guarantee %d/3** | Garantía de forja %d/3（不變） | 제작 연패 보장 %d/3（不變） | 鍛造連敗保証 %d/3（不變） |
| 鍛造失敗！累積 1 格保底進度 | pity bar → **guarantee bar** | barra de garantía | 보장 게이지 | 保証ゲージ |
| 累積 3 次升階失敗將啟動必成功保底機制 | …guaranteed success pity → **After 3 failed upgrades, the next one is guaranteed** | Tras 3 fallos, la siguiente mejora está garantizada | 승급 3회 실패 시 다음은 확정 성공 | 昇階に3回失敗すると次は必ず成功 |
| 第七次保底啟動！突破跳階成功 | 7th pity triggered → **7th-try guarantee! Tier leap succeeded** | ¡Garantía del 7.º intento! Salto de grado logrado | 7회차 보장 발동! 단계 도약 성공 | 7回目の保証発動！跳階成功 |

理由：
- **Guarantee** 是《原神》官方規則用的詞，一般玩家（不混社群的人）也看得懂；Pity 對不玩抽卡的人來說是「可憐」的意思，讀起來像在同情玩家。
- es 統一用 Garantía，拿掉直譯的「Piedad」。
- ko 統一用 보장（保障），不用社群俗稱 천장，跟其他句子一致。
- ja 統一用 保証；「天井」是玩家俗稱，跟 ko 同理。
- 「保底虔誠」的「虔誠」是抽魂的世界觀詞（葫蘆、星曜），建議譯成 Devotion／Devoción／정성／信心，不要硬接一個 Pity。
- zh_TW／zh_CN 的「保底」本來就是玩家熟悉的中文說法，不改。

## 4. 待 KC 確認

1. 裝備最高品質的中文名統一叫「秘寶」（木人樁結算的「神品」跟著改），OK 嗎？
2. 撞名處理：保留裝備＝Legendary，抽魂「傳奇」改 Fabled／Fabuloso／설화、ko「極」改 신화？還是反過來改裝備品質？
3. 兩件裝備名拿掉「多巴胺」，OK 嗎？
4. 保底一律用 Guarantee／Garantía／보장／保証，不用 Pity／천장／天井，OK 嗎？

確認後由程式改翻譯檔（含 key 搬動）與 `dummy_settlement_dialog.gd` 的標籤，並跑 `check_content_loc`。
