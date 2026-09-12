extends Control
## 抽魂結果卡占位：掛 Alice `soul_result_card.png`＋Bingo toast key。
## 模組邊界：只顯示；抽獎邏輯在 soul_draw_v2。

const DEFAULT_CARD := "res://assets/sprites/pack_a/v2/ui/soul_result_card.png"

var _art: TextureRect
var _label: Label


func _ready() -> void:
	_ensure()


func _ensure() -> void:
	if _art != null:
		return
	_art = TextureRect.new()
	_art.name = "ResultCardArt"
	_art.set_anchors_preset(Control.PRESET_FULL_RECT)
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	add_child(_art)
	_label = Label.new()
	_label.name = "ResultToast"
	_label.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_label.offset_top = -72
	_label.offset_bottom = -16
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.add_theme_font_size_override("font_size", 20)
	add_child(_label)
	show_placeholder()


func show_placeholder(toast_key: String = "soul.pull_start", card_path: String = DEFAULT_CARD) -> void:
	_ensure()
	var path := card_path
	if not ResourceLoader.exists(path) and not FileAccess.file_exists(path):
		path = DEFAULT_CARD
	if ResourceLoader.exists(path) or FileAccess.file_exists(path):
		_art.texture = load(path) as Texture2D
	_label.text = toast_key


func show_drop(drop: Dictionary, card_path: String = DEFAULT_CARD) -> void:
	var key: String = str(drop.get("toastKey", "soul.pull_part"))
	show_placeholder(key, card_path)
