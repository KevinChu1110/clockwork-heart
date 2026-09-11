class_name ChestGlowHud
extends Control
## Ken W2-K1 HUD：胸口光環 + 外圈刻度（非藍 mana 條、非第二資源條）。
## 掛在玩家胸口錨點；由 WindStamina.changed 驅動重繪。

var wind: WindStamina = null
var _pulse: float = 0.0


func setup(stamina: WindStamina) -> void:
	wind = stamina
	if wind != null and not wind.changed.is_connected(_on_changed):
		wind.changed.connect(_on_changed)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	custom_minimum_size = Vector2(80, 80)
	queue_redraw()


func _on_changed(_c: int, _m: int) -> void:
	queue_redraw()


func _process(delta: float) -> void:
	_pulse += delta * 2.4
	queue_redraw()


func _draw() -> void:
	if wind == null:
		return
	# 契約自檢：風格必須是 chest_glow_ring_ticks，絕不可畫 ProgressBar／藍條。
	if wind.hud_style() != "chest_glow_ring_ticks":
		return

	var center := size * 0.5
	var radius := float(wind.hud.get("ringRadiusPx", 28))
	var glow := _parse_color(str(wind.hud.get("glowColor", "#2EC4B6")))
	var lit := _parse_color(str(wind.hud.get("tickColorLit", "#D4A017")))
	var dim := _parse_color(str(wind.hud.get("tickColorDim", "#6B5A3E")))
	var tick_n := int(wind.hud.get("HudTickCount", wind.max_stamina))
	tick_n = maxi(1, tick_n)

	var alpha := wind.glow_alpha()
	var pulse := 0.85 + 0.15 * sin(_pulse)
	glow.a = alpha * pulse
	draw_circle(center, radius * 0.55, glow)
	# 外圈細環
	var ring := glow
	ring.a = alpha * 0.9
	draw_arc(center, radius, 0.0, TAU, 48, ring, 2.0, true)

	# 刻度：已消耗＝dim，剩餘＝lit（順時針從上方）
	var remaining := wind.current
	for i in tick_n:
		var ang := -PI * 0.5 + TAU * (float(i) / float(tick_n))
		var inner := radius - 4.0
		var outer := radius + 6.0
		var a := center + Vector2(cos(ang), sin(ang)) * inner
		var b := center + Vector2(cos(ang), sin(ang)) * outer
		var col := lit if i < remaining else dim
		col.a = 0.95
		draw_line(a, b, col, 2.5, true)


func _parse_color(hex: String) -> Color:
	var c := Color.html(hex)
	if c.a <= 0.0 and not hex.begins_with("#"):
		return Color(0.18, 0.77, 0.71, 1.0)
	return c
