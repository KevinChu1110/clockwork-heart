# 《發條之心》大廳角色頁三欄武器槽新增更換裝備彈窗連動武器庫 查驗清單與驗收報告 (t_a53d6368)

- **執行人**：阿宏（發條之心·程式 sideworker）
- **關聯任務**：`t_a53d6368`（🎮 遊戲開發｜大廳角色頁三欄武器槽新增更換裝備彈窗連動武器庫）
- **交付目錄**：`proofs/t_a53d6368/`
- **遵循規範**：
  - `review.md` 規範：740~760px 多巴胺橫屏彈窗、按鈕熱區 >= 48px、立體果凍厚底 5px、零 Emoji、粉圓體 (Open Huninn)。
  - `clock-review-checklist.md`：
    - 連續截圖不可重複（SHA256 不得相同），存證對齊驗收項目與完整互動過程。
    - 彈窗與卡片正確佈局尺寸（custom_minimum_size / min_size），避免坍塌或溢出。
    - 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換支援。
    - `clock-check` 自動化檢查全部通過。

---

## 一、 實機全景截圖核驗清單（1280x720）

| 編號 | 實機截圖檔名 | 涵蓋內容 | 破圖 | 零Emoji | 零截字 | SHA256 (前12碼) | 驗證結果 |
|---|---|---|:---:|:---:|:---:|---|:---:|
| 01 | `proof_01_character_tab_before.png` | 角色頁裝備分頁（未開彈窗，展示首選/副手/絕技槽位與「更換裝備」按鈕） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `0378d0a02322` | 合格 (PASS) |
| 02 | `proof_02_weapon_swap_dialog_open.png` | 多巴胺風格武器選擇彈窗（750px 橫屏置中、三欄 Tab、武器庫候選清單、屬性說明與按鈕） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `b718fd575d28` | 合格 (PASS) |
| 03 | `proof_03_character_tab_after_swap.png` | 更換裝備後角色頁即時刷新（武器槽位、攻擊力/戰力數值連動、紙娃娃連動） | ✓ 無破圖 | ✓ 零Emoji | ✓ 零截字 | `6626eba04794` | 合格 (PASS) |

- **防作弊校驗**：三張實機截圖 SHA256 完全獨立互異（無重複上傳冒充）。
- **Vision 視覺審核**：經 Vision 驗證，彈窗居中精準，圓角 16~22px，字級階梯清晰，按鈕熱區與立體果凍厚底完整呈現。

---

## 二、 語系對照與詞條清單

所有玩家可見文字均透過 `ContentLoc.text("ui", ...)` / `_t()` 對接 `game/data/i18n/content/<locale>/ui.json`：

