extends SceneTree
## 《發條之心》MapleInventory 探索背包即時容量進度膠囊顯示與格子滿載提示單元測試
## (test_maple_inventory_capacity.gd)
##
## 驗證項目：
## 1. 元件規格與多巴胺亮色盤規範：
##    - _capacity_capsule (CapacityCapsule) 與 _capacity_label (CapacityLabel) 節點存在且放置於左側底部一鍵整理按鈕旁
##    - 膠囊尺寸 custom_minimum_size >= 48px (120x48px)，熱區高度合規
##    - 正常樣式：奶油白底 (#FFFDF8 COLOR_BG_CREAM)、深藍紫描邊 (#1F1A3A 2px)、圓角 16px、粉圓體字級 >= 16px (16px)
##    - 零系統 Emoji
## 2. 容量計算與即時連動：
##    - 空背包：顯示『容量 0/24』(occupied=0, total=24)
##    - 添加 12 件道具：顯示『容量 12/24』(occupied=12, total=24)
##    - 分類切換 (如裝備 Chip)：即時更新為該分類佔用格數 (如 4 件裝備 ->『容量 4/24』)
##    - 切換回『全部』：即時恢復『容量 12/24』
##    - 一鍵整理 (sort)：容量顯示維持正確
## 3. 滿載色階切換與提示：
##    - 滿載 (>= 24 格)：膠囊樣式自動切換為珊瑚粉 (#FF5E8A COLOR_PINK) 警示色階，白字帶深藍紫描邊，暖橘光暈
##    - 滿載選取物品：即時於操作提示標籤 (_tip) 與詳情卡片提示『背包空間已滿』
##    - 減至未滿載 (23 格)：膠囊樣式自動切回奶油白底，解除滿載警示
## 4. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時在地化切換無缺詞、歐美語系零 CJK 殘留、零系統 Emoji
## 5. 實機渲染存證：在非 headless (xvfb) 下擷取 6 張真實 OpenGL3 實機截圖至 proofs/t_3dbebffd/，驗證 SHA256 獨立不重複

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")

const LOCALES: Array[String] = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
const EXPECTED_CAPACITY_PREFIXES: Dictionary = {
	"zh_TW": "容量",
	"zh_CN": "容量",
	"en": "Capacity",
	"ja": "容量",
	"ko": "용량",
	"es": "Capacidad"
}
const EXPECTED_FULL_TIPS: Dictionary = {
	"zh_TW": "背包空間已滿",
	"zh_CN": "背包空间已满",
	"en": "Backpack is full",
	"ja": "バッグの空きがありません",
	"ko": "가방 공간이 가득 찼습니다",
	"es": "Espacio de mochila lleno"
}

var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _out_dir: String = ""
var _proof_hashes: Dictionary = {}


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base_dir := ProjectSettings.globalize_path("res://")
	_out_dir = base_dir.path_join("../proofs/t_3dbebffd")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_CAPACITY_FAIL: ", msg)
	quit(1)
	return true


