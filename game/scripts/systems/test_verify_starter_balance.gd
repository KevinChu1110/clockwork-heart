extends SceneTree
## 無頭測試：斷言五族開局武器皆為 T1、effective_atk 不重複計算
## 執行指令：godot --path game --headless -s res://scripts/systems/test_verify_starter_balance.gd

func _initialize() -> void:
	print("== 測試五族開局武器 T1 規格與 effective_atk 運算 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if gs == null or eq == null:
		push_error("缺少 GameState 或 EquipmentSystem autoload")
		print("VERIFY_STARTER_BALANCE_FAIL")
		quit(1)
		return

	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	var expected_t1_ids = {
		"rabbit": "rusty_blade",
		"lion": "ash_spear",
		"fox": "star_rod",
		"boar": "anvil_hammer",
		"macaque": "wrap_gloves",
	}

	for r in races:
		gs.call("reset_new_game", r)
		var expected_id: String = str(expected_t1_ids[r])
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

		if base_tier != 1 or inst_tier != 1:
			push_error("%s 開局武器 %s 階級不為 T1 (base_tier=%d, inst_tier=%d)" % [r, base_id, base_tier, inst_tier])
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

		# 驗證沒有雙重累加 weapon_atk
		var base_char_atk: int = int(gs.atk)
		var w_atk: int = int(winst.get("rolled", {}).get("atk", 0))
		var wb: Dictionary = gs.weapon_class_bonuses()
		var class_atk: int = int(wb.get("atk", 0))
		var match_bonus: int = 2 if str(winst.get("line", "")) != "" and str(winst.get("line", "")) == gs._migrate_path_style(gs.path_style) else 0
		var expected_single_atk: int = base_char_atk + w_atk + class_atk + match_bonus
		if eff_atk != expected_single_atk:
			push_error("%s effective_atk (%d) != 預期單次疊加值 (%d) [base=%d, weapon=%d, class=%d, match=%d]" % [
				r, eff_atk, expected_single_atk, base_char_atk, w_atk, class_atk, match_bonus
			])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return

		# 驗證 legacy weapon_atk 不影響 effective_atk
		var orig_atk: int = int(gs.effective_atk())
		gs.weapon_atk = 999
		var tampered_atk: int = int(gs.effective_atk())
		if orig_atk != tampered_atk:
			push_error("%s 修改 legacy weapon_atk 導致 effective_atk 變動 (%d -> %d)，仍有 legacy 耦合" % [
				r, orig_atk, tampered_atk
			])
			print("VERIFY_STARTER_BALANCE_FAIL")
			quit(1)
			return
		gs.weapon_atk = w_atk

		# 驗證鍛造：鍛造成功一次後 effective_atk 必須比鍛造前大 (+2)
		gs.gold = 500
		gs.forge_fail_streak = 3
		var fs: Node = root.get_node_or_null("ForgeSystem")
		if fs != null:
			var forge_res: Dictionary = fs.call("try_forge")
			if not bool(forge_res.get("ok", false)):
				push_error("%s 鍛造保底應成功，但回傳失敗" % r)
				print("VERIFY_STARTER_BALANCE_FAIL")
				quit(1)
				return
			var post_forge_atk: int = int(gs.effective_atk())
			if post_forge_atk <= eff_atk:
				push_error("%s 鍛造後 effective_atk (%d) 未大於鍛造前 (%d)" % [r, post_forge_atk, eff_atk])
				print("VERIFY_STARTER_BALANCE_FAIL")
				quit(1)
				return
			if post_forge_atk != eff_atk + 2:
				push_error("%s 鍛造後 effective_atk 增量應為 2，實際為 %d -> %d" % [r, eff_atk, post_forge_atk])
				print("VERIFY_STARTER_BALANCE_FAIL")
				quit(1)
				return

		print("✓ %s 開局武器 %s (T%d, %s, ATK %d) | 實質 ATK: %d (鍛造後: %d)" % [
			r, base_id, inst_tier, str(winst.get("name", "")), w_atk, eff_atk, int(gs.effective_atk())
		])

	print("VERIFY_STARTER_BALANCE_OK")
	quit(0)
