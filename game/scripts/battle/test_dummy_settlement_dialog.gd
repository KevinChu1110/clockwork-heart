extends SceneTree
## 木人樁試招結算數據卡單元測試
## godot --headless -s res://scripts/battle/test_dummy_settlement_dialog.gd
##
## 守三件事：
##   1. BattleSim.make_dummy_fight + step 累積總傷害、耗時、計算 DPS
##   2. DummySettlementDialog 結算面板正確包含總傷害、耗時、DPS 欄位且數值對齊
##   3. 完成確認按鈕觸發回調與關閉

const BattleSim := preload("res://scripts/battle/battle_sim.gd")
const DummySettlementDialogScript := preload("res://scripts/battle/dummy_settlement_dialog.gd")


func _stats() -> Dictionary:
	return {
		"name": "測試勇者",
		"max_hp": 80,
		"hp": 80,
		"atk": 25,
		"def": 6,
		"speed": 12.0,
		"crit": 10.0,
		"crit_dmg": 50.0,
		"dmg_variance": 0.05,
		"can_skill": true,
		"slash_lv": 1,
		"weapon_class": "sword",
	}


func _initialize() -> void:
	var ok := true

	## 1. 檢驗 BattleSim 數據掛勾（步進 5 秒，木人受擊累積總傷害、耗時與 DPS）
	print("=== 檢驗 1: BattleSim.get_dummy_combat_stats ===")
	var sim := BattleSim.make_dummy_fight(_stats())
	var total_dt := 0.0
	while total_dt < 5.0 and not sim.finished:
		sim.step(0.1)
		total_dt += 0.1

	var combat_stats: Dictionary = sim.get_dummy_combat_stats()
	var total_dmg := int(combat_stats.get("total_damage", 0))
	var elapsed := float(combat_stats.get("elapsed_time", 0.0))
	var dps := float(combat_stats.get("dps", 0.0))

	if total_dmg <= 0:
		push_error("total_damage 應大於 0，得 %d" % total_dmg)
		ok = false
	else:
		print("  ok total_damage = %d" % total_dmg)

	if elapsed < 4.8 or elapsed > 5.2:
		push_error("elapsed_time 應約為 5.0 秒，得 %.2f" % elapsed)
		ok = false
	else:
		print("  ok elapsed_time = %.2f" % elapsed)

	var expected_dps := float(total_dmg) / elapsed
	if absf(dps - expected_dps) > 0.05:
		push_error("dps 應為 %.2f，得 %.2f" % [expected_dps, dps])
		ok = false
	else:
		print("  ok dps = %.2f" % dps)

	## 2. 檢驗 DummySettlementDialog 結算面板結構與欄位
	print("=== 檢驗 2: DummySettlementDialog 結構與數值 ===")
	var sample_stats := {
		"total_damage": 350,
		"elapsed_time": 10.0,
		"dps": 35.0,
	}

	var call_state := {"confirmed": false}
	var dlg: Control = DummySettlementDialogScript.show_dialog(
		root,
		sample_stats,
		func(): call_state["confirmed"] = true
	)

	if dlg == null:
		push_error("DummySettlementDialog 建立失敗")
		ok = false
	else:
		var dmg_card := dlg.find_child("TotalDamageCard", true, false)
		var time_card := dlg.find_child("ElapsedTimeCard", true, false)
		var dps_card := dlg.find_child("DpsCard", true, false)
		var confirm_btn: Button = dlg.find_child("ConfirmButton", true, false) as Button

		if dmg_card == null:
			push_error("結算面板缺少 TotalDamageCard（總傷害卡片）")
			ok = false
		else:
			print("  ok 找到 TotalDamageCard")

		if time_card == null:
			push_error("結算面板缺少 ElapsedTimeCard（耗時卡片）")
			ok = false
		else:
			print("  ok 找到 ElapsedTimeCard")

		if dps_card == null:
			push_error("結算面板缺少 DpsCard（DPS卡片）")
			ok = false
		else:
			print("  ok 找到 DpsCard")

		if confirm_btn == null:
			push_error("結算面板缺少 ConfirmButton（確認按鈕）")
			ok = false
		else:
			print("  ok 找到 ConfirmButton")

		# 檢驗欄位文字
		var dmg_val: Label = dlg.find_child("DamageValueLabel", true, false) as Label
		var time_val: Label = dlg.find_child("TimeValueLabel", true, false) as Label
		var dps_val: Label = dlg.find_child("DpsValueLabel", true, false) as Label

		if dmg_val == null or dmg_val.text != "350":
			push_error("DamageValueLabel 數值不符，期望 '350'，得 '%s'" % (dmg_val.text if dmg_val else "null"))
			ok = false
		else:
			print("  ok DamageValueLabel = 350")

		if time_val == null or time_val.text != "10.0":
			push_error("TimeValueLabel 數值不符，期望 '10.0'，得 '%s'" % (time_val.text if time_val else "null"))
			ok = false
		else:
			print("  ok TimeValueLabel = 10.0")

		if dps_val == null or dps_val.text != "35.0":
			push_error("DpsValueLabel 數值不符，期望 '35.0'，得 '%s'" % (dps_val.text if dps_val else "null"))
			ok = false
		else:
			print("  ok DpsValueLabel = 35.0")

		# 檢驗 getters
		if dlg.has_method("get_total_damage") and dlg.get_total_damage() != 350:
			push_error("get_total_damage() 得 %d" % dlg.get_total_damage())
			ok = false
		if dlg.has_method("get_elapsed_time") and absf(dlg.get_elapsed_time() - 10.0) > 0.001:
			push_error("get_elapsed_time() 得 %.2f" % dlg.get_elapsed_time())
			ok = false
		if dlg.has_method("get_dps") and absf(dlg.get_dps() - 35.0) > 0.001:
			push_error("get_dps() 得 %.2f" % dlg.get_dps())
			ok = false

		## 3. 檢驗確認按鈕點擊回調
		print("=== 檢驗 3: 確認按鈕點擊回調 ===")
		if confirm_btn != null:
			confirm_btn.pressed.emit()
			if not bool(call_state["confirmed"]):
				push_error("點擊確認按鈕未觸發 on_confirm 回調")
				ok = false
			else:
				print("  ok confirmed_called == true")

	if ok:
		print("DUMMY_SETTLEMENT_DIALOG_OK")
		quit(0)
	else:
		print("DUMMY_SETTLEMENT_DIALOG_FAIL")
		quit(1)
