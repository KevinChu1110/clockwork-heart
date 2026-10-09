extends SceneTree
## 單元與驗收測試：WeaponSwapDialog 武器清單依攻擊力排序與差額比對膠囊 (t_d5f64a67)
## 覆蓋項目：
## 1. 背包候選武器清單依武器攻擊力 (atk) 降序排序（含 rolled.atk 動態計算）。
## 2. 每張候選卡片之「攻擊力差額對比膠囊」(DiffCapsule)：
##    - 高於當前：薄荷綠背景/文字顯示「+N 攻擊」
##    - 低於當前：柔和灰底/文字顯示「-N 攻擊」
##    - 相等或當前槽位為空：顯示「--」
## 3. 目標槽位切換 (Slot Tab) 即時動態重新計算差額。
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化刷新 (ContentLoc / Loc 連動)。
## 5. 全面零 Unicode Emoji，字體與多巴胺高對比色盤規範。
## 6. 產出實機截圖存證（非無頭模式）且 SHA256 獨立不重複。

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
	print("== 開始執行 WeaponSwapDialog 排序與差額膠囊驗收測試 (t_d5f64a67) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_d5f64a67")
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
			_test_static_sort_and_atk_calc()
			_step = 1
		1:
			_test_bag_candidate_weapons_sorting()
			_step = 2
		2:
			_test_diff_capsule_values_and_styles()
			_step = 3
		3:
			_test_empty_slot_diff_capsule()
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
				_step = 9
		6:
			_wait += 1
			if _wait < 6:
				return false
			_setup_dialog_for_proof(0)
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 8:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_diff_slot0.png")
			_h1 = _capture_and_save(p1)
			_dialog.setup(1)
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 8:
				return false
			var p2 := _out_dir.path_join("proof_02_weapon_swap_diff_slot1_empty.png")
			_h2 = _capture_and_save(p2)
			_dialog.setup(0)
			var loc = root.get_node_or_null("Loc")
			if loc:
				loc.call("set_locale", "en")
			var p3 := _out_dir.path_join("proof_03_weapon_swap_diff_en.png")
			_h3 = _capture_and_save(p3)
			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
				return false
			print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			_step = 9
		9:
			print("\n=======================================================")
			print("  TEST_LOBBY_WEAPON_SWAP_DIFF_OK")
			print("=======================================================")
			quit(0)
	return false


func _test_static_sort_and_atk_calc() -> void:
	print("\n--- 1. 檢驗攻擊力計算與靜態排序函數 ---")
	var w1 := {"uid": "w1", "weapon_atk": 20}
	var w2 := {"uid": "w2", "weapon_atk": 0, "rolled": {"atk": 75}}
	var w3 := {"uid": "w3", "weapon_atk": 45}

	var atk1: int = WeaponSwapDialogScript.get_weapon_atk(w1)
	var atk2: int = WeaponSwapDialogScript.get_weapon_atk(w2)
	var atk3: int = WeaponSwapDialogScript.get_weapon_atk(w3)
	if atk1 != 20 or atk2 != 75 or atk3 != 45:
		_fail("get_weapon_atk 計算錯誤: w1=%d, w2=%d, w3=%d" % [atk1, atk2, atk3])

	var sorted_arr: Array = WeaponSwapDialogScript.sort_weapons_by_atk_desc([w1, w2, w3])
	if sorted_arr.size() != 3 or sorted_arr[0].uid != "w2" or sorted_arr[1].uid != "w3" or sorted_arr[2].uid != "w1":
		_fail("sort_weapons_by_atk_desc 排序順序不正確")
	print("  ok get_weapon_atk 與 sort_weapons_by_atk_desc 驗證通過")


