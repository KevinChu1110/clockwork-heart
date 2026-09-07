extends SceneTree
## 手藝工坊寶石櫃檢視無頭測試：godot --headless -s res://scripts/systems/test_gem_case_inspect.gd
##
## 驗證界線與功能：
##   1. 專屬盤點與數值總覽：inspect_gem_case() 與 gem_case_status_bbcode() 正確呈現全身孔位與加成。
##   2. 呼叫 GemSystem.worn_bonuses()：正確呈現武器／防具各孔位鑲嵌色階與六維總加成（暴擊、攻擊%、命中、生命%、防禦%、迴避）。
##   3. 嚴守器軸界線無第四軸：六維總加成僅含授權之六維，無任何未授權第四軸屬性。
##   4. 純讀取無副作用：盤點與 BBCode 產生過程不改動任何玩家數值與存檔。
##   5. main.gd 專屬互動與面板入口綁定：gem_case 正確串接 _go_gem_case_panel()，而非直通通用熔煉介面。

var _ok := true


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	print("== 測試手藝工坊寶石櫃檢視：全身鑲嵌盤點與數值總覽 ==")
	var gs: Node = root.get_node_or_null("GameState")
	var gem: Node = root.get_node_or_null("GemSystem")
	var eq: Node = root.get_node_or_null("EquipmentSystem")

	if gs == null or gem == null or eq == null:
		_fail("GameState / GemSystem / EquipmentSystem autoload 缺失")
		print("GEM_CASE_INSPECT_FAIL")
		quit(1)
		return

	gs.reset_new_game()
	eq._ensure_state()
	gem._ensure_bag()
	gem._ensure_shards()
	gs.level = 10
	gs.gold = 1000

	## 1) 初始未裝備／未鑲嵌狀態檢驗
	gs.equip_worn = {}
	gs.equip_slots["weapon"] = ""
	gs.equip_slots["armor"] = ""
	gs.gem_bag = []

	var survey0: Dictionary = gem.inspect_gem_case()
	if int(survey0.get("total_sockets", 0)) != 2:
		_fail("總孔位數應為 2（武器、防具各一孔），得 %d" % int(survey0.get("total_sockets", 0)))
	if int(survey0.get("filled_sockets", -1)) != 0:
		_fail("初始已鑲嵌孔位應為 0，得 %d" % int(survey0.get("filled_sockets", -1)))
	if int(survey0.get("bag_gems_count", -1)) != 0:
		_fail("背包寶石數應為 0，得 %d" % int(survey0.get("bag_gems_count", -1)))

	var slots0: Array = survey0.get("slots", [])
	if slots0.size() != 2:
		_fail("孔位列表長度應為 2，得 %d" % slots0.size())
	for s in slots0:
		if bool(s.get("is_equipped", true)):
			_fail("初始不應有裝備穿戴：%s" % str(s.get("slot", "")))
		if bool(s.get("has_gem", true)):
			_fail("初始孔位不應有寶石：%s" % str(s.get("slot", "")))

	var wb0: Dictionary = survey0.get("worn_bonuses", {})
	for k in ["crit", "atk_pct", "hit", "hp_pct", "def_pct", "eva"]:
		if float(wb0.get(k, -1.0)) != 0.0:
			_fail("初始全身寶石加成 %s 應為 0.0，得 %f" % [k, float(wb0.get(k, 0.0))])
	print("  ok 初始空裝空孔盤點檢驗通過")

	## 2) 嚴格遵守器軸界線：無第四軸檢驗
	var authorized_axes := ["crit", "atk_pct", "hit", "hp_pct", "def_pct", "eva"]
	for k in wb0.keys():
		if not str(k) in authorized_axes:
			_fail("發現未授權的第四軸屬性鍵：%s" % str(k))
	var direct_wb: Dictionary = gem.worn_bonuses()
	for k in direct_wb.keys():
		if not str(k) in authorized_axes:
			_fail("worn_bonuses 發現未授權的第四軸屬性鍵：%s" % str(k))
	print("  ok 器軸界線檢驗通過：六維數值純正，無第四軸")

	## 3) 穿戴裝備與鑲嵌寶石驗證：武器（紅·暴擊）＋ 防具（黃·防禦%）
	var test_sword := {
		"uid": "test_w1",
		"base_id": "sword_basic",
		"name": "青鋼短劍",
		"slot": "weapon",
		"tier": 1,
		"line": "sword",
		"quality": "common",
		"gem": {
			"color": "red",
			"level": 2,
		},
	}
	var test_armor := {
		"uid": "test_a1",
		"base_id": "cloth_basic",
		"name": "厚皮甲",
		"slot": "armor",
		"tier": 1,
		"line": "armor",
		"quality": "common",
		"gem": {
			"color": "yellow",
			"level": 3,
		},
	}
	gs.equip_worn = {
		"test_w1": test_sword,
		"test_a1": test_armor,
	}
	gs.equip_slots["weapon"] = "test_w1"
	gs.equip_slots["armor"] = "test_a1"

	var survey1: Dictionary = gem.inspect_gem_case()
	if int(survey1.get("filled_sockets", 0)) != 2:
		_fail("已鑲嵌孔位應為 2，得 %d" % int(survey1.get("filled_sockets", 0)))

	var slots1: Array = survey1.get("slots", [])
	var w_slot: Dictionary = slots1[0]
	var a_slot: Dictionary = slots1[1]

	if not bool(w_slot.get("is_equipped", false)) or not bool(w_slot.get("has_gem", false)):
		_fail("武器欄位應已穿戴且已鑲嵌")
	if str(w_slot.get("bonus_key", "")) != "crit" or float(w_slot.get("bonus_val", 0.0)) != 4.0:
		_fail("武器紅寶石 Lv2 加成應為 crit +4.0，得 %s +%f" % [str(w_slot.get("bonus_key", "")), float(w_slot.get("bonus_val", 0.0))])

	if not bool(a_slot.get("is_equipped", false)) or not bool(a_slot.get("has_gem", false)):
		_fail("防具欄位應已穿戴且已鑲嵌")
	if str(a_slot.get("bonus_key", "")) != "def_pct" or not is_equal_approx(float(a_slot.get("bonus_val", 0.0)), 0.12):
		_fail("防具黃寶石 Lv3 加成應為 def_pct +0.12，得 %s +%f" % [str(a_slot.get("bonus_key", "")), float(a_slot.get("bonus_val", 0.0))])

	var wb1: Dictionary = survey1.get("worn_bonuses", {})
	if float(wb1.get("crit", 0.0)) != 4.0:
		_fail("六維總加成暴擊應為 4.0，得 %f" % float(wb1.get("crit", 0.0)))
	if not is_equal_approx(float(wb1.get("def_pct", 0.0)), 0.12):
		_fail("六維總加成防禦%應為 0.12，得 %f" % float(wb1.get("def_pct", 0.0)))
	if float(wb1.get("atk_pct", 0.0)) != 0.0 or float(wb1.get("hp_pct", 0.0)) != 0.0:
		_fail("未鑲嵌屬性應為 0.0")
	print("  ok 武器（紅2）與防具（黃3）鑲嵌與六維加成計算正確")

	## 4) 切換色階測試：武器（黃·攻擊% ＋ 藍·命中）與 防具（紅·生命% ＋ 藍·迴避）
	test_sword["gem"] = {"color": "blue", "level": 3}
	test_armor["gem"] = {"color": "red", "level": 1}
	var survey2: Dictionary = gem.inspect_gem_case()
	var wb2: Dictionary = survey2.get("worn_bonuses", {})
	if float(wb2.get("hit", 0.0)) != 9.0:
		_fail("武器藍寶石 Lv3 命中應為 9.0，得 %f" % float(wb2.get("hit", 0.0)))
	if not is_equal_approx(float(wb2.get("hp_pct", 0.0)), 0.03):
		_fail("防具紅寶石 Lv1 生命% 應為 0.03，得 %f" % float(wb2.get("hp_pct", 0.0)))

	test_sword["gem"] = {"color": "yellow", "level": 2}
	test_armor["gem"] = {"color": "blue", "level": 2}
	var survey3: Dictionary = gem.inspect_gem_case()
	var wb3: Dictionary = survey3.get("worn_bonuses", {})
	if not is_equal_approx(float(wb3.get("atk_pct", 0.0)), 0.08):
		_fail("武器黃寶石 Lv2 攻擊% 應為 0.08，得 %f" % float(wb3.get("atk_pct", 0.0)))
	if float(wb3.get("eva", 0.0)) != 6.0:
		_fail("防具藍寶石 Lv2 迴避 應為 6.0，得 %f" % float(wb3.get("eva", 0.0)))
	print("  ok 各色階（黃／藍／紅）在武器與防具上之對應效果驗證全數通過")

	## 5) 純讀取無副作用檢驗
	var gold_before: int = gs.gold
	var level_before: int = gs.level
	var equip_worn_before: Dictionary = gs.equip_worn.duplicate(true)
	var gem_bag_before: Array = gs.gem_bag.duplicate(true)

	for _i in range(5):
		var _s: Dictionary = gem.inspect_gem_case()
		var _bb: String = gem.gem_case_status_bbcode()

	if gs.gold != gold_before or gs.level != level_before:
		_fail("寶石櫃盤點不應改動玩家基礎數值")
	if gs.equip_worn != equip_worn_before:
		_fail("寶石櫃盤點不應改動穿戴裝備")
	if gs.gem_bag != gem_bag_before:
		_fail("寶石櫃盤點不應改動背包寶石")
	print("  ok 純讀取無副作用檢驗通過")

	## 6) BBCode 格式與無 Emoji 規範檢驗
	var bb_text: String = gem.gem_case_status_bbcode()
	if not "手藝工坊 · 寶石櫃檢視" in bb_text:
		_fail("BBCode 缺少手藝工坊寶石櫃標題")
	if not "裝備鑲嵌孔位盤點" in bb_text:
		_fail("BBCode 缺少孔位盤點段落")
	if not "全身寶石六維總加成" in bb_text:
		_fail("BBCode 缺少全身寶石六維總加成段落")
	for kw in ["暴擊", "攻擊%", "命中", "生命%", "防禦%", "迴避"]:
		if not kw in bb_text:
			_fail("BBCode 缺少六維關鍵字：%s" % kw)

	var banned_emojis := ["⭐", "🌟", "✨", "⚔️", "🛡️", "❤️", "💎", "🔮"]
	for em in banned_emojis:
		if em in bb_text:
			_fail("BBCode 包含違規系統 Emoji：%s" % em)
	print("  ok BBCode 格式與無系統 Emoji 檢驗通過")

	## 7) 檢驗 main.gd 專屬互動與面板入口綁定
	var main_src: String = FileAccess.get_file_as_string("res://scripts/main.gd")
	if main_src == "":
		_fail("讀取 main.gd 失敗")
	else:
		if not "func _go_gem_case_panel() -> void:" in main_src:
			_fail("main.gd 缺少 _go_gem_case_panel() 宣告")
		if not '"gem_case":' in main_src:
			_fail("main.gd 缺少 gem_case 互動 match 分支")
		if not "_go_gem_case_panel" in main_src:
			_fail("main.gd 缺少 _go_gem_case_panel 引用")
		# 確認 gem_case 不再直接通往 _go_gem_panel
		if '"gem_case", "cold_furnace"' in main_src or '"gem_case":\n\t\t\t\t\t_go_gem_panel()' in main_src:
			_fail("gem_case 仍直通通用熔煉介面，未走專屬盤點互動")
		print("  ok main.gd gem_case 專屬盤點互動與面板綁定檢驗通過")

	if _ok:
		print("GEM_CASE_INSPECT_OK")
		quit(0)
	else:
		print("GEM_CASE_INSPECT_FAIL")
		quit(1)
