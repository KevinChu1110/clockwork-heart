extends Control
## W8-F4 最小 Hub：onboard_w8 → soul_draw_play → C0 首通／掃蕩 一條龍。

const OnboardScript := preload("res://scripts/systems/onboard/onboard_view.gd")
const SoulScript := preload("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
const RuntimeScript := preload("res://scripts/systems/wave8/w8_runtime.gd")
const UiStyle := preload("res://scripts/ui/ui_style.gd")
const I18N_PATH := "res://data/i18n/zh_TW.json"
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

enum Phase { ONBOARD, SOUL, CHAPTER }

var phase: int = Phase.ONBOARD
var _host: Control
var _banner: Label
var _toast: Label
var _chapter_panel: Control
var runtime
var _i18n: Dictionary = {}
var _child: Node = null
var _font: Font = null


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	anchor_right = 1.0
	anchor_bottom = 1.0
	grow_horizontal = Control.GROW_DIRECTION_BOTH
	grow_vertical = Control.GROW_DIRECTION_BOTH
	custom_minimum_size = Vector2(1280, 720)

	if ResourceLoader.exists(FONT_PATH):
		_font = load(FONT_PATH) as Font
	if FileAccess.file_exists(I18N_PATH):
		var parsed = JSON.parse_string(FileAccess.get_file_as_string(I18N_PATH))
		if typeof(parsed) == TYPE_DICTIONARY:
			_i18n = parsed as Dictionary
	_build_shell()
	runtime = RuntimeScript.new()
	runtime.setup()
	_goto(Phase.ONBOARD)


func _tr(key: String) -> String:
	return str(_i18n.get(key, key))


func _apply_label(lbl: Label, font_size: int, color: Color, outline: bool = false) -> void:
	lbl.add_theme_font_size_override("font_size", font_size)
	lbl.add_theme_color_override("font_color", color)
	if outline:
		lbl.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.95))
		lbl.add_theme_constant_override("outline_size", 2)
	if _font != null:
		lbl.add_theme_font_override("font", _font)


func _build_shell() -> void:
	var bg := Panel.new()
	bg.name = "BackgroundPanel"
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.anchor_right = 1.0
	bg.anchor_bottom = 1.0
	bg.grow_horizontal = Control.GROW_DIRECTION_BOTH
	bg.grow_vertical = Control.GROW_DIRECTION_BOTH
	var bg_style := StyleBoxFlat.new()
	bg_style.bg_color = UiStyle.TATA_CARD_BG
	bg.add_theme_stylebox_override("panel", bg_style)
	add_child(bg)

	_banner = Label.new()
	_banner.name = "Banner"
	_banner.position = Vector2(40, 14)
	_apply_label(_banner, 24, UiStyle.INK, true)
	add_child(_banner)

	_toast = Label.new()
	_toast.name = "Toast"
	_toast.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_toast.offset_top = 40
	_toast.offset_bottom = 72
	_toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label(_toast, 22, UiStyle.TATA_ORANGE, true)
	add_child(_toast)

	_host = Control.new()
	_host.name = "PhaseHost"
	_host.set_anchors_preset(Control.PRESET_FULL_RECT)
	_host.anchor_right = 1.0
	_host.anchor_bottom = 1.0
	_host.offset_top = 74
	_host.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_host.grow_vertical = Control.GROW_DIRECTION_BOTH
	add_child(_host)


func _clear_host() -> void:
	if _child != null and is_instance_valid(_child):
		_child.queue_free()
	_child = null
	for c in _host.get_children():
		c.queue_free()


func _goto(p: int) -> void:
	phase = p
	_clear_host()
	match p:
		Phase.ONBOARD:
			_banner.text = "玩具堆邊緣 · 新手引導"
			var v = OnboardScript.new()
			v.set_anchors_preset(Control.PRESET_FULL_RECT)
			_host.add_child(v)
			_child = v
			v.finished.connect(func() -> void:
				_flash("新手引導完成，前往聚魂")
				_goto(Phase.SOUL)
			)
		Phase.SOUL:
			_banner.text = "玩具堆邊緣 · 聚魂抽取"
			var v = SoulScript.new()
			v.set_anchors_preset(Control.PRESET_FULL_RECT)
			_host.add_child(v)
			_child = v
			v.continue_requested.connect(func() -> void:
				_flash("前往玩具堆邊緣")
				_goto(Phase.CHAPTER)
			)
		Phase.CHAPTER:
			_banner.text = "玩具堆邊緣 · 首通與掃蕩 · 發條 %d/%d" % [runtime.daily.wind, runtime.daily.wind_max]
			_build_chapter_panel()
			_refresh_daily_event_ui()


