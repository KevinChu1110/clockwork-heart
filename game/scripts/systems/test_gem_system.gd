extends SceneTree
## godot --headless -s res://scripts/systems/test_gem_system.gd


func _initialize() -> void:
	var gem = root.get_node_or_null("GemSystem")
	var gs = root.get_node_or_null("GameState")
	var eq = root.get_node_or_null("EquipmentSystem")
	if gem == null or gs == null:
		push_error("autoload missing")
		print("GEM_FAIL")
		quit(1)
		return
	gs.reset_new_game()
	gs.gem_bag = []
	gs.level = 10
	gs.gold = 500

	## 合成 3→1
	gem.add_gem("red", 1, 3)
	assert(gem.count_of("red", 1) == 3, "have 3 red1")
	var fr: Dictionary = gem.fuse("red", 1)
	assert(bool(fr.get("ok", false)), "fuse ok %s" % fr)
	assert(gem.count_of("red", 1) == 0, "consumed")
	assert(gem.count_of("red", 2) == 1, "got red2")
	print("  ok fuse 3→1")

	## 鑲嵌必定成功、替換
	eq._ensure_state()
	var w := {
		"uid": "gw1", "base_id": "t", "name": "測劍", "slot": "weapon",
		"tier": 1, "line": "sword", "quality": "common", "quality_label": "凡",
		"rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
	}
	gs.equip_worn["gw1"] = w
	gs.equip_slots["weapon"] = "gw1"
	gs.weapon_loadout = ["gw1", "", ""]
	var gid := str(gs.gem_bag[0].get("id", ""))
	var sr: Dictionary = gem.socket("gw1", gid)
	assert(bool(sr.get("ok", false)), "socket %s" % sr)
	assert(str(gs.equip_worn["gw1"].get("gem", {}).get("color", "")) == "red", "gem on weapon")
	var b: Dictionary = gem.worn_bonuses()
	assert(float(b.get("crit", 0.0)) > 0.0, "crit bonus")
	print("  ok socket + bonuses")

	## 未解鎖
	gs.level = 5
	gs.gem_bag = []
	gem.add_gem("blue", 1, 3)
	var bad: Dictionary = gem.fuse("blue", 1)
	assert(not bool(bad.get("ok", true)), "lv5 cannot fuse")
	print("  ok level gate")

	## 熔爐第二產線
	gs.level = 20
	gs.gold = 3000
	gs.gem_furnace = false
	gs.gem_smelt_day = ""
	gs.gem_smelt_used = 0
	gs.gem_shards = {"red": 0, "yellow": 0, "blue": 0}
	gs.gem_bag = []
	assert(gem.smelt_lines_per_day() == 1, "no furnace = 1 line")
	gem.add_shards("yellow", 6)
	var sm1: Dictionary = gem.smelt("yellow")
	assert(bool(sm1.get("ok", false)), "smelt1 %s" % sm1)
	assert(gem.smelt_left_today() == 0, "line spent")
	var sm_block: Dictionary = gem.smelt("yellow")
	assert(not bool(sm_block.get("ok", true)), "no second line yet")
	var uf: Dictionary = gem.unlock_furnace()
	assert(bool(uf.get("ok", false)), "unlock furnace %s" % uf)
	assert(gem.furnace_unlocked(), "furnace on")
	assert(gem.smelt_lines_per_day() == 2, "two lines")
	## 換日重置後雙線
	gs.gem_smelt_day = "2000-01-01"
	gs.gem_smelt_used = 0
	gem.add_shards("blue", 6)
	assert(bool(gem.smelt("blue").get("ok", false)), "line A")
	assert(bool(gem.smelt("blue").get("ok", false)), "line B furnace")
	assert(gem.smelt_left_today() == 0, "both lines used")
	print("  ok furnace second line")

	## 勳章解鎖（原作 50 枚）
	gs.gem_furnace = false
	gs.gold = 0
	var inv = root.get_node_or_null("InventorySystem")
	if inv:
		inv.add_item("medal", 50)
		var um: Dictionary = gem.unlock_furnace("medal")
		assert(bool(um.get("ok", false)), "medal unlock %s" % um)
		assert(gem.furnace_unlocked(), "furnace from medals")
		assert(int(inv.count("medal")) == 0, "medals spent")
		print("  ok medal unlock")
	else:
		print("  skip medal unlock (no InventorySystem)")

	## == 一鍵鑲嵌 auto_socket 測試 ==
	gs.level = 20
	gs.equip_worn = {}
	gs.equip_slots = {}
	gs.gem_bag = []
	gs.gold = 1000

	# 1. 未穿戴裝備時
	var r_no_equip: Dictionary = gem.auto_socket()
	assert(not bool(r_no_equip.get("ok", true)), "no equip should fail")
	assert("未穿戴" in str(r_no_equip.get("msg", "")), "no equip msg")
	print("  ok auto_socket: no equip check")

	# 2. 穿戴裝備但背包無寶石
	var tw := {
		"uid": "test_w1", "name": "測試武器", "slot": "weapon",
		"tier": 1, "line": "sword", "quality": "common",
	}
	var ta := {
		"uid": "test_a1", "name": "測試防具", "slot": "armor",
		"tier": 1, "line": "heavy", "quality": "common",
	}
	gs.equip_worn["test_w1"] = tw
	gs.equip_worn["test_a1"] = ta
	gs.equip_slots["weapon"] = "test_w1"
	gs.equip_slots["armor"] = "test_a1"

	var r_no_gem: Dictionary = gem.auto_socket()
	assert(not bool(r_no_gem.get("ok", true)), "no gems should fail")
	assert("背包沒有" in str(r_no_gem.get("msg", "")), "no gem msg")
	print("  ok auto_socket: no gem in bag check")

	# 3. 有空孔有寶石但金幣不足
	gem.add_gem("red", 1, 1)
	gs.gold = 0
	var r_no_gold: Dictionary = gem.auto_socket()
	assert(not bool(r_no_gold.get("ok", true)), "no gold should fail")
	assert("金幣不足" in str(r_no_gold.get("msg", "")), "no gold msg")
	print("  ok auto_socket: insufficient gold check")

	# 4. 只填空孔，已鑲嵌的不動（武器空孔，防具已有紅1）
	gs.gold = 1000
	gs.gem_bag = []
	ta["gem"] = {"color": "red", "level": 1}
	gs.equip_worn["test_a1"] = ta
	gem.add_gem("blue", 1, 1)
	gem.add_gem("yellow", 2, 1)
	var r_single: Dictionary = gem.auto_socket()
	assert(bool(r_single.get("ok", false)), "auto_socket 1 slot ok")
	assert(int(r_single.get("count", 0)) == 1, "socketed 1 slot")
	# 武器應鑲入黃2（等級較高優先）
	var w_gem: Dictionary = gs.equip_worn["test_w1"].get("gem", {})
	assert(str(w_gem.get("color", "")) == "yellow" and int(w_gem.get("level", 0)) == 2, "weapon got yellow 2")
	# 防具紅1保持不變（不可覆蓋已有鑲嵌）
	var a_gem: Dictionary = gs.equip_worn["test_a1"].get("gem", {})
	assert(str(a_gem.get("color", "")) == "red" and int(a_gem.get("level", 0)) == 1, "armor gem unchanged")
	# 背包剩餘 blue 1
	assert(gs.gem_bag.size() == 1 and str(gs.gem_bag[0].get("color", "")) == "blue", "gem_bag remaining")
	print("  ok auto_socket: single empty slot filled without touching existing")

	# 5. 全滿時不進行鑲嵌
	var r_full: Dictionary = gem.auto_socket()
	assert(not bool(r_full.get("ok", true)), "full slots should not socket")
	assert("無閒置空孔" in str(r_full.get("msg", "")), "full slots msg")
	print("  ok auto_socket: full slots guard")

	# 6. 雙空孔一次填補（高階等級優先、部位相性優先）
	tw.erase("gem")
	ta.erase("gem")
	gs.equip_worn["test_w1"] = tw
	gs.equip_worn["test_a1"] = ta
	gs.gem_bag = []
	gem.add_gem("red", 1, 1)
	gem.add_gem("yellow", 2, 1)
	gem.add_gem("blue", 3, 1)
	var r_double: Dictionary = gem.auto_socket()
	assert(bool(r_double.get("ok", false)), "auto_socket 2 slots ok")
	assert(int(r_double.get("count", 0)) == 2, "socketed 2 slots")
	assert(str(gs.equip_worn["test_w1"].get("gem", {}).get("color", "")) == "blue", "weapon got blue 3")
	assert(int(gs.equip_worn["test_w1"].get("gem", {}).get("level", 0)) == 3, "weapon got lv 3")
	assert(str(gs.equip_worn["test_a1"].get("gem", {}).get("color", "")) == "yellow", "armor got yellow 2")
	assert(int(gs.equip_worn["test_a1"].get("gem", {}).get("level", 0)) == 2, "armor got lv 2")
	assert(gs.gem_bag.size() == 1 and str(gs.gem_bag[0].get("color", "")) == "red", "red 1 left in bag")
	var bonuses: Dictionary = gem.worn_bonuses()
	assert(float(bonuses.get("hit", 0.0)) > 0.0, "hit bonus from blue on weapon")
	assert(float(bonuses.get("def_pct", 0.0)) > 0.0, "def_pct bonus from yellow on armor")
	print("  ok auto_socket: double empty slots filled with optimal gems")

	print("GEM_OK")
	quit(0)
