class_name MaplePaperdollShowcase
extends Control
## 《發條之心》楓之谷 Character.wz 骨骼錨點與部件分層掛載展示場景
## 1. 支援首發三大族即時無縫切換（發條白兔、熾火赤狐、烈金雄獅）
## 2. 部件自由置換（塗裝、外裝、光學義眼、武器、發條鑰匙、頭部單元、背飾）
## 3. 具備即時呼吸待機動態（Body 呼吸帶動全身錨點子節點聯動、發條鑰匙自轉、眼睛自然眨眼）
## 4. 動態 Z-Order 調整
## 5. 錨點視覺化 Debug 覆蓋層（AnchorDebugOverlay 連動各族專屬身材比例）

signal race_switched(race_id: String)

const MaplePaperdollClass = preload("res://scripts/art/maple_paperdoll.gd")

const RACE_SPECS := {
	"rabbit": {
		"name": "發條白兔",
		"spec_path": "res://data/tables/maple_paperdoll_rabbit.json",
		"color": Color("#FFD028")
	},
	"fox": {
		"name": "熾火赤狐",
		"spec_path": "res://data/tables/maple_paperdoll_fox.json",
		"color": Color("#FFA010")
	},
	"lion": {
		"name": "烈金雄獅",
		"spec_path": "res://data/tables/maple_paperdoll_lion.json",
		"color": Color("#FF5E8A")
	}
}

@onready var doll_container: Node2D = $DollContainer
@onready var paperdoll: Node2D = $DollContainer/MaplePaperdoll
@onready var anchor_debug_overlay: Control = $AnchorDebugOverlay
@onready var lbl_info: Label = $UI/PanelInfo/VBox/LblInfo
@onready var controls_vbox: VBoxContainer = $UI/PanelControls/Scroll/VBox
@onready var race_chips_container: Container = get_node_or_null("UI/PanelRaceChips/HBoxRaceChips")

var current_race: String = "rabbit"
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
		paperdoll.load_spec(RACE_SPECS[current_race]["spec_path"])

	_setup_race_chips()
	_build_control_buttons()
	_update_info_label()


func _process(_delta: float) -> void:
	if show_anchor_debug and anchor_debug_overlay != null:
		anchor_debug_overlay.queue_redraw()


## 切換首發展示種族
func select_race(race_id: String) -> void:
	if not RACE_SPECS.has(race_id):
		return
	current_race = race_id
	var rdata: Dictionary = RACE_SPECS[race_id]
	if paperdoll != null:
		paperdoll.load_spec(rdata["spec_path"])

	_update_race_chips_ui()
	_build_control_buttons()
	_update_info_label()
	if anchor_debug_overlay != null:
		anchor_debug_overlay.queue_redraw()
	race_switched.emit(race_id)


