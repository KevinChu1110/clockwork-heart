extends SceneTree
## 單元與驗收測試：EquipmentSystem 與 WeaponSwapDialog 裝備鎖定保護機制 (t_3195d5e4)
## 驗證：
## 1. EquipmentSystem is_equip_locked 與 set_equip_locked API，並持久化至 equip_worn / equip_bag。
## 2. 鐵匠鋪分解（dismantle / dismantle_weapon）自動攔截已鎖定裝備，回傳明確提示。
## 3. WeaponSwapDialog 武器卡片上新增「鎖定/已鎖」多巴胺厚底小按鈕（熱區 >= 48px），即時切換狀態與音效連動。
## 4. 零系統 Emoji、多巴胺亮色盤規範、粉圓體與六語系在地化支援。
## 5. 實機截圖存證（若非無頭環境）。

const WeaponSwapDialogScript = preload("res://scripts/ui/weapon_swap_dialog.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _frame_count: int = 0
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _dialog: WeaponSwapDialogScript = null
var _h1: String = ""
var _h2: String = ""
var _h3: String = ""
var _test_uid1: String = ""
var _test_uid2: String = ""


func _initialize() -> void:
	print("== 開始執行 EquipmentSystem 與 WeaponSwapDialog 裝備鎖定保護驗收測試 (t_3195d5e4) ==")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	_out_dir = ProjectSettings.globalize_path("res://proofs/t_3195d5e4")
	DirAccess.make_dir_recursive_absolute(_out_dir)
	var top_proofs := ProjectSettings.globalize_path("res://../proofs/t_3195d5e4")
	DirAccess.make_dir_recursive_absolute(top_proofs)

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var inv = root.get_node_or_null("InventorySystem")
	var dt = root.get_node_or_null("DataTables")
	var loc = root.get_node_or_null("Loc")

	if gs == null or eq == null or inv == null:
		_fail("缺少必要 Autoload 節點 (GameState / EquipmentSystem / InventorySystem)")
		return

	if dt and dt.has_method("reload"):
		dt.call("reload")
	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")

	gs.reset_new_game("rabbit")
	_step = 0


func _process(_delta: float) -> bool:
	_frame_count += 1
	if _frame_count < 2:
		return false

	match _step:
		0:
			_test_equipment_system_lock_api()
			_step = 1
		1:
			_test_blacksmith_dismantle_interception()
			_step = 2
		2:
			_test_weapon_swap_dialog_ui()
			_step = 3
		3:
			_test_i18n_locales_and_no_emoji()
			_step = 4
		4:
			if DisplayServer.get_name() != "headless":
				print("\n--- 5. 擷取實機截圖存證並驗證 SHA256 不重複 ---")
				_wait = 0
				_step = 5
			else:
				print("\n--- 5. 無頭模式 (headless)，略過 Viewport 截圖與雜湊比對 ---")
				_step = 9
		5:
			_wait += 1
			if _wait < 6:
				return false
			_setup_dialog_for_proof(0)
			_wait = 0
			_step = 6
		6:
			_wait += 1
			if _wait < 10:
				return false
			var p1 := _out_dir.path_join("proof_01_weapon_swap_lock_btn_unlocked.png")
			_h1 = _capture_and_save(p1)

			# 切換鎖定狀態進行第二張截圖
			if is_instance_valid(_dialog):
				var card := _dialog.find_child("WeaponCard_" + _test_uid1, true, false)
				if card:
					var lbtn: Button = card.find_child("BtnLock", true, false) as Button
					if lbtn:
						lbtn.emit_signal("pressed")
			_wait = 0
			_step = 7
		7:
			_wait += 1
			if _wait < 10:
				return false
			var p2 := _out_dir.path_join("proof_02_weapon_swap_lock_btn_locked.png")
			_h2 = _capture_and_save(p2)

			# 切換至英文語系進行第三張截圖
			var loc = root.get_node_or_null("Loc")
			if loc and loc.has_method("set_locale"):
				loc.call("set_locale", "en")
			_wait = 0
			_step = 8
		8:
			_wait += 1
			if _wait < 10:
				return false
			var p3 := _out_dir.path_join("proof_03_weapon_swap_lock_i18n_en.png")
			_h3 = _capture_and_save(p3)

			if _h1 == _h2 or _h2 == _h3 or _h1 == _h3:
				_fail("截圖 SHA256 重複！不可上傳相同截圖冒充流程: h1=%s, h2=%s, h3=%s" % [_h1, _h2, _h3])
				return false
			print("  ok 成功產出 3 張實機截圖存證且 SHA256 皆獨立不重複")
			_step = 9
		9:
			if is_instance_valid(_dialog):
				_dialog.queue_free()
				_dialog = null
			print("\n=======================================================")
			print("  TEST_EQUIPMENT_LOCK_PROTECTION_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


## 1. 測試 EquipmentSystem 鎖定狀態管理與持久化
func _test_equipment_system_lock_api() -> void:
	print("\n--- 1. 檢驗 EquipmentSystem 鎖定狀態管理與持久化 ---")
	var eq = root.get_node_or_null("EquipmentSystem")
	var gs = root.get_node_or_null("GameState")

	# 空 uid 測試
	_assert(not eq.is_equip_locked(""), "空 uid 查詢應回傳 false")
	_assert(not eq.set_equip_locked("", true), "空 uid 設定應回傳 false")

	# 生成測試裝備 1（背包裝備）
	var w1: Dictionary = eq.roll_instance("knight_saber", "epic")
	var uid1: String = str(w1.get("uid", ""))
	_test_uid1 = uid1
	_assert(not uid1.is_empty(), "裝備 1 生成應具備合法 uid")
	_assert(not eq.is_equip_locked(uid1), "新生成裝備預設鎖定狀態應為 false")
	eq.add_to_bag(w1)

	# 驗證背包裝備鎖定與解鎖
	var ok1: bool = bool(eq.set_equip_locked(uid1, true))
	_assert(ok1, "設定背包裝備為鎖定應成功")
	_assert(eq.is_equip_locked(uid1), "查詢已鎖定背包裝備應為 true")

	var ok2: bool = bool(eq.set_equip_locked(uid1, false))
	_assert(ok2, "解除背包裝備鎖定應成功")
	_assert(not eq.is_equip_locked(uid1), "解除鎖定後應為 false")

	# 驗證裝備中（equip_worn）狀態下鎖定
	eq.set_equip_locked(uid1, true)
	eq.equip_weapon_to_loadout(uid1, 0)
	_assert(gs.equip_worn.has(uid1), "裝備 1 應已穿上至 equip_worn")
	_assert(eq.is_equip_locked(uid1), "穿上後在 equip_worn 中依然保持鎖定狀態")

	eq.set_equip_locked(uid1, false)
	_assert(not eq.is_equip_locked(uid1), "在 equip_worn 中解鎖應為 false")

	eq.set_equip_locked(uid1, true)
	_assert(eq.is_equip_locked(uid1), "在 equip_worn 中重新鎖定應為 true")

	# 驗證序列化持久化 (to_dict / from_dict)
	var state_dict: Dictionary = gs.to_dict()
	gs.reset_new_game("rabbit")
	_assert(not eq.is_equip_locked(uid1), "重置新遊戲後舊 uid 不應存在")

	gs.from_dict(state_dict)
	_assert(eq.is_equip_locked(uid1), "從存檔還原後裝備鎖定狀態必須保持為 true")

	print("  ok EquipmentSystem is_equip_locked / set_equip_locked 與持久化驗證通過")


## 2. 測試鐵匠鋪防分解攔截機制 (dismantle / dismantle_weapon)
func _test_blacksmith_dismantle_interception() -> void:
	print("\n--- 2. 檢驗鐵匠鋪防分解攔截機制 (dismantle / dismantle_weapon) ---")
	var eq = root.get_node_or_null("EquipmentSystem")
	var gs = root.get_node_or_null("GameState")
	var inv = root.get_node_or_null("InventorySystem")
	var forge = root.get_node_or_null("ForgeSystem")

	gs.equip_bag = []
	var prev_scrap: int = inv.count("iron_scrap")
	var prev_gold: int = gs.gold

	# 產生珍貴神兵（T2 上品長槍）
	var w: Dictionary = eq.roll_instance("ash_spear", "rare")
	var uid: String = str(w.get("uid", ""))
	eq.add_to_bag(w)

	# 鎖定該神兵
	eq.set_equip_locked(uid, true)
	_assert(eq.is_equip_locked(uid), "神兵應處於鎖定狀態")

	# 1. 呼叫 EquipmentSystem.dismantle(uid) 應被阻擋
	var r1: Dictionary = eq.dismantle(uid)
	_assert(not bool(r1.get("ok", true)), "已鎖定裝備呼叫 dismantle 必須失敗")
	var msg1: String = str(r1.get("msg", ""))
	_assert(msg1.find("裝備已鎖定，無法分解") >= 0, "回傳訊息應明確提示【裝備已鎖定，無法分解】，實際: %s" % msg1)
	_assert(not eq.find_bag(uid).is_empty(), "被阻擋後裝備仍應保留於背包")
	_assert(inv.count("iron_scrap") == prev_scrap, "鐵屑數量不可增加")
	_assert(gs.gold == prev_gold, "金幣數量不可增加")

	# 2. 呼叫 EquipmentSystem.dismantle_weapon(uid) 應被阻擋
	var r2: Dictionary = eq.dismantle_weapon(uid)
	_assert(not bool(r2.get("ok", true)), "已鎖定裝備呼叫 dismantle_weapon 必須失敗")
	var msg2: String = str(r2.get("msg", ""))
	_assert(msg2.find("裝備已鎖定，無法分解") >= 0, "dismantle_weapon 回傳訊息提示正確")

	# 3. 呼叫 ForgeSystem.dismantle_weapon(uid) 應被阻擋
	if forge and forge.has_method("dismantle_weapon"):
		var r3: Dictionary = forge.dismantle_weapon(uid)
		_assert(not bool(r3.get("ok", true)), "ForgeSystem.dismantle_weapon 已鎖定裝備必須失敗")
		var msg3: String = str(r3.get("msg", ""))
		_assert(msg3.find("裝備已鎖定，無法分解") >= 0, "ForgeSystem 回傳訊息提示正確")

	# 解鎖後正常分解驗證
	eq.set_equip_locked(uid, false)
	_assert(not eq.is_equip_locked(uid), "解除鎖定應成功")

	var r_succ: Dictionary = eq.dismantle(uid)
	_assert(bool(r_succ.get("ok", false)), "解鎖後分解必須成功: %s" % r_succ)
	_assert(eq.find_bag(uid).is_empty(), "成功分解後裝備應已自背包移除")
	_assert(inv.count("iron_scrap") > prev_scrap, "成功分解後鐵屑應增加")
	_assert(gs.gold > prev_gold, "成功分解後金幣應增加")

	print("  ok 鐵匠鋪防誤拆安全攔截機制與解鎖分解驗證通過")


## 3. 測試 WeaponSwapDialog 卡片鎖定按鈕與 UI 連動
func _test_weapon_swap_dialog_ui() -> void:
	print("\n--- 3. 檢驗 WeaponSwapDialog 武器卡片鎖定按鈕、熱區與 UI 連動 ---")
	var eq = root.get_node_or_null("EquipmentSystem")
	var gs = root.get_node_or_null("GameState")

	# 準備 2 件測試武器：1 件未鎖、1 件已鎖
	var w1: Dictionary = eq.roll_instance("rusty_blade", "common")
	_test_uid1 = str(w1.get("uid", ""))
	eq.add_to_bag(w1)
	eq.set_equip_locked(_test_uid1, false)

	var w2: Dictionary = eq.roll_instance("notch_axe", "epic")
	_test_uid2 = str(w2.get("uid", ""))
	eq.add_to_bag(w2)
	eq.set_equip_locked(_test_uid2, true)

	var dlg = WeaponSwapDialogScript.new(0)
	root.add_child(dlg)
	dlg.setup(0)

	var card1 := dlg.find_child("WeaponCard_" + _test_uid1, true, false)
	_assert(card1 != null, "應找到測試裝備 1 之卡片")
	var lock_btn1: Button = card1.find_child("BtnLock", true, false) as Button
	_assert(lock_btn1 != null, "卡片 1 應包含 BtnLock 按鈕")
	_assert(lock_btn1.custom_minimum_size.x >= 48 and lock_btn1.custom_minimum_size.y >= 48, "BtnLock 熱區尺寸必須 >= 48px，實際為: %s" % str(lock_btn1.custom_minimum_size))
	_assert(lock_btn1.text == "鎖定", "未鎖定裝備按鈕文字應為【鎖定】，實際為: %s" % lock_btn1.text)

	var card2 := dlg.find_child("WeaponCard_" + _test_uid2, true, false)
	_assert(card2 != null, "應找到測試裝備 2 之卡片")
	var lock_btn2: Button = card2.find_child("BtnLock", true, false) as Button
	_assert(lock_btn2 != null, "卡片 2 應包含 BtnLock 按鈕")
	_assert(lock_btn2.text == "已鎖", "已鎖定裝備按鈕文字應為【已鎖】，實際為: %s" % lock_btn2.text)

	# 測試點擊按鈕 1（未鎖 -> 鎖定）
	var sig_data := {"received": false, "uid": "", "locked": false}
	dlg.weapon_lock_changed.connect(func(u: String, l: bool):
		sig_data["received"] = true
		sig_data["uid"] = u
		sig_data["locked"] = l
	)

	lock_btn1.pressed.emit()
	_assert(bool(sig_data["received"]), "點擊 BtnLock 應發出 weapon_lock_changed 信號")
	_assert(str(sig_data["uid"]) == _test_uid1, "信號之 uid 應與點擊武器相符")
	_assert(bool(sig_data["locked"]) == true, "切換後鎖定狀態應為 true")
	_assert(eq.is_equip_locked(_test_uid1), "EquipmentSystem 中狀態應同步為 true")
	_assert(lock_btn1.text == "已鎖", "點擊後按鈕文字應即時更新為【已鎖】，實際為: %s" % lock_btn1.text)

	# 再次點擊按鈕 1（鎖定 -> 解鎖）
	sig_data["received"] = false
	lock_btn1.pressed.emit()
	_assert(bool(sig_data["received"]), "再次點擊應發出 weapon_lock_changed 信號")
	_assert(bool(sig_data["locked"]) == false, "切換後鎖定狀態應為 false")
	_assert(not eq.is_equip_locked(_test_uid1), "EquipmentSystem 中狀態應同步為 false")
	_assert(lock_btn1.text == "鎖定", "按鈕文字應即時更新為【鎖定】，實際為: %s" % lock_btn1.text)

	dlg.queue_free()
	print("  ok WeaponSwapDialog 卡片鎖定按鈕樣式、尺寸與點擊即時連動驗證通過")


## 4. 測試六語系在地化即時切換與零系統 Emoji 規範
func _test_i18n_locales_and_no_emoji() -> void:
	print("\n--- 4. 檢驗六語系即時切換與零系統 Emoji 規範 ---")
	var loc = root.get_node_or_null("Loc")
	var expected_lock: Dictionary = {
		"zh_TW": "鎖定",
		"zh_CN": "锁定",
		"en": "Lock",
		"ja": "ロック",
		"ko": "잠금",
		"es": "Bloquear"
	}
	var expected_locked: Dictionary = {
		"zh_TW": "已鎖",
		"zh_CN": "已锁",
		"en": "Locked",
		"ja": "ロック中",
		"ko": "잠김",
		"es": "Bloqueado"
	}
	var expected_dismantle_refusal: Dictionary = {
		"zh_TW": "裝備已鎖定，無法分解。",
		"zh_CN": "装备已锁定，无法分解。",
		"en": "Equipment is locked and cannot be dismantled.",
		"ja": "装備がロックされているため分解できません。",
		"ko": "장비가 잠겨 있어 분해할 수 없습니다.",
		"es": "El equipo está bloqueado y no se puede desmantelar."
	}

	for lang in ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]:
		if loc and loc.has_method("set_locale"):
			loc.call("set_locale", lang)

		var t_lock := ContentLoc.text("ui", "鎖定")
		var t_locked := ContentLoc.text("ui", "已鎖")
		var t_refuse := ContentLoc.text("ui", "裝備已鎖定，無法分解。")

		_assert(t_lock == expected_lock[lang], "[%s] '鎖定' 譯文不符，預期 '%s' 實得 '%s'" % [lang, expected_lock[lang], t_lock])
		_assert(t_locked == expected_locked[lang], "[%s] '已鎖' 譯文不符，預期 '%s' 實得 '%s'" % [lang, expected_locked[lang], t_locked])
		_assert(t_refuse == expected_dismantle_refusal[lang], "[%s] '裝備已鎖定，無法分解。' 譯文不符，預期 '%s' 實得 '%s'" % [lang, expected_dismantle_refusal[lang], t_refuse])

		_assert_no_emoji(t_lock, "%s_lock" % lang)
		_assert_no_emoji(t_locked, "%s_locked" % lang)
		_assert_no_emoji(t_refuse, "%s_refuse" % lang)

		print("  ok [%s] 語系在地化: lock=\"%s\", locked=\"%s\" 且零 Emoji" % [lang, t_lock, t_locked])

	if loc and loc.has_method("set_locale"):
		loc.call("set_locale", "zh_TW")


func _setup_dialog_for_proof(slot: int) -> void:
	if is_instance_valid(_dialog):
		_dialog.queue_free()
		_dialog = null

	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	gs.reset_new_game("rabbit")
	gs.equip_bag = [
		{
			"uid": "w_bag_mythic",
			"slot": "weapon",
			"name": "天樞星宿寶劍",
			"line": "sword",
			"quality": "epic",
			"quality_label": "秘寶",
			"weapon_atk": 85,
			"locked": false,
			"rolled": {"def": 25, "hp": 60, "crit_dmg": 24.5}
		},
		{
			"uid": "w_bag_locked",
			"slot": "weapon",
			"name": "玄鐵破陣長槍",
			"line": "spear",
			"quality": "rare",
			"quality_label": "上品",
			"weapon_atk": 68,
			"locked": true,
			"rolled": {"def": 12, "hp": 30, "crit_dmg": 10.0}
		}
	]
	_test_uid1 = "w_bag_mythic"
	_test_uid2 = "w_bag_locked"

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
	var top_path := ProjectSettings.globalize_path("res://../proofs/t_3195d5e4").path_join(path.get_file())
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
	push_error("TEST_EQUIPMENT_LOCK_PROTECTION_FAIL: " + msg)
	print("❌ TEST_EQUIPMENT_LOCK_PROTECTION_FAIL: ", msg)
	quit(1)
