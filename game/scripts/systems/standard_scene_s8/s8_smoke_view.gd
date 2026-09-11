extends Control
## §8 可玩切片 View：三相按鈕 + 胸口光環 HUD + 糖果屑 VFX + Pack-A 藝術。
## 執行：Godot 4.7 開 scenes/s8_smoke/s8_smoke.tscn（F6）。
## 空白鍵／滑鼠＝逐步；H＝一次自動跑完；底列三相鈕＝探索／戰鬥／拆解。

const WindStaminaScript := preload("res://scripts/systems/wind_stamina/wind_stamina.gd")
const ChestGlowHudScript := preload("res://scripts/systems/wind_stamina/chest_glow_hud.gd")
const S8SmokeFlowScript := preload("res://scripts/systems/standard_scene_s8/s8_smoke_flow.gd")
const CandyChipVfxScript := preload("res://scripts/systems/candy_chip_vfx/candy_chip_vfx.gd")

const TEX_EXPLORE := "res://assets/sprites/s8_smoke/e03_explore.png"
const TEX_COMBAT := "res://assets/sprites/s8_smoke/b02_combat.png"
const TEX_DISMANTLE := "res://assets/sprites/s8_smoke/d02_dismantle.png"
## Alice Pack-A（缺檔不崩潰）
const TEX_CEL_B02 := "res://assets/sprites/pack_a/xiaobai_b02_cel.png"

var flow: S8SmokeFlow
var hud: ChestGlowHud
var _art: TextureRect
var _dialog: Label
var _phase_lbl: Label
var _hint: Label
var _log: RichTextLabel
var _chest_anchor: Control
var _cost_lbl: Label
var _btn_explore: Button
var _btn_combat: Button
var _btn_dismantle: Button
var _drop_preview: TextureRect
var _toast: Label
var _done: bool = false
var _deadline_highlight: bool = false
var _dismantle_pulse: Tween


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_build()
	flow = S8SmokeFlowScript.new()
	flow.auto_advance = false
	flow.setup()
	hud.setup(flow.wind)
	flow.phase_changed.connect(_on_phase)
	flow.log_line.connect(_on_log)
	flow.finished.connect(_on_finished)
	flow.part_break_fx.connect(_on_part_break_fx)
	flow.stamina_spent.connect(_on_stamina_spent)
	flow.err_toast.connect(_on_err_toast)
	flow.first_break_deadline.connect(_on_first_break_deadline)
	flow.start()
	_refresh_art()
	_refresh_phase_buttons()
	set_process(true)


func _build() -> void:
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.10, 0.09, 0.12, 1.0)
	add_child(bg)

	_art = TextureRect.new()
	_art.set_anchors_preset(Control.PRESET_FULL_RECT)
	_art.offset_left = 40
	_art.offset_top = 40
	_art.offset_right = -40
	_art.offset_bottom = -200
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	add_child(_art)

	# 胸口光錨點：偏角色胸口可讀位置
	_chest_anchor = Control.new()
	_chest_anchor.name = "ChestGlowAnchor"
	_chest_anchor.position = Vector2(640, 360)
	_chest_anchor.size = Vector2(96, 96)
	add_child(_chest_anchor)

	hud = ChestGlowHudScript.new()
	hud.name = "ChestGlowHud"
	hud.position = Vector2(-8, -8)
	hud.size = Vector2(96, 96)
	hud.custom_minimum_size = Vector2(96, 96)
	_chest_anchor.add_child(hud)

	_cost_lbl = Label.new()
	_cost_lbl.position = Vector2(700, 340)
	_cost_lbl.add_theme_font_size_override("font_size", 15)
	_cost_lbl.add_theme_color_override("font_color", Color(0.85, 0.78, 0.45))
	_cost_lbl.text = ""
	add_child(_cost_lbl)

	_drop_preview = TextureRect.new()
	_drop_preview.position = Vector2(980, 120)
	_drop_preview.size = Vector2(160, 160)
	_drop_preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_drop_preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_drop_preview.visible = false
	_drop_preview.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_drop_preview)

	_phase_lbl = Label.new()
	_phase_lbl.position = Vector2(48, 16)
	_phase_lbl.add_theme_font_size_override("font_size", 18)
	_phase_lbl.add_theme_color_override("font_color", Color(0.85, 0.82, 0.70))
	add_child(_phase_lbl)

	_dialog = Label.new()
	_dialog.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dialog.offset_top = -190
	_dialog.offset_left = 48
	_dialog.offset_right = -48
	_dialog.offset_bottom = -118
	_dialog.add_theme_font_size_override("font_size", 22)
	_dialog.add_theme_color_override("font_color", Color(0.95, 0.93, 0.88))
	_dialog.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_dialog)

	_hint = Label.new()
	_hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_hint.offset_top = -52
	_hint.offset_left = 48
	_hint.offset_right = -48
	_hint.offset_bottom = -20
	_hint.text = "空白鍵／點擊＝下一步 · 底列三相鈕 · H＝自動跑完 · Esc＝結束"
	_hint.add_theme_font_size_override("font_size", 14)
	_hint.add_theme_color_override("font_color", Color(0.65, 0.62, 0.55))
	add_child(_hint)

	_log = RichTextLabel.new()
	_log.position = Vector2(48, 48)
	_log.size = Vector2(420, 200)
	_log.bbcode_enabled = false
	_log.fit_content = false
	_log.scroll_following = true
	_log.add_theme_font_size_override("normal_font_size", 13)
	_log.add_theme_color_override("default_color", Color(0.7, 0.75, 0.7, 0.85))
	add_child(_log)

	_build_toast()
	_build_phase_buttons()


