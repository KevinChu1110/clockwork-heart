class_name EnergyLackDialog
extends Control
## 《發條之心》體力/能量不足彈窗（含看廣告拿體力掛鉤）
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 零系統 emoji、零開發用語。
## 6. 連接 EnergySystem 看廣告回復能量邏輯。

signal energy_granted(amount: int)
signal closed()

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const MockAdDialogScript := preload("res://scripts/ui/mock_ad_dialog.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


## ── 多巴胺鮮亮色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫文字
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MINT  := Color("#1A7A30")  ## 壓明度薄荷綠
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃

var _dialog_card: PanelContainer
var _energy_val_label: Label
var _status_detail_label: Label
var _desc_lbl: Label
var _ad_btn: Button
var _cached_font: Font = null

var _on_granted: Callable = Callable()
var _on_close: Callable = Callable()


static func show_dialog(parent: Node, on_granted: Callable = Callable(), on_close: Callable = Callable()) -> Control:
	var dlg = load("res://scripts/ui/energy_lack_dialog.gd").new()
	dlg.setup(on_granted, on_close)
	parent.add_child(dlg)
	return dlg


func setup(on_granted: Callable = Callable(), on_close: Callable = Callable()) -> void:
	_on_granted = on_granted
	_on_close = on_close


func _ready() -> void:
	name = "EnergyLackDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 90

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build_ui()
	_refresh_display()


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	var scrim_btn := Button.new()
	scrim_btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_btn.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_btn.add_theme_stylebox_override("normal", esb)
	scrim_btn.add_theme_stylebox_override("hover", esb)
	scrim_btn.add_theme_stylebox_override("pressed", esb)
	scrim_btn.pressed.connect(_on_close_clicked)
	scrim.add_child(scrim_btn)

	# 2. 置中卡片 (寬 750px)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "EnergyLackCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 440)
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
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

	# 標題列 + 關閉鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.text = _t("能量不足")
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_close_clicked)
	head.add_child(close_btn)

	# 分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# 當前能量狀態卡片
	var status_card := PanelContainer.new()
	status_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	v.add_child(status_card)

	var sc_m := MarginContainer.new()
	sc_m.add_theme_constant_override("margin_left", 20)
	sc_m.add_theme_constant_override("margin_right", 20)
	sc_m.add_theme_constant_override("margin_top", 14)
	sc_m.add_theme_constant_override("margin_bottom", 14)
	status_card.add_child(sc_m)

	var sc_v := VBoxContainer.new()
	sc_v.add_theme_constant_override("separation", 8)
	sc_m.add_child(sc_v)

	_energy_val_label = Label.new()
	_energy_val_label.text = _t("當前能量：—")
	_energy_val_label.add_theme_font_size_override("font_size", 20)
	_energy_val_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_energy_val_label.add_theme_font_override("font", _cached_font)
	sc_v.add_child(_energy_val_label)

	_status_detail_label = Label.new()
	_status_detail_label.text = _t("自然回復：—")
	_status_detail_label.add_theme_font_size_override("font_size", 15)
	_status_detail_label.add_theme_color_override("font_color", COLOR_TEXT_GOLD)
	sc_v.add_child(_status_detail_label)

	var desc_lbl := Label.new()
	_desc_lbl = desc_lbl
	desc_lbl.text = _t("出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！")
	desc_lbl.add_theme_font_size_override("font_size", 16)
	desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	v.add_child(desc_lbl)

	# 底部雙操作按鈕 (高度 >= 50px)
	var btn_h := HBoxContainer.new()
	btn_h.add_theme_constant_override("separation", 16)
	btn_h.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(btn_h)

	# 看廣告拿體力按鈕 (薄荷綠立體果凍厚底)
	_ad_btn = Button.new()
	_ad_btn.name = "WatchAdBtn"
	_ad_btn.custom_minimum_size = Vector2(340, 52)
	_ad_btn.add_theme_font_size_override("font_size", 18)
	_ad_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	_ad_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_ad_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_ad_btn.add_theme_font_override("font", _cached_font)
	_ad_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6))
	_ad_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5CE879"), COLOR_BORDER, 6))
	_ad_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3DBB55"), COLOR_BORDER, 2))
	_ad_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#B0ADBE"), COLOR_BORDER, 3))
	_ad_btn.pressed.connect(_on_watch_ad_clicked)
	btn_h.add_child(_ad_btn)

	# 返回按鈕 (溫暖米黃/橙底)
	var back_btn := Button.new()
	back_btn.name = "BackBtn"
	back_btn.text = _t("稍後再來")
	back_btn.custom_minimum_size = Vector2(180, 52)
	back_btn.add_theme_font_size_override("font_size", 18)
	back_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		back_btn.add_theme_font_override("font", _cached_font)
	back_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 6))
	back_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFF0D0"), COLOR_BORDER, 6))
	back_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#FFE0A0"), COLOR_BORDER, 2))
	back_btn.pressed.connect(_on_close_clicked)
	btn_h.add_child(back_btn)


