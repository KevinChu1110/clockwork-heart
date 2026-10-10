extends SceneTree
## 《發條之心》探索背包一鍵整理功能與果凍按鈕測試 (test_maple_inventory_sort.gd)
## 驗證項目：
## 1. 一鍵整理按鈕 (BtnSortItems) 存在、尺寸 120x48px、熱區 >= 48px、金黃果凍厚底 5px
## 2. 六語系 (en, ja, ko, es, zh_CN, zh_TW) 在地化文字即時切換無缺詞、零系統 Emoji
## 3. 背包物品排序邏輯驗證：依裝備/寶石/消耗品/材料分類優先序及品質降序排列
## 4. 點擊後介面即時刷新、各格子內容連動正確、無 SCRIPT ERROR

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
	print("MAPLE_INVENTORY_SORT_FAIL: ", msg)
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

			# ── 1. 驗證一鍵整理按鈕 (BtnSortItems) 存在與尺寸規格 ──
			print("--- 1. 驗證一鍵整理按鈕規格 ---")
			var sort_btn: Button = _inv.find_child("BtnSortItems", true, false)
			if sort_btn == null:
				return _fail("找不到 BtnSortItems 按鈕節點")

			if sort_btn.custom_minimum_size.x != 120.0 or sort_btn.custom_minimum_size.y != 48.0:
				return _fail("BtnSortItems 尺寸不符合 120x48px，實際為: %s" % str(sort_btn.custom_minimum_size))
			print("  ok BtnSortItems 尺寸符合 120x48px (熱區 >= 48px)")

			# 驗證 StyleBoxFlat 果凍厚底 5px
			var normal_sb = sort_btn.get_theme_stylebox("normal")
			if not (normal_sb is StyleBoxFlat):
				return _fail("BtnSortItems normal stylebox 應為 StyleBoxFlat")
			var sb_flat: StyleBoxFlat = normal_sb as StyleBoxFlat
			if sb_flat.border_width_bottom != 5:
				return _fail("BtnSortItems 果凍底厚度應為 5px，實際為: %d" % sb_flat.border_width_bottom)
			print("  ok BtnSortItems 果凍底厚度符合 5px 規範")

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
			print("\n--- 2. 驗證六語系在地化文字切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			if loc == null:
				return _fail("找不到 Loc autoload 節點")

			var sort_btn: Button = _inv.find_child("BtnSortItems", true, false)
			var expected_texts := {
				"en": "Auto-Sort",
				"ja": "一括整理",
				"ko": "자동 정리",
				"es": "Organizar",
				"zh_CN": "一键整理",
				"zh_TW": "一鍵整理"
			}

			for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
				loc.call("set_locale", code)
				var expected: String = expected_texts[code]
				if sort_btn.text != expected:
					return _fail("[%s] 語系一鍵整理按鈕文字錯誤: 期望 '%s'，實際 '%s'" % [code, expected, sort_btn.text])
				print("  ok [%s] 一鍵整理按鈕文字符合: %s" % [code, sort_btn.text])

			loc.call("set_locale", "zh_TW")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			# ── 3. 驗證物品分類優先序與品質降序排列邏輯 ──
			print("\n--- 3. 驗證物品排序邏輯（裝備/寶石/消耗品/材料優先序及品質降序）---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			if inv_sys == null:
				return _fail("找不到 InventorySystem 節點")

			# 清除既有背包
			var gs: Node = root.get_node_or_null("GameState")
			if gs and "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()

			# 註冊涵蓋四分類與多種品質的測試道具
			# (1) 裝備 (kind: weapon / equipment) - 分類 1
			inv_sys.call("register_item", "t_w_epic", {"name": "赤金重刃", "kind": "weapon", "quality": "epic", "desc": "史詩武器"})
			inv_sys.call("register_item", "t_w_rare", {"name": "黃銅佩劍", "kind": "weapon", "quality": "rare", "desc": "稀有武器"})
			inv_sys.call("register_item", "t_eq_common", {"name": "舊鐵甲片", "kind": "equipment", "quality": "common", "desc": "凡品防具"})

			# (2) 寶石 (kind: gem) - 分類 2
			inv_sys.call("register_item", "t_gem_epic", {"name": "星耀璀璨寶石", "kind": "gem", "quality": "epic", "desc": "史詩寶石"})
			inv_sys.call("register_item", "t_gem_rare", {"name": "緋紅赤血寶石", "kind": "gem", "quality": "rare", "desc": "稀有寶石"})
			inv_sys.call("register_item", "t_gem_common", {"name": "原礦粗磨寶石", "kind": "gem", "level": 1, "desc": "1級普通寶石"})

			# (3) 消耗品 (kind: consumable) - 分類 3
			inv_sys.call("register_item", "t_pot_epic", {"name": "天宮靈泉", "kind": "consumable", "quality": "epic", "desc": "史詩藥水"})
			inv_sys.call("register_item", "t_pot_uncommon", {"name": "精煉潤滑油", "kind": "consumable", "quality": "uncommon", "desc": "良品藥水"})
			inv_sys.call("register_item", "t_pot_common", {"name": "微光潤滑油", "kind": "consumable", "quality": "common", "desc": "凡品藥水"})

			# (4) 材料 (kind: material) - 分類 4
			inv_sys.call("register_item", "t_mat_rare", {"name": "高階發條晶砂", "kind": "material", "quality": "rare", "desc": "稀有材料"})
			inv_sys.call("register_item", "t_mat_common", {"name": "基礎鍛造鐵屑", "kind": "material", "quality": "common", "desc": "凡品材料"})

			# (5) 其他/重要道具 (kind: key) - 分類 5
			inv_sys.call("register_item", "t_key_item", {"name": "古老發條鑰匙", "kind": "key", "desc": "重要道具"})

			# 故意以打亂的順序加入背包
			inv_sys.call("add_item", "t_mat_common", 5)
			inv_sys.call("add_item", "t_pot_uncommon", 2)
			inv_sys.call("add_item", "t_gem_common", 1)
			inv_sys.call("add_item", "t_w_rare", 1)
			inv_sys.call("add_item", "t_key_item", 1)
			inv_sys.call("add_item", "t_pot_epic", 1)
			inv_sys.call("add_item", "t_w_epic", 1)
			inv_sys.call("add_item", "t_gem_rare", 1)
			inv_sys.call("add_item", "t_mat_rare", 3)
			inv_sys.call("add_item", "t_eq_common", 1)
			inv_sys.call("add_item", "t_gem_epic", 1)
			inv_sys.call("add_item", "t_pot_common", 4)

			# 刷新未排序狀態
			_inv.refresh()
			var bag_ids_before: Array = _inv.get("_bag_ids")
			print("  未排序前第 0 格物品 ID: %s" % (bag_ids_before[0] if bag_ids_before.size() > 0 else "無"))

			# 點擊「一鍵整理」按鈕
			var sort_btn: Button = _inv.find_child("BtnSortItems", true, false)
			sort_btn.pressed.emit()

			# 驗證排序後狀態
			if not _inv.call("is_sorted"):
				return _fail("點擊一鍵整理後 _inv.is_sorted 應為 true")

			var bag_ids_after: Array = _inv.get("_bag_ids")

			# 預期的嚴格排列順序：
			# 裝備 (t_w_epic, t_w_rare, t_eq_common)
			# 寶石 (t_gem_epic, t_gem_rare, t_gem_common)
			# 消耗品 (t_pot_epic, t_pot_uncommon, t_pot_common)
			# 材料 (t_mat_rare, t_mat_common)
			# 其他 (t_key_item)
			var expected_sorted_ids := [
				"t_w_epic",       # 裝備 · epic (4)
				"t_w_rare",       # 裝備 · rare (3)
				"t_eq_common",    # 裝備 · common (1)
				"t_gem_epic",     # 寶石 · epic (4)
				"t_gem_rare",     # 寶石 · rare (3)
				"t_gem_common",   # 寶石 · common/lvl 1
				"t_pot_epic",     # 消耗品 · epic (4)
				"t_pot_uncommon", # 消耗品 · uncommon (2)
				"t_pot_common",   # 消耗品 · common (1)
				"t_mat_rare",     # 材料 · rare (3)
				"t_mat_common",   # 材料 · common (1)
				"t_key_item"      # 其他/重要道具
			]

			for idx in range(expected_sorted_ids.size()):
				var expected_id: String = expected_sorted_ids[idx]
				var actual_id: String = str(bag_ids_after[idx])
				if actual_id != expected_id:
					return _fail("排序後第 %d 格物品錯誤: 預期 '%s'，實際 '%s' (完整順序: %s)" % [
						idx, expected_id, actual_id, str(bag_ids_after.slice(0, expected_sorted_ids.size()))
					])
				print("  ok 格子 [%02d] -> %s (分類與品質降序完全正確)" % [idx, actual_id])

			# 驗證介面即時連動：選取第一個物品 (t_w_epic)，詳情名稱應為「赤金重刃」
			_inv.call("_on_cell", 0, MOUSE_BUTTON_LEFT)
			var detail_name_lbl: Label = _inv.get("_detail_name")
			if detail_name_lbl == null or detail_name_lbl.text != "赤金重刃":
				return _fail("排序後點選第 0 格 (t_w_epic) 詳情標題未連動，實際為: %s" % (detail_name_lbl.text if detail_name_lbl else "null"))
			print("  ok 排序後格子選取與詳情面板即時連動正確: %s" % detail_name_lbl.text)

			# 驗證無頭截圖防護與保存截圖
			if DisplayServer.get_name() != "headless":
				var img: Image = root.get_viewport().get_texture().get_image()
				if img:
					var p_proof := ProjectSettings.globalize_path("res://../proofs/t_604b6c45/proof_maple_inventory_sort.png")
					DirAccess.make_dir_recursive_absolute(p_proof.get_base_dir())
					img.save_png(p_proof)
					print("  ok 實機截圖存證成功: %s" % p_proof)

			print("\nMAPLE_INVENTORY_SORT_OK")
			quit(0)
			return true

	return false
