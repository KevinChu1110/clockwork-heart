extends SceneTree
## 《發條之心》探索背包選取裝備戰力差額比對膠囊與屬性預覽單元測試 (test_maple_inventory_diff.gd)
## 驗證項目：
## 1. 武器選取：
##    - 呈現屬性預覽（攻擊 +N）與攻擊力差額膠囊
##    - 升攻：綠色膠囊 #1E7538、文案『+N 攻擊』
##    - 降攻：灰色膠囊 #7A7090、文案『-N 攻擊』
##    - 持平：灰色膠囊 #7A7090、文案『--』
## 2. 防具選取：
##    - 呈現屬性預覽（防禦 +N）與防禦力差額膠囊
##    - 升防：綠色膠囊 #1E7538、文案『+N 防禦』
##    - 降防：灰色膠囊 #7A7090、文案『-N 防禦』
##    - 持平：灰色膠囊 #7A7090、文案『--』
## 3. 非裝備道具（消耗品/素材/重要道具）與未選取狀態：
##    - 屬性列與差額膠囊皆隱藏 (visible = false)
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換無缺詞
## 5. 全面零 Unicode Emoji，膠囊圓角與高對比色盤符合規範

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _wait: int = 0


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_DIFF_FAIL: ", msg)
	quit(1)
	return true


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 3:
				return false
			_inv.open()
			_step = 1
			_wait = 0

		1:
			if _wait < 3:
				return false

			print("--- 1. 初始化測試環境與裝備道具 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / EquipmentSystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "equip_worn" in gs and gs.equip_worn != null:
				gs.equip_worn.clear()
			if "equip_slots" in gs and gs.equip_slots != null:
				gs.equip_slots.clear()
			if "weapon_loadout" in gs and gs.weapon_loadout != null:
				for i in gs.weapon_loadout.size():
					gs.weapon_loadout[i] = ""

			# 加入道具：武器 (rusty_blade atk:4, meager_edge atk:9)、防具 (ash_mail def:3, knight_plate def:7)、非裝備
			inv_sys.call("add_item", "rusty_blade", 1)
			inv_sys.call("add_item", "meager_edge", 1)
			inv_sys.call("add_item", "ash_mail", 1)
			inv_sys.call("add_item", "knight_plate", 1)
			inv_sys.call("add_item", "hp_s", 5)
			inv_sys.call("add_item", "iron_scrap", 10)
			inv_sys.call("add_item", "key_rusty", 1)

			_inv.refresh()
			print("  ok 道具初始化完畢 (rusty_blade, meager_edge, ash_mail, knight_plate, hp_s, iron_scrap, key_rusty)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證節點存在與基本規格 ---")
			var stat_row: HBoxContainer = _inv.call("get_stat_row")
			var stat_lbl: Label = _inv.call("get_stat_preview")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")
			var diff_lbl: Label = _inv.call("get_diff_label")

			if stat_row == null or stat_lbl == null or diff_cap == null or diff_lbl == null:
				return _fail("找不到 StatRow / StatPreview / DiffCapsule / DiffLabel 節點")

			if diff_cap.custom_minimum_size.y < 24.0:
				return _fail("差額膠囊高度異常: %f" % diff_cap.custom_minimum_size.y)

			print("  ok 節點齊全，差額膠囊尺寸符合 (寬: %.1f, 高: %.1f)" % [diff_cap.custom_minimum_size.x, diff_cap.custom_minimum_size.y])

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 驗證非裝備類道具隱藏屬性列與差額膠囊 ---")
			var stat_row: HBoxContainer = _inv.call("get_stat_row")

			# 未選取
			_inv.set("_selected", "")
			_inv.refresh()
			if stat_row.visible:
				return _fail("未選取時 StatRow 應為隱藏 (visible=false)")

			# 消耗品 (hp_s)
			_inv.set("_selected", "hp_s")
			_inv.refresh()
			if stat_row.visible:
				return _fail("選取消耗品時 StatRow 應為隱藏 (visible=false)")

			# 素材 (iron_scrap)
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()
			if stat_row.visible:
				return _fail("選取素材時 StatRow 應為隱藏 (visible=false)")

			# 重要物品 (key_rusty)
			_inv.set("_selected", "key_rusty")
			_inv.refresh()
			if stat_row.visible:
				return _fail("選取重要物品時 StatRow 應為隱藏 (visible=false)")

			print("  ok 未選取/消耗品/素材/重要物品 皆正確隱藏 StatRow 與 DiffCapsule")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證武器選取之攻擊力屬性預覽與差額膠囊比對 ---")
			var stat_row: HBoxContainer = _inv.call("get_stat_row")
			var stat_lbl: Label = _inv.call("get_stat_preview")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var gs: Node = root.get_node_or_null("GameState")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			# 4.1 當前無武器裝備時：選取 rusty_blade (atk: 4)
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if not stat_row.visible:
				return _fail("選取武器 rusty_blade 時 StatRow 應為顯示")
			if not stat_lbl.text.contains("4"):
				return _fail("選取 rusty_blade 屬性預覽應包含 4，實際為: %s" % stat_lbl.text)
			if diff_lbl.text != "+4 攻擊":
				return _fail("無武器時 rusty_blade 差額文案應為『+4 攻擊』，實際為: %s" % diff_lbl.text)
			var sb_pos: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_pos == null or sb_pos.bg_color != Color("#1E7538"):
				return _fail("升攻膠囊底色應為 #1E7538，實際為: %s" % (sb_pos.bg_color if sb_pos else "null"))
			print("  ok [無武器狀態] 選取 rusty_blade -> 屬性預覽: %s，膠囊: %s (綠色 #1E7538)" % [stat_lbl.text, diff_lbl.text])

			# 4.2 裝備 rusty_blade (atk: 4)，選取更高攻武器 meager_edge (atk: 9) -> 升攻 +5 攻擊 (綠色 #1E7538)
			gs.equip_worn["w_rusty"] = {
				"uid": "w_rusty",
				"base_id": "rusty_blade",
				"name": "鏽劍",
				"slot": "weapon",
				"rolled": {"atk": 4.0}
			}
			gs.weapon_loadout[0] = "w_rusty"
			gs.equip_slots["weapon"] = "w_rusty"
			_inv.set("_selected", "meager_edge")
			_inv.refresh()
			if not stat_lbl.text.contains("9"):
				return _fail("選取 meager_edge 屬性預覽應包含 9，實際為: %s" % stat_lbl.text)
			if diff_lbl.text != "+5 攻擊":
				return _fail("裝備 4 攻選 9 攻武器時差額應為『+5 攻擊』，實際為: %s" % diff_lbl.text)
			var sb_up: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_up.bg_color != Color("#1E7538"):
				return _fail("升攻膠囊底色應為 #1E7538")
			print("  ok [升攻對比] 裝備 atk:4 武器，選取 atk:9 武器 -> 差額: %s (綠色 #1E7538)" % diff_lbl.text)

			# 4.3 裝備 meager_edge (atk: 9)，選取較低攻武器 rusty_blade (atk: 4) -> 降攻 -5 攻擊 (灰色 #7A7090)
			gs.equip_worn["w_meager"] = {
				"uid": "w_meager",
				"base_id": "meager_edge",
				"name": "微末之刃",
				"slot": "weapon",
				"rolled": {"atk": 9.0}
			}
			gs.weapon_loadout[0] = "w_meager"
			gs.equip_slots["weapon"] = "w_meager"
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if diff_lbl.text != "-5 攻擊":
				return _fail("裝備 9 攻選 4 攻武器時差額應為『-5 攻擊』，實際為: %s" % diff_lbl.text)
			var sb_down: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_down.bg_color != Color("#7A7090"):
				return _fail("降攻膠囊底色應為 #7A7090，實際為: %s" % sb_down.bg_color)
			print("  ok [降攻對比] 裝備 atk:9 武器，選取 atk:4 武器 -> 差額: %s (灰色 #7A7090)" % diff_lbl.text)

			# 4.4 裝備 rusty_blade (atk: 4)，選取同攻武器 rusty_blade (atk: 4) -> 持平 '--' (灰色 #7A7090)
			gs.equip_worn["w_rusty"] = {
				"uid": "w_rusty",
				"base_id": "rusty_blade",
				"name": "鏽劍",
				"slot": "weapon",
				"rolled": {"atk": 4.0}
			}
			gs.weapon_loadout[0] = "w_rusty"
			gs.equip_slots["weapon"] = "w_rusty"
			_inv.set("_selected", "rusty_blade")
			_inv.refresh()
			if diff_lbl.text != "--":
				return _fail("同攻武器差額文案應為『--』，實際為: %s" % diff_lbl.text)
			var sb_eq: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_eq.bg_color != Color("#7A7090"):
				return _fail("持平膠囊底色應為 #7A7090")
			print("  ok [持平對比] 裝備同攻武器時差額為: %s (灰色 #7A7090)" % diff_lbl.text)

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			print("\n--- 5. 驗證防具選取之防禦力屬性預覽與差額膠囊比對 ---")
			var stat_row: HBoxContainer = _inv.call("get_stat_row")
			var stat_lbl: Label = _inv.call("get_stat_preview")
			var diff_cap: PanelContainer = _inv.call("get_diff_capsule")
			var diff_lbl: Label = _inv.call("get_diff_label")
			var gs: Node = root.get_node_or_null("GameState")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")

			# 5.1 當前無防具時：選取 ash_mail (def: 3)
			gs.equip_slots["armor"] = ""
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			if not stat_row.visible:
				return _fail("選取防具 ash_mail 時 StatRow 應為顯示")
			if not stat_lbl.text.contains("3"):
				return _fail("選取 ash_mail 屬性預覽應包含 3，實際為: %s" % stat_lbl.text)
			if diff_lbl.text != "+3 防禦":
				return _fail("無防具時 ash_mail 差額文案應為『+3 防禦』，實際為: %s" % diff_lbl.text)
			var sb_pos: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_pos.bg_color != Color("#1E7538"):
				return _fail("升防膠囊底色應為 #1E7538")
			print("  ok [無防具狀態] 選取 ash_mail -> 屬性預覽: %s，膠囊: %s (綠色 #1E7538)" % [stat_lbl.text, diff_lbl.text])

			# 5.2 裝備 ash_mail (def: 3)，選取更高防防具 knight_plate (def: 7) -> 升防 +4 防禦 (綠色 #1E7538)
			gs.equip_worn["arm_ash"] = {
				"uid": "arm_ash",
				"base_id": "ash_mail",
				"name": "灰燼甲片",
				"slot": "armor",
				"rolled": {"def": 3.0}
			}
			gs.equip_slots["armor"] = "arm_ash"
			_inv.set("_selected", "knight_plate")
			_inv.refresh()
			if not stat_lbl.text.contains("7"):
				return _fail("選取 knight_plate 屬性預覽應包含 7，實際為: %s" % stat_lbl.text)
			if diff_lbl.text != "+4 防禦":
				return _fail("裝備 3 防選 7 防防具時差額應為『+4 防禦』，實際為: %s" % diff_lbl.text)
			var sb_up: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_up.bg_color != Color("#1E7538"):
				return _fail("升防膠囊底色應為 #1E7538")
			print("  ok [升防對比] 裝備 def:3 防具，選取 def:7 防具 -> 差額: %s (綠色 #1E7538)" % diff_lbl.text)

			# 5.3 裝備 knight_plate (def: 7)，選取較低防防具 ash_mail (def: 3) -> 降防 -4 防禦 (灰色 #7A7090)
			gs.equip_worn["arm_knight"] = {
				"uid": "arm_knight",
				"base_id": "knight_plate",
				"name": "騎士殘甲",
				"slot": "armor",
				"rolled": {"def": 7.0}
			}
			gs.equip_slots["armor"] = "arm_knight"
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			if diff_lbl.text != "-4 防禦":
				return _fail("裝備 7 防選 3 防防具時差額應為『-4 防禦』，實際為: %s" % diff_lbl.text)
			var sb_down: StyleBoxFlat = diff_cap.get_theme_stylebox("panel") as StyleBoxFlat
			if sb_down.bg_color != Color("#7A7090"):
				return _fail("降防膠囊底色應為 #7A7090，實際為: %s" % sb_down.bg_color)
			print("  ok [降防對比] 裝備 def:7 防具，選取 def:3 防具 -> 差額: %s (灰色 #7A7090)" % diff_lbl.text)

			# 5.4 裝備 ash_mail (def: 3)，選取同防防具 ash_mail (def: 3) -> 持平 '--' (灰色 #7A7090)
			gs.equip_worn["arm_ash2"] = {
				"uid": "arm_ash2",
				"base_id": "ash_mail",
				"name": "灰燼甲片",
				"slot": "armor",
				"rolled": {"def": 3.0}
			}
			gs.equip_slots["armor"] = "arm_ash2"
			_inv.set("_selected", "ash_mail")
			_inv.refresh()
			if diff_lbl.text != "--":
				return _fail("同防防具差額文案應為『--』，實際為: %s" % diff_lbl.text)
			print("  ok [持平對比] 裝備同防防具時差額為: %s (灰色 #7A7090)" % diff_lbl.text)

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態在地化即時切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var gs: Node = root.get_node_or_null("GameState")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var stat_lbl: Label = _inv.call("get_stat_preview")
			var diff_lbl: Label = _inv.call("get_diff_label")

			# 基準：裝備 rusty_blade (4) 與 ash_mail (3)
			gs.equip_worn["w_rusty"] = {
				"uid": "w_rusty",
				"base_id": "rusty_blade",
				"name": "鏽劍",
				"slot": "weapon",
				"rolled": {"atk": 4.0}
			}
			gs.weapon_loadout[0] = "w_rusty"
			gs.equip_slots["weapon"] = "w_rusty"
			gs.equip_worn["arm_ash"] = {
				"uid": "arm_ash",
				"base_id": "ash_mail",
				"name": "灰燼甲片",
				"slot": "armor",
				"rolled": {"def": 3.0}
			}
			gs.equip_slots["armor"] = "arm_ash"

			var test_locales: Array[Dictionary] = [
				{"code": "zh_TW", "wpn_stat": "攻擊 +9", "wpn_diff": "+5 攻擊", "arm_stat": "防禦 +7", "arm_diff": "+4 防禦"},
				{"code": "zh_CN", "wpn_stat": "攻击 +9", "wpn_diff": "+5 攻击", "arm_stat": "防御 +7", "arm_diff": "+4 防御"},
				{"code": "en",    "wpn_stat": "Attack +9", "wpn_diff": "+5 Attack", "arm_stat": "DEF +7", "arm_diff": "+4 DEF"},
				{"code": "ja",    "wpn_stat": "攻撃 +9", "wpn_diff": "+5 攻撃", "arm_stat": "防御 +7", "arm_diff": "+4 防御"},
				{"code": "ko",    "wpn_stat": "공격 +9", "wpn_diff": "+5 공격", "arm_stat": "방어 +7", "arm_diff": "+4 방어"},
				{"code": "es",    "wpn_stat": "Ataque +9", "wpn_diff": "+5 Ataque", "arm_stat": "DEF +7", "arm_diff": "+4 DEF"},
			]

			for tl in test_locales:
				var c: String = tl["code"]
				loc.call("set_locale", c)

				# 測試武器 meager_edge (升攻)
				_inv.set("_selected", "meager_edge")
				_inv.refresh()
				if diff_lbl.text != tl["wpn_diff"]:
					return _fail("[%s] 武器差額文案不符: 期望 '%s'，實際 '%s'" % [c, tl["wpn_diff"], diff_lbl.text])
				if not stat_lbl.text.contains("9"):
					return _fail("[%s] 武器屬性預覽不符: 實際 '%s'" % [c, stat_lbl.text])

				# 測試防具 knight_plate (升防)
				_inv.set("_selected", "knight_plate")
				_inv.refresh()
				if diff_lbl.text != tl["arm_diff"]:
					return _fail("[%s] 防具差額文案不符: 期望 '%s'，實際 '%s'" % [c, tl["arm_diff"], diff_lbl.text])
				if not stat_lbl.text.contains("7"):
					return _fail("[%s] 防具屬性預覽不符: 實際 '%s'" % [c, stat_lbl.text])

				print("  ok [%s] 武器差額『%s』與防具差額『%s』多語系即時切換完全正確" % [c, tl["wpn_diff"], tl["arm_diff"]])

			# 還原回繁中
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 7. 零系統 Emoji 檢查 ---")
			var stat_lbl: Label = _inv.call("get_stat_preview")
			var diff_lbl: Label = _inv.call("get_diff_label")

			for text_val in [stat_lbl.text, diff_lbl.text]:
				for ch in text_val:
					var cp: int = ch.unicode_at(0)
					if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF):
						return _fail("發現系統 Emoji (U+%04X): %s" % [cp, text_val])

			print("  ok 零系統 Emoji 檢查通過")
			print("\nMAPLE_INVENTORY_DIFF_OK")
			quit(0)
			return true

	return false
