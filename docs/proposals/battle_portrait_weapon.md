# 提案：戰鬥立繪要不要顯示「實際裝備的武器」（#74）

> **狀態：草案，待 KC 決定。** 對應 issue：#74（承接 #72／PR #73 的發現）。
> 本文件只做現況調查、數量盤點和選項比較，**不改戰鬥規則、數值或程式**。
> 盤點基準：`origin/main` `ad28947d`（2026-10-12）。數字都是在這個 commit 上數出來的，不是估的；估算的會標「估」。

## 0. 一句話結論

- 裝備表（`game/data/tables/equipment.json`）有 **28 個武器 id，沒有任何一個**能在 69 個種族裡的任何一族解析到戰鬥立繪用的 512 武器圖（用 `PaperdollRenderer.resolve_slot_texture_path_512` 逐族逐 id 實測，命中 0）。
- 現在立繪上出現的武器，只有兩種來源：**種族預設武器**（61 族有圖、8 族沒有），或大廳換武器時用「武器系 → 圖」小對照表硬湊的結果（只對 12 個族、24 個 race×武器組合有效；其餘會寫成 `"none"`，變成空手）。
- 玩家換了什麼武器，立繪大多不會變；少數情況還會**變空手**，比「不變」更糟。

---

## 1. 現況：立繪武器圖是怎麼選的

### 1.1 戰鬥待機立繪（idle）

1. `battle_view.gd` 的 `_apply_battle_art()` 先呼叫 `WindingKeyAnimator.setup_for(player_body, race, slots)`，`slots` 來自 `GameState.paperdoll_slots`（**不是裝備欄**）。
2. `WindingKeyAnimator.build_body_texture_no_key()` 呼叫 `PaperdollRenderer.build_composite_texture_512(race, slots)` 合成無鑰匙的素體圖。
3. `slots["weapon"]` 的值決定武器圖層：
   - **空字串（沒設定）**：`_get_default_variant_id(race, "weapon")` 給種族預設武器，例如兔 `wpn_dawn_blade`、狐 `wpn_astral_staff`、狼 `weapon_wolf_scrap_sawblade_greatsword`。
   - **`"none"`**：不畫武器層，**空手**。
   - **某個 id**：只找「本族」的 `paperdoll/<race>/weapon/<id>_512.png`（武器 512 解析**不會跨族借圖**，`paperdoll_renderer.gd` 的 `resolve_slot_texture_path_512` 末尾也明寫武器不退回 61×72 HUD 小圖），找不到就**空手**。
4. 所以裝備 id（`rusty_blade`、`star_rod` …）直接放進 `slots["weapon"]` 一定找不到圖。

### 1.2 退回路徑（沒有攻擊姿勢圖的種族）

- 攻擊／受擊／技能等姿勢，`_set_player_pose()` 先找 `SpriteDB.player_pose(pose, race)`（`assets/sprites/player/poses/<race>/<pose>_512.png`，**武器是畫死在圖裡的**）。
- 找不到就退回 `_get_player_equipped_idle_texture()`（`battle_view.gd` 約 2329 行）：若 `slots["weapon"]` 是空的，就把**裝備欄武器的 `base_id`** 塞進去，然後合成。因為 `base_id` 沒有對應圖，多數種族變**空手**（PR #73 的探針圖已證實）。
- 有姿勢圖的種族：56／69；沒有的：**13 族**（capybara、caterpillar、cuttlefish、donkey、falcon、giraffe、gorilla、kite、meerkat、peacock、salamander、scorpion、squirrel）。其中 capybara、caterpillar、cuttlefish、falcon、kite、meerkat、peacock、scorpion 這 8 族**連預設武器圖也沒有**，不管走哪條路都是空手。

### 1.3 大廳的另一套硬湊（容易被忽略）

`game/scripts/ui/mobile_lobby.gd` 的 `_sync_hero_weapon_paperdoll()`（4671 行起）會在換武器、切武器槽、關武器彈窗時，把 `GameState.paperdoll_slots["weapon"]` **改寫**成：