func _build_phase_buttons() -> void:
	## 拇指友善三相鈕：探索 / 戰鬥 / 拆解（可發現、清楚標籤）
	var row := HBoxContainer.new()
	row.name = "PhaseButtons"
	row.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	row.offset_top = -110
	row.offset_bottom = -56
	row.offset_left = 48
	row.offset_right = -48
	row.add_theme_constant_override("separation", 16)
	add_child(row)

	_btn_explore = _make_phase_btn("探索", "explore")
	_btn_combat = _make_phase_btn("戰鬥", "combat")
	_btn_dismantle = _make_phase_btn("拆解", "dismantle")
	row.add_child(_btn_explore)
	row.add_child(_btn_combat)
	row.add_child(_btn_dismantle)


func _make_phase_btn(label: String, group: String) -> Button:
	var b := Button.new()
	b.text = label
	b.custom_minimum_size = Vector2(160, 52)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.add_theme_font_size_override("font_size", 22)
	# 奶油果凍感底（非黑曜石 HUD）
	var n := StyleBoxFlat.new()
	n.bg_color = Color(0.96, 0.90, 0.78, 0.95)
	n.corner_radius_top_left = 16
	n.corner_radius_top_right = 16
	n.corner_radius_bottom_left = 16
	n.corner_radius_bottom_right = 16
	n.content_margin_left = 12
	n.content_margin_right = 12
	n.content_margin_top = 8
	n.content_margin_bottom = 8
	n.border_width_bottom = 4
	n.border_color = Color(0.78, 0.62, 0.35, 1.0)
	b.add_theme_stylebox_override("normal", n)
	var h := n.duplicate() as StyleBoxFlat
	h.bg_color = Color(1.0, 0.95, 0.85, 1.0)
	b.add_theme_stylebox_override("hover", h)
	var p := n.duplicate() as StyleBoxFlat
	p.bg_color = Color(0.90, 0.82, 0.65, 1.0)
	b.add_theme_stylebox_override("pressed", p)
	b.add_theme_color_override("font_color", Color(0.25, 0.18, 0.12))
	b.pressed.connect(func() -> void:
		_on_phase_btn(group)
	)
	return b



func _build_toast() -> void:
	## W5-K1 ERR_* 短橫幅（與對白 Label 分離）
	var host := CenterContainer.new()
	host.name = "ErrToastHost"
	host.set_anchors_preset(Control.PRESET_TOP_WIDE)
	host.offset_top = 8
	host.offset_bottom = 48
	host.mouse_filter = Control.MOUSE_FILTER_IGNORE
	host.z_index = 100
	add_child(host)
	_toast = Label.new()
	_toast.name = "ErrToast"
	_toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_toast.add_theme_font_size_override("font_size", 18)
	_toast.add_theme_color_override("font_color", Color(0.20, 0.12, 0.08))
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(1.0, 0.92, 0.72, 0.96)
	sb.corner_radius_top_left = 12
	sb.corner_radius_top_right = 12
	sb.corner_radius_bottom_left = 12
	sb.corner_radius_bottom_right = 12
	sb.content_margin_left = 18
	sb.content_margin_right = 18
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	sb.border_width_bottom = 3
	sb.border_color = Color(0.85, 0.55, 0.25, 1.0)
	_toast.add_theme_stylebox_override("normal", sb)
	_toast.visible = false
	_toast.mouse_filter = Control.MOUSE_FILTER_IGNORE
	host.add_child(_toast)


func _process(_delta: float) -> void:
	if _done or flow == null:
		return
	flow.poll_first_break_deadline()


func _on_err_toast(code: String, message: String) -> void:
	_show_err_toast(message if message != "" else code)


