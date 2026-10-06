extends Control
## 抽魂結果卡：稀有度框只有五色（白/藍/紫/金/彩），卡面一律是完整零件圖。
## 卡圖／名稱／框色統一從 soul_draw_card_catalog.gd 取。

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const DEFAULT_CARD := "res://assets/sprites/pack_a/v2/ui/soul_result_card.png"
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const Catalog := preload("res://scripts/ui/soul_draw/soul_draw_card_catalog.gd")

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

	var tier_data: Dictionary = Catalog.frame_data("gold")
	_card_panel.add_theme_stylebox_override("panel", _build_card_style(tier_data))
	_set_rainbow(false)
	_stars_lbl.text = ""
	_stars_lbl.add_theme_color_override("font_color", tier_data.frame)

	_art.texture = Catalog.idle_texture()

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

	var drop: Dictionary = Catalog.normalize_drop(_current_drop)
	var kind_str: String = str(drop.get("kind", ""))
	var drop_id: String = str(drop.get("DropId", ""))
	var kind_display: String = _t(Catalog.kind_name(kind_str))
	var name_display: String = _t(Catalog.drop_name(drop_id))

	# 稀有度只顯示五色框
	var frame_key: String = Catalog.frame_key_for_drop(drop)
	var tier_data: Dictionary = Catalog.frame_data(frame_key)
	set_meta("frame", frame_key)
	set_meta("drop_id", drop_id)

	# 套用果凍色階光框
	_card_panel.add_theme_stylebox_override("panel", _build_card_style(tier_data))
	_set_rainbow(bool(tier_data.get("rainbow", false)))
	_stars_lbl.text = "%s  %s" % [tier_data.get("stars", "★"), _t(str(tier_data.get("name", "")))]
	_stars_lbl.add_theme_color_override("font_color", tier_data.frame)

	# 更新微光光輪顏色
	if _halo_bg:
		var h_style: StyleBoxFlat = _halo_bg.get_theme_stylebox("panel") as StyleBoxFlat
		if h_style:
			h_style.shadow_color = tier_data.get("glow", Color(1, 0.8, 0.2, 0.5))

	# 載入精緻立繪或純淨透明零件圖示
	_art.texture = Catalog.art_texture(drop_id)

	_badge_lbl.text = kind_display
	_badge.add_theme_stylebox_override("panel", _build_badge_style(tier_data.badge))

	_label.text = tr_key(_current_toast_key)
	_drop_lbl.text = "【%s】 %s" % [kind_display, name_display]


func _set_rainbow(on: bool) -> void:
	var band: Node = _card_panel.get_node_or_null("RainbowBand")
	if on and band == null:
		band = Catalog.rainbow_band(6)
		_card_panel.add_child(band)
	if band != null:
		(band as CanvasItem).visible = on


func refresh() -> void:
	if _is_showing_drop:
		_render_drop()
	else:
		_render_placeholder()