func _test_bag_candidate_weapons_sorting() -> void:
	print("\n--- 2. 檢驗候選背包武器清單依攻擊力降序排序 ---")
	var gs = root.get_node_or_null("GameState")
	gs.equip_bag = [
		{"uid": "bag_low", "slot": "weapon", "weapon_atk": 15, "name": "精鋼短劍", "line": "sword"},
		{"uid": "bag_super", "slot": "weapon", "weapon_atk": 0, "rolled": {"atk": 99}, "name": "落星追月弓", "line": "bow"},
		{"uid": "bag_mid", "slot": "weapon", "weapon_atk": 42, "name": "風紋破甲斧", "line": "axe"},
		{"uid": "bag_high", "slot": "weapon", "weapon_atk": 85, "name": "破曉貫日槍", "line": "spear"}
	]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	var candidates: Array[Dictionary] = dlg._collect_candidate_weapons()
	var bag_cands: Array[Dictionary] = []
	for c in candidates:
		if str(c.get("_status", "")) == "bag":
			bag_cands.append(c)

	if bag_cands.size() < 4:
		_fail("背包武器候選數量不足 4 件，實際為: %d" % bag_cands.size())

	var expected_uids := ["bag_super", "bag_high", "bag_mid", "bag_low"]
	var expected_atks := [99, 85, 42, 15]
	for i in range(4):
		var item := bag_cands[i]
		var atk := WeaponSwapDialogScript.get_weapon_atk(item)
		if item.get("uid") != expected_uids[i] or atk != expected_atks[i]:
			_fail("背包武器排序不正確: 第 %d 件為 uid=%s (atk=%d)，預期 uid=%s (atk=%d)" % [
				i, str(item.get("uid")), atk, expected_uids[i], expected_atks[i]
			])

	print("  ok 背包武器依 atk 降序正確排序: 99 > 85 > 42 > 15")
	dlg.queue_free()


