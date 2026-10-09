extends SceneTree
## 單元與驗收測試：WeaponSwapDialog 支援五色品質稀有度篩選 Chip 列 (t_96b721c6)
## 覆蓋項目：
## 1. 武器清單上方品質稀有度篩選 Chip 按鈕列（全部、凡品、精工、稀有、史詩、傳說）。
## 2. 按鈕熱區 >= 48px，果凍厚底 (4~5px)，圓角 12~16px，使用粉圓體，零系統 Emoji。
## 3. 點選各品質 Chip 即時過濾候選武器清單，僅顯示對應品質武器；選中呈現多巴胺五色高亮，未選中呈現柔和米黃底。
## 4. 支援與既有流派篩選 Chip 列及攻擊力降序排序平滑疊加生效，切換時即時重算可見武器數量。
## 5. 無對應品質武器時呈現友善空狀態提示而不破版。
## 6. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化連動與零 Emoji。
## 7. 實機渲染環境下產出獨立 SHA256 存證截圖。

const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _out_dir: String = ""
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _dialog: WeaponSwapDialogScript = null
var _hashes: Array[String] = []


func _initialize() -> void:
	print("== 開始執行 WeaponSwapDialog 五色品質篩選 Chip 驗收測試 (t_96b721c6) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_96b721c6")
	DirAccess.make_dir_recursive_absolute(_out_dir)

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
			_test_static_quality_matching()
			_step = 1
		1:
			_test_chip_bar_and_attributes()
			_step = 2
		2:
			_test_candidate_filtering_and_chip_clicking()
			_step = 3
		3:
			_test_stacked_filtering_with_line_and_sorting()
			_step = 4
		4:
			_test_empty_filter_state()
			_step = 5
		5:
			_test_i18n_locales()
			_step = 6
		6:
			if DisplayServer.get_name() != "headless":
				print("\n--- 7. 擷取實機截圖存證並驗證 SHA256 不重複 ---")
				_wait = 0
				_step = 7
			else:
				print("\n--- 7. 無頭模式 (headless)，略過 Viewport 截圖與雜湊比對 ---")
				_step = 12
		7:
			_wait += 1
			if _wait < 6:
				return false
			_setup_dialog_for_proof("all", "all")
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 8:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_quality_all.png")
			_capture_and_record(p1)
			_dialog.set_quality_filter("rare")
			_wait = 0
			_step = 9
		9:
			_wait += 1
			if _wait < 8:
				return false
			var p2 := _out_dir.path_join("proof_02_weapon_swap_quality_rare.png")
			_capture_and_record(p2)
			_dialog.set_line_filter("sword")
			_dialog.set_quality_filter("rare")
			_wait = 0
			_step = 10
		10:
			_wait += 1
			if _wait < 8:
				return false
			var p3 := _out_dir.path_join("proof_03_weapon_swap_quality_stacked.png")
			_capture_and_record(p3)
			_dialog.set_line_filter("gun")
			_dialog.set_quality_filter("legendary")
			_wait = 0
			_step = 11
		11:
			_wait += 1
			if _wait < 8:
				return false
			var p4 := _out_dir.path_join("proof_04_weapon_swap_quality_empty.png")
			_capture_and_record(p4)
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_dialog.set_line_filter("all")
			_dialog.set_quality_filter("epic")
			_wait = 0
			_step = 12
		12:
			if DisplayServer.get_name() != "headless":
				_wait += 1
				if _wait < 8:
					return false
				var p5 := _out_dir.path_join("proof_05_weapon_swap_quality_en.png")
				_capture_and_record(p5)
				_verify_hashes()
			_cleanup_dialog()
			print("\n=======================================================")
			print("  TEST_WEAPON_SWAP_QUALITY_FILTER_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _test_static_quality_matching() -> void:
	print("\n--- 1. 檢驗靜態品質正規化與比對函數 ---")
	# 通配
	_assert(WeaponSwapDialogScript.matches_quality_filter("common", "凡品", "all"), "all 應匹配 common")
	_assert(WeaponSwapDialogScript.matches_quality_filter("rare", "稀有", "全部"), "全部 應匹配 rare")
	_assert(WeaponSwapDialogScript.matches_quality_filter("legendary", "傳說", ""), "空字串 應匹配 legendary")

	# common
	_assert(WeaponSwapDialogScript.matches_quality_filter("common", "凡品", "common"), "common 應匹配 common")
	_assert(WeaponSwapDialogScript.matches_quality_filter("common", "", "凡品"), "凡品 應匹配 common")
	_assert(WeaponSwapDialogScript.matches_quality_filter("", "凡品", "common"), "common 應匹配 凡品")
	_assert(WeaponSwapDialogScript.matches_quality_filter("common", "凡", "white"), "white 應匹配 凡品")

	# uncommon
	_assert(WeaponSwapDialogScript.matches_quality_filter("uncommon", "精工", "uncommon"), "uncommon 應匹配 uncommon")
	_assert(WeaponSwapDialogScript.matches_quality_filter("uncommon", "良品", "精工"), "精工 應匹配 uncommon")
	_assert(WeaponSwapDialogScript.matches_quality_filter("", "良品", "uncommon"), "uncommon 應匹配 良品")
	_assert(WeaponSwapDialogScript.matches_quality_filter("uncommon", "綠", "green"), "green 應匹配 uncommon")

	# rare
	_assert(WeaponSwapDialogScript.matches_quality_filter("rare", "稀有", "rare"), "rare 應匹配 rare")
	_assert(WeaponSwapDialogScript.matches_quality_filter("rare", "上品", "稀有"), "稀有 應匹配 rare")
	_assert(WeaponSwapDialogScript.matches_quality_filter("", "上品", "rare"), "rare 應匹配 上品")
	_assert(WeaponSwapDialogScript.matches_quality_filter("rare", "藍", "blue"), "blue 應匹配 rare")

	# epic
	_assert(WeaponSwapDialogScript.matches_quality_filter("epic", "史詩", "epic"), "epic 應匹配 epic")
	_assert(WeaponSwapDialogScript.matches_quality_filter("epic", "極品", "史詩"), "史詩 應匹配 epic")
	_assert(WeaponSwapDialogScript.matches_quality_filter("epic", "秘寶", "epic"), "epic 應匹配 秘寶")
	_assert(WeaponSwapDialogScript.matches_quality_filter("epic", "紫", "purple"), "purple 應匹配 epic")

	# legendary
	_assert(WeaponSwapDialogScript.matches_quality_filter("legendary", "傳說", "legendary"), "legendary 應匹配 legendary")
	_assert(WeaponSwapDialogScript.matches_quality_filter("legendary", "神品", "傳說"), "傳說 應匹配 legendary")
	_assert(WeaponSwapDialogScript.matches_quality_filter("", "神品", "legendary"), "legendary 應匹配 神品")
	_assert(WeaponSwapDialogScript.matches_quality_filter("legendary", "金", "gold"), "gold 應匹配 legendary")

	# 互不混淆
	_assert(not WeaponSwapDialogScript.matches_quality_filter("common", "凡品", "rare"), "common 不應匹配 rare")
	_assert(not WeaponSwapDialogScript.matches_quality_filter("epic", "史詩", "legendary"), "epic 不應匹配 legendary")
	_assert(not WeaponSwapDialogScript.matches_quality_filter("uncommon", "精工", "epic"), "uncommon 不應匹配 epic")

	print("  ok matches_quality_filter 與 _normalize_quality 驗證通過")


func _test_chip_bar_and_attributes() -> void:
	print("\n--- 2. 檢驗品質篩選 Chip 列結構、熱區與多巴胺樣式規範 ---")
	_setup_dialog_for_proof("all", "all")

	var scroll := _dialog.get_node_or_null("DialogCard/RootVBox/QualityFilterScroll")
	_assert(scroll != null, "必須包含 QualityFilterScroll 節點")
	_assert(scroll is ScrollContainer, "QualityFilterScroll 必須為 ScrollContainer")

	var hbox := scroll.get_node_or_null("QualityFilterHBox")
	_assert(hbox != null, "必須包含 QualityFilterHBox 節點")
	_assert(hbox is HBoxContainer, "QualityFilterHBox 必須為 HBoxContainer")

	var q_chips: Dictionary = _dialog.get_quality_chips()
	_assert(q_chips.size() == 6, "必須包含 6 個品質篩選 Chip 按鈕 (實際: %d)" % q_chips.size())

	var expected_ids := ["all", "common", "uncommon", "rare", "epic", "legendary"]
	for qid in expected_ids:
		_assert(q_chips.has(qid), "品質 Chip 列表必須包含 id '%s'" % qid)
		var btn: Button = q_chips[qid]
		_assert(btn.custom_minimum_size.y >= 48, "按鈕熱區高度必須 >= 48px (實際: %.1f)" % btn.custom_minimum_size.y)
		_assert(not _has_emoji(btn.text), "按鈕文字不可包含系統 Emoji: %s" % btn.text)

	# 檢查預設選中 Chip 為 "all"，樣式呈現多巴胺暖橘高亮 (#FFA010)
	var all_btn: Button = q_chips["all"]
	var normal_sb: StyleBoxFlat = all_btn.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(normal_sb != null, "Chip 按鈕必須套用 StyleBoxFlat")
	_assert(normal_sb.bg_color == WeaponSwapDialogScript.COLOR_ORANGE, "選中 Chip 背景色必須為多巴胺暖橘 #FFA010")
	_assert(normal_sb.border_width_bottom == 5, "選中 Chip 果凍厚底必須為 5px")
	_assert(normal_sb.corner_radius_top_left >= 12 and normal_sb.corner_radius_top_left <= 16, "圓角必須在 12~16px")

	# 檢查未選中 Chip 為柔和米黃底
	var rare_btn: Button = q_chips["rare"]
	var unsel_sb: StyleBoxFlat = rare_btn.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(unsel_sb != null, "未選中 Chip 必須套用 StyleBoxFlat")
	_assert(unsel_sb.bg_color == WeaponSwapDialogScript.COLOR_CARD_WARM, "未選中 Chip 背景色必須為柔和米黃底 #FFF8E7")
	_assert(unsel_sb.border_width_bottom == 4, "未選中 Chip 果凍底厚度為 4px")

	print("  ok QualityFilterScroll 與 6 個品質 Chip 按鈕樣式驗證合格")


func _test_candidate_filtering_and_chip_clicking() -> void:
	print("\n--- 3. 檢驗點擊品質 Chip 即時過濾候選清單與即時重算數量 ---")
	var gs = root.get_node_or_null("GameState")

	# 準備 5 種不同品質的武器
	var mock_bag := [
		{"uid": "w_common_1", "slot": "weapon", "name": "生鏽鐵劍", "line": "sword", "quality": "common", "quality_label": "凡品", "weapon_atk": 20},
		{"uid": "w_uncommon_1", "slot": "weapon", "name": "精鑄長槍", "line": "spear", "quality": "uncommon", "quality_label": "精工", "weapon_atk": 35},
		{"uid": "w_rare_1", "slot": "weapon", "name": "碧空短匕", "line": "dagger", "quality": "rare", "quality_label": "稀有", "weapon_atk": 45},
		{"uid": "w_rare_2", "slot": "weapon", "name": "太極靈晶", "line": "crystal", "quality": "rare", "quality_label": "上品", "weapon_atk": 48},
		{"uid": "w_epic_1", "slot": "weapon", "name": "雷霆重斧", "line": "axe", "quality": "epic", "quality_label": "史詩", "weapon_atk": 60},
		{"uid": "w_legendary_1", "slot": "weapon", "name": "星宿神弓", "line": "bow", "quality": "legendary", "quality_label": "傳說", "weapon_atk": 80},
	]
	gs.equip_bag = mock_bag.duplicate(true)

	# 槽位 0 裝備凡品劍
	var cur_w := {"uid": "eq_slot0", "slot": "weapon", "name": "新手鐵劍", "line": "sword", "quality": "common", "quality_label": "凡品", "weapon_atk": 15}
	gs.equip_worn = {"eq_slot0": cur_w}
	gs.weapon_loadout = ["eq_slot0", "", ""]

	_dialog.setup(0)

	# 1. 驗證「全部」: 呈現所有 7 把候選武器 (1 當前槽位 + 6 背包)
	_dialog.set_line_filter("all")
	_dialog.set_quality_filter("all")
	_assert(_dialog.get_visible_weapons_count() == 7, "選「全部」時應有 7 把武器 (實際: %d)" % _dialog.get_visible_weapons_count())

	# 2. 點擊「稀有」Chip: 應有 2 把稀有武器
	var rare_chip: Button = _dialog.get_quality_chip("rare")
	_assert(rare_chip != null, "應取得 rare chip 按鈕")
	rare_chip.emit_signal("pressed")
	_assert(_dialog.get_current_filter_quality() == "rare", "當前品質篩選應為 rare")
	_assert(_dialog.get_visible_weapons_count() == 2, "稀有武器應過濾出 2 把 (實際: %d)" % _dialog.get_visible_weapons_count())

	# 驗證按鈕顏色切換為天藍多巴胺色
	var rare_sb: StyleBoxFlat = rare_chip.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(rare_sb.bg_color == Color("#38A0FF"), "選中稀有 Chip 背景色應為 #38A0FF")

	# 3. 點擊「史詩」Chip: 應有 1 把史詩武器
	var epic_chip: Button = _dialog.get_quality_chip("epic")
	epic_chip.emit_signal("pressed")
	_assert(_dialog.get_current_filter_quality() == "epic", "當前品質篩選應為 epic")
	_assert(_dialog.get_visible_weapons_count() == 1, "史詩武器應過濾出 1 把 (實際: %d)" % _dialog.get_visible_weapons_count())

	# 4. 點擊「傳說」Chip: 應有 1 把傳說武器
	var leg_chip: Button = _dialog.get_quality_chip("legendary")
	leg_chip.emit_signal("pressed")
	_assert(_dialog.get_current_filter_quality() == "legendary", "當前品質篩選應為 legendary")
	_assert(_dialog.get_visible_weapons_count() == 1, "傳說武器應過濾出 1 把 (實際: %d)" % _dialog.get_visible_weapons_count())

	# 5. 點擊「凡品」Chip: 應有 2 把凡品武器 (當前槽位 1 + 背包 1)
	var com_chip: Button = _dialog.get_quality_chip("common")
	com_chip.emit_signal("pressed")
	_assert(_dialog.get_visible_weapons_count() == 2, "凡品武器應過濾出 2 把 (實際: %d)" % _dialog.get_visible_weapons_count())

	# 6. 點擊「全部」Chip: 還原至 7 把
	var all_chip: Button = _dialog.get_quality_chip("all")
	all_chip.emit_signal("pressed")
	_assert(_dialog.get_visible_weapons_count() == 7, "還原「全部」應為 7 把 (實際: %d)" % _dialog.get_visible_weapons_count())

	print("  ok 各品質 Chip 點選即時過濾與全部還原驗證通過")


func _test_stacked_filtering_with_line_and_sorting() -> void:
	print("\n--- 4. 檢驗流派 Chip + 品質 Chip 雙向疊加篩選與攻擊力排序 ---")
	var gs = root.get_node_or_null("GameState")

	# 背包包含多把劍，不同攻擊力與品質
	var mock_bag := [
		{"uid": "sw_com_1", "slot": "weapon", "name": "凡品鐵劍A", "line": "sword", "quality": "common", "weapon_atk": 25},
		{"uid": "sw_rare_low", "slot": "weapon", "name": "青鋒劍(稀有低攻)", "line": "sword", "quality": "rare", "weapon_atk": 40},
		{"uid": "sw_rare_high", "slot": "weapon", "name": "碧落霜華(稀有高攻)", "line": "sword", "quality": "rare", "weapon_atk": 55},
		{"uid": "bw_rare_1", "slot": "weapon", "name": "穿雲弓(稀有)", "line": "bow", "quality": "rare", "weapon_atk": 50},
		{"uid": "sw_epic_1", "slot": "weapon", "name": "滅寂魔劍(史詩)", "line": "sword", "quality": "epic", "weapon_atk": 70},
	]
	gs.equip_bag = mock_bag.duplicate(true)
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]

	_dialog.setup(0)

	# 1. 疊加: 流派=劍 + 品質=稀有
	_dialog.set_line_filter("sword")
	_dialog.set_quality_filter("rare")

	var filtered := _dialog.get_candidate_weapons()
	_assert(filtered.size() == 2, "流派=劍 且 品質=稀有 應過濾出 2 把劍 (實際: %d)" % filtered.size())

	# 2. 驗證攻擊力降序排序: 55 atk 必須排在 40 atk 前面
	_assert(WeaponSwapDialogScript.get_weapon_atk(filtered[0]) == 55, "第 1 把武器應為高攻 55")
	_assert(WeaponSwapDialogScript.get_weapon_atk(filtered[1]) == 40, "第 2 把武器應為低攻 40")

	# 3. 疊加: 流派=弓 + 品質=稀有
	_dialog.set_line_filter("bow")
	var bow_rare := _dialog.get_candidate_weapons()
	_assert(bow_rare.size() == 1, "流派=弓 且 品質=稀有 應為 1 把 (實際: %d)" % bow_rare.size())
	_assert(bow_rare[0]["uid"] == "bw_rare_1", "武器 uid 應為 bw_rare_1")

	# 4. 疊加信號驗證
	var sig_state := {"received": false, "quality": ""}
	_dialog.quality_filter_changed.connect(func(qid: String):
		sig_state["received"] = true
		sig_state["quality"] = qid
	)
	_dialog.set_quality_filter("epic")
	_assert(bool(sig_state["received"]) and str(sig_state["quality"]) == "epic", "切換品質應觸發 quality_filter_changed 信號")

	print("  ok 流派 Chip 與品質 Chip 疊加篩選及攻擊力排序降序驗證通過")


