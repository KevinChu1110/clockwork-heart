class_name WindupDailyDialog
extends Control
## 《發條之心》冒險委託每日上發條彈窗 (WindupDailyDialog)
## 依手遊人體工學與 review.md 第 28、29 條規範：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 連接既有 WindupDailySystem「今天，誰需要上發條？」當日個案。
##    兩個選項可選、完成發獎勵、當天不可再領。
## 4. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const OBSIDIAN_CARD   := Color(0.078, 0.071, 0.094, 0.98)
const OBSIDIAN_WARM   := Color(0.102, 0.090, 0.122, 1.0)
const OBSIDIAN_DEEP   := Color(0.027, 0.024, 0.039, 1.0)
const GOLD_CLASSICAL  := Color(0.831, 0.686, 0.216, 1.0)
const GOLD_HOVER      := Color(0.941, 0.843, 0.549, 1.0)
const INK_IVORY       := Color(0.957, 0.922, 0.831, 1.0)
const INK_MUTED       := Color(0.65, 0.60, 0.52, 1.0)
const LINE_GOLD       := Color(0.831, 0.686, 0.216, 0.5)
const BTN_GREEN_BG    := Color(0.20, 0.58, 0.32, 1.0)
const BTN_GREEN_BORDER:= Color(0.35, 0.78, 0.48, 1.0)
const COLOR_SUCCESS   := Color(0.31, 0.85, 0.42, 1.0)

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
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(OBSIDIAN_CARD, GOLD_CLASSICAL, 1, 4, 14))
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
	title_lbl.add_theme_font_size_override("font_size", 20)
	title_lbl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(_on_close)
	head.add_child(close_btn)

	# 金色分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 2)
	sep.color = LINE_GOLD
	v.add_child(sep)

	# 個案內容卡片 (PanelContainer)
	var case_panel := PanelContainer.new()
	case_panel.add_theme_stylebox_override("panel", _create_panel_style(OBSIDIAN_WARM, LINE_GOLD, 1, 2, 10))
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
	_case_title_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		_case_title_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_case_title_label)

	_case_desc_label = Label.new()
	_case_desc_label.name = "CaseDesc"
	_case_desc_label.text = "委託描述"
	_case_desc_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_case_desc_label.add_theme_font_size_override("font_size", 15)
	_case_desc_label.add_theme_color_override("font_color", INK_IVORY)
	if _cached_font:
		_case_desc_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_case_desc_label)

	_prompt_label = Label.new()
	_prompt_label.name = "CasePrompt"
	_prompt_label.text = "對話提示"
	_prompt_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_prompt_label.add_theme_font_size_override("font_size", 14)
	_prompt_label.add_theme_color_override("font_color", GOLD_HOVER)
	if _cached_font:
		_prompt_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_prompt_label)

	_unlock_label = Label.new()
	_unlock_label.name = "CaseUnlock"
	_unlock_label.text = ""
	_unlock_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_unlock_label.add_theme_font_size_override("font_size", 14)
	_unlock_label.add_theme_color_override("font_color", COLOR_SUCCESS)
	if _cached_font:
		_unlock_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_unlock_label)

	_milestone_label = Label.new()
	_milestone_label.name = "MilestoneHint"
	_milestone_label.text = "累計上發條 0 次"
	_milestone_label.add_theme_font_size_override("font_size", 13)
	_milestone_label.add_theme_color_override("font_color", INK_MUTED)
	if _cached_font:
		_milestone_label.add_theme_font_override("font", _cached_font)
	cv.add_child(_milestone_label)

	# 獎勵與反饋訊息
	_msg_label = Label.new()
	_msg_label.name = "MsgLabel"
	_msg_label.text = "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1"
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 14)
	_msg_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 委託行動選項按鈕區 (按鈕高 >= 50)
	_choices_box = HBoxContainer.new()
	_choices_box.name = "ChoicesBox"
	_choices_box.alignment = BoxContainer.ALIGNMENT_CENTER
	_choices_box.add_theme_constant_override("separation", 16)
	v.add_child(_choices_box)

	# 底部關閉按鈕列
	var foot := HBoxContainer.new()
	foot.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(foot)

	var btn_leave := Button.new()
	btn_leave.name = "BtnCloseWindup"
	btn_leave.text = "離開委託"
	btn_leave.custom_minimum_size = Vector2(180, 50)
	btn_leave.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		btn_leave.add_theme_font_override("font", _cached_font)
	btn_leave.add_theme_stylebox_override("normal", _create_button_style(OBSIDIAN_WARM, LINE_GOLD, 4))
	btn_leave.add_theme_stylebox_override("hover", _create_button_style(Color(0.15, 0.13, 0.18), GOLD_HOVER, 4))
	btn_leave.add_theme_stylebox_override("pressed", _create_button_style(Color(0.08, 0.07, 0.10), LINE_GOLD, 2))
	btn_leave.add_theme_color_override("font_color", INK_IVORY)
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
		_prompt_label.add_theme_color_override("font_color", COLOR_SUCCESS)
		var unlock_text := str(c.get("unlock", ""))
		if unlock_text.is_empty():
			_unlock_label.text = "這截發條輕輕咬合，發出溫柔的運轉聲。"
		else:
			_unlock_label.text = unlock_text
		_unlock_label.visible = true

		_msg_label.text = "今日委託獎勵已領取，明日將輪替新個案。"
		_msg_label.add_theme_color_override("font_color", INK_MUTED)

		var done_btn := Button.new()
		done_btn.name = "BtnDoneStatus"
		done_btn.text = "今日委託已完成（當日不可再領）"
		done_btn.disabled = true
		done_btn.custom_minimum_size = Vector2(320, 50)
		done_btn.add_theme_font_size_override("font_size", 15)
		if _cached_font:
			done_btn.add_theme_font_override("font", _cached_font)
		done_btn.add_theme_stylebox_override("disabled", _create_button_style(Color(0.12, 0.11, 0.15), Color(0.25, 0.22, 0.30), 2))
		done_btn.add_theme_color_override("font_disabled_color", INK_MUTED)
		_choices_box.add_child(done_btn)
	else:
		_prompt_label.text = str(c.get("prompt", "請選擇行動為發條玩具轉緊發條："))
		_prompt_label.add_theme_color_override("font_color", GOLD_HOVER)
		_unlock_label.text = ""
		_unlock_label.visible = false

		_msg_label.text = "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1"
		_msg_label.add_theme_color_override("font_color", GOLD_CLASSICAL)

		var choices: Array = c.get("choices", [])
		for i in range(choices.size()):
			var ch: Dictionary = choices[i]
			var cid := str(ch.get("id", ""))
			var clabel := str(ch.get("label", cid))

			var btn := Button.new()
			btn.name = "ChoiceBtn_%d" % i
			btn.text = clabel
			btn.custom_minimum_size = Vector2(260, 50)
			btn.add_theme_font_size_override("font_size", 16)
			if _cached_font:
				btn.add_theme_font_override("font", _cached_font)
			btn.add_theme_stylebox_override("normal", _create_button_style(BTN_GREEN_BG, BTN_GREEN_BORDER, 4))
			btn.add_theme_stylebox_override("hover", _create_button_style(Color(0.25, 0.68, 0.38), BTN_GREEN_BORDER, 4))
			btn.add_theme_stylebox_override("pressed", _create_button_style(Color(0.16, 0.48, 0.25), BTN_GREEN_BORDER, 2))
			btn.add_theme_color_override("font_color", Color.WHITE)

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
		_msg_label.add_theme_color_override("font_color", COLOR_SUCCESS)
	else:
		_msg_label.text = str(r.get("msg", "領取失敗"))
		_msg_label.add_theme_color_override("font_color", Color(1.0, 0.5, 0.4))


func _on_close() -> void:
	closed.emit()
	queue_free()


func _create_panel_style(bg: Color, border: Color, border_w: int = 1, bottom_w: int = 3, radius: int = 12) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	return sb


func _create_button_style(bg: Color, border: Color, bottom_border: int = 4) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(1)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	return sb
