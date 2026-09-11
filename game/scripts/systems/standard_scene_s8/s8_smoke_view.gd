extends Control
## §8 可玩切片 View：掛 placeholder 三態圖 + 胸口光環 HUD + 對白。
## 執行：Godot 4.7 開 scenes/s8_smoke/s8_smoke.tscn（F6）。
## 空白鍵／滑鼠＝逐步；H＝一次自動跑完。

const WindStaminaScript := preload("res://scripts/systems/wind_stamina/wind_stamina.gd")
const ChestGlowHudScript := preload("res://scripts/systems/wind_stamina/chest_glow_hud.gd")
const S8SmokeFlowScript := preload("res://scripts/systems/standard_scene_s8/s8_smoke_flow.gd")

const TEX_EXPLORE := "res://assets/sprites/s8_smoke/e03_explore.png"
const TEX_COMBAT := "res://assets/sprites/s8_smoke/b02_combat.png"
const TEX_DISMANTLE := "res://assets/sprites/s8_smoke/d02_dismantle.png"

var flow: S8SmokeFlow
var hud: ChestGlowHud
var _art: TextureRect
var _dialog: Label
var _phase_lbl: Label
var _hint: Label
var _log: RichTextLabel
var _chest_anchor: Control
var _done: bool = false


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
	flow.start()
	_refresh_art()


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
	_art.offset_bottom = -160
	_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	add_child(_art)

	_chest_anchor = Control.new()
	_chest_anchor.position = Vector2(640, 380)
	_chest_anchor.size = Vector2(80, 80)
	add_child(_chest_anchor)

	hud = ChestGlowHudScript.new()
	hud.position = Vector2(-40, -40)
	hud.size = Vector2(80, 80)
	_chest_anchor.add_child(hud)

	_phase_lbl = Label.new()
	_phase_lbl.position = Vector2(48, 16)
	_phase_lbl.add_theme_font_size_override("font_size", 18)
	_phase_lbl.add_theme_color_override("font_color", Color(0.85, 0.82, 0.70))
	add_child(_phase_lbl)

	_dialog = Label.new()
	_dialog.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dialog.offset_top = -140
	_dialog.offset_left = 48
	_dialog.offset_right = -48
	_dialog.offset_bottom = -72
	_dialog.add_theme_font_size_override("font_size", 22)
	_dialog.add_theme_color_override("font_color", Color(0.95, 0.93, 0.88))
	_dialog.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(_dialog)

	_hint = Label.new()
	_hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_hint.offset_top = -56
	_hint.offset_left = 48
	_hint.offset_right = -48
	_hint.offset_bottom = -24
	_hint.text = "空白鍵／點擊＝下一步 · H＝自動跑完 · Esc＝結束"
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


func _unhandled_input(event: InputEvent) -> void:
	if _done:
		if event.is_action_pressed("ui_cancel"):
			get_tree().quit()
		return
	if event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
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
		return
	flow.advance()
	_refresh_art()


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


func _refresh_art() -> void:
	if flow == null:
		return
	var path := TEX_EXPLORE
	var p := flow.phase
	if p >= S8SmokeFlow.Phase.B01_START and p <= S8SmokeFlow.Phase.B07_END:
		path = TEX_COMBAT
	elif p >= S8SmokeFlow.Phase.D01_START:
		path = TEX_DISMANTLE
	if ResourceLoader.exists(path):
		_art.texture = load(path) as Texture2D
