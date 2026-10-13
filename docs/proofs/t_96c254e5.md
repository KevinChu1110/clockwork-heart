# 全面回歸驗收證明 · 鐵匠機芯卸下、背包戰魂快捷、聚魂殿背包快捷等後五分支合進主線 (t_96c254e5)

## 1. 任務背景與驗收目標
本卡為平台與維運整併卡（`t_96c254e5`），承接第一批合併卡（`t_9d9c55bf`，commit `8341a60b6`）完成後，將以下五個已由測試小婷（`sideqa`）完成獨立驗收並簽核通過之核心養成與快捷連動分支完整整合進 `main` 主線：

1. **`forge-core-unequip-all`（t_571a8f41）**：分支 `origin/agent/20261013-forge-core-unequip-all-t_571a8f41`
   - 天宮鐵匠 `ForgeDialog` 機芯五槽新增『一鍵卸下全部機芯』果凍按鈕（`BtnUnequipAllCores`，高 46px，熱區 >= 48px，珊瑚粉 #FF5E8A，深藍紫描邊 #1F1A3A，厚底 5px，圓角 16px，與一鍵校準按鈕成對並列，零系統 Emoji）。
   - 連動 `CoreSystem.unequip_part` 遍歷卸下五大槽位機芯至未裝備背包，戰力即時刷新，Toast「已卸下所有機芯」，空槽防呆提示「未裝備任何機芯」，六語系支援。
2. **`inventory-soul-shortcut`（t_3726e90e）**：分支 `origin/agent/20261013-inventory-soul-shortcut-t_3726e90e`
   - `MapleInventory` 探索背包戰魂素材（`windup_fragment`, `soul_crystal`）詳情新增『前往聚魂』快捷果凍按鈕（`BtnGoSoul`，高 52px，熱區 >= 48px，金黃 #FFD028，深藍紫描邊 #1F1A3A，厚底 5px，圓角 18px，字級 18px，零系統 Emoji）。
   - 發射 `go_soul_hall_requested` 訊號關閉背包並直通大廳聚魂殿堂（`Tab.SOUL_HALL`），互斥隱藏其他快捷鈕，六語系支援。
3. **`soul-hall-inventory-shortcut`（t_13a0ab72）**：分支 `origin/agent/20261013-soul-hall-inventory-shortcut-t_13a0ab72`
   - 大廳聚魂殿堂底欄新增『前往背包』快捷果凍按鈕（`BtnGoInventory`，高 52px，寬 200px，熱區 >= 48px，珊瑚粉 #FF5E8A，深藍紫描邊 #1F1A3A，厚底 5px，圓角 18px，字級 16px，與吸收灰魂、聚魂十連並列，零系統 Emoji）。
   - 點擊後直通探索背包並自動切換至素材分類頁籤（`material`），達成背包與聚魂殿雙向閉環，六語系支援。
4. **`energy-lack-shop-shortcut`（t_f25c0492）**：分支 `origin/agent/20261013-energy-lack-shop-shortcut-t_f25c0492`
   - `EnergyLackDialog` 能量不足彈窗操作區新增『前往商城』快捷果凍按鈕（`BtnGoShop`，高 52px，寬 180px，熱區 >= 48px，暖橘 #FFA010，深藍紫描邊 #1F1A3A，厚底 6px，圓角 20px，與觀看廣告、稍後再來並列，零系統 Emoji）。
   - 發射 `shop_requested` 訊號關閉彈窗並連動大廳開啟 `ShopDialog`，六語系即時切換支援。
5. **`vault-forge-shortcut`（t_842a278f）**：分支 `origin/agent/20261013-vault-forge-shortcut-t_842a278f`
   - `ClockworkVaultDialog` 發條儲能庫放置收益彈窗操作區新增『前往鍛造』快捷果凍按鈕（`BtnGoForge`，高 52px，寬 200px，熱區 >= 48px，金黃 #FFD028，深藍紫描邊 #1F1A3A，厚底 5px，圓角 18px，字級 18px，與領取、雙倍領取並列，零系統 Emoji）。
   - 發射 `forge_requested` 訊號關閉彈窗並直通天宮鐵匠 `ForgeDialog`，將放置累積之鐵屑直接導流至裝備鍛造與機芯校準，六語系支援。

