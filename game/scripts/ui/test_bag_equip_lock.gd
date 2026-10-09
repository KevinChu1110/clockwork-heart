extends SceneTree
## 單元與驗收測試：背包Tab物品詳情支援武器裝備鎖定狀態顯示與快捷切換 (t_cf49329c)
## 覆蓋：
## 1. 背包點選武器裝備時顯示鎖定狀態標籤膠囊（金色/深藍紫）與鎖定/解鎖按鈕。
## 2. 點擊按鈕即時呼叫 EquipmentSystem.set_equip_locked(uid, new_locked) 切換狀態並連動持久化至 GameState。
## 3. 裝備鎖定時下方的使用/賣出按鈕自動禁用或點擊時提示裝備已鎖定無法出售，防止玩家誤操作。
## 4. 遵守多巴胺亮色盤、粉圓體、零系統 Emoji、支援六語系即時切換。
## 5. 實機截圖存證（1280x720 PNG）。

const MobileLobbyScript := preload("res://scripts/ui/mobile_lobby.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _lobby: Control = null
var _gs: Node = null
var _eq: Node = null
var _inv: Node = null
var _loc: Node = null
var _out_dir: String = ""
var _test_uid1: String = "w_test_sword"
var _test_uid2: String = "w_test_spear"
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""


func _initialize() -> void:
	print("== 開始執行 背包Tab武器裝備鎖定狀態顯示與快捷切換 驗收測試 (t_cf49329c) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_cf49329c")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var top_proofs := ProjectSettings.globalize_path("res://../proofs/t_cf49329c")
	DirAccess.make_dir_recursive_absolute(top_proofs)

	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_inv = root.get_node_or_null("InventorySystem")
	_loc = root.get_node_or_null("Loc")
	var dt = root.get_node_or_null("DataTables")

	if _gs == null or _eq == null or _inv == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / InventorySystem)")
		return

	if dt and dt.has_method("reload"):
		dt.call("reload")
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	_gs.reset_new_game("rabbit")
	_step = 0


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	match _step:
		0:
			_setup_test_environment()
			_step = 1
		1:
			_test_bag_equip_unlocked_state()
			_step = 2
		2:
			_test_bag_equip_toggle_lock()
			_step = 3
		3:
			_test_bag_equip_lock_misuse_prevention()
			_step = 4
		4:
			_test_bag_equip_unlock()
			_step = 5
		5:
			_test_bag_regular_item_selection()
			_step = 6
		6:
			_test_bag_equip_lock_i18n()
			_step = 7
		7:
			if DisplayServer.get_name() != "headless":
				print("\n--- 7. 擷取實機截圖存證 (1280x720) ---")
				_wait = 0
				_step = 8
			else:
				print("\n--- 7. 無頭模式 (headless)，略過實體 Viewport 截圖比對 ---")
				_step = 12
		8:
			_wait += 1
			if _wait < 6:
				return false
			_setup_lobby_for_proof_unlocked()
			_wait = 0
			_step = 9
		9:
			_wait += 1
			if _wait < 6:
				return false
			var p1 := _out_dir.path_join("proof_01_bag_equip_unlocked.png")
			_h1 = _capture_and_save(p1)
			# 切換鎖定狀態進行第二張截圖
			var lock_btn: Button = _lobby.get_bag_lock_button()
			if lock_btn:
				lock_btn.emit_signal("pressed")
			_wait = 0
			_step = 10
		10:
			_wait += 1
			if _wait < 6:
				return false
			var p2 := _out_dir.path_join("proof_02_bag_equip_locked.png")
			_h2 = _capture_and_save(p2)
			# 切換至英文語系進行第三張截圖
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "en")
			_lobby.call("_show_toast", ContentLoc.text("ui", "已鎖定裝備"))
			_wait = 0
			_step = 11
		11:
			_wait += 1
			if _wait < 6:
				return false
			var p3 := _out_dir.path_join("proof_03_bag_equip_lock_i18n_en.png")
			_h3 = _capture_and_save(p3)
			if _loc and _loc.has_method("set_locale"):
				_loc.call("set_locale", "zh_TW")

			_assert(_h1 != _h2, "截圖 1 與截圖 2 (未鎖定 vs 已鎖定) SHA256 不得相同")
			_assert(_h2 != _h3, "截圖 2 與截圖 3 (中文 vs 英文) SHA256 不得相同")
			print("  ✓ 實機 3 張存證截圖 SHA256 驗證全數獨立不重複")
			_step = 12
		12:
			print("\n=======================================================")
			print("🎉 全部背包裝備鎖定狀態顯示與快捷切換驗證項通過！")
			print("TEST_BAG_EQUIP_LOCK_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _setup_test_environment() -> void:
	print("\n--- 1. 設定測試環境與背包物品清單 ---")
	if is_instance_valid(_lobby):
		_lobby.queue_free()
		_lobby = null

	_gs.equip_bag = [
		{
			"uid": _test_uid1,
			"base_id": "rusty_blade",
			"slot": "weapon",
			"name": "",
			"line": "sword",
			"quality": "epic",
			"quality_label": "秘寶",
			"tier": 2,
			"locked": false,
			"rolled": {"atk": 75, "def": 20, "hp": 50, "crit": 8.0}
		},
		{
			"uid": _test_uid2,
			"base_id": "ash_spear",
			"slot": "weapon",
			"name": "",
			"line": "spear",
			"quality": "rare",
			"quality_label": "上品",
			"tier": 2,
			"locked": true,
			"rolled": {"atk": 65, "def": 15, "hp": 30, "crit": 5.0}
		}
	]

	_inv.call("grant_starter")

	_lobby = MobileLobbyScript.new()
	root.add_child(_lobby)

	# 切換至 Tab.BAG
	_lobby.call("_switch_tab", MobileLobbyScript.Tab.BAG)
	_lobby.call("_refresh_bag_tab")
	print("  ✓ 大廳背包分頁建立完成，已配置未鎖定與已鎖定武器")


func _test_bag_equip_unlocked_state() -> void:
	print("\n--- 2. 測試選中未鎖定裝備時之膠囊標籤與按鈕樣式 ---")
	_lobby.set("_selected_bag_item", _test_uid1)
	_lobby.call("_update_bag_detail", _inv)

	var capsule: PanelContainer = _lobby.get_bag_lock_capsule()
	var lbl: Label = _lobby.get_bag_lock_label()
	var lock_btn: Button = _lobby.get_bag_lock_button()
	var use_btn: Button = _lobby.get("_bag_use_btn")

	_assert(capsule != null and capsule.visible, "選中武器時 LockCapsule 應為可見")
	_assert(lbl != null and lbl.text == "未鎖定", "未鎖定武器標籤文字應為『未鎖定』，實得: " + (lbl.text if lbl else ""))
	_assert(lock_btn != null and lock_btn.visible, "選中武器時 LockBtn 應為可見")
	_assert(lock_btn.text == "鎖定", "未鎖定武器切換按鈕文字應為『鎖定』，實得: " + lock_btn.text)
	_assert(lock_btn.custom_minimum_size.y >= 48.0, "LockBtn 觸控熱區高度應 >= 48px，實得: %.1f" % lock_btn.custom_minimum_size.y)
	_assert(use_btn != null and not use_btn.disabled, "未鎖定裝備時使用/賣出按鈕應為可用 (not disabled)")

	# 驗證膠囊文字尺寸 >= 14px 零 PPT 小字
	var fsz: int = lbl.get_theme_font_size("font_size")
	_assert(fsz >= 14, "膠囊標籤字級應 >= 14px，實得: %d" % fsz)

	print("  ✓ 未鎖定裝備：深藍紫膠囊『未鎖定』、多巴胺厚底鈕『鎖定』、使用按鈕可用")


func _test_bag_equip_toggle_lock() -> void:
	print("\n--- 3. 測試點擊鎖定按鈕切換為已鎖定狀態與持久化 ---")
	var lock_btn: Button = _lobby.get_bag_lock_button()
	_assert(lock_btn != null, "找不到 LockBtn")

	# 模擬點擊
	_lobby.call("_on_bag_lock_pressed")

	_assert(_eq.call("is_equip_locked", _test_uid1) == true, "點擊後 EquipmentSystem.is_equip_locked 應回傳 true")

	# 驗證 GameState 持久化
	var found_in_bag := false
	for e in _gs.equip_bag:
		if str(e.get("uid", "")) == _test_uid1:
			_assert(bool(e.get("locked", false)) == true, "GameState.equip_bag 內資料 locked 屬性應同步為 true")
			found_in_bag = true
			break
	_assert(found_in_bag, "在 GameState.equip_bag 找不到測試裝備")

	var lbl: Label = _lobby.get_bag_lock_label()
	var use_btn: Button = _lobby.get("_bag_use_btn")
	_assert(lbl.text == "已鎖定", "鎖定後膠囊文字應為『已鎖定』，實得: " + lbl.text)
	_assert(lock_btn.text == "解鎖", "鎖定後按鈕文字應為『解鎖』，實得: " + lock_btn.text)
	_assert(use_btn.disabled == true, "鎖定狀態下使用/賣出按鈕應自動禁用 (disabled == true)")
	_assert(use_btn.text.contains("已鎖定") or use_btn.text.contains("無法出售"), "禁用按鈕文字應提示無法出售，實得: " + use_btn.text)

	print("  ✓ 鎖定成功：持久化至 GameState、金色膠囊『已鎖定』、按鈕『解鎖』、使用按鈕自動禁用")


func _test_bag_equip_lock_misuse_prevention() -> void:
	print("\n--- 4. 測試防誤操作攔截（使用/賣出/分解全面防呆阻擋） ---")
	# 4.1 點擊背包使用/賣出按鈕防呆
	_lobby.call("_on_bag_use_pressed")
	_assert(_eq.call("is_equip_locked", _test_uid1) == true, "誤操作後裝備仍應保持鎖定狀態")

	# 4.2 鐵匠鋪分解 (dismantle) 防呆攔截
	var res_dis: Dictionary = _eq.call("dismantle", _test_uid1)
	_assert(bool(res_dis.get("ok", true)) == false, "已鎖定裝備呼叫 dismantle 應失敗 (ok == false)")
	var dis_msg: String = str(res_dis.get("msg", ""))
	_assert(dis_msg.contains("已鎖定") and dis_msg.contains("無法分解"), "分解提示訊息應說明裝備已鎖定無法分解，實得: " + dis_msg)

	print("  ✓ 防誤賣防誤拆攔截成功：背包與系統層面皆具備防呆機制")


func _test_bag_equip_unlock() -> void:
	print("\n--- 5. 測試點擊解鎖按鈕恢復未鎖定狀態 ---")
	_lobby.call("_on_bag_lock_pressed")

	_assert(_eq.call("is_equip_locked", _test_uid1) == false, "解鎖後 is_equip_locked 應回傳 false")
	var lbl: Label = _lobby.get_bag_lock_label()
	var lock_btn: Button = _lobby.get_bag_lock_button()
	var use_btn: Button = _lobby.get("_bag_use_btn")

	_assert(lbl.text == "未鎖定", "解鎖後膠囊文字應恢復為『未鎖定』")
	_assert(lock_btn.text == "鎖定", "解鎖後按鈕文字應恢復為『鎖定』")
	_assert(use_btn.disabled == false, "解鎖後使用/賣出按鈕應恢復可用")

	print("  ✓ 解鎖成功：膠囊與按鈕狀態正確恢復")


func _test_bag_regular_item_selection() -> void:
	print("\n--- 6. 測試選中一般消耗品/道具時隱藏鎖定膠囊與按鈕 ---")
	# 選取初始給予之 hp_s
	_lobby.set("_selected_bag_item", "hp_s")
	_lobby.call("_update_bag_detail", _inv)

	var capsule: PanelContainer = _lobby.get_bag_lock_capsule()
	var lock_btn: Button = _lobby.get_bag_lock_button()

	_assert(capsule.visible == false, "選中一般道具時 LockCapsule 應隱藏 (visible == false)")
	_assert(lock_btn.visible == false, "選中一般道具時 LockBtn 應隱藏 (visible == false)")

	print("  ✓ 一般消耗品/道具正常隱藏鎖定相關 UI")


func _test_bag_equip_lock_i18n() -> void:
	print("\n--- 6. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時在地化切換 ---")
	var expected_lock := {
		"zh_TW": "鎖定", "zh_CN": "锁定", "en": "Lock",
		"ja": "ロック", "ko": "잠금", "es": "Bloquear"
	}
	var expected_unlock := {
		"zh_TW": "解鎖", "zh_CN": "解锁", "en": "Unlock",
		"ja": "ロック解除", "ko": "잠금 해제", "es": "Desbloquear"
	}
	var expected_locked_capsule := {
		"zh_TW": "已鎖定", "zh_CN": "已锁定", "en": "Locked",
		"ja": "ロック中", "ko": "잠김", "es": "Bloqueado"
	}
	var expected_unlocked_capsule := {
		"zh_TW": "未鎖定", "zh_CN": "未锁定", "en": "Unlocked",
		"ja": "未ロック", "ko": "미잠금", "es": "Desbloqueado"
	}

	for lang in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
		if _loc and _loc.has_method("set_locale"):
			_loc.call("set_locale", lang)

		# 測試未鎖定武器顯示
		_lobby.set("_selected_bag_item", _test_uid1)
		_lobby.call("_update_bag_detail", _inv)

		var lbl: Label = _lobby.get_bag_lock_label()
		var lock_btn: Button = _lobby.get_bag_lock_button()

		_assert(lbl.text == expected_unlocked_capsule[lang], "[%s] 未鎖定膠囊文字翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_unlocked_capsule[lang], lbl.text])
		_assert(lock_btn.text == expected_lock[lang], "[%s] 鎖定按鈕文字翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_lock[lang], lock_btn.text])

		_assert_no_emoji(lbl.text, "%s_unlocked_lbl" % lang)
		_assert_no_emoji(lock_btn.text, "%s_lock_btn" % lang)

		# 測試已鎖定武器顯示
		_lobby.set("_selected_bag_item", _test_uid2)
		_lobby.call("_update_bag_detail", _inv)

		_assert(lbl.text == expected_locked_capsule[lang], "[%s] 已鎖定膠囊文字翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_locked_capsule[lang], lbl.text])
		_assert(lock_btn.text == expected_unlock[lang], "[%s] 解鎖按鈕文字翻譯不符: 預期 '%s', 實得 '%s'" % [lang, expected_unlock[lang], lock_btn.text])

		_assert_no_emoji(lbl.text, "%s_locked_lbl" % lang)
		_assert_no_emoji(lock_btn.text, "%s_unlock_btn" % lang)

		print("  ✓ [%s] 語系在地化比對成功，零系統 Emoji" % lang)

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")


func _setup_lobby_for_proof_unlocked() -> void:
	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")
	_lobby.set("_selected_bag_item", _test_uid1)
	_lobby.call("_update_bag_detail", _inv)


func _capture_and_save(path: String) -> String:
	var vp := root.get_viewport()
	if vp == null:
		_fail("Viewport 不存在，無法擷取畫面")
		return ""
	var tex := vp.get_texture()
	if tex == null:
		_fail("Viewport Texture 不存在")
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		_fail("Viewport 紋理為空，無法儲存截圖")
		return ""
	var err := img.save_png(path)
	if err != OK:
		_fail("儲存截圖失敗: %s, err=%d" % [path, err])
		return ""
	var top_path := ProjectSettings.globalize_path("res://../proofs/t_cf49329c").path_join(path.get_file())
	img.save_png(top_path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		_fail("無法讀取已儲存之截圖: %s" % path)
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證已儲存: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)


func _assert_no_emoji(s: String, context: String) -> void:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			_fail("違規包含系統 Emoji: context=%s, char=%s, code=0x%X" % [context, c, code])


func _fail(msg: String) -> void:
	push_error("TEST_BAG_EQUIP_LOCK_FAIL: " + msg)
	print("❌ TEST_BAG_EQUIP_LOCK_FAIL: ", msg)
	quit(1)
