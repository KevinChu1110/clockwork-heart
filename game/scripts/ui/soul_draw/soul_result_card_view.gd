extends Control
## 抽魂結果卡：Alice 圖＋Bingo toast（可解析 i18n）。
## 模組邊界：只顯示；抽獎在 soul_draw_v2。

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const DEFAULT_CARD := "res://assets/sprites/pack_a/v2/ui/soul_result_card.png"
const I18N_PATH := "res://data/i18n/zh_TW.json"
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺字典色盤（只用這五色） ──
const COLOR_GOLD   := UiStyle.TATA_YELLOW  ## 金黃 Color(1.0, 0.82, 0.18, 1.0)
const COLOR_ORANGE := UiStyle.TATA_ORANGE  ## 暖橘 Color(1.0, 0.54, 0.12, 1.0)
const COLOR_MINT   := UiStyle.TATA_GREEN   ## 薄荷綠 Color(0.30, 0.82, 0.44, 1.0)
const COLOR_SKY    := UiStyle.TATA_BLUE    ## 天藍 Color(0.24, 0.68, 0.98, 1.0)
const COLOR_PINK   := UiStyle.TATA_PINK    ## 珊瑚粉 Color(1.0, 0.40, 0.60, 1.0)

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
var _art: TextureRect
var _badge: PanelContainer
var _badge_lbl: Label
var _label: Label
var _drop_lbl: Label
var _i18n: Dictionary = {}
var _font: Font = null


func _ready() -> void:
	_load_font()
	_load_i18n()
	_ensure()


func _load_font() -> void:
	if _font == null and ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font


func _load_i18n() -> void:
	if FileAccess.file_exists(I18N_PATH):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(I18N_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_i18n = parsed as Dictionary


func tr_key(key: String) -> String:
	if _i18n.has(key):
		return str(_i18n[key])
	return key


func _ensure() -> void:
	if _art != null:
		return
	_load_font()

	# 1. 奶油卡底板
	_card_panel = Panel.new()
	_card_panel.name = "CardPanel"
	_card_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	_card_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	add_child(_card_panel)

	# 2. 插畫展示（等比縮放居中）
	_art = TextureRect.new()
	_art.name = "ResultCardArt"
	_art.set_anchors_preset(Control.PRESET_FULL_RECT)
	_art.offset_left = 16
	_art.offset_top = 16
	_art.offset_right = -16
	_art.offset_bottom = -118
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	add_child(_art)

	# 3. 多巴胺類別 Badge（深暖褐字色，不准亮底亮字）
	_badge = PanelContainer.new()
	_badge.name = "RarityBadge"
	_badge.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_badge.offset_top = -112
	_badge.offset_bottom = -82
	_badge_lbl = Label.new()
	_badge_lbl.name = "BadgeLabel"
	_badge_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_lbl.add_theme_font_size_override("font_size", 16)
	_badge_lbl.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		_badge_lbl.add_theme_font_override("font", _font)
	_badge.add_child(_badge_lbl)
	add_child(_badge)

	# 4. 結果台詞 Toast
	_label = Label.new()
	_label.name = "ResultToast"
	_label.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_label.offset_left = 20
	_label.offset_right = -20
	_label.offset_top = -78
	_label.offset_bottom = -48
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.add_theme_font_size_override("font_size", 22)
	_label.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		_label.add_theme_font_override("font", _font)
	add_child(_label)

	# 5. 掉落物細節明細
	_drop_lbl = Label.new()
	_drop_lbl.name = "DropIdLabel"
	_drop_lbl.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_drop_lbl.offset_left = 20
	_drop_lbl.offset_right = -20
	_drop_lbl.offset_top = -44
	_drop_lbl.offset_bottom = -14
	_drop_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_drop_lbl.add_theme_font_size_override("font_size", 16)
	_drop_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	if _font != null:
		_drop_lbl.add_theme_font_override("font", _font)
	add_child(_drop_lbl)

	show_placeholder()


func _build_badge_style(color: Color) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = color
	s.border_color = UiStyle.BORDER_DARK
	s.set_border_width_all(2)
	s.border_width_bottom = 3
	s.set_corner_radius_all(10)
	s.content_margin_left = 14
	s.content_margin_right = 14
	s.content_margin_top = 3
	s.content_margin_bottom = 3
	return s


func show_placeholder(toast_key: String = "soul.pull_start", card_path: String = DEFAULT_CARD) -> void:
	_ensure()
	if _i18n.is_empty():
		_load_i18n()
	var path := card_path
	if not ResourceLoader.exists(path) and not FileAccess.file_exists(path):
		path = DEFAULT_CARD
	if ResourceLoader.exists(path) or FileAccess.file_exists(path):
		_art.texture = load(path) as Texture2D
	_badge_lbl.text = "封靈"
	_badge.add_theme_stylebox_override("panel", _build_badge_style(COLOR_GOLD))
	_label.text = tr_key(toast_key)
	_drop_lbl.text = ""


func show_drop(drop: Dictionary, card_path: String = DEFAULT_CARD) -> void:
	var key: String = str(drop.get("toastKey", "soul.pull_part"))
	show_placeholder(key, card_path)
	var kind_str: String = str(drop.get("kind", ""))
	var drop_id: String = str(drop.get("DropId", ""))
	var kind_display: String = KIND_NAMES.get(kind_str, kind_str)
	var name_display: String = DROP_NAMES.get(drop_id, drop_id)

	var badge_col := COLOR_GOLD
	match kind_str:
		"outfit":
			badge_col = COLOR_ORANGE
		"part":
			badge_col = COLOR_SKY
		"junk":
			badge_col = COLOR_PINK
		_:
			badge_col = COLOR_MINT

	_badge_lbl.text = kind_display
	_badge.add_theme_stylebox_override("panel", _build_badge_style(badge_col))
	_drop_lbl.text = "【%s】 %s" % [kind_display, name_display]
