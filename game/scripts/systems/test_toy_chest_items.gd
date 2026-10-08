extends SceneTree
## 探索寶箱消耗品與材料專有名詞玩具世界化驗證 (test_toy_chest_items.gd)
##
## 驗收重點：
## 1. 六語系 item.json 結構與 key 完全一致（zh_TW, zh_CN, en, ja, ko, es）
## 2. 消耗品與材料專有名詞 100% 玩具世界化，零舊奇幻肉骨／食物／藥水殘留
## 3. InventorySystem 道具名稱、說明、使用流程在各語系正常執行
## 4. 探索寶箱掉落、拾取與使用消耗品流程無報錯，0 SCRIPT ERROR

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const TARGET_ITEMS := ["hp_s", "hp_m", "bread", "antidote", "hunt_bone", "hunt_hide", "star_ore", "wolf_fang"]

const FORBIDDEN_SUBSTRINGS := [
	"小紅水", "中紅水", "乾糧", "清焰露", "焰骨", "溢皮", "狼牙",
	"小红水", "中红水", "干粮",
	"Small Red Draught", "Medium Red Draught", "Dry Rations", "Flameclear Dew", "Flame Bone", "Spill Hide", "Wolf Fang",
	"小さな赤い水", "中くらいの赤い水", "干し飯", "清焰の露", "焰の骨", "溢れ皮", "狼の牙",
	"작은 붉은 물", "중간 붉은 물", "마른 양식", "청염 이슬", "불꽃 뼈", "넘친 가죽", "늑대 이빨",
	"Poción roja pequeña", "Poción roja mediana", "Ración seca", "Rocío apagallamas", "Hueso llameante", "Piel de derrame", "Colmillo de lobo"
]

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _initialize() -> void:
	print("=== 開始 test_toy_chest_items 測試 ===")
	_test_item_json_structure_and_keys()
	_test_inventory_and_chest_workflow()
	_finish()

func _test_item_json_structure_and_keys() -> void:
	print("--- 1. 驗證六語系 item.json 結構、key 一致性與零奇幻殘留 ---")
	var base_keys: Array = []
	var json_data: Dictionary = {}

	for loc in LOCALES:
		var path := "res://data/i18n/content/%s/item.json" % loc
		if not FileAccess.file_exists(path):
			_fail("語系檔不存在: " + path)
			return
		var f := FileAccess.open(path, FileAccess.READ)
		var text := f.get_as_text()
		var parsed = JSON.parse_string(text)
		if typeof(parsed) != TYPE_DICTIONARY:
			_fail("%s/item.json 解析失敗或非 Dictionary" % loc)
			return
		var d: Dictionary = parsed
		json_data[loc] = d

		var keys := d.keys()
		keys.sort()
		if base_keys.is_empty():
			base_keys = keys
		else:
			if keys != base_keys:
				_fail("%s/item.json keys 與基準不一致: 差異=%s" % [loc, str(_diff_keys(base_keys, keys))])

		# 驗證每個 item 都有 name 和 desc
		for k in keys:
			var entry: Dictionary = d.get(k, {})
			var n: String = str(entry.get("name", ""))
			var desc: String = str(entry.get("desc", ""))
			if n.strip_edges() == "":
				_fail("%s/item.json 道具 %s 缺少 name" % [loc, k])
			if desc.strip_edges() == "":
				_fail("%s/item.json 道具 %s 缺少 desc" % [loc, k])

			# 檢查違規舊奇幻名詞殘留
			for forbidden in FORBIDDEN_SUBSTRINGS:
				if n.contains(forbidden) or desc.contains(forbidden):
					_fail("%s/item.json 道具 %s 殘留舊奇幻 RPG 詞彙「%s」" % [loc, k, forbidden])

	print("  ok 六語系 item.json 結構與 %d 個 key 完全一致，零舊奇幻 RPG 詞彙殘留" % base_keys.size())

func _diff_keys(a: Array, b: Array) -> Array:
	var diff: Array = []
	for k in a:
		if not b.has(k):
			diff.append("-" + str(k))
	for k in b:
		if not a.has(k):
			diff.append("+" + str(k))
	return diff

