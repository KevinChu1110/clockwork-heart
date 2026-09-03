class_name UiStyle
extends RefCounted
## 據點 UI：深木底、銅金邊、淺字。對齊原作村莊／楓式面板，不用網頁粉紅。

## ── 塔塔冒險隊風格多巴胺鮮亮色盤 (Tata Dopamine Vibrant Palette) ──
const TATA_YELLOW := Color(1.0, 0.82, 0.18, 1.0)       ## 陽光金黃
const TATA_ORANGE := Color(1.0, 0.56, 0.14, 1.0)       ## 活力暖橘
const TATA_GREEN := Color(0.28, 0.85, 0.42, 1.0)        ## 清新薄荷綠
const TATA_BLUE := Color(0.22, 0.68, 1.0, 1.0)          ## 晴空蔚藍
const TATA_PINK := Color(1.0, 0.38, 0.58, 1.0)          ## 珊瑚活力粉
const TATA_NAVY := Color(0.12, 0.10, 0.24, 1.0)         ## 現代深藍紫描邊 (告別髒黑)
const TATA_CARD_BG := Color(0.14, 0.12, 0.26, 0.95)     ## 高級星空藍紫卡片底
const TATA_CREAM := Color(0.98, 0.98, 0.95, 1.0)        ## 奶油米白

const KEY := TATA_YELLOW
const KEY_STRONG := TATA_ORANGE
const KEY_DEEP := Color(0.85, 0.42, 0.08, 1.0)
const KEY_SOFT := Color(1.0, 0.94, 0.70, 1.0)
const KEY_FAINT := Color(1.0, 0.98, 0.88, 1.0)

## ── Surface / Wood dark (全面升級為通透藍紫) ──
const WOOD_DARKEST := TATA_NAVY
const WOOD_DARK := Color(0.16, 0.14, 0.30, 1.0)
const WOOD_MID := Color(0.22, 0.18, 0.38, 1.0)
const WOOD := WOOD_DARK
const WOOD_LIGHT := Color(0.55, 0.52, 0.75, 1.0)

## ── Paper / Ink ──
const PAPER := TATA_CREAM
const PAPER_SOFT := Color(1.0, 1.0, 1.0, 0.98)
const CREAM := TATA_NAVY
const CREAM_DIM := Color(0.45, 0.42, 0.60, 1.0)
const INK := TATA_NAVY
const INK_DIM := Color(0.45, 0.42, 0.60, 1.0)
const INK_FAINT := Color(0.68, 0.65, 0.80, 1.0)

## 深色插畫描邊
const BORDER_DARK := TATA_NAVY
const BORDER_MID := Color(0.45, 0.40, 0.68, 0.9)
const LINE := TATA_YELLOW
const LINE_SOFT := BORDER_MID

const GOLD := KEY_STRONG
const COPPER := KEY
const COPPER_DIM := KEY_STRONG
const MIST := Color(0.45, 0.48, 0.62, 1.0)
const DANGER := KEY_DEEP
const GOOD := Color(0.243, 0.608, 0.420, 1.0)  ## #3e9b6b

## 深木底 HUD 上的字（狀態板／快捷欄／名牌共用，不要各檔自己寫數字）
const HUD_TEXT := Color(0.96, 0.94, 0.90, 1.0)
const HUD_TEXT_DIM := Color(0.70, 0.66, 0.60, 1.0)
const HUD_GOLD := Color(0.90, 0.85, 0.75, 1.0)
const HUD_LV := Color(0.95, 0.72, 0.45, 1.0)
const HUD_KEYCAP := Color(0.95, 0.75, 0.45, 1.0)
## 探索：任務「！」與點地光圈
const QUEST_PING := Color(1.0, 0.86, 0.32, 1.0)
const QUEST_PING_OUTLINE := Color(0.12, 0.08, 0.05, 1.0)
const TAP_RING := Color(1.0, 0.86, 0.55, 0.95)

## 血／藍／經驗
const HP_FILL := Color(0.86, 0.28, 0.32, 1.0)
const HP_BG := Color(0.22, 0.12, 0.14, 0.95)
const MP_FILL := Color(0.55, 0.42, 0.82, 1.0)  ## 星屑偏紫
const MP_BG := Color(0.14, 0.12, 0.22, 0.95)
const EXP_FILL := Color(0.78, 0.62, 0.28, 1.0)
const EXP_BG := Color(0.18, 0.14, 0.10, 0.95)
const RAGE_FILL := Color(0.95, 0.55, 0.25, 1.0)