- 候選：裝備 `base_id` → `WEAPON_LINE_TO_PAPERDOLL[武器系]`（4630 行，12 個武器系各對一張 `wpn_*`）→ 原始 id。
- 逐個用 `resolve_slot_texture_path_512(race, "weapon", cid)` 試，第一個找得到本族 512 圖的就用；**全找不到就寫 `"none"`**。

問題是 12 張 `wpn_*_512.png` **各只屬於一個種族**（`wpn_dawn_blade` 只有兔、`wpn_astral_staff` 只有狐…）。所以只有「該族剛好擁有該武器系的那張圖」才命中。**這個值會存進存檔**（`paperdoll_slots` 會序列化）。

> 這一段是讀程式碼得出的推論，沒有實際在大廳點過；PR #73 觀察到的「idle 永遠是種族預設武器」是**沒碰過大廳換武器**時的情況。建議實作前先在實機驗證一次。

---

## 2. 真實數量（逐項可重現）

方法：Godot headless 逐族逐 id 呼叫 `resolve_slot_texture_path_512`，再加上檔案系統盤點。

| 項目 | 數量 | 說明 |
|---|---:|---|
| 種族數 | **69** | `assets/sprites/player/paperdoll/<race>/` |
| 裝備 base id 總數 | 44 | `equipment.json` 的 `bases` |
| 其中武器槽 | **28** | 其餘 16 個是防具／飾品（armor 7、necklace 2、amulet 2、ring 2、earring 1、bracelet 1、belt 1），不屬於本議題 |
| 武器系（`line`） | **14** | sword 5、iron 3、bow 2、dagger 2、fist 2、axe 2、spear 2、gun 2、dart 2、crystal 2、magic 1、claw 1、soul 1、hammer 1 |
| **缺立繪武器圖的武器 id** | **28／28** | 實測 28 個 id × 69 族，0 命中 |
| 起始武器 | 69 族 → **13 個不同 id** | anvil_hammer、ash_spear、flint_gun、hunt_claw、meager_edge、mist_darts、notch_axe、reed_bow、rusty_blade、shard_focus、star_fang、star_rod、wrap_gloves；13 個都缺圖 |
| 種族預設武器 512 圖 | **61 張**（61 族各 1 張） | 13 張 `wpn_*`（原始 13 族）＋ 48 張 `weapon_<race>_*`；皆為 512×512 整張畫布 |
| 完全沒有預設武器圖的種族 | **8** | capybara、caterpillar、cuttlefish、falcon、kite、meerkat、peacock、scorpion（資料夾只有 `.gitkeep`） |
| `WEAPON_LINE_TO_PAPERDOLL` 涵蓋的武器系 | 12／14 | 缺 `iron`（3 個 id）和 `soul`（1 個 id）＝**4 個 id 完全沒對照** |
| 大廳硬湊後「立繪真的是裝備武器」的 race×武器組合 | **24／1932（1.2%）** | 1932＝69 族×28 武器；24＝12 個武器系各自只對 1 個族（rabbit 吃 5 個劍、lion 2、…） |
| 以起始武器計：硬湊後立繪武器正確的種族 | **11／69** | rabbit、lion、fox、boar、tiger、crane、penguin、tortoise、elephant、frog、panda |
| 以起始武器計：硬湊後會變空手的種族 | **58／69** | 其中 50 族本來有預設武器圖（等於**被硬湊弄丟**），8 族本來就沒有 |

> 補充：武器圖是**整張 512 畫布**，連「握武器的手」一起畫、位置依種族手的位置而定（目視 rabbit／fox／hound 的圖確認）。所以同一把武器**不能直接跨族共用**，這是下面選項 A 工作量大的根本原因。
>
> 另外，各族 `weapon/` 目錄下的 128×128 圖（61 張）是 512 圖的低解析版；共用的 `paperdoll/weapon/<裝備id>.png`（27 張）是 72 px 背包小圖示，**不能**拿來當立繪（程式也明確禁止）。

---

## 3. 選項比較

> 以下三個選項來自 issue #74 原文；我另外補一個 A 的變體（A′），標明是補充。

### 選項 A：做「裝備 → 立繪武器圖」對照表，請美術補圖

**要補多少圖（估）**

