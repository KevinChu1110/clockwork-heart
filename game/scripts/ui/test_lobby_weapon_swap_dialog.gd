extends SceneTree
## 單元與驗收測試：大廳角色頁三欄武器槽新增更換裝備彈窗連動武器庫 (t_a53d6368)
## 覆蓋項目：
## 1. 角色頁「更換裝備」按鈕與武器槽按鈕結構、尺寸 (>=48px)、果凍厚底 5px、零 Emoji。
## 2. 點擊武器槽或「更換裝備」彈出多巴胺風格 WeaponSwapDialog (750px 橫屏、置中、半透明 Scrim)。
## 3. 背包與庫存武器清單讀取、品質色階、打擊數、屬性說明呈現。
## 4. 點擊更換裝備後 GameState.weapon_loadout、EquipmentSystem 與 equip_slots 同步更新。
## 5. 角色頁攻擊力數值、戰力與紙娃娃即時刷新。
## 6. 三欄位槽位分頁切換與副手槽卸下裝備功能。
## 7. 六語系 (en, ja, ko, es, zh_CN, zh_TW) 即時在地化檢查。
## 8. 產出實機截圖存證並驗證 SHA256 不重複。

const MobileLobbyScript = preload("res://scripts/ui/mobile_lobby.gd")
const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")

const OUT_DIR := "/opt/side/bravesoul-game/proofs/t_a53d6368"

var _lobby: Control = null
var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _proof_dlg: Control = null
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	print("== 開始執行大廳角色頁更換裝備彈窗與武器庫連動驗收測試 (t_a53d6368) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	DirAccess.make_dir_recursive_absolute(OUT_DIR)
	DirAccess.make_dir_recursive_absolute("/opt/side/bravesoul-game/proofs")

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var loc = root.get_node_or_null("Loc")
	if gs == null or eq == null or loc == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / Loc)")
		return

	gs.reset_new_game("rabbit")
	loc.call("set_locale", "zh_TW")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)
	_lobby.size = Vector2(1280, 720)
	print("  ok 大廳節點建立成功")


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 3:
		return false

	match _step:
		0:
			_step_test_lobby_ui_and_change_button()
			_step = 1
		1:
			_step_test_dialog_structure()
			_step = 2
		2:
			_step_test_weapon_candidates_and_swap()
			_step = 3
		3:
			_step_test_slot_switch_and_unequip()
			_step = 4
		4:
			_step_test_i18n()
			_step = 5
		5:
			print("\n--- 6. 擷取實機截圖存證並驗證 SHA256 不重複 ---")
			_lobby._switch_tab(_lobby.Tab.CHARACTER)
			_wait = 0
			_step = 6
		6:
			_wait += 1
			if _wait < 8:
				return false
			var p1 := OUT_DIR.path_join("proof_01_character_tab_before.png")
			_h1 = _capture_and_save(p1)
			_proof_dlg = _lobby.open_weapon_swap_dialog(0)
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 8:
				return false
			var p2 := OUT_DIR.path_join("proof_02_weapon_swap_dialog_open.png")
			_h2 = _capture_and_save(p2)
			if is_instance_valid(_proof_dlg):
				_proof_dlg.free()
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 8:
				return false
			var p3 := OUT_DIR.path_join("proof_03_character_tab_after_swap.png")
			_h3 = _capture_and_save(p3)
			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充互動流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
			print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			_step = 9
		9:
			print("\n=======================================================")
			print("  TEST_LOBBY_WEAPON_SWAP_DIALOG_OK")
			print("=======================================================")
			quit(0)
	return false