static func panel_style(accent: Color = LINE) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = TATA_CARD_BG
	s.border_color = accent if accent != LINE else TATA_YELLOW
	s.set_border_width_all(3)
	s.border_width_bottom = 6
	s.set_corner_radius_all(22)
	s.content_margin_left = 22
	s.content_margin_right = 22
	s.content_margin_top = 18
	s.content_margin_bottom = 20
	s.shadow_color = Color(0.08, 0.05, 0.18, 0.6)
	s.shadow_size = 14
	s.shadow_offset = Vector2(0, 6)
	return s


static func panel_style_dark() -> StyleBoxFlat:
	## HUD / 面板：深色暖木／金邊質感框
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.13, 0.12, 0.15, 0.92)
	s.border_color = Color(0.75, 0.60, 0.45, 0.85)
	s.set_border_width_all(1)
	s.set_corner_radius_all(8)
	s.content_margin_left = 10
	s.content_margin_right = 10
	s.content_margin_top = 8
	s.content_margin_bottom = 8
	s.shadow_color = Color(0.05, 0.04, 0.06, 0.35)
	s.shadow_size = 8
	s.shadow_offset = Vector2(0, 3)
	return s


static func header_style() -> StyleBoxFlat:
	## 標題列（暗木銅邊）
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.16, 0.13, 0.10, 0.96)
	s.border_color = Color(0.78, 0.58, 0.32, 0.9)
	s.set_border_width_all(0)
	s.border_width_bottom = 1
	s.set_corner_radius_all(0)
	s.corner_radius_top_left = 8
	s.corner_radius_top_right = 8
	s.content_margin_left = 10
	s.content_margin_right = 8
	s.content_margin_top = 6
	s.content_margin_bottom = 6
	return s


static func interact_badge_style() -> StyleBoxFlat:
	## 靠近互動物件時的「E」框
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.20, 0.16, 0.14, 0.96)
	s.border_color = Color(0.92, 0.75, 0.45, 1.0)
	s.set_border_width_all(2)
	s.set_corner_radius_all(8)
	s.content_margin_left = 8
	s.content_margin_right = 8
	s.content_margin_top = 4
	s.content_margin_bottom = 4
	s.shadow_color = Color(0.05, 0.04, 0.06, 0.4)
	s.shadow_size = 6
	s.shadow_offset = Vector2(0, 2)
	return s


static func interact_name_style() -> StyleBoxFlat:
	## 靠近時才顯示的名稱小牌
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.14, 0.13, 0.16, 0.92)
	s.border_color = Color(0.75, 0.60, 0.45, 0.7)
	s.set_border_width_all(1)
	s.set_corner_radius_all(6)
	s.content_margin_left = 8
	s.content_margin_right = 8
	s.content_margin_top = 3
	s.content_margin_bottom = 3
	s.shadow_color = Color(0.05, 0.04, 0.06, 0.3)
	s.shadow_size = 4
	return s


static func hint_bar_style() -> StyleBoxFlat:
	## 底部操作提示框
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.12, 0.11, 0.14, 0.92)
	s.border_color = Color(0.75, 0.60, 0.45, 0.75)
	s.set_border_width_all(1)
	s.set_corner_radius_all(10)
	s.content_margin_left = 14
	s.content_margin_right = 14
	s.content_margin_top = 8
	s.content_margin_bottom = 8
	s.shadow_color = Color(0.05, 0.04, 0.06, 0.35)
	s.shadow_size = 6
	return s


## 深色底上的台詞字（CREAM 已被當成 ink 用在淺底標題，不能拿來寫旁白）
const CAPTION := Color(0.96, 0.93, 0.88, 1.0)
const CAPTION_DIM := Color(0.72, 0.68, 0.62, 1.0)


static func dialogue_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.10, 0.09, 0.12, 1.0)
	s.border_color = Color(0.85, 0.68, 0.48, 0.95)
	s.set_border_width_all(2)
	s.set_corner_radius_all(6)
	s.content_margin_left = 16
	s.content_margin_right = 16
	s.content_margin_top = 12
	s.content_margin_bottom = 10
	s.shadow_color = Color(0.04, 0.03, 0.05, 0.55)
	s.shadow_size = 14
	return s


