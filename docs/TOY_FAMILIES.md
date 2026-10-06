# TOY_FAMILIES · 衣櫥玩具家族規格（待 KC 確認）

> 狀態：**草案，待 KC 確認**（#34）。確認後再開程式／美術 issue 照規格調整；美術 #30 等這份。  
> 依據：PR #19（`w9/wardrobe-toy-families` @ f02c7e3）的 `game/scripts/art/toy_family.gd`、`game/scripts/ui/wardrobe_dialog.gd`；`game/data/tables/paperdoll_slots.json`（main，#19 沒改）；`docs/CLOCKWORK_ART_MUSIC_BRIEF.md` §1、§2。  
> 這份只寫規格，不改程式和資料表。

---

## 0. 已定，不在這份討論

- 衣櫥分頁只用四個玩具家族，不再用狐、獅、野豬毛皮種族（brief §2）。主角是兔子剪影（brief §1）。
- 創角只拿掉狐、獅、野豬；虎、鶴、熊等其他動物種族先保留。**這份規格不下架任何種族**，只說明它們對到哪個家族。

---

## 1. 四個家族

分頁順序＝`FAMILIES` 陣列順序。預設家族 `DEFAULT_FAMILY = nutcracker_rabbit`。

| # | id | 名稱 | 定位 | 視覺關鍵字（設計建議） | 輪廓 |
|---|---|---|---|---|---|
| 1 | `nutcracker_rabbit` | 胡桃鉗兔 | 近衛 | 軍禮服、金肩章、雙排扣、高筒帽、直立長耳、木漆＋黃銅 | 直、挺、窄 |
| 2 | `music_box` | 八音盒 | 樂匣 | 音筒梳齒、鏤空金屬、琺瑯彩繪、音叉、風鈴、星盤、舞者底座 | 細、對稱、精巧 |
| 3 | `tin_soldier` | 錫兵 | 儀隊 | 錫鐵板甲、鉚釘、十字／T 柄重鑰、金屬帽纓、長槍、鍛鎚、排氣管 | 方、厚、重 |
| 4 | `carousel` | 旋轉木馬 | 巡遊 | 螺旋金柱、條紋頂棚、波浪鑲邊、捲草巴洛克、翼飾、騎兵馬具、晨曦／日曜 | 圓、華麗、會轉 |

- 「定位」是程式裡的 `archetype_zh`；視覺關鍵字是這份新提的，程式沒有。
- 四家族共用 brief 的限制：玩具材質（搪瓷、黃銅、車線布），不要毛皮、羽毛、皮革；1px 深色描邊。帽纓、翼飾都畫成金屬或布。

---

## 2. 歸類規則（#19 程式現況）

### 2.1 本體

`art_race_for()`：毛皮種族（fox／lion／boar）、空值、家族 id → 兔子本體 `rabbit`；其他種族 id 原樣回傳。  
所以虎、鶴、熊等舊存檔或創角選到的本體，仍畫自己的本體，只是衣櫥分頁用家族篩。

### 2.2 部件 → 家族（`family_of_item()`，照順序判斷）

1. 空值、`none`／`bare`／`empty`、基本款（`none` 和本體預設件）→ `""`，**每個分頁都看得到**。
2. 本體原廠件（`RACES_DATA[本體].costumes／chassis`）→ 本體所屬家族。兔子原廠三套外裝、三款塗裝都在胡桃鉗兔。**這條比 `ITEM_FAMILY` 優先。**
3. `ITEM_FAMILY` 有列 → 照表。
4. 其他 → `DEFAULT_FAMILY`（胡桃鉗兔）。

### 2.3 衣櫥列哪些部件

- 外裝、塗裝：本體原廠件，加上 `race` 是 `universal` 或本體的通用件，而且要有本體的 512 圖（外裝也認 `paperdoll/common/costume/`）。
- 頭部、發條鑰匙、武器、光學核心、隨身奇玩：`race` 是 `universal` 或本體就列，**不檢查 512 圖**。
- `race` 是 fox／lion／boar 的部件一律不列（`is_fur_item()`）。
- 只讀資料表的 `sample_variants`，**不讀 `default_items`**。

### 2.4 存檔

- `LEGACY_RACE_TO_FAMILY`：舊種族 id → 家族，用來決定開衣櫥時停在哪個分頁、非兔本體的原廠件歸哪頁。沒列到的回胡桃鉗兔。
- 換裝時把目前家族寫進 `flags["wardrobe.family"]`。
- 舊存檔是 fox／lion／boar：載入時改回兔子，原 id 記在 `flags["wardrobe.legacy_race"]`，家族記在 `flags["wardrobe.family"]`。

