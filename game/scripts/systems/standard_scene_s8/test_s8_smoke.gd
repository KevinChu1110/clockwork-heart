extends SceneTree
## Wave-2 §8 無頭煙測：探索→戰鬥→拆一部位。
## godot --path game --headless -s res://scripts/systems/standard_scene_s8/test_s8_smoke.gd

const S8SmokeFlowScript := preload("res://scripts/systems/standard_scene_s8/s8_smoke_flow.gd")
const WindStaminaScript := preload("res://scripts/systems/wind_stamina/wind_stamina.gd")
const ChestGlowHudScript := preload("res://scripts/systems/wind_stamina/chest_glow_hud.gd")


func _initialize() -> void:
	print("== W2 §8 smoke (explore→combat→dismantle) ==")
	var ok := true

	var wind: WindStamina = WindStaminaScript.new()
	wind.load_defaults()
	if wind.data_id != "W2-K1":
		push_error("expected W2-K1 id")
		ok = false
	if wind.max_stamina != 15:
		push_error("WindStaminaMax != 15")
		ok = false
	if wind.cost_of("E02_exploreTick") != 1 or wind.cost_of("B01_combatEnter") != 2:
		push_error("cost table mismatch")
		ok = false
	if not is_equal_approx(wind.part_unlock_hp(), 0.70):
		push_error("PartUnlockHP != 0.70")
		ok = false
	if wind.hud_style() != "chest_glow_ring_ticks":
		push_error("HUD style must be chest_glow_ring_ticks")
		ok = false
	if not wind.hud_forbids_blue_mana():
		push_error("HUD must forbid blue_mana_bar + second_resource_bar")
		ok = false
	print("  ok - W2-K1 constants loaded")

	# HUD 可實例化（無藍條 ProgressBar）
	var hud: ChestGlowHud = ChestGlowHudScript.new()
	root.add_child(hud)
	hud.setup(wind)
	if hud.get_child_count() > 0:
		# 允許空；禁止自己長出 ProgressBar
		for c in hud.get_children():
			if c is ProgressBar:
				push_error("ChestGlowHud must not contain ProgressBar")
				ok = false
	print("  ok - ChestGlowHud (glow+ticks, no mana bar)")

	var flow: S8SmokeFlow = S8SmokeFlowScript.new()
	var result: Dictionary = flow.run_to_completion()
	print("  result: ", result)
	if not bool(result.get("ok", false)):
		push_error("flow failed: %s" % str(result.get("summary", "")))
		ok = false
	if not bool(result.get("part_broken", false)):
		push_error("expected one part broken")
		ok = false
	if not bool(result.get("part_unlocked", false)):
		push_error("expected part unlock")
		ok = false
	var loot: Array = result.get("loot", []) as Array
	if loot.is_empty() or str(loot[0]) != "drop_brass_gear":
		push_error("expected drop_brass_gear, got %s" % str(loot))
		ok = false
	# 花費下限：explore1 + combatEnter2 + ≥1 strike + dismantle2 + pull1
	var spent := int(result.get("max", 15)) - int(result.get("wind", 0))
	if spent < 6:
		push_error("expected WindStamina drain ≥6, spent=%d" % spent)
		ok = false
	print("  ok - flow E→B→D loot=%s wind_left=%s spent=%d" % [str(loot), str(result.get("wind")), spent])

	# Bingo W4 對白 key（e02_hud / b02_hint）必須存在且無藍條用語
	var d_e02 := str(result.get("dialog_e02", ""))
	var d_b02 := str(result.get("dialog_b02", ""))
	if d_e02.find("發條") < 0:
		push_error("s8.e02_hud missing 發條 wording")
		ok = false
	if d_b02.find("拆") < 0:
		push_error("s8.b02_hint should guide dismantle")
		ok = false
	for bad in ["藍條", "mana", "能量條"]:
		if d_e02.find(bad) >= 0 or d_b02.find(bad) >= 0:
			push_error("dialog must not contain %s" % bad)
			ok = false
	# 糖果屑腳本可載入
	var candy_path := "res://scripts/systems/candy_chip_vfx/candy_chip_vfx.gd"
	if not ResourceLoader.exists(candy_path):
		push_error("CandyChipVfx missing")
		ok = false
	else:
		print("  ok - CandyChipVfx + Bingo dialogue keys")


	# battle_sim 既有門檻對齊（常數旁註，不重寫 battle_sim）
	const BattleSim := preload("res://scripts/battle/battle_sim.gd")
	if not is_equal_approx(BattleSim.PART_BREAK_HP_RATIO, 0.70):
		push_error("battle_sim PART_BREAK_HP_RATIO should stay 0.70 (Ken PartUnlockHP)")
		ok = false
	else:
		print("  ok - battle_sim.PART_BREAK_HP_RATIO=0.70 aligned")

	if ok:
		print("S8_SMOKE_SUCCESS")
		quit(0)
	else:
		print("S8_SMOKE_FAIL")
		quit(1)
