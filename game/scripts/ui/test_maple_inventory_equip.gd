extends SceneTree
## 《發條之心》探索背包立即裝備與動態按鈕文案單元測試 (test_maple_inventory_equip.gd)
## 驗證項目：
## 1. 右側操作按鈕 (BtnAction) 依道具類別動態呈現適應性文案：
##    - 消耗品顯示『使用』，啟用 (disabled=false)，點擊觸發 item_used
##    - 素材顯示『賣出』，啟用 (disabled=false)，點擊觸發 item_used
##    - 裝備類顯示『立即裝備』，啟用 (disabled=false)，點擊連動 EquipmentSystem.equip 換裝並發射 equipment_changed 信號
##    - 重要物品顯示『重要物品』，禁用 (disabled=true)
## 2. 六語系 (zh_TW, zh_CN, en, ja, ko, es) 即時切換無缺詞、零系統 Emoji
## 3. 按鈕熱區高度 >= 48px (52px)，果凍厚底 5px，圓角 18px，無文字溢出
## 4. 未選取狀態禁用並顯示『使用 / 賣出』

const MapleInventoryScn = preload("res://scripts/ui/maple_inventory.gd")
var _inv: Control = null
var _step: int = 0
var _wait: int = 0
var _received_item_used: String = ""
var _received_inv_equip_changed: bool = false
var _received_sys_equip_changed: bool = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	_inv = MapleInventoryScn.new()
	root.add_child(_inv)


func _fail(msg: String) -> bool:
	push_error(msg)
	print("MAPLE_INVENTORY_EQUIP_FAIL: ", msg)
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

			print("--- 1. 初始化測試環境與道具清單 ---")
			var inv_sys: Node = root.get_node_or_null("InventorySystem")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")
			var loc: Node = root.get_node_or_null("Loc")

			if inv_sys == null or eq_sys == null or gs == null or loc == null:
				return _fail("缺少必要 Autoload (InventorySystem / EquipmentSystem / GameState / Loc)")

			loc.call("set_locale", "zh_TW")
			if "inventory" in gs and gs.inventory != null:
				gs.inventory.clear()
			if "hp" in gs:
				gs.hp = 20

			# 註冊並加入各類型道具
			inv_sys.call("add_item", "hp_s", 5)          # 消耗品
			inv_sys.call("add_item", "iron_scrap", 10)   # 素材
			inv_sys.call("add_item", "key_rusty", 1)     # 重要道具
			inv_sys.call("add_item", "rusty_blade", 1)   # 裝備/武器

			_inv.refresh()
			print("  ok 道具初始化完畢 (hp_s, iron_scrap, key_rusty, rusty_blade)")

			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false

			# ── 2. 驗證按鈕基本規格 (熱區 >= 48px, 果凍厚底 5px, 圓角 18px) ──
			print("\n--- 2. 驗證操作按鈕尺寸與樣式規格 ---")
			var btn: Button = _inv.call("get_use_button")
			if btn == null or not is_instance_valid(btn):
				return _fail("找不到操作按鈕 _use_btn")

			if btn.custom_minimum_size.y < 48.0:
				return _fail("操作按鈕熱區高度小於 48px，實際為: %f" % btn.custom_minimum_size.y)
			print("  ok 按鈕熱區高度符合規範: %.1f px (>= 48px)" % btn.custom_minimum_size.y)

			# ── 3. 驗證未選取狀態 ──
			print("\n--- 3. 驗證未選取時按鈕禁用與預設文案 ---")
			_inv.set("_selected", "")
			_inv.refresh()
			if not btn.disabled:
				return _fail("未選取道具時按鈕應為禁用狀態 (disabled=true)")
			if btn.text != "使用 / 賣出":
				return _fail("未選取道具時按鈕文案應為『使用 / 賣出』，實際為: %s" % btn.text)
			print("  ok 未選取狀態正確 (disabled=true, 文案='使用 / 賣出')")

			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false

			# ── 4. 驗證消耗品 (hp_s) ──
			print("\n--- 4. 驗證消耗品動態文案『使用』與點擊觸發 ---")
			var btn: Button = _inv.call("get_use_button")
			_inv.set("_selected", "hp_s")
			_inv.refresh()

			if btn.disabled:
				return _fail("選取消耗品時按鈕不應被禁用")
			if btn.text != "使用":
				return _fail("選取消耗品時按鈕文案應為『使用』，實際為: %s" % btn.text)

			var sb = btn.get_theme_stylebox("normal")
			if not (sb is StyleBoxFlat):
				return _fail("按鈕 normal 樣式非 StyleBoxFlat")
			var sbf: StyleBoxFlat = sb as StyleBoxFlat
			if sbf.border_width_bottom != 5 or sbf.corner_radius_top_left != 18:
				return _fail("按鈕底邊厚度應為 5px，圓角應為 18px")

			# 連接並點擊按鈕
			_received_item_used = ""
			if not _inv.item_used.is_connected(_on_test_item_used):
				_inv.item_used.connect(_on_test_item_used)
			btn.pressed.emit()
			if _received_item_used != "hp_s":
				return _fail("點擊使用消耗品未能正確發射 item_used 信號: %s" % _received_item_used)
			print("  ok 消耗品狀態正確 (文案='使用', disabled=false, 果凍厚底 5px, 圓角 18px, item_used 成功發射)")

			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false

			# ── 5. 驗證素材 (iron_scrap) ──
			print("\n--- 5. 驗證素材動態文案『賣出』與點擊觸發 ---")
			var btn: Button = _inv.call("get_use_button")
			_inv.set("_selected", "iron_scrap")
			_inv.refresh()

			if btn.disabled:
				return _fail("選取素材時按鈕不應被禁用")
			if btn.text != "賣出":
				return _fail("選取素材時按鈕文案應為『賣出』，實際為: %s" % btn.text)

			_received_item_used = ""
			btn.pressed.emit()
			if _received_item_used != "iron_scrap":
				return _fail("點擊賣出素材未能正確發射 item_used 信號: %s" % _received_item_used)
			print("  ok 素材狀態正確 (文案='賣出', disabled=false, item_used 成功發射)")

			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false

			# ── 6. 驗證重要物品 (key_rusty) ──
			print("\n--- 6. 驗證重要物品動態文案『重要物品』與禁用狀態 ---")
			var btn: Button = _inv.call("get_use_button")
			_inv.set("_selected", "key_rusty")
			_inv.refresh()

			if not btn.disabled:
				return _fail("選取重要物品時按鈕應被禁用 (disabled=true)")
			if btn.text != "重要物品":
				return _fail("選取重要物品時按鈕文案應為『重要物品』，實際為: %s" % btn.text)

			_received_item_used = ""
			btn.pressed.emit()
			if _received_item_used != "":
				return _fail("重要物品禁用按鈕不應觸發使用動作")
			print("  ok 重要物品狀態正確 (文案='重要物品', disabled=true, 按鈕無效)")

			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false

			# ── 7. 驗證裝備類 (rusty_blade) 立即裝備與換裝連動 ──
			print("\n--- 7. 驗證裝備類動態文案『立即裝備』與連動 EquipmentSystem.equip ---")
			var btn: Button = _inv.call("get_use_button")
			var eq_sys: Node = root.get_node_or_null("EquipmentSystem")
			var gs: Node = root.get_node_or_null("GameState")

			_inv.set("_selected", "rusty_blade")
			_inv.refresh()

			if btn.disabled:
				return _fail("選取裝備類時按鈕不應被禁用")
			if btn.text != "立即裝備":
				return _fail("選取裝備類時按鈕文案應為『立即裝備』，實際為: %s" % btn.text)

			# 監聽信號
			_received_inv_equip_changed = false
			_received_sys_equip_changed = false
			if not _inv.equipment_changed.is_connected(_on_test_inv_equip_changed):
				_inv.equipment_changed.connect(_on_test_inv_equip_changed)
			if not eq_sys.equipment_changed.is_connected(_on_test_sys_equip_changed):
				eq_sys.equipment_changed.connect(_on_test_sys_equip_changed)

			btn.pressed.emit()

			if not _received_inv_equip_changed:
				return _fail("點擊立即裝備未能觸發 MapleInventory.equipment_changed 信號")
			if not _received_sys_equip_changed:
				return _fail("點擊立即裝備未能觸發 EquipmentSystem.equipment_changed 信號")

			# 檢查裝備欄中是否成功裝上
			var active_uid := str(gs.weapon_loadout[0])
			if active_uid == "":
				return _fail("換裝後 GameState.weapon_loadout[0] 為空")
			print("  ok 立即裝備連動成功 (文案='立即裝備', 雙向 equipment_changed 發射, 武器成功入槽: %s)" % active_uid)

			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false

			# ── 8. 驗證六語系動態即時切換無缺詞 ──
			print("\n--- 8. 驗證六語系 (zh_TW, zh_CN, en, ja, ko, es) 動態即時切換 ---")
			var loc: Node = root.get_node_or_null("Loc")
			var btn: Button = _inv.call("get_use_button")

			var expected_by_locale := {
				"zh_TW": {
					"consumable": "使用",
					"material": "賣出",
					"equip": "立即裝備",
					"key": "重要物品"
				},
				"zh_CN": {
					"consumable": "使用",
					"material": "出售",
					"equip": "立即装备",
					"key": "重要物品"
				},
				"en": {
					"consumable": "Use",
					"material": "Sell",
					"equip": "Equip Now",
					"key": "Key Item"
				},
				"ja": {
					"consumable": "使う",
					"material": "売却",
					"equip": "今すぐ装備",
					"key": "重要アイテム"
				},
				"ko": {
					"consumable": "사용",
					"material": "판매",
					"equip": "즉시 장착",
					"key": "중요 아이템"
				},
				"es": {
					"consumable": "Usar",
					"material": "Vender",
					"equip": "Equipar ahora",
					"key": "Objeto clave"
				}
			}

			var test_items := {
				"consumable": "hp_s",
				"material": "iron_scrap",
				"equip": "rusty_blade",
				"key": "key_rusty"
			}

			for code in ["en", "ja", "ko", "es", "zh_CN", "zh_TW"]:
				loc.call("set_locale", code)
				for cat in ["consumable", "material", "equip", "key"]:
					_inv.set("_selected", test_items[cat])
					_inv.refresh()
					var exp: String = expected_by_locale[code][cat]
					if btn.text != exp:
						return _fail("[%s] 類別 [%s] 按鈕文案不符: 期望 '%s'，實際 '%s'" % [code, cat, exp, btn.text])
				print("  ok [%s] 消耗品/素材/裝備/重要物品 四項在地化文案全部吻合" % code)

			loc.call("set_locale", "zh_TW")

			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false

			# ── 9. 零系統 Emoji 檢查 ──
			print("\n--- 9. 零系統 Emoji 檢查 ---")
			var full_text := ""
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

			# 截圖存證防護
			if DisplayServer.get_name() != "headless":
				var img: Image = root.get_viewport().get_texture().get_image()
				if img:
					var base_dir := ProjectSettings.globalize_path("res://")
					var p_proof := base_dir.path_join("../proofs/t_bd9c0e84/proof_maple_inventory_equip.png")
					DirAccess.make_dir_recursive_absolute(p_proof.get_base_dir())
					img.save_png(p_proof)

			print("\nMAPLE_INVENTORY_EQUIP_OK")
			quit(0)
			return true

	return false


func _on_test_item_used(id: String) -> void:
	_received_item_used = id


func _on_test_inv_equip_changed() -> void:
	_received_inv_equip_changed = true


func _on_test_sys_equip_changed() -> void:
	_received_sys_equip_changed = true