func _show_err_toast(msg: String) -> void:
	if _toast == null or msg == "":
		return
	_toast.text = msg
	_toast.visible = true
	_toast.modulate.a = 1.0
	var tw := create_tween()
	tw.tween_interval(1.6)
	tw.tween_property(_toast, "modulate:a", 0.0, 0.35)
	tw.tween_callback(func() -> void:
		if _toast:
			_toast.visible = false
			_toast.modulate.a = 1.0
	)


func _on_first_break_deadline() -> void:
	_deadline_highlight = true
	if flow != null:
		flow.nudge_dismantle_ready()
	_start_dismantle_pulse()
	_refresh_phase_buttons()
	_on_log("UI: 拆解鈕 pulse（首拆逾時）")


func _start_dismantle_pulse() -> void:
	if _btn_dismantle == null:
		return
	if _dismantle_pulse != null and _dismantle_pulse.is_valid():
		_dismantle_pulse.kill()
	_btn_dismantle.pivot_offset = _btn_dismantle.size * 0.5
	_dismantle_pulse = create_tween()
	_dismantle_pulse.set_loops()
	_dismantle_pulse.tween_property(_btn_dismantle, "modulate", Color(1.35, 1.15, 0.55, 1.0), 0.45)
	_dismantle_pulse.tween_property(_btn_dismantle, "modulate", Color(1.0, 0.95, 0.75, 1.0), 0.45)


func _stop_dismantle_pulse() -> void:
	if _dismantle_pulse != null and _dismantle_pulse.is_valid():
		_dismantle_pulse.kill()
	_dismantle_pulse = null


func _on_phase_btn(group: String) -> void:
	if _done or flow == null:
		return
	# 拆解前若部位未解鎖：toast ERR_PART_LOCKED（不 softlock）
	if group == "dismantle" and flow.phase < S8SmokeFlow.Phase.B03_PART_UNLOCK and not flow.part_unlocked:
		# 仍允許 goto_group 推進；若尚在探索僅 toast 提示
		if flow.phase < S8SmokeFlow.Phase.B01_START:
			_show_err_toast(flow.wind.err_toast("ERR_PART_LOCKED"))
	flow.goto_group(group)
	if group == "dismantle" or flow.phase_group() == "dismantle":
		_deadline_highlight = false
		_stop_dismantle_pulse()
	if flow.first_break_done:
		_deadline_highlight = false
		_stop_dismantle_pulse()
	_refresh_art()
	_refresh_phase_buttons()


func _refresh_phase_buttons() -> void:
	if flow == null:
		return
	var g := flow.phase_group()
	_style_active(_btn_explore, g == "explore")
	_style_active(_btn_combat, g == "combat")
	var dismantle_on := g == "dismantle" or _deadline_highlight
	_style_active(_btn_dismantle, dismantle_on)
	if _deadline_highlight and g != "dismantle":
		if _dismantle_pulse == null or not _dismantle_pulse.is_valid():
			_start_dismantle_pulse()


func _style_active(b: Button, on: bool) -> void:
	if b == null:
		return
	# 逾時 pulse 中的拆解鈕：不要每幀蓋掉 modulate
	var pulsing := b == _btn_dismantle and _deadline_highlight and (_dismantle_pulse != null and _dismantle_pulse.is_valid())
	if not pulsing:
		b.modulate = Color(1.15, 1.05, 0.85, 1.0) if on else Color(0.85, 0.85, 0.85, 0.9)
	# 啟用組加角標感
	var base := b.text.replace(" · 進行中", "").replace(" · 來拆！", "")
	if b == _btn_dismantle and _deadline_highlight and not (flow != null and flow.phase_group() == "dismantle"):
		b.text = "%s · 來拆！" % base
	elif on:
		b.text = "%s · 進行中" % base
	else:
		b.text = base


func _unhandled_input(event: InputEvent) -> void:
	if _done:
		if event.is_action_pressed("ui_cancel"):
			get_tree().quit()
		return
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		# 點在按鈕上時不要雙觸發
		if event is InputEventMouseButton:
			var hover := get_viewport().gui_get_hovered_control()
			if hover is Button:
				return
		_step()
		get_viewport().set_input_as_handled()
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_H:
			_auto_finish()
			get_viewport().set_input_as_handled()
		elif event.keycode == KEY_ESCAPE:
			get_tree().quit()


func _step() -> void:
	if flow == null or _done:
		return
	# B02：一次打到 unlock（避免連點數十下）；之後走一般 advance。
	if flow.phase == S8SmokeFlow.Phase.B02_COMBAT:
		flow._run_combat_loop()
		_refresh_art()
		_refresh_phase_buttons()
		return
	flow.advance()
	_refresh_art()
	_refresh_phase_buttons()