| 粒度 | 公式 | 張數 | 備註 |
|---|---|---:|---|
| A-1 每族×每個武器系 | 69 族 × 14 系 − 現有 61 | **約 905**（上限） | 同系不同階共用一張；現有 61 張假設都剛好能抵一格，實際可能更多 |
| A-2 每族×每個武器 id | 69 族 × 28 id − 現有 61 | **約 1,871**（上限） | 每階都有不同外觀 |
| A-3 只補起始武器 | 69 族 × 1（各族自己的起始武器） | **約 69 − 現有可用張數** | 只解決「起始」，換了別的武器還是不變 |
| A′（補充）共用武器圖層＋握點資料 | 28（或 14）張**去手**武器圖 ＋ 69 筆握點／角度資料 | **14–28 張圖**＋資料 | 要先改現有 61 張（把手和武器分層），再改 renderer；不是純補圖 |

- 每張圖要花多少美術時間：**未查證**（repo 裡沒有這個紀錄，需美術回報）。以下工時只估工程，美術工時請美術另估。
- 攻擊／受擊／技能姿勢（56 族 × 5 張 = 280 張，另有 47 張 idle）**武器是畫在姿勢圖裡的**（目視 wolf 的 `attack_512.png` 手持的是弓，跟 idle 的劍不同）。選項 A 如果只做 idle 合成，**攻擊一出手武器就會換回姿勢圖裡畫死的那把**，反而更突兀。要一起解決得重畫姿勢圖，或改成「攻擊姿勢圖不含武器、武器另外疊」，工作量再翻很多倍。

**優點**
- 唯一真正達成「換武器立繪就變」的方案，對標手遊的回饋缺口才算補上。
- 可以順便讓裝備的外觀分階（高階武器看起來更好），成為養成的視覺獎勵。

**缺點／風險**
- 張數大（A-1 約 905、A-2 約 1,871），美術時間和風格一致性是最大風險。
- 姿勢圖的武器是畫死的，單做 idle 會前後不一致（見上）。
- 要擴 `WEAPON_LINE_TO_PAPERDOLL` 或新增資料表，並處理存檔裡已存的 `paperdoll_slots["weapon"]`。
- 包體會變大（核心 PCK 已 49.03 MB，見 `docs/W3_CORE_SIZE.md`；每張 512 圖的大小要實測，**未查證**）。

**工程工時（估，不含美術）**：對照表＋載入＋存檔相容＋測試約 **2–4 人天**；A′ 另加 renderer 分層和握點工具約 **5–10 人天**。這是我的判斷估算，不是量測。

### 選項 B：退回路徑也用種族預設武器，至少不空手

**做什麼**
1. `battle_view.gd` 的 `_get_player_equipped_idle_texture()`：不要把裝備 `base_id` 塞進 `slots["weapon"]`（issue 的 B）。
2. **同時**處理 `mobile_lobby.gd` 的 `_sync_hero_weapon_paperdoll()`：找不到對應圖時寫 `""`（用預設武器）而不是 `"none"`。否則 §2 的 58 族會繼續空手。issue 沒提到這一點，是我調查時新發現的。

**優點**
- 改動小（兩處、各幾行），不動規則和數值，不需要美術。
- 消除「變空手」的退步；idle、退回路徑、大廳三處行為一致。
- 可以先做，不會擋 A。

**缺點／風險**
- 看不到實際裝備的武器，**對標缺口沒有解決**。
- 8 族沒有預設武器圖，還是空手，要另外請美術補（8 張，比 A 小很多，可視為 B 的附帶項）。
- 要確認 `"none"` 是否還有「玩家刻意卸武器」的語意（`_sync_hero_weapon_paperdoll()` 在沒裝備時也寫 `"none"`，這個要保留）。

**工程工時（估）**：約 **0.5–1 人天**（含一支測試：69 族全部 idle 都有武器層，8 族除外）。

### 選項 C：先做 B，A 依 #55 對標結論排優先

**做什麼**：B 照上面做；A 不立刻開工，等 #55（PR #58）的對標結論和 KC 對美術預算的決定。

