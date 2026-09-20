class_name MockAdDialog
extends Control
## 《發條之心》獎勵型廣告展示視窗（本機假讀秒占位版）
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 零系統 emoji、零開發用語（不露出 SDK、Mock、佔位等詞）。
## 6. 倒數 2 秒本機計時，計時完成發放獎勵。

signal ad_completed(reward_type: String)
signal ad_cancelled(reward_type: String)

const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
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

var reward_type: String = "energy"  ## energy | revive
var _on_success: Callable = Callable()
var _on_cancel: Callable = Callable()

var _dialog_card: PanelContainer
var _status_label: Label
var _countdown_label: Label
var _action_btn: Button
var _progress_bar: ProgressBar
var _cached_font: Font = null

var _time_total: float = 2.0
var _time_left: float = 2.0
var _is_finished: bool = false
var _timer_active: bool = true


static func show_ad(parent: Node, p_reward_type: String, on_success: Callable, on_cancel: Callable = Callable()) -> Control:
	var dlg = load("res://scripts/ui/mock_ad_dialog.gd").new()
	dlg.setup(p_reward_type, on_success, on_cancel)
	parent.add_child(dlg)
	return dlg


func setup(p_reward_type: String, on_success: Callable = Callable(), on_cancel: Callable = Callable()) -> void:
	reward_type = p_reward_type
	_on_success = on_success
	_on_cancel = on_cancel


func _ready() -> void:
	name = "MockAdDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 100

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build_ui()


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	add_child(scrim)

	# 2. 置中卡片 (寬 750px)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "AdCard"
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

	# 頂部標題列 + 關閉鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.text = _t("贊助商廣告")
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

	# 廣告內容主視覺框（多巴胺金黃底）
	var ad_box := PanelContainer.new()
	ad_box.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 18))
	ad_box.custom_minimum_size = Vector2(0, 180)
	v.add_child(ad_box)

	var ab_m := MarginContainer.new()
	ab_m.add_theme_constant_override("margin_left", 20)
	ab_m.add_theme_constant_override("margin_right", 20)
	ab_m.add_theme_constant_override("margin_top", 16)
	ab_m.add_theme_constant_override("margin_bottom", 16)
	ad_box.add_child(ab_m)

	var ab_v := VBoxContainer.new()
	ab_v.alignment = BoxContainer.ALIGNMENT_CENTER
	ab_v.add_theme_constant_override("separation", 10)
	ab_m.add_child(ab_v)

	var sponsor_title := Label.new()
	sponsor_title.text = _t("發條工坊 · 上鍊補給")
	sponsor_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sponsor_title.add_theme_font_size_override("font_size", 20)
	sponsor_title.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		sponsor_title.add_theme_font_override("font", _cached_font)
	ab_v.add_child(sponsor_title)

	var sponsor_desc := Label.new()
	if reward_type == "revive":
		sponsor_desc.text = _t("齒輪重新咬合，金屬骨架再度充能！\n贊助商為倒下的玩具勇者提供重返戰場的二次機會。")
	else:
		sponsor_desc.text = _t("發條鬆了跑不動？轉動發條就有力氣！\n歇口氣看看工坊消息，冒險動能馬上補滿。")
	sponsor_desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sponsor_desc.add_theme_font_size_override("font_size", 16)
	sponsor_desc.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	ab_v.add_child(sponsor_desc)

	# 進度條與狀態列
	var prog_v := VBoxContainer.new()
	prog_v.add_theme_constant_override("separation", 6)
	v.add_child(prog_v)

	var status_h := HBoxContainer.new()
	prog_v.add_child(status_h)

	_status_label = Label.new()
	_status_label.text = _t("廣告播映中……")
	_status_label.add_theme_font_size_override("font_size", 15)
	_status_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_status_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	status_h.add_child(_status_label)

	_countdown_label = Label.new()
	_countdown_label.text = _t("剩餘 %d 秒") % 2
	_countdown_label.add_theme_font_size_override("font_size", 16)
	_countdown_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	status_h.add_child(_countdown_label)

	_progress_bar = ProgressBar.new()
	_progress_bar.custom_minimum_size = Vector2(0, 18)
	_progress_bar.max_value = 100.0
	_progress_bar.value = 0.0
	_progress_bar.show_percentage = false

	var bg_sb := StyleBoxFlat.new()
	bg_sb.bg_color = Color("#E5E0D5")
	bg_sb.set_corner_radius_all(9)
	bg_sb.border_color = COLOR_BORDER
	bg_sb.set_border_width_all(1)
	_progress_bar.add_theme_stylebox_override("background", bg_sb)

	var fill_sb := StyleBoxFlat.new()
	fill_sb.bg_color = COLOR_MINT
	fill_sb.set_corner_radius_all(9)
	_progress_bar.add_theme_stylebox_override("fill", fill_sb)
	prog_v.add_child(_progress_bar)

	# 底部操作按鈕（高度 >= 50px）
	var btn_h := HBoxContainer.new()
	btn_h.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(btn_h)

	_action_btn = Button.new()
	_action_btn.text = _t("廣告播放中 (請稍候)")
	_action_btn.custom_minimum_size = Vector2(280, 52)
	_action_btn.disabled = true
	_action_btn.add_theme_font_size_override("font_size", 18)
	_action_btn.add_theme_color_override("font_color", Color("#FFFDF8"))
	_action_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_action_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_action_btn.add_theme_font_override("font", _cached_font)
	_action_btn.add_theme_stylebox_override("normal", _create_button_style(Color("#8E8B9E"), COLOR_BORDER, 4))
	_action_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#B0ADBE"), COLOR_BORDER, 3))
	_action_btn.pressed.connect(_on_claim_reward)
	btn_h.add_child(_action_btn)


func _process(delta: float) -> void:
	if not _timer_active or _is_finished:
		return

	_time_left = maxf(0.0, _time_left - delta)
	var pct := (1.0 - (_time_left / _time_total)) * 100.0
	if _progress_bar:
		_progress_bar.value = pct

	var sec_ceil := int(ceil(_time_left))
	if _countdown_label:
		if sec_ceil > 0:
			_countdown_label.text = _t("剩餘 %d 秒") % sec_ceil
		else:
			_countdown_label.text = _t("播映完畢！")

	if _time_left <= 0.0:
		_on_ad_playback_completed()


func _on_ad_playback_completed() -> void:
	_is_finished = true
	_timer_active = false
	if _status_label:
		_status_label.text = _t("觀看完成！已可領取獎勵。")
		_status_label.add_theme_color_override("font_color", COLOR_TEXT_MINT)
	if _action_btn:
		_action_btn.disabled = false
		_action_btn.text = _t("領取獎勵")
		_action_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6))
		_action_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5CE879"), COLOR_BORDER, 6))
		_action_btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3DBB55"), COLOR_BORDER, 2))


func skip_countdown() -> void:
	## 供單元測試或快速跳過時使用
	_time_left = 0.0
	_on_ad_playback_completed()


func _on_claim_reward() -> void:
	ad_completed.emit(reward_type)
	if _on_success.is_valid():
		_on_success.call()
	queue_free()


func _on_close_clicked() -> void:
	if _is_finished:
		_on_claim_reward()
		return
	ad_cancelled.emit(reward_type)
	if _on_cancel.is_valid():
		_on_cancel.call()
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
	sb.content_margin_left = 20
	sb.content_margin_right = 20
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.3)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb
