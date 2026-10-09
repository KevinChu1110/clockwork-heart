extends SceneTree
## 單元與驗收測試：WeaponSwapDialog 支援流派篩選 Chip 列 (t_82892ad5)
## 覆蓋項目：
## 1. 武器清單上方水平捲動流派篩選 Chip 按鈕列（全部、劍、長槍、斧、錘、匕首、鎚、拳套、爪、法杖、靈晶、弓、銃）。
## 2. 按鈕熱區 >= 48px，果凍厚底 (4~5px)，圓角 12~16px，使用粉圓體，零系統 Emoji。
## 3. 點選各流派 Chip 即時過濾候選武器清單，僅顯示對應流派武器；選中呈現多巴胺暖橘高亮 (#FFA010)，未選中呈現柔和米黃底。
## 4. 點選「全部」時呈現所有候選武器。
## 5. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化連動與零 Emoji。
## 6. 實機渲染環境下產出 3 張獨立 SHA256 存證截圖。

const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _out_dir: String = ""
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _dialog: WeaponSwapDialogScript = null
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	print("== 開始執行 WeaponSwapDialog 流派篩選 Chip 驗收測試 (t_82892ad5) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_82892ad5")
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
			_test_static_line_matching()
			_step = 1
		1:
			_test_chip_bar_and_attributes()
			_step = 2
		2:
			_test_candidate_filtering_and_chip_clicking()
			_step = 3
		3:
			_test_empty_filter_state()
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
			_setup_dialog_for_proof("all")
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 8:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_filter_all.png")
			_h1 = _capture_and_save(p1)
			_dialog.set_line_filter("bow")
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 8:
				return false
			var p2 := _out_dir.path_join("proof_02_weapon_swap_filter_bow.png")
			_h2 = _capture_and_save(p2)
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			_dialog.set_line_filter("all")
			_wait = 0
			_step = 9
		9:
			_wait += 1
			if _wait < 8:
				return false
			var p3 := _out_dir.path_join("proof_03_weapon_swap_filter_en.png")
			_h3 = _capture_and_save(p3)
			_step = 10
		10:
			if DisplayServer.get_name() != "headless":
				_verify_hashes()
			_cleanup_dialog()
			print("\n=======================================================")
			print("  TEST_LOBBY_WEAPON_SWAP_FILTER_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _test_static_line_matching() -> void:
	print("\n--- 1. 檢驗靜態流派正規化與篩選比對函數 ---")
	_assert(WeaponSwapDialogScript.matches_line_filter("sword", "all"), "all 應匹配 sword")
	_assert(WeaponSwapDialogScript.matches_line_filter("bow", "all"), "all 應匹配 bow")
	_assert(WeaponSwapDialogScript.matches_line_filter("hammer", "all"), "all 應匹配 hammer")
	_assert(WeaponSwapDialogScript.matches_line_filter("sword", "全部"), "全部 應匹配 sword")

	_assert(WeaponSwapDialogScript.matches_line_filter("sword", "sword"), "sword 應匹配 sword")
	_assert(WeaponSwapDialogScript.matches_line_filter("sword", "劍"), "劍 應匹配 sword")
	_assert(not WeaponSwapDialogScript.matches_line_filter("sword", "spear"), "sword 不應匹配 spear")

	# 鎚 / 錘 雙向對應
	_assert(WeaponSwapDialogScript.matches_line_filter("hammer", "hammer"), "hammer 應匹配 hammer")
	_assert(WeaponSwapDialogScript.matches_line_filter("hammer", "hammer_alt"), "hammer_alt 應匹配 hammer")
	_assert(WeaponSwapDialogScript.matches_line_filter("hammer", "鎚"), "鎚 應匹配 hammer")
	_assert(WeaponSwapDialogScript.matches_line_filter("hammer", "錘"), "錘 應匹配 hammer")
	_assert(WeaponSwapDialogScript.matches_line_filter("鎚", "hammer"), "hammer 應匹配 鎚")
	_assert(WeaponSwapDialogScript.matches_line_filter("錘", "hammer"), "hammer 應匹配 錘")

	# 其他武器流派比對
	_assert(WeaponSwapDialogScript.matches_line_filter("spear", "長槍"), "長槍 應匹配 spear")
	_assert(WeaponSwapDialogScript.matches_line_filter("axe", "斧"), "斧 應匹配 axe")
	_assert(WeaponSwapDialogScript.matches_line_filter("dagger", "匕首"), "匕首 應匹配 dagger")
	_assert(WeaponSwapDialogScript.matches_line_filter("fist", "拳套"), "拳套 應匹配 fist")
	_assert(WeaponSwapDialogScript.matches_line_filter("claw", "爪"), "爪 應匹配 claw")
	_assert(WeaponSwapDialogScript.matches_line_filter("magic", "法杖"), "法杖 應匹配 magic")
	_assert(WeaponSwapDialogScript.matches_line_filter("crystal", "靈晶"), "靈晶 應匹配 crystal")
	_assert(WeaponSwapDialogScript.matches_line_filter("bow", "弓"), "弓 應匹配 bow")
	_assert(WeaponSwapDialogScript.matches_line_filter("gun", "銃"), "銃 應匹配 gun")

	print("  ok matches_line_filter 與 _normalize_line 驗證通過")


func _test_chip_bar_and_attributes() -> void:
	print("\n--- 2. 檢驗流派篩選 Chip 列結構、熱區與樣式規範 ---")
	_setup_dialog_for_proof("all")

	var scroll := _dialog.get_node_or_null("DialogCard/RootVBox/LineFilterScroll")
	_assert(scroll != null, "必須包含 LineFilterScroll 節點")
	_assert(scroll is ScrollContainer, "LineFilterScroll 必須為 ScrollContainer")

	var hbox := scroll.get_node_or_null("LineFilterHBox")
	_assert(hbox != null, "必須包含 LineFilterHBox 節點")
	_assert(hbox is HBoxContainer, "LineFilterHBox 必須為 HBoxContainer")

	var chips: Dictionary = _dialog.get_filter_chips()
	_assert(chips.size() == 13, "必須包含 13 個流派篩選 Chip 按鈕 (實際: %d)" % chips.size())

	var expected_ids := [
		"all", "sword", "spear", "axe", "hammer_alt", "dagger",
		"hammer", "fist", "claw", "magic", "crystal", "bow", "gun"
	]
	for cid in expected_ids:
		_assert(chips.has(cid), "Chip 列表必須包含 id '%s'" % cid)
		var btn: Button = chips[cid]
		_assert(btn.custom_minimum_size.y >= 48, "按鈕熱區高度必須 >= 48px (實際: %.1f)" % btn.custom_minimum_size.y)
		_assert(not _has_emoji(btn.text), "按鈕文字不可包含系統 Emoji: %s" % btn.text)

	# 檢查預設選中 Chip 為 "all"，樣式呈現多巴胺暖橘高亮 (#FFA010)
	var all_btn: Button = chips["all"]
	var normal_sb: StyleBoxFlat = all_btn.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(normal_sb != null, "Chip 按鈕必須套用 StyleBoxFlat")
	_assert(normal_sb.bg_color == WeaponSwapDialogScript.COLOR_ORANGE, "選中 Chip 背景色必須為多巴胺暖橘 #FFA010")
	_assert(normal_sb.border_width_bottom == 5, "選中 Chip 果凍厚底必須為 5px")
	_assert(normal_sb.corner_radius_top_left >= 12 and normal_sb.corner_radius_top_left <= 16, "圓角必須在 12~16px")

	# 檢查未選中 Chip 為柔和米黃底
	var sword_btn: Button = chips["sword"]
	var unsel_sb: StyleBoxFlat = sword_btn.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(unsel_sb != null, "未選中 Chip 必須套用 StyleBoxFlat")
	_assert(unsel_sb.bg_color == WeaponSwapDialogScript.COLOR_CARD_WARM, "未選中 Chip 背景色必須為柔和米黃底 #FFF8E7")
	_assert(unsel_sb.border_width_bottom == 4, "未選中 Chip 果凍底厚度為 4px")

	print("  ok LineFilterScroll 與 13 個 Chip 按鈕樣式驗證合格")


func _test_candidate_filtering_and_chip_clicking() -> void:
	print("\n--- 3. 檢驗點擊流派 Chip 即時過濾候選清單與「全部」還原 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 準備 11 種不同流派的武器
	var mock_bag := [
		{"uid": "b_sword", "slot": "weapon", "name": "晨曦長劍", "line": "sword", "weapon_atk": 50},
		{"uid": "b_spear", "slot": "weapon", "name": "疾風戰槍", "line": "spear", "weapon_atk": 45},
		{"uid": "b_axe", "slot": "weapon", "name": "熔爐重斧", "line": "axe", "weapon_atk": 60},
		{"uid": "b_hammer", "slot": "weapon", "name": "碎岩鐵鎚", "line": "hammer", "weapon_atk": 55},
		{"uid": "b_dagger", "slot": "weapon", "name": "暗影短匕", "line": "dagger", "weapon_atk": 40},
		{"uid": "b_fist", "slot": "weapon", "name": "暴烈拳套", "line": "fist", "weapon_atk": 35},
		{"uid": "b_claw", "slot": "weapon", "name": "裂鋼雙爪", "line": "claw", "weapon_atk": 42},
		{"uid": "b_magic", "slot": "weapon", "name": "星盤法杖", "line": "magic", "weapon_atk": 48},
		{"uid": "b_crystal", "slot": "weapon", "name": "太極靈晶", "line": "crystal", "weapon_atk": 38},
		{"uid": "b_bow", "slot": "weapon", "name": "獵風神弓", "line": "bow", "weapon_atk": 52},
		{"uid": "b_gun", "slot": "weapon", "name": "雷火長銃", "line": "gun", "weapon_atk": 65},
	]
	gs.equip_bag = mock_bag.duplicate(true)

	# 槽位 0 裝備一把劍
	var cur_w := {"uid": "eq_slot0", "slot": "weapon", "name": "生鏽鐵劍", "line": "sword", "weapon_atk": 20}
	gs.equip_worn = {"eq_slot0": cur_w}
	gs.weapon_loadout = ["eq_slot0", "", ""]

	_dialog.setup(0)

	# 1. 驗證「全部」: 呈現所有 12 把候選武器 (1 當前槽位 + 11 背包)
	_dialog.set_line_filter("all")
	var all_candidates: Array = _dialog.get_candidate_weapons()
	_assert(all_candidates.size() == 12, "選「全部」時應呈現所有 12 把候選武器 (實際: %d)" % all_candidates.size())

	# 2. 點擊「弓」Chip: 僅呈現弓流派
	var bow_chip: Button = _dialog.get_filter_chip("bow")
	_assert(bow_chip != null, "應取得 bow chip 按鈕")
	bow_chip.emit_signal("pressed")
	_assert(_dialog.get_current_filter_line() == "bow", "當前流派篩選應切換為 bow")

	var bow_candidates: Array = _dialog.get_candidate_weapons()
	_assert(bow_candidates.size() == 1, "過濾「弓」應僅有 1 把武器 (實際: %d)" % bow_candidates.size())
	_assert(bow_candidates[0]["uid"] == "b_bow", "過濾結果應為 b_bow")
	var bow_sb: StyleBoxFlat = bow_chip.get_theme_stylebox("normal") as StyleBoxFlat
	_assert(bow_sb.bg_color == WeaponSwapDialogScript.COLOR_ORANGE, "選中 bow Chip 應高亮 #FFA010")

	# 3. 點擊「長槍」Chip
	var spear_chip: Button = _dialog.get_filter_chip("spear")
	spear_chip.emit_signal("pressed")
	var spear_candidates: Array = _dialog.get_candidate_weapons()
	_assert(spear_candidates.size() == 1 and spear_candidates[0]["uid"] == "b_spear", "過濾長槍結果應為 b_spear")

	# 4. 點擊「鎚」(hammer) Chip
	var hammer_chip: Button = _dialog.get_filter_chip("hammer")
	hammer_chip.emit_signal("pressed")
	var hammer_candidates: Array = _dialog.get_candidate_weapons()
	_assert(hammer_candidates.size() == 1 and hammer_candidates[0]["uid"] == "b_hammer", "過濾鎚結果應為 b_hammer")

	# 5. 點擊「錘」(hammer_alt) Chip
	var hammer_alt_chip: Button = _dialog.get_filter_chip("hammer_alt")
	hammer_alt_chip.emit_signal("pressed")
	var hammer_alt_candidates: Array = _dialog.get_candidate_weapons()
	_assert(hammer_alt_candidates.size() == 1 and hammer_alt_candidates[0]["uid"] == "b_hammer", "過濾錘結果應為 b_hammer")

	# 6. 點擊「劍」Chip: 當前槽位劍 + 背包劍 = 2 把
	var sword_chip: Button = _dialog.get_filter_chip("sword")
	sword_chip.emit_signal("pressed")
	var sword_candidates: Array = _dialog.get_candidate_weapons()
	_assert(sword_candidates.size() == 2, "過濾劍應包含當前劍與背包劍共 2 把 (實際: %d)" % sword_candidates.size())

	# 7. 點回「全部」Chip: 還原為 12 把
	var all_chip: Button = _dialog.get_filter_chip("all")
	all_chip.emit_signal("pressed")
	_assert(_dialog.get_candidate_weapons().size() == 12, "點回全部應還原為 12 把武器")

	print("  ok 各流派 Chip 點選即時過濾與全部還原驗證通過")


func _test_empty_filter_state() -> void:
	print("\n--- 4. 檢驗流派過濾無匹配武器時之空狀態面板 ---")
	var gs = root.get_node_or_null("GameState")
	# 背包僅放一把劍，無任何法杖
	gs.equip_bag = [
		{"uid": "b_only_sword", "slot": "weapon", "name": "單把劍", "line": "sword", "weapon_atk": 20}
	]
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]
	_dialog.setup(0)

	_dialog.set_line_filter("magic")
	var magic_candidates: Array = _dialog.get_candidate_weapons()
	_assert(magic_candidates.is_empty(), "無匹配流派候選清單應為空")

	var empty_panel := _dialog.get_node_or_null("DialogCard/RootVBox/WeaponsScroll/WeaponsBox/EmptyPanel")
	_assert(empty_panel != null, "必須包含 EmptyPanel")
	_assert(empty_panel.visible, "無匹配流派時 EmptyPanel 必須可見")

	print("  ok 空狀態面板顯示正確")


func _test_i18n_locales() -> void:
	print("\n--- 5. 檢驗六語系即時切換與 ContentLoc 連動 ---")
	var loc = root.get_node_or_null("Loc")
	var test_locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

	var expected_all := {
		"zh_TW": "全部", "zh_CN": "全部", "en": "All", "ja": "全部", "ko": "전체", "es": "Todo"
	}
	var expected_sword := {
		"zh_TW": "劍", "zh_CN": "剑", "en": "Sword", "ja": "剣", "ko": "검", "es": "Espada"
	}
	var expected_spear := {
		"zh_TW": "長槍", "zh_CN": "长枪", "en": "Spear", "ja": "長槍", "ko": "창", "es": "Lanza"
	}
	var expected_bow := {
		"zh_TW": "弓", "zh_CN": "弓", "en": "Bow", "ja": "弓", "ko": "활", "es": "Arco"
	}
	var expected_gun := {
		"zh_TW": "銃", "zh_CN": "铳", "en": "Gun", "ja": "銃", "ko": "총", "es": "Fusil"
	}
	var expected_hammer := {
		"zh_TW": "鎚", "zh_CN": "锤", "en": "Hammer", "ja": "槌", "ko": "망치", "es": "Martillo"
	}
	var expected_hammer_alt := {
		"zh_TW": "錘", "zh_CN": "锤", "en": "Mace", "ja": "金槌", "ko": "철퇴", "es": "Maza"
	}

	for code in test_locales:
		loc.call("set_locale", code)
		_assert(not _has_emoji(_dialog.get_filter_chip("all").text), "[%s] 全部 Chip 不得含 Emoji" % code)
		_assert(_dialog.get_filter_chip("all").text == expected_all[code],
			"[%s] 全部 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_all[code], _dialog.get_filter_chip("all").text])
		_assert(_dialog.get_filter_chip("sword").text == expected_sword[code],
			"[%s] 劍 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_sword[code], _dialog.get_filter_chip("sword").text])
		_assert(_dialog.get_filter_chip("spear").text == expected_spear[code],
			"[%s] 長槍 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_spear[code], _dialog.get_filter_chip("spear").text])
		_assert(_dialog.get_filter_chip("bow").text == expected_bow[code],
			"[%s] 弓 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_bow[code], _dialog.get_filter_chip("bow").text])
		_assert(_dialog.get_filter_chip("gun").text == expected_gun[code],
			"[%s] 銃 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_gun[code], _dialog.get_filter_chip("gun").text])
		_assert(_dialog.get_filter_chip("hammer").text == expected_hammer[code],
			"[%s] 鎚 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_hammer[code], _dialog.get_filter_chip("hammer").text])
		_assert(_dialog.get_filter_chip("hammer_alt").text == expected_hammer_alt[code],
			"[%s] 錘 Chip 文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected_hammer_alt[code], _dialog.get_filter_chip("hammer_alt").text])
		print("  ok [%s] 語系在地化正確: all=%s, sword=%s, spear=%s, bow=%s, gun=%s" % [
			code,
			_dialog.get_filter_chip("all").text,
			_dialog.get_filter_chip("sword").text,
			_dialog.get_filter_chip("spear").text,
			_dialog.get_filter_chip("bow").text,
			_dialog.get_filter_chip("gun").text,
		])

	# 測試完切回 zh_TW
	loc.call("set_locale", "zh_TW")


func _setup_dialog_for_proof(filter_id: String) -> void:
	_cleanup_dialog()
	var gs = root.get_node_or_null("GameState")
	if gs:
		gs.equip_bag = [
			{"uid": "b_sword", "slot": "weapon", "name": "晨曦長劍", "line": "sword", "weapon_atk": 50},
			{"uid": "b_bow", "slot": "weapon", "name": "獵風神弓", "line": "bow", "weapon_atk": 52},
			{"uid": "b_spear", "slot": "weapon", "name": "疾風戰槍", "line": "spear", "weapon_atk": 45},
			{"uid": "b_axe", "slot": "weapon", "name": "熔爐重斧", "line": "axe", "weapon_atk": 60},
			{"uid": "b_gun", "slot": "weapon", "name": "雷火長銃", "line": "gun", "weapon_atk": 65},
		]
		gs.equip_worn = {
			"eq_slot0": {"uid": "eq_slot0", "slot": "weapon", "name": "守護者之刃", "line": "sword", "weapon_atk": 30}
		}
		gs.weapon_loadout = ["eq_slot0", "", ""]

	_dialog = WeaponSwapDialogScript.new(0)
	root.add_child(_dialog)
	_dialog.setup(0)
	_dialog.set_line_filter(filter_id)


func _cleanup_dialog() -> void:
	if _dialog != null and is_instance_valid(_dialog):
		_dialog.queue_free()
		_dialog = null


func _capture_and_save(file_path: String) -> String:
	var img := root.get_texture().get_image()
	if img == null or img.is_empty():
		_fail("無法自 Viewport 獲取 Image")
		return ""
	var err := img.save_png(file_path)
	if err != OK:
		_fail("儲存截圖失敗: %s (err=%d)" % [file_path, err])
		return ""
	var fa := FileAccess.open(file_path, FileAccess.READ)
	if fa == null:
		_fail("無法讀取存證截圖: %s" % file_path)
		return ""
	var raw := fa.get_buffer(fa.get_length())
	var h := raw.hex_encode()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(raw)
	var sha := ctx.finish().hex_encode()
	print("  [截圖存證] %s (SHA256: %s)" % [file_path.get_file(), sha])
	return sha


func _verify_hashes() -> void:
	_assert(_h1 != "" and _h2 != "" and _h3 != "", "3 張存證截圖 SHA256 不得為空")
	_assert(_h1 != _h2, "截圖 1 與截圖 2 SHA256 不得相同（必須呈現流派切換動態）")
	_assert(_h2 != _h3, "截圖 2 與截圖 3 SHA256 不得相同（必須呈現多語系切換）")
	_assert(_h1 != _h3, "截圖 1 與截圖 3 SHA256 不得相同")
	print("  ok 3 張實機截圖 SHA256 皆獨立不重複，存證合格")


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail("斷言失敗: " + msg)


func _fail(msg: String) -> void:
	push_error("[TEST FAIL] " + msg)
	printerr("[TEST FAIL] " + msg)
	print("TEST_LOBBY_WEAPON_SWAP_FILTER_FAIL: " + msg)
	quit(1)