**優點**
- 最快止血、不押注大量美術。
- 讓 KC 有時間先用 1 個族做 A′ 的原型，再決定要不要走全量。

**缺點／風險**
- 缺口短期內不補，換武器立繪仍不變。
- 如果 #55 之後沒有人排 A，會變成永遠停在 B。
- 目前 `docs/BENCHMARK.md` 還沒有「換裝立繪要變」這一條；若 KC 選 C，我可以在 #55 補一條加分項。

**工程工時（估）**：B 的工時＋決策會議；A 之後另算。

---

## 4. 比較表

| | A | B | C |
|---|---|---|---|
| 換武器立繪會變 | ✅ | ❌ | ❌（之後才可能） |
| 美術需求 | 約 905–1,871 張（A′ 14–28 張＋改圖） | 0（8 族補預設圖另算） | 0（A 之後另算） |
| 工程（估） | 2–4 人天（A′ 5–10） | 0.5–1 人天 | 0.5–1 人天 |
| 風險 | 美術量、姿勢圖不一致、包體 | 低 | 低 |
| 是否擋後續 | 否 | 否 | 否 |

---

## 5. 建議（溫和，待 KC 決定）

> **這只是調查者的傾向，不是決定。**

我傾向 **選項 C**：

1. 先做 B（兩處小改），因為大廳硬湊會把 58 族弄成空手，這是現在就存在的退步，修起來很便宜。
2. A 先不全量開工。若要走 A，建議先挑 1–2 個族試做 A′（共用去手武器圖＋握點），拿到實際單張美術時間和包體大小，再決定 A-1／A-2／A′。
3. 不管選哪個，**姿勢圖畫死武器**的問題要一起決定，否則單做 idle 會前後不一致。

## 6. 待 KC 決定

| 編號 | 問題 | 選項 |
|---|---|---|
| Q1 | 選哪個方向 | A／B／C |
| Q2 | 若走 A，粒度 | A-1 每族×武器系／A-2 每族×每個武器／A-3 只補起始武器／A′ 共用武器圖層 |
| Q3 | 攻擊等姿勢圖裡畫死的武器怎麼處理 | 維持不管／重畫／改成不含武器再疊 |
| Q4 | 8 個沒有預設武器圖的族（capybara、caterpillar、cuttlefish、falcon、kite、meerkat、peacock、scorpion）要不要補 | 補／暫不補 |
| Q5 | `iron`（3 個 id）和 `soul`（1 個 id）兩個武器系沒有對照，要歸到哪個外觀系 | 歸入既有系／各補一張 |

## 7. 驗證方式（給 QA／實作者）

- 盤點可重現：`godot --headless --path game -s <探針腳本>`，對 69 族×28 武器呼叫 `PaperdollRenderer.resolve_slot_texture_path_512(race, "weapon", id)`，統計非空字串數。
- 做完 B 之後的驗收：69 族（扣掉 8 個沒有預設圖的）idle 立繪都有武器層；在大廳換武器、重開遊戲、進戰鬥，立繪都不變成空手；`test_character_creation_flow` 照常通過。
- 做完 A 之後的驗收：每個武器 id 在每個種族都解析得到圖（解析結果不為空）；攻擊姿勢前後武器外觀一致。

## 8. 引用的程式與資料

- `game/scripts/battle/battle_view.gd`：`_apply_battle_art()`、`_set_player_pose()`、`_get_player_equipped_idle_texture()`
- `game/scripts/art/winding_key_animator.gd`：`setup_for()`、`build_body_texture_no_key()`
- `game/scripts/art/paperdoll_renderer.gd`：`resolve_slot_texture_path_512()`、`_get_default_variant_id()`
- `game/scripts/art/sprite_db.gd`：`player_equipped_idle()`、`player_pose()`
- `game/scripts/ui/mobile_lobby.gd`：`WEAPON_LINE_TO_PAPERDOLL`、`_resolve_hero_weapon_paperdoll_id()`、`_sync_hero_weapon_paperdoll()`
- `game/scripts/systems/equipment_system.gd`：`RACE_STARTER_WEAPONS`（69 族）
- `game/data/tables/equipment.json`：`bases`
- PR #73（#72）：探針圖與決策說明