由程式員工阿宏（`sideworker`）在 `main` 分支執行五分支乾淨整併，無語法與資源衝突，執行全套單元測試與關聯回歸測試全數通過，並透過 `/root/project_status.py` 將五大項目狀態同步至『已上線』。

---\n
## 2. 自動化測試與檢查執行結果

| 測試項目 | 執行指令 | 測試結果 | 判定 |
|---|---|---|:---:|
| **無頭引擎冒煙測試** | `godot --path game --headless --quit-after 3` | 0 SCRIPT ERROR，DisplaySettings 與 GraphicsProfile 正常套用 (exit 0) | **PASS** |
| **鐵匠五槽一鍵卸下單元測試** | `godot --path game --headless -s res://scripts/ui/test_forge_dialog_unequip_all.gd` | `TEST_FORGE_DIALOG_UNEQUIP_ALL_OK`，按鈕規格、卸下五槽、戰力即時刷新、空槽防呆與六語系全綠 | **PASS** |
| **背包戰魂前往聚魂快捷單元測試** | `godot --path game --headless -s res://scripts/ui/test_maple_inventory_soul_shortcut.gd` | `MAPLE_INVENTORY_SOUL_SHORTCUT_OK`，按鈕熱區、互斥顯示、信號直達聚魂殿、六語系全綠 | **PASS** |
| **聚魂殿前往背包快捷單元測試** | `godot --path game --headless -s res://scripts/ui/test_soul_hall_inventory_shortcut.gd` | `TEST_SOUL_HALL_INVENTORY_SHORTCUT_OK`，底欄三鈕並列、連動背包素材頁籤、雙向閉環與六語系全綠 | **PASS** |
| **能量不足前往商城快捷單元測試** | `godot --path game --headless -s res://scripts/ui/test_energy_lack_shop_shortcut.gd` | `TEST_ENERGY_LACK_SHOP_SHORTCUT_OK`，底欄三鈕並列、信號連動 ShopDialog、六語系全綠 | **PASS** |
| **能量不足多語系連動測試** | `godot --path game --headless -s res://scripts/ui/test_energy_lack_i18n.gd` | `TEST_ENERGY_LACK_I18N_OK`，六語系動態切換、免廣告模式、上限模式無缺詞 | **PASS** |
| **發條儲能庫前往鍛造快捷單元測試** | `godot --path game --headless -s res://scripts/ui/test_vault_forge_shortcut.gd` | `TEST_VAULT_FORGE_SHORTCUT_OK`，底欄三鈕並列、直通天宮鐵匠、鐵屑導流、六語系全綠 | **PASS** |
| **鍛造關聯全套測試** | `TEST_FILTER=forge ./tools/run_tests.sh` | 14/14 PASS，全數通過 | **PASS** |
| **背包關聯全套測試** | `TEST_FILTER=inventory ./tools/run_tests.sh` | 20/20 PASS，全數通過 | **PASS** |
| **戰魂與聚魂關聯全套測試** | `TEST_FILTER=soul ./tools/run_tests.sh` | 8/8 PASS，全數通過 | **PASS** |
| **體力與能量關聯全套測試** | `TEST_FILTER=energy ./tools/run_tests.sh` | 6/6 PASS，全數通過 | **PASS** |
| **儲能庫關聯全套測試** | `TEST_FILTER=vault ./tools/run_tests.sh` | 4/4 PASS，全數通過 | **PASS** |
| **大廳機芯更換彈窗回歸測試** | `godot --path game --headless -s res://scripts/ui/test_lobby_core_replace_dialog.gd` | `TEST_LOBBY_CORE_REPLACE_DIALOG_OK`，Slot/TierLabel 14px 徹底清除小字 | **PASS** |
| **大廳主流程回歸測試** | `godot --path game --headless -s res://scripts/ui/test_mobile_lobby.gd` | `MOBILE_LOBBY_OK`，大廳各殿堂與功能回歸無破壞 | **PASS** |
| **代碼與素材關聯檢查** | `/root/bin/clock-check /opt/side/bravesoul-game` | 🖼️ 新增／修改素材 0 個，缺 .import 0 個；⚠️ 直接在 main 上改（本卡為維運整併卡，預期操作） | **PASS** |
| **官網線上存活檢查** | `/root/bin/clock-check --live` | ✅ 官網 14 頁都打得開，沒有舊名詞 | **PASS** |

