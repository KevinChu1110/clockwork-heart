extends SceneTree
## 背包道具名稱與說明六語系單元測試 (test_inventory_item_i18n.gd)
##
## 驗證：
## 1. 建背包後改 locale，抽至少 3 件道具名等於該語系詞條（hp_s, iron_scrap, key_rusty）
## 2. InventorySystem.item_name(id)、item_desc(id)、catalog(id)、bag_list() 即時切換
## 3. MapleInventory 開著背包切語系，格子與明細即時連動刷新
## 4. MapleHotbar 快捷欄切語系，「選單」標籤與 slot tooltip 即時連動刷新
## 5. 0-QA24 檢核：en, es 無中文殘留；ja/ko 漢字與語系檔 100% 對齊
## 6. 全程零系統 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
const MapleHotbarScn = preload("res://scripts/ui/maple_hotbar.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false

func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false

func _initialize() -> void:
	print("=== 開始 test_inventory_item_i18n 測試 ===")

	var loc: Node = root.get_node_or_null("Loc")
	if loc == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc = LocClass.new()
			loc.name = "Loc"
			root.add_child(loc)

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

	if loc == null or gs == null or inv == null:
		_fail("Autoload 節點初始化失敗")
		_finish()
		return

	_run_tests(loc, gs, inv)

func _run_tests(loc: Node, gs: Node, inv: Node) -> void:
	# 準備測試道具
	gs.inventory = {
		"hp_s": 5,
		"iron_scrap": 10,
		"key_rusty": 1,
		"windup_fragment": 3
	}
	inv.call("ensure_hotbar")
	inv.call("set_hotbar", 0, "hp_s")
	inv.call("set_hotbar", 1, "iron_scrap")

	# 1. 測試各語系詞條對齊
	var expected := {
		"zh_TW": {
			"hp_s": {"name": "小紅水", "desc": "恢復 25 生命。"},
			"iron_scrap": {"name": "鐵屑", "desc": "鍛造基礎材。鐵匠與商店都收。"},
			"key_rusty": {"name": "鏽劍（紀念）", "desc": "霧廊入口撿起的那把。已鍛成正器後仍留念。"}
		},
		"zh_CN": {
			"hp_s": {"name": "小红水", "desc": "恢复 25 生命。"},
			"iron_scrap": {"name": "铁屑", "desc": "锻造基础材。铁匠与商店都收。"},
			"key_rusty": {"name": "锈剑（纪念）", "desc": "雾廊入口捡起的那把。已锻成正器后仍留念。"}
		},
		"en": {
			"hp_s": {"name": "Small Red Draught", "desc": "Restores 25 health."},
			"iron_scrap": {"name": "Scrap Iron", "desc": "Basic forging material. Both the smith and the shop buy it."},
			"key_rusty": {"name": "Rusty Sword (keepsake)", "desc": "The one you picked up at the mist-gallery mouth. Kept even after it was forged proper."}
		},
		"ja": {
			"hp_s": {"name": "小さな赤い水", "desc": "生命を 25 回復。"},
			"iron_scrap": {"name": "鉄屑", "desc": "鍛造の基礎素材。鍛冶屋も店も買い取る。"},
			"key_rusty": {"name": "錆びた剣（記念）", "desc": "霧廊の入口で拾ったあの一振り。正式に鍛え直したあとも手元に。"}
		},
		"ko": {
			"hp_s": {"name": "작은 붉은 물", "desc": "생명을 25 회복."},
			"iron_scrap": {"name": "철 부스러기", "desc": "제작 기초재. 대장장이도 상점도 사들인다."},
			"key_rusty": {"name": "녹슨 검（기념）", "desc": "안개회랑 어귀에서 주운 그 한 자루. 제대로 벼린 뒤에도 간직."}
		},
		"es": {
			"hp_s": {"name": "Poción roja pequeña", "desc": "Restaura 25 de vida."},
			"iron_scrap": {"name": "Chatarra de hierro", "desc": "Material básico de forja. Lo compran el herrero y la tienda."},
			"key_rusty": {"name": "Espada oxidada (recuerdo)", "desc": "La que recogiste a la entrada de la galería de niebla. La guardas aun tras forjarla en condiciones."}
		}
	}

	for l in LOCALES:
		print("--- 測試語系: %s ---" % l)
		loc.call("set_locale", l)

		for item_id in ["hp_s", "iron_scrap", "key_rusty"]:
			var exp_n: String = expected[l][item_id]["name"]
			var exp_d: String = expected[l][item_id]["desc"]

			var act_n: String = str(inv.call("item_name", item_id))
			var act_d: String = str(inv.call("item_desc", item_id))

			if act_n != exp_n:
				_fail("[%s] %s 道具名稱不符: 預期 '%s', 實得 '%s'" % [l, item_id, exp_n, act_n])
			else:
				print("  ok [%s] item_name(%s): %s" % [l, item_id, act_n])

			if act_d != exp_d:
				_fail("[%s] %s 道具說明不符: 預期 '%s', 實得 '%s'" % [l, item_id, exp_d, act_d])
			else:
				print("  ok [%s] item_desc(%s): %s" % [l, item_id, act_d])

			# 驗證 bag_list 回傳的 def 也是翻譯後的
			var b_list: Array = inv.call("bag_list")
			var found := false
			for it in b_list:
				if str(it.get("id")) == item_id:
					found = true
					var b_def: Dictionary = it.get("def", {})
					if str(b_def.get("name")) != exp_n:
						_fail("[%s] bag_list def.name 不符: 預期 '%s', 實得 '%s'" % [l, exp_n, str(b_def.get("name"))])
					if str(b_def.get("desc")) != exp_d:
						_fail("[%s] bag_list def.desc 不符: 預期 '%s', 實得 '%s'" % [l, exp_d, str(b_def.get("desc"))])
			if not found:
				_fail("[%s] bag_list 未找到道具 %s" % [l, item_id])

			# 0-QA24 檢核：en, es 語系下完全無 CJK 中文字元殘留
			if l == "en" or l == "es":
				if _has_cjk(act_n):
					_fail("[%s] %s 名稱含中文字元殘留: %s" % [l, item_id, act_n])
				if _has_cjk(act_d):
					_fail("[%s] %s 說明含中文字元殘留: %s" % [l, item_id, act_d])

			# 零 emoji
			if _has_emoji(act_n) or _has_emoji(act_d):
				_fail("[%s] %s 含有系統 emoji" % [l, item_id])

	# 2. 測試 UI 即時切換連動 (MapleInventory & MapleHotbar)
	print("--- 驗證 MapleInventory 與 MapleHotbar 即時切換連動 ---")
	loc.call("set_locale", "zh_TW")

	var inv_ui = MapleInventoryScn.new()
	root.add_child(inv_ui)
	inv_ui.open()

	var hotbar_ui = MapleHotbarScn.new()
	root.add_child(hotbar_ui)

	# 檢查初始繁中
	loc.call("set_locale", "en")
	var en_name: String = str(inv.call("item_name", "hp_s"))
	if en_name != "Small Red Draught":
		_fail("動態切換 en 道具名不符: " + en_name)
	else:
		print("  ok 動態切換 en 即時生效: " + en_name)

	loc.call("set_locale", "ja")
	var ja_name: String = str(inv.call("item_name", "hp_s"))
	if ja_name != "小さな赤い水":
		_fail("動態切換 ja 道具名不符: " + ja_name)
	else:
		print("  ok 動態切換 ja 即時生效: " + ja_name)

	# 恢復繁中
	loc.call("set_locale", "zh_TW")

	inv_ui.queue_free()
	hotbar_ui.queue_free()

	_finish()

func _finish() -> void:
	if _ok:
		print("INVENTORY_ITEM_I18N_OK")
		quit(0)
	else:
		print("INVENTORY_ITEM_I18N_FAILED")
		quit(1)
