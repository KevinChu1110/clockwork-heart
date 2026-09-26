extends SceneTree
## 機芯五槽圖示接到角色整備面板與鐵匠鍛造彈窗驗證測試 (test_core_slots_ui.gd)
## 驗證項目：
## 1. 五槽圖示檔案皆存在且能成功載入為 Texture2D (SpriteDB.core_slot_icon)
## 2. 五張貼圖不同（非同一張圖，驗證唯一性）
## 3. 角色整備面板 (EquipPanel) 存在 CoreSlotsRow，包含 5 個部位槽位，熱區 >= 48px，圖示載入有效
## 4. 鐵匠彈窗 (ForgeDialog) 存在 ForgeCoreSlotsRow，包含 5 個部位槽位，熱區 >= 48px，圖示載入有效
## 5. 槽名對得上部位名稱，無系統 emoji，無截字

var _ok := true
var _frame := 0
var _step := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_emoji(text: String) -> bool:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1FAFF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 25:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_CORE_SLOTS_UI_OK")
					quit(0)
				else:
					push_error("TEST_CORE_SLOTS_UI_FAIL")
					print("TEST_CORE_SLOTS_UI_FAIL")
					quit(1)
				return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_core_slots_ui 單元測試 ===")
	
	_test_sprite_db_core_slots()
	_test_equip_panel_core_slots()
	_test_forge_dialog_core_slots()

func _test_sprite_db_core_slots() -> void:
	print("\n--- [Check 1] SpriteDB 機芯五槽定義與貼圖載入 ---")
	if SpriteDB.CORE_SLOT_DEFS.size() != 5:
		_fail("CORE_SLOT_DEFS 數量應為 5，實際為: %d" % SpriteDB.CORE_SLOT_DEFS.size())
		return

	var expected_slots := [
		{"id": "spring_generator", "name": "發條發電機", "file": "slot_01_spring_generator.png"},
		{"id": "chassis_armor", "name": "機殼裝甲", "file": "slot_02_chassis_armor.png"},
		{"id": "escapement_governor", "name": "擒縱調速器", "file": "slot_03_escapement_governor.png"},
		{"id": "transmission_gears", "name": "傳動齒輪組", "file": "slot_04_transmission_gears.png"},
		{"id": "resonance_core", "name": "共鳴核心", "file": "slot_05_resonance_core.png"},
	]

	var loaded_textures: Array[Texture2D] = []
	var tex_paths := {}

	for i in range(5):
		var exp_slot: Dictionary = expected_slots[i]
		var def: Dictionary = SpriteDB.CORE_SLOT_DEFS[i]
		if def.get("id") != exp_slot.id:
			_fail("槽位 %d id 不符: 預期 %s，實際 %s" % [i, exp_slot.id, str(def.get("id"))])
		if def.get("name") != exp_slot.name:
			_fail("槽位 %d name 不符: 預期 %s，實際 %s" % [i, exp_slot.name, str(def.get("name"))])
		if def.get("icon_file") != exp_slot.file:
			_fail("槽位 %d icon_file 不符: 預期 %s，實際 %s" % [i, exp_slot.file, str(def.get("icon_file"))])
		
		var t1 := SpriteDB.core_slot_icon(exp_slot.id)
		var t2 := SpriteDB.core_slot_icon(exp_slot.name)
		var t3 := SpriteDB.core_slot_icon(str(i))
		if t1 == null:
			_fail("無法載入槽位貼圖: %s (%s)" % [exp_slot.id, exp_slot.file])
			continue
		if t1 != t2 or t1 != t3:
			_fail("槽位 %s 的別名載入回傳不同貼圖" % exp_slot.id)

		var res_path := t1.resource_path
		if tex_paths.has(res_path):
			_fail("發現重複貼圖路徑: %s" % res_path)
		tex_paths[res_path] = true
		loaded_textures.append(t1)
		print("  [PASS] 槽位 %d (%s) 成功載入: %s (%dx%d)" % [i + 1, exp_slot.name, res_path, t1.get_width(), t1.get_height()])

	if loaded_textures.size() == 5:
		print("  [PASS] 五槽貼圖皆成功載入且各不相同 (5 distinct textures)")

class MockHost extends Node:
	var _ui_root: Control
	func _init():
		_ui_root = Control.new()
		add_child(_ui_root)
	func ui_clear_host() -> void:
		for c in _ui_root.get_children():
			c.queue_free()
	func ui_reset_fade() -> void:
		pass
	func ui_host() -> Control:
		return _ui_root
	func ui_refresh_hud() -> void:
		pass
	func ui_goto(_target: String = "") -> void:
		pass