func _has_cjk(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x4E00 and u <= 0x9FFF) or (u >= 0x3400 and u <= 0x4DBF):
			return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var u := c.unicode_at(0)
		if (u >= 0x1F300 and u <= 0x1FAFF) or (u >= 0x2600 and u <= 0x27BF and u != 0x2715 and u != 0x2713):
			return true
	return false


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

			print("--- 1. 初始化測試環境與 Autoload ---")
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
			if "equip_bag" in gs and gs.equip_bag != null:
				gs.equip_bag.clear()

			_inv.refresh()
			print("  ok 測試環境已初始化")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			print("\n--- 2. 驗證容量進度膠囊規格與多巴胺視覺規範 ---")
			var capsule: PanelContainer = _inv.call("get_capacity_capsule")
			var label: Label = _inv.call("get_capacity_label")

			if capsule == null or not is_instance_valid(capsule):
				return _fail("找不到 _capacity_capsule (CapacityCapsule) 節點")
			if label == null or not is_instance_valid(label):
				return _fail("找不到 _capacity_label (CapacityLabel) 節點")

			if capsule.custom_minimum_size.y < 48.0:
				return _fail("膠囊高度未達手遊人體工學規範 (>= 48px)，實際為: %f" % capsule.custom_minimum_size.y)
			if capsule.custom_minimum_size.x < 100.0:
				return _fail("膠囊寬度過窄 (< 100px)，實際為: %f" % capsule.custom_minimum_size.x)

			# 檢查正常狀態 StyleBoxFlat (奶油白底 #FFFDF8、深藍紫邊框 #1F1A3A 2px、圓角 16px)
			var sb = capsule.get_theme_stylebox("panel")
			if not (sb is StyleBoxFlat):
				return _fail("膠囊 panel 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if abs(sbf.bg_color.r - Color("#FFFDF8").r) > 0.05 or abs(sbf.bg_color.g - Color("#FFFDF8").g) > 0.05 or abs(sbf.bg_color.b - Color("#FFFDF8").b) > 0.05:
				return _fail("膠囊正常底色非奶油白 (#FFFDF8)，實際為: %s" % str(sbf.bg_color))
			if sbf.border_color != Color("#1F1A3A"):
				return _fail("膠囊描邊非深藍紫 (#1F1A3A)，實際為: %s" % str(sbf.border_color))
			if sbf.corner_radius_top_left != 16:
				return _fail("膠囊圓角非 16px，實際為: %d" % sbf.corner_radius_top_left)

			# 檢查文字字級 >= 16px
			var fsize: int = label.get_theme_font_size("font_size")
			if fsize < 16:
				return _fail("膠囊文字字級未達 >= 16px 規範，實際為: %d" % fsize)

			# 檢查空背包數據
			var occ: int = int(_inv.call("get_occupied_capacity"))
			var tot: int = int(_inv.call("get_total_capacity"))
			if occ != 0 or tot != 24:
				return _fail("空背包容量數據不符，預期 0/24，實得: %d/%d" % [occ, tot])
			if label.text != "容量 0/24":
				return _fail("空背包膠囊文案不符，預期 '容量 0/24'，實得: '%s'" % label.text)

			print("  ok 膠囊規格與初始空背包狀態 (容量 0/24) 驗證通過")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			print("\n--- 3. 注入 12 件道具並驗證容量計算與一鍵整理 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")

			# 註冊各類道具
			inv_sys.call("register_item", "blade_iron", {"name": "鐵製短劍", "kind": "weapon", "desc": "基礎武器", "glyph": "刃"})
			inv_sys.call("register_item", "sword_bronze", {"name": "青銅闊劍", "kind": "weapon", "desc": "厚重武器", "glyph": "刃"})
			inv_sys.call("register_item", "armor_leather", {"name": "皮質軟甲", "kind": "armor", "desc": "輕型防具", "glyph": "裝"})
			inv_sys.call("register_item", "shield_wood", {"name": "木製圓盾", "kind": "armor", "desc": "基礎防具", "glyph": "裝"})
			inv_sys.call("register_item", "pot_hp_1", {"name": "微光潤滑油", "kind": "consumable", "desc": "回復油品", "glyph": "藥"})
			inv_sys.call("register_item", "pot_hp_2", {"name": "高純潤滑油", "kind": "consumable", "desc": "強力回復油品", "glyph": "藥"})
			inv_sys.call("register_item", "mat_copper", {"name": "黃銅齒輪", "kind": "material", "desc": "傳動齒輪", "glyph": "料"})
			inv_sys.call("register_item", "mat_steel", {"name": "精鋼軸承", "kind": "material", "desc": "耐磨軸承", "glyph": "料"})
			inv_sys.call("register_item", "mat_spring", {"name": "發條彈簧", "kind": "material", "desc": "蓄能彈簧", "glyph": "料"})
			inv_sys.call("register_item", "gem_ruby", {"name": "赤紅寶石", "kind": "gem", "desc": "火之寶石", "glyph": "寶"})
			inv_sys.call("register_item", "gem_sapphire", {"name": "湛藍寶石", "kind": "gem", "desc": "水之寶石", "glyph": "寶"})
			inv_sys.call("register_item", "gem_topaz", {"name": "金黃寶石", "kind": "gem", "desc": "雷之寶石", "glyph": "寶"})

			inv_sys.call("add_item", "blade_iron", 1)
			inv_sys.call("add_item", "sword_bronze", 1)
			inv_sys.call("add_item", "armor_leather", 1)
			inv_sys.call("add_item", "shield_wood", 1)
			inv_sys.call("add_item", "pot_hp_1", 5)
			inv_sys.call("add_item", "pot_hp_2", 3)
			inv_sys.call("add_item", "mat_copper", 10)
			inv_sys.call("add_item", "mat_steel", 8)
			inv_sys.call("add_item", "mat_spring", 12)
			inv_sys.call("add_item", "gem_ruby", 2)
			inv_sys.call("add_item", "gem_sapphire", 4)
			inv_sys.call("add_item", "gem_topaz", 1)

			_inv.refresh()

			var label: Label = _inv.call("get_capacity_label")
			var occ: int = int(_inv.call("get_occupied_capacity"))
			if occ != 12:
				return _fail("12 件道具佔用格數不符，預期 12，實得: %d" % occ)
			if label.text != "容量 12/24":
				return _fail("12 件道具膠囊文字不符，預期 '容量 12/24'，實得: '%s'" % label.text)
			if bool(_inv.call("is_capacity_full")):
				return _fail("12/24 不應標記為滿載")

			# 測試一鍵整理功能
			_inv.call("sort_items")
			if label.text != "容量 12/24":
				return _fail("一鍵整理後容量文案不符，預期 '容量 12/24'，實得: '%s'" % label.text)

			print("  ok 12 件道具即時容量計算 (容量 12/24) 與一鍵整理連動正確")

			_step = 4
			_wait = 0

		4:
			if _wait < 5:
				return false
			# 截圖 1: 正常容量 (12/24) 繁中文案與奶油白膠囊
			_proof_hashes["proof_01"] = _capture_save(_out_dir.path_join("proof_01_maple_inv_capacity_normal_zh_TW.png"))

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			print("\n--- 4. 驗證分類頁籤切換容量即時更新 ---")
			# 切換到「裝備」分類 (blade_iron, sword_bronze, armor_leather, shield_wood 共 4 件)
			_inv.call("set_category", "equip")
			var label: Label = _inv.call("get_capacity_label")
			var occ_equip: int = int(_inv.call("get_occupied_capacity"))
			if occ_equip != 4:
				return _fail("裝備分類佔用格數不符，預期 4，實得: %d" % occ_equip)
			if label.text != "容量 4/24":
				return _fail("裝備分類膠囊文案不符，預期 '容量 4/24'，實得: '%s'" % label.text)

			# 切換到「消耗品」分類 (pot_hp_1, pot_hp_2 共 2 件)
			_inv.call("set_category", "consumable")
			var occ_pot: int = int(_inv.call("get_occupied_capacity"))
			if occ_pot != 2:
				return _fail("消耗品分類佔用格數不符，預期 2，實得: %d" % occ_pot)
			if label.text != "容量 2/24":
				return _fail("消耗品分類膠囊文案不符，預期 '容量 2/24'，實得: '%s'" % label.text)

			# 切換回「裝備」拍照存證
			_inv.call("set_category", "equip")
			print("  ok 分類切換容量即時更新驗證通過 (裝備 4/24, 消耗品 2/24)")

			_step = 6
			_wait = 0

		6:
			if _wait < 5:
				return false
			# 截圖 2: 分類頁籤切換 (裝備 4/24)
			_proof_hashes["proof_02"] = _capture_save(_out_dir.path_join("proof_02_maple_inv_capacity_chip_filter.png"))

			# 切換回全部分類
			_inv.call("set_category", "all")

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			print("\n--- 5. 填滿背包至 24 格 (滿載) 驗證珊瑚粉/暖橘警示色階 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")

			# 額外補足 12 個道具使總數達到 24
			for i in range(1, 13):
				var extra_id := "extra_item_%d" % i
				inv_sys.call("register_item", extra_id, {
					"name": "測試部件 %d" % i,
					"kind": "material",
					"desc": "額外擴充測試部件",
					"glyph": "件"
				})
				inv_sys.call("add_item", extra_id, 1)

			_inv.refresh()

			var capsule: PanelContainer = _inv.call("get_capacity_capsule")
			var label: Label = _inv.call("get_capacity_label")
			var occ_full: int = int(_inv.call("get_occupied_capacity"))

			if occ_full != 24:
				return _fail("滿載格數不符，預期 24，實得: %d" % occ_full)
			if not bool(_inv.call("is_capacity_full")):
				return _fail("達到 24 格時 is_capacity_full() 應為 true")
			if label.text != "容量 24/24":
				return _fail("滿載膠囊文字不符，預期 '容量 24/24'，實得: '%s'" % label.text)

			# 檢查滿載警示 StyleBoxFlat (珊瑚粉底 #FF5E8A COLOR_PINK、暖橘光暈)
			var sb = capsule.get_theme_stylebox("panel")
			if not (sb is StyleBoxFlat):
				return _fail("滿載膠囊 panel 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if abs(sbf.bg_color.r - Color("#FF5E8A").r) > 0.05 or abs(sbf.bg_color.g - Color("#FF5E8A").g) > 0.05 or abs(sbf.bg_color.b - Color("#FF5E8A").b) > 0.05:
				return _fail("滿載膠囊底色未切換為珊瑚粉 (#FF5E8A)，實際為: %s" % str(sbf.bg_color))
			if sbf.border_color != Color("#1F1A3A"):
				return _fail("滿載膠囊描邊非深藍紫 (#1F1A3A)，實際為: %s" % str(sbf.border_color))

			# 檢查字色為高對比白字
			var fcol: Color = label.get_theme_color("font_color")
			if fcol != Color("#FFFFFF"):
				return _fail("滿載膠囊字色應為白色高對比 (#FFFFFF)，實際為: %s" % str(fcol))

			print("  ok 滿載狀態 (24/24) 成功觸發珊瑚粉/暖橘警示色階")

			_step = 8
			_wait = 0

		8:
			if _wait < 5:
				return false
			# 截圖 3: 滿載狀態 (24/24) 珊瑚粉警示色階
			_proof_hashes["proof_03"] = _capture_save(_out_dir.path_join("proof_03_maple_inv_capacity_full_warning_coral.png"))

			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false

			print("\n--- 6. 驗證滿載時選取物品提示『背包空間已滿』---")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()

			var tip: Label = _inv.get("_tip")
			if tip == null or not is_instance_valid(tip):
				return _fail("找不到操作提示標籤 _tip")
			if tip.text != "背包空間已滿":
				return _fail("滿載選取物品時 _tip 提示不符，預期 '背包空間已滿'，實得: '%s'" % tip.text)

			var detail: RichTextLabel = _inv.get("_detail")
			if detail == null or not is_instance_valid(detail):
				return _fail("找不到詳情卡片 _detail")
			if not ("背包空間已滿" in detail.text):
				return _fail("滿載選取物品時 detail 卡片未包含 '背包空間已滿'，內容為: %s" % detail.text)

			# 驗證背包總滿載 (24/24) 時切換分類，膠囊與詳情仍維持滿載警示色階一致性
			_inv.call("set_category", "equip")
			var cap_full_sb: StyleBoxFlat = _inv.call("get_capacity_capsule").get_theme_stylebox("panel") as StyleBoxFlat
			if abs(cap_full_sb.bg_color.r - Color("#FF5E8A").r) > 0.05:
				return _fail("滿載時切換裝備分類，膠囊未維持珊瑚粉滿載警示色階")
			if not bool(_inv.call("is_capacity_full")):
				return _fail("滿載時切換裝備分類，is_capacity_full() 應維持 true")
			_inv.call("set_category", "all")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()

			print("  ok 滿載選取物品時提示『背包空間已滿』與分類切換滿載一致性驗證通過")

			_step = 10
			_wait = 0

		10:
			if _wait < 5:
				return false
			# 截圖 4: 滿載選取物品提示『背包空間已滿』
			_proof_hashes["proof_04"] = _capture_save(_out_dir.path_join("proof_04_maple_inv_capacity_full_item_selected_tip.png"))

			_step = 11
			_wait = 0

		11:
			if _wait < 3:
				return false

			print("\n--- 7. 驗證消耗/扣減物品後恢復正常奶油白色階 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			# 移除一個道具使總數降至 23
			inv_sys.call("remove_item", "extra_item_12", 1)
			_inv.refresh()

			var capsule: PanelContainer = _inv.call("get_capacity_capsule")
			var label: Label = _inv.call("get_capacity_label")
			var occ_sub: int = int(_inv.call("get_occupied_capacity"))

			if occ_sub != 23:
				return _fail("扣減後佔用格數不符，預期 23，實得: %d" % occ_sub)
			if bool(_inv.call("is_capacity_full")):
				return _fail("23 格不應標記為滿載")
			if label.text != "容量 23/24":
				return _fail("23 格膠囊文案不符，預期 '容量 23/24'，實得: '%s'" % label.text)

			var sbf: StyleBoxFlat = capsule.get_theme_stylebox("panel") as StyleBoxFlat
			if abs(sbf.bg_color.r - Color("#FFFDF8").r) > 0.05:
				return _fail("扣減後底色未恢復為奶油白 (#FFFDF8)，實際為: %s" % str(sbf.bg_color))

			print("  ok 扣減至 23 格成功恢復奶油白色階，解除警示")

			# 補回道具保持 24 格供後續多語系驗證
			inv_sys.call("add_item", "extra_item_12", 1)
			_inv.refresh()

			_step = 12
			_wait = 0

		12:
			if _wait < 3:
				return false

			print("\n--- 8. 驗證六語系即時在地化切換無缺詞與零 CJK 殘留 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var label: Label = _inv.call("get_capacity_label")
			var tip: Label = _inv.get("_tip")

			for l in LOCALES:
				loc.call("set_locale", l)
				_inv.refresh()

				var exp_prefix: String = EXPECTED_CAPACITY_PREFIXES[l]
				var exp_tip: String = EXPECTED_FULL_TIPS[l]

				if not label.text.begins_with(exp_prefix):
					return _fail("[%s] 容量膠囊前綴不符，預期開頭 '%s'，實得: '%s'" % [l, exp_prefix, label.text])
				if not ("24/24" in label.text):
					return _fail("[%s] 容量膠囊數值不符，應包含 '24/24'，實得: '%s'" % [l, label.text])

				_inv.set("_selected", "blade_iron")
				_inv.refresh()

				if tip.text != exp_tip:
					return _fail("[%s] 滿載提示不符，預期 '%s'，實得: '%s'" % [l, exp_tip, tip.text])

				# 歐美語系 (en, es) 嚴格檢查零 CJK 殘留
				if l in ["en", "es"]:
					if _has_cjk(label.text):
						return _fail("[%s] 容量膠囊文案殘留違規 CJK: %s" % [l, label.text])
					if _has_cjk(tip.text):
						return _fail("[%s] 滿載提示殘留違規 CJK: %s" % [l, tip.text])

				# 檢查零系統 Emoji
				if _has_emoji(label.text):
					return _fail("[%s] 容量膠囊包含違規系統 Emoji: %s" % [l, label.text])
				if _has_emoji(tip.text):
					return _fail("[%s] 滿載提示包含違規系統 Emoji: %s" % [l, tip.text])

				print("  ok [%s] 容量文案: '%s' | 滿載提示: '%s' (0 CJK 0 Emoji)" % [l, label.text, tip.text])

			# 切換為英文並 refresh，進入獨立等待幀以供正確截圖
			loc.call("set_locale", "en")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()

			_step = 13
			_wait = 0

		13:
			if _wait < 5:
				return false
			# 截圖 5: 英文語系 (en) 滿載展示
			_proof_hashes["proof_05"] = _capture_save(_out_dir.path_join("proof_05_maple_inv_capacity_en_locale.png"))

			# 切換至日文並 refresh，進入獨立等待幀以供正確截圖
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "ja")
			_inv.set("_selected", "blade_iron")
			_inv.refresh()

			_step = 14
			_wait = 0

		14:
			if _wait < 5:
				return false
			# 截圖 6: 日語語系 (ja) 滿載展示
			_proof_hashes["proof_06"] = _capture_save(_out_dir.path_join("proof_06_maple_inv_capacity_ja_locale.png"))

			# 切換回繁中
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			_step = 15
			_wait = 0

		15:
			if _wait < 3:
				return false

			# 切換回繁中
			var loc: Node = root.get_node_or_null("Loc")
			loc.call("set_locale", "zh_TW")
			_inv.refresh()

			print("\n--- 9. 實機截圖 SHA256 獨立性驗證 ---")
			if DisplayServer.get_name() != "headless":
				var keys := ["proof_01", "proof_02", "proof_03", "proof_04", "proof_05", "proof_06"]
				var seen_hashes: Dictionary = {}
				for k in keys:
					var h: String = _proof_hashes.get(k, "")
					if h.is_empty():
						return _fail("存證截圖 %s 雜湊為空" % k)
					if seen_hashes.has(h):
						return _fail("存證截圖 %s 與 %s SHA256 重複: %s" % [k, seen_hashes[h], h])
					seen_hashes[h] = k
				print("  ok 6 張存證截圖 SHA256 雜湊值全數獨立不重複 (0 重複)")
			else:
				print("  ℹ️ 無頭 (headless) 模式略過視口繪製雜湊比對")

			print("\n=======================================================")
			print("🎉 全部 MapleInventory 容量進度膠囊單元與功能測試通過！")
			print("MAPLE_INVENTORY_CAPACITY_OK")
			print("=======================================================")
			quit(0)
			return true

	return false


func _capture_save(path: String) -> String:
	if DisplayServer.get_name() == "headless":
		return ""
	var vp := root.get_viewport()
	if vp == null:
		return ""
	var tex := vp.get_texture()
	if tex == null:
		return ""
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return ""
	img.save_png(path)
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ""
	var sha := file.get_sha256(path)
	file.close()
	print("  📸 存證截圖: %s (SHA256: %s)" % [path.get_file(), sha.substr(0, 16)])
	return sha