func _is_ad_removed() -> bool:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var es: Node = (loop as SceneTree).root.get_node_or_null("EnergySystem")
		if es and es.has_method("is_ad_removed"):
			return bool(es.call("is_ad_removed"))
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs:
			if "has_removed_ads" in gs:
				return bool(gs.get("has_removed_ads"))
			if gs.has_method("get_flag"):
				return bool(gs.call("get_flag", "has_removed_ads", false))
	return false


func _refresh_display() -> void:
	var cur := 0
	var mx := 15
	var loop := Engine.get_main_loop()
	var es: Node = null
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es:
		if es.has_method("current"):
			cur = int(es.call("current"))
		if "MAX_ENERGY" in es:
			mx = int(es.get("MAX_ENERGY"))

	if _energy_val_label:
		_energy_val_label.text = _t("當前能量：%d／%d") % [cur, mx]

	if _status_detail_label:
		if es and es.has_method("status_line"):
			_status_detail_label.text = str(es.call("status_line"))
		else:
			_status_detail_label.text = _t("能量恢復中……")

	var left := 0
	var cap := 3
	var can_claim := false
	if es:
		if es.has_method("ad_rewards_left_today"):
			left = int(es.call("ad_rewards_left_today"))
		if "DAILY_AD_REWARD_CAP" in es:
			cap = int(es.get("DAILY_AD_REWARD_CAP"))
		if es.has_method("can_claim_ad_energy"):
			can_claim = bool(es.call("can_claim_ad_energy"))

	var ad_removed := _is_ad_removed()
	if _desc_lbl:
		if ad_removed:
			_desc_lbl.text = _t("出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是直接領取補充 3 點能量！")
		else:
			_desc_lbl.text = _t("出發探索或挑戰戰鬥需要充足的發條能量。\n您可以稍候等待能量自然回復，或是觀看廣告立即補充 3 點能量！")

	if _ad_btn:
		if can_claim:
			_ad_btn.disabled = false
			if ad_removed:
				_ad_btn.text = _t("已移除廣告，直接領取 (+3)  (%d/%d)") % [left, cap]
			else:
				_ad_btn.text = _t("觀看廣告回復能量 (+3)  (%d/%d)") % [left, cap]
		else:
			_ad_btn.disabled = true
			if ad_removed:
				_ad_btn.text = _t("今日領取次數已達上限 (0/%d)") % cap
			else:
				_ad_btn.text = _t("今日廣告次數已達上限 (0/%d)") % cap


func _on_watch_ad_clicked() -> void:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es and es.has_method("can_claim_ad_energy") and not bool(es.call("can_claim_ad_energy")):
		return

	if _is_ad_removed():
		_on_ad_watch_success()
		return

	# 開啟本機假讀秒占位廣告畫面
	MockAdDialogScript.show_ad(self, "energy", func():
		_on_ad_watch_success()
	)


func _on_ad_watch_success() -> void:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")

	if es and es.has_method("claim_ad_energy"):
		es.call("claim_ad_energy", 3)

	_refresh_display()
	energy_granted.emit(3)

	if _on_granted.is_valid():
		_on_granted.call()


func _on_close_clicked() -> void:
	closed.emit()
	if _on_close.is_valid():
		_on_close.call()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
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
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.3)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb
