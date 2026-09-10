class_name WindupDailyDialog
extends Control
## 《發條之心》冒險委託每日上發條彈窗 (WindupDailyDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 連接既有 WindupDailySystem「今天，誰需要上發條？」當日個案。
##    兩個選項可選、完成發獎勵、當天不可再領。
## 7. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字

var _dialog_card: PanelContainer
var _case_title_label: Label
var _case_desc_label: Label
var _prompt_label: Label
var _unlock_label: Label
var _milestone_label: Label
var _choices_box: HBoxContainer
var _msg_label: Label
var _choice_buttons: Array[Button] = []
var _cached_font: Font = null


func _ready() -> void:
	name = "WindupDailyDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	WindupDailySystem.refresh()
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
	scrim_btn.pressed.connect(_on_close)
	scrim.add_child(scrim_btn)

	# 2. 置中卡片 (寬 750px，符合 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "WindupDailyCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(750, 480)
	# 奶油米白底 + 深藍紫立體邊框 + 22px 大圓角
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_dialog_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 12)
	margin.add_child(v)

	# 標題列 + 右上「✕」關閉按鈕 (50x50)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.text = "冒險委託 · 今天誰需要上發條"
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_ORANGE)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 亮橘色粗分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	# 個案內容卡片 (溫暖米黃卡片底 + 20px 圓角)
	var case_panel := PanelContainer.new()
	case_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 20))
	v.add_child(case_panel)

	var cm := MarginContainer.new()
	cm.add_theme_constant_override("margin_left", 16)
	cm.add_theme_constant_override("margin_right", 16)
	cm.add_theme_constant_override("margin_top", 12)
	cm.add_theme_constant_override("margin_bottom", 12)
	case_panel.add_child(cm)

	var cv := VBoxContainer.new()
	cv.add_theme_constant_override("separation", 8)
	cm.add_child(cv)

	_case_title_label = Label.new()
	_case_title_label.name = "CaseTitle"
	_case_title_label.text = "【個案委託】"
	_case_title_label.add_theme_font_size_override("font_size", 18)
	_case_title_label.add_theme_color_override("font_color", COLOR_ORANGE)
	_case_title_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_case_title_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_case_title_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_case_title_label)

	_case_desc_label = Label.new()
	_case_desc_label.name = "CaseDesc"
	_case_desc_label.text = "委託描述"
	_case_desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_case_desc_label.add_theme_font_size_override("font_size", 16)
	_case_desc_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_case_desc_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_case_desc_label.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_case_desc_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_case_desc_label)

	_prompt_label = Label.new()
	_prompt_label.name = "CasePrompt"
	_prompt_label.text = "對話提示"
	_prompt_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_prompt_label.add_theme_font_size_override("font_size", 16)
	_prompt_label.add_theme_color_override("font_color", COLOR_SKY)
	_prompt_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_prompt_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_prompt_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_prompt_label)

	_unlock_label = Label.new()
	_unlock_label.name = "CaseUnlock"
	_unlock_label.text = ""
	_unlock_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_unlock_label.add_theme_font_size_override("font_size", 16)
	_unlock_label.add_theme_color_override("font_color", COLOR_PINK)
	_unlock_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_unlock_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_unlock_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_unlock_label)

	_milestone_label = Label.new()
	_milestone_label.name = "MilestoneHint"
	_milestone_label.text = "累計上發條 0 次"
	_milestone_label.add_theme_font_size_override("font_size", 16)
	_milestone_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_milestone_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_milestone_label.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_milestone_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_milestone_label)

	# 獎勵與反饋訊息
	_msg_label = Label.new()
	_msg_label.name = "MsgLabel"
	_msg_label.text = "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1"
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 16)
	_msg_label.add_theme_color_override("font_color", COLOR_ORANGE)
	_msg_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_msg_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 委託行動選項按鈕區 (按鈕高 >= 50, 薄荷綠立體果凍厚底 6px)
	_choices_box = HBoxContainer.new()
	_choices_box.name = "ChoicesBox"
	_choices_box.alignment = BoxContainer.ALIGNMENT_CENTER
	_choices_box.add_theme_constant_override("separation", 16)
	v.add_child(_choices_box)

	# 底部關閉按鈕列 (金黃立體厚底 5px)
	var foot := HBoxContainer.new()
	foot.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(foot)

	var btn_leave := Button.new()
	btn_leave.name = "BtnCloseWindup"
	btn_leave.text = "離開委託"
	btn_leave.custom_minimum_size = Vector2(180, 52)
	btn_leave.add_theme_font_size_override("font_size", 18)
	btn_leave.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_leave.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_leave.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		btn_leave.add_theme_font_override("font", _cached_font)
	btn_leave.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20, 2))
	btn_leave.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 20, 2))
	btn_leave.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
	btn_leave.pressed.connect(_on_close)
	foot.add_child(btn_leave)


