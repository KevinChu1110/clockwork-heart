extends SceneTree
## 無頭測試：鐵匠鍛造頁一鍵分解多餘裝備與確認彈窗測試
## 執行指令：godot --path game --headless -s res://scripts/ui/test_forge_batch_dismantle.gd

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  ✓ ", msg)


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF):
			return true
	return false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_FORGE_BATCH_DISMANTLE_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_BATCH_DISMANTLE_FAIL")
					print("TEST_FORGE_BATCH_DISMANTLE_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_forge_batch_dismantle 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	var gs = root_node.get_node_or_null("GameState")
	var eq = root_node.get_node_or_null("EquipmentSystem")
	var inv = root_node.get_node_or_null("InventorySystem")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	if gs == null or eq == null or inv == null:
		_fail("缺少必要的 Autoload 節點")
		return

	gs.call("reset_new_game")
	gs.equip_bag = []
	gs.gold = 500

	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法載入 forge_dialog.gd")
		return

	var dlg = ForgeDialogScn.new()
	root_node.add_child(dlg)

	# 1. 驗證 BtnBatchDismantle 按鈕存在與人體工學尺寸
	var btn_dismantle: Button = dlg.find_child("BtnBatchDismantle", true, false) as Button
	_assert(btn_dismantle != null, "ForgeDialog 必須存在 BtnBatchDismantle 按鈕")
	if btn_dismantle:
		_assert(btn_dismantle.custom_minimum_size.x >= 120 and btn_dismantle.custom_minimum_size.y >= 48,
			"BtnBatchDismantle 尺寸符合熱區規範 >= 48px: %s" % str(btn_dismantle.custom_minimum_size))
		_assert(not _has_emoji(btn_dismantle.text), "BtnBatchDismantle 文字嚴禁 Emoji: %s" % btn_dismantle.text)
		_assert(btn_dismantle.text == "一鍵分解", "初始繁中文案應為『一鍵分解』: %s" % btn_dismantle.text)

	# 2. 背包為空時點擊一鍵分解按鈕：不開彈窗、顯示提示訊息
	btn_dismantle.pressed.emit()
	var msg_lbl: Label = dlg.find_child("MsgLabel", true, false) as Label
	_assert(msg_lbl != null and msg_lbl.text.contains("背包沒有多餘未裝備的低階裝備"),
		"背包無多餘裝備時點擊應顯示無裝提示: %s" % (msg_lbl.text if msg_lbl else ""))
	var confirm_dlg = dlg.find_child("DismantleConfirmDialog", true, false)
	_assert(confirm_dlg == null, "背包無裝備時不應開啟確認彈窗")

	# 3. 準備測試裝備：
	#    - 凡品武器 1 件 (common) -> 應納入分解
	#    - 良品護甲 1 件 (uncommon) -> 應納入分解
	#    - 貴重上品飾品 1 件 (rare) -> 保護貴重裝備，不納入未標記分解
	#    - 已上鎖凡品 1 件 (locked=true) -> 玩家上鎖保護，不納入分解
	#    - 裝備中的裝備 1 件 (equip_worn) -> 已穿戴保護，不納入分解
	var c_inst: Dictionary = eq.roll_instance("rusty_blade", "common")
	eq.add_to_bag(c_inst)

	var u_inst: Dictionary = eq.roll_instance("meager_edge", "uncommon")
	eq.add_to_bag(u_inst)

	var r_inst: Dictionary = eq.roll_instance("knight_saber", "rare")
	eq.add_to_bag(r_inst)

	var locked_inst: Dictionary = eq.roll_instance("ash_mail", "common")
	locked_inst["locked"] = true
	eq.add_to_bag(locked_inst)

	var worn_uid := str(gs.equip_slots.get("weapon", ""))
	_assert(not worn_uid.is_empty(), "角色應有開局裝備中武器")

	var surplus_items: Array = eq.get_surplus_bag_items()
	_assert(surplus_items.size() == 2, "get_surplus_bag_items 應精確篩選出 2 件未鎖定之低階未裝備 (實際 %d 件)" % surplus_items.size())

	# 計算預估鐵屑與金幣
	var y1: Dictionary = eq.dismantle_yield(c_inst)
	var y2: Dictionary = eq.dismantle_yield(u_inst)
	var exp_scrap: int = int(y1.get("iron_scrap", 0)) + int(y2.get("iron_scrap", 0))
	var exp_gold: int = int(y1.get("gold", 0)) + int(y2.get("gold", 0))

	# 4. 點擊一鍵分解按鈕 -> 彈出確認彈窗 (DismantleConfirmDialog)
	btn_dismantle.pressed.emit()
	confirm_dlg = dlg.find_child("DismantleConfirmDialog", true, false)
	_assert(confirm_dlg != null, "點擊一鍵分解後應彈出 DismantleConfirmDialog 確認彈窗")

	if confirm_dlg:
		var title_lbl: Label = confirm_dlg.find_child("ConfirmTitleLabel", true, false) as Label
		var count_lbl: Label = confirm_dlg.find_child("DismantleCountLabel", true, false) as Label
		var yield_lbl: Label = confirm_dlg.find_child("DismantleYieldLabel", true, false) as Label
		var safe_lbl: Label = confirm_dlg.find_child("DismantleSafeLabel", true, false) as Label
		var btn_cancel: Button = confirm_dlg.find_child("BtnCancelDismantle", true, false) as Button
		var btn_confirm: Button = confirm_dlg.find_child("BtnConfirmDismantle", true, false) as Button

		_assert(title_lbl != null and title_lbl.text.contains("確認一鍵分解"), "彈窗標題正確")
		_assert(count_lbl != null and count_lbl.text.contains("2"), "彈窗數量顯示正確 (2 件)")
		_assert(yield_lbl != null and yield_lbl.text.contains(str(exp_scrap)) and yield_lbl.text.contains(str(exp_gold)),
			"彈窗預估收益顯示正確: 鐵屑×%d、金幣+%d" % [exp_scrap, exp_gold])
		_assert(safe_lbl != null and safe_lbl.text.contains("貴重裝備受保護"), "彈窗防誤觸貴重裝備提示正確")
		_assert(btn_cancel != null and btn_cancel.custom_minimum_size.y >= 48, "取消按鈕熱區合格")
		_assert(btn_confirm != null and btn_confirm.custom_minimum_size.y >= 48, "確認分解按鈕熱區合格")

		# 5. 測試取消按鈕：點擊取消後彈窗關閉且裝備未被分解
		btn_cancel.pressed.emit()
		var confirm_closed = dlg.find_child("DismantleConfirmDialog", true, false)
		_assert(confirm_closed == null or confirm_closed.is_queued_for_deletion(), "點擊取消按鈕應關閉確認彈窗")
		_assert(gs.equip_bag.size() == 4, "取消後背包裝備數量仍為 4 件未變")

	# 6. 再次點擊一鍵分解並確認分解
	btn_dismantle.pressed.emit()
	confirm_dlg = dlg.find_child("DismantleConfirmDialog", true, false)
	_assert(confirm_dlg != null, "重新開啟確認彈窗成功")

	var pre_scrap: int = inv.count("iron_scrap")
	var pre_gold: int = gs.gold

	if confirm_dlg:
		var btn_confirm: Button = confirm_dlg.find_child("BtnConfirmDismantle", true, false) as Button
		btn_confirm.pressed.emit()

		# 驗證彈窗關閉
		var confirm_post = dlg.find_child("DismantleConfirmDialog", true, false)
		_assert(confirm_post == null or confirm_post.is_queued_for_deletion(), "確認分解後彈窗關閉")

		# 驗證背包多餘裝備已清空，但貴重裝備與已上鎖裝備保留
		_assert(eq.find_bag(str(c_inst.get("uid"))).is_empty(), "凡品裝備已自背包清除")
		_assert(eq.find_bag(str(u_inst.get("uid"))).is_empty(), "良品裝備已自背包清除")
		_assert(not eq.find_bag(str(r_inst.get("uid"))).is_empty(), "貴重上品裝備完整保留在背包")
		_assert(not eq.find_bag(str(locked_inst.get("uid"))).is_empty(), "上鎖裝備完整保留在背包")

		# 驗證材料增加
		_assert(inv.count("iron_scrap") == pre_scrap + exp_scrap, "鐵屑數量增加: 原 %d -> 現 %d (+%d)" % [pre_scrap, inv.count("iron_scrap"), exp_scrap])
		_assert(gs.gold == pre_gold + exp_gold, "金幣數量增加: 原 %d -> 現 %d (+%d)" % [pre_gold, gs.gold, exp_gold])

		# 驗證回饋訊息
		if msg_lbl:
			_assert(msg_lbl.text.contains("已分解 2 件多餘裝備") and msg_lbl.text.contains(str(exp_scrap)),
				"鍛造頁訊息標籤回報成功: %s" % msg_lbl.text)

	# 7. 測試多語系即時切換
	print("\n--- 測試一鍵分解相關多國語系即時切換 ---")
	for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
		if loc_node:
			loc_node.call("set_locale", code)
		_assert(not _has_emoji(btn_dismantle.text), "[%s] 一鍵分解按鈕無 Emoji: %s" % [code, btn_dismantle.text])

	dlg.queue_free()
	print("=== test_forge_batch_dismantle 測試完成 ===")
