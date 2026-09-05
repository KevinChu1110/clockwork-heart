extends SceneTree
## 無頭測試：鐵匠鋪廢鐵桶拆解多餘裝備回收為鐵屑與金幣
## 執行指令：godot --path game --headless -s res://scripts/systems/test_equipment_dismantle.gd

func _initialize() -> void:
	print("== 測試裝備拆解與廢鐵桶回收 ==")
	var eq = root.get_node_or_null("EquipmentSystem")
	var gs = root.get_node_or_null("GameState")
	var inv = root.get_node_or_null("InventorySystem")
	var dt = root.get_node_or_null("DataTables")
	if dt and dt.has_method("reload"):
		dt.call("reload")

	if eq == null or gs == null or inv == null:
		push_error("缺少必要的 Autoload 節點")
		print("EQUIPMENT_DISMANTLE_FAIL")
		quit(1)
		return

	test_dismantle_yield(eq)
	test_dismantle_success(eq, gs, inv)
	test_dismantle_cannot_dismantle_equipped(eq, gs, inv)
	test_dismantle_invalid_uid(eq, gs, inv)
	test_scrap_bin_interaction_contract()

	print("EQUIPMENT_DISMANTLE_OK")
	quit(0)


## 1. 測試收益預覽與數值規則
func test_dismantle_yield(eq: Node) -> void:
	# 空裝備
	var empty_y: Dictionary = eq.dismantle_yield({})
	assert(int(empty_y.get("iron_scrap", -1)) == 0, "空裝備鐵屑應為 0")
	assert(int(empty_y.get("gold", -1)) == 0, "空裝備金幣應為 0")

	# T1 凡品 (tier=1, quality="common")
	var t1_common := {"tier": 1, "quality": "common"}
	var y1: Dictionary = eq.dismantle_yield(t1_common)
	assert(int(y1.get("iron_scrap", 0)) == 1, "T1 凡品應回收 1 個鐵屑")
	assert(int(y1.get("gold", 0)) == 15, "T1 凡品應回收 15 金幣")

	# T1 良品 (tier=1, quality="uncommon")
	var t1_uncommon := {"tier": 1, "quality": "uncommon"}
	var y2: Dictionary = eq.dismantle_yield(t1_uncommon)
	assert(int(y2.get("iron_scrap", 0)) == 2, "T1 良品應回收 2 個鐵屑")
	assert(int(y2.get("gold", 0)) == 25, "T1 良品應回收 25 金幣")

	# T2 上品 (tier=2, quality="rare")
	var t2_rare := {"tier": 2, "quality": "rare"}
	var y3: Dictionary = eq.dismantle_yield(t2_rare)
	assert(int(y3.get("iron_scrap", 0)) == 4, "T2 上品應回收 4 個鐵屑 (2 + 2)")
	assert(int(y3.get("gold", 0)) == 55, "T2 上品應回收 55 金幣 (30 + 25)")

	# T3 秘寶 (tier=3, quality="epic")
	var t3_epic := {"tier": 3, "quality": "epic"}
	var y4: Dictionary = eq.dismantle_yield(t3_epic)
	assert(int(y4.get("iron_scrap", 0)) == 6, "T3 秘寶應回收 6 個鐵屑 (3 + 3)")
	assert(int(y4.get("gold", 0)) == 95, "T3 秘寶應回收 95 金幣 (45 + 50)")

	print("  ok - dismantle_yield 數值規則正確")