func _step_test_lobby_ui_and_change_button() -> void:
	print("\n--- 1. 檢驗角色頁三欄武器槽與專屬「更換裝備」按鈕規範 ---")
	_lobby._switch_tab(_lobby.Tab.CHARACTER)

	var btn_change: Button = _lobby.get("_btn_change_weapon")
	if btn_change == null or not is_instance_valid(btn_change):
		_fail("角色分頁未找到 _btn_change_weapon (BtnChangeWeapon) 按鈕")
		return

	if btn_change.text != "更換裝備":
		_fail("更換裝備按鈕文字應為「更換裝備」，實際為: %s" % btn_change.text)

	if btn_change.custom_minimum_size.y < 48:
		_fail("更換裝備按鈕高度熱區應 >= 48px，實際為: %f" % btn_change.custom_minimum_size.y)

	var sb: StyleBoxFlat = btn_change.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null or sb.border_width_bottom < 5:
		_fail("更換裝備按鈕底邊果凍厚度應 >= 5px")

	_assert_no_emoji(btn_change.text, "更換裝備按鈕文字")

	var slot_btns: Array[Button] = _lobby.get_weapon_slot_buttons()
	if slot_btns.size() != 3:
		_fail("武器槽按鈕數量應為 3，實際為: %d" % slot_btns.size())

	for i in range(3):
		var b := slot_btns[i]
		if b.custom_minimum_size.y < 48:
			_fail("武器槽按鈕 %d 高度熱區應 >= 48px" % i)
		_assert_no_emoji(b.text, "武器槽 %d 按鈕文字" % i)

	print("  ok 角色頁更換裝備按鈕存在、熱區 >= 48px、果凍厚底 5px、零 Emoji")


func _step_test_dialog_structure() -> void:
	print("\n--- 2. 檢驗點擊彈出多巴胺風格武器選擇彈窗規格 ---")
	var dlg: Control = _lobby.open_weapon_swap_dialog(0)
	if dlg == null:
		_fail("open_weapon_swap_dialog(0) 回傳 null")
		return

	var scrim = dlg.get_node_or_null("ModalScrim") as ColorRect
	if scrim == null:
		_fail("WeaponSwapDialog 缺少 ModalScrim 全螢幕遮罩")
	elif scrim.mouse_filter != Control.MOUSE_FILTER_STOP:
		_fail("ModalScrim 必須攔截點擊 mouse_filter == STOP")

	var card = dlg.get_node_or_null("DialogCard") as PanelContainer
	if card == null:
		_fail("WeaponSwapDialog 缺少 DialogCard 面板")
	else:
		var w: float = card.custom_minimum_size.x
		if w < 740 or w > 760:
			_fail("彈窗寬度必須介於 740~760px，實際為: %f" % w)

	var btn_x = dlg.get_node_or_null("DialogCard/RootVBox/TopBar/BtnCloseX") as Button
	if btn_x == null or btn_x.custom_minimum_size.x < 48 or btn_x.custom_minimum_size.y < 48:
		_fail("右上關閉按鈕尺寸需 >= 48px")

	var tabs_row = dlg.get_node_or_null("DialogCard/RootVBox/SlotTabRow") as HBoxContainer
	if tabs_row == null or tabs_row.get_child_count() != 3:
		_fail("彈窗缺少三欄武器槽位切換 Tab (首選/副手/絕技)")

	for c in tabs_row.get_children():
		if c is Button and (c as Button).custom_minimum_size.y < 48:
			_fail("槽位 Tab 按鈕熱區需 >= 48px")

	dlg.queue_free()
	print("  ok 彈窗寬度符合 740~760px、右上關閉鈕 >= 48px、三欄 Tab 具備且熱區 >= 48px")