func _refresh_display() -> void:
	WindupDailySystem.refresh()
	var c: Dictionary = WindupDailySystem.todays_case()
	var is_done := WindupDailySystem.is_done_today()

	_case_title_label.text = "【%s】 %s" % [str(c.get("npc", "NPC")), str(c.get("title", "未命名個案"))]
	_case_desc_label.text = str(c.get("desc", ""))

	_milestone_label.text = "累計上發條 %d 次 · %s" % [WindupDailySystem.windup_count(), WindupDailySystem.milestone_hint()]

	for child in _choices_box.get_children():
		child.queue_free()
	_choice_buttons.clear()

	if is_done:
		_prompt_label.text = "今天這截發條已經上好。明天再來看誰需要。"
		_prompt_label.add_theme_color_override("font_color", COLOR_MINT)
		var unlock_text := str(c.get("unlock", ""))
		if unlock_text.is_empty():
			_unlock_label.text = "這截發條輕輕咬合，發出溫柔的運轉聲。"
		else:
			_unlock_label.text = unlock_text
		_unlock_label.visible = true

		_msg_label.text = "今日委託獎勵已領取，明日將輪替新個案。"
		_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)

		var done_btn := Button.new()
		done_btn.name = "BtnDoneStatus"
		done_btn.text = "今日委託已完成（當日不可再領）"
		done_btn.disabled = true
		done_btn.custom_minimum_size = Vector2(320, 52)
		done_btn.add_theme_font_size_override("font_size", 16)
		done_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		done_btn.add_theme_color_override("font_disabled_color", COLOR_TEXT_DARK)
		done_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		done_btn.add_theme_constant_override("outline_size", 1)
		if _cached_font:
			done_btn.add_theme_font_override("font", _cached_font)
		done_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#EFEAE0"), COLOR_BORDER, 3, 20, 2))
		_choices_box.add_child(done_btn)
	else:
		_prompt_label.text = str(c.get("prompt", "請選擇行動為發條玩具轉緊發條："))
		_prompt_label.add_theme_color_override("font_color", COLOR_SKY)
		_unlock_label.text = ""
		_unlock_label.visible = false

		_msg_label.text = "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1"
		_msg_label.add_theme_color_override("font_color", COLOR_ORANGE)

		var choices: Array = c.get("choices", [])
		for i in range(choices.size()):
			var ch: Dictionary = choices[i]
			var cid := str(ch.get("id", ""))
			var clabel := str(ch.get("label", cid))

			var btn := Button.new()
			btn.name = "ChoiceBtn_%d" % i
			btn.text = clabel
			btn.custom_minimum_size = Vector2(260, 52)
			btn.add_theme_font_size_override("font_size", 16)
			btn.add_theme_color_override("font_color", Color.WHITE)
			btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
			btn.add_theme_constant_override("outline_size", 4)
			if _cached_font:
				btn.add_theme_font_override("font", _cached_font)
			btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 20, 2))
			btn.add_theme_stylebox_override("hover", _create_button_style(Color("#68E882"), COLOR_BORDER, 6, 20, 2))
			btn.add_theme_stylebox_override("pressed", _create_button_style(Color("#3BBF55"), COLOR_BORDER, 2, 20, 2))

			btn.pressed.connect(func():
				_on_choice_selected(cid)
			)
			_choices_box.add_child(btn)
			_choice_buttons.append(btn)


func _on_choice_selected(choice_id: String) -> void:
	var r: Dictionary = WindupDailySystem.complete(choice_id)
	SaveManager.save_game()
	_refresh_display()
	if bool(r.get("ok", false)):
		_msg_label.text = "委託完成！" + str(r.get("msg", "已獲得獎勵！"))
		_msg_label.add_theme_color_override("font_color", COLOR_MINT)
	else:
		_msg_label.text = str(r.get("msg", "領取失敗"))
		_msg_label.add_theme_color_override("font_color", COLOR_PINK)


func _on_close() -> void:
	closed.emit()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	sb.shadow_size = 10
	sb.shadow_offset = Vector2(0, 5)
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
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.35)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb
