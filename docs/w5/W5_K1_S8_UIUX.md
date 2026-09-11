# W5-K1 · §8 UIUX 規格（Ken → Frank）

> Owner：Ken｜交 Frank W5-F4  
> 資料：`game/data/ken/w5_k1_s8_uiux.json`（並合併進 `w2_k1_wind_stamina.json`）

## ERR_* toast（UI 橫幅，非旁白）

| code | zh-TW toast |
|------|-------------|
| `ERR_STAMINA` | 發條不夠了 |
| `ERR_PART_LOCKED` | 這個部位還沒鬆 |

⛔ Bingo `s8.err_stamina`（「發條轉不動了——先休息。」）僅旁白／voiceover 備選，**不可**當 toast。

## FirstBreakDeadlineSec

- 常數：`60`
- 自 smoke start 起 60 秒內未完成首次部位打碎 → 強制高亮「拆解」三相鈕（pulse／glow）
- 可選 nudge 進 dismantle-ready；**不可 softlock**

## 驗收

- [ ] toast 字串＝上表；旁白不取代 toast
- [ ] `FirstBreakDeadlineSec=60` 可從 Ken／WindStamina 讀出
- [ ] 無頭 `S8_SMOKE_SUCCESS` 仍綠
