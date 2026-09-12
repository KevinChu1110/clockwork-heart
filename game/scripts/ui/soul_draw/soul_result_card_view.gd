extends Control
## 抽魂結果卡：Alice 圖＋Bingo toast（可解析 i18n）。
## 模組邊界：只顯示；抽獎在 soul_draw_v2。

const DEFAULT_CARD := "res://assets/sprites/pack_a/v2/ui/soul_result_card.png"
const I18N_PATH := "res://data/i18n/zh_TW.json"

var _art: TextureRect
var _label: Label
var _drop_lbl: Label
var _i18n: Dictionary = {}


func _ready() -> void:
	_load_i18n()
	_ensure()


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
	_art = TextureRect.new()
	_art.name = "ResultCardArt"
	_art.set_anchors_preset(Control.PRESET_FULL_RECT)
	_art.offset_bottom = -120
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	add_child(_art)
	_label = Label.new()
	_label.name = "ResultToast"
	_label.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_label.offset_top = -110
	_label.offset_bottom = -60
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.add_theme_font_size_override("font_size", 22)
	_label.add_theme_color_override("font_color", Color(0.95, 0.92, 0.82))
	add_child(_label)
	_drop_lbl = Label.new()
	_drop_lbl.name = "DropIdLabel"
	_drop_lbl.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_drop_lbl.offset_top = -52
	_drop_lbl.offset_bottom = -12
	_drop_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_drop_lbl.add_theme_font_size_override("font_size", 16)
	_drop_lbl.add_theme_color_override("font_color", Color(0.75, 0.78, 0.7))
	add_child(_drop_lbl)
	show_placeholder()


func show_placeholder(toast_key: String = "soul.pull_start", card_path: String = DEFAULT_CARD) -> void:
	_ensure()
	if _i18n.is_empty():
		_load_i18n()
	var path := card_path
	if not ResourceLoader.exists(path) and not FileAccess.file_exists(path):
		path = DEFAULT_CARD
	if ResourceLoader.exists(path) or FileAccess.file_exists(path):
		_art.texture = load(path) as Texture2D
	_label.text = tr_key(toast_key)
	_drop_lbl.text = ""


func show_drop(drop: Dictionary, card_path: String = DEFAULT_CARD) -> void:
	var key: String = str(drop.get("toastKey", "soul.pull_part"))
	show_placeholder(key, card_path)
	_drop_lbl.text = "%s · %s" % [str(drop.get("kind", "")), str(drop.get("DropId", ""))]
