class_name DummySettlementDialog
extends Control
## 《發條之心》木人樁試招結算數據卡 (DummySettlementDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~32px 加粗帶深色厚描邊，零小字。
## 6. 零 emoji、零系統字型符號。
## 7. 「招」軸訓練回饋，不混用「器／魂」用語。

signal confirmed()

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 奶油米白底
const COLOR_CARD_WARM   := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_AMBER  := Color("#FFEED6")  ## 暖琥珀柔和卡片底
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_AMBER  := Color("#B05000")  ## 壓明度暖琥珀
const COLOR_TEXT_MUTED  := Color("#7A6E8A")  ## 輔助標籤灰紫

var _dialog_card: PanelContainer
var _damage_label: Label
var _time_label: Label
var _dps_label: Label
var _tip_label: Label
var _confirm_btn: Button
var _cached_font: Font = null

var _total_damage: int = 0
var _elapsed_time: float = 0.0
var _dps: float = 0.0
var _on_confirm: Callable = Callable()


static func show_dialog(parent: Node, stats: Dictionary = {}, on_confirm: Callable = Callable()) -> Control:
	var dlg = load("res://scripts/battle/dummy_settlement_dialog.gd").new()
	dlg.setup(stats, on_confirm)
	parent.add_child(dlg)
	return dlg


func setup(stats: Dictionary = {}, on_confirm: Callable = Callable()) -> void:
	_total_damage = int(stats.get("total_damage", 0))
	_elapsed_time = float(stats.get("elapsed_time", 0.0))
	_dps = float(stats.get("dps", 0.0))
	_on_confirm = on_confirm

	if _dialog_card == null:
		_build_ui()
	_refresh_display()


func _ready() -> void:
	name = "DummySettlementDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 95

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	if _dialog_card == null:
		_build_ui()
	_refresh_display()


func _build_ui() -> void:
	if _dialog_card != null:
		return

	if ResourceLoader.exists(FONT_PATH) and _cached_font == null:
		_cached_font = load(FONT_PATH) as Font

	# 1. 全螢幕半透明遮罩 (Scrim) - 輕透半透明遮罩，使背後戰鬥場景清晰可見
	var scrim := ResponsiveUi.make_scrim(Color(0.05, 0.04, 0.08, 0.42))
	add_child(scrim)

	# 2. 置中容器
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	# 3. 彈窗主卡片 (寬 750px，浮空微陰影)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "DummySettlementCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 420)
	_dialog_card.add_theme_stylebox_override("panel", _create_floating_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 18)
	margin.add_theme_constant_override("margin_bottom", 20)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	margin.add_child(v)

	# ── 標題列 + 關閉按鈕 ──
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_col := VBoxContainer.new()
	title_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_col.add_theme_constant_override("separation", 2)
	head.add_child(title_col)

	var title_lbl := Label.new()
	title_lbl.name = "TitleLabel"
	title_lbl.text = _t("木人試招數據卡")
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(title_lbl)

	var sub_lbl := Label.new()
	sub_lbl.name = "SubTitleLabel"
	sub_lbl.text = _t("武術館「招」軸訓練回饋 · 能量消耗 0")
	sub_lbl.add_theme_font_size_override("font_size", 13)
	sub_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	if _cached_font:
		sub_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(sub_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_confirm_clicked)
	head.add_child(close_btn)

	# ── 分隔線 ──
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# ── 三項數據核心卡片 (總傷害 / 耗時 / DPS) ──
	var stats_hbox := HBoxContainer.new()
	stats_hbox.name = "StatsHBox"
	stats_hbox.add_theme_constant_override("separation", 12)
	v.add_child(stats_hbox)

	# 卡片 1: 本次總傷害
	var res1 := _build_metric_card(
		"TotalDamageCard",
		"DamageValueLabel",
		_t("本次總傷害"),
		_t("招式命中累積"),
		COLOR_CARD_GOLD,
		COLOR_TEXT_GOLD,
		"點"
	)
	_damage_label = res1.value_label
	stats_hbox.add_child(res1.card)

	# 卡片 2: 戰鬥耗時
	var res2 := _build_metric_card(
		"ElapsedTimeCard",
		"TimeValueLabel",
		_t("試招耗時"),
		_t("戰鬥歷程秒數"),
		COLOR_CARD_WARM,
		COLOR_TEXT_ORANGE,
		"秒"
	)
	_time_label = res2.value_label
	stats_hbox.add_child(res2.card)

	# 卡片 3: 本次DPS
	var res3 := _build_metric_card(
		"DpsCard",
		"DpsValueLabel",
		_t("秒傷 (DPS)"),
		_t("每秒平均輸出"),
		COLOR_CARD_AMBER,
		COLOR_TEXT_AMBER,
		"點 / 秒"
	)
	_dps_label = res3.value_label
	stats_hbox.add_child(res3.card)

	# ── 提示說明卡片 ──
	var tip_card := PanelContainer.new()
	tip_card.name = "TipCard"
	tip_card.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 16))
	v.add_child(tip_card)

	var tip_margin := MarginContainer.new()
	tip_margin.add_theme_constant_override("margin_left", 16)
	tip_margin.add_theme_constant_override("margin_right", 16)
	tip_margin.add_theme_constant_override("margin_top", 10)
	tip_margin.add_theme_constant_override("margin_bottom", 10)
	tip_card.add_child(tip_margin)

	_tip_label = Label.new()
	_tip_label.name = "TipLabel"
	_tip_label.text = _t("木人樁為不消耗能量的自由試招訓練。可在武術館兵器架調配各色兵刃，體會不同招式的出招前搖與段數節奏。")
	_tip_label.add_theme_font_size_override("font_size", 14)
	_tip_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_tip_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if _cached_font:
		_tip_label.add_theme_font_override("font", _cached_font)
	tip_margin.add_child(_tip_label)

	# ── 底部確認按鈕 ──
	var btn_center := CenterContainer.new()
	v.add_child(btn_center)

	_confirm_btn = Button.new()
	_confirm_btn.name = "ConfirmButton"
	_confirm_btn.text = _t("完成試招")
	_confirm_btn.custom_minimum_size = Vector2(240, 52)
	_confirm_btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_confirm_btn.add_theme_font_size_override("font_size", 18)
	_confirm_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_confirm_btn.add_theme_font_override("font", _cached_font)

	var btn_normal := _create_button_style(COLOR_GOLD, COLOR_BORDER, 6, 20)
	var btn_hover := _create_button_style(Color("#FFE050"), COLOR_BORDER, 6, 20)
	var btn_pressed := _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 20)
	btn_pressed.content_margin_top = 12
	btn_pressed.content_margin_bottom = 8

	_confirm_btn.add_theme_stylebox_override("normal", btn_normal)
	_confirm_btn.add_theme_stylebox_override("hover", btn_hover)
	_confirm_btn.add_theme_stylebox_override("pressed", btn_pressed)
	_confirm_btn.add_theme_stylebox_override("focus", btn_normal)

	_confirm_btn.pressed.connect(_on_confirm_clicked)
	btn_center.add_child(_confirm_btn)


