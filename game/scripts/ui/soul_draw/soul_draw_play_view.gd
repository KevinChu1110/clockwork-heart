extends Control
signal continue_requested
## SoulDraw 可玩 UI：扣票 → 抽一格 → 結果卡。
## ⛔ 不開第二轉蛋；唯一池＝soul_draw_v2。

const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const LoadoutScript := preload("res://scripts/systems/paper_doll_v2/character_loadout.gd")
const EconScript := preload("res://scripts/systems/wave8/w8_economy.gd")
const ConfigK1 := preload("res://scripts/systems/wave8/w8_k1_config.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const DailyScript := preload("res://scripts/systems/wave8/w8_daily_cycle.gd")

var pool
var loadout
var econ
var daily
var card
var _ticket_lbl: Label
var _log: RichTextLabel
var _btn: Button
var _err: Label


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
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


func _build() -> void:
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.09, 0.08, 0.11, 1)
	add_child(bg)

	var title := Label.new()
	title.text = "抽魂 · 唯一池"
	title.position = Vector2(40, 24)
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color(0.95, 0.9, 0.75))
	add_child(title)

	_ticket_lbl = Label.new()
	_ticket_lbl.position = Vector2(40, 64)
	_ticket_lbl.add_theme_font_size_override("font_size", 18)
	add_child(_ticket_lbl)

	card = CardScript.new()
	card.name = "SoulResultCard"
	card.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.offset_left = 80
	card.offset_top = 100
	card.offset_right = -80
	card.offset_bottom = -180
	add_child(card)

	_btn = Button.new()
	_btn.text = "上緊——抽一格"
	_btn.custom_minimum_size = Vector2(280, 56)
	_btn.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_btn.offset_left = -140
	_btn.offset_right = 140
	_btn.offset_top = -140
	_btn.offset_bottom = -84
	_btn.pressed.connect(_on_pull)
	add_child(_btn)

	var cont := Button.new()
	cont.name = "ContinueBtn"
	cont.text = "去玩具堆邊緣（C0）"
	cont.custom_minimum_size = Vector2(280, 48)
	cont.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	cont.offset_left = -140
	cont.offset_right = 140
	cont.offset_top = -76
	cont.offset_bottom = -28
	cont.pressed.connect(func() -> void: continue_requested.emit())
	add_child(cont)

	_err = Label.new()
	_err.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_err.offset_top = -72
	_err.offset_bottom = -40
	_err.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_err.add_theme_color_override("font_color", Color(1.0, 0.75, 0.45))
	add_child(_err)

	_log = RichTextLabel.new()
	_log.position = Vector2(40, 420)
	_log.size = Vector2(360, 200)
	_log.bbcode_enabled = false
	add_child(_log)


func _refresh() -> void:
	_ticket_lbl.text = "SoulTicket ×%d · 今日已抽 %d" % [econ.soul_tickets, daily.daily_soul_pulls]


func _on_pull() -> void:
	_err.text = ""
	if not daily.can_soul_pull():
		_err.text = card.tr_key("err.daily_cap_pull")
		return
	if not econ.spend_soul_pull():
		_err.text = "抽魂票不足"
		return
	daily.note_soul_pull()
	card.show_placeholder("soul.pull_start")
	var drop: Dictionary = pool.pull()
	loadout.apply_soul_drop(drop)
	card.show_drop(drop)
	_log.append_text("%s\n" % str(drop))
	_refresh()
