class_name ResponsiveUi
extends RefCounted
## Safe Area ＋ Anchors ＋ 可縮放 UI。
## 1280×720 只是視窗後備值，不是版面基準（Product Lock §5.1 第 3 項）。

const DIALOG_W_MIN := 740.0
const DIALOG_W_MAX := 760.0
const BTN_H := 50.0
const CLOSE_SIZE := 50.0
const PAD := 12.0
## 字級相對這個高度微縮，不當版面寬高。
const REF_H := 720.0


static func viewport_size(n: Node) -> Vector2:
	if n != null and n.is_inside_tree() and n.get_viewport():
		var s := n.get_viewport().get_visible_rect().size
		if s.x >= 8.0 and s.y >= 8.0:
			return s
	return Vector2(1280, 720)


static func safe_margin(n: Node) -> Vector4:
	## x=left y=top z=right w=bottom，viewport 像素。
	var fallback := Vector4(PAD, PAD, PAD, PAD)
	var vp := viewport_size(n)
	if n == null or not n.is_inside_tree():
		return fallback
	var win := n.get_window()
	if win == null:
		return fallback
	var safe := DisplayServer.get_display_safe_area()
	if safe.size.x <= 1 or safe.size.y <= 1:
		return fallback
	var win_rect := Rect2(Vector2(win.position), Vector2(win.size))
	if win_rect.size.x <= 1.0 or win_rect.size.y <= 1.0:
		return fallback
	var inter := Rect2(safe).intersection(win_rect)
	if inter.size.x <= 1.0 or inter.size.y <= 1.0:
		return fallback
	var sx := vp.x / win_rect.size.x
	var sy := vp.y / win_rect.size.y
	var left := maxf(PAD, (inter.position.x - win_rect.position.x) * sx)
	var top := maxf(PAD, (inter.position.y - win_rect.position.y) * sy)
	var right := maxf(PAD, (win_rect.end.x - inter.end.x) * sx)
	var bottom := maxf(PAD, (win_rect.end.y - inter.end.y) * sy)
	return Vector4(left, top, right, bottom)


static func apply_safe_margins(ctrl: Control, extra: Vector4 = Vector4.ZERO) -> void:
	if ctrl == null:
		return
	ctrl.set_anchors_preset(Control.PRESET_FULL_RECT)
	var m := safe_margin(ctrl)
	ctrl.offset_left = m.x + extra.x
	ctrl.offset_top = m.y + extra.y
	ctrl.offset_right = -(m.z + extra.z)
	ctrl.offset_bottom = -(m.w + extra.w)


static func dialog_width(n: Node) -> float:
	var vp := viewport_size(n)
	var m := safe_margin(n)
	var avail := vp.x - m.x - m.z
	if avail >= DIALOG_W_MAX:
		return DIALOG_W_MAX
	if avail >= DIALOG_W_MIN:
		return clampf(avail, DIALOG_W_MIN, DIALOG_W_MAX)
	## 極窄仍不縮成 420 欄；橫屏手機／平板都不該走到這。
	return maxf(avail, DIALOG_W_MIN)


static func apply_dialog_card(card: Control) -> void:
	if card == null:
		return
	var w := dialog_width(card)
	card.custom_minimum_size.x = w


static func apply_core_button(btn: Button) -> void:
	if btn == null:
		return
	if btn.custom_minimum_size.y < BTN_H:
		btn.custom_minimum_size.y = BTN_H


static func ui_scale(n: Node) -> float:
	return clampf(viewport_size(n).y / REF_H, 0.85, 1.35)


static func make_close_button(cb: Callable) -> Button:
	var btn := Button.new()
	btn.name = "CloseBtn"
	btn.text = "關閉"
	btn.custom_minimum_size = Vector2(CLOSE_SIZE, CLOSE_SIZE)
	btn.add_theme_font_size_override("font_size", 15)
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.22, 0.16, 0.12, 0.95)
	csb.border_color = Color(0.85, 0.70, 0.35, 0.9)
	csb.set_border_width_all(2)
	csb.set_corner_radius_all(18)
	btn.add_theme_stylebox_override("normal", csb)
	btn.add_theme_stylebox_override("hover", csb)
	btn.add_theme_stylebox_override("pressed", csb)
	btn.add_theme_color_override("font_color", Color(1.0, 0.90, 0.80))
	if cb.is_valid():
		btn.pressed.connect(cb)
	return btn