| 來源原文 (zh_TW) | 英文 (en) | 日文 (ja) | 韓文 (ko) | 西班牙文 (es) | 簡體中文 (zh_CN) |
|---|---|---|---|---|---|
| 更換裝備 | Change Equipment | 装備変更 | 장비 교체 | Cambiar equipo | 更换装备 |
| 武器庫 · 更換裝備 | Armory · Change Equipment | 武器庫 · 装備変更 | 무기고 · 장비 교체 | Armería · Cambiar equipo | 武器库 · 更换装备 |
| 選擇要裝備至【%s】的武器 · 即時連動紙娃娃與屬性 | Select weapon for [%s] · Live paperdoll & stat sync | 【%s】に装備する武器を選択 · 着せ替えとステータス即時連動 | [%s]에 장착할 무기 선택 · 외형 및 능력치 즉시 연동 | Selecciona arma para [%s] · Sincronización en vivo | 选择要装备至【%s】的武器 · 实时连动纸娃娃与属性 |
| 背包與庫存尚無可替換武器 | No alternative weapons in inventory | バッグとインベントリに交換可能な武器がありません | 가방과 보관함에 교체 가능한 무기가 없습니다 | No hay armas alternativas en el inventario | 背包与库存尚无可替换武器 |
| 可前往冒險出征獲取或在鍛造殿堂打造新武器 | Acquire from adventure sorties or forge in the Hall | 冒険の出征で入手するか鍛冶の殿堂で作成できます | 모험 출정에서 획득하거나 대장간에서 제작할 수 있습니다 | Consíguelas en expediciones o forja en la Sala | 可前往冒险出征获取或在锻造殿堂打造新武器 |
| 卸下武器 | Unequip | 武器を外す | 무기 해제 | Desequipar | 卸下武器 |
| 使用中 | In Use | 使用中 | 사용 중 | En uso | 使用中 |
| 裝備 | Equip | 装備 | 장착 | Equipar | 装备 |
| 調換至此欄 | Swap to this slot | この欄に付け替え | 이 슬롯으로 변경 | Cambiar a esta ranura | 调换至此栏 |
| 其他欄位使用中 | In other slot | 他のスロットで使用中 | 다른 슬롯에서 사용 중 | En otra casilla | 其他栏位使用中 |
| 當前槽位裝備中 | Equipped in slot | 現在のスロットに装備中 | 현재 슬롯 장착 중 | Equipado aquí | 当前槽位装备中 |
| 需達 Lv%d 解鎖 | Requires Lv%d | Lv%d で解放 | Lv%d 시 해금 | Requiere Nv.%d | 需达 Lv%d 解锁 |
| 當前槽位尚未裝備武器 | No weapon equipped in this slot | 現在スロットに武器が装備されていません | 현재 슬롯에 무기가 장착되지 않았습니다 | No hay arma equipada en esta ranura | 当前槽位尚未装备武器 |
| 點擊武器卡片即可立即更換，即時更新戰鬥屬性與外觀紙娃娃 | Click a weapon to equip immediately · Live stat and appearance update | 武器カードをクリックすると即座に変更され、能力値と外見が更新されます | 무기 카드를 클릭하면 즉시 교체되며 전투 능력치와 종이인형이 갱신됩니다 | Toca un arma para equiparla al instante · Actualiza atributos y aspecto | 点击武器卡片即可立即更换，实时更新战斗属性与外观纸娃娃 |

---

## 三、 測試覆蓋與驗證結果

1. **無頭冒煙測試**：
   - `godot --path game --headless --quit-after 3`：0 SCRIPT ERROR，編譯與加載完全正常。
2. **單元與驗收測試**：
   - `res://scripts/ui/test_lobby_weapon_swap_dialog.gd`：
     - ✓ 角色頁三欄武器槽按鈕與「更換裝備」按鈕結構、熱區 >= 48px、立體厚底 5px、零 Emoji。
     - ✓ 彈窗寬度 750px（740~760px 規範）、置中 ModalScrim 攔截點擊、右上關閉鈕 >= 48px。
     - ✓ 背包與庫存武器候選清單讀取、品質色階、流派打擊數、屬性說明正確。
     - ✓ 裝備更換後 `GameState.weapon_loadout`、`GameState.equip_slots["weapon"]`、`GameState.path_style` 正確同步。
     - ✓ 面板攻擊力（`effective_atk`）與有效戰力（`power_score`）即時刷新。
     - ✓ 副手欄位（Lv10 解鎖）裝備與卸下武器功能，卸下道具正確回流 `equip_bag`。
     - ✓ 六語系（zh_TW / zh_CN / en / ja / ko / es）即時動態切換全部通過且零 Emoji。
     - ✓ 產出 3 張實機截圖存證且 SHA256 獨立互異。
     - 測試結論：`TEST_LOBBY_WEAPON_SWAP_DIALOG_OK` 通過。
3. **既有迴歸測試**：
   - `res://scripts/ui/test_lobby_weapon_loadout_live.gd`：`LOBBY_WEAPON_LOADOUT_LIVE_OK` 通過。
   - `res://scripts/ui/test_mobile_lobby.gd`：`MOBILE_LOBBY_OK` 通過。
4. **自動化審查檢查器**：
   - `/root/bin/clock-check /opt/side/bravesoul-game`：
     - `✅ 全過：素材都有 .import、路徑與 autoload 接上、語系 key 齊、沒有舊名詞`。