func _build_chapter_panel() -> void:
	var card := Panel.new()
	card.name = "ChapterPanel"
	card.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.anchor_right = 1.0
	card.anchor_bottom = 1.0
	card.offset_left = 40
	card.offset_top = 16
	card.offset_right = -40
	card.offset_bottom = -28
	card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	card.grow_vertical = Control.GROW_DIRECTION_BOTH
	card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_host.add_child(card)
	_chapter_panel = card
	_child = card

	var info := Label.new()
	info.name = "Info"
	info.position = Vector2(36, 26)
	_apply_label(info, 22, UiStyle.INK)
	info.text = "章節「玩具堆邊緣」\n金幣 %d · 聚魂券 %d · 等級 %d\n發條 %d/%d · 今日掃蕩 %d" % [
		runtime.econ.gold, runtime.econ.soul_tickets, runtime.growth.level,
		runtime.daily.wind, runtime.daily.wind_max, runtime.daily.daily_sweeps
	]
	_chapter_panel.add_child(info)

	var row := HBoxContainer.new()
	row.position = Vector2(36, 144)
	row.add_theme_constant_override("separation", 16)
	_chapter_panel.add_child(row)

	var b1 := Button.new()
	b1.text = "首通 玩具堆邊緣"
	b1.custom_minimum_size = Vector2(210, 52)
	UiStyle.style_button(b1, true)
	b1.pressed.connect(_on_first_clear)
	row.add_child(b1)

	var b2 := Button.new()
	b2.text = "掃蕩 玩具堆邊緣"
	b2.custom_minimum_size = Vector2(210, 52)
	UiStyle.style_button(b2, false)
	b2.pressed.connect(_on_sweep)
	row.add_child(b2)

	var b3 := Button.new()
	b3.text = "等 8 分（模擬回復）"
	b3.custom_minimum_size = Vector2(220, 52)
	UiStyle.style_button(b3, false)
	b3.pressed.connect(_on_sim_regen)
	row.add_child(b3)

	var b4 := Button.new()
	b4.text = "前往聚魂"
	b4.custom_minimum_size = Vector2(160, 52)
	UiStyle.style_button(b4, false)
	b4.pressed.connect(func() -> void: _goto(Phase.SOUL))
	row.add_child(b4)

	_build_daily_event_block()

	var hint := Label.new()
	hint.name = "Hint"
	hint.position = Vector2(36, 460)
	hint.text = "引導流程：新手引導 → 聚魂抽取 → 章節挑戰。日常發條每日一選，漏天不補。"
	_apply_label(hint, 17, Color(0.36, 0.26, 0.18, 1.0))
	_chapter_panel.add_child(hint)


func _refresh_chapter_info() -> void:
	if _chapter_panel == null:
		return
	var info: Label = _chapter_panel.get_node_or_null("Info") as Label
	if info == null:
		return
	info.text = "章節「玩具堆邊緣」\n金幣 %d · 聚魂券 %d · 等級 %d\n發條 %d/%d · 今日掃蕩 %d" % [
		runtime.econ.gold, runtime.econ.soul_tickets, runtime.growth.level,
		runtime.daily.wind, runtime.daily.wind_max, runtime.daily.daily_sweeps
	]
	_banner.text = "玩具堆邊緣 · 首通與掃蕩 · 發條 %d/%d" % [runtime.daily.wind, runtime.daily.wind_max]
	_refresh_daily_event_ui()


func _flash(msg: String) -> void:
	_toast.text = msg


func _on_first_clear() -> void:
	runtime.daily.wind = max(runtime.daily.wind, 15)
	var r: Dictionary = runtime.do_first_clear("C0_S8")
	if bool(r.get("ok", false)):
		_flash(_tr(str(r.get("toastKey", "reward.first_clear"))))
	else:
		_flash("首通失敗：%s" % str(r.get("error", "")))
	_refresh_chapter_info()