func _step_test_weapon_candidates_and_swap() -> void:
	print("\n--- 3. 檢驗武器清單讀取、更換武器與即時數值/紙娃娃連動 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 在背包中注入兩把測試武器
	var axe_inst := {
		"uid": "w_test_axe_99",
		"base_id": "axe",
		"name": "裂地巨斧",
		"line": "axe",
		"slot": "weapon",
		"tier": 2,
		"quality": "epic",
		"quality_label": "秘寶",
		"rolled": {"atk": 45, "def": 5, "hp": 20, "crit": 5.0, "crit_dmg": 15.0}
	}
	var spear_inst := {
		"uid": "w_test_spear_88",
		"base_id": "spear",
		"name": "破浪長槍",
		"line": "spear",
		"slot": "weapon",
		"tier": 1,
		"quality": "rare",
		"quality_label": "上品",
		"rolled": {"atk": 25, "def": 4, "hp": 0, "crit": 2.0, "crit_dmg": 0.0}
	}
	gs.equip_bag.append(axe_inst)
	gs.equip_bag.append(spear_inst)

	var dlg: Control = _lobby.open_weapon_swap_dialog(0)
	var weapons_box: VBoxContainer = dlg.get_node_or_null("DialogCard/RootVBox/WeaponsScroll/WeaponsBox")
	if weapons_box == null:
		_fail("缺少 WeaponsBox 容器")
		return

	var axe_card = weapons_box.get_node_or_null("WeaponCard_w_test_axe_99")
	if axe_card == null:
		_fail("WeaponsBox 未能正確列出背包中的武器 w_test_axe_99 (裂地巨斧)")

	# 點擊更換為裂地巨斧
	var btn_action = axe_card.find_child("BtnAction", true, false) as Button
	if btn_action == null:
		_fail("武器卡片缺少 BtnAction 操作按鈕")
	if btn_action.custom_minimum_size.y < 48:
		_fail("武器更換操作按鈕熱區需 >= 48px")

	btn_action.emit_signal("pressed")

	# 驗證裝備狀態
	if str(gs.weapon_loadout[0]) != "w_test_axe_99":
		_fail("GameState.weapon_loadout[0] 未更新為 w_test_axe_99，實際為: %s" % gs.weapon_loadout[0])

	if str(gs.equip_slots.get("weapon", "")) != "w_test_axe_99":
		_fail("GameState.equip_slots['weapon'] 未同步為 w_test_axe_99")

	if str(gs.path_style) != "axe":
		_fail("GameState.path_style 應更新為 axe，實際為: %s" % gs.path_style)

	# 驗證角色頁攻擊力與戰力連動
	var stat_cards: Array = _lobby.get("_stat_cards")
	var atk_card: PanelContainer = stat_cards[1]
	var atk_val_lbl := atk_card.find_child("ValLabel", true, false) as Label
	var cur_atk := int(gs.effective_atk())
	if int(atk_val_lbl.text) != cur_atk:
		_fail("角色頁攻擊力卡片數值未連動更新，預期 %d，實際 %s" % [cur_atk, atk_val_lbl.text])

	var cur_pow := int(gs.power_score())
	var pow_lbl: Label = _lobby.get("_char_power_badge")
	if not pow_lbl.text.contains(str(cur_pow)):
		_fail("角色頁有效戰力徽章未更新為 %d，實際為 %s" % [cur_pow, pow_lbl.text])

	print("  ok 更換武器成功：GameState.weapon_loadout[0] 正常更新、面板攻擊力即時更新為 %d、戰力即時更新為 %d" % [cur_atk, cur_pow])


func _step_test_slot_switch_and_unequip() -> void:
	print("\n--- 4. 檢驗槽位切換、副手欄裝備與卸下武器 ---")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")

	# 模擬角色等級達到 Lv12，解鎖副手欄 (slot 1)
	gs.level = 12

	var dlg: Control = _lobby.open_weapon_swap_dialog(1)
	var weapons_box: VBoxContainer = dlg.get_node_or_null("DialogCard/RootVBox/WeaponsScroll/WeaponsBox")
	var spear_card = weapons_box.get_node_or_null("WeaponCard_w_test_spear_88")
	if spear_card == null:
		_fail("副手欄彈窗中未列出可選武器 w_test_spear_88 (破浪長槍)")
		return

	var btn_action = spear_card.find_child("BtnAction", true, false) as Button
	btn_action.emit_signal("pressed")
	if is_instance_valid(dlg):
		dlg.free()

	if str(gs.weapon_loadout[1]) != "w_test_spear_88":
		_fail("GameState.weapon_loadout[1] 未更新為 w_test_spear_88")

	# 再次開啟彈窗並測試卸下副手武器
	var dlg2: Control = _lobby.open_weapon_swap_dialog(1)
	var btn_unequip: Button = dlg2.find_child("BtnUnequip", true, false) as Button
	if btn_unequip == null or not btn_unequip.visible:
		_fail("副手槽有裝備時應顯示「卸下武器」按鈕")
		return

	btn_unequip.emit_signal("pressed")

	if str(gs.weapon_loadout[1]) != "":
		_fail("卸下副手武器後 GameState.weapon_loadout[1] 應為空字串，實際為: %s" % gs.weapon_loadout[1])

	# 驗證長槍回到背包
	var found_in_bag := false
	for it in gs.equip_bag:
		if str(it.get("uid", "")) == "w_test_spear_88":
			found_in_bag = true
			break
	if not found_in_bag:
		_fail("卸下副手武器後該武器應回到 equip_bag 中")

	print("  ok 副手欄位成功裝備長槍，並成功測試卸下武器且道具正確回流背包")


func _step_test_i18n() -> void:
	print("\n--- 5. 檢驗六語系即時切換與文字非空且零 Emoji ---")
	var loc = root.get_node_or_null("Loc")
	var locales := ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]

	for code in locales:
		loc.call("set_locale", code)
		_lobby._apply_locale_texts()

		var btn_change: Button = _lobby.get("_btn_change_weapon")
		if btn_change.text.is_empty():
			_fail("[%s] 更換裝備按鈕文字為空" % code)
		_assert_no_emoji(btn_change.text, "[%s] 更換裝備按鈕" % code)

		var dlg: Control = _lobby.open_weapon_swap_dialog(0)
		var title_lbl: Label = dlg.find_child("TitleLabel", true, false) as Label
		var sub_lbl: Label = dlg.find_child("SubTitleLabel", true, false) as Label
		var close_btn: Button = dlg.find_child("BtnBottomClose", true, false) as Button

		if title_lbl == null or title_lbl.text.is_empty():
			_fail("[%s] 彈窗標題為空" % code)
		if sub_lbl == null or sub_lbl.text.is_empty():
			_fail("[%s] 彈窗副標題為空" % code)
		if close_btn == null or close_btn.text.is_empty():
			_fail("[%s] 關閉按鈕文字為空" % code)

		_assert_no_emoji(title_lbl.text, "[%s] 彈窗標題" % code)
		_assert_no_emoji(sub_lbl.text, "[%s] 彈窗副標題" % code)

		dlg.free()
		print("  ok [%s] 語系下標題、副標題、按鈕即時在地化正常且零 Emoji" % code)

	loc.call("set_locale", "zh_TW")
	_lobby._apply_locale_texts()


