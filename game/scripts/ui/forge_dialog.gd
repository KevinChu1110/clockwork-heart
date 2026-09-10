class_name ForgeDialog
extends Control
## 《發條之心》王都鐵匠鍛造彈窗 (ForgeDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 18~24px，主要按鈕做立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 連接既有鍛造系統與連敗保底進度 (3 格保底)。
## 7. 零 emoji、零系統字型符號。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
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
const COLOR_CARD_PINK  := Color("#FFF0F4")  ## 珊瑚粉柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字

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
	title_lbl.text = "王都鐵匠 · 裝備鍛造"
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

	# 武器當前數值面板 (亮金黃溫暖卡片底)
	var status_panel := PanelContainer.new()
	status_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 20))
	v.add_child(status_panel)

	var s_margin := MarginContainer.new()
	s_margin.add_theme_constant_override("margin_left", 16)
	s_margin.add_theme_constant_override("margin_right", 16)
	s_margin.add_theme_constant_override("margin_top", 12)
	s_margin.add_theme_constant_override("margin_bottom", 12)
	status_panel.add_child(s_margin)

	var sv := VBoxContainer.new()
	sv.add_theme_constant_override("separation", 6)
	s_margin.add_child(sv)

	_weapon_label = Label.new()
	_weapon_label.text = "當前裝備：微末之刃（第 2 階）"
	_weapon_label.add_theme_font_size_override("font_size", 18)
	_weapon_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_weapon_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_weapon_label.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		_weapon_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_weapon_label)

	var stats_grid := GridContainer.new()
	stats_grid.columns = 2
	stats_grid.add_theme_constant_override("h_separation", 24)
	stats_grid.add_theme_constant_override("v_separation", 6)
	sv.add_child(stats_grid)

	_atk_label = _create_info_label(stats_grid, "武器攻擊：+9")
	_gold_label = _create_info_label(stats_grid, "持有金幣：0")
	_cost_label = _create_info_label(stats_grid, "升階花費：80 金幣")
	_rate_label = _create_info_label(stats_grid, "基礎成功率：77%")

	_slots_label = Label.new()
	_slots_label.text = "魂槽開放：1/4 槽"
	_slots_label.add_theme_font_size_override("font_size", 16)
	_slots_label.add_theme_color_override("font_color", COLOR_SKY)
	_slots_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_slots_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_slots_label.add_theme_font_override("font", _cached_font)
	sv.add_child(_slots_label)

	# 既有連敗保底進度條區塊 (珊瑚粉卡片底)
	var pity_panel := PanelContainer.new()
	pity_panel.name = "PityContainer"
	pity_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_PINK, COLOR_BORDER, 2, 4, 20))
	v.add_child(pity_panel)

	var pm := MarginContainer.new()
	pm.add_theme_constant_override("margin_left", 16)
	pm.add_theme_constant_override("margin_right", 16)
	pm.add_theme_constant_override("margin_top", 10)
	pm.add_theme_constant_override("margin_bottom", 10)
	pity_panel.add_child(pm)

	var pv := VBoxContainer.new()
	pv.add_theme_constant_override("separation", 6)
	pm.add_child(pv)

	_pity_title_label = Label.new()
	_pity_title_label.text = "鍛造連敗保底 0/3 · 滿 3 格釘釘摔錘必成功"
	_pity_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_title_label.add_theme_font_size_override("font_size", 17)
	_pity_title_label.add_theme_color_override("font_color", COLOR_PINK)
	_pity_title_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_pity_title_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_pity_title_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_title_label)

	var bar_row := HBoxContainer.new()
	bar_row.name = "PityBarRow"
	bar_row.alignment = BoxContainer.ALIGNMENT_CENTER
	bar_row.add_theme_constant_override("separation", 10)
	pv.add_child(bar_row)

	_pity_bars.clear()
	for i in range(3):
		var seg := ProgressBar.new()
		seg.min_value = 0
		seg.max_value = 1
		seg.value = 0.0
		seg.custom_minimum_size = Vector2(160, 22)
		seg.show_percentage = false
		var fill_color: Color = COLOR_ORANGE if i < 2 else COLOR_PINK
		_style_dopamine_progress(seg, fill_color, Color("#FFFDF8"))
		bar_row.add_child(seg)
		_pity_bars.append(seg)

	_pity_sub_label = Label.new()
	_pity_sub_label.text = "升階失敗累積 1 格 · 升階成功清空進度"
	_pity_sub_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_pity_sub_label.add_theme_font_size_override("font_size", 16)
	_pity_sub_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_pity_sub_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_pity_sub_label.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_pity_sub_label.add_theme_font_override("font", _cached_font)
	pv.add_child(_pity_sub_label)

	# 訊息回饋
	_msg_label = Label.new()
	_msg_label.text = ""
	_msg_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_msg_label.add_theme_font_size_override("font_size", 16)
	_msg_label.add_theme_color_override("font_color", COLOR_ORANGE)
	_msg_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_msg_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_msg_label.add_theme_font_override("font", _cached_font)
	v.add_child(_msg_label)

	# 動作按鈕列 (按鈕高 >= 50)
	var act_row := HBoxContainer.new()
	act_row.add_theme_constant_override("separation", 16)
	act_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(act_row)

	# 主要按鈕：強化升階 (薄荷綠立體果凍厚底 6px)
	_btn_forge = Button.new()
	_btn_forge.name = "BtnForge"
	_btn_forge.text = "強化升階（消耗 80 金幣）"
	_btn_forge.custom_minimum_size = Vector2(280, 52)
	_btn_forge.add_theme_font_size_override("font_size", 18)
	_btn_forge.add_theme_color_override("font_color", Color.WHITE)
	_btn_forge.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_forge.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_btn_forge.add_theme_font_override("font", _cached_font)
	_btn_forge.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 20, 2))
	_btn_forge.add_theme_stylebox_override("hover", _create_button_style(Color("#68E882"), COLOR_BORDER, 6, 20, 2))
	_btn_forge.add_theme_stylebox_override("pressed", _create_button_style(Color("#3BBF55"), COLOR_BORDER, 2, 20, 2))
	_btn_forge.add_theme_stylebox_override("disabled", _create_button_style(Color("#D0DDD2"), COLOR_BORDER, 3, 20, 2))
	_btn_forge.pressed.connect(_on_forge_pressed)
	act_row.add_child(_btn_forge)

	# 次要按鈕：離開鐵匠鋪 (金黃立體厚底 5px)
	_btn_close = Button.new()
	_btn_close.name = "BtnCloseForge"
	_btn_close.text = "離開鐵匠鋪"
	_btn_close.custom_minimum_size = Vector2(160, 52)
	_btn_close.add_theme_font_size_override("font_size", 18)
	_btn_close.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_btn_close.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_close.add_theme_constant_override("outline_size", 1)
	if _cached_font:
		_btn_close.add_theme_font_override("font", _cached_font)
	_btn_close.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 20, 2))
	_btn_close.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 20, 2))
	_btn_close.add_theme_stylebox_override("pressed", _create_button_style(Color("#E5BA1B"), COLOR_BORDER, 2, 20, 2))
	_btn_close.pressed.connect(_on_close)
	act_row.add_child(_btn_close)


