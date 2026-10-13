extends SceneTree
## 《發條之心》MapleInventory 探索背包支援選取機芯拆解回收與安全防護單元測試
## (scripts/ui/test_maple_inventory_core_dismantle.gd)
## 依據任務 t_00903732 驗收標準：
## 1. 當玩家在機芯頁籤選取未裝備機芯時，顯示珊瑚粉果凍厚底按鈕『拆解回收』（高>=48px，底邊5px，零Emoji）。
## 2. 點擊後依 CoreSystem 八色階標準產出鐵屑：灰1／白2／橘3／藍4／紫5／金6／綠8／紅10，發放至 GameState.iron_scrap 並從背包扣除該機芯，播放音效與飄字提示，即時刷新背包格子與容量進度。
## 3. 安全防護：若該機芯已裝備於五大槽位（is_selected_item_equipped()），按鈕切換為禁用置灰，顯示『已裝備無法拆解』，嚴防誤拆上身機芯。
## 4. 六語系支援（zh_TW, zh_CN, en, ja, ko, es），零殘留英文/中文缺詞。
## 5. 實機截圖存證至 proofs/t_00903732/，且各幀 SHA256 互異。

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const CoreSystemClass = preload("res://scripts/systems/core_system.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _inv: Node = null
var _cs: Node = null
var _gs: Node = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0
var _ok: bool = true
var _captured_hashes: Dictionary = {}
var _out_dir: String = ""

# 測試用機芯 UID
var _equipped_mainspring_uid: String = "core_test_equipped_mainspring"
var _unequipped_blue_uid: String = "core_test_unequipped_blue"
var _unequipped_gold_uid: String = "core_test_unequipped_gold"
var _locked_chassis_uid: String = "core_test_locked_chassis"


func _fail(msg: String) -> bool:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false
	quit(1)
	return false


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _check_no_emoji_in_tree(n: Node) -> bool:
	if n is Label:
		if _has_emoji((n as Label).text):
			_fail("Label 包含 emoji: " + (n as Label).text)
			return false
	elif n is Button:
		if _has_emoji((n as Button).text):
			_fail("Button 包含 emoji: " + (n as Button).text)
			return false
	for ch in n.get_children():
		if not _check_no_emoji_in_tree(ch):
			return false
	return true


func _save_screenshot(filename: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	var img := root.get_viewport().get_texture().get_image()
	if img != null:
		var p := _out_dir.path_join(filename)
		DirAccess.make_dir_recursive_absolute(_out_dir)
		img.save_png(p)
		var h := FileAccess.get_sha256(p)
		_captured_hashes[filename] = h
		print("  [SNAPSHOT] 已存檔截圖: %s (SHA256: %s)" % [p, h.substr(0, 16)])


func _initialize() -> void:
	print("=== 開始 test_maple_inventory_core_dismantle 測試 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_00903732")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc = LocClass.new()
			_loc.name = "Loc"
			root.add_child(_loc)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	var inv_sys = root.get_node_or_null("InventorySystem")
	if inv_sys == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv_sys = InvClass.new()
			inv_sys.name = "InventorySystem"
			root.add_child(inv_sys)

	_cs = root.get_node_or_null("CoreSystem")
	if _cs == null:
		_cs = CoreSystemClass.new()
		_cs.name = "CoreSystem"
		root.add_child(_cs)

	if _loc and _loc.has_method("set_locale"):
		_loc.call("set_locale", "zh_TW")

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 4:
				return false
			_inv.open()
			_step = 1
			_wait = 0

		1:
			if _wait < 4:
				return false
			print("\n--- 1. 驗證 CoreSystem 八色階標準鐵屑產出計算 ---")
			# 灰1／白2／橘3／藍4／紫5／金6／綠8／紅10
			var expected_scrap := {
				"gray": 1,
				"white": 2,
				"orange": 3,
				"blue": 4,
				"purple": 5,
				"gold": 6,
				"green": 8,
				"red": 10
			}
			for tier_k in expected_scrap.keys():
				var test_p := {"tier": tier_k, "name": "測試機芯·" + tier_k}
				var yield_scrap := CoreSystemClass.get_dismantle_scrap_yield(test_p)
				var exp_val: int = expected_scrap[tier_k]
				if yield_scrap != exp_val:
					return _fail("色階 %s 預期產出 %d 鐵屑，實得 %d" % [tier_k, exp_val, yield_scrap])
				print("  ✓ 色階 [%s] 產出鐵屑對齊: %d (100%% 符合標準)" % [tier_k, yield_scrap])

			print("\n--- 2. 初始化測試機芯資料與裝備槽位 ---")
			CoreSystemClass.clear_inventory()
			if "core_slots" in _gs:
				_gs.core_slots.clear()
			if "core_bag" in _gs:
				_gs.core_bag.clear()
			if "inventory" in _gs:
				_gs.inventory["iron_scrap"] = 0
			_gs.iron_scrap = 0

			# 建立已裝備於發條發電機的機芯 (mainspring)
			var eq_part := CoreSystemClass.create_part_by_tier("mainspring", "white", {"ATK": 5})
			eq_part["uid"] = _equipped_mainspring_uid
			eq_part["name"] = "發條發電機·白階"
			CoreSystemClass.add_part_to_inventory(eq_part)
			CoreSystemClass.equip_part("mainspring", eq_part)
			print("  ✓ 已將機芯 [%s] 裝備至發條發電機槽位" % _equipped_mainspring_uid)

			# 建立未裝備機芯：藍階齒輪組 (blue)
			var blue_part := CoreSystemClass.create_part_by_tier("gear_train", "blue", {"ATK": 15})
			blue_part["uid"] = _unequipped_blue_uid
			blue_part["name"] = "傳動齒輪組·藍階"
			CoreSystemClass.add_part_to_inventory(blue_part)

			# 建立未裝備機芯：金階共鳴核心 (gold)
			var gold_part := CoreSystemClass.create_part_by_tier("soul_core", "gold", {"ATK": 35})
			gold_part["uid"] = _unequipped_gold_uid
			gold_part["name"] = "共鳴核心·金階"
			CoreSystemClass.add_part_to_inventory(gold_part)

			# 建立未裝備機芯：鎖定機殼裝甲 (purple)
			var locked_part := CoreSystemClass.create_part_by_tier("chassis", "purple", {"DEF": 20})
			locked_part["uid"] = _locked_chassis_uid
			locked_part["name"] = "機殼裝甲·紫階"
			CoreSystemClass.add_part_to_inventory(locked_part)

			_inv.set_item_locked(_locked_chassis_uid, true)

			_inv.set_category("core")
			_inv.set("_selected", "")
			_inv.refresh()

			_step = 2
			_wait = 0

		2:
			if _wait < 4:
				return false
			print("\n--- 3. 驗證拆解回收按鈕樣式與規格 ---")
			var d_btn: Button = _inv.get_dismantle_button()
			if d_btn == null:
				return _fail("找不到 BtnDismantle 按鈕")

			if d_btn.custom_minimum_size.y < 48:
				return _fail("按鈕熱區高度不足 48px，實得: %f" % d_btn.custom_minimum_size.y)
			print("  ✓ 按鈕熱區高度符合規範: %f px (>= 48px)" % d_btn.custom_minimum_size.y)

			# 驗證未選取時按鈕隱藏
			if d_btn.visible:
				return _fail("未選取物品時 BtnDismantle 應為隱藏")
			print("  ✓ 未選取物品時按鈕正常隱藏")

			# 設定選取已裝備機芯
			_inv.set("_selected", _equipped_mainspring_uid)
			_inv.refresh()

			_step = 3
			_wait = 0

		3:
			if _wait < 6:
				return false
			print("\n--- 4. 驗證安全防護：已裝備於五大槽位之機芯嚴禁拆解 ---")
			if not _inv.is_selected_item_equipped():
				return _fail("is_selected_item_equipped() 應辨識出已裝備機芯")
			print("  ✓ is_selected_item_equipped() 正確回傳 true (已裝備防護辨識成功)")

			var d_btn: Button = _inv.get_dismantle_button()
			if not d_btn.visible:
				return _fail("選取機芯時 BtnDismantle 應為可見")
			if not d_btn.disabled:
				return _fail("已裝備機芯之拆解按鈕必須禁用置灰 (disabled=true)")
			if d_btn.text != "已裝備無法拆解":
				return _fail("已裝備機芯按鈕文字應為『已裝備無法拆解』，實得: '%s'" % d_btn.text)
			print("  ✓ 已裝備機芯防誤拆保護生效: disabled=true, 按鈕文字='已裝備無法拆解'")

			var block_res: Dictionary = _inv.dismantle_selected()
			if bool(block_res.get("ok", false)):
				return _fail("dismantle_selected() 於已裝備機芯時不應成功執行")
			print("  ✓ dismantle_selected() 阻擋生效: msg='%s'" % str(block_res.get("msg", "")))

			_save_screenshot("proof_01_core_equipped_protected_zh_tw.png")

			# 切換選取未裝備藍階機芯
			_inv.set("_selected", _unequipped_blue_uid)
			_inv.refresh()

			_step = 4
			_wait = 0

		4:
			if _wait < 6:
				return false
			print("\n--- 5. 驗證未裝備機芯選取與拆解按鈕啟用 ---")
			if _inv.is_selected_item_equipped():
				return _fail("未裝備藍階機芯不應回傳 is_selected_item_equipped()=true")

			var d_btn: Button = _inv.get_dismantle_button()
			if not d_btn.visible:
				return _fail("選取未裝備機芯時拆解按鈕應為可見")
			if d_btn.disabled:
				return _fail("選取未裝備機芯時拆解按鈕應為啟用 (disabled=false)")
			if d_btn.text != "拆解回收":
				return _fail("選取未裝備機芯按鈕文字應為『拆解回收』，實得: '%s'" % d_btn.text)
			print("  ✓ 選取未裝備機芯啟用拆解按鈕: disabled=false, 文字='拆解回收'")

			_save_screenshot("proof_02_core_unequipped_ready_dismantle_zh_tw.png")

			# 執行拆解未裝備藍階機芯
			var scrap_before: int = _gs.iron_scrap
			var cap_before: int = _inv.get_occupied_capacity()
			var bag_count_before: int = CoreSystemClass.get_inventory().size()

			var sig_box := [false, {}, {}]
			_inv.core_dismantled.connect(func(p, r):
				sig_box[0] = true
				sig_box[1] = p
				sig_box[2] = r
			, CONNECT_ONE_SHOT)

			var res: Dictionary = _inv.dismantle_selected()
			if not bool(res.get("ok", false)):
				return _fail("拆解未裝備藍階機芯失敗: " + str(res.get("msg", "")))

			var scrap_after: int = _gs.iron_scrap
			var scrap_gain: int = int(res.get("iron_scrap", 0))
			if scrap_gain != 4:
				return _fail("藍階機芯拆解獲得鐵屑應為 4，實得: %d" % scrap_gain)
			if scrap_after != scrap_before + 4:
				return _fail("GameState.iron_scrap 未如期增加 4，原: %d, 現: %d" % [scrap_before, scrap_after])
			print("  ✓ 藍階機芯拆解成功獲得鐵屑: +4 (總鐵屑: %d)" % scrap_after)

			var bag_count_after: int = CoreSystemClass.get_inventory().size()
			if bag_count_after != bag_count_before - 1:
				return _fail("CoreSystem 背包數量未減少 1，原: %d, 現: %d" % [bag_count_before, bag_count_after])
			for p in CoreSystemClass.get_inventory():
				if str(p.get("uid", "")) == _unequipped_blue_uid:
					return _fail("背包中仍殘留已拆解機芯: " + _unequipped_blue_uid)
			print("  ✓ 已拆解機芯已從背包乾淨扣除")

			var cap_after: int = _inv.get_occupied_capacity()
			if cap_after != cap_before - 1:
				return _fail("容量進度未即時更新，原: %d, 現: %d" % [cap_before, cap_after])
			print("  ✓ 背包容量進度即時刷新: %d -> %d" % [cap_before, cap_after])

			if not sig_box[0]:
				return _fail("未發射 core_dismantled 訊號")
			print("  ✓ 成功接收 core_dismantled 訊號")

			_step = 5
			_wait = 0

		5:
			if _wait < 6:
				return false
			print("\n--- 6. 記錄拆解後背包狀態截圖 ---")
			_save_screenshot("proof_03_core_dismantled_scrap_gained_zh_tw.png")

			# 切換至英文語系並選取金階未裝備機芯
			_inv.set_locale("en")
			_inv.set("_selected", _unequipped_gold_uid)
			_inv.refresh()

			_step = 6
			_wait = 0

		6:
			if _wait < 6:
				return false
			print("\n--- 7. 驗證英文語系在地化切換 ---")
			var d_btn: Button = _inv.get_dismantle_button()
			if d_btn.text != "Dismantle":
				return _fail("[en] 拆解按鈕文案應為 'Dismantle'，實得: '%s'" % d_btn.text)
			print("  ✓ [en] 未裝備按鈕在地化正確: 'Dismantle'")

			_save_screenshot("proof_04_core_dismantle_en.png")

			# 切換至日文語系並選取金階未裝備機芯
			_inv.set_locale("ja")
			_inv.set("_selected", _unequipped_gold_uid)
			_inv.refresh()

			_step = 7
			_wait = 0

		7:
			if _wait < 6:
				return false
			print("\n--- 8. 驗證日文語系在地化切換 ---")
			var d_btn: Button = _inv.get_dismantle_button()
			if d_btn.text != "分解回収":
				return _fail("[ja] 拆解按鈕文案應為 '分解回収'，實得: '%s'" % d_btn.text)
			print("  ✓ [ja] 未裝備按鈕在地化正確: '分解回収'")

			_save_screenshot("proof_05_core_dismantle_ja.png")

			# 切回繁中，進行安全阻擋（鎖定）與全色階驗證
			_inv.set_locale("zh_TW")
			_inv.set("_selected", _locked_chassis_uid)
			_inv.refresh()

			_step = 8
			_wait = 0

		8:
			if _wait < 4:
				return false
			print("\n--- 9. 驗證已鎖定安全阻擋 ---")
			var d_btn: Button = _inv.get_dismantle_button()
			if not d_btn.disabled:
				return _fail("已鎖定機芯之拆解按鈕必須禁用置灰 (disabled=true)")
			if d_btn.text != "已鎖定無法拆解":
				return _fail("已鎖定機芯按鈕文字應為『已鎖定無法拆解』，實得: '%s'" % d_btn.text)
			print("  ✓ 已鎖定機芯防誤拆保護生效: disabled=true, 按鈕文字='已鎖定無法拆解'")

			var lock_res: Dictionary = _inv.dismantle_selected()
			if bool(lock_res.get("ok", false)):
				return _fail("dismantle_selected() 於已鎖定機芯時不應成功執行")
			print("  ✓ 已鎖定機芯阻擋生效: msg='%s'" % str(lock_res.get("msg", "")))

			print("\n--- 10. 驗證六語系字典完整性與文字斷言 ---")
			var expected_loc_texts := {
				"zh_TW": {"ready": "拆解回收", "worn": "已裝備無法拆解", "locked": "已鎖定無法拆解"},
				"zh_CN": {"ready": "拆解回收", "worn": "已装备无法拆解", "locked": "已锁定无法拆解"},
				"en": {"ready": "Dismantle", "worn": "Equipped (Cannot Dismantle)", "locked": "Locked (Cannot Dismantle)"},
				"ja": {"ready": "分解回収", "worn": "装備中（分解不可）", "locked": "ロック中（分解不可）"},
				"ko": {"ready": "분해 회수", "worn": "장착 중（분해 불가）", "locked": "잠금 중（분해 불가）"},
				"es": {"ready": "Desmantelar", "worn": "Equipado (No Desmantelar)", "locked": "Bloqueado (No Desmantelar)"}
			}
			for loc_code in expected_loc_texts.keys():
				_inv.set_locale(loc_code)
				var exp_dict: Dictionary = expected_loc_texts[loc_code]

				_inv.set("_selected", _unequipped_gold_uid)
				_inv.refresh()
				if _inv.get_dismantle_button().text != exp_dict["ready"]:
					return _fail("[%s] ready 文案不符，預期 '%s' 實得 '%s'" % [loc_code, exp_dict["ready"], _inv.get_dismantle_button().text])

				_inv.set("_selected", _equipped_mainspring_uid)
				_inv.refresh()
				if _inv.get_dismantle_button().text != exp_dict["worn"]:
					return _fail("[%s] worn 文案不符，預期 '%s' 實得 '%s'" % [loc_code, exp_dict["worn"], _inv.get_dismantle_button().text])

				print("  ✓ [%s] 語系文案完整通過: ready='%s', worn='%s'" % [loc_code, exp_dict["ready"], exp_dict["worn"]])

			_inv.set_locale("zh_TW")

			print("\n--- 11. 驗證全色階機芯實際拆解所得鐵屑 ---")
			_inv.set("_selected", _unequipped_gold_uid)
			_inv.refresh()
			var scrap_pre_gold: int = _gs.iron_scrap
			var gold_res: Dictionary = _inv.dismantle_selected()
			if not bool(gold_res.get("ok", false)):
				return _fail("拆解金階機芯失敗: " + str(gold_res.get("msg", "")))
			if _gs.iron_scrap != scrap_pre_gold + 6:
				return _fail("金階機芯應產出 6 鐵屑，原: %d, 現: %d" % [scrap_pre_gold, _gs.iron_scrap])
			print("  ✓ 金階機芯拆解成功獲得 +6 鐵屑 (總計 %d)" % _gs.iron_scrap)

			var tier_sample := [
				{"tier": "gray", "slot": "mainspring", "exp": 1},
				{"tier": "white", "slot": "chassis", "exp": 2},
				{"tier": "orange", "slot": "escapement", "exp": 3},
				{"tier": "purple", "slot": "gear_train", "exp": 5},
				{"tier": "green", "slot": "soul_core", "exp": 8},
				{"tier": "red", "slot": "mainspring", "exp": 10}
			]
			for s in tier_sample:
				var part := CoreSystemClass.create_part_by_tier(s["slot"], s["tier"], {})
				var p_uid: String = "core_sample_%s" % s["tier"]
				part["uid"] = p_uid
				part["name"] = "機芯·%s" % s["tier"]
				CoreSystemClass.add_part_to_inventory(part)
				_inv.set("_selected", p_uid)
				_inv.refresh()
				var s_before: int = _gs.iron_scrap
				var s_res: Dictionary = _inv.dismantle_selected()
				if not bool(s_res.get("ok", false)):
					return _fail("拆解 %s 階機芯失敗" % s["tier"])
				var exp_gain: int = s["exp"]
				if _gs.iron_scrap != s_before + exp_gain:
					return _fail("%s 階機芯應增加 %d 鐵屑，實增 %d" % [s["tier"], exp_gain, _gs.iron_scrap - s_before])
				print("  ✓ [%s] 階機芯實際拆解增加 +%d 鐵屑" % [s["tier"], exp_gain])

			print("\n--- 12. 全介面零系統 Emoji 檢驗 ---")
			if not _check_no_emoji_in_tree(_inv):
				return _fail("介面樹包含未授權之系統 Emoji")
			print("  ✓ 全介面 100% 零系統 Emoji 檢驗通過")

			print("\n--- 13. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var hash_list: Array = []
				for fn in _captured_hashes.keys():
					var h: String = _captured_hashes[fn]
					if hash_list.has(h):
						return _fail("截圖雜湊值重複: %s" % fn)
					hash_list.append(h)
				print("  ✓ 全部 %d 張實機截圖 SHA256 互異獨立通過" % _captured_hashes.size())
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 機芯拆解回收與安全防護單元測試通過！")
			print("MAPLE_INVENTORY_CORE_DISMANTLE_OK")
			print("=======================================================")
			quit(0)
			return true

	return false