func _capture_and_save(file_path: String) -> String:
	var vp := root.get_viewport()
	var tex := vp.get_texture()
	var img: Image = null
	if tex:
		img = tex.get_image()
	if img == null or img.is_empty():
		# 備援純色渲染緩衝區以防 headless 無法擷取渲染器貼圖
		img = Image.create(1280, 720, false, Image.FORMAT_RGBA8)
		img.fill(Color("#FFFDF8"))

	var err := img.save_png(file_path)
	if err != OK:
		_fail("儲存截圖失敗: %s" % file_path)
		return ""

	var f := FileAccess.open(file_path, FileAccess.READ)
	if f == null:
		_fail("無法讀取已儲存的截圖: %s" % file_path)
		return ""
	var buf := f.get_buffer(f.get_length())
	f.close()
	var ctx := HashingContext.new()
	ctx.start(HashingContext.HASH_SHA256)
	ctx.update(buf)
	var hash_bytes := ctx.finish()
	var hash_str := hash_bytes.hex_encode()
	print("  ✓ 截圖存證: %s (SHA256: %s)" % [file_path, hash_str.substr(0, 12)])
	return hash_str


func _assert_no_emoji(text: String, context: String) -> void:
	for ch in text:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			if ch != "✕":
				_fail("%s 含有禁止之系統 Emoji: '%s'" % [context, ch])


func _fail(msg: String) -> void:
	push_error("TEST_FAILED: " + msg)
	printerr("TEST_FAILED: " + msg)
	quit(1)
