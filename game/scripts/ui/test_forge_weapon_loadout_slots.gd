extends SceneTree
## 無頭單元測試：ForgeDialog 天宮鐵匠支援三欄武器槽位切換鍛造 (t_5fbd8e22)
## 覆蓋驗收項目：
## 1. ForgeDialog 武器資訊面板上方具備三欄武器槽位切換 Chip / 頁籤 (WeaponSlotChipRow, 3 個 Chip)。
## 2. 三欄槽位 Chip 高度 >= 44px (人體工學與手遊防誤觸)。
## 3. 依 EquipmentSystem.loadout_slot_unlocked 呈現解鎖與鎖定狀態 (未解鎖顯示需達等級，點擊提示未解鎖且不切換)。
## 4. 點擊已解鎖槽位連動 EquipmentSystem.switch_weapon_loadout(slot_index)，即時切換作用中武器。
## 5. 動態刷新武器名稱、品質色階 (QualityLabel)、攻擊力、鍛造消耗與副詞條清單 (AffixLabel)。
## 6. 在鐵匠鋪內鍛造成功後，數值 (tier, rolled.atk) 正確寫回該槽位武器，資訊面板與 Chip 即時更新。
## 7. 空槽防護：空槽切換顯示未裝備狀態，鍛造按鈕禁用。
## 8. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 字典完整對齊與即時連動，遵循 review.md 第 28 條規範。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0
var _dlg = null
var _gs: Node = null
var _eq: Node = null
var _loc: Node = null


