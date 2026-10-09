extends SceneTree
## 單元與驗收測試：WeaponSwapDialog 完整顯示武器隨機副詞條與屬性標籤膠囊 (t_dcba17d2)
## 覆蓋項目：
## 1. 靜態函數 extract_substats, has_substats, format_substat_text, get_substat_colors, get_substat_name。
## 2. 武器清單卡片 (_build_weapon_card) 動態生成副詞條膠囊列 (SubstatsRow)，白板武器 vs 含副詞條武器。
## 3. 目標槽位已有裝備時，候選武器副詞條相對於當前裝備之增減差額標籤 (+N / -N) 與完整屬性展示。
## 4. 槽位摘要面板 (SlotSummaryPanel) 動態展示當前裝備之副詞條膠囊列 (SlotSubstatsBox)。
## 5. 遵循多巴胺鮮亮高飽和色盤（圓角 10~14px、字級 >= 12px 帶深藍紫加粗文字、零系統 Emoji）。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化連動刷新 (ContentLoc / Loc 連動)。
## 7. 實機渲染環境產出 3 張獨立 SHA256 存證截圖。

const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _out_dir: String = ""
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _dialog: Control = null
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	print("== 開始執行 WeaponSwapDialog 副詞條膠囊標籤驗收測試 (t_dcba17d2) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_dcba17d2")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var top_proofs := ProjectSettings.globalize_path("res://../proofs/t_dcba17d2")
	DirAccess.make_dir_recursive_absolute(top_proofs)

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	if gs == null or eq == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / Loc)")
		return

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_step = 0


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	match _step:
		0:
			_test_static_helpers()
			_step = 1
		1:
			_test_plain_vs_rolled_weapon_cards()
			_step = 2
		2:
			_test_slot_summary_substats()
			_step = 3
		3:
			_test_substat_difference_comparison()
			_step = 4
		4:
			_test_i18n_locales()
			_step = 5
		5:
			if DisplayServer.get_name() != "headless":
				print("\n--- 6. 擷取實機截圖存證並驗證 SHA256 不重複 ---")
				_wait = 0
				_step = 6
			else:
				print("\n--- 6. 無頭模式 (headless)，略過 Viewport 截圖與雜湊比對 ---")
				_step = 10
		6:
			_wait += 1
			if _wait < 6:
				return false
			_setup_dialog_for_proof(0)
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 10:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_substats_slot0.png")
			_h1 = _capture_and_save(p1)
			_setup_dialog_for_proof(1)
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 10:
				return false
			var p2 := _out_dir.path_join("proof_02_weapon_swap_substats_diff.png")
			_h2 = _capture_and_save(p2)
			_setup_dialog_for_proof(0)
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_wait = 0
			_step = 9
		9:
			_wait += 1
			if _wait < 10:
				return false
			var p3 := _out_dir.path_join("proof_03_weapon_swap_substats_en.png")
			_h3 = _capture_and_save(p3)
			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
				return false
			print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			_step = 10
		10:
			if is_instance_valid(_dialog):
				_dialog.queue_free()
				_dialog = null
			print("\n=======================================================")
			print("  TEST_WEAPON_SWAP_SUBSTATS_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _test_static_helpers() -> void:
	print("\n--- 1. 檢驗靜態副詞條提取與文字格式化函數 ---")
	var w_rolled := {
		"uid": "w_test",
		"weapon_atk": 45,
		"rolled": {
			"def": 15,
			"hp": 40,
			"crit_dmg": 18.5,
			"crit": 5.0
		}
	}
	var subs: Dictionary = WeaponSwapDialogScript.extract_substats(w_rolled)
	if subs["def"] != 15 or subs["hp"] != 40 or absf(subs["crit_dmg"] - 18.5) > 0.01 or absf(subs["crit"] - 5.0) > 0.01:
		_fail("extract_substats 提取失敗: " + str(subs))
	if not WeaponSwapDialogScript.has_substats(w_rolled):
		_fail("has_substats 應判定含副詞條武器為 true")

	var w_plain := {"uid": "w_plain", "weapon_atk": 20, "rolled": {}}
	if WeaponSwapDialogScript.has_substats(w_plain):
		_fail("has_substats 應判定白板武器為 false")

	var def_txt: String = WeaponSwapDialogScript.format_substat_text("def", 15.0, 0.0, false)
	var hp_txt: String = WeaponSwapDialogScript.format_substat_text("hp", 40.0, 0.0, false)
	var cdmg_txt: String = WeaponSwapDialogScript.format_substat_text("crit_dmg", 18.5, 0.0, false)

	if not ("防禦 +15" in def_txt or "DEF +15" in def_txt):
		_fail("format_substat_text def 格式錯誤: " + def_txt)
	if not ("生命 +40" in hp_txt or "HP +40" in hp_txt):
		_fail("format_substat_text hp 格式錯誤: " + hp_txt)
	if not ("暴傷 +18.5%" in cdmg_txt or "Crit DMG +18.5%" in cdmg_txt):
		_fail("format_substat_text crit_dmg 格式錯誤: " + cdmg_txt)

	# 差額格式化
	var diff_pos_txt: String = WeaponSwapDialogScript.format_substat_text("def", 15.0, 10.0, true)
	if not ("+10" in diff_pos_txt):
		_fail("正差額應包含 (+10): " + diff_pos_txt)

	var diff_neg_txt: String = WeaponSwapDialogScript.format_substat_text("hp", 40.0, -15.0, true)
	if not ("-15" in diff_neg_txt):
		_fail("負差額應包含 (-15): " + diff_neg_txt)

	print("  ok extract_substats, has_substats 與 format_substat_text 驗證通過")


func _test_plain_vs_rolled_weapon_cards() -> void:
	print("\n--- 2. 檢驗白板武器 vs 含副詞條武器之卡片與膠囊渲染正確性 ---")
	var gs = root.get_node_or_null("GameState")
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]

	gs.equip_bag = [
		{
			"uid": "w_plain_card",
			"slot": "weapon",
			"name": "白板鐵劍",
			"line": "sword",
			"weapon_atk": 25,
			"rolled": {}
		},
		{
			"uid": "w_rolled_card",
			"slot": "weapon",
			"name": "靈犀神劍",
			"line": "sword",
			"weapon_atk": 50,
			"rolled": {
				"def": 15,
				"hp": 40,
				"crit_dmg": 18.5
			}
		}
	]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	# 1. 檢驗白板武器卡片
	var plain_card: PanelContainer = dlg.find_child("WeaponCard_w_plain_card", true, false) as PanelContainer
	if plain_card == null:
		_fail("找不到白板武器卡片 WeaponCard_w_plain_card")
	var plain_subs_row: HBoxContainer = plain_card.find_child("SubstatsRow", true, false) as HBoxContainer
	if plain_subs_row == null:
		_fail("白板卡片缺少 SubstatsRow 容器")
	if plain_subs_row.visible and plain_subs_row.get_child_count() > 0:
		_fail("白板卡片之 SubstatsRow 應為空且不可見")

	# 2. 檢驗含副詞條武器卡片
	var rolled_card: PanelContainer = dlg.find_child("WeaponCard_w_rolled_card", true, false) as PanelContainer
	if rolled_card == null:
		_fail("找不到含副詞條卡片 WeaponCard_w_rolled_card")
	var rolled_subs_row: HBoxContainer = rolled_card.find_child("SubstatsRow", true, false) as HBoxContainer
	if rolled_subs_row == null or not rolled_subs_row.visible:
		_fail("含副詞條卡片之 SubstatsRow 應存在且可見")

	var cap_def: PanelContainer = rolled_subs_row.find_child("SubstatCapsule_def", true, false) as PanelContainer
	var cap_hp: PanelContainer = rolled_subs_row.find_child("SubstatCapsule_hp", true, false) as PanelContainer
	var cap_cdmg: PanelContainer = rolled_subs_row.find_child("SubstatCapsule_crit_dmg", true, false) as PanelContainer

	if cap_def == null or cap_hp == null or cap_cdmg == null:
		_fail("含副詞條卡片缺少對應之 SubstatCapsule 節點")

	# 檢驗膠囊樣式與多巴胺配色規範
	var def_sb: StyleBoxFlat = cap_def.get_theme_stylebox("panel") as StyleBoxFlat
	if def_sb == null or def_sb.bg_color != WeaponSwapDialogScript.COLOR_SUBSTAT_DEF_BG:
		_fail("防禦膠囊背景色不符合天藍柔底規範")
	if def_sb.corner_radius_top_left < 10 or def_sb.corner_radius_top_left > 14:
		_fail("膠囊圓角不符合 10~14px 規範: %d" % def_sb.corner_radius_top_left)

	var def_lbl: Label = cap_def.find_child("SubstatLabel", true, false) as Label
	if def_lbl == null or not ("防禦 +15" in def_lbl.text):
		_fail("防禦膠囊文字錯誤: " + (def_lbl.text if def_lbl else "null"))
	_assert_no_emoji(def_lbl.text, "def_lbl")

	var hp_lbl: Label = cap_hp.find_child("SubstatLabel", true, false) as Label
	if hp_lbl == null or not ("生命 +40" in hp_lbl.text):
		_fail("生命膠囊文字錯誤: " + (hp_lbl.text if hp_lbl else "null"))
	_assert_no_emoji(hp_lbl.text, "hp_lbl")

	var cdmg_lbl: Label = cap_cdmg.find_child("SubstatLabel", true, false) as Label
	if cdmg_lbl == null or not ("暴傷 +18.5%" in cdmg_lbl.text):
		_fail("暴傷膠囊文字錯誤: " + (cdmg_lbl.text if cdmg_lbl else "null"))
	_assert_no_emoji(cdmg_lbl.text, "cdmg_lbl")

	print("  ok 白板武器無膠囊、含副詞條武器精準生成防禦/生命/暴傷多巴胺膠囊列")
	dlg.queue_free()


