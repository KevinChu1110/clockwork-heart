class_name ChestGlowHud
extends Control
## Ken W2-K1 HUD：胸口光環 + 外圈刻度（非藍 mana 條、非第二資源條）。
## 掛在玩家胸口錨點；由 WindStamina.changed / spent 驅動重繪與扣點回饋。

var wind: WindStamina = null
var _pulse: float = 0.0
## 扣點閃爍：>0 時外圈／刻度短暫提亮並顯示 −N
var _drain_flash: float = 0.0
var _last_spend: int = 0
var _spend_label_alpha: float = 0.0


func setup(stamina: WindStamina) -> void:
	wind = stamina
	if wind != null:
		if not wind.changed.is_connected(_on_changed):
			wind.changed.connect(_on_changed)
		if not wind.spent.is_connected(_on_spent):
			wind.spent.connect(_on_spent)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	custom_minimum_size = Vector2(80, 80)
	queue_redraw()


func _on_changed(_c: int, _m: int) -> void:
	queue_redraw()


func _on_spent(_action_id: String, amount: int, _remaining: int) -> void:
	if amount <= 0:
		return
	_last_spend = amount
	_drain_flash = 0.55
	_spend_label_alpha = 1.0
	queue_redraw()


## 外部也可手動觸發（例如 View 在已知成本時先閃一下）。
func pulse_drain(amount: int) -> void:
	_on_spent("", amount, 0)


func _process(delta: float) -> void:
	_pulse += delta * 2.4
	if _drain_flash > 0.0:
		_drain_flash = maxf(0.0, _drain_flash - delta)
	if _spend_label_alpha > 0.0:
		_spend_label_alpha = maxf(0.0, _spend_label_alpha - delta * 1.6)
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
	# 扣點時胸口光短暫爆亮（仍非藍條）
	if _drain_flash > 0.0:
		pulse += 0.35 * (_drain_flash / 0.55)
		alpha = minf(1.0, alpha + 0.25)
	glow.a = alpha * pulse
	draw_circle(center, radius * 0.55, glow)
	# 外圈細環
	var ring := glow
	ring.a = alpha * 0.9
	var ring_w := 2.0 + (2.5 if _drain_flash > 0.0 else 0.0)
	draw_arc(center, radius, 0.0, TAU, 48, ring, ring_w, true)

	# 刻度：已消耗＝dim，剩餘＝lit（順時針從上方）
	var remaining := wind.current
	for i in tick_n:
		var ang := -PI * 0.5 + TAU * (float(i) / float(tick_n))
		var inner := radius - 4.0
		var outer := radius + 6.0
		# 剛扣掉的那幾格短暫閃紅金，讓「tick drain」可讀
		var just_drained := _drain_flash > 0.0 and i >= remaining and i < remaining + _last_spend
		if just_drained:
			outer += 3.0
		var a := center + Vector2(cos(ang), sin(ang)) * inner
		var b := center + Vector2(cos(ang), sin(ang)) * outer
		var col := lit if i < remaining else dim
		if just_drained:
			col = Color(1.0, 0.55, 0.35, 1.0)
		col.a = 0.95
		draw_line(a, b, col, 2.5 if not just_drained else 3.5, true)

	# −N 飄字（發條成本可見，用語避開「藍條／mana」）
	if _spend_label_alpha > 0.05 and _last_spend > 0:
		var font := ThemeDB.fallback_font
		var fs := 16
		var txt := "−%d" % _last_spend
		var pos := center + Vector2(-10, -radius - 18.0 * (1.0 - _spend_label_alpha))
		var c := Color(0.95, 0.85, 0.45, _spend_label_alpha)
		draw_string(font, pos, txt, HORIZONTAL_ALIGNMENT_LEFT, -1, fs, c)


func _parse_color(hex: String) -> Color:
	var c := Color.html(hex)
	if c.a <= 0.0 and not hex.begins_with("#"):
		return Color(0.18, 0.77, 0.71, 1.0)
	return c
