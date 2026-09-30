extends Control
signal continue_requested
## SoulDraw 可玩 UI：扣票 → 發條儀式召喚動效 → 單抽/十連抽多巴胺結果卡。
## ⛔ 不開第二轉蛋；唯一池＝soul_draw_v2。

const UiStyle := preload("res://scripts/ui/ui_style.gd")
const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const LoadoutScript := preload("res://scripts/systems/paper_doll_v2/character_loadout.gd")
const EconScript := preload("res://scripts/systems/wave8/w8_economy.gd")
const ConfigK1 := preload("res://scripts/systems/wave8/w8_k1_config.gd")
const CardScript := preload("res://scripts/ui/soul_draw/soul_result_card_view.gd")
const DailyScript := preload("res://scripts/systems/wave8/w8_daily_cycle.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const SummonFxScript := preload("res://scripts/ui/soul_draw/soul_summon_fx.gd")
const TenPullScript := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

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

var pool
var loadout
var econ
var daily
var card
var _title_lbl: Label
var _ticket_lbl: Label
var _footprint_lbl: Label
var _log: RichTextLabel
var _btn: Button
var _btn_ten: Button
var _cont_btn: Button
var _err: Label
var _summon_fx: Control
var _ten_pull_view: Control
var _font: Font = null
var _last_err_key: String = ""


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()


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
	_refresh()


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_load_font()
	_build()
	_connect_loc_signal()
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

	# 1. 溫潤奶油全屏底板（#FFFDF8）
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = UiStyle.CREAM
	add_child(bg)

	var outer_panel := Panel.new()
	outer_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	outer_panel.offset_left = 12
	outer_panel.offset_top = 12
	outer_panel.offset_right = -12
	outer_panel.offset_bottom = -12
	outer_panel.add_theme_stylebox_override("panel", UiStyle.panel_style())
	add_child(outer_panel)

	# 2. 標題（一級字 26px，深暖褐 INK）
	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("抽魂 · 封靈罐")
	_title_lbl.position = Vector2(40, 24)
	_title_lbl.add_theme_font_size_override("font_size", 26)
	_title_lbl.add_theme_color_override("font_color", UiStyle.INK)
	if _font != null:
		_title_lbl.add_theme_font_override("font", _font)
	add_child(_title_lbl)

	# 3. 票數資訊（二級字 18px，深暖褐次級字）
	_ticket_lbl = Label.new()
	_ticket_lbl.name = "TicketLabel"
	_ticket_lbl.position = Vector2(40, 62)
	_ticket_lbl.add_theme_font_size_override("font_size", 18)
	_ticket_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	if _font != null:
		_ticket_lbl.add_theme_font_override("font", _font)
	add_child(_ticket_lbl)

	# 3b. 足跡連線提示（二級字 15px，深暖褐次級字）
	_footprint_lbl = Label.new()
	_footprint_lbl.name = "FootprintLabel"
	_footprint_lbl.position = Vector2(40, 90)
	_footprint_lbl.add_theme_font_size_override("font_size", 15)
	_footprint_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	if _font != null:
		_footprint_lbl.add_theme_font_override("font", _font)
	add_child(_footprint_lbl)

	# 4. 結果卡（多巴胺果凍色階光框規格）
	card = CardScript.new()
	card.name = "SoulResultCard"
	card.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.offset_left = 40
	card.offset_top = 118
	card.offset_right = -40
	card.offset_bottom = -165
	add_child(card)

	# 5. 錯誤提示（三級字 16px，深色 DANGER）
	_err = Label.new()
	_err.name = "ErrorLabel"
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

	# 6. 單抽主按鈕「上緊——抽一格」（消耗 1 票）
	_btn = Button.new()
	_btn.name = "PullBtn"
	_btn.text = _t("上緊——抽一格")
	_btn.custom_minimum_size = Vector2(200, 54)
	_btn.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_btn.offset_left = -215
	_btn.offset_right = -15
	_btn.offset_top = -128
	_btn.offset_bottom = -74
	_btn.pressed.connect(_on_pull)
	UiStyle.style_button(_btn, true)
	if _font != null:
		_btn.add_theme_font_override("font", _font)
	add_child(_btn)

	# 6b. 十連抽主按鈕「連轉——抽十格」（消耗 10 票，多巴胺亮橘果凍）
	_btn_ten = Button.new()
	_btn_ten.name = "PullTenBtn"
	_btn_ten.text = _t("連轉——抽十格")
	_btn_ten.custom_minimum_size = Vector2(200, 54)
	_btn_ten.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_btn_ten.offset_left = 15
	_btn_ten.offset_right = 215
	_btn_ten.offset_top = -128
	_btn_ten.offset_bottom = -74
	_btn_ten.pressed.connect(_on_pull_ten)
	UiStyle.style_button(_btn_ten, true)
	# 增強十連抽按鈕的多巴胺果凍暖橘感
	var ten_style := StyleBoxFlat.new()
	ten_style.bg_color = Color("#FFA010")
	ten_style.border_color = Color("#1F1A3A")
	ten_style.set_border_width_all(3)
	ten_style.border_width_bottom = 6
	ten_style.set_corner_radius_all(18)
	ten_style.shadow_color = Color(1.0, 0.63, 0.06, 0.5)
	ten_style.shadow_size = 10
	_btn_ten.add_theme_stylebox_override("normal", ten_style)
	if _font != null:
		_btn_ten.add_theme_font_override("font", _font)
	add_child(_btn_ten)

	# 7. 次按鈕「去玩具堆邊緣」（高度 50px ≥ 50px）
	_cont_btn = Button.new()
	_cont_btn.name = "ContinueBtn"
	_cont_btn.text = _t("去玩具堆邊緣")
	_cont_btn.custom_minimum_size = Vector2(300, 50)
	_cont_btn.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	_cont_btn.offset_left = -150
	_cont_btn.offset_right = 150
	_cont_btn.offset_top = -66
	_cont_btn.offset_bottom = -16
	_cont_btn.pressed.connect(func() -> void: continue_requested.emit())
	UiStyle.style_button(_cont_btn, false)
	if _font != null:
		_cont_btn.add_theme_font_override("font", _font)
	add_child(_cont_btn)

	# 8. 相容性 log（不可見，不覆蓋畫面）
	_log = RichTextLabel.new()
	_log.visible = false
	add_child(_log)

	# 9. 召喚儀式感動效層（發條鑰匙上鍊、金色齒輪解鎖、彩糖星芒爆散）
	_summon_fx = SummonFxScript.new()
	_summon_fx.name = "SoulSummonFx"
	add_child(_summon_fx)
	_summon_fx.set_anchors_preset(Control.PRESET_FULL_RECT)
	_summon_fx.offset_left = 0
	_summon_fx.offset_top = 0
	_summon_fx.offset_right = 0
	_summon_fx.offset_bottom = 0

	# 10. 十連抽多巴胺結果面板（5x2 陣列、色階光框、流光）
	_ten_pull_view = TenPullScript.new()
	_ten_pull_view.name = "SoulTenPullView"
	_ten_pull_view.pull_again_requested.connect(_on_pull_ten)
	add_child(_ten_pull_view)
	_ten_pull_view.set_anchors_preset(Control.PRESET_FULL_RECT)
	_ten_pull_view.offset_left = 0
	_ten_pull_view.offset_top = 0
	_ten_pull_view.offset_right = 0
	_ten_pull_view.offset_bottom = 0


func _refresh() -> void:
	if _title_lbl and is_instance_valid(_title_lbl):
		_title_lbl.text = _t("抽魂 · 封靈罐")
	if _btn and is_instance_valid(_btn):
		_btn.text = _t("上緊——抽一格")
	if _btn_ten and is_instance_valid(_btn_ten):
		_btn_ten.text = _t("連轉——抽十格")
	if _cont_btn and is_instance_valid(_cont_btn):
		_cont_btn.text = _t("去玩具堆邊緣")
	if _ticket_lbl and is_instance_valid(_ticket_lbl):
		var tickets: int = econ.soul_tickets if econ != null else 0
		var pulls: int = daily.daily_soul_pulls if daily != null else 0
		_ticket_lbl.text = _t("封靈票 ×%d · 今日已抽 %d") % [tickets, pulls]
	if _footprint_lbl and is_instance_valid(_footprint_lbl):
		_footprint_lbl.text = _get_footprint_line()
	if _err and is_instance_valid(_err):
		if _last_err_key == "lack_tickets":
			_err.text = _t("封靈票不足")
		elif _last_err_key == "daily_cap":
			_err.text = _t("err.daily_cap_pull")
			if _err.text == "err.daily_cap_pull" and card != null and card.has_method("tr_key"):
				_err.text = card.tr_key("err.daily_cap_pull")
		elif _last_err_key == "":
			_err.text = ""
	if card and is_instance_valid(card) and card.has_method("refresh"):
		card.refresh()


func _on_pull() -> void:
	_last_err_key = ""
	_err.text = ""
	if not daily.can_soul_pull():
		_last_err_key = "daily_cap"
		_err.text = _t("err.daily_cap_pull")
		if _err.text == "err.daily_cap_pull" and card != null and card.has_method("tr_key"):
			_err.text = card.tr_key("err.daily_cap_pull")
		return
	if not econ.spend_soul_pull():
		_last_err_key = "lack_tickets"
		_err.text = _t("封靈票不足")
		return

	daily.note_soul_pull()
	var drop: Dictionary = pool.pull()
	loadout.apply_soul_drop(drop)
	_log.append_text("%s\n" % str(drop))

	# 播放召喚儀式動效後展示結果卡
	if _summon_fx and is_instance_valid(_summon_fx):
		_summon_fx.play_summon(false, func():
			card.show_drop(drop)
		)
	else:
		card.show_drop(drop)

	_refresh()


func _on_pull_ten() -> void:
	_last_err_key = ""
	_err.text = ""

	# 檢查是否能進行 10 抽
	var remaining_cap: int = 30 - daily.daily_soul_pulls
	if remaining_cap < 10:
		_last_err_key = "daily_cap"
		_err.text = _t("err.daily_cap_pull")
		if _err.text == "err.daily_cap_pull" and card != null and card.has_method("tr_key"):
			_err.text = card.tr_key("err.daily_cap_pull")
		return

	if econ.soul_tickets < 10:
		_last_err_key = "lack_tickets"
		_err.text = _t("封靈票不足")
		return

	var drops: Array[Dictionary] = []
	for i in range(10):
		if not econ.spend_soul_pull():
			break
		daily.note_soul_pull()
		var drop: Dictionary = pool.pull()
		loadout.apply_soul_drop(drop)
		drops.append(drop)
		_log.append_text("%s\n" % str(drop))

	# 播放十連召喚儀式動效後展開十連結果面板
	if _summon_fx and is_instance_valid(_summon_fx):
		_summon_fx.play_summon(true, func():
			if _ten_pull_view and is_instance_valid(_ten_pull_view):
				_ten_pull_view.show_drops(drops)
		)
	elif _ten_pull_view and is_instance_valid(_ten_pull_view):
		_ten_pull_view.show_drops(drops)

	_refresh()


func _get_footprint_line() -> String:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var ss: Node = (loop as SceneTree).root.get_node_or_null("SoulSystem")
		if ss and ss.has_method("ritual_footprint_line"):
			return str(ss.call("ritual_footprint_line"))
	return ""