func _on_sweep() -> void:
	runtime.daily.wind = max(runtime.daily.wind, int(runtime.config.chapter_def("C0_S8").get("staminaEnter", 2)))
	runtime.econ.gold = max(runtime.econ.gold, 100)
	var r: Dictionary = runtime.do_sweep("C0_S8")
	if bool(r.get("ok", false)):
		_flash(_tr(str(r.get("toastKey", "reward.sweep"))))
	else:
		var err: String = str(r.get("error", ""))
		if err == "daily_sweep_cap":
			_flash(_tr("err.daily_cap_sweep"))
		elif err == "already_cleared_use_sweep" or err == "cannot_sweep":
			_flash("需先首通，或發條／掃蕩次數不足")
		else:
			_flash("掃蕩失敗：%s" % err)
	_refresh_chapter_info()


func _on_sim_regen() -> void:
	## 模擬過 8 分鐘，讓回復可感知
	runtime.daily.last_regen_unix = Time.get_unix_time_from_system() - 8 * 60
	var before: int = runtime.daily.wind
	var gained: int = runtime.daily.tick_regen()
	_flash("%s（%d→%d，＋%d）" % [_tr("reward.stamina_regen"), before, runtime.daily.wind, gained])
	_refresh_chapter_info()


func _build_daily_event_block() -> void:
	var box := VBoxContainer.new()
	box.name = "DailyEventBox"
	box.position = Vector2(36, 240)
	box.add_theme_constant_override("separation", 12)
	_chapter_panel.add_child(box)

	var title := Label.new()
	title.name = "DailyTitle"
	_apply_label(title, 22, UiStyle.INK, true)
	box.add_child(title)

	var body := Label.new()
	body.name = "DailyBody"
	_apply_label(body, 18, Color(0.32, 0.22, 0.14, 1.0))
	box.add_child(body)

	var row := HBoxContainer.new()
	row.name = "DailyChoices"
	row.add_theme_constant_override("separation", 16)
	box.add_child(row)

	_refresh_daily_event_ui()


func _format_daily_toast(toast_key: String, tokens: Dictionary) -> String:
	var tpl: String = _tr(toast_key)
	for k in tokens.keys():
		tpl = tpl.replace("{%s}" % str(k), str(tokens[k]))
	return tpl


func _refresh_daily_event_ui() -> void:
	if _chapter_panel == null:
		return
	var box: VBoxContainer = _chapter_panel.get_node_or_null("DailyEventBox") as VBoxContainer
	if box == null:
		return
	var title: Label = box.get_node_or_null("DailyTitle") as Label
	var body: Label = box.get_node_or_null("DailyBody") as Label
	var row: HBoxContainer = box.get_node_or_null("DailyChoices") as HBoxContainer
	if title == null or row == null:
		return
	for c in row.get_children():
		c.queue_free()

	var info: Dictionary = runtime.today_daily_event()
	var ev: Dictionary = info.get("event", {}) as Dictionary
	var day_id: String = str(ev.get("DayId", "?"))
	var picked: bool = bool(info.get("picked", false))
	if picked:
		title.text = "%s · %s" % [_tr("daily.title"), _tr("daily.already")]
	else:
		title.text = _tr("daily.title")
	if body != null:
		body.text = _tr("daily.%s.body" % day_id)

	for ch in ev.get("choices", []) as Array:
		if typeof(ch) != TYPE_DICTIONARY:
			continue
		var choice: Dictionary = ch as Dictionary
		var cid: String = str(choice.get("ChoiceId", ""))
		var label_key: String = "daily.%s.%s" % [day_id, cid]
		var label: String = _tr(label_key)
		if label == label_key:
			label = str(choice.get("label", cid))
		var b := Button.new()
		b.text = label
		b.custom_minimum_size = Vector2(220, 52)
		b.disabled = picked
		UiStyle.style_button(b, not picked)
		var pick_id: String = cid
		b.pressed.connect(func() -> void: _on_daily_pick(pick_id))
		row.add_child(b)


func _on_daily_pick(choice_id: String) -> void:
	var r: Dictionary = runtime.do_daily_event_pick(choice_id)
	if bool(r.get("ok", false)):
		var tokens: Dictionary = r.get("tokens", {}) as Dictionary
		_flash(_format_daily_toast(str(r.get("toastKey", "reward.daily_event")), tokens))
	else:
		var err: String = str(r.get("error", ""))
		if err == "already_picked":
			_flash(_tr("daily.already"))
		else:
			_flash("日常發條失敗：%s" % err)
	_refresh_chapter_info()
	_refresh_daily_event_ui()