func _test_inventory_and_chest_workflow() -> void:
	print("--- 2. 驗證 InventorySystem 與開寶箱道具流程 ---")
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var inv: Node = root.get_node_or_null("InventorySystem")
	if inv == null:
		var InvClass = load("res://scripts/systems/inventory_system.gd")
		if InvClass:
			inv = InvClass.new()
			inv.name = "InventorySystem"
			root.add_child(inv)

	if loc_node == null or gs == null or inv == null:
		_fail("Autoload 節點初始化失敗")
		return

	# 驗證所有目標道具在各語系下的 item_name() 與 item_desc()
	for l in LOCALES:
		loc_node.call("set_locale", l)
		for item_id in TARGET_ITEMS:
			var n: String = str(inv.call("item_name", item_id))
			var d: String = str(inv.call("item_desc", item_id))
			if n == "" or n == item_id:
				_fail("[%s] %s item_name() 回傳異常: %s" % [l, item_id, n])
			for forbidden in FORBIDDEN_SUBSTRINGS:
				if n.contains(forbidden) or d.contains(forbidden):
					_fail("[%s] %s 包含違規殘留名詞「%s」" % [l, item_id, forbidden])

	# 驗證寶箱掉落與使用消耗品流程（切回繁中測試行為）
	loc_node.call("set_locale", "zh_TW")
	gs.inventory = {}
	gs.hp = 50
	var max_hp = gs.effective_max_hp()

	# 模擬寶箱開箱掉落消耗品
	inv.call("add_item", "hp_s", 2)
	inv.call("add_item", "bread", 2)
	inv.call("add_item", "dust_crumb", 2)
	inv.call("add_item", "hunt_bone", 1)
	inv.call("add_item", "hunt_hide", 1)
	inv.call("add_item", "star_ore", 1)

	if int(inv.call("count", "hp_s")) != 2:
		_fail("寶箱掉落加入 hp_s 數量不符")
	if int(inv.call("count", "bread")) != 2:
		_fail("寶箱掉落加入 bread 數量不符")

	# 使用微光潤滑油 (hp_s, heal 25)
	var hp_before: int = gs.hp
	var res_hp: Dictionary = inv.call("use_item", "hp_s")
	if not bool(res_hp.get("ok", false)):
		_fail("使用微光潤滑油 (hp_s) 失敗: " + str(res_hp.get("msg", "")))
	elif not str(res_hp.get("msg", "")).contains("微光潤滑油"):
		_fail("使用微光潤滑油訊息未包含正確名稱: " + str(res_hp.get("msg", "")))
	elif gs.hp != mini(max_hp, hp_before + 25):
		_fail("使用微光潤滑油生命回復數值不符: hp=%d" % gs.hp)

	# 使用微型備用齒輪 (bread, heal 15)
	hp_before = gs.hp
	var res_bread: Dictionary = inv.call("use_item", "bread")
	if not bool(res_bread.get("ok", false)):
		_fail("使用微型備用齒輪 (bread) 失敗: " + str(res_bread.get("msg", "")))
	elif not str(res_bread.get("msg", "")).contains("微型備用齒輪"):
		_fail("使用微型備用齒輪訊息未包含正確名稱: " + str(res_bread.get("msg", "")))

	# 使用星屑碎 (dust_crumb)
	var dust_before: int = gs.stardust
	var res_dust: Dictionary = inv.call("use_item", "dust_crumb")
	if not bool(res_dust.get("ok", false)):
		_fail("使用星屑碎失敗: " + str(res_dust.get("msg", "")))
	elif gs.stardust != dust_before + 1:
		_fail("使用星屑碎未增加星屑")

	# 驗證寶箱文案生成
	var WorldContentScript = load("res://scripts/world/world_content.gd")
	if WorldContentScript:
		var chests: Dictionary = WorldContentScript.chests()
		if not chests.has("supply_crate"):
			_fail("缺少 supply_crate 寶箱定義")
		else:
			var sc: Dictionary = chests["supply_crate"]
			var t: String = str(sc.get("text", ""))
			if t.contains("乾糧"):
				_fail("supply_crate 文案殘留「乾糧」: " + t)
			elif not t.contains("微型齒輪") and not t.contains("齒輪"):
				_fail("supply_crate 文案未包含齒輪玩具詞彙: " + t)

	print("  ok 寶箱掉落、物品欄更新與道具使用流程完整驗證通過，0 報錯")

func _finish() -> void:
	if _ok:
		print("TOY_CHEST_ITEMS_OK")
		quit(0)
	else:
		print("TOY_CHEST_ITEMS_FAILED")
		quit(1)
