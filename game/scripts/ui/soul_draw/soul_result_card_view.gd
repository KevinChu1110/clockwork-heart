extends Control
## 抽魂結果卡：多巴胺果凍色階光框（白/橘/藍/紫/金/紅）與立體流光效果。
## 支援透明高清立繪與零件圖示，徹底消除簡報 PPT 感。

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const DEFAULT_CARD := "res://assets/sprites/pack_a/v2/ui/soul_result_card.png"
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺色階定義（白/橘/藍/紫/金/紅） ──
const TIER_COLORS := {
	"white": {
		"frame": Color("#667085"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#475467"),
		"glow": Color(0.6, 0.65, 0.75, 0.55),
		"badge": Color("#EAECF0"),
		"stars": "",
		"name": "普通"
	},
	"orange": {
		"frame": Color("#FFA010"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#E68A00"),
		"glow": Color(1.0, 0.63, 0.06, 0.65),
		"badge": Color("#FFA010"),
		"stars": "",
		"name": "優良"
	},
	"blue": {
		"frame": Color("#38A0FF"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#1E88E5"),
		"glow": Color(0.22, 0.63, 1.0, 0.65),
		"badge": Color("#38A0FF"),
		"stars": "",
		"name": "稀有"
	},
	"purple": {
		"frame": Color("#A259FF"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#8E24AA"),
		"glow": Color(0.64, 0.35, 1.0, 0.70),
		"badge": Color("#A259FF"),
		"stars": "",
		"name": "史詩"
	},
	"gold": {
		"frame": Color("#FFD028"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#C48D00"),
		"glow": Color(1.0, 0.82, 0.16, 0.75),
		"badge": Color("#FFD028"),
		"stars": "",
		"name": "傳奇"
	},
	"red": {
		"frame": Color("#FF4D4D"),
		"bg": Color("#FFFDF8"),
		"border": Color("#1F1A3A"),
		"bottom": Color("#B71C1C"),
		"glow": Color(1.0, 0.30, 0.30, 0.80),
		"badge": Color("#FF4D4D"),
		"stars": "",
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

var _card_panel: Panel
var _shimmer_container: Control
var _shimmer_bar: ColorRect
var _halo_bg: Panel
var _art: TextureRect
var _stars_lbl: Label
var _tier_lbl: Label
var _badge: PanelContainer
var _badge_lbl: Label
var _label: Label
var _drop_lbl: Label
var _i18n: Dictionary = {}
var _font: Font = null

var _is_showing_drop: bool = false
var _current_drop: Dictionary = {}
var _current_toast_key: String = "soul.pull_start"
var _current_card_path: String = DEFAULT_CARD
var _shimmer_tween: Tween = null


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()
	if _shimmer_tween and _shimmer_tween.is_valid():
		_shimmer_tween.kill()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	refresh()


func _ready() -> void:
	_load_font()
	_load_i18n()
	_ensure()
	_connect_loc_signal()
	_start_shimmer()


func _load_font() -> void:
	if _font == null and ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font


static func get_current_locale() -> String:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc != null and loc.get("locale") != null:
			return str(loc.get("locale"))
	return ContentLoc.locale()


func _load_i18n() -> void:
	var lc := get_current_locale()
	var path := "res://data/i18n/%s.json" % lc
	if not FileAccess.file_exists(path):
		path = "res://data/i18n/zh_TW.json"
	if FileAccess.file_exists(path):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
		if typeof(parsed) == TYPE_DICTIONARY:
			_i18n = parsed as Dictionary


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


func tr_key(key: String) -> String:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var res = str(loc.call("t", key))
			if res != "" and res != key:
				return res
	if _i18n.has(key):
		return str(_i18n[key])
	return key


func _ensure() -> void:
	if _card_panel != null:
		return
	_load_font()

	# 1. 多巴胺果凍色階光框底板（圓角 22px，厚底 6px，立體果凍發光）
	_card_panel = Panel.new()
	_card_panel.name = "CardPanel"
	_card_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_card_panel)

	# 2. 流光容器
	_shimmer_container = Control.new()
	_shimmer_container.set_anchors_preset(Control.PRESET_FULL_RECT)
	_shimmer_container.clip_contents = true
	_card_panel.add_child(_shimmer_container)

	_shimmer_bar = ColorRect.new()
	_shimmer_bar.size = Vector2(180, 800)
	_shimmer_bar.position = Vector2(-250, -100)
	_shimmer_bar.rotation = 0.35
	_shimmer_bar.color = Color(1.0, 1.0, 1.0, 0.25)
	_shimmer_container.add_child(_shimmer_bar)

	# 2b. 中央懸浮微光光輪（破除黑盒，營造通透感）
	_halo_bg = Panel.new()
	_halo_bg.name = "HaloGlow"
	_halo_bg.set_anchors_preset(Control.PRESET_CENTER)
	_halo_bg.offset_left = -140
	_halo_bg.offset_right = 140
	_halo_bg.offset_top = -140
	_halo_bg.offset_bottom = 140
	var h_style := StyleBoxFlat.new()
	h_style.bg_color = Color(1.0, 0.95, 0.8, 0.18)
	h_style.set_corner_radius_all(140)
	h_style.shadow_color = Color(1.0, 0.82, 0.18, 0.35)
	h_style.shadow_size = 28
	_halo_bg.add_theme_stylebox_override("panel", h_style)
	_card_panel.add_child(_halo_bg)

	# 3. 頂部星級標籤
	_stars_lbl = Label.new()
	_stars_lbl.name = "StarsLabel"
	_stars_lbl.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_stars_lbl.offset_top = 18
	_stars_lbl.offset_bottom = 44
	_stars_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_stars_lbl.add_theme_font_size_override("font_size", 18)
	_stars_lbl.add_theme_color_override("font_color", Color("#FFD028"))
	if _font != null:
		_stars_lbl.add_theme_font_override("font", _font)
	add_child(_stars_lbl)

	# 4. 中央立繪/圖示展示（乾淨透底，等比縮放居中）
	_art = TextureRect.new()
	_art.name = "ResultCardArt"
	_art.set_anchors_preset(Control.PRESET_FULL_RECT)
	_art.offset_left = 32
	_art.offset_top = 44
	_art.offset_right = -32
	_art.offset_bottom = -116
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	add_child(_art)

	# 5. 多巴胺類別 Badge（直接掛在根以符合 RarityBadge/BadgeLabel 路徑）
	_badge = PanelContainer.new()
	_badge.name = "RarityBadge"
	_badge.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_badge.offset_top = -112
	_badge.offset_bottom = -80
	_badge_lbl = Label.new()
	_badge_lbl.name = "BadgeLabel"
	_badge_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_lbl.add_theme_font_size_override("font_size", 16)
	_badge_lbl.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		_badge_lbl.add_theme_font_override("font", _font)
	_badge.add_child(_badge_lbl)
	add_child(_badge)

	# 6. 結果台詞 Toast
	_label = Label.new()
	_label.name = "ResultToast"
	_label.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_label.offset_left = 20
	_label.offset_right = -20
	_label.offset_top = -78
	_label.offset_bottom = -46
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.add_theme_font_size_override("font_size", 22)
	_label.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		_label.add_theme_font_override("font", _font)
	add_child(_label)

	# 7. 掉落物品項明細（超大加粗粉圓體）
	_drop_lbl = Label.new()
	_drop_lbl.name = "DropIdLabel"
	_drop_lbl.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_drop_lbl.offset_left = 20
	_drop_lbl.offset_right = -20
	_drop_lbl.offset_top = -44
	_drop_lbl.offset_bottom = -12
	_drop_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_drop_lbl.add_theme_font_size_override("font_size", 18)
	_drop_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	if _font != null:
		_drop_lbl.add_theme_font_override("font", _font)
	add_child(_drop_lbl)

	show_placeholder()


func _start_shimmer() -> void:
	if _shimmer_tween and _shimmer_tween.is_valid():
		_shimmer_tween.kill()
	_shimmer_tween = create_tween().set_loops()
	_shimmer_tween.tween_property(_shimmer_bar, "position:x", 1200.0, 0.75)\
		.from(-250.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN_OUT)
	_shimmer_tween.tween_interval(2.2)


func _build_card_style(tier_data: Dictionary) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = tier_data.get("bg", Color("#FFFDF8"))
	s.border_color = tier_data.get("frame", Color("#FFD028"))
	s.set_border_width_all(4)
	s.border_width_bottom = 6
	s.set_corner_radius_all(22)
	s.shadow_color = tier_data.get("glow", Color(1, 0.8, 0.2, 0.6))
	s.shadow_size = 18
	return s


func _build_badge_style(color: Color) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = color
	s.border_color = UiStyle.BORDER_DARK
	s.set_border_width_all(2)
	s.border_width_bottom = 4
	s.set_corner_radius_all(12)
	s.content_margin_left = 18
	s.content_margin_right = 18
	s.content_margin_top = 4
	s.content_margin_bottom = 4
	return s


func show_placeholder(toast_key: String = "soul.pull_start", card_path: String = DEFAULT_CARD) -> void:
	_is_showing_drop = false
	_current_drop = {}
	_current_toast_key = toast_key
	_current_card_path = card_path
	_render_placeholder()


func _render_placeholder() -> void:
	_ensure()
	_load_i18n()

	var tier_data: Dictionary = TIER_COLORS["gold"]
	_card_panel.add_theme_stylebox_override("panel", _build_card_style(tier_data))
	_stars_lbl.text = _t(str(tier_data.get("name", "傳奇")))
	_stars_lbl.add_theme_color_override("font_color", tier_data.frame)

	var default_icon := "res://assets/sprites/player/paperdoll/rabbit/winding_key/key_classic_brass_512.png"
	if ResourceLoader.exists(default_icon):
		_art.texture = load(default_icon) as Texture2D
	elif ResourceLoader.exists(DEFAULT_CARD):
		_art.texture = load(DEFAULT_CARD) as Texture2D

	_badge_lbl.text = _t("封靈")
	_badge.add_theme_stylebox_override("panel", _build_badge_style(tier_data.badge))
	_label.text = tr_key(_current_toast_key)
	_drop_lbl.text = ""


func show_drop(drop: Dictionary, card_path: String = DEFAULT_CARD) -> void:
	_is_showing_drop = true
	_current_drop = drop
	_current_card_path = card_path
	_current_toast_key = str(drop.get("toastKey", "soul.pull_part"))
	_render_drop()


func _render_drop() -> void:
	_ensure()
	_load_i18n()

	var kind_str: String = str(_current_drop.get("kind", ""))
	var drop_id: String = str(_current_drop.get("DropId", ""))
	var kind_raw: String = KIND_NAMES.get(kind_str, kind_str)
	var name_raw: String = DROP_NAMES.get(drop_id, drop_id)
	var kind_display: String = _t(kind_raw)
	var name_display: String = _t(name_raw)

	# 決定稀有度色階
	var tier_key: String = DROP_TIERS.get(drop_id, "orange")
	if kind_str == "outfit":
		tier_key = "purple"
	elif kind_str == "junk":
		tier_key = "white"

	var tier_data: Dictionary = TIER_COLORS.get(tier_key, TIER_COLORS["orange"])

	# 套用果凍色階光框
	_card_panel.add_theme_stylebox_override("panel", _build_card_style(tier_data))
	_stars_lbl.text = _t(str(tier_data.get("name", "")))
	_stars_lbl.add_theme_color_override("font_color", tier_data.frame)

	# 更新微光光輪顏色
	if _halo_bg:
		var h_style: StyleBoxFlat = _halo_bg.get_theme_stylebox("panel") as StyleBoxFlat
		if h_style:
			h_style.shadow_color = tier_data.get("glow", Color(1, 0.8, 0.2, 0.5))

	# 載入精緻立繪或純淨透明零件圖示
	var asset_path: String = DROP_ASSETS.get(drop_id, "")
	if asset_path != "" and ResourceLoader.exists(asset_path):
		_art.texture = load(asset_path) as Texture2D
	elif ResourceLoader.exists(_current_card_path):
		_art.texture = load(_current_card_path) as Texture2D

	_badge_lbl.text = kind_display
	_badge.add_theme_stylebox_override("panel", _build_badge_style(tier_data.badge))

	_label.text = tr_key(_current_toast_key)
	_drop_lbl.text = "【%s】 %s" % [kind_display, name_display]


func refresh() -> void:
	if _is_showing_drop:
		_render_drop()
	else:
		_render_placeholder()
