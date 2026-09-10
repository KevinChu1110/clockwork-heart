class_name ForgeDialog
extends Control
## 《發條之心》王都鐵匠鍛造彈窗 (ForgeDialog)
## 依手遊人體工學與 review.md 第 28、29 條規範：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 連接既有鍛造系統與連敗保底進度 (3 格保底)。
## 4. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
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

var _dialog_card: PanelContainer
var _weapon_label: Label
var _atk_label: Label
var _gold_label: Label
var _cost_label: Label
var _rate_label: Label
var _slots_label: Label

var _pity_title_label: Label
var _pity_sub_label: Label
var _pity_bars: Array[ProgressBar] = []

var _msg_label: Label
var _btn_forge: Button
var _btn_close: Button
var _cached_font: Font = null


func _ready() -> void:
	name = "ForgeDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_ensure_initial_state()
	_build_ui()
	_refresh_display()


func _ensure_initial_state() -> void:
	if not GameState.has_flag("c1_forged"):
		GameState.set_flag("c1_forged", true)
	if GameState.weapon_tier < 1:
		GameState.weapon_tier = 2
	if GameState.weapon_atk <= 0:
		GameState.weapon_atk = 9
	if GameState.weapon_name.is_empty():
		GameState.weapon_name = "微末之刃"


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

	# 2. 置中卡片 (寬 750px，符合 review.md 第 28 條 740~760px 規範)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_dialog_card = PanelContainer.new()
	_dialog_card.name = "ForgeCard"
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
	title_lbl.text = "王都鐵匠 · 裝備鍛造"
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

	# 武器當前數值面板
	var status_panel := PanelContainer.new()
	status_panel.add_theme_stylebox_override("panel", _create_panel_style(OBSIDIAN_WARM, LINE_GOLD, 1, 2, 10))
	v.add_child(status_panel)

	var s_margin := MarginContainer.new()
	s_margin.add_theme_constant_override("margin_left", 14)
	s_margin.add_theme_constant_override("margin_right", 14)
	s_margin.add_theme_constant_override("margin_top", 10)
	s_margin.add_theme_constant_override("margin_bottom", 10)
	status_panel.add_child(s_margin)

	var sv := VBoxContainer.new()
	sv.add_theme_constant_override("separation", 6)
	s_margin.add_child(sv)

	_weapon_label = Label.new()
	_weapon_label.text = "當前裝備：微末之刃（第 2 階）"
	_weapon_label.add_theme_font_size_override("font_size", 18)
	_weapon_label.add_theme_color_override("font_color", INK_IVORY)
	if _cached_font:
		_weapon_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_weapon_label)

	var stats_grid := GridContainer.new()
	stats_grid.columns = 2
	stats_grid.add_theme_constant_override("h_separation", 24)
	stats_grid.add_theme_constant_override("v_separation", 4)
	sv.add_child(stats_grid)

	_atk_label = _create_info_label(stats_grid, "武器攻擊：+9")
	_gold_label = _create_info_label(stats_grid, "持有金幣：0")
	_cost_label = _create_info_label(stats_grid, "升階花費：80 金幣")
	_rate_label = _create_info_label(stats_grid, "基礎成功率：77%")

	_slots_label = Label.new()
	_slots_label.text = "魂槽開放：1/4 槽"
	_slots_label.add_theme_font_size_override("font_size", 14)
	_slots_label.add_theme_color_override("font_color", INK_MUTED)
	if _cached_font:
		_slots_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_slots_label)

	# 既有連敗保底進度條區塊
	var pity_panel := PanelContainer.new()
	pity_panel.name = "PityContainer"
	pity_panel.add_theme_stylebox_override("panel", _create_panel_style(OBSIDIAN_DEEP, LINE_GOLD, 1, 2, 10))
	v.add_child(pity_panel)

	var pm := MarginContainer.new()
	pm.add_theme_constant_override("margin_left", 14)
	pm.add_theme_constant_override("margin_right", 14)
	pm.add_theme_constant_override("margin_top", 10)
	pm.add_theme_constant_override("margin_bottom", 10)
	pity_panel.add_child(pm)

	var pv := VBoxContainer.new()
	pv.add_theme_constant_override("separation", 6)
	pm.add_child(pv)

	_pity_title_label = Label.new()
	_pity_title_label.text = "鍛造連敗保底 0/3 · 滿 3 格釘釘摔錘必成功"
	_pity_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_title_label.add_theme_font_size_override("font_size", 15)
	_pity_title_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		_pity_title_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_title_label)

	var bar_row := HBoxContainer.new()
	bar_row.name = "PityBarRow"
	bar_row.alignment = BoxContainer.ALIGNMENT_CENTER
	bar_row.add_theme_constant_override("separation", 8)
	pv.add_child(bar_row)

	_pity_bars.clear()
	for i in range(3):
		var seg := ProgressBar.new()
		seg.min_value = 0
		seg.max_value = 1
		seg.value = 0.0
		seg.custom_minimum_size = Vector2(160, 18)
		seg.show_percentage = false
		var fill_color: Color = Color(1.0, 0.63, 0.06) if i < 2 else Color(1.0, 0.38, 0.28)
		UiStyle.style_progress(seg, fill_color, Color(0.16, 0.14, 0.20))
		bar_row.add_child(seg)
		_pity_bars.append(seg)

	_pity_sub_label = Label.new()
	_pity_sub_label.text = "升階失敗累積 1 格 · 升階成功清空進度"
	_pity_sub_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_sub_label.add_theme_font_size_override("font_size", 13)
	_pity_sub_label.add_theme_color_override("font_color", INK_MUTED)
	if _cached_font:
		_pity_sub_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_sub_label)

	# 訊息回饋
	_msg_label = Label.new()
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 14)
	_msg_label.add_theme_color_override("font_color", GOLD_HOVER)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 動作按鈕列 (按鈕高 >= 50)
	var act_row := HBoxContainer.new()
	act_row.add_theme_constant_override("separation", 16)
	act_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(act_row)

	_btn_forge = Button.new()
	_btn_forge.name = "BtnForge"
	_btn_forge.text = "強化升階（消耗 80 金幣）"
	_btn_forge.custom_minimum_size = Vector2(280, 52)
	_btn_forge.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_btn_forge.add_theme_font_override("font", _cached_font)
	_btn_forge.add_theme_stylebox_override("normal", _create_button_style(BTN_GREEN_BG, BTN_GREEN_BORDER, 4))
	_btn_forge.add_theme_stylebox_override("hover", _create_button_style(Color(0.25, 0.68, 0.38), BTN_GREEN_BORDER, 4))
	_btn_forge.add_theme_stylebox_override("pressed", _create_button_style(Color(0.16, 0.48, 0.25), BTN_GREEN_BORDER, 2))
	_btn_forge.add_theme_color_override("font_color", Color.WHITE)
	_btn_forge.pressed.connect(_on_forge_pressed)
	act_row.add_child(_btn_forge)

	_btn_close = Button.new()
	_btn_close.name = "BtnCloseForge"
	_btn_close.text = "離開鐵匠鋪"
	_btn_close.custom_minimum_size = Vector2(160, 52)
	_btn_close.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_btn_close.add_theme_font_override("font", _cached_font)
	_btn_close.add_theme_stylebox_override("normal", _create_button_style(OBSIDIAN_WARM, LINE_GOLD, 4))
	_btn_close.add_theme_stylebox_override("hover", _create_button_style(Color(0.15, 0.13, 0.18), GOLD_HOVER, 4))
	_btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color(0.08, 0.07, 0.10), LINE_GOLD, 2))
	_btn_close.add_theme_color_override("font_color", INK_IVORY)
	_btn_close.pressed.connect(_on_close)
	act_row.add_child(_btn_close)


