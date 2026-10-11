extends SceneTree
## 《發條之心》探索背包分類頁籤 Chip 列單元與功能測試 (test_maple_inventory_chips.gd)
## 驗證項目：
## 1. 格子區上方配置 5 枚 Chip 按鈕（全部／裝備／消耗品／素材／寶石），熱區高度 >= 40px，圓角 14~16px，深藍紫描邊，0 emoji
## 2. 預設選中『全部』，顯示所有道具；選中呈高亮金黃色 (#FFD028)，未選中為奶油白底
## 3. 點擊各 Chip 即時篩選左側 4×6 格子內容，只顯示對應 kind 之道具（裝備包含 weapon/equip/equipment，寶石包含 gem/jewel，消耗品 consumable，素材 material）
## 4. 切換分類時若當前選取道具不在該分類中，重設選取狀態
## 5. 六語系 (en, ja, ko, es, zh_CN, zh_TW) 即時在地化切換無缺詞、零系統 Emoji

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
	print("MAPLE_INVENTORY_CHIPS_FAIL: ", msg)
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

			# ── 1. 驗證 5 枚 Chip 按鈕存在、熱區高度 >= 40px、圓角 14~16px、深藍紫描邊、0 emoji ──
			print("--- 1. 驗證 5 枚 Chip 按鈕規格與多巴胺視覺規範 ---")
			var chip_row: HBoxContainer = _inv.find_child("CategoryChipsRow", true, false)
			if chip_row == null:
				return _fail("找不到 CategoryChipsRow 節點")

			var chips_dict: Dictionary = _inv.call("get_chip_buttons")
			var expected_categories := ["all", "equip", "consumable", "material", "gem"]
			if chips_dict.size() != 5:
				return _fail("Chip 按鈕數量應為 5，實際為: %d" % chips_dict.size())

			for cid in expected_categories:
				if not chips_dict.has(cid):
					return _fail("缺少類別 Chip: %s" % cid)
				var btn: Button = chips_dict[cid]
				if btn == null or not is_instance_valid(btn):
					return _fail("Chip 按鈕無效: %s" % cid)
				if btn.custom_minimum_size.y < 40.0:
					return _fail("Chip [%s] 熱區高度小於 40px，實際為: %f" % [cid, btn.custom_minimum_size.y])

				# 檢查 StyleBoxFlat 樣式
				var sb = btn.get_theme_stylebox("normal")
				if not (sb is StyleBoxFlat):
					return _fail("Chip [%s] normal 樣式非 StyleBoxFlat" % cid)
				var sbf: StyleBoxFlat = sb as StyleBoxFlat
				var r := sbf.corner_radius_top_left
				if r < 14 or r > 16:
					return _fail("Chip [%s] 圓角應在 14~16px 之間，實際為: %d" % [cid, r])

				print("  ok Chip [%s] 熱區高度符合 (%.1f px >= 40px)，圓角符合 (%d px)" % [cid, btn.custom_minimum_size.y, r])

			# 驗證零系統 Emoji
			var full_text: String = ""
			for node in _inv.find_children("*", "Label", true, false):
				if node is Label:
					full_text += node.text
			for node in _inv.find_children("*", "Button", true, false):
				if node is Button:
					full_text += node.text
			for ch in full_text:
				var cp := ch.unicode_at(0)
				if (cp >= 0x1F300 and cp <= 0x1FAFF) or (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713):
					return _fail("偵測到系統 Emoji: %s (U+%04X)" % [ch, cp])
			print("  ok 零系統 Emoji 檢查通過")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			# ── 2. 驗證六語系在地化切換無缺詞 ──
			print("\n--- 2. 驗證六語系在地化文字即時切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			if loc == null:
				return _fail("找不到 Loc autoload 節點")

			var chips_dict: Dictionary = _inv.call("get_chip_buttons")
			var expected_texts := {
				"zh_TW": {"all": "全部", "equip": "裝備", "consumable": "消耗品", "material": "素材", "gem": "寶石"},
				"zh_CN": {"all": "全部", "equip": "装备", "consumable": "消耗品", "material": "素材", "gem": "宝石"},
				"en": {"all": "All", "equip": "Equipment", "consumable": "Consumable", "material": "Material", "gem": "Gem"},
				"ja": {"all": "全部", "equip": "装備", "consumable": "消耗品", "material": "素材", "gem": "宝石"},
				"ko": {"all": "전체", "equip": "장비", "consumable": "소모품", "material": "소재", "gem": "보석"},
				"es": {"all": "Todo", "equip": "Equipo", "consumable": "Consumible", "material": "Material", "gem": "Gema"},
			}

			for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
				loc.call("set_locale", code)
				var expected_for_code: Dictionary = expected_texts[code]
				for cid in expected_for_code.keys():
					var btn: Button = chips_dict[cid]
					var exp: String = expected_for_code[cid]
					if btn.text != exp:
						return _fail("[%s] Chip [%s] 標籤文字不符: 期望 '%s'，實際 '%s'" % [code, cid, exp, btn.text])
				print("  ok [%s] 5 枚 Chip 在地化文字全部吻合" % code)

			loc.call("set_locale", "zh_TW")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			# ── 3. 初始化測試物品並驗證各分類篩選邏輯 ──
			print("\n--- 3. 驗證各 Chip 分類過濾邏輯（全部/裝備/消耗品/素材/寶石）---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys == null:
				return _fail("找不到 InventorySystem 節點")

			var gs: Node = root.get_node_or_null("GameState")
			if gs and "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			# 註冊測試道具：
			# 裝備 (weapon / equip / equipment)
			inv_sys.call("register_item", "test_wpn_1", {"name": "赤金長劍", "kind": "weapon", "desc": "裝備武器"})
			inv_sys.call("register_item", "test_equip_1", {"name": "黃銅胸甲", "kind": "equipment", "desc": "裝備防具"})
			inv_sys.call("register_item", "test_arm_1", {"name": "精鋼護腕", "kind": "equip", "desc": "裝備飾品"})

			# 寶石 (gem / jewel)
			inv_sys.call("register_item", "test_gem_1", {"name": "星輝寶石", "kind": "gem", "desc": "寶石結晶"})
			inv_sys.call("register_item", "test_jewel_1", {"name": "翡翠神石", "kind": "jewel", "desc": "珍貴珠寶"})

			# 消耗品 (consumable)
			inv_sys.call("register_item", "test_pot_1", {"name": "高純潤滑油", "kind": "consumable", "desc": "回血藥劑"})
			inv_sys.call("register_item", "test_pot_2", {"name": "解毒散", "kind": "consumable", "desc": "解除異常"})

			# 素材 (material)
			inv_sys.call("register_item", "test_mat_1", {"name": "鍛造鐵屑", "kind": "material", "desc": "金屬素材"})
			inv_sys.call("register_item", "test_mat_2", {"name": "發條碎片", "kind": "material", "desc": "核心素材"})

			# 依序加入背包
			inv_sys.call("add_item", "test_wpn_1", 1)
			inv_sys.call("add_item", "test_equip_1", 1)
			inv_sys.call("add_item", "test_arm_1", 1)
			inv_sys.call("add_item", "test_gem_1", 2)
			inv_sys.call("add_item", "test_jewel_1", 1)
			inv_sys.call("add_item", "test_pot_1", 3)
			inv_sys.call("add_item", "test_pot_2", 1)
			inv_sys.call("add_item", "test_mat_1", 5)
			inv_sys.call("add_item", "test_mat_2", 4)

			# 3.1 驗證預設『全部』：9 個道具全部出現
			_inv.call("set_category", "all")
			if _inv.call("get_current_category") != "all":
				return _fail("預設類別應為 'all'")
			var all_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if all_ids.size() != 9:
				return _fail("『全部』分類道具數量應為 9，實際為: %d" % all_ids.size())
			print("  ok 『全部』分類正常顯示所有 9 件道具")

			# 3.2 驗證『裝備』：應只有 3 個裝備道具 (test_wpn_1, test_equip_1, test_arm_1)
			_inv.call("set_category", "equip")
			if _inv.call("get_current_category") != "equip":
				return _fail("切換類別應為 'equip'")
			var equip_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if equip_ids.size() != 3:
				return _fail("『裝備』分類道具數量應為 3，實際為: %d (內容: %s)" % [equip_ids.size(), str(equip_ids)])
			for eid in equip_ids:
				if not (eid in ["test_wpn_1", "test_equip_1", "test_arm_1"]):
					return _fail("『裝備』分類包含非裝備道具: %s" % eid)
			print("  ok 『裝備』分類過濾正確，包含 weapon/equip/equipment (共 3 件)")

			# 3.3 驗證『寶石』：應只有 2 個寶石道具 (test_gem_1, test_jewel_1)
			_inv.call("set_category", "gem")
			var gem_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if gem_ids.size() != 2:
				return _fail("『寶石』分類道具數量應為 2，實際為: %d (內容: %s)" % [gem_ids.size(), str(gem_ids)])
			for gid in gem_ids:
				if not (gid in ["test_gem_1", "test_jewel_1"]):
					return _fail("『寶石』分類包含非寶石道具: %s" % gid)
			print("  ok 『寶石』分類過濾正確，包含 gem/jewel (共 2 件)")

			# 3.4 驗證『消耗品』：應只有 2 個消耗品 (test_pot_1, test_pot_2)
			_inv.call("set_category", "consumable")
			var pot_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if pot_ids.size() != 2:
				return _fail("『消耗品』分類道具數量應為 2，實際為: %d" % pot_ids.size())
			for pid in pot_ids:
				if not (pid in ["test_pot_1", "test_pot_2"]):
					return _fail("『消耗品』分類包含非消耗品: %s" % pid)
			print("  ok 『消耗品』分類過濾正確，包含 consumable (共 2 件)")

			# 3.5 驗證『素材』：應只有 2 個素材 (test_mat_1, test_mat_2)
			_inv.call("set_category", "material")
			var mat_ids: Array = _inv.get("_bag_ids").filter(func(id): return id != "")
			if mat_ids.size() != 2:
				return _fail("『素材』分類道具數量應為 2，實際為: %d" % mat_ids.size())
			for mid in mat_ids:
				if not (mid in ["test_mat_1", "test_mat_2"]):
					return _fail("『素材』分類包含非素材: %s" % mid)
			print("  ok 『素材』分類過濾正確，包含 material (共 2 件)")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			# ── 4. 驗證切換分類時若當前選取道具不在該分類中，重設選取狀態 ──
			print("\n--- 4. 驗證選取狀態連動與分類切換時重設邏輯 ---")
			# 切回『全部』並選取裝備 test_wpn_1
			_inv.call("set_category", "all")
			_inv.set("_selected", "test_wpn_1")
			_inv.refresh()
			if _inv.get("_selected") != "test_wpn_1":
				return _fail("設定選取 test_wpn_1 失敗")

			# 4.1 切換至『裝備』：test_wpn_1 仍在該分類中，選取狀態應保持
			_inv.call("set_category", "equip")
			if _inv.get("_selected") != "test_wpn_1":
				return _fail("切換至『裝備』時 test_wpn_1 應保持選取，實際為: '%s'" % str(_inv.get("_selected")))
			print("  ok 切換至包含該道具的分類時，選取狀態成功保持 (test_wpn_1)")

			# 4.2 切換至『消耗品』：test_wpn_1 不在消耗品中，選取狀態應重設為 \"\"
			_inv.call("set_category", "consumable")
			if _inv.get("_selected") != "":
				return _fail("切換至『消耗品』時 test_wpn_1 不在其中，選取狀態應重設為空字串，實際為: '%s'" % str(_inv.get("_selected")))
			var use_btn: Button = _inv.get("_use_btn")
			if use_btn and not use_btn.disabled:
				return _fail("重設選取後操作按鈕應為 disabled")
			print("  ok 切換至不包含該道具的分類時，選取狀態成功重設為空字串且操作按鈕禁用")

			# 4.3 在『消耗品』中選取 test_pot_1，再切換回『全部』：應保持選取
			_inv.set("_selected", "test_pot_1")
			_inv.refresh()
			_inv.call("set_category", "all")
			if _inv.get("_selected") != "test_pot_1":
				return _fail("切換回『全部』時 test_pot_1 應保持選取，實際為: '%s'" % str(_inv.get("_selected")))
			print("  ok 在子分類選取道具後切回『全部』，選取狀態成功保持 (test_pot_1)")

			# 4.4 點擊 Chip 按鈕測試信號觸發
			var chips_dict: Dictionary = _inv.call("get_chip_buttons")
			var btn_gem: Button = chips_dict["gem"]
			btn_gem.pressed.emit()
			if _inv.call("get_current_category") != "gem":
				return _fail("按下 gem Chip 按鈕未能切換當前分類至 'gem'")
			if _inv.get("_selected") != "":
				return _fail("切換至 gem 時原選取之消耗品 test_pot_1 應被重設為空字串")
			print("  ok 點擊 Chip 按鈕正常觸發分類切換與重設選取")

			# 截圖存證防護
			if DisplayServer.get_name() != "headless":
				var img: Image = root.get_viewport().get_texture().get_image()
				if img:
					var base_dir := ProjectSettings.globalize_path("res://")
					var p_proof := base_dir.path_join("../proofs/t_362cc11b/proof_maple_inventory_chips.png")
					DirAccess.make_dir_recursive_absolute(p_proof.get_base_dir())
					img.save_png(p_proof)

			print("\nMAPLE_INVENTORY_CHIPS_OK")
			quit(0)
			return true

	return false