## 切換塗裝素體
func select_chassis(chassis_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_body(chassis_id)
		_update_info_label()


## 切換玩具外裝
func select_costume(costume_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_costume(costume_id)
		_update_info_label()


## 切換面部光學核心
func select_eyes(eyes_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_eyes(eyes_id)
		_update_info_label()


## 切換頭部耳朵/鬃毛單元
func select_head_unit(head_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_head_unit(head_id)
		_update_info_label()


## 切換手持武器
func select_weapon(weapon_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_weapon(weapon_id)
		_update_info_label()


## 切換發條鑰匙
func select_winding_key(key_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_winding_key(key_id)
		_update_info_label()


## 切換背部飾品/尾巴
func select_back_curio(curio_id: String) -> void:
	if paperdoll != null:
		paperdoll.set_back_curio(curio_id)
		_update_info_label()


## 切換武器前後 Z-Order (前持 z=40 vs 背持 z=4)
func toggle_weapon_z_order() -> void:
	if paperdoll != null:
		var cur_z: int = int(paperdoll.get_part_z_index("weapon"))
		var new_z: int = 4 if cur_z == 40 else 40
		paperdoll.set_part_z_index("weapon", new_z)
		_update_info_label()


## 切換發條鑰匙前後 Z-Order (後背 z=5 vs 前方/透視 z=15)
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


## 切換錨點視覺化覆蓋層開關
func toggle_anchor_debug() -> void:
	show_anchor_debug = not show_anchor_debug
	if anchor_debug_overlay != null:
		anchor_debug_overlay.visible = show_anchor_debug


func _update_info_label() -> void:
	if lbl_info == null or paperdoll == null:
		return
	var rname: String = RACE_SPECS.get(current_race, {}).get("name", "發條白兔")
	var loadout: Dictionary = paperdoll.get_current_loadout()
	var z_order: Dictionary = paperdoll.get_layer_order()
	var txt: String = "【%s · 楓之谷錨點掛載展示】\n" % rname
	txt += "• 塗裝素體: %s (Z: %d)\n" % [loadout.get("body", ""), z_order.get("body", 0)]
	txt += "• 頭部耳朵: %s (Z: %d)\n" % [loadout.get("head_unit", ""), z_order.get("head_unit", 0)]
	txt += "• 面部光學: %s (Z: %d)\n" % [loadout.get("eyes", ""), z_order.get("eyes", 0)]
	txt += "• 玩具外裝: %s (Z: %d)\n" % [loadout.get("costume", ""), z_order.get("costume", 0)]
	txt += "• 手持武器: %s (Z: %d)\n" % [loadout.get("weapon", ""), z_order.get("weapon", 0)]
	txt += "• 發條鑰匙: %s (Z: %d)\n" % [loadout.get("winding_key", ""), z_order.get("winding_key", 0)]
	if loadout.has("back_curio") and str(loadout["back_curio"]) not in ["none", ""]:
		txt += "• 背部尾飾: %s (Z: %d)\n" % [loadout.get("back_curio", ""), z_order.get("back_curio", 0)]
	txt += "• 呼吸動態: %s" % ["啟用中 (Active)" if paperdoll.breathing_enabled else "暫停 (Paused)"]
	lbl_info.text = txt


## 設置左側獨立種族晶片按鈕列
func _setup_race_chips() -> void:
	var chips_container := race_chips_container
	if chips_container == null:
		var panel_race := get_node_or_null("UI/PanelRaceChips")
		if panel_race == null:
			var ui_node: Node = get_node_or_null("UI")
			if ui_node != null:
				var pnl := PanelContainer.new()
				pnl.name = "PanelRaceChips"
				pnl.offset_left = 40.0
				pnl.offset_top = 280.0
				pnl.offset_right = 440.0
				pnl.offset_bottom = 356.0
				var style := StyleBoxFlat.new()
				style.bg_color = Color(1, 1, 1, 0.92)
				style.border_width_left = 3
				style.border_width_top = 3
				style.border_width_right = 3
				style.border_width_bottom = 5
				style.border_color = Color("#1F1A3A")
				style.corner_radius_top_left = 18
				style.corner_radius_top_right = 18
				style.corner_radius_bottom_right = 18
				style.corner_radius_bottom_left = 18
				pnl.add_theme_stylebox_override("panel", style)
				ui_node.add_child(pnl)

				var hbox := HBoxContainer.new()
				hbox.name = "HBoxRaceChips"
				hbox.add_theme_constant_override("separation", 10)
				hbox.alignment = BoxContainer.ALIGNMENT_CENTER
				pnl.add_child(hbox)
				chips_container = hbox
				race_chips_container = hbox

	if chips_container == null:
		return

	for child in chips_container.get_children():
		child.queue_free()

	for r_id in ["rabbit", "fox", "lion"]:
		var r_data: Dictionary = RACE_SPECS[r_id]
		var btn := _create_chip_button(r_id, r_data["name"], r_data["color"], func(): select_race(r_id))
		btn.custom_minimum_size = Vector2(120, 48)
		chips_container.add_child(btn)

	_update_race_chips_ui()


## 刷新種族按鈕高亮狀態
func _update_race_chips_ui() -> void:
	if race_chips_container != null:
		for btn in race_chips_container.get_children():
			if btn is Button and btn.has_meta("race_id"):
				var r_id: String = str(btn.get_meta("race_id"))
				_apply_chip_style(btn, r_id == current_race, RACE_SPECS[r_id]["color"])


## 動態建立右側控制面板操作按鈕
func _build_control_buttons() -> void:
	if controls_vbox == null:
		return
	# 清除除標題外的現有項目
	for child in controls_vbox.get_children():
		if child.name != "LblTitle":
			child.queue_free()

	# 0. 首發種族切換 Chip 列
	_add_section_header("首發種族切換 (Race Selection)")
	var race_chip_row := HBoxContainer.new()
	race_chip_row.add_theme_constant_override("separation", 8)
	controls_vbox.add_child(race_chip_row)

	for r_id in ["rabbit", "fox", "lion"]:
		var r_data: Dictionary = RACE_SPECS[r_id]
		var chip := _create_chip_button(r_id, r_data["name"], r_data["color"], func(): select_race(r_id))
		chip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		race_chip_row.add_child(chip)
		_apply_chip_style(chip, r_id == current_race, r_data["color"])

	# 依據當前種族建立部件置換清單
	match current_race:
		"rabbit":
			_build_rabbit_buttons()
		"fox":
			_build_fox_buttons()
		"lion":
			_build_lion_buttons()

	# 通用層級與動態控制組
	_add_section_header("骨骼層級與動態 (Controls)")
	_create_button_grid([
		{"label": "切換武器前後", "color": Color("#4ED86A"), "fn": func(): toggle_weapon_z_order()},
		{"label": "切換發條鑰匙前後", "color": Color("#4ED86A"), "fn": func(): toggle_key_z_order()},
		{"label": "待機呼吸動態開關", "color": Color("#4ED86A"), "fn": func(): toggle_breathing()},
		{"label": "骨骼錨點標記開關", "color": Color("#4ED86A"), "fn": func(): toggle_anchor_debug()},
	])


func _build_rabbit_buttons() -> void:
	# 1. 塗裝素體組
	_add_section_header("塗裝素體 (Chassis)")
	_create_button_grid([
		{"label": "經典象牙白", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_ivory_stock")},
		{"label": "黃銅榮耀金", "color": Color("#FFA010"), "fn": func(): select_chassis("paint_brass_gold")},
		{"label": "午夜深空藍", "color": Color("#38A0FF"), "fn": func(): select_chassis("paint_midnight_navy")},
	])

	# 2. 兔耳單元
	_add_section_header("挺立兔耳 (Head Unit)")
	_create_button_grid([
		{"label": "挺立白兔耳", "color": Color("#FFD028"), "fn": func(): select_head_unit("ear_rabbit_straight")},
		{"label": "黃銅挺立兔耳", "color": Color("#FFA010"), "fn": func(): select_head_unit("ear_rabbit_straight_brass")},
		{"label": "午夜深藍兔耳", "color": Color("#38A0FF"), "fn": func(): select_head_unit("ear_rabbit_straight_midnight")},
	])

	# 3. 玩具外裝組
	_add_section_header("玩具外裝 (Costume)")
	_create_button_grid([
		{"label": "胡桃鉗衛兵服", "color": Color("#FFA010"), "fn": func(): select_costume("costume_nutcracker_guard")},
		{"label": "皇家遊行禮服", "color": Color("#FF5E8A"), "fn": func(): select_costume("costume_royal_parade")},
		{"label": "蒸汽工匠套裝", "color": Color("#4ED86A"), "fn": func(): select_costume("costume_steam_artisan")},
		{"label": "卸除外裝 (素體)", "color": Color("#FFA010"), "fn": func(): select_costume("none")},
	])

	# 4. 面部光學組
	_add_section_header("面部光學核心 (Eyes)")
	_create_button_grid([
		{"label": "天青祖母綠", "color": Color("#4ED86A"), "fn": func(): select_eyes("eyes_cyan_emerald")},
		{"label": "琥珀黃金核心", "color": Color("#FFD028"), "fn": func(): select_eyes("eyes_amber_gold")},
		{"label": "休眠閉眼眨眼", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_blink")},
		{"label": "純淨面甲 (無眼)", "color": Color("#FF5E8A"), "fn": func(): select_eyes("none")},
	])

	# 5. 手持武器組
	_add_section_header("手持武器 (Weapon)")
	_create_button_grid([
		{"label": "破曉短劍", "color": Color("#4ED86A"), "fn": func(): select_weapon("wpn_dawn_blade")},
		{"label": "卸除武器 (空手)", "color": Color("#4ED86A"), "fn": func(): select_weapon("none")},
	])

	# 6. 發條鑰匙組
	_add_section_header("發條鑰匙 (Winding Key)")
	_create_button_grid([
		{"label": "經典雙環黃銅鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("key_classic_brass")},
		{"label": "卸除發條鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("none")},
	])


func _build_fox_buttons() -> void:
	# 1. 塗裝素體組
	_add_section_header("塗裝素體 (Chassis)")
	_create_button_grid([
		{"label": "熾火赤狐橘金", "color": Color("#FFA010"), "fn": func(): select_chassis("paint_fox_orange")},
		{"label": "經典象牙白", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_ivory_stock")},
		{"label": "翡翠琉璃釉", "color": Color("#4ED86A"), "fn": func(): select_chassis("paint_emerald_glaze")},
	])

	# 2. 狐耳單元
	_add_section_header("雷達狐耳 (Head Unit)")
	_create_button_grid([
		{"label": "雷達狐耳·赤金", "color": Color("#FFA010"), "fn": func(): select_head_unit("ear_fox_radar_orange")},
		{"label": "雷達狐耳·象牙白", "color": Color("#FFD028"), "fn": func(): select_head_unit("ear_fox_radar_ivory")},
		{"label": "雷達狐耳·翡翠綠", "color": Color("#4ED86A"), "fn": func(): select_head_unit("ear_fox_radar_emerald")},
	])

	# 3. 玩具外裝組
	_add_section_header("玩具外裝 (Costume)")
	_create_button_grid([
		{"label": "星相斗篷", "color": Color("#FFA010"), "fn": func(): select_costume("costume_astral_cape")},
		{"label": "星相學者外裝", "color": Color("#FF5E8A"), "fn": func(): select_costume("costume_astral_observer")},
		{"label": "卸除外裝 (素體)", "color": Color("#FFA010"), "fn": func(): select_costume("none")},
	])

	# 4. 面部光學組
	_add_section_header("面部光學核心 (Eyes)")
	_create_button_grid([
		{"label": "天青祖母綠", "color": Color("#4ED86A"), "fn": func(): select_eyes("eyes_cyan_emerald")},
		{"label": "琥珀黃金核心", "color": Color("#FFD028"), "fn": func(): select_eyes("eyes_amber_gold")},
		{"label": "休眠閉眼眨眼", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_blink")},
		{"label": "純淨面甲 (無眼)", "color": Color("#FF5E8A"), "fn": func(): select_eyes("none")},
	])

	# 5. 手持武器組
	_add_section_header("手持武器 (Weapon)")
	_create_button_grid([
		{"label": "星相占星法杖", "color": Color("#4ED86A"), "fn": func(): select_weapon("wpn_astral_staff")},
		{"label": "卸除武器 (空手)", "color": Color("#4ED86A"), "fn": func(): select_weapon("none")},
	])

	# 6. 發條鑰匙組
	_add_section_header("發條鑰匙 (Winding Key)")
	_create_button_grid([
		{"label": "經典雙環黃銅鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("key_classic_brass")},
		{"label": "卸除發條鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("none")},
	])


func _build_lion_buttons() -> void:
	# 1. 塗裝素體組
	_add_section_header("塗裝素體 (Chassis)")
	_create_button_grid([
		{"label": "黃銅榮耀金", "color": Color("#FFA010"), "fn": func(): select_chassis("paint_brass_gold")},
		{"label": "經典象牙白", "color": Color("#FFD028"), "fn": func(): select_chassis("paint_ivory_stock")},
		{"label": "午夜深空藍", "color": Color("#38A0FF"), "fn": func(): select_chassis("paint_midnight_navy")},
	])

	# 2. 金屬獅鬃
	_add_section_header("鍍金獅鬃 (Head Unit)")
	_create_button_grid([
		{"label": "鍍金獅鬃·黃銅", "color": Color("#FFA010"), "fn": func(): select_head_unit("ear_lion_gilded_mane_brass")},
		{"label": "鍍金獅鬃·象牙白", "color": Color("#FFD028"), "fn": func(): select_head_unit("ear_lion_gilded_mane_ivory")},
		{"label": "鍍金獅鬃·午夜藍", "color": Color("#38A0FF"), "fn": func(): select_head_unit("ear_lion_gilded_mane_midnight")},
		{"label": "鍍金獅鬃·經典原色", "color": Color("#FFA010"), "fn": func(): select_head_unit("ear_lion_gilded_mane")},
	])

	# 3. 玩具外裝組
	_add_section_header("玩具外裝 (Costume)")
	_create_button_grid([
		{"label": "皇家禁衛重鎧", "color": Color("#FFA010"), "fn": func(): select_costume("costume_royal_guard")},
		{"label": "胡桃鉗衛兵服", "color": Color("#FF5E8A"), "fn": func(): select_costume("costume_nutcracker_guard")},
		{"label": "蒸汽工匠套裝", "color": Color("#4ED86A"), "fn": func(): select_costume("costume_steam_artisan")},
		{"label": "卸除外裝 (素體)", "color": Color("#FFA010"), "fn": func(): select_costume("none")},
	])

	# 4. 面部光學組
	_add_section_header("面部光學核心 (Eyes)")
	_create_button_grid([
		{"label": "琥珀黃金核心", "color": Color("#FFD028"), "fn": func(): select_eyes("eyes_amber_gold")},
		{"label": "天青祖母綠", "color": Color("#4ED86A"), "fn": func(): select_eyes("eyes_cyan_emerald")},
		{"label": "休眠閉眼眨眼", "color": Color("#38A0FF"), "fn": func(): select_eyes("eyes_blink")},
		{"label": "純淨面甲 (無眼)", "color": Color("#FF5E8A"), "fn": func(): select_eyes("none")},
	])

	# 5. 手持武器組
	_add_section_header("手持武器 (Weapon)")
	_create_button_grid([
		{"label": "騎士重裝長槍", "color": Color("#4ED86A"), "fn": func(): select_weapon("wpn_knight_lance")},
		{"label": "卸除武器 (空手)", "color": Color("#4ED86A"), "fn": func(): select_weapon("none")},
	])

	# 6. 發條鑰匙組
	_add_section_header("發條鑰匙 (Winding Key)")
	_create_button_grid([
		{"label": "經典雙環黃銅鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("key_classic_brass")},
		{"label": "卸除發條鑰匙", "color": Color("#FFD028"), "fn": func(): select_winding_key("none")},
	])

	# 7. 背部尾飾
	_add_section_header("發條獅尾 (Back Curio)")
	_create_button_grid([
		{"label": "發條獅尾飾件", "color": Color("#FF5E8A"), "fn": func(): select_back_curio("curio_lion_fan_tail")},
		{"label": "卸除背部飾品", "color": Color("#FF5E8A"), "fn": func(): select_back_curio("none")},
	])


func _add_section_header(title: String) -> void:
	var lbl := Label.new()
	lbl.text = "▶ " + title
	lbl.add_theme_font_override("font", preload("res://assets/fonts/jf-openhuninn-2.1.ttf"))
	lbl.add_theme_font_size_override("font_size", 14)
	lbl.add_theme_color_override("font_color", Color("#1F1A3A"))
	controls_vbox.add_child(lbl)


func _create_chip_button(race_id: String, label_text: String, bg_c: Color, fn: Callable) -> Button:
	var btn := Button.new()
	btn.text = label_text
	btn.set_meta("race_id", race_id)
	btn.custom_minimum_size = Vector2(100, 48)

	var font: FontFile = preload("res://assets/fonts/jf-openhuninn-2.1.ttf")
	btn.add_theme_font_override("font", font)
	btn.add_theme_font_size_override("font_size", 14)
	btn.add_theme_color_override("font_color", Color("#1F1A3A"))
	btn.add_theme_color_override("font_hover_color", Color("#1F1A3A"))
	btn.add_theme_color_override("font_pressed_color", Color("#1F1A3A"))

	_apply_chip_style(btn, race_id == current_race, bg_c)
	btn.pressed.connect(fn)
	return btn


func _apply_chip_style(btn: Button, is_active: bool, bg_c: Color) -> void:
	var style_normal := StyleBoxFlat.new()
	style_normal.bg_color = bg_c if is_active else bg_c.darkened(0.18)
	style_normal.border_width_left = 3 if is_active else 2
	style_normal.border_width_top = 3 if is_active else 2
	style_normal.border_width_right = 3 if is_active else 2
	style_normal.border_width_bottom = 6 if is_active else 4
	style_normal.border_color = Color("#1F1A3A")
	style_normal.corner_radius_top_left = 16
	style_normal.corner_radius_top_right = 16
	style_normal.corner_radius_bottom_right = 16
	style_normal.corner_radius_bottom_left = 16
	btn.add_theme_stylebox_override("normal", style_normal)

	var style_hover := style_normal.duplicate() as StyleBoxFlat
	style_hover.bg_color = bg_c.lightened(0.12)
	btn.add_theme_stylebox_override("hover", style_hover)

	var style_pressed := style_normal.duplicate() as StyleBoxFlat
	style_pressed.border_width_bottom = 2
	style_pressed.border_width_top = 6
	btn.add_theme_stylebox_override("pressed", style_pressed)


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