func _auto_finish() -> void:
	var result: Dictionary = S8SmokeFlowScript.new().run_to_completion()
	_on_log(str(result.get("summary", "")))
	_dialog.text = "自動跑完：%s" % str(result.get("summary", ""))
	_done = bool(result.get("ok", false))
	_phase_lbl.text = "DONE" if _done else "FAIL"
	if _done:
		_on_log("S8_SMOKE_SUCCESS")


func _on_phase(phase: String, line: String) -> void:
	_phase_lbl.text = "§8 · %s · 發條 %d/%d" % [phase, flow.wind.current, flow.wind.max_stamina]
	_dialog.text = line
	_refresh_art()
	_refresh_phase_buttons()
	_update_cost_caption()


func _on_stamina_spent(action_id: String, amount: int, remaining: int) -> void:
	if amount <= 0:
		return
	_cost_lbl.text = "發條 −%d · %s → %d/%d" % [
		amount, action_id, remaining, flow.wind.max_stamina
	]
	# HUD 自身已聽 spent；再保險 pulse 一次
	if hud != null:
		hud.pulse_drain(amount)


func _update_cost_caption() -> void:
	if flow == null or flow.wind == null:
		return
	var g := flow.phase_group()
	var tip := ""
	match g:
		"explore":
			tip = "探索節奏 · E02_exploreTick=%d" % flow.wind.cost_of("E02_exploreTick")
		"combat":
			tip = "戰鬥 · 進場=%d／打擊=%d" % [
				flow.wind.cost_of("B01_combatEnter"), flow.wind.cost_of("B_strike")
			]
		"dismantle":
			tip = "拆解 · 進場=%d／抽零件=%d" % [
				flow.wind.cost_of("D01_dismantleEnter"), flow.wind.cost_of("D_pullPart")
			]
	if _cost_lbl.text.is_empty() or not _cost_lbl.text.begins_with("發條 −"):
		_cost_lbl.text = tip


func _on_part_break_fx(drop_id: String, _part_name: String) -> void:
	_deadline_highlight = false
	_stop_dismantle_pulse()
	var origin := Vector2(720, 400)
	if _chest_anchor != null:
		origin = _chest_anchor.global_position + Vector2(200, 40)
	CandyChipVfxScript.play(self, origin, drop_id)
	_show_drop_icon(drop_id)


func _show_drop_icon(drop_id: String) -> void:
	var path := str(CandyChipVfxScript.DROP_ICON_PATHS.get(drop_id, ""))
	if path.is_empty() or not ResourceLoader.exists(path):
		_drop_preview.visible = false
		_drop_preview.texture = null
		return
	var tex: Texture2D = load(path) as Texture2D
	if tex == null:
		_drop_preview.visible = false
		return
	_drop_preview.texture = tex
	_drop_preview.visible = true
	_drop_preview.modulate = Color(1, 1, 1, 1)
	var tw := create_tween()
	_drop_preview.scale = Vector2(0.7, 0.7)
	_drop_preview.pivot_offset = _drop_preview.size * 0.5
	tw.tween_property(_drop_preview, "scale", Vector2(1.0, 1.0), 0.2)


func _on_log(text: String) -> void:
	_log.append_text(text + "\n")


func _on_finished(ok: bool, summary: String) -> void:
	_done = true
	_on_log(summary)
	if ok:
		_on_log("S8_SMOKE_SUCCESS")
		_dialog.text = "%s\n（煙測完成 — 發條還沒停。）" % summary
	else:
		_on_log("S8_SMOKE_FAIL")
		_dialog.text = summary
	_refresh_phase_buttons()


func _refresh_art() -> void:
	if flow == null:
		return
	var path := TEX_EXPLORE
	var p := flow.phase
	if p >= S8SmokeFlow.Phase.B01_START and p <= S8SmokeFlow.Phase.B07_END:
		# Pack-A 單手劍 cel 優先；缺則回退 placeholder
		path = TEX_CEL_B02 if ResourceLoader.exists(TEX_CEL_B02) else TEX_COMBAT
	elif p >= S8SmokeFlow.Phase.D01_START:
		path = TEX_DISMANTLE
	if ResourceLoader.exists(path):
		_art.texture = load(path) as Texture2D
	# 胸口錨點：戰鬥時略偏右下（角色胸口感）
	if _chest_anchor != null:
		if p >= S8SmokeFlow.Phase.B01_START and p <= S8SmokeFlow.Phase.B07_END:
			_chest_anchor.position = Vector2(580, 340)
		elif p >= S8SmokeFlow.Phase.D01_START:
			_chest_anchor.position = Vector2(560, 360)
		else:
			_chest_anchor.position = Vector2(640, 380)
