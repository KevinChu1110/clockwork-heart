class_name MaplePaperdollShowcase
extends Control
## 《發條之心》楓之谷 Character.wz 骨骼錨點與部件分層掛載展示場景
## 1. 展示發條白兔單一待機方向錨點拼裝
## 2. 部件自由置換（塗裝、外裝、眼睛、武器、發條鑰匙）
## 3. 具備即時呼吸待機動態（Body 呼吸帶動全身錨點子節點聯動、發條鑰匙自轉、眼睛自然眨眼）
## 4. 動態 Z-Order 調整
## 5. 錨點視覺化 Debug 檢視（neck/navel/hand/brow/back_key）

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")

@onready var doll_container: Node2D = $DollContainer
@onready var paperdoll: Node2D = $DollContainer/MaplePaperdoll
@onready var anchor_debug_overlay: Control = $AnchorDebugOverlay
@onready var lbl_info: Label = $UI/PanelInfo/VBox/LblInfo
@onready var controls_vbox: VBoxContainer = $UI/PanelControls/Scroll/VBox

var show_anchor_debug: bool = true


func _ready() -> void:
	if paperdoll == null:
		var doll_inst = MaplePaperdollClass.new()
		doll_inst.name = "MaplePaperdoll"
		if doll_container != null:
			doll_container.add_child(doll_inst)
		else:
			add_child(doll_inst)
		paperdoll = doll_inst

	if paperdoll != null:
		paperdoll.position = Vector2(0, 0)
		paperdoll.breathing_enabled = true
	_build_control_buttons()
	_update_info_label()


func _process(_delta: float) -> void:
	if show_anchor_debug and anchor_debug_overlay != null:
		anchor_debug_overlay.queue_redraw()


