extends SceneTree
## 無頭測試：斷言鍛造成功後 effective_atk 必大於鍛造前，且鍛造前後 effective_atk 與面板顯示值一致
## 執行指令：godot --path game --headless -s res://scripts/systems/test_verify_forge_effective_atk.gd

func _initialize() -> void:
	print("== 測試天宮鐵匠鍛造與 effective_atk 增益一致性 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var eq: Node = root.get_node_or_null("EquipmentSystem")
	var fs: Node = root.get_node_or_null("ForgeSystem")
	var dt: Node = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if gs == null or eq == null or fs == null:
		push_error("缺少 GameState、EquipmentSystem 或 ForgeSystem autoload")
		print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
		quit(1)
		return

	var ForgeDialogScript = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogScript == null:
		push_error("無法載入 forge_dialog.gd")
		print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
		quit(1)
		return

	var races = ["rabbit", "lion", "fox", "boar", "macaque"]
	print("\n| 種族 | 武器 (T1) | 鍛造前面板 | 鍛造前 effective_atk | 鍛造後面板 | 鍛造後 effective_atk | ATK Delta | 判定 |")
	print("|---|---|---|---|---|---|---|---|")

	for r in races:
		gs.call("reset_new_game", r)
		var wuid: String = str(gs.equip_slots.get("weapon", ""))
		if wuid.is_empty() or not gs.equip_worn.has(wuid):
			push_error("%s 開局未正確裝備武器" % r)
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		var winst_pre: Dictionary = gs.equip_worn[wuid]
		var wname: String = str(winst_pre.get("name", "武器"))
		var pre_weapon_atk: int = int(winst_pre.get("rolled", {}).get("atk", 0))
		var pre_eff_atk: int = int(gs.effective_atk())
		var pre_tier: int = int(gs.weapon_tier)

		# 實例化 ForgeDialog 檢驗面板取值方法
		var dialog = ForgeDialogScript.new()
		var pre_panel_atk: int = int(dialog._current_weapon_atk())
		dialog.free()

		if pre_panel_atk != pre_weapon_atk:
			push_error("%s 鍛造前面板顯示值 (%d) 與武器實例 rolled.atk (%d) 不一致" % [r, pre_panel_atk, pre_weapon_atk])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		# 準備鍛造資源與保底
		gs.gold = 500
		gs.forge_fail_streak = 3 # 觸發連敗保底，確保鍛造成功
		var forge_res: Dictionary = fs.try_forge()
		if not bool(forge_res.get("ok", false)):
			push_error("%s 鍛造保底應成功，但回傳: %s" % [r, str(forge_res)])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		var winst_post: Dictionary = gs.equip_worn[wuid]
		var post_weapon_atk: int = int(winst_post.get("rolled", {}).get("atk", 0))
		var post_eff_atk: int = int(gs.effective_atk())
		var post_tier: int = int(gs.weapon_tier)

		var dialog_post = ForgeDialogScript.new()
		var post_panel_atk: int = int(dialog_post._current_weapon_atk())
		dialog_post.free()

		var delta_eff: int = post_eff_atk - pre_eff_atk
		var delta_panel: int = post_panel_atk - pre_panel_atk

		# 核心斷言 1：鍛造成功一次後 effective_atk 必須比鍛造前大
		if post_eff_atk <= pre_eff_atk:
			push_error("%s 鍛造後 effective_atk (%d) 未大於鍛造前 (%d)！delta=%d" % [r, post_eff_atk, pre_eff_atk, delta_eff])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		# 核心斷言 2：鍛造增加值必須為 +2
		if delta_eff != 2:
			push_error("%s effective_atk 增量應為 2，實際為 %d (%d -> %d)" % [r, delta_eff, pre_eff_atk, post_eff_atk])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		# 核心斷言 3：面板顯示值必須與真實武器攻擊完全一致
		if post_panel_atk != post_weapon_atk:
			push_error("%s 鍛造後面板顯示值 (%d) 與武器實例 rolled.atk (%d) 不一致" % [r, post_panel_atk, post_weapon_atk])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		# 核心斷言 4：面板增量與 effective_atk 增量必須完全一致
		if delta_panel != delta_eff:
			push_error("%s 面板增量 (%d) 與 effective_atk 增量 (%d) 不一致" % [r, delta_panel, delta_eff])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		# 核心斷言 5：器階必須 +1
		if post_tier != pre_tier + 1:
			push_error("%s 器階未提升 (%d -> %d)" % [r, pre_tier, post_tier])
			print("VERIFY_FORGE_EFFECTIVE_ATK_FAIL")
			quit(1)
			return

		print("| %s | %s | +%d | %d | +%d | %d | +%d | PASS |" % [
			r, wname, pre_panel_atk, pre_eff_atk, post_panel_atk, post_eff_atk, delta_eff
		])

	print("\n所有種族鍛造後 effective_atk 均正確成長且與面板顯示值完全一致！")
	print("VERIFY_FORGE_EFFECTIVE_ATK_OK")
	quit(0)