func _create_info_label(parent: Container, text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 14)
	l.add_theme_color_override("font_color", INK_IVORY)
	if _cached_font:
		l.add_theme_font_override("font", _cached_font)
	parent.add_child(l)
	return l


func _refresh_display() -> void:
	var at_max := GameState.weapon_tier >= ForgeSystem.FORGE_MAX_TIER
	var wname := GameState.weapon_display() if GameState.has_method("weapon_display") else GameState.weapon_name
	_weapon_label.text = "當前裝備：%s（第 %d 階）" % [wname, GameState.weapon_tier]
	_atk_label.text = "武器攻擊：+%d" % GameState.weapon_atk
	_gold_label.text = "持有金幣：%d" % GameState.gold

	var cost := ForgeSystem.forge_cost()
	if at_max:
		_cost_label.text = "升階花費：已達上限"
		_rate_label.text = "成功率：已封頂"
		_btn_forge.text = "鍛造已封頂"
		_btn_forge.disabled = true
	else:
		_cost_label.text = "升階花費：%d 金幣" % cost
		var rate_pct := int(ForgeSystem.forge_rate_base() * 100.0)
		_rate_label.text = "基礎成功率：%d%%" % rate_pct
		_btn_forge.text = "強化升階（消耗 %d 金幣）" % cost
		_btn_forge.disabled = false

	# 魂槽狀態
	var slots := SoulSystem.slot_count()
	var next_slot := 0
	for need in SoulSystem.SLOT_TIERS:
		if GameState.weapon_tier < need:
			next_slot = need
			break
	if next_slot > 0:
		_slots_label.text = "魂槽開放：%d/%d 槽（下一槽需器階 %d）" % [slots, SoulSystem.SLOT_TIERS.size(), next_slot]
	else:
		_slots_label.text = "魂槽開放：%d/%d 槽（已全數開放）" % [slots, SoulSystem.SLOT_TIERS.size()]

	# 保底進度條
	var streak: int = clampi(GameState.forge_fail_streak, 0, 3)
	if at_max:
		_pity_title_label.text = "器階已達上限 · 鍛造已封頂"
		_pity_sub_label.text = "所有階級均已鍛造完成"
	elif streak < 3:
		_pity_title_label.text = "鍛造連敗保底 %d/3 · 滿 3 格釘釘摔錘必成功" % streak
		if streak == 2:
			_pity_sub_label.text = "再失敗 1 次將觸發第 3 格摔錘保底"
		elif streak == 1:
			_pity_sub_label.text = "升階失敗累積 1 格 · 升階成功清空進度"
		else:
			_pity_sub_label.text = "累積 3 次升階失敗將啟動必成功保底機制"
	else:
		_pity_title_label.text = "保底已滿 3/3 · 本次升階釘釘摔錘必成功！"
		_pity_sub_label.text = "保底已觸發 · 釘釘發脾氣必定升階"

	for i in range(_pity_bars.size()):
		_pity_bars[i].value = 1.0 if streak > i else 0.0


func _on_forge_pressed() -> void:
	var res: Dictionary = ForgeSystem.try_forge()
	match str(res.get("code", "")):
		"tier_max":
			_msg_label.text = "器階已達上限，無法再進行鍛造！"
			_msg_label.add_theme_color_override("font_color", INK_MUTED)
		"no_gold":
			var cost: int = int(res.get("cost", ForgeSystem.forge_cost()))
			_msg_label.text = "金幣不足！升階需要 %d 金幣。" % cost
			_msg_label.add_theme_color_override("font_color", Color(1.0, 0.45, 0.45))
		"success":
			var scrap_tip := "（消耗鐵屑穩火）" if bool(res.get("used_scrap", false)) else ""
			_msg_label.text = "鍛造成功！升階至第 %d 階，攻擊力上升！%s" % [GameState.weapon_tier, scrap_tip]
			_msg_label.add_theme_color_override("font_color", Color(0.4, 0.95, 0.5))
		"pity_break":
			_msg_label.text = "鍛造失敗！釘釘摔錘了，吃塊消氣餅回復體力！"
			_msg_label.add_theme_color_override("font_color", Color(1.0, 0.75, 0.3))
		"failed":
			var streak: int = int(res.get("fail_streak", GameState.forge_fail_streak))
			_msg_label.text = "鍛造失敗！累積 1 格保底進度（目前 %d/3 格）。" % streak
			_msg_label.add_theme_color_override("font_color", Color(1.0, 0.6, 0.35))
	_refresh_display()


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