func _test_slot_summary_substats() -> void:
	print("\n--- 3. 檢驗槽位摘要面板 (SlotSummaryPanel) 副詞條膠囊列連動 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 槽位 0 裝備含副詞條武器
	var cur_w := {
		"uid": "w_equipped_slot0",
		"slot": "weapon",
		"name": "發條神將之劍",
		"line": "sword",
		"weapon_atk": 60,
		"rolled": {
			"def": 20,
			"hp": 50,
			"crit_dmg": 15.0
		}
	}
	gs.equip_worn = {"w_equipped_slot0": cur_w}
	gs.weapon_loadout = ["w_equipped_slot0", "", ""]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	var slot_subs_box: HBoxContainer = dlg.find_child("SlotSubstatsBox", true, false) as HBoxContainer
	if slot_subs_box == null:
		_fail("SlotSummaryPanel 缺少 SlotSubstatsBox 容器")

	var s_def: PanelContainer = slot_subs_box.find_child("SubstatCapsule_def", true, false) as PanelContainer
	var s_hp: PanelContainer = slot_subs_box.find_child("SubstatCapsule_hp", true, false) as PanelContainer
	var s_cdmg: PanelContainer = slot_subs_box.find_child("SubstatCapsule_crit_dmg", true, false) as PanelContainer

	if s_def == null or s_hp == null or s_cdmg == null:
		_fail("SlotSubstatsBox 未生成槽位裝備的副詞條膠囊")

	var l_def: Label = s_def.find_child("SubstatLabel", true, false) as Label
	var l_hp: Label = s_hp.find_child("SubstatLabel", true, false) as Label
	var l_cdmg: Label = s_cdmg.find_child("SubstatLabel", true, false) as Label

	if l_def == null or not ("防禦 +20" in l_def.text):
		_fail("摘要面板防禦文字錯誤: " + (l_def.text if l_def else "null"))
	if l_hp == null or not ("生命 +50" in l_hp.text):
		_fail("摘要面板生命文字錯誤: " + (l_hp.text if l_hp else "null"))
	if l_cdmg == null or not ("暴傷 +15.0%" in l_cdmg.text):
		_fail("摘要面板暴傷文字錯誤: " + (l_cdmg.text if l_cdmg else "null"))

	print("  ok 槽位摘要面板 (SlotSummaryPanel) 成功完整展示當前裝備副詞條膠囊列")
	dlg.queue_free()


func _test_substat_difference_comparison() -> void:
	print("\n--- 4. 檢驗目標槽位已有裝備時之副詞條增減差異提示 (+N / -N) ---")
	var gs = root.get_node_or_null("GameState")
	# 當前槽位裝備：def 10, hp 30, crit_dmg 10.0
	var cur_w := {
		"uid": "w_base_equipped",
		"slot": "weapon",
		"name": "守護短劍",
		"line": "sword",
		"weapon_atk": 30,
		"rolled": {
			"def": 10,
			"hp": 30,
			"crit_dmg": 10.0
		}
	}
	gs.equip_worn = {"w_base_equipped": cur_w}
	gs.weapon_loadout = ["w_base_equipped", "", ""]

	gs.equip_bag = [
		{
			# 比當前高：def 25 (+15), hp 45 (+15), crit_dmg 22.5 (+12.5)
			"uid": "w_higher",
			"slot": "weapon",
			"name": "極光之刃",
			"line": "sword",
			"weapon_atk": 50,
			"rolled": {
				"def": 25,
				"hp": 45,
				"crit_dmg": 22.5
			}
		},
		{
			# 比當前低：def 4 (-6), hp 10 (-20)
			"uid": "w_lower",
			"slot": "weapon",
			"name": "鏽蝕細劍",
			"line": "sword",
			"weapon_atk": 20,
			"rolled": {
				"def": 4,
				"hp": 10
			}
		}
	]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	# 1. 檢驗比當前高的候選卡片
	var high_card: PanelContainer = dlg.find_child("WeaponCard_w_higher", true, false) as PanelContainer
	if high_card == null:
		_fail("未找到 w_higher 卡片")
		return
	var h_def_cap: PanelContainer = high_card.find_child("SubstatCapsule_def", true, false) as PanelContainer
	var h_hp_cap: PanelContainer = high_card.find_child("SubstatCapsule_hp", true, false) as PanelContainer
	var h_cdmg_cap: PanelContainer = high_card.find_child("SubstatCapsule_crit_dmg", true, false) as PanelContainer

	var h_def_lbl: Label = h_def_cap.find_child("SubstatLabel", true, false) as Label if h_def_cap else null
	var h_hp_lbl: Label = h_hp_cap.find_child("SubstatLabel", true, false) as Label if h_hp_cap else null
	var h_cdmg_lbl: Label = h_cdmg_cap.find_child("SubstatLabel", true, false) as Label if h_cdmg_cap else null

	if h_def_lbl == null or not ("+15" in h_def_lbl.text):
		_fail("w_higher 防禦應顯示 (+15) 增益提示: " + (h_def_lbl.text if h_def_lbl else "null"))
		return
	if h_hp_lbl == null or not ("+15" in h_hp_lbl.text):
		_fail("w_higher 生命應顯示 (+15) 增益提示: " + (h_hp_lbl.text if h_hp_lbl else "null"))
		return
	if h_cdmg_lbl == null or not ("+12.5%" in h_cdmg_lbl.text):
		_fail("w_higher 暴傷應顯示 (+12.5%) 增益提示: " + (h_cdmg_lbl.text if h_cdmg_lbl else "null"))
		return

	# 2. 檢驗比當前低的候選卡片
	var low_card: PanelContainer = dlg.find_child("WeaponCard_w_lower", true, false) as PanelContainer
	if low_card == null:
		_fail("未找到 w_lower 卡片")
		return
	var l_def_cap: PanelContainer = low_card.find_child("SubstatCapsule_def", true, false) as PanelContainer
	var l_hp_cap: PanelContainer = low_card.find_child("SubstatCapsule_hp", true, false) as PanelContainer

	var l_def_lbl: Label = l_def_cap.find_child("SubstatLabel", true, false) as Label if l_def_cap else null
	var l_hp_lbl: Label = l_hp_cap.find_child("SubstatLabel", true, false) as Label if l_hp_cap else null

	if l_def_lbl == null or not ("-6" in l_def_lbl.text):
		_fail("w_lower 防禦應顯示 (-6) 減損提示: " + (l_def_lbl.text if l_def_lbl else "null"))
		return
	if l_hp_lbl == null or not ("-20" in l_hp_lbl.text):
		_fail("w_lower 生命應顯示 (-20) 減損提示: " + (l_hp_lbl.text if l_hp_lbl else "null"))
		return

	print("  ok 目標槽位已有裝備時，副詞條動態呈現清晰之增減差異提示 (+15 / -6)")
	dlg.queue_free()


func _test_i18n_locales() -> void:
	print("\n--- 5. 檢驗六語系即時切換與 ContentLoc 連動 (防禦/生命/暴傷) ---")
	var loc = root.get_node_or_null("Loc")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

	var expected_terms := {
		"zh_TW": {"def": "防禦", "hp": "生命", "cdmg": "暴傷"},
		"zh_CN": {"def": "防御", "hp": "生命", "cdmg": "暴伤"},
		"en":    {"def": "DEF", "hp": "HP", "cdmg": "Crit DMG"},
		"ja":    {"def": "防御", "hp": "HP", "cdmg": "会心ダメ"},
		"ko":    {"def": "방어", "hp": "HP", "cdmg": "치명타 피해"},
		"es":    {"def": "DEF", "hp": "Salud", "cdmg": "Daño Crít."},
	}

	var gs = root.get_node_or_null("GameState")
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]
	gs.equip_bag = [
		{
			"uid": "w_i18n_test",
			"slot": "weapon",
			"name": "六語測試神弓",
			"line": "bow",
			"weapon_atk": 40,
			"rolled": {
				"def": 15,
				"hp": 40,
				"crit_dmg": 18.5
			}
		}
	]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	for lc in locales:
		loc.call("set_locale", lc)
		var exp_dict: Dictionary = expected_terms[lc]
		var exp_def: String = str(exp_dict["def"])
		var exp_hp: String = str(exp_dict["hp"])
		var exp_cdmg: String = str(exp_dict["cdmg"])

		var card: PanelContainer = dlg.find_child("WeaponCard_w_i18n_test", true, false) as PanelContainer
		if card == null:
			_fail("[%s] 未找到 w_i18n_test 卡片" % lc)

		var def_cap: PanelContainer = card.find_child("SubstatCapsule_def", true, false) as PanelContainer
		var hp_cap: PanelContainer = card.find_child("SubstatCapsule_hp", true, false) as PanelContainer
		var cdmg_cap: PanelContainer = card.find_child("SubstatCapsule_crit_dmg", true, false) as PanelContainer

		var def_lbl: Label = def_cap.find_child("SubstatLabel", true, false) as Label if def_cap else null
		var hp_lbl: Label = hp_cap.find_child("SubstatLabel", true, false) as Label if hp_cap else null
		var cdmg_lbl: Label = cdmg_cap.find_child("SubstatLabel", true, false) as Label if cdmg_cap else null

		if def_lbl == null or not (exp_def in def_lbl.text):
			_fail("[%s] 防禦語系錯誤: 預期包含 %s，實際為 %s" % [lc, exp_def, def_lbl.text if def_lbl else "null"])
		if hp_lbl == null or not (exp_hp in hp_lbl.text):
			_fail("[%s] 生命語系錯誤: 預期包含 %s，實際為 %s" % [lc, exp_hp, hp_lbl.text if hp_lbl else "null"])
		if cdmg_lbl == null or not (exp_cdmg in cdmg_lbl.text):
			_fail("[%s] 暴傷語系錯誤: 預期包含 %s，實際為 %s" % [lc, exp_cdmg, cdmg_lbl.text if cdmg_lbl else "null"])

		_assert_no_emoji(def_lbl.text, "[%s] def" % lc)
		_assert_no_emoji(hp_lbl.text, "[%s] hp" % lc)
		_assert_no_emoji(cdmg_lbl.text, "[%s] cdmg" % lc)

		print("  ok [%s] 語系即時在地化: def=\"%s\", hp=\"%s\", cdmg=\"%s\" 且零 Emoji" % [
			lc, def_lbl.text, hp_lbl.text, cdmg_lbl.text
		])

	loc.call("set_locale", "zh_TW")
	dlg.queue_free()


