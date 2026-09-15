extends SceneTree
## 無頭測試：斷言五族開局武器與起手技能、鍛造成功有效提升 effective_atk
## 執行指令：godot --path game --headless -s res://scripts/systems/test_verify_starter_balance.gd

func _initialize() -> void:
	print("== 測試五族開局武器規格、起手技能與鍛造有效性 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	var fs: Node = root.get_node_or_null("ForgeSystem")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if gs == null or eq == null:
		push_error("缺少 GameState 或 EquipmentSystem autoload")
		print("VERIFY_STARTER_BALANCE_FAIL")
		quit(1)
		return

	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	var expected_starters = {
		"rabbit": {"id": "dawn_blade", "tier": 5, "skill_id": "slash", "skill_name": "橫斬"},
		"lion": {"id": "knight_pike", "tier": 3, "skill_id": "line_thrust", "skill_name": "一線突刺"},
		"fox": {"id": "star_rod", "tier": 1, "skill_id": "magic_bolt", "skill_name": "魔彈"},
		"boar": {"id": "anvil_hammer", "tier": 1, "skill_id": "stone_crush", "skill_name": "碎岩鎚"},
		"macaque": {"id": "hunt_claw", "tier": 3, "skill_id": "claw_rake", "skill_name": "裂爪"},
	}

	for r in races:
		gs.call("reset_new_game", r)
		var exp_info: Dictionary = expected_starters[r]
		var expected_id: String = str(exp_info["id"])
		var expected_tier: int = int(exp_info["tier"])
		var assigned_id_gs: String = str(gs.RACE_STARTER_WEAPONS.get(r, ""))
		var assigned_id_eq: String = str(eq.starter_weapon_id_for_race(r))

		if assigned_id_gs != expected_id:
			push_error("GameState.RACE_STARTER_WEAPONS[%s] 應為 %s，實際為 %s" % [r, expected_id, assigned_id_gs])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		if assigned_id_eq != expected_id:
			push_error("EquipmentSystem.starter_weapon_id_for_race(%s) 應為 %s，實際為 %s" % [r, expected_id, assigned_id_eq])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		var wuid: String = str(gs.equip_slots.get("weapon", ""))
		if wuid.is_empty() or not gs.equip_worn.has(wuid):
			push_error("%s 開局未正確裝備武器" % r)
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		var winst: Dictionary = gs.equip_worn[wuid]
		var base_id: String = str(winst.get("base_id", ""))
		var bdef: Dictionary = eq.base_def(base_id)
		var base_tier: int = int(bdef.get("tier", 0))
		var inst_tier: int = int(winst.get("tier", 0))

		if base_tier != expected_tier or inst_tier != expected_tier:
			push_error("%s 開局武器 %s 階級不為 T%d (base_tier=%d, inst_tier=%d)" % [r, base_id, expected_tier, base_tier, inst_tier])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		# 驗證 effective_atk 計算與 BattleSim.gather_player_stats 一致
		var stats: Dictionary = BattleSim.gather_player_stats()
		var eff_atk: int = int(gs.effective_atk())
		var sim_atk: int = int(stats.get("atk", 0))
		if eff_atk != sim_atk:
			push_error("%s effective_atk (%d) 與 BattleSim stats.atk (%d) 不一致" % [r, eff_atk, sim_atk])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		# 驗證 weapon_atk 正確計入 effective_atk（鍛造系統數值出口）
		var atk_before: int = int(gs.effective_atk())
		gs.weapon_atk += 2
		var atk_after: int = int(gs.effective_atk())
		if atk_after != atk_before + 2:
			push_error("%s weapon_atk 增加 2 點後 effective_atk 未相應增加" % r)
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		gs.weapon_atk -= 2

		var w_atk: int = int(winst.get("rolled", {}).get("atk", 0))
		print("✓ %s 開局武器 %s (T%d, %s, ATK %d) | 實質 ATK: %d" % [
			r, base_id, inst_tier, str(winst.get("name", "")), w_atk, eff_atk
		])

		# 驗證五族開局皆已習得對應武器線起手技能，且 can_skill 皆為 true
		var can_sk: bool = bool(stats.get("can_skill", false))
		var sk_id: String = str(stats.get("skill_id", ""))
		var sk_name: String = str(stats.get("skill_name", ""))
		var sk_mult: float = float(stats.get("skill_mult", 0.0))
		var sk_hits: int = int(stats.get("skill_hits", 1))
		if not can_sk:
			push_error("%s 開局 can_skill 為 false，滿怒無法放技能" % r)
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		if sk_id.is_empty():
			push_error("%s 開局缺少對應武器線技能 id" % r)
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		var exp_sk_id: String = str(exp_info["skill_id"])
		if sk_id != exp_sk_id:
			push_error("%s 開局技能 id 預期為 %s，實際為 %s" % [r, exp_sk_id, sk_id])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		var total_mult: float = sk_mult * float(sk_hits)
		print("✓ %s 開局技能: [%s] %s | 單段倍率: %.2f (段數: %d, 總倍率: %.2f) | can_skill: %s" % [
			r, sk_id, sk_name, sk_mult, sk_hits, total_mult, str(can_sk)
		])

	# 鍛造系統完整升階流程驗證（保底必定成功升階，驗證 effective_atk 提升）
	if fs and fs.has_method("try_forge"):
		gs.reset_new_game("rabbit")
		gs.gold = 500
		var pre_tier: int = int(gs.weapon_tier)
		var pre_watk: int = int(gs.weapon_atk)
		var pre_eff_atk: int = int(gs.effective_atk())
		gs.forge_fail_streak = 3 # 觸發保底必定成功
		var f_res: Dictionary = fs.call("try_forge")
		if not bool(f_res.get("ok", false)):
			push_error("ForgeSystem 保底鍛造失敗: %s" % str(f_res))
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		var post_tier: int = int(gs.weapon_tier)
		var post_watk: int = int(gs.weapon_atk)
		var post_eff_atk: int = int(gs.effective_atk())
		if post_tier != pre_tier + 1:
			push_error("ForgeSystem 鍛造後 tier 未 +1 (%d -> %d)" % [pre_tier, post_tier])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		if post_watk != pre_watk + 2:
			push_error("ForgeSystem 鍛造後 weapon_atk 未 +2 (%d -> %d)" % [pre_watk, post_watk])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		if post_eff_atk != pre_eff_atk + 2:
			push_error("ForgeSystem 鍛造後 effective_atk 未上升 2 點 (%d -> %d)" % [pre_eff_atk, post_eff_atk])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		print("✓ 鍛造升階驗證成功：tier %d -> %d, weapon_atk %d -> %d, effective_atk %d -> %d" % [
			pre_tier, post_tier, pre_watk, post_watk, pre_eff_atk, post_eff_atk
		])

	print("\nVERIFY_STARTER_BALANCE_OK")
	quit(0)
