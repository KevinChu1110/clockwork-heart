extends SceneTree
## 無頭測試：武術館兵器架流派快捷切換與招式預覽

func _initialize() -> void:
	print("== 測試武術館兵器架流派快捷切換與招式預覽 ==")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	var sk = root.get_node_or_null("SkillSystem")
	var dt = root.get_node_or_null("DataTables")
	if gs == null or eq == null or sk == null or dt == null:
		push_error("autoload missing")
		quit(1)
		return

	gs.reset_new_game()
	dt.reload()
	eq._ensure_state()
	sk.ensure_skill_map()
	gs.level = 16  ## 解鎖全部 3 個武器欄位

	# 1. 驗證初始 summary 結構
	var summary: Dictionary = eq.get_weapon_wall_summary()
	assert(summary.has("loadouts"), "summary 應有 loadouts")
	assert(summary.has("active_index"), "summary 應有 active_index")
	assert(summary.has("styles"), "summary 應有 styles")

	var loadouts: Array = summary.get("loadouts", [])
	assert(loadouts.size() == 3, "應有 3 個武器欄位，實際 %d" % loadouts.size())

	for lo in loadouts:
		assert(bool(lo.get("unlocked", false)), "Lv16 應皆已解鎖")

	# 2. 準備兩把測試武器：劍與斧
	var w_sword: Dictionary = {
		"uid": "wall_test_sword",
		"base_id": "test_sword",
		"name": "青鋼短劍",
		"slot": "weapon",
		"tier": 1,
		"line": "sword",
		"quality": "common",
		"quality_label": "凡",
		"rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
	}
	var w_axe: Dictionary = {
		"uid": "wall_test_axe",
		"base_id": "test_axe",
		"name": "破陣戰斧",
		"slot": "weapon",
		"tier": 1,
		"line": "axe",
		"quality": "common",
		"quality_label": "凡",
		"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
	}

	gs.equip_bag = [w_sword, w_axe]
	gs.equip_worn = {}
	gs.weapon_loadout = ["", "", ""]
	gs.weapon_loadout_active = 0
	gs.equip_slots["weapon"] = ""

	# 裝備至欄位 0 與欄位 1
	var r0: Dictionary = eq.equip_weapon_to_loadout("wall_test_sword", 0)
	assert(bool(r0.get("ok", false)), "裝備欄位 0 應成功")
	var r1: Dictionary = eq.equip_weapon_to_loadout("wall_test_axe", 1)
	assert(bool(r1.get("ok", false)), "裝備欄位 1 應成功")

	# 切換至欄位 0
	eq.switch_weapon_loadout(0)

	# 3. 檢查 summary 中的武器欄位資料與流派
	var sum_equipped: Dictionary = eq.get_weapon_wall_summary()
	var lo_eq: Array = sum_equipped.get("loadouts", [])
	assert(str(lo_eq[0].get("uid", "")) == "wall_test_sword", "欄位 0 應為青鋼短劍")
	assert(str(lo_eq[0].get("line", "")) == "sword", "欄位 0 流派應為 sword")
	assert(str(lo_eq[0].get("line_name", "")) == "劍", "欄位 0 流派名應為 劍")
	assert(bool(lo_eq[0].get("is_active", false)), "欄位 0 應為 active")

	assert(str(lo_eq[1].get("uid", "")) == "wall_test_axe", "欄位 1 應為破陣戰斧")
	assert(str(lo_eq[1].get("line", "")) == "axe", "欄位 1 流派應為 axe")
	assert(str(lo_eq[1].get("line_name", "")) == "斧", "欄位 1 流派名應為 斧")
	assert(not bool(lo_eq[1].get("is_active", true)), "欄位 1 應非 active")

	# 4. 呼叫 EquipmentSystem.switch_weapon_loadout 切換當前武器
	var sw_res: Dictionary = eq.switch_weapon_loadout(1)
	assert(bool(sw_res.get("ok", false)), "切換至欄位 1 應成功")
	assert(int(gs.weapon_loadout_active) == 1, "當前 active 應為 1")
	assert(str(gs.path_style) == "axe", "切換後流派應跟隨武器變為 axe")

	var sum_switched: Dictionary = eq.get_weapon_wall_summary()
	var lo_sw: Array = sum_switched.get("loadouts", [])
	assert(int(sum_switched.get("active_index", -1)) == 1, "summary active_index 應為 1")
	assert(not bool(lo_sw[0].get("is_active", true)), "欄位 0 應非 active")
	assert(bool(lo_sw[1].get("is_active", false)), "欄位 1 應為 active")

	# 5. 驗證 12 種武器流派起手招式與熟練狀態預覽
	var styles: Array = sum_switched.get("styles", [])
	assert(styles.size() == 12, "武器流派應恰好為 12 種，實際 %d" % styles.size())

	var expected_classes := {
		"sword": {"name": "劍", "sig": "slash", "sig_name": "橫斬"},
		"spear": {"name": "長槍", "sig": "line_thrust", "sig_name": "一線突刺"},
		"axe": {"name": "斧", "sig": "axe_split", "sig_name": "劈砍"},
		"hammer": {"name": "鎚", "sig": "stone_crush", "sig_name": "碎岩鎚"},
		"dagger": {"name": "匕首", "sig": "quick_stab", "sig_name": "急刺"},
		"dart": {"name": "鏢", "sig": "mist_needle", "sig_name": "霧影鏢"},
		"fist": {"name": "拳", "sig": "combo_fist", "sig_name": "連環拳"},
		"claw": {"name": "爪", "sig": "claw_rake", "sig_name": "裂爪"},
		"magic": {"name": "杖", "sig": "magic_bolt", "sig_name": "魔彈"},
		"crystal": {"name": "水晶", "sig": "shard_bolt", "sig_name": "晶屑彈"},
		"bow": {"name": "弓", "sig": "quick_shot", "sig_name": "速射"},
		"gun": {"name": "火槍", "sig": "powder_shot", "sig_name": "火銃點射"},
	}

	var found_keys := {}
	for st in styles:
		var sid: String = str(st.get("id", ""))
		assert(expected_classes.has(sid), "未知流派 id: %s" % sid)
		found_keys[sid] = true

		var exp: Dictionary = expected_classes[sid]
		assert(str(st.get("name", "")) == exp["name"], "流派名稱不符: %s vs %s" % [st.get("name", ""), exp["name"]])
		assert(str(st.get("signature_id", "")) == exp["sig"], "起手招式 id 不符: %s" % sid)
		assert(str(st.get("signature_name", "")) == exp["sig_name"], "起手招式名稱不符: %s" % sid)
		assert(st.has("mastery_text"), "應具備熟練狀態文字")
		assert(st.has("level"), "應具備等級")
		assert(st.has("mastery"), "應具備熟練點數")

		# 驗證當前流派標記
		if sid == "axe":
			assert(bool(st.get("is_current_path", false)), "axe 應為當前流派")
		else:
			assert(not bool(st.get("is_current_path", true)), "%s 應非當前流派" % sid)

	assert(found_keys.size() == 12, "12 種流派應全數涵蓋")

	# 6. 測試熟練度變更與反映
	sk.learn("axe_split", 1)
	sk.add_mastery("axe_split", 15)
	var sum_mastery: Dictionary = eq.get_weapon_wall_summary()
	for st in sum_mastery.get("styles", []):
		if str(st.get("id", "")) == "axe":
			assert(bool(st.get("learned", false)), "axe 起手式應已習得")
			assert(int(st.get("level", 0)) == 1, "axe 起手式等級應為 1")
			assert(int(st.get("mastery", 0)) == 15, "axe 起手式熟練度應為 15")
			assert("15" in str(st.get("mastery_text", "")), "熟練度文字應包含 15")

	# 7. 驗證 town_tutor 中 weapon_wall 實體存在
	var MapCatalogClass = load("res://scripts/world/map_catalog.gd")
	var tutor_map: Dictionary = MapCatalogClass._town_tutor()
	var wall_found := false
	for ent in tutor_map.get("entities", []):
		if str(ent.get("id", "")) == "weapon_wall":
			wall_found = true
			assert(str(ent.get("label", "")) == "兵器牆", "weapon_wall 標籤應為 兵器牆")
			break
	assert(wall_found, "town_tutor 中必須有 weapon_wall 實體")

	print("WEAPON_WALL_OK")
	quit(0)