func _test_empty_filter_state() -> void:
	print("\n--- 5. 檢驗品質過濾無匹配武器時之友善空狀態面板 ---")
	var gs = root.get_node_or_null("GameState")
	gs.equip_bag = [
		{"uid": "w1", "slot": "weapon", "name": "普通劍", "line": "sword", "quality": "common", "weapon_atk": 20}
	]
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]

	_dialog.setup(0)

	# 1. 僅選傳說品質 (無傳說武器)
	_dialog.set_line_filter("all")
	_dialog.set_quality_filter("legendary")

	var empty_panel: PanelContainer = _dialog.get_node_or_null("DialogCard/RootVBox/WeaponsScroll/WeaponsBox/EmptyPanel")
	_assert(empty_panel != null, "必須包含 EmptyPanel")
	_assert(empty_panel.visible, "無匹配武器時 EmptyPanel 必須為 visible")

	var empty_title: Label = empty_panel.find_child("EmptyTitle", true, false) as Label
	var empty_sub: Label = empty_panel.find_child("EmptySub", true, false) as Label
	_assert(empty_title != null and not empty_title.text.is_empty(), "空狀態標題不可為空")
	_assert(empty_sub != null and not empty_sub.text.is_empty(), "空狀態副標題不可為空")
	_assert(not _has_emoji(empty_title.text), "空狀態標題不可包含 Emoji")
	_assert(not _has_emoji(empty_sub.text), "空狀態副標題不可包含 Emoji")

	# 2. 同時選槍 + 史詩 (雙重無匹配)
	_dialog.set_line_filter("spear")
	_dialog.set_quality_filter("epic")
	_assert(empty_panel.visible, "雙重無匹配時 EmptyPanel 必須為 visible")
	_assert(not empty_title.text.is_empty(), "雙重無匹配空狀態標題正常")

	print("  ok 品質過濾友善空狀態面板驗證通過")


