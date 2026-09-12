extends Control
## W8-F4 最小 Hub：onboard_w8 → soul_draw_play → C0 首通／掃蕩 一條龍。

const OnboardScript := preload("res://scripts/systems/onboard/onboard_view.gd")
const SoulScript := preload("res://scripts/ui/soul_draw/soul_draw_play_view.gd")
const RuntimeScript := preload("res://scripts/systems/wave8/w8_runtime.gd")
const I18N_PATH := "res://data/i18n/zh_TW.json"

enum Phase { ONBOARD, SOUL, CHAPTER }

var phase: int = Phase.ONBOARD
var _host: Control
var _banner: Label
var _toast: Label
var _chapter_panel: Control
var runtime
var _i18n: Dictionary = {}
var _child: Node = null


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
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


func _build_shell() -> void:
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.07, 0.07, 0.09, 1)
	add_child(bg)

	_banner = Label.new()
	_banner.position = Vector2(24, 8)
	_banner.add_theme_font_size_override("font_size", 18)
	_banner.add_theme_color_override("font_color", Color(0.9, 0.85, 0.65))
	add_child(_banner)

	_toast = Label.new()
	_toast.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_toast.offset_top = 36
	_toast.offset_bottom = 64
	_toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_toast.add_theme_font_size_override("font_size", 16)
	_toast.add_theme_color_override("font_color", Color(1.0, 0.92, 0.7))
	add_child(_toast)

	_host = Control.new()
	_host.name = "PhaseHost"
	_host.set_anchors_preset(Control.PRESET_FULL_RECT)
	_host.offset_top = 68
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
			_banner.text = "Hub · ① 新手 onb"
			var v = OnboardScript.new()
			v.set_anchors_preset(Control.PRESET_FULL_RECT)
			_host.add_child(v)
			_child = v
			v.finished.connect(func() -> void:
				_flash("新手完成 → 抽魂")
				_goto(Phase.SOUL)
			)
		Phase.SOUL:
			_banner.text = "Hub · ② 抽魂結果卡"
			var v = SoulScript.new()
			v.set_anchors_preset(Control.PRESET_FULL_RECT)
			_host.add_child(v)
			_child = v
			v.continue_requested.connect(func() -> void:
				_flash("前往 C0 玩具堆邊緣")
				_goto(Phase.CHAPTER)
			)
		Phase.CHAPTER:
			_banner.text = "Hub · ③ C0 首通／掃蕩 · 發條 %d/%d" % [runtime.daily.wind, runtime.daily.wind_max]
			_build_chapter_panel()


func _build_chapter_panel() -> void:
	_chapter_panel = Control.new()
	_chapter_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	_host.add_child(_chapter_panel)
	_child = _chapter_panel

	var info := Label.new()
	info.position = Vector2(48, 24)
	info.add_theme_font_size_override("font_size", 22)
	info.add_theme_color_override("font_color", Color(0.95, 0.93, 0.88))
	info.text = "章節 C0_S8「玩具堆邊緣」\nGold %d · SoulTicket %d · Lv %d\n發條 %d/%d · 今日掃蕩 %d" % [
		runtime.econ.gold, runtime.econ.soul_tickets, runtime.growth.level,
		runtime.daily.wind, runtime.daily.wind_max, runtime.daily.daily_sweeps
	]
	info.name = "Info"
	_chapter_panel.add_child(info)

	var row := HBoxContainer.new()
	row.position = Vector2(48, 160)
	row.add_theme_constant_override("separation", 16)
	_chapter_panel.add_child(row)

	var b1 := Button.new()
	b1.text = "首通 C0_S8"
	b1.custom_minimum_size = Vector2(200, 52)
	b1.pressed.connect(_on_first_clear)
	row.add_child(b1)

	var b2 := Button.new()
	b2.text = "掃蕩 C0_S8"
	b2.custom_minimum_size = Vector2(200, 52)
	b2.pressed.connect(_on_sweep)
	row.add_child(b2)

	var b3 := Button.new()
	b3.text = "等 8 分（模擬回復）"
	b3.custom_minimum_size = Vector2(220, 52)
	b3.pressed.connect(_on_sim_regen)
	row.add_child(b3)

	var b4 := Button.new()
	b4.text = "回抽魂"
	b4.custom_minimum_size = Vector2(140, 52)
	b4.pressed.connect(func() -> void: _goto(Phase.SOUL))
	row.add_child(b4)

	var hint := Label.new()
	hint.position = Vector2(48, 240)
	hint.text = "一條龍：新手 → 抽魂 → 本頁。也可開獨立場景 F6。"
	hint.add_theme_color_override("font_color", Color(0.65, 0.62, 0.55))
	_chapter_panel.add_child(hint)


func _refresh_chapter_info() -> void:
	if _chapter_panel == null:
		return
	var info: Label = _chapter_panel.get_node_or_null("Info") as Label
	if info == null:
		return
	info.text = "章節 C0_S8「玩具堆邊緣」\nGold %d · SoulTicket %d · Lv %d\n發條 %d/%d · 今日掃蕩 %d" % [
		runtime.econ.gold, runtime.econ.soul_tickets, runtime.growth.level,
		runtime.daily.wind, runtime.daily.wind_max, runtime.daily.daily_sweeps
	]
	_banner.text = "Hub · ③ C0 首通／掃蕩 · 發條 %d/%d" % [runtime.daily.wind, runtime.daily.wind_max]


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
			_flash("需先首通，或體力／日限不足")
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