---\n
## 3. 實機 Framebuffer 截圖存證與 SHA256 雜湊表 (proofs/t_96c254e5/)
所有截圖皆以真實 OpenGL3 渲染驅動於 1280×720 解析度下透過真實 Viewport Framebuffer 產生，零假圖，32 張 SHA256 各自獨立無重複：

### A. 天宮鐵匠機芯五槽一鍵卸下全部機芯（8 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_01_forge_core_slots_equipped_zh_TW.png` | 繁中鐵匠五槽裝備狀態與成對並列之 BtnAutoCalibrateCore 與 BtnUnequipAllCores（珊瑚粉 #FF5E8A、高 46px） | 1280×720 | `d4cad5fce749bcdf97f536ab432c0a33cb2c28c5cfb9ae745c541186a06c4d9a` |
| `proof_02_forge_unequip_clicked_toast_reset_zh_TW.png` | 點擊一鍵卸下後五槽重置為未裝備、戰力即時下降與『已卸下所有機芯』Toast 提示 | 1280×720 | `5c0745fdf40f1fc5e600eaedb24d45834d4a4452d5b50e90c703e82527a69e57` |
| `proof_03_forge_unequip_empty_guard_zh_TW.png` | 五槽均為空時點擊一鍵卸下之防呆『未裝備任何機芯』Toast 提示 | 1280×720 | `b1cb26cf17524055fccf02acfc06f4835565989dd274a9d32d317b8b0624e164` |
| `proof_04_forge_unequip_all_en.png` | 英文語系 (en) 一鍵卸下 Quick Unsocket 按鈕與 UI，零 CJK 殘留 | 1280×720 | `55819c4a3133034ee1deaf10b18522b2414d7531a83e05f6f085662234aa4abe` |
| `proof_05_forge_unequip_all_ja.png` | 日文語系 (ja) 一鍵卸下 一括解除 按鈕與 UI | 1280×720 | `6f51170d417c8994524a3f2eeb74ed69eab1a0a06e83d9566e28549d66f4f5c6` |
| `proof_06_forge_unequip_all_ko.png` | 韓文語系 (ko) 一鍵卸下 일괄 해제 按鈕與 UI | 1280×720 | `cddffb327e0649bd9e8fb1156faa1bb329707b52f3404a1d451bc04963739b98` |
| `proof_07_forge_unequip_all_es.png` | 西文語系 (es) 一鍵卸下 Desengarzar Todo 按鈕與 UI | 1280×720 | `f1ae85d4e05f64f3c2cadc38980e37db9719802f30e09c3accf8b1ea4279123e` |
| `proof_08_forge_unequip_all_zh_CN.png` | 簡中語系 (zh_CN) 一鍵卸下 一键卸下 按鈕與 UI | 1280×720 | `427a7dc4df4a2a20632beffbb58b0f93e4677052c43da89bf950fb10d0525428` |