func _build_metric_card(card_name: String, val_name: String, title_text: String, sub_text: String, bg_col: Color, accent_col: Color, unit_text: String = "點") -> Dictionary:
	var card := PanelContainer.new()
	card.name = card_name
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.custom_minimum_size = Vector2(0, 130)
	card.add_theme_stylebox_override("panel", _create_inner_card_style(bg_col, COLOR_BORDER, 2, 4, 18))

	var m := MarginContainer.new()
	m.name = "Margin"
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 12)
	m.add_theme_constant_override("margin_bottom", 12)
	card.add_child(m)

	var cv := VBoxContainer.new()
	cv.name = "VBox"
	cv.add_theme_constant_override("separation", 4)
	cv.alignment = BoxContainer.ALIGNMENT_CENTER
	m.add_child(cv)

	var h_lbl := Label.new()
	h_lbl.name = "HeaderLabel"
	h_lbl.text = title_text
	h_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	h_lbl.add_theme_font_size_override("font_size", 16)
	h_lbl.add_theme_color_override("font_color", accent_col)
	if _cached_font:
		h_lbl.add_theme_font_override("font", _cached_font)
	cv.add_child(h_lbl)

	var v_row := HBoxContainer.new()
	v_row.name = "ValueRow"
	v_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v_row.add_theme_constant_override("separation", 4)
	cv.add_child(v_row)

	var val_lbl := Label.new()
	val_lbl.name = val_name
	val_lbl.text = "0"
	val_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	val_lbl.add_theme_font_size_override("font_size", 30)
	val_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	val_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	val_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		val_lbl.add_theme_font_override("font", _cached_font)
	v_row.add_child(val_lbl)

	var u_lbl := Label.new()
	u_lbl.name = "UnitLabel"
	u_lbl.text = unit_text
	u_lbl.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
	u_lbl.add_theme_font_size_override("font_size", 14)
	u_lbl.add_theme_color_override("font_color", accent_col)
	if _cached_font:
		u_lbl.add_theme_font_override("font", _cached_font)
	v_row.add_child(u_lbl)

	var sub_tag := Label.new()
	sub_tag.name = "SubTagLabel"
	sub_tag.text = sub_text
	sub_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sub_tag.add_theme_font_size_override("font_size", 12)
	sub_tag.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		sub_tag.add_theme_font_override("font", _cached_font)
	cv.add_child(sub_tag)

	return {"card": card, "value_label": val_lbl}


func _refresh_display() -> void:
	if _damage_label:
		_damage_label.text = str(_total_damage)
	if _time_label:
		_time_label.text = "%.1f" % _elapsed_time
	if _dps_label:
		_dps_label.text = "%.1f" % _dps


func _on_confirm_clicked() -> void:
	confirmed.emit()
	if _on_confirm.is_valid():
		_on_confirm.call()
	queue_free()


func get_total_damage() -> int:
	return _total_damage


func get_elapsed_time() -> float:
	return _elapsed_time


func get_dps() -> float:
	return _dps


func get_damage_text() -> String:
	return _damage_label.text if _damage_label else ""


func get_time_text() -> String:
	return _time_label.text if _time_label else ""


func get_dps_text() -> String:
	return _dps_label.text if _dps_label else ""


func _create_floating_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	return sb


func _create_inner_card_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 18) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 20, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 18
	sb.content_margin_right = 18
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8 + bottom_border
	return sb