static func chip_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.99, 0.98, 0.95, 0.96)
	s.border_color = BORDER_DARK
	s.set_border_width_all(2)
	s.set_corner_radius_all(6)
	s.content_margin_left = 8
	s.content_margin_right = 8
	s.content_margin_top = 3
	s.content_margin_bottom = 3
	s.shadow_color = Color(0.12, 0.08, 0.04, 0.15)
	s.shadow_size = 4
	s.shadow_offset = Vector2(0, 1)
	return s


static func button_normal() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.22, 0.18, 0.38, 0.94)
	s.border_color = Color(0.50, 0.44, 0.72, 0.9)
	s.set_border_width_all(2)
	s.border_width_bottom = 5
	s.set_corner_radius_all(18)
	s.content_margin_left = 18
	s.content_margin_right = 18
	s.content_margin_top = 10
	s.content_margin_bottom = 12
	s.shadow_color = Color(0.08, 0.05, 0.16, 0.4)
	s.shadow_size = 5
	s.shadow_offset = Vector2(0, 3)
	return s


static func button_hover() -> StyleBoxFlat:
	var s := button_normal()
	s.bg_color = Color(0.28, 0.24, 0.48, 0.98)
	s.border_color = TATA_YELLOW
	return s


static func button_pressed() -> StyleBoxFlat:
	var s := button_normal()
	s.bg_color = Color(0.18, 0.14, 0.32, 1.0)
	s.border_width_bottom = 2
	s.content_margin_top = 13
	s.content_margin_bottom = 9
	return s


static func button_disabled() -> StyleBoxFlat:
	var s := button_normal()
	s.bg_color = Color(0.18, 0.16, 0.28, 0.6)
	s.border_color = Color(0.35, 0.32, 0.48, 0.4)
	s.border_width_bottom = 2
	return s


static func button_primary() -> StyleBoxFlat:
	## 塔塔風超大果凍金黃按鈕 (Jelly Gold Button)
	var s := StyleBoxFlat.new()
	s.bg_color = TATA_YELLOW
	s.border_color = Color(1.0, 0.96, 0.75, 1.0)
	s.set_border_width_all(2)
	s.border_width_bottom = 6
	s.set_corner_radius_all(20)
	s.content_margin_left = 22
	s.content_margin_right = 22
	s.content_margin_top = 11
	s.content_margin_bottom = 14
	s.shadow_color = Color(1.0, 0.65, 0.10, 0.55)
	s.shadow_size = 8
	s.shadow_offset = Vector2(0, 4)
	return s


static func button_primary_hover() -> StyleBoxFlat:
	var s := button_primary()
	s.bg_color = Color(1.0, 0.88, 0.28, 1.0)
	return s


static func style_button(btn: Button, primary: bool = false) -> void:
	if primary:
		btn.add_theme_stylebox_override("normal", button_primary())
		btn.add_theme_stylebox_override("hover", button_primary_hover())
		btn.add_theme_stylebox_override("pressed", button_primary())
		btn.add_theme_stylebox_override("focus", button_primary_hover())
		btn.add_theme_stylebox_override("disabled", button_disabled())
		btn.add_theme_color_override("font_color", Color(0.20, 0.10, 0.02, 1.0))
		btn.add_theme_color_override("font_hover_color", Color(0.12, 0.05, 0.01, 1.0))
		btn.add_theme_color_override("font_pressed_color", Color(0.20, 0.10, 0.02, 0.9))
		btn.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.9))
		btn.add_theme_constant_override("outline_size", 2)
	else:
		btn.add_theme_stylebox_override("normal", button_normal())
		btn.add_theme_stylebox_override("hover", button_hover())
		btn.add_theme_stylebox_override("pressed", button_pressed())
		btn.add_theme_stylebox_override("focus", button_hover())
		btn.add_theme_stylebox_override("disabled", button_disabled())
		btn.add_theme_color_override("font_color", Color.WHITE)
		btn.add_theme_color_override("font_hover_color", TATA_YELLOW)
		btn.add_theme_color_override("font_pressed_color", Color(0.9, 0.85, 0.80, 1.0))
		btn.add_theme_color_override("font_outline_color", TATA_NAVY)
		btn.add_theme_constant_override("outline_size", 3)
	btn.add_theme_color_override("font_disabled_color", Color(0.6, 0.55, 0.7, 0.7))
	btn.add_theme_font_size_override("font_size", 17)
	btn.custom_minimum_size = Vector2(0, 48)


