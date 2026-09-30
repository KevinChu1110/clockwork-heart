class_name SoulTenPullView
extends Control
## 聚魂殿堂十連抽結果面板：5x2 陣列、多巴胺果凍色階光框（白/橘/藍/紫/金/紅）與流光效果。

signal collect_requested
signal pull_again_requested

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const TIER_COLORS := {
	"white": {
		"frame": Color("#667085"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#475467"),
		"glow": Color(0.6, 0.65, 0.75, 0.5),
		"badge": Color("#EAECF0"),
		"stars": "★ ☆ ☆",
		"name": "普通"
	},
	"orange": {
		"frame": Color("#FFA010"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#E68A00"),
		"glow": Color(1.0, 0.63, 0.06, 0.65),
		"badge": Color("#FFA010"),
		"stars": "★ ★ ☆",
		"name": "優良"
	},
	"blue": {
		"frame": Color("#38A0FF"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#1E88E5"),
		"glow": Color(0.22, 0.63, 1.0, 0.65),
		"badge": Color("#38A0FF"),
		"stars": "★ ★ ★",
		"name": "稀有"
	},
	"purple": {
		"frame": Color("#A259FF"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#8E24AA"),
		"glow": Color(0.64, 0.35, 1.0, 0.70),
		"badge": Color("#A259FF"),
		"stars": "★ ★ ★ ★",
		"name": "史詩"
	},
	"gold": {
		"frame": Color("#FFD028"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#C48D00"),
		"glow": Color(1.0, 0.82, 0.16, 0.75),
		"badge": Color("#FFD028"),
		"stars": "★ ★ ★ ★ ★",
		"name": "傳奇"
	},
	"red": {
		"frame": Color("#FF4D4D"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#B71C1C"),
		"glow": Color(1.0, 0.30, 0.30, 0.80),
		"badge": Color("#FF4D4D"),
		"stars": "✦ ✦ ✦ ✦ ✦",
		"name": "神話"
	}
}

const DROP_ASSETS := {
	"drop_brass_gear": "res://assets/icons/core_slots/slot_04_transmission_gears.png",
	"drop_spring_coil": "res://assets/icons/core_slots/slot_01_spring_generator.png",
	"drop_core_shard": "res://assets/sprites/player/paperdoll/rabbit/optic_core/core_cyan_emerald_512.png",
	"junk_enamel_chip": "res://assets/icons/core_slots/slot_02_chassis_armor.png",
	"outfit_cream": "res://assets/sprites/pack_a/v2/chars/xiaobai_base.png",
	"outfit_brass_vest": "res://assets/sprites/pack_a/v2/chars/lion_base.png",
	"outfit_scarf_tunic": "res://assets/sprites/pack_a/v2/chars/fox_base.png",
	"outfit_worker_apron": "res://assets/sprites/pack_a/v2/chars/pig_base.png"
}

const DROP_TIERS := {
	"junk_enamel_chip": "white",
	"drop_brass_gear": "orange",
	"drop_spring_coil": "blue",
	"outfit_cream": "purple",
	"outfit_brass_vest": "purple",
	"outfit_scarf_tunic": "purple",
	"outfit_worker_apron": "purple",
	"drop_core_shard": "gold"
}

const DROP_NAMES := {
	"drop_brass_gear": "黃銅齒輪",
	"drop_spring_coil": "發條游絲",
	"drop_core_shard": "核心碎片",
	"outfit_cream": "小白 · 奶油便服",
	"outfit_brass_vest": "獅 · 黃銅背心",
	"outfit_scarf_tunic": "狐 · 圍巾長衫",
	"outfit_worker_apron": "野豬 · 工匠工裙",
	"junk_enamel_chip": "搪瓷碎屑"
}

const KIND_NAMES := {
	"outfit": "換裝",
	"part": "零件",
	"junk": "雜件"
}

var _bg: ColorRect
var _title_lbl: Label
var _grid: GridContainer
var _btn_again: Button
var _btn_collect: Button
var _cards: Array[Control] = []
var _drops: Array[Dictionary] = []
var _font: Font = null


static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res


func _ready() -> void:
	custom_minimum_size = Vector2(1280, 720)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	offset_left = 0
	offset_top = 0
	offset_right = 0
	offset_bottom = 0
	_load_font()
	_build_ui()
	_connect_loc_signal()
	visible = false


func _load_font() -> void:
	if _font == null and ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	if _title_lbl:
		_title_lbl.text = _t("✦ 封靈連轉結果 ✦")
	if _btn_again:
		_btn_again.text = _t("再連轉一次")
	if _btn_collect:
		_btn_collect.text = _t("收入行囊")
	if not _drops.is_empty():
		show_drops(_drops)


func _build_ui() -> void:
	# 1. 溫暖暗幕半透明背景
	_bg = ColorRect.new()
	_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bg.custom_minimum_size = Vector2(1280, 720)
	_bg.color = Color(0.08, 0.07, 0.14, 0.98)
	add_child(_bg)

	# 2. 標題
	_title_lbl = Label.new()
	_title_lbl.text = _t("✦ 封靈連轉結果 ✦")
	_title_lbl.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_title_lbl.offset_top = 24
	_title_lbl.offset_bottom = 64
	_title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_title_lbl.add_theme_font_size_override("font_size", 28)
	_title_lbl.add_theme_color_override("font_color", Color("#FFD028"))
	if _font != null:
		_title_lbl.add_theme_font_override("font", _font)
	add_child(_title_lbl)

	# 3. 5 欄 2 列結果卡網格
	var center_box := CenterContainer.new()
	center_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	center_box.offset_top = 70
	center_box.offset_bottom = -80
	add_child(center_box)

	_grid = GridContainer.new()
	_grid.columns = 5
	_grid.add_theme_constant_override("h_separation", 18)
	_grid.add_theme_constant_override("v_separation", 16)
	center_box.add_child(_grid)

	# 4. 底部按鈕區
	var btn_row := HBoxContainer.new()
	btn_row.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	btn_row.offset_left = -260
	btn_row.offset_right = 260
	btn_row.offset_top = -70
	btn_row.offset_bottom = -16
	btn_row.add_theme_constant_override("separation", 24)
	add_child(btn_row)

	_btn_again = Button.new()
	_btn_again.text = _t("再連轉一次")
	_btn_again.custom_minimum_size = Vector2(230, 52)
	UiStyle.style_button(_btn_again, true)
	if _font != null:
		_btn_again.add_theme_font_override("font", _font)
	_btn_again.pressed.connect(func(): pull_again_requested.emit())
	btn_row.add_child(_btn_again)

	_btn_collect = Button.new()
	_btn_collect.text = _t("收入行囊")
	_btn_collect.custom_minimum_size = Vector2(230, 52)
	UiStyle.style_button(_btn_collect, false)
	if _font != null:
		_btn_collect.add_theme_font_override("font", _font)
	_btn_collect.pressed.connect(func():
		visible = false
		collect_requested.emit()
	)
	btn_row.add_child(_btn_collect)


func show_drops(drops: Array[Dictionary]) -> void:
	_drops = drops
	visible = true
	if size.x <= 0 or size.y <= 0:
		size = Vector2(1280, 720)

	# 清理舊卡片
	for c in _grid.get_children():
		c.queue_free()
	_cards.clear()

	for i in range(drops.size()):
		var drop: Dictionary = drops[i]
		var card := _create_mini_card(drop, i)
		_grid.add_child(card)
		_cards.append(card)


func _create_mini_card(drop: Dictionary, index: int) -> Control:
	var kind_str: String = str(drop.get("kind", ""))
	var drop_id: String = str(drop.get("DropId", ""))
	var kind_raw: String = KIND_NAMES.get(kind_str, kind_str)
	var name_raw: String = DROP_NAMES.get(drop_id, drop_id)
	var kind_display: String = _t(kind_raw)
	var name_display: String = _t(name_raw)

	var tier_key: String = DROP_TIERS.get(drop_id, "orange")
	if kind_str == "outfit":
		tier_key = "purple"
	elif kind_str == "junk":
		tier_key = "white"

	var tier_data: Dictionary = TIER_COLORS.get(tier_key, TIER_COLORS["orange"])

	var root_card := Control.new()
	root_card.custom_minimum_size = Vector2(210, 240)
	root_card.pivot_offset = Vector2(105, 120)

	# 果凍底板
	var panel := Panel.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	var style := StyleBoxFlat.new()
	style.bg_color = tier_data.get("bg", Color("#FFFDF8"))
	style.border_color = tier_data.get("frame", Color("#FFD028"))
	style.set_border_width_all(3)
	style.border_width_bottom = 5
	style.set_corner_radius_all(18)
	style.shadow_color = tier_data.get("glow", Color(1, 0.8, 0.2, 0.6))
	style.shadow_size = 14
	panel.add_theme_stylebox_override("panel", style)
	root_card.add_child(panel)

	# 頂部星級與稀有度
	var top_lbl := Label.new()
	top_lbl.text = "%s %s" % [tier_data.get("stars", "★ ★"), tier_data.get("name", "")]
	top_lbl.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_lbl.offset_top = 10
	top_lbl.offset_bottom = 30
	top_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	top_lbl.add_theme_font_size_override("font_size", 14)
	top_lbl.add_theme_color_override("font_color", tier_data.frame)
	if _font != null:
		top_lbl.add_theme_font_override("font", _font)
	panel.add_child(top_lbl)

	# 中央微光光圈
	var halo := Panel.new()
	halo.set_anchors_preset(Control.PRESET_CENTER)
	halo.offset_left = -45
	halo.offset_right = 45
	halo.offset_top = -45
	halo.offset_bottom = 45
	var h_style := StyleBoxFlat.new()
	h_style.bg_color = Color(1, 1, 1, 0.05)
	h_style.set_corner_radius_all(45)
	h_style.shadow_color = tier_data.get("glow", Color(1, 0.8, 0.2, 0.3))
	h_style.shadow_size = 16
	halo.add_theme_stylebox_override("panel", h_style)
	panel.add_child(halo)

	# 中央圖示 / 立繪（乾淨透明底）
	var art := TextureRect.new()
	art.set_anchors_preset(Control.PRESET_FULL_RECT)
	art.offset_left = 18
	art.offset_top = 34
	art.offset_right = -18
	art.offset_bottom = -54
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	var asset_path: String = DROP_ASSETS.get(drop_id, "")
	if asset_path != "" and ResourceLoader.exists(asset_path):
		art.texture = load(asset_path) as Texture2D
	panel.add_child(art)

	# 類別 Badge
	var badge_box := PanelContainer.new()
	badge_box.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	badge_box.offset_top = -52
	badge_box.offset_bottom = -28
	var b_style := StyleBoxFlat.new()
	b_style.bg_color = tier_data.badge
	b_style.border_color = UiStyle.BORDER_DARK
	b_style.set_border_width_all(2)
	b_style.border_width_bottom = 3
	b_style.set_corner_radius_all(10)
	b_style.content_margin_left = 12
	b_style.content_margin_right = 12
	b_style.content_margin_top = 2
	b_style.content_margin_bottom = 2
	badge_box.add_theme_stylebox_override("panel", b_style)

	var b_lbl := Label.new()
	b_lbl.text = kind_display
	b_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	b_lbl.add_theme_font_size_override("font_size", 13)
	b_lbl.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		b_lbl.add_theme_font_override("font", _font)
	badge_box.add_child(b_lbl)
	panel.add_child(badge_box)

	# 底部名稱
	var name_lbl := Label.new()
	name_lbl.text = name_display
	name_lbl.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	name_lbl.offset_left = 8
	name_lbl.offset_right = -8
	name_lbl.offset_top = -26
	name_lbl.offset_bottom = -6
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 15)
	name_lbl.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		name_lbl.add_theme_font_override("font", _font)
	panel.add_child(name_lbl)

	# 依序錯落彈入動畫
	root_card.scale = Vector2(0.2, 0.2)
	root_card.modulate = Color(1, 1, 1, 0)
	var tw := create_tween()
	tw.tween_interval(index * 0.04)
	tw.tween_property(root_card, "scale", Vector2(1.0, 1.0), 0.25)\
		.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.parallel().tween_property(root_card, "modulate:a", 1.0, 0.2)

	return root_card