func _test_i18n_locales() -> void:
	print("\n--- 6. 檢驗六語系即時切換與 ContentLoc 在地化連動 ---")
	var loc = root.get_node_or_null("Loc")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

	for code in locales:
		if loc:
			loc.call("set_locale", code)

		var chips := _dialog.get_quality_chips()
		for qid in ["all", "common", "uncommon", "rare", "epic", "legendary"]:
			var btn: Button = chips[qid]
			_assert(not btn.text.is_empty(), "[%s] 品質 Chip '%s' 文字不可為空" % [code, qid])
			_assert(not _has_emoji(btn.text), "[%s] 品質 Chip '%s' 文字不可有 Emoji: %s" % [code, qid, btn.text])

		# 抽驗各語系代表詞
		match code:
			"en":
				_assert(chips["all"].text == "All", "en all 應為 All")
				_assert(chips["common"].text == "Common", "en common 應為 Common")
				_assert(chips["rare"].text == "Rare", "en rare 應為 Rare")
				_assert(chips["legendary"].text == "Legendary", "en legendary 應為 Legendary")
			"zh_CN":
				_assert(chips["epic"].text == "史诗", "zh_CN epic 應為 史诗")
				_assert(chips["legendary"].text == "传说", "zh_CN legendary 應為 传说")
			"ja":
				_assert(chips["legendary"].text == "伝説", "ja legendary 應為 伝説")
			"ko":
				_assert(chips["all"].text == "전체", "ko all 應為 전체")
				_assert(chips["legendary"].text == "전설", "ko legendary 應為 전설")
			"es":
				_assert(chips["all"].text == "Todo", "es all 應為 Todo")
				_assert(chips["legendary"].text == "Legendario", "es legendary 應為 Legendario")

	# 切回繁中
	if loc:
		loc.call("set_locale", "zh_TW")

	print("  ok 六語系即時切換與在地化對照驗證合格")