---

## 3. `ITEM_FAMILY` 部件對照（41 筆）

「理由」是從部件名稱推的。「兔子衣櫥實際」是照 §2 規則跑出來的結果，跟表上家族不一樣的標 ⚠。

### 3.1 外裝（costume）

| id | 名稱 | 表上家族 | 理由 | 兔子衣櫥實際 |
|---|---|---|---|---|
| `costume_viking_harness` | 粗獷鍛爐護胸鐵束帶 | 錫兵 | 鍛鐵、束帶，重甲 | 錫兵 |
| `costume_viking_ironclad` | 維京重裝鍛鐵板甲 | 錫兵 | 重甲 | ⚠ 不列（資料表 `race: boar`，毛皮專屬） |
| `costume_royal_parade` | 皇家巡遊金屬禮服 | 錫兵 | 皇家、禮服，儀隊 | ⚠ 胡桃鉗兔（兔子原廠件，規則 2 優先） |
| `costume_astral_cape` | 星紋見習占星斗篷 | 八音盒 | 星紋、占星 | 八音盒 |
| `costume_astral_observer` | 星象觀測者金屬儀裝 | 八音盒 | 星象、儀器 | ⚠ 不列（沒有兔子／common 512 圖） |
| `costume_dawn_monk_tunic` | 晨曦行者武道短褂 | 旋轉木馬 | 晨曦系 | 旋轉木馬 |

### 3.2 塗裝（chassis）

| id | 名稱 | 表上家族 | 理由 | 兔子衣櫥實際 |
|---|---|---|---|---|
| `paint_nutcracker_red` | 胡桃鉗皇家朱紅 | 胡桃鉗兔 | 胡桃鉗紅 | ⚠ 不列（沒有兔子 512 圖） |
| `paint_midnight_navy` | 午夜深藍烤漆 | 錫兵 | 深藍軍裝色 | ⚠ 胡桃鉗兔（兔子原廠件） |
| `paint_emerald_glaze` | 翡翠螢光釉面 | 八音盒 | 琺瑯釉 | ⚠ 不列（沒有兔子 512 圖） |
| `paint_brass_gold` | 黃銅原金拋光 | 旋轉木馬 | 金柱 | ⚠ 胡桃鉗兔（兔子原廠件） |

### 3.3 發條鑰匙（winding_key）

| 家族 | 部件 |
|---|---|
| 八音盒（音叉、風鈴、八音） | `key_butterfly_t` 八音盒T型蝶翼發條、`key_swan_octave_dual_loop_brass` 雙環八音八度、`key_giraffe_three_ring_carillon_brass` 三環鏤空八音音筒、`key_petaurista_three_leaf_windchime_brass` 三葉禪韻風鈴、`key_woodpecker_high_frequency_percussion_key` 雙葉調速高頻音叉、⚠ `key_lynx_twin_ring_chime_brass` 雙環八音風鈴（在資料表 `default_items`，衣櫥不列） |
| 錫兵（十字、T 柄、重工） | `key_royal_crown` 皇家十字冠冕、`key_cross_pendulum` 玄軸雙重重錘十字、`key_heavy_cross_wheel` 重工十字同心輪、`key_wolf_heavy_pojun_cross` 高扭力破軍重工十字、`key_bison_heavy_cross_t_bar_cast_iron` 重工十字T柄生鐵、`key_gorilla_heavy_t_forged_key` 巨輪鍛工重型T字 |
| 旋轉木馬（翼、巴洛克、星芒） | `key_starlight_cog` 星芒齒輪旋鈕、`key_winged_angel` 展翼天國雙重、`key_twin_wing_concentric` 雙蝶翼同心圓、`key_tri_wing_zephyr` 三翼凌雲風輪、`key_courser_baroque_trefoil_gold` 巴洛克雙聯三葉草、`key_peacock_filigree_sunburst_key` 晨曦巴洛克日曜鏤空 |

### 3.4 武器、光學核心、隨身奇玩