## 切換塗裝
func select_chassis(chassis_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_body(chassis_id)
		_update_info_label()


## 切換外裝
func select_costume(costume_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_costume(costume_id)
		_update_info_label()


## 切換眼睛
func select_eyes(eyes_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_eyes(eyes_id)
		_update_info_label()


## 切換武器
func select_weapon(weapon_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_weapon(weapon_id)
		_update_info_label()


## 切換發條鑰匙
func select_winding_key(key_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_winding_key(key_id)
		_update_info_label()


## 切換武器前後 Z-Order (前持 z=40 vs 背持 z=4)
func toggle_weapon_z_order() -> void:
	if paperdoll != null:
		var cur_z: int = int(paperdoll.get_part_z_index("weapon"))
		var new_z: int = 4 if cur_z == 40 else 40
		paperdoll.set_part_z_index("weapon", new_z)
		_update_info_label()


## 切換發條鑰匙前後 Z-Order (後背 z=5 vs 胸前/立體透視 z=15)
func toggle_key_z_order() -> void:
	if paperdoll != null:
		var cur_z: int = int(paperdoll.get_part_z_index("winding_key"))
		var new_z: int = 15 if cur_z == 5 else 5
		paperdoll.set_part_z_index("winding_key", new_z)
		_update_info_label()


## 切換呼吸待機動態開關
func toggle_breathing() -> void:
	if paperdoll != null:
		paperdoll.breathing_enabled = not paperdoll.breathing_enabled
		_update_info_label()


## 切換錨點視覺化覆蓋層
func toggle_anchor_debug() -> void:
	show_anchor_debug = not show_anchor_debug
	if anchor_debug_overlay != null:
		anchor_debug_overlay.visible = show_anchor_debug


func _update_info_label() -> void:
	if lbl_info == null or paperdoll == null:
		return
	var loadout: Dictionary = paperdoll.get_current_loadout()
	var z_order: Dictionary = paperdoll.get_layer_order()
	var txt: String = "【發條白兔 · 楓之谷錨點部件掛載展示】\n"
	txt += "• 塗裝素體: %s (Z: %d)\n" % [loadout.get("body", ""), z_order.get("body", 0)]
	txt += "• 頭部耳朵: %s (Z: %d)\n" % [loadout.get("head_unit", ""), z_order.get("head_unit", 0)]
	txt += "• 面部光學: %s (Z: %d)\n" % [loadout.get("eyes", ""), z_order.get("eyes", 0)]
	txt += "• 玩具外裝: %s (Z: %d)\n" % [loadout.get("costume", ""), z_order.get("costume", 0)]
	txt += "• 手持武器: %s (Z: %d)\n" % [loadout.get("weapon", ""), z_order.get("weapon", 0)]
	txt += "• 發條鑰匙: %s (Z: %d)\n" % [loadout.get("winding_key", ""), z_order.get("winding_key", 0)]
	txt += "• 呼吸動態: %s" % ["啟用中 (Active)" if paperdoll.breathing_enabled else "暫停 (Paused)"]
	lbl_info.text = txt


## 動態建立右側控制面板操作按鈕
func _build_control_buttons() -> void:
	if controls_vbox == null:
		return
	# 清除除標題外的現有項目
	for child in controls_vbox.get_children():
		if child.name != "LblTitle":
			child.queue_free()

	# 1. 塗裝素體組
	_add_section_header("塗裝素體 (Chassis)")
	_create_button_grid([
		{"label": "經典象牙白", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_ivory_stock")},
		{"label": "黃銅榮耀金", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_brass_gold")},
		{"label": "午夜深空藍", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_midnight_navy")},
	])

	# 2. 玩具外裝組
	_add_section_header("玩具外裝 (Costume)")
	_create_button_grid([
		{"label": "胡桃鉗衛兵服", "color": Color("#FFA010"), "fn": func(): select_costume("costume_nutcracker_guard")},
		{"label": "皇家遊行禮服", "color": Color("#FFA010"), "fn": func(): select_costume("costume_royal_parade")},
		{"label": "蒸汽工匠套裝", "color": Color("#FFA010"), "fn": func(): select_costume("costume_steam_artisan")},
		{"label": "卸除外裝 (素體)", "color": Color("#FFA010"), "fn": func(): select_costume("none")},
	])

	# 3. 面部光學組
	_add_section_header("面部光學核心 (Eyes)")
	_create_button_grid([
		{"label": "天青祖母綠", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_cyan_emerald")},
		{"label": "琥珀黃金核心", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_amber_gold")},
		{"label": "休眠閉眼眨眼", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_blink")},
		{"label": "純淨面甲 (無眼)", "color": Color("#38A0FF"), "fn": func(): select_eyes("none")},
	])

	# 4. 層級與動態控制組
	_add_section_header("骨骼層級與動態 (Controls)")
	_create_button_grid([
		{"label": "切換武器前後", "color": Color("#4ED86A"), "fn": func(): toggle_weapon_z_order()},
		{"label": "切換發條鑰匙前後", "color": Color("#4ED86A"), "fn": func(): toggle_key_z_order()},
		{"label": "待機呼吸動態開關", "color": Color("#4ED86A"), "fn": func(): toggle_breathing()},
		{"label": "骨骼錨點標記開關", "color": Color("#4ED86A"), "fn": func(): toggle_anchor_debug()},
	])


func _add_section_header(title: String) -> void:
	var lbl := Label.new()
	lbl.text = "▶ " + title
	lbl.add_theme_font_override("font", preload("res://assets/fonts/jf-openhuninn-2.1.ttf"))
	lbl.add_theme_font_size_override("font_size", 14)
	lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
	controls_vbox.add_child(lbl)


func _create_button_grid(btn_defs: Array) -> void:
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	controls_vbox.add_child(grid)

	for bdef in btn_defs:
		var btn := Button.new()
		btn.text = bdef.label
		btn.custom_minimum_size = Vector2(170, 48)
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL

		# 字體與樣式設定
		var font: FontFile = preload("res://assets/fonts/jf-openhuninn-2.1.ttf")
		btn.add_theme_font_override("font", font)
		btn.add_theme_font_size_override("font_size", 13)
		btn.add_theme_color_override("font_color", Color("#1F1A3A"))
		btn.add_theme_color_override("font_hover_color", Color("#1F1A3A"))
		btn.add_theme_color_override("font_pressed_color", Color("#1F1A3A"))

		var bg_c: Color = bdef.color
		var style_normal := StyleBoxFlat.new()
		style_normal.bg_color = bg_c
		style_normal.border_width_left = 2
		style_normal.border_width_top = 2
		style_normal.border_width_right = 2
		style_normal.border_width_bottom = 5
		style_normal.border_color = Color("#1F1A3A")
		style_normal.corner_radius_top_left = 14
		style_normal.corner_radius_top_right = 14
		style_normal.corner_radius_bottom_right = 14
		style_normal.corner_radius_bottom_left = 14
		btn.add_theme_stylebox_override("normal", style_normal)

		var style_hover := style_normal.duplicate() as StyleBoxFlat
		style_hover.bg_color = bg_c.lightened(0.12)
		btn.add_theme_stylebox_override("hover", style_hover)

		var style_pressed := style_normal.duplicate() as StyleBoxFlat
		style_pressed.border_width_bottom = 2
		style_pressed.border_width_top = 5
		btn.add_theme_stylebox_override("pressed", style_pressed)

		var fn: Callable = bdef.fn
		btn.pressed.connect(fn)
		grid.add_child(btn)