func _setup_dialog_for_proof(line: String, quality: String) -> void:
	_cleanup_dialog()
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.equip_bag = [
			{"uid": "proof_w1", "slot": "weapon", "name": "青霜寒劍", "line": "sword", "quality": "rare", "quality_label": "稀有", "weapon_atk": 45, "rolled": {"def": 12, "hp": 30}},
			{"uid": "proof_w2", "slot": "weapon", "name": "烈火重斧", "line": "axe", "quality": "epic", "quality_label": "史詩", "weapon_atk": 65, "rolled": {"crit_dmg": 15.0}},
			{"uid": "proof_w3", "slot": "weapon", "name": "星辰神弓", "line": "bow", "quality": "legendary", "quality_label": "傳說", "weapon_atk": 85, "rolled": {"crit": 12.0}},
			{"uid": "proof_w4", "slot": "weapon", "name": "工匠短匕", "line": "dagger", "quality": "uncommon", "quality_label": "精工", "weapon_atk": 30},
			{"uid": "proof_w5", "slot": "weapon", "name": "白鐵長劍", "line": "sword", "quality": "common", "quality_label": "凡品", "weapon_atk": 22},
		]
		var cur_w := {"uid": "proof_eq0", "slot": "weapon", "name": "巡管戰劍", "line": "sword", "quality": "common", "quality_label": "凡品", "weapon_atk": 20}
		gs.equip_worn = {"proof_eq0": cur_w}
		gs.weapon_loadout = ["proof_eq0", "", ""]

	_dialog = WeaponSwapDialogScript.new(0)
	root.add_child(_dialog)
	_dialog.setup(0)
	_dialog.set_line_filter(line)
	_dialog.set_quality_filter(quality)