func _setup_dialog_for_proof(slot: int) -> void:
	if is_instance_valid(_dialog):
		_dialog.queue_free()
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.equip_worn = {
			"eq_dawn": {
				"uid": "eq_dawn",
				"slot": "weapon",
				"name": "兔族破曉之劍",
				"line": "sword",
				"weapon_atk": 30,
				"rolled": {"def": 10, "hp": 25, "crit_dmg": 10.0}
			}
		}
		gs.weapon_loadout = ["eq_dawn", "", ""]
		gs.equip_bag = [
			{
				"uid": "w_bag_god",
				"slot": "weapon",
				"name": "流火星核重劍",
				"line": "sword",
				"weapon_atk": 75,
				"rolled": {"def": 25, "hp": 60, "crit_dmg": 24.5}
			},
			{
				"uid": "w_bag_speed",
				"slot": "weapon",
				"name": "疾風翠羽短匕",
				"line": "dagger",
				"weapon_atk": 42,
				"rolled": {"def": 5, "hp": 15, "crit_dmg": 8.0}
			},
			{
				"uid": "w_bag_plain",
				"slot": "weapon",
				"name": "訓練練習木劍",
				"line": "sword",
				"weapon_atk": 15,
				"rolled": {}
			}
		]
	_dialog = WeaponSwapDialogScript.new(slot)
	root.add_child(_dialog)
	_dialog.setup(slot)


func _capture_and_save(path: String) -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("Viewport 不存在，無法擷取畫面")
		return ""
	var img: Image = vp.get_texture().get_image()
	if img == null or img.is_empty():
		_fail("Viewport 紋理為空，無法儲存截圖")
		return ""
	var err := img.save_png(path)
	if err != OK:
		_fail("儲存截圖失敗: %s, err=%d" % [path, err])
		return ""
	var top_path := ProjectSettings.globalize_path("res://../proofs/t_dcba17d2").path_join(path.get_file())
	img.save_png(top_path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		_fail("無法讀取已儲存之截圖: %s" % path)
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證已儲存: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _assert_no_emoji(s: String, context: String) -> void:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			_fail("違規包含系統 Emoji: context=%s, char=%s, code=0x%X" % [context, c, code])


func _fail(msg: String) -> void:
	push_error("TEST_WEAPON_SWAP_SUBSTATS_FAIL: " + msg)
	print("❌ TEST_WEAPON_SWAP_SUBSTATS_FAIL: ", msg)
	quit(1)