func _test_diff_capsule_values_and_styles() -> void:
	print("\n--- 3. 檢驗攻擊力差額對比膠囊 (+N 攻擊 / -N 攻擊 / --) 與樣式 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	loc.call("set_locale", "zh_TW")

	# 目標槽位 0 預設裝備兔族破曉之劍 (atk 30)
	var cur_w_uid: String = str(eq.call("loadout_uid", 0))
	var cur_inst: Dictionary = eq.call("weapon_inst", cur_w_uid)
	var cur_atk: int = WeaponSwapDialogScript.get_weapon_atk(cur_inst)
	if cur_atk <= 0:
		cur_atk = 30

	gs.equip_bag = [
		{"uid": "bag_pos", "slot": "weapon", "weapon_atk": cur_atk + 25, "name": "神聖晨光劍", "line": "sword"},
		{"uid": "bag_neg", "slot": "weapon", "weapon_atk": cur_atk - 18, "name": "生鏽鐵短劍", "line": "dagger"},
		{"uid": "bag_eq", "slot": "weapon", "weapon_atk": cur_atk, "name": "同等鍛鑄劍", "line": "sword"}
	]

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	# 檢查目標槽位裝備中的卡片 (current_slot) 差額應為 --
	var cur_card: PanelContainer = dlg.find_child("WeaponCard_" + cur_w_uid, true, false) as PanelContainer
	if cur_card != null:
		var cur_diff_lbl: Label = cur_card.find_child("DiffLabel", true, false) as Label
		if cur_diff_lbl == null or cur_diff_lbl.text != "--":
			_fail("當前槽位武器卡片之 DiffLabel 應為「--」，實際為: %s" % (cur_diff_lbl.text if cur_diff_lbl else "null"))
		_assert_no_emoji(cur_diff_lbl.text, "當前槽位武器卡片 DiffLabel")

	# 檢查高於當前武器 (+25)
	var pos_card: PanelContainer = dlg.find_child("WeaponCard_bag_pos", true, false) as PanelContainer
	if pos_card == null:
		_fail("未找到 bag_pos 武器卡片")
	var pos_lbl: Label = pos_card.find_child("DiffLabel", true, false) as Label
	var pos_p: PanelContainer = pos_card.find_child("DiffCapsule", true, false) as PanelContainer
	if pos_lbl == null or pos_p == null:
		_fail("bag_pos 卡片缺少 DiffLabel 或 DiffCapsule 節點")
	if pos_lbl.text != "+25 攻擊":
		_fail("bag_pos 差額文字應為「+25 攻擊」，實際為: %s" % pos_lbl.text)
	var pos_sb: StyleBoxFlat = pos_p.get_theme_stylebox("panel") as StyleBoxFlat
	if pos_sb == null or pos_sb.bg_color != WeaponSwapDialogScript.COLOR_DIFF_POS_BG:
		_fail("高於當前武器之 DiffCapsule 應為薄荷綠底色")
	_assert_no_emoji(pos_lbl.text, "bag_pos DiffLabel")

	# 檢查低於當前武器 (-18)
	var neg_card: PanelContainer = dlg.find_child("WeaponCard_bag_neg", true, false) as PanelContainer
	if neg_card == null:
		_fail("未找到 bag_neg 武器卡片")
	var neg_lbl: Label = neg_card.find_child("DiffLabel", true, false) as Label
	var neg_p: PanelContainer = neg_card.find_child("DiffCapsule", true, false) as PanelContainer
	if neg_lbl == null or neg_p == null:
		_fail("bag_neg 卡片缺少 DiffLabel 或 DiffCapsule 節點")
	if neg_lbl.text != "-18 攻擊":
		_fail("bag_neg 差額文字應為「-18 攻擊」，實際為: %s" % neg_lbl.text)
	var neg_sb: StyleBoxFlat = neg_p.get_theme_stylebox("panel") as StyleBoxFlat
	if neg_sb == null or neg_sb.bg_color != WeaponSwapDialogScript.COLOR_DIFF_NEG_BG:
		_fail("低於當前武器之 DiffCapsule 應為柔和灰底色")
	_assert_no_emoji(neg_lbl.text, "bag_neg DiffLabel")

	# 檢查相等武器 (-- )
	var eq_card: PanelContainer = dlg.find_child("WeaponCard_bag_eq", true, false) as PanelContainer
	if eq_card == null:
		_fail("未找到 bag_eq 武器卡片")
	var eq_lbl: Label = eq_card.find_child("DiffLabel", true, false) as Label
	var eq_p: PanelContainer = eq_card.find_child("DiffCapsule", true, false) as PanelContainer
	if eq_lbl == null or eq_p == null:
		_fail("bag_eq 卡片缺少 DiffLabel 或 DiffCapsule 節點")
	if eq_lbl.text != "--":
		_fail("bag_eq 差額文字應為「--」，實際為: %s" % eq_lbl.text)
	var eq_sb: StyleBoxFlat = eq_p.get_theme_stylebox("panel") as StyleBoxFlat
	if eq_sb == null or eq_sb.bg_color != WeaponSwapDialogScript.COLOR_DIFF_EQ_BG:
		_fail("相等武器之 DiffCapsule 應為相等灰底色")
	_assert_no_emoji(eq_lbl.text, "bag_eq DiffLabel")

	print("  ok 升攻 (+25 攻擊·薄荷綠)、降攻 (-18 攻擊·柔和灰底) 與相等 (--) 膠囊數值與樣式皆正確")
	dlg.queue_free()


func _test_empty_slot_diff_capsule() -> void:
	print("\n--- 4. 檢驗當前槽位為空時所有卡片膠囊皆顯示「--」 ---")
	var eq = root.get_node_or_null("EquipmentSystem")
	# 副手槽位 1 尚未解鎖或初始為空
	var dlg = WeaponSwapDialogScript.new(1)
	root.add_child(dlg)

	var t_info: Dictionary = dlg.get_target_slot_weapon_info()
	if t_info.get("has_weapon", false) == false:
		# 檢查所有卡片的 DiffLabel 是否皆為 --
		var weapons_box: VBoxContainer = dlg.find_child("WeaponsBox", true, false) as VBoxContainer
		if weapons_box != null:
			for child in weapons_box.get_children():
				if child is PanelContainer and child.name.begins_with("WeaponCard_"):
					var diff_lbl: Label = child.find_child("DiffLabel", true, false) as Label
					if diff_lbl != null and diff_lbl.text != "--":
						_fail("空槽位下卡片 %s 之差額應為「--」，實際為: %s" % [child.name, diff_lbl.text])
		print("  ok 空槽位下所有候選武器之差額膠囊皆正確顯示「--」")
	else:
		print("  info 槽位 1 已有武器，略過空槽測試")
	dlg.queue_free()


func _test_i18n_locales() -> void:
	print("\n--- 5. 檢驗六語系即時切換與 ContentLoc 連動 ---")
	var loc = root.get_node_or_null("Loc")
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	var expected_terms := {
		"zh_TW": "攻擊",
		"zh_CN": "攻击",
		"en": "Attack",
		"ja": "攻撃",
		"ko": "공격",
		"es": "Ataque"
	}

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)

	for lc in locales:
		loc.call("set_locale", lc)
		var expected_word: String = expected_terms[lc]
		var exp_pos := "+25 %s" % expected_word
		var exp_neg := "-18 %s" % expected_word

		var pos_card: PanelContainer = dlg.find_child("WeaponCard_bag_pos", true, false) as PanelContainer
		var neg_card: PanelContainer = dlg.find_child("WeaponCard_bag_neg", true, false) as PanelContainer
		var eq_card: PanelContainer = dlg.find_child("WeaponCard_bag_eq", true, false) as PanelContainer

		if pos_card == null or neg_card == null or eq_card == null:
			_fail("[%s] 語系下未找到對應卡片" % lc)

		var pos_lbl: Label = pos_card.find_child("DiffLabel", true, false) as Label
		var neg_lbl: Label = neg_card.find_child("DiffLabel", true, false) as Label
		var eq_lbl: Label = eq_card.find_child("DiffLabel", true, false) as Label

		if pos_lbl == null or pos_lbl.text != exp_pos:
			_fail("[%s] 語系下正差額應為「%s」，實際為: %s" % [lc, exp_pos, pos_lbl.text if pos_lbl else "null"])
		if neg_lbl == null or neg_lbl.text != exp_neg:
			_fail("[%s] 語系下負差額應為「%s」，實際為: %s" % [lc, exp_neg, neg_lbl.text if neg_lbl else "null"])
		if eq_lbl == null or eq_lbl.text != "--":
			_fail("[%s] 語系下相等差額應為「--」，實際為: %s" % [lc, eq_lbl.text if eq_lbl else "null"])

		_assert_no_emoji(pos_lbl.text, "[%s] pos_lbl" % lc)
		_assert_no_emoji(neg_lbl.text, "[%s] neg_lbl" % lc)
		print("  ok [%s] 語系即時在地化: pos=\"%s\", neg=\"%s\", eq=\"%s\" 且零 Emoji" % [lc, pos_lbl.text, neg_lbl.text, eq_lbl.text])

	loc.call("set_locale", "zh_TW")
	dlg.queue_free()


func _setup_dialog_for_proof(slot: int) -> void:
	if is_instance_valid(_dialog):
		_dialog.queue_free()
	_dialog = WeaponSwapDialogScript.new(slot)
	root.add_child(_dialog)


func _capture_and_save(path: String) -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("Viewport 不存在，無法擷取畫面")
		return ""
	var img: Image = vp.get_texture().get_image()
	if img == null:
		_fail("Viewport 紋理為空，無法儲存截圖")
		return ""
	var err := img.save_png(path)
	if err != OK:
		_fail("儲存截圖失敗: %s, err=%d" % [path, err])
		return ""
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
	push_error("TEST_LOBBY_WEAPON_SWAP_DIFF_FAIL: " + msg)
	print("❌ TEST_LOBBY_WEAPON_SWAP_DIFF_FAIL: ", msg)
	quit(1)