func _create_info_label(parent: Container, text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", 16)
	l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	l.add_theme_color_override("font_outline_color", COLOR_BORDER)
	l.add_theme_constant_override("outline_size", 1)
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
			_msg_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		"no_gold":
			var cost: int = int(res.get("cost", ForgeSystem.forge_cost()))
			_msg_label.text = "金幣不足！升階需要 %d 金幣。" % cost
			_msg_label.add_theme_color_override("font_color", COLOR_PINK)
		"success":
			var scrap_tip := "（消耗鐵屑穩火）" if bool(res.get("used_scrap", false)) else ""
			_msg_label.text = "鍛造成功！升階至第 %d 階，攻擊力上升！%s" % [GameState.weapon_tier, scrap_tip]
			_msg_label.add_theme_color_override("font_color", COLOR_MINT)
		"pity_break":
			_msg_label.text = "鍛造失敗！釘釘摔錘了，吃塊消氣餅回復體力！"
			_msg_label.add_theme_color_override("font_color", COLOR_ORANGE)
		"failed":
			var streak: int = int(res.get("fail_streak", GameState.forge_fail_streak))
			_msg_label.text = "鍛造失敗！累積 1 格保底進度（目前 %d/3 格）。" % streak
			_msg_label.add_theme_color_override("font_color", COLOR_PINK)
	_refresh_display()


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


func _style_dopamine_progress(bar: ProgressBar, fill: Color, bg: Color = Color("#FFFDF8")) -> void:
	var bg_s := StyleBoxFlat.new()
	bg_s.bg_color = bg
	bg_s.border_color = COLOR_BORDER
	bg_s.set_border_width_all(2)
	bg_s.border_width_bottom = 4
	bg_s.set_corner_radius_all(12)

	var fill_s := StyleBoxFlat.new()
	fill_s.bg_color = fill
	fill_s.border_color = COLOR_BORDER
	fill_s.set_border_width_all(1)
	fill_s.border_width_bottom = 2
	fill_s.set_corner_radius_all(10)

	bar.add_theme_stylebox_override("background", bg_s)
	bar.add_theme_stylebox_override("fill", fill_s)
	bar.show_percentage = false