func _cleanup_dialog() -> void:
	if is_instance_valid(_dialog):
		_dialog.queue_free()
		_dialog = null


func _capture_and_record(path: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null:
		return
	img.save_png(path)
	var f := FileAccess.open(path, FileAccess.READ)
	if f != null:
		var buf := f.get_buffer(f.get_length())
		f.close()
		var hash_str := FileAccess.get_sha256(path)
		_hashes.append(hash_str)
		print("  -> 截圖存證: %s (SHA256: %s)" % [path.get_file(), hash_str.substr(0, 16)])


func _verify_hashes() -> void:
	print("--- 檢查截圖 SHA256 唯一性 ---")
	for i in range(_hashes.size()):
		for j in range(i + 1, _hashes.size()):
			if _hashes[i] == _hashes[j]:
				_fail("截圖雜湊比對失敗：第 %d 張與第 %d 張 SHA256 相同！" % [i + 1, j + 1])
				return
	print("  ok 所有截圖存證雜湊皆獨立唯一")


func _has_emoji(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if code >= 0x1F300 and code <= 0x1F9FF:
			return true
		if code >= 0x2600 and code <= 0x27BF:
			return true
	return false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail("斷言失敗: " + msg)


func _fail(msg: String) -> void:
	print("FAIL: " + msg)
	quit(1)