### B. MapleInventory 探索背包戰魂素材前往聚魂快捷（6 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_09_inv_soul_fragment_go_soul_zh_TW.png` | 選中戰魂碎片時展示『前往聚魂』金黃果凍厚底按鈕 (高 52px) | 1280×720 | `daf4568411b40a48175000d69746fa5a0908548c35f58afa0c948218cc758472` |
| `proof_10_inv_soul_shortcut_en.png` | 英文語系 (en) 下『Go to Soul Draw』按鈕展示，零 CJK 殘留 | 1280×720 | `26368ee09a7183673d0bdf7cfaf143ea9d87430fe7688d260fc04269e25b5c87` |
| `proof_11_inv_soul_shortcut_ja.png` | 日文語系 (ja) 下『魂寄せへ』按鈕展示 | 1280×720 | `6bef4fd0c2b42df79fa6271647c001e577172a852f3d9f554a21aadb9fe0d728` |
| `proof_12_inv_soul_shortcut_ko.png` | 韓文語系 (ko) 下『영혼 뽑기로 이동』按鈕展示 | 1280×720 | `fb8164be7e27eefaabb38fe793b63678dd6fa205ee0e1f7b95eaef2e9475d3dc` |
| `proof_13_inv_soul_shortcut_es.png` | 西文語系 (es) 下『Ir a extracción de almas』按鈕展示，零 CJK 殘留 | 1280×720 | `53ddab50802e22e66809cfde9b20aaf5dd50332d923401fd677ea186e61d437a` |
| `proof_14_inv_click_go_soul_opens_soul_hall.png` | 點擊前往聚魂後關閉背包直達大廳聚魂殿堂實景 | 1280×720 | `b6b36baa82e783fd1aae18a5c1be8da975d25a324891f582fad9872f042691dd` |

### C. 大廳聚魂殿堂前往背包快捷（6 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_15_soul_hall_three_buttons_zh_TW.png` | 繁中聚魂殿堂底欄三顆果凍按鈕並列（吸收灰魂／前往背包／聚魂十連） | 1280×720 | `cc56eaea21e882a25e81228eba970d44a826ec163f7d52990c5c0623a0a70244` |
| `proof_16_soul_hall_go_inv_en.png` | 英文語系 (en) 下『Go to Inventory』按鈕展示，零 CJK 殘留 | 1280×720 | `82d8bc7e862962b26f528763c97014a8b7c9d3aa3e564c2d7d4ace6e7e65546e` |
| `proof_17_soul_hall_go_inv_ja.png` | 日文語系 (ja) 下『インベントリへ進む』按鈕展示 | 1280×720 | `5dcda0d84698bc1448f55a7f389265a6b1d4c17e020ffcb4f5e28a796faef204` |
| `proof_18_soul_hall_go_inv_ko.png` | 韓文語系 (ko) 下『인벤토리로 이동』按鈕展示 | 1280×720 | `5e1a8b1d8cda85393e32ca0530c566e0804569c3dfcf70d70a484a316cb9c42e` |
| `proof_19_soul_hall_go_inv_es.png` | 西文語系 (es) 下『Ir al Inventario』按鈕展示，零 CJK 殘留 | 1280×720 | `ee2971adc964973cfff8751c5ed8e054d5dff7b77342cb2ed5b252a3bc39a6d3` |
| `proof_20_soul_hall_click_go_inv_opens_material_tab.png` | 點擊前往背包直通探索背包素材頁籤實景 | 1280×720 | `b7f6cab9f24904cf55e4bb4b621b6911b6610dc87e6cdf8afe361f792791fbff` |

### D. EnergyLackDialog 能量不足前往商城快捷（6 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_21_energy_lack_three_buttons_zh_TW.png` | 繁中能量不足彈窗三顆果凍按鈕並列（看廣告／前往商城／稍後再來） | 1280×720 | `1fc1513c0e427d113b5034f03dc0d336ee7637fcf92096c03d37cf227b938c26` |
| `proof_22_energy_lack_btn_go_shop_en.png` | 英文語系 (en) 下『Go to Shop』按鈕展示，零 CJK 殘留 | 1280×720 | `63bdfff36bb7a4c6d1be35af059ac4c90214fa8f5b3cf437e3512298de27397c` |
| `proof_23_energy_lack_btn_go_shop_ja.png` | 日文語系 (ja) 下『ショップへ』按鈕展示 | 1280×720 | `a422eb5924a486c98a349b69fa5ae1307df422d303cf6f6d0767c960de5d6d0b` |
| `proof_24_energy_lack_btn_go_shop_ko.png` | 韓文語系 (ko) 下『상점으로』按鈕展示 | 1280×720 | `514576e48b627ad6242385c3685489e16448010f1066391e848484bfb4c36f4b` |
| `proof_25_energy_lack_btn_go_shop_es.png` | 西文語系 (es) 下『Ir a la tienda』按鈕展示，零 CJK 殘留 | 1280×720 | `239201644727742c92bf87f53687ac74b78bcc0dfd05f2f41d15f4936acdda15` |
| `proof_26_energy_lack_click_go_shop_opens_shop_dialog.png` | 點擊前往商城關閉彈窗並連動開啟 ShopDialog 實景 | 1280×720 | `897e183c24aa3ced77489a67f77ecb7cbe9bda21534debc1886cb8738feb856f` |