## 2. 測試成功拆解背包中的裝備
func test_dismantle_success(eq: Node, gs: Node, inv: Node) -> void:
	gs.reset_new_game()
	gs.equip_bag = []
	gs.gold = 100

	# 產生一件 T1 凡品裝備並加入背包
	var inst: Dictionary = eq.roll_instance("rusty_blade", "common")
	assert(not inst.is_empty(), "裝備生成失敗")
	var uid: String = str(inst.get("uid", ""))
	eq.add_to_bag(inst)
	assert(eq.find_bag(uid).is_empty() == false, "裝備應在背包中")

	var prev_scrap: int = inv.count("iron_scrap")
	var prev_gold: int = gs.gold

	var yield_val: Dictionary = eq.dismantle_yield(inst)
	var exp_scrap: int = int(yield_val.get("iron_scrap", 0))
	var exp_gold: int = int(yield_val.get("gold", 0))

	var res: Dictionary = eq.dismantle(uid)
	assert(bool(res.get("ok", false)), "拆解應成功: %s" % res)
	assert(int(res.get("iron_scrap", 0)) == exp_scrap, "回傳鐵屑數量相符")
	assert(int(res.get("gold", 0)) == exp_gold, "回傳金幣數量相符")

	# 驗證背包已移除該裝備
	assert(eq.find_bag(uid).is_empty(), "拆解後裝備應已自背包中移除")
	# 驗證資源增加
	assert(inv.count("iron_scrap") == prev_scrap + exp_scrap, "鐵屑數量應增加")
	assert(gs.gold == prev_gold + exp_gold, "金幣數量應增加")

	print("  ok - dismantle 成功回收未裝備的裝備並發放鐵屑與金幣")


## 3. 測試裝備中的裝備不可拆解（安全守門）
func test_dismantle_cannot_dismantle_equipped(eq: Node, gs: Node, inv: Node) -> void:
	gs.reset_new_game()
	gs.equip_bag = []

	# 產生裝備並穿上
	var inst: Dictionary = eq.roll_instance("rusty_blade", "common")
	var uid: String = str(inst.get("uid", ""))
	eq.add_to_bag(inst)
	var er: Dictionary = eq.equip(uid)
	assert(bool(er.get("ok", false)), "穿裝備應成功")
	assert(gs.equip_worn.has(uid), "裝備應在 equip_worn")

	var prev_scrap: int = inv.count("iron_scrap")
	var prev_gold: int = gs.gold

	# 嘗試拆解裝備中的裝備
	var res: Dictionary = eq.dismantle(uid)
	assert(not bool(res.get("ok", true)), "裝備中的裝備應禁止拆解")
	assert(gs.equip_worn.has(uid), "裝備仍應在 equip_worn")
	assert(inv.count("iron_scrap") == prev_scrap, "鐵屑不應變更")
	assert(gs.gold == prev_gold, "金幣不應變更")

	# 卸下後再拆解應成功
	var un_res: Dictionary = eq.unequip("weapon")
	assert(bool(un_res.get("ok", false)), "卸裝應成功")
	assert(eq.find_bag(uid).is_empty() == false, "卸裝後裝備應回背包")

	var res2: Dictionary = eq.dismantle(uid)
	assert(bool(res2.get("ok", false)), "卸裝後拆解應成功: %s" % res2)
	assert(eq.find_bag(uid).is_empty(), "拆解後背包應無此裝")

	print("  ok - 裝備中的裝備禁止拆解，卸下後可正常拆解")


## 4. 測試無效或不存在的 uid
func test_dismantle_invalid_uid(eq: Node, _gs: Node, _inv: Node) -> void:
	var res_empty: Dictionary = eq.dismantle("")
	assert(not bool(res_empty.get("ok", true)), "空 uid 應失敗")

	var res_ghost: Dictionary = eq.dismantle("non_existent_uid_12345")
	assert(not bool(res_ghost.get("ok", true)), "不存在的 uid 應失敗")

	print("  ok - 無效與不存在的 uid 守門測試通過")


## 5. 測試 town_forge 廢鐵桶互動契約
func test_scrap_bin_interaction_contract() -> void:
	var MapCatalogC = load("res://scripts/world/map_catalog.gd")
	var forge_map: Dictionary = MapCatalogC.build("town_forge")
	assert(not forge_map.is_empty(), "town_forge 地圖應可建構")

	var found_scrap_bin := false
	for e in forge_map.get("entities", []):
		if str(e.get("id", "")) == "scrap_bin":
			found_scrap_bin = true
			break
	assert(found_scrap_bin, "town_forge 必須包含 scrap_bin 互動實體")

	# 檢視 main.gd 中是否有 scrap_bin 處理與 _go_scrap_bin_panel
	var main_src: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	assert(main_src.find("\"scrap_bin\":") >= 0, "main.gd 應包含 scrap_bin 互動分支")
	assert(main_src.find("_go_scrap_bin_panel") >= 0, "main.gd 應呼叫或定義 _go_scrap_bin_panel")

	print("  ok - town_forge 與 main.gd scrap_bin 互動契約檢查通過")