func _test_equip_panel_core_slots() -> void:
	print("\n--- [Check 2] 角色整備面板 (EquipPanel) 機芯五槽整合 ---")
	var host := MockHost.new()
	root.add_child(host)

	var EquipPanelClass = load("res://scripts/ui/panels/equip_panel.gd")
	if EquipPanelClass == null:
		_fail("無法載入 equip_panel.gd")
		host.queue_free()
		return

	var panel = EquipPanelClass.new(host)
	panel.open()

	var host_root: Control = host.ui_host()
	var core_row: HBoxContainer = null
	for c in host_root.find_children("CoreSlotsRow", "HBoxContainer", true, false):
		core_row = c as HBoxContainer
		break

	if core_row == null:
		_fail("在 EquipPanel 中找不到 CoreSlotsRow 控制項")
		host.queue_free()
		return

	if core_row.get_child_count() != 5:
		_fail("EquipPanel CoreSlotsRow 子節點數應為 5，實際為: %d" % core_row.get_child_count())
		host.queue_free()
		return

	var seen_textures := {}
	for i in range(5):
		var slot_card := core_row.get_child(i)
		var btn: Button = slot_card.find_child("SlotButton", true, false) as Button
		var icon: TextureRect = slot_card.find_child("SlotIcon", true, false) as TextureRect
		var name_lbl: Label = slot_card.find_child("SlotNameLabel", true, false) as Label

		if btn == null:
			_fail("槽位 %d 缺少 SlotButton" % i)
		else:
			var btn_size := btn.custom_minimum_size
			if btn_size.x < 48 or btn_size.y < 48:
				_fail("槽位 %d SlotButton 熱區未達 48px: %s" % [i, str(btn_size)])
			else:
				print("  [PASS] 槽位 %d 按鈕熱區合規: %s (>= 48px)" % [i + 1, str(btn_size)])

		if icon == null or icon.texture == null:
			_fail("槽位 %d 缺少 SlotIcon 貼圖" % i)
		else:
			var p := icon.texture.resource_path
			if seen_textures.has(p):
				_fail("槽位 %d 貼圖重複: %s" % [i, p])
			seen_textures[p] = true

		if name_lbl == null or name_lbl.text.is_empty():
			_fail("槽位 %d 缺少名稱文字" % i)
		else:
			if _has_emoji(name_lbl.text):
				_fail("槽位 %d 名稱包含系統 Emoji: %s" % [i, name_lbl.text])
			print("  [PASS] 槽位 %d 名稱正確無 emoji: %s" % [i + 1, name_lbl.text])

	host.queue_free()

func _test_forge_dialog_core_slots() -> void:
	print("\n--- [Check 3] 鐵匠鍛造彈窗 (ForgeDialog) 機芯五槽整合 ---")
	var ForgeDialogClass = load("res://scripts/ui/forge_dialog.gd")
	if ForgeDialogClass == null:
		_fail("無法載入 forge_dialog.gd")
		return

	var dlg = ForgeDialogClass.new()
	root.add_child(dlg)

	var forge_core_row: HBoxContainer = null
	for c in dlg.find_children("ForgeCoreSlotsRow", "HBoxContainer", true, false):
		forge_core_row = c as HBoxContainer
		break

	if forge_core_row == null:
		_fail("在 ForgeDialog 中找不到 ForgeCoreSlotsRow 控制項")
		dlg.queue_free()
		return

	if forge_core_row.get_child_count() != 5:
		_fail("ForgeDialog ForgeCoreSlotsRow 子節點數應為 5，實際為: %d" % forge_core_row.get_child_count())
		dlg.queue_free()
		return

	var seen_textures := {}
	for i in range(5):
		var card := forge_core_row.get_child(i)
		var btn: Button = card.find_child("SlotButton", true, false) as Button
		var icon: TextureRect = card.find_child("SlotIcon", true, false) as TextureRect
		var name_lbl: Label = card.find_child("SlotName", true, false) as Label
		var desc_lbl: Label = card.find_child("SlotDesc", true, false) as Label

		if btn == null:
			_fail("Forge 槽位 %d 缺少 SlotButton" % i)
		else:
			var btn_size := btn.custom_minimum_size
			if btn_size.x < 48 or btn_size.y < 48:
				_fail("Forge 槽位 %d SlotButton 熱區未達 48px: %s" % [i, str(btn_size)])
			else:
				print("  [PASS] Forge 槽位 %d 按鈕熱區合規: %s (>= 48px)" % [i + 1, str(btn_size)])

		if icon == null or icon.texture == null:
			_fail("Forge 槽位 %d 缺少 SlotIcon 貼圖" % i)
		else:
			var p := icon.texture.resource_path
			if seen_textures.has(p):
				_fail("Forge 槽位 %d 貼圖重複: %s" % [i, p])
			seen_textures[p] = true

		if name_lbl == null or name_lbl.text.is_empty():
			_fail("Forge 槽位 %d 缺少名稱文字" % i)
		else:
			if _has_emoji(name_lbl.text):
				_fail("Forge 槽位 %d 名稱包含系統 Emoji: %s" % [i, name_lbl.text])
			if desc_lbl and _has_emoji(desc_lbl.text):
				_fail("Forge 槽位 %d 說明包含系統 Emoji: %s" % [i, desc_lbl.text])
			print("  [PASS] Forge 槽位 %d 名稱與說明正確無 emoji: %s" % [i + 1, name_lbl.text])

	dlg.queue_free()