### E. ClockworkVaultDialog 發條儲能庫前往鍛造快捷（6 張）
| 截圖檔名 | 說明 | 尺寸 | SHA256 |
|---|---|---|---|
| `proof_27_vault_three_buttons_zh_TW.png` | 繁中發條儲能庫底欄三顆果凍按鈕並列（領取／雙倍領取／前往鍛造） | 1280×720 | `3da05fb57945e9c231cddeef7ae8fc1da84e176f6ce4dbf26c4809384553b5ce` |
| `proof_28_vault_go_forge_en.png` | 英文語系 (en) 下『Go to Forge』按鈕展示，零 CJK 殘留 | 1280×720 | `60c785408e3c63d8b1ca30fd0c0e63ef13f38a4b4d2a2cec9a696bf6c8adce39` |
| `proof_29_vault_go_forge_ja.png` | 日文語系 (ja) 下『鍛造へ進む』按鈕展示 | 1280×720 | `bc985344e597263e75de4f84146c868b6aa76e03923affbb9550c59e1062fd68` |
| `proof_30_vault_go_forge_ko.png` | 韓文語系 (ko) 下『단조로 이동』按鈕展示 | 1280×720 | `e2f57d47232ba99cdc3ae2bc3bc4343bb315b3a0ef712f09fcaefac2c97b8db2` |
| `proof_31_vault_go_forge_es.png` | 西文語系 (es) 下『Ir a Forja』按鈕展示，零 CJK 殘留 | 1280×720 | `b61ac790024dfd9063fd879d41befa14e904bf67fa1260af99eff7f44eae06de` |
| `proof_32_vault_click_go_forge_opens_forge_dialog.png` | 點擊前往鍛造關閉彈窗並直通天宮鐵匠實景 | 1280×720 | `eba841cb81ab04385cb2c4afd27e3ae2f88e860e6368f1262080d90664f4c2d6` |

---\n
## 4. 常見退回自查清單核對 (clock-review-checklist.md)
- [x] **畫面與素材**：
  - 各快捷與操作按鈕熱區皆嚴格符合手機端規範（>= 48px，高度 46~52px，寬度 105~200px）。
  - 按鈕樣式均為多巴胺立體果凍厚底按鈕（金黃 #FFD028、珊瑚粉 #FF5E8A、暖橘 #FFA010，厚底 5~6px，深藍紫描邊 2px，圓角 16~20px）。
  - 全域零系統 Emoji，全面使用開源粉圓體與高對比多巴胺色盤，徹底清除 13px 以下小字。
  - 32 張實機截圖 SHA256 各自獨立無重複，Viewport 與語系渲染完整無黑屏、無文字穿框。
- [x] **測試與證據**：
  - 無頭引擎冒煙測試 0 SCRIPT ERROR 通過 (exit 0)。
  - 五大功能專屬單元測試與關聯測試全數 PASS。
  - 測試輸出無 flaky 時序競爭。
- [x] **程式與邏輯**：
  - 合併無未解衝突，所有 autoload、信號連動、語系字串完全對齊。
  - 卸下機芯安全歸還背包，戰力即時刷新，防呆保護完善。
  - 背包與聚魂殿、儲能庫與鐵匠、體力不足與商城雙向直通連動閉環運作正常。
- [x] **資料與文案**：
  - 六語系（zh_TW, zh_CN, en, ja, ko, es）鍵值齊全，歐美語系零 CJK 殘留。
  - 無已退役舊名詞（霧隱村／今日村莊／白霧村 零殘留）。
- [x] **流程與交付**：
  - `docs/PROJECTS.json` 透過 `python3 /root/project_status.py` 將五大項目全數更新為『已上線』。
  - 工作目錄乾淨，無未追蹤或未提交之暫存檔案。
