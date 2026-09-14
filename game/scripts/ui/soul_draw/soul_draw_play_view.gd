extends Control
signal continue_requested
## SoulDraw 可玩 UI：扣票 → 抽一格 → 結果卡。
## ⛔ 不開第二轉蛋；唯一池＝soul_draw_v2。

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const LoadoutScript := preload("res://scripts/systems/paper_doll_v2/character_loadout.gd")
const EconScript := preload("res://scripts/systems/wave8/w8_economy.gd")
const ConfigK1 := preload("res://scripts/systems/wave8/w8_k1_config.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const DailyScript := preload("res://scripts/systems/wave8/w8_daily_cycle.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

var pool
var loadout
var econ
var daily
var card
var _ticket_lbl: Label
var _log: RichTextLabel
var _btn: Button
var _err: Label
var _font: Font = null


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_load_font()
	_build()
	var k1 = ConfigK1.new()
	k1.load_from()
	econ = EconScript.new()
	econ.setup(k1, 100, 3)
	daily = DailyScript.new()
	daily.setup(k1)
	pool = PoolScript.new()
	pool.setup()
	loadout = LoadoutScript.new()
	loadout.setup()
	_refresh()


func _load_font() -> void:
	if _font == null and ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font


func _build() -> void:
	_load_font()

	# 1. 溫潤奶油全屏底板（取代 0.09 黑底）
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = UiStyle.TATA_CARD_BG
	add_child(bg)

	var outer_panel := Panel.new()
	outer_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	outer_panel.offset_left = 12
	outer_panel.offset_top = 12
	outer_panel.offset_right = -12
	outer_panel.offset_bottom = -12
	outer_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	add_child(outer_panel)

	# 2. 標題（一級字 26px，深暖褐 INK，封靈罐）
	var title := Label.new()
	title.text = "抽魂 · 封靈罐"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		title.add_theme_font_override("font", _font)
	add_child(title)

	# 3. 票數資訊（二級字 18px，深暖褐次級字）
	_ticket_lbl = Label.new()
	_ticket_lbl.position = Vector2(40, 62)
	_ticket_lbl.add_theme_font_size_override("font_size", 18)
	_ticket_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	if _font != null:
		_ticket_lbl.add_theme_font_override("font", _font)
	add_child(_ticket_lbl)

	# 4. 結果卡（奶油卡規格）
	card = CardScript.new()
	card.name = "SoulResultCard"
	card.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.offset_left = 40
	card.offset_top = 96
	card.offset_right = -40
	card.offset_bottom = -165
	add_child(card)

	# 5. 錯誤提示（三級字 16px，深色 DANGER，不可亮底亮字）
	_err = Label.new()
	_err.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_err.offset_left = -200
	_err.offset_right = 200
	_err.offset_top = -158
	_err.offset_bottom = -132
	_err.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_err.add_theme_font_size_override("font_size", 16)
	_err.add_theme_color_override("font_color", UiStyle.DANGER)
	if _font != null:
		_err.add_theme_font_override("font", _font)
	add_child(_err)

	# 6. 主按鈕「上緊——抽一格」（UiStyle.style_button(btn, true)，高度 54px ≥ 50px）
	_btn = Button.new()
	_btn.text = "上緊——抽一格"
	_btn.custom_minimum_size = Vector2(300, 54)
	_btn.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_btn.offset_left = -150
	_btn.offset_right = 150
	_btn.offset_top = -128
	_btn.offset_bottom = -74
	_btn.pressed.connect(_on_pull)
	UiStyle.style_button(_btn, true)
	if _font != null:
		_btn.add_theme_font_override("font", _font)
	add_child(_btn)

	# 7. 次按鈕「去玩具堆邊緣（C0）」（UiStyle.style_button(btn, false)，高度 50px ≥ 50px）
	var cont := Button.new()
	cont.name = "ContinueBtn"
	cont.text = "去玩具堆邊緣"
	cont.custom_minimum_size = Vector2(300, 50)
	cont.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	cont.offset_left = -150
	cont.offset_right = 150
	cont.offset_top = -66
	cont.offset_bottom = -16
	cont.pressed.connect(func() -> void: continue_requested.emit())
	UiStyle.style_button(cont, false)
	if _font != null:
		cont.add_theme_font_override("font", _font)
	add_child(cont)

	# 8. 相容性 log（不可見，不覆蓋畫面）
	_log = RichTextLabel.new()
	_log.visible = false
	add_child(_log)


func _refresh() -> void:
	_ticket_lbl.text = "封靈票 ×%d · 今日已抽 %d" % [econ.soul_tickets, daily.daily_soul_pulls]


func _on_pull() -> void:
	_err.text = ""
	if not daily.can_soul_pull():
		_err.text = card.tr_key("err.daily_cap_pull")
		return
	if not econ.spend_soul_pull():
		_err.text = "封靈票不足"
		return
	daily.note_soul_pull()
	card.show_placeholder("soul.pull_start")
	var drop: Dictionary = pool.pull()
	loadout.apply_soul_drop(drop)
	card.show_drop(drop)
	_log.append_text("%s\n" % str(drop))
	_refresh()