static func attach_red_dot(parent: Control, offset: Vector2 = Vector2(-4, -4)) -> Panel:
	var dot := Panel.new()
	dot.custom_minimum_size = Vector2(10, 10)
	dot.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	dot.offset_left = offset.x - 10
	dot.offset_top = offset.y
	dot.offset_right = offset.x
	dot.offset_bottom = offset.y + 10
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = Color(0.95, 0.25, 0.25, 1.0)
	dsb.border_color = Color(1.0, 0.9, 0.9, 1.0)
	dsb.set_border_width_all(1)
	dsb.set_corner_radius_all(5)
	dsb.shadow_color = Color(0.95, 0.25, 0.25, 0.5)
	dsb.shadow_size = 3
	dot.add_theme_stylebox_override("panel", dsb)
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(dot)
	return dot


static func style_progress(bar: ProgressBar, fill: Color, bg: Color) -> void:
	var bg_s := StyleBoxFlat.new()
	bg_s.bg_color = bg
	bg_s.set_border_width_all(1)
	bg_s.border_color = LINE
	bg_s.set_corner_radius_all(4)
	var fill_s := StyleBoxFlat.new()
	fill_s.bg_color = fill
	fill_s.set_corner_radius_all(3)
	bar.add_theme_stylebox_override("background", bg_s)
	bar.add_theme_stylebox_override("fill", fill_s)
	bar.show_percentage = false


static func dim_rect(parent: Control, alpha: float = 0.45) -> ColorRect:
	var d := ColorRect.new()
	d.set_anchors_preset(Control.PRESET_FULL_RECT)
	d.color = Color(0.08, 0.07, 0.10, alpha)
	d.mouse_filter = Control.MOUSE_FILTER_STOP
	parent.add_child(d)
	return d


static func name_tag_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.99, 0.98, 0.95, 0.96)
	s.border_color = BORDER_DARK
	s.set_border_width_all(2)
	s.set_corner_radius_all(5)
	s.content_margin_left = 6
	s.content_margin_right = 6
	s.content_margin_top = 1
	s.content_margin_bottom = 1
	s.shadow_color = Color(0.12, 0.08, 0.04, 0.15)
	s.shadow_size = 3
	return s


static func slot_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.98, 0.96, 0.93, 1.0)
	s.border_color = BORDER_DARK
	s.set_border_width_all(2)
	s.set_corner_radius_all(6)
	return s


## 快捷欄：深木格。空格淡邊、有東西銅邊；「選單」鈕用同一套，不再是白底淡字。
static func slot_empty_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.18, 0.16, 0.20, 0.9)
	s.border_color = Color(0.40, 0.35, 0.30, 0.7)
	s.set_border_width_all(1)
	s.set_corner_radius_all(4)
	return s


static func slot_filled_style() -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.25, 0.20, 0.28, 0.95)
	s.border_color = Color(0.85, 0.65, 0.40, 0.9)
	s.set_border_width_all(2)
	s.set_corner_radius_all(4)
	return s


static func slot_menu_style() -> StyleBoxFlat:
	var s := slot_filled_style()
	s.bg_color = Color(0.16, 0.13, 0.10, 0.96)
	s.border_color = Color(0.78, 0.58, 0.32, 0.9)
	s.set_border_width_all(1)
	return s


## 底部短訊（存檔了、用了藥）：跟提示框同一張皮，任何底圖上都讀得到。
static func toast_style() -> StyleBoxFlat:
	var s := hint_bar_style()
	s.content_margin_top = 6
	s.content_margin_bottom = 6
	return s


static func add_button_juice(btn: Button) -> void:
	if btn == null or not is_instance_valid(btn):
		return
	btn.pivot_offset = btn.size * 0.5
	btn.mouse_entered.connect(func():
		if btn and is_instance_valid(btn):
			btn.pivot_offset = btn.size * 0.5
			var tw := btn.create_tween()
			tw.tween_property(btn, "scale", Vector2(1.05, 1.05), 0.1).set_trans(Tween.TRANS_SINE)
	)
	btn.mouse_exited.connect(func():
		if btn and is_instance_valid(btn):
			var tw := btn.create_tween()
			tw.tween_property(btn, "scale", Vector2.ONE, 0.1)
	)
	btn.button_down.connect(func():
		if btn and is_instance_valid(btn):
			btn.pivot_offset = btn.size * 0.5
			var tw := btn.create_tween()
			tw.tween_property(btn, "scale", Vector2(0.95, 0.95), 0.05)
	)
	btn.button_up.connect(func():
		if btn and is_instance_valid(btn):
			var tw := btn.create_tween()
			tw.tween_property(btn, "scale", Vector2(1.05, 1.05), 0.05)
	)