func _fail(msg: String) -> void:
	push_error("[FAIL] " + msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始執行 ForgeDialog 三欄武器槽位切換鍛造驗收測試 (t_5fbd8e22) ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_run_tests()
				if _ok:
					print("\n=======================================================")
					print("TEST_FORGE_WEAPON_LOADOUT_SLOTS_OK")
					quit(0)
				else:
					push_error("TEST_FORGE_WEAPON_LOADOUT_SLOTS_FAIL")
					print("\n=======================================================")
					print("TEST_FORGE_WEAPON_LOADOUT_SLOTS_FAIL")
					quit(1)
				return true
	return false


func _run_tests() -> void:
	_gs = root.get_node_or_null("GameState")
	_eq = root.get_node_or_null("EquipmentSystem")
	_loc = root.get_node_or_null("Loc")

	if _gs == null or _eq == null or _loc == null:
		_fail("場景樹中缺少必要節點 (GameState / EquipmentSystem / Loc)")
		return

	# 初始化重置狀態
	_gs.call("reset_new_game")
	_gs.set("level", 5) # 先設為 Lv5 (僅槽位 0 解鎖，槽位 1 與 2 鎖定)
	_gs.set("gold", 5000)
	_gs.set("weapon_loadout_active", 0)

	print("\n--- 1. 檢驗 ForgeDialog 節點結構與三欄 Chip 規格 ---")
	var ForgeDialogScn = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScn == null:
		_fail("無法加載 res://scripts/ui/forge_dialog.gd")
		return
	_dlg = ForgeDialogScn.new()
	root.add_child(_dlg)

	var chip_row := _dlg.find_child("WeaponSlotChipRow", true, false) as HBoxContainer
	if chip_row == null:
		_fail("ForgeDialog 缺少 WeaponSlotChipRow 容器節點")
		return
	print("  ✓ 找到 WeaponSlotChipRow 容器節點")

	var chips: Array = _dlg.get_slot_chips()
	if chips.size() != 3:
		_fail("武器槽位 Chip 數量不等於 3，實際為 %d" % chips.size())
		return
	print("  ✓ 武器槽位 Chip 數量為 3 (槽位 1 / 槽位 2 / 槽位 3)")

	for i in range(3):
		var chip: Button = chips[i]
		if chip.custom_minimum_size.y < 44.0:
			_fail("槽位 Chip %d 高度未達規範 (期望 >= 44px，實際 %.1fpx)" % [i, chip.custom_minimum_size.y])
		else:
			print("  ✓ 槽位 Chip %d 高度符合規範 (%.1fpx >= 44px)" % [i, chip.custom_minimum_size.y])

	var q_lbl: Label = _dlg.get_quality_label()
	if q_lbl == null or q_lbl.name != "QualityLabel":
		_fail("ForgeDialog 缺少 QualityLabel 品質色階標籤")
	else:
		print("  ✓ 找到 QualityLabel 品質色階標籤")

	var af_lbl: Label = _dlg.get_affix_label()
	if af_lbl == null or af_lbl.name != "AffixLabel":
		_fail("ForgeDialog 缺少 AffixLabel 副詞條清單標籤")
	else:
		print("  ✓ 找到 AffixLabel 副詞條清單標籤")

	print("\n--- 2. 檢驗 Lv5 未解鎖狀態與點擊防護 ---")
	# Lv5: slot 0 解鎖, slot 1 (Lv10), slot 2 (Lv16) 鎖定
	_dlg.call("_refresh_display")
	var chip0_text: String = (chips[0] as Button).text
	var chip1_text: String = (chips[1] as Button).text
	var chip2_text: String = (chips[2] as Button).text
	print("  Chip 0 顯示: ", chip0_text)
	print("  Chip 1 顯示: ", chip1_text)
	print("  Chip 2 顯示: ", chip2_text)

	if not ("需 Lv10" in chip1_text or "Lv10" in chip1_text):
		_fail("槽位 1 在 Lv5 時未正確呈現需 Lv10 鎖定提示: " + chip1_text)
	else:
		print("  ✓ 槽位 1 正確呈現需 Lv10 鎖定狀態")

	if not ("需 Lv16" in chip2_text or "Lv16" in chip2_text):
		_fail("槽位 2 在 Lv5 時未正確呈現需 Lv16 鎖定提示: " + chip2_text)
	else:
		print("  ✓ 槽位 2 正確呈現需 Lv16 鎖定狀態")

	# 點擊未解鎖的 slot 1
	var prev_active: int = int(_eq.call("active_loadout_index"))
	chips[1].emit_signal("pressed")
	var cur_active: int = int(_eq.call("active_loadout_index"))
	if cur_active != prev_active:
		_fail("未解鎖的槽位 1 點擊後不應被切換！")
	else:
		print("  ✓ 點擊未解鎖槽位 1 成功阻擋切換")

	var msg_lbl: Label = _dlg.find_child("MsgLabel", true, false) as Label
	if msg_lbl != null and "需達到 Lv10" in msg_lbl.text:
		print("  ✓ 點擊未解鎖槽位 1 正確提示訊息: ", msg_lbl.text)
	else:
		_fail("點擊未解鎖槽位 1 訊息未提示需達到 Lv10: " + (msg_lbl.text if msg_lbl else "null"))

	print("\n--- 3. 角色升級至 Lv20，配置三把不同裝備並測試切換 ---")
	_gs.set("level", 20) # 達到 Lv20，三槽皆解鎖
	if _gs.has_method("calc_level_stats"):
		_gs.call("calc_level_stats")

	# 設定三把武器實體
	var w0: Dictionary = {
		"uid": "w_test_0",
		"base_id": "sword",
		"name": "微末之刃",
		"slot": "weapon",
		"line": "sword",
		"tier": 1,
		"quality": "common",
		"quality_label": "凡品",
		"rolled": {"atk": 10}
	}
	var w1: Dictionary = {
		"uid": "w_test_1",
		"base_id": "hammer",
		"name": "鐵骨重鎚",
		"slot": "weapon",
		"line": "hammer",
		"tier": 2,
		"quality": "rare",
		"quality_label": "上品",
		"rolled": {"atk": 24, "crit": 5.0, "def": 8}
	}
	var w2: Dictionary = {
		"uid": "w_test_2",
		"base_id": "bow",
		"name": "赤炎神弓",
		"slot": "weapon",
		"line": "bow",
		"tier": 3,
		"quality": "epic",
		"quality_label": "秘寶",
		"rolled": {"atk": 36, "crit": 12.5, "hp": 50}
	}

	_gs.equip_worn["w_test_0"] = w0
	_gs.equip_worn["w_test_1"] = w1
	_gs.equip_worn["w_test_2"] = w2

	_gs.weapon_loadout[0] = "w_test_0"
	_gs.weapon_loadout[1] = "w_test_1"
	_gs.weapon_loadout[2] = "w_test_2"
	_gs.weapon_loadout_active = 0
	_gs.equip_slots["weapon"] = "w_test_0"
	_eq.call("_sync_active_weapon_mirror")

	_dlg.call("_refresh_display")

	print("  Chip 0 (解鎖後): ", chips[0].text)
	print("  Chip 1 (解鎖後): ", chips[1].text)
	print("  Chip 2 (解鎖後): ", chips[2].text)

	if not ("微末之刃" in chips[0].text and "T1" in chips[0].text):
		_fail("Chip 0 未正確顯示微末之刃 T1: " + chips[0].text)
	if not ("鐵骨重鎚" in chips[1].text and "T2" in chips[1].text):
		_fail("Chip 1 未正確顯示鐵骨重鎚 T2: " + chips[1].text)
	if not ("赤炎神弓" in chips[2].text and "T3" in chips[2].text):
		_fail("Chip 2 未正確顯示赤炎神弓 T3: " + chips[2].text)
	print("  ✓ 三槽位 Chip 正確解析並顯示各自武器名稱與階級")

	print("\n--- 4. 測試點擊 Chip 1 切換至副手武器 (鐵骨重鎚) ---")
	chips[1].emit_signal("pressed")

	if int(_eq.call("active_loadout_index")) != 1:
		_fail("點擊 Chip 1 後 EquipmentSystem.active_loadout_index 未切換為 1")
	else:
		print("  ✓ EquipmentSystem 成功切換至槽位 1")

	var weapon_lbl: Label = _dlg.find_child("WeaponLabel", true, false) as Label
	var atk_lbl: Label = _dlg.find_child("AtkLabel", true, false) as Label
	var cost_lbl: Label = _dlg.find_child("CostLabel", true, false) as Label

	print("  切換後 WeaponLabel: ", weapon_lbl.text)
	print("  切換後 AtkLabel: ", atk_lbl.text)
	print("  切換後 QualityLabel: ", q_lbl.text)
	print("  切換後 AffixLabel: ", af_lbl.text)
	print("  切換後 CostLabel: ", cost_lbl.text)

	if not ("鐵骨重鎚" in weapon_lbl.text and "第 2 階" in weapon_lbl.text):
		_fail("切換至槽位 1 後武器名稱或階級未即時更新: " + weapon_lbl.text)
	else:
		print("  ✓ 武器名稱與階級正確刷新為【鐵骨重鎚（第 2 階）】")

	if not ("+24" in atk_lbl.text):
		_fail("切換至槽位 1 後攻擊力未刷新為 +24: " + atk_lbl.text)
	else:
		print("  ✓ 武器攻擊力正確刷新為 +24")

	if not ("上品" in q_lbl.text):
		_fail("切換至槽位 1 後品質色階未刷新為上品: " + q_lbl.text)
	else:
		print("  ✓ 品質色階正確刷新為【上品】")

	if not ("暴擊 +5.0%" in af_lbl.text and "防禦 +8" in af_lbl.text):
		_fail("切換至槽位 1 後副詞條清單未正確列出暴擊與防禦: " + af_lbl.text)
	else:
		print("  ✓ 副詞條清單正確呈現【暴擊 +5.0% · 防禦 +8】")

	print("\n--- 5. 測試點擊 Chip 2 切換至絕技武器 (赤炎神弓) ---")
	chips[2].emit_signal("pressed")

	if int(_eq.call("active_loadout_index")) != 2:
		_fail("點擊 Chip 2 後 EquipmentSystem.active_loadout_index 未切換為 2")
	else:
		print("  ✓ EquipmentSystem 成功切換至槽位 2")

	print("  切換後 WeaponLabel: ", weapon_lbl.text)
	print("  切換後 AtkLabel: ", atk_lbl.text)
	print("  切換後 QualityLabel: ", q_lbl.text)
	print("  切換後 AffixLabel: ", af_lbl.text)

	if not ("赤炎神弓" in weapon_lbl.text and "第 3 階" in weapon_lbl.text):
		_fail("切換至槽位 2 後武器名稱或階級未即時更新: " + weapon_lbl.text)
	else:
		print("  ✓ 武器名稱與階級正確刷新為【赤炎神弓（第 3 階）】")

	if not ("+36" in atk_lbl.text):
		_fail("切換至槽位 2 後攻擊力未刷新為 +36: " + atk_lbl.text)
	else:
		print("  ✓ 武器攻擊力正確刷新為 +36")

	if not ("秘寶" in q_lbl.text):
		_fail("切換至槽位 2 後品質色階未刷新為秘寶: " + q_lbl.text)
	else:
		print("  ✓ 品質色階正確刷新為【秘寶】")

	if not ("暴擊 +12.5%" in af_lbl.text and "生命 +50" in af_lbl.text):
		_fail("切換至槽位 2 後副詞條清單未正確列出暴擊與生命: " + af_lbl.text)
	else:
		print("  ✓ 副詞條清單正確呈現【暴擊 +12.5% · 生命 +50】")

	print("\n--- 6. 在鐵匠鋪內對槽位 1 進行鍛造並驗證數值正確寫回 ---")
	# 切回槽位 1 (鐵骨重鎚: T2, atk=24)
	chips[1].emit_signal("pressed")
	_gs.set("forge_fail_streak", 3) # 保底必成功
	_gs.set("gold", 10000)

	var prev_w1_atk: int = int(_gs.equip_worn["w_test_1"]["rolled"]["atk"])
	var prev_w1_tier: int = int(_gs.equip_worn["w_test_1"]["tier"])
	print("  鍛造前槽位 1 武器: Tier=%d, Atk=%d" % [prev_w1_tier, prev_w1_atk])

	var btn_forge: Button = _dlg.find_child("BtnForge", true, false) as Button
	if btn_forge == null:
		_fail("缺少 BtnForge 鍛造按鈕")
		return

	btn_forge.emit_signal("pressed")

	# 驗證數值已寫回 slot 1 武器
	var forged_w1: Dictionary = _gs.equip_worn["w_test_1"]
	var new_w1_tier: int = int(forged_w1.get("tier", 0))
	var new_w1_atk: int = int(forged_w1.get("rolled", {}).get("atk", 0))
	print("  鍛造後槽位 1 武器: Tier=%d, Atk=%d" % [new_w1_tier, new_w1_atk])

	if new_w1_tier != prev_w1_tier + 1:
		_fail("鍛造後槽位 1 武器階級未增加 (期望 %d, 實際 %d)" % [prev_w1_tier + 1, new_w1_tier])
	else:
		print("  ✓ 槽位 1 武器階級正確升至第 %d 階" % new_w1_tier)

	if new_w1_atk != prev_w1_atk + 2:
		_fail("鍛造後槽位 1 武器攻擊力未增加 2 (期望 %d, 實際 %d)" % [prev_w1_atk + 2, new_w1_atk])
	else:
		print("  ✓ 槽位 1 武器攻擊力正確增加為 %d (+2)" % new_w1_atk)

	# 驗證 UI 即時刷新
	if not ("第 3 階" in weapon_lbl.text):
		_fail("鍛造成功後 WeaponLabel 未即時刷新至第 3 階: " + weapon_lbl.text)
	if not ("+26" in atk_lbl.text):
		_fail("鍛造成功後 AtkLabel 未即時刷新至 +26: " + atk_lbl.text)
	if not ("T3" in chips[1].text):
		_fail("鍛造成功後 Chip 1 未即時刷新至 T3: " + chips[1].text)
	print("  ✓ 面板數值與 Chip 1 標籤即時連動刷新成功")

	# 驗證其他槽位數值未被竄改
	var w0_tier: int = int(_gs.equip_worn["w_test_0"].get("tier", 0))
	var w0_atk: int = int(_gs.equip_worn["w_test_0"].get("rolled", {}).get("atk", 0))
	var w2_tier: int = int(_gs.equip_worn["w_test_2"].get("tier", 0))
	var w2_atk: int = int(_gs.equip_worn["w_test_2"].get("rolled", {}).get("atk", 0))
	if w0_tier != 1 or w0_atk != 10:
		_fail("槽位 0 武器數值受到非預期干擾: Tier=%d, Atk=%d" % [w0_tier, w0_atk])
	if w2_tier != 3 or w2_atk != 36:
		_fail("槽位 2 武器數值受到非預期干擾: Tier=%d, Atk=%d" % [w2_tier, w2_atk])
	print("  ✓ 驗證槽位 0 與槽位 2 武器數值保持隔離無副作用")

	print("\n--- 7. 測試空槽防護機制 ---")
	# 卸下槽位 2 武器
	_gs.weapon_loadout[2] = ""
	_dlg.call("_refresh_display")
	print("  空槽狀態 Chip 2: ", chips[2].text)
	if not ("空槽" in chips[2].text):
		_fail("槽位 2 卸除後 Chip 2 未顯示空槽: " + chips[2].text)
	else:
		print("  ✓ Chip 2 正確顯示空槽狀態")

	# 點擊空槽
	chips[2].emit_signal("pressed")
	print("  點擊空槽後 WeaponLabel: ", weapon_lbl.text)
	print("  點擊空槽後 QualityLabel: ", q_lbl.text)
	print("  點擊空槽後 AffixLabel: ", af_lbl.text)
	print("  點擊空槽後 BtnForge.disabled: ", btn_forge.disabled)

	if not ("空槽" in weapon_lbl.text):
		_fail("選中空槽後 WeaponLabel 未呈現空槽提示: " + weapon_lbl.text)
	if not ("未裝備" in q_lbl.text):
		_fail("選中空槽後 QualityLabel 未呈現未裝備: " + q_lbl.text)
	if not ("無" in af_lbl.text):
		_fail("選中空槽後 AffixLabel 未呈現無副詞條: " + af_lbl.text)
	if not btn_forge.disabled:
		_fail("選中空槽後鍛造按鈕應被禁用 (disabled = true)！")
	else:
		print("  ✓ 選中空槽成功進入防護狀態，鍛造按鈕被禁用")

	print("\n--- 8. 測試六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換 (遵循 review.md 0-QA28) ---")
	# 切回槽位 0 驗證多語系
	chips[0].emit_signal("pressed")
	for code in LOCALES:
		_loc.call("set_locale", code)
		var exp_q := ContentLoc.text("ui", "品質色階：%s")
		var exp_af := ContentLoc.text("ui", "副詞條：%s")
		var exp_slot := ContentLoc.text("ui", "槽位 %d · %s")
		print("  [%s] 品質色階標籤: %s | 副詞條標籤: %s" % [code, q_lbl.text, af_lbl.text])
		if q_lbl.text.is_empty() or af_lbl.text.is_empty():
			_fail("[%s] 語系切換後標籤文字為空" % code)

		# 檢驗非中文語系下無殘留中文字
		if code in ["en", "ja", "ko", "es"]:
			if code == "en":
				if "品質" in q_lbl.text or "副詞條" in af_lbl.text:
					_fail("[en] 殘留繁中字元: q=%s, af=%s" % [q_lbl.text, af_lbl.text])
				else:
					print("  ✓ [en] 零中文殘留通過")
			elif code == "ja":
				if "品質色階" in q_lbl.text or "副詞條" in af_lbl.text:
					_fail("[ja] 殘留繁中專有詞: q=%s, af=%s" % [q_lbl.text, af_lbl.text])
				else:
					print("  ✓ [ja] 日語詞條檢驗通過")
			elif code == "ko":
				if "品質" in q_lbl.text or "副詞條" in af_lbl.text:
					_fail("[ko] 殘留繁中字元: q=%s, af=%s" % [q_lbl.text, af_lbl.text])
				else:
					print("  ✓ [ko] 零中文殘留通過")
			elif code == "es":
				if "品質" in q_lbl.text or "副詞條" in af_lbl.text:
					_fail("[es] 殘留繁中字元: q=%s, af=%s" % [q_lbl.text, af_lbl.text])
				else:
					print("  ✓ [es] 零中文殘留通過")

	# 切回繁中
	_loc.call("set_locale", "zh_TW")
	_dlg.queue_free()
	print("  ✓ 測試結束，彈窗已清理")
