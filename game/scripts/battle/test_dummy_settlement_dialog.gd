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

	## 2. 檢驗 DummySettlementDialog 結算面板結構與欄位（雙按鈕並列）
	print("=== 檢驗 2: DummySettlementDialog 結構與數值 ===")
	var sample_stats := {
		"total_damage": 350,
		"elapsed_time": 10.0,
		"dps": 35.0,
	}

	var call_state := {
		"confirmed": false,
		"retried": false,
		"signal_confirmed": false,
		"signal_retried": false,
	}
	var dlg: Control = DummySettlementDialogScript.show_dialog(
		root,
		sample_stats,
		func(): call_state["confirmed"] = true,
		func(): call_state["retried"] = true
	)

	if dlg == null:
		push_error("DummySettlementDialog 建立失敗")
		ok = false
	else:
		dlg.confirmed.connect(func(): call_state["signal_confirmed"] = true)
		dlg.retry_requested.connect(func(): call_state["signal_retried"] = true)

		var dmg_card := dlg.find_child("TotalDamageCard", true, false)
		var time_card := dlg.find_child("ElapsedTimeCard", true, false)
		var dps_card := dlg.find_child("DpsCard", true, false)
		var retry_btn: Button = dlg.find_child("RetryButton", true, false) as Button
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

		if retry_btn == null:
			push_error("結算面板缺少 RetryButton（再次試招按鈕）")
			ok = false
		else:
			print("  ok 找到 RetryButton")
			if retry_btn.custom_minimum_size.y < 48:
				push_error("RetryButton 高度應 >= 48px，得 %.1f" % retry_btn.custom_minimum_size.y)
				ok = false
			else:
				print("  ok RetryButton 高度 >= 48px (%.1fpx)" % retry_btn.custom_minimum_size.y)
			if retry_btn.text != "再次試招":
				push_error("RetryButton 文字應為 '再次試招'，得 '%s'" % retry_btn.text)
				ok = false
			else:
				print("  ok RetryButton 文字為 '再次試招'")

		if confirm_btn == null:
			push_error("結算面板缺少 ConfirmButton（確認按鈕）")
			ok = false
		else:
			print("  ok 找到 ConfirmButton")
			if confirm_btn.custom_minimum_size.y < 48:
				push_error("ConfirmButton 高度應 >= 48px，得 %.1f" % confirm_btn.custom_minimum_size.y)
				ok = false
			else:
				print("  ok ConfirmButton 高度 >= 48px (%.1fpx)" % confirm_btn.custom_minimum_size.y)
			if confirm_btn.text != "完成試招":
				push_error("ConfirmButton 文字應為 '完成試招'，得 '%s'" % confirm_btn.text)
				ok = false
			else:
				print("  ok ConfirmButton 文字為 '完成試招'")

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
		if dlg.has_method("get_retry_text") and dlg.get_retry_text() != "再次試招":
			push_error("get_retry_text() 得 '%s'" % dlg.get_retry_text())
			ok = false
		if dlg.has_method("get_confirm_text") and dlg.get_confirm_text() != "完成試招":
			push_error("get_confirm_text() 得 '%s'" % dlg.get_confirm_text())
			ok = false

		## 3. 檢驗再次試招與確認按鈕回調與信號
		print("=== 檢驗 3: 雙按鈕回調與信號發送 ===")
		# 檢驗 retry 按鈕
		if retry_btn != null:
			retry_btn.pressed.emit()
			if not bool(call_state["retried"]):
				push_error("點擊再次試招未觸發 on_retry 回調")
				ok = false
			else:
				print("  ok retried_called == true")
			if not bool(call_state["signal_retried"]):
				push_error("點擊再次試招未發出 retry_requested 信號")
				ok = false
			else:
				print("  ok retry_requested signal emitted == true")

		# 檢驗 confirm 按鈕 (使用新 instance)
		var call_state_conf := {"confirmed": false, "signal_confirmed": false}
		var dlg_conf: Control = DummySettlementDialogScript.show_dialog(
			root,
			sample_stats,
			func(): call_state_conf["confirmed"] = true
		)
		dlg_conf.confirmed.connect(func(): call_state_conf["signal_confirmed"] = true)
		var conf_btn2: Button = dlg_conf.find_child("ConfirmButton", true, false) as Button
		if conf_btn2 != null:
			conf_btn2.pressed.emit()
			if not bool(call_state_conf["confirmed"]):
				push_error("點擊確認按鈕未觸發 on_confirm 回調")
				ok = false
			else:
				print("  ok confirmed_called == true")
			if not bool(call_state_conf["signal_confirmed"]):
				push_error("點擊確認按鈕未發出 confirmed 信號")
				ok = false
			else:
				print("  ok confirmed signal emitted == true")

	## 4. 檢驗再次試招重置狀態與重新計時/刷新木人樁血量
	print("=== 檢驗 4: 木人樁狀態重置與重新試招驗證 ===")
	var sim_run := BattleSim.make_dummy_fight(_stats())
	for _i in range(50):
		sim_run.step(0.1)
	var stats_run := sim_run.get_dummy_combat_stats()
	var run_dmg := int(stats_run.get("total_damage", 0))
	var dummy_unit := sim_run.get_unit("training_dummy")
	if run_dmg <= 0 or dummy_unit.hp >= dummy_unit.max_hp:
		push_error("試招進行中木人樁應已受損，得 hp=%d/%d, total_damage=%d" % [dummy_unit.hp, dummy_unit.max_hp, run_dmg])
		ok = false
	else:
		print("  ok 試招前段傷害累積 hp=%d/%d, total_damage=%d" % [dummy_unit.hp, dummy_unit.max_hp, run_dmg])

	# 模擬觸發再次試招：重新建立試招 fight
	var sim_re := BattleSim.make_dummy_fight(_stats())
	var dummy_re := sim_re.get_unit("training_dummy")
	var stats_re := sim_re.get_dummy_combat_stats()
	if dummy_re.hp != dummy_re.max_hp or dummy_re.hp != 500:
		push_error("再次試招木人樁 HP 應刷新為 500 滿血，得 %d" % dummy_re.hp)
		ok = false
	else:
		print("  ok 再次試招木人樁 HP 刷新為滿血 500")

	if float(stats_re.get("elapsed_time", 0.0)) != 0.0 or int(stats_re.get("total_damage", 0)) != 0:
		push_error("再次試招計時與傷害應歸零，得 time=%.2f, dmg=%d" % [float(stats_re.get("elapsed_time", 0.0)), int(stats_re.get("total_damage", 0))])
		ok = false
	else:
		print("  ok 再次試招計時與總傷害成功重置歸零 (time=0.0, dmg=0)")

	for _i in range(50):
		sim_re.step(0.1)
	var stats_re2 := sim_re.get_dummy_combat_stats()
	if int(stats_re2.get("total_damage", 0)) <= 0 or float(stats_re2.get("elapsed_time", 0.0)) < 4.8:
		push_error("再次試招重新開打後應正常累計數值，得 dmg=%d, time=%.2f" % [int(stats_re2.get("total_damage", 0)), float(stats_re2.get("elapsed_time", 0.0))])
		ok = false
	else:
		print("  ok 再次試招重新開打正常運作 (time=%.2fs, dmg=%d)" % [float(stats_re2.get("elapsed_time", 0.0)), int(stats_re2.get("total_damage", 0))])

	if ok:
		print("DUMMY_SETTLEMENT_DIALOG_OK")
		quit(0)
	else:
		print("DUMMY_SETTLEMENT_DIALOG_FAIL")
		quit(1)