| 槽位 | 八音盒 | 錫兵 | 旋轉木馬 |
|---|---|---|---|
| 武器 | `wpn_astral_staff` 星盤晶核秘術法杖、`wpn_bagua_astrolabe` 玄機八卦發條星盤、`weapon_swan_octave_spiral_lance` 八音螺旋穿刺長槍 | `wpn_knight_lance` 皇家黃銅突刺長槍、`wpn_anvil_greathammer` 鍛爐鐵砧重型戰鎚、`weapon_hound_stellar_beacon_lance` 星軌雷達天線長槍 | `weapon_courser_cavalry_saber` 晨曦齒輪騎兵劍、`wpn_zephyr_wing_bow` 風弦羽翼機關弓 |
| 光學核心 | `core_astral_amethyst` 星海紫晶透鏡 | `core_pilot_visor` 護目鏡覆蓋型光學面板 | `core_amber_sun` 琥珀烈陽透鏡 |
| 隨身奇玩 | `curio_floating_musicbox` 懸浮微型齒輪八音盒 | `curio_steam_exhaust` 迷你雙聯蒸氣排氣管 | （無） |

表上沒有胡桃鉗兔的鑰匙、武器、核心、奇玩；胡桃鉗兔分頁的這幾格全靠規則 4（沒列到就歸胡桃鉗兔）。

---

## 4. `LEGACY_RACE_TO_FAMILY`（69 個舊種族）

`RACE_KEYS` 69 個 id 全有對應（PR #19 說明寫 70，實際 69）。

| 家族 | 數量 | 舊種族 | 推得出的規則 |
|---|---:|---|---|
| 胡桃鉗兔 | 20 | 兔、猴、熊貓、犬、貓、海獺、浣熊、刺蝟、袋鼠、松鼠、狐獴、河狸、伶鼬、蜜獾、水豚、鼴鼠、鼯鼠、猞猁、狐猴、旱獺 | 中小型哺乳類 |
| 八音盒 | 20 | **狐**、**鶴**、蛙、鴞、青蛇、神隼、靈羊、變色龍、蝙蝠、孔雀、渡鴉、赤鳶、天鵝、守宮、啄木鳥、毛蟲、烏賊、巨嘴鳥、飛螢、翠鳥 | 鳥類、法術／觀星、小型精巧 |
| 錫兵 | 19 | **獅**、**野豬**、**虎**、**熊**、龜、象、穿山甲、鋼狼、蜥蜴、犀牛、巨猩、野牛、犰狳、石蟹、河馬、金龜、海象、羚牛、沙蠍 | 大型、重甲、力量型 |
| 旋轉木馬 | 10 | 企鵝、鹿、海馬、旗魚、駿駒、海豹、駱駝、長頸鹿、蝠魟、頑驢 | 坐騎、蹄類、水族 |

- 狐→八音盒、獅／野豬→錫兵：只用在舊存檔轉換（本體改回兔子，記下家族）。
- 虎→錫兵、熊→錫兵、鶴→八音盒：這三族照 KC 決定先保留，選它們當本體時，原廠件歸這幾頁。

---

## 5. 兔子衣櫥各分頁實際內容（#19 現況）

「基本款」每個分頁都看得到。數字是件數。

| 槽位 | 基本款 | 胡桃鉗兔 | 八音盒 | 錫兵 | 旋轉木馬 |
|---|---|---|---|---|---|
| 外裝 | 胡桃鉗近衛軍裝、無外裝 | 蒸氣工匠吊帶工作裝、皇家巡遊金屬禮服 | 星紋見習占星斗篷 | 粗獷鍛爐護胸鐵束帶 | 晨曦行者武道短褂 |
| 塗裝 | 原廠象牙白 | 黃銅原金拋光、午夜深藍烤漆 | 0 | 0 | 0 |
| 頭部 | 雙聯長立金屬耳 | 0 | 0 | 0 | 0 |
| 發條鑰匙 | 雙孔古銅 | 39（全是沒列到的通用鑰匙） | 5 | 6 | 6 |
| 武器 | 晨曦發條單手長劍 | 48（全是沒列到的通用武器） | 3 | 3 | 2 |
| 光學核心 | 天青翡翠透鏡 | 0 | 1 | 1 | 1 |
| 隨身奇玩 | 自走發條通訊小信鴿 | 0 | 1 | 1 | 0 |

- 八音盒、錫兵、旋轉木馬：外裝各 1 件（都是通用件），塗裝 0、頭部 0。
- 胡桃鉗兔：鑰匙和武器被規則 4 塞滿，裡面很多主題不合（太極雙魚、深海三叉、熔爐十字…）。
- 鑰匙、武器、核心、奇玩不檢查兔子 512 圖；上表除了基本款，兔子資料夾裡都沒有對應 512 圖，實際畫出來靠渲染器的通用路徑。美術補圖時以實機畫面為準。
