class_name PowerStatDialog
extends Control
## 《發條之心》大廳頂部戰力屬性總覽彈窗 (PowerStatDialog)
## 依多巴胺鮮亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗規格：寬 720px，黑曜石底色＋多巴胺卡片底，圓角 18px。
## 2. 右上「✕」關閉按鈕尺寸 50x50px，底部按鈕 140x48px（熱區 >= 48px，果凍厚底 5px）。
## 3. 全螢幕半透明遮罩 (Scrim)，點擊遮罩關閉。
## 4. 整合展示：綜合戰力總覽（成長拆解）、基礎六維屬性、三欄武器裝備貢獻、寶石孔位加成與招式心法加成。
## 5. 零系統 Emoji，使用粉圓體 (Open Huninn)。
## 6. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換刷新)。

signal closed()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

static func _t(s: String) -> String:
	var res := ContentLoc.text("ui", s)
	if res != s:
		return res
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_method("t"):
			var loc_t = str(loc.call("t", s))
			if loc_t != "" and loc_t != s:
				return loc_t
	return res

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD         := Color("#FFD028")  ## 金黃
const COLOR_ORANGE       := Color("#FFA010")  ## 暖橘
const COLOR_MINT         := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY          := Color("#38A0FF")  ## 天藍
const COLOR_PINK         := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER       := Color("#1F1A3A")  ## 深藍紫描邊

## ── 底色規範 ──
const COLOR_OBSIDIAN     := Color("#141118")  ## 黑曜石底色
const COLOR_BG_CARD      := Color("#1E1A26")  ## 暗卡片深底
const COLOR_CARD_WARM    := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD    := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_SKY     := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_MINT    := Color("#EAF9EE")  ## 柔和薄荷卡片底
const COLOR_CARD_MUTED   := Color("#EFEBE0")  ## 壓暗奶油底
const COLOR_BORDER_MUTED := Color("#D2CCC0")  ## 壓暗淡邊框

## ── 文字顏色 ──
const COLOR_TEXT_DARK    := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD    := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE  := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MUTED   := Color("#6B6680")  ## 次要輔助文字
const COLOR_TEXT_LIGHT   := Color("#FFFDF8")  ## 奶油白高亮文字
const COLOR_TEXT_DIM     := Color("#888294")  ## 壓暗提示文字

const DIALOG_WIDTH  := 720
const DIALOG_HEIGHT := 520
const CORNER_RADIUS := 18

var _scrim: ColorRect
var _dialog_card: PanelContainer
var _title_lbl: Label
var _sub_title_lbl: Label
var _close_x_btn: Button
var _bottom_close_btn: Button
var _scroll_box: ScrollContainer
var _content_vbox: VBoxContainer

var _cached_font: Font = null
var _built: bool = false


func _enter_tree() -> void:
	_connect_loc_signal()


func _exit_tree() -> void:
	_disconnect_loc_signal()


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and not loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	refresh()


func _ready() -> void:
	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_ui()
	refresh()


func _build_ui() -> void:
	if _built:
		return
	_built = true
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP

	# 1. 全螢幕半透明遮罩 (Scrim)
	_scrim = ColorRect.new()
	_scrim.name = "ModalScrim"
	_scrim.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_scrim.color = Color(0.10, 0.08, 0.14, 0.78)
	_scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	_scrim.gui_input.connect(func(ev: InputEvent):
		if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
			_on_close_pressed()
	)
	add_child(_scrim)

	# 2. 置中黑曜石底色彈窗卡片 (720 x 520)
	var card := PanelContainer.new()
	card.name = "DialogCard"
	card.custom_minimum_size = Vector2(DIALOG_WIDTH, DIALOG_HEIGHT)
	card.set_anchors_preset(Control.PRESET_CENTER)
	card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	card.grow_vertical = Control.GROW_DIRECTION_BOTH
	card.mouse_filter = Control.MOUSE_FILTER_STOP

	var card_sb := StyleBoxFlat.new()
	card_sb.bg_color = COLOR_OBSIDIAN
	card_sb.border_color = Color("#836D38")
	card_sb.set_border_width_all(2)
	card_sb.border_width_bottom = 5
	card_sb.set_corner_radius_all(CORNER_RADIUS)
	card_sb.content_margin_left = 18
	card_sb.content_margin_right = 18
	card_sb.content_margin_top = 14
	card_sb.content_margin_bottom = 14
	card_sb.shadow_color = Color(0.06, 0.04, 0.10, 0.45)
	card_sb.shadow_size = 10
	card_sb.shadow_offset = Vector2(0, 4)
	card.add_theme_stylebox_override("panel", card_sb)
	add_child(card)
	_dialog_card = card

	var root_v := VBoxContainer.new()
	root_v.name = "RootVBox"
	root_v.add_theme_constant_override("separation", 10)
	root_v.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.add_child(root_v)

	# 3. 頂部列（標題 + 副標 + 右上✕）
	var top_h := HBoxContainer.new()
	top_h.name = "TopBar"
	top_h.add_theme_constant_override("separation", 8)
	root_v.add_child(top_h)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.add_theme_constant_override("separation", 2)
	top_h.add_child(title_box)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("戰力屬性總覽")
	_apply_font(_title_lbl, 20, COLOR_TEXT_LIGHT, true)
	_title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_lbl.add_theme_constant_override("outline_size", 3)
	title_box.add_child(_title_lbl)

	_sub_title_lbl = Label.new()
	_sub_title_lbl.name = "SubTitleLabel"
	_sub_title_lbl.text = _t("角色核心數值與裝備流派加成詳情")
	_apply_font(_sub_title_lbl, 13, Color("#C8B99D"))
	title_box.add_child(_sub_title_lbl)

	_close_x_btn = Button.new()
	_close_x_btn.name = "BtnCloseX"
	_close_x_btn.text = "✕"
	_close_x_btn.custom_minimum_size = Vector2(50, 50)
	_style_jelly_btn(_close_x_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 18, 5, 18)
	_close_x_btn.pressed.connect(_on_close_pressed)
	top_h.add_child(_close_x_btn)

	# 4. 可滾動內容容器 (ScrollContainer)
	_scroll_box = ScrollContainer.new()
	_scroll_box.name = "ScrollBox"
	_scroll_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_scroll_box.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root_v.add_child(_scroll_box)

	_content_vbox = VBoxContainer.new()
	_content_vbox.name = "ContentVBox"
	_content_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_content_vbox.add_theme_constant_override("separation", 10)
	_scroll_box.add_child(_content_vbox)

	# 5. 底部按鈕列
	var bottom_h := HBoxContainer.new()
	bottom_h.name = "BottomBar"
	bottom_h.alignment = BoxContainer.ALIGNMENT_CENTER
	root_v.add_child(bottom_h)

	_bottom_close_btn = Button.new()
	_bottom_close_btn.name = "BtnBottomClose"
	_bottom_close_btn.text = _t("關閉")
	_bottom_close_btn.custom_minimum_size = Vector2(140, 48)
	_style_jelly_btn(_bottom_close_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 16, 5, 16)
	_bottom_close_btn.pressed.connect(_on_close_pressed)
	bottom_h.add_child(_bottom_close_btn)


## 重新讀取數值並渲染內容
func refresh() -> void:
	if not _built:
		return

	var gs := _gs()
	var eq := _eq()
	var gem := _gem()
	var sk := _sk()

	# 更新頂部文字
	if _title_lbl:
		_title_lbl.text = _t("戰力屬性總覽")
	if _sub_title_lbl:
		var p_name := str(gs.player_name) if gs and "player_name" in gs else "勇者"
		var p_lv := int(gs.level) if gs and "level" in gs else 1
		var p_path := str(gs.call("path_display")) if gs and gs.has_method("path_display") else ""
		_sub_title_lbl.text = "%s · Lv.%d%s" % [p_name, p_lv, (" · " + p_path) if not p_path.is_empty() else ""]
	if _bottom_close_btn:
		_bottom_close_btn.text = _t("關閉")

	# 清空內容區
	for child in _content_vbox.get_children():
		child.queue_free()

	# 1. 綜合戰力總覽卡片
	_content_vbox.add_child(_build_power_overview_card(gs))

	# 2. 基礎六維屬性卡片
	_content_vbox.add_child(_build_six_stats_card(gs))

	# 3. 三欄武器裝備貢獻卡片
	_content_vbox.add_child(_build_weapon_loadout_card(gs, eq))

	# 4. 寶石孔位與招式心法加成卡片（雙欄）
	_content_vbox.add_child(_build_gem_and_skill_card(gs, gem, sk))


## 綜合戰力總覽卡片
func _build_power_overview_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "PowerOverviewCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 16)
	m.add_child(h)

	# 左側大號戰力徽章
	var pow_box := PanelContainer.new()
	pow_box.name = "PowerBadge"
	pow_box.custom_minimum_size = Vector2(140, 72)
	pow_box.add_theme_stylebox_override("panel", _create_card_style(COLOR_OBSIDIAN, Color("#D4AF37"), 2, 3, 12))
	var pv := VBoxContainer.new()
	pv.alignment = BoxContainer.ALIGNMENT_CENTER
	pv.add_theme_constant_override("separation", 2)
	pow_box.add_child(pv)

	var p_title := Label.new()
	p_title.text = _t("綜合戰力")
	p_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(p_title, 12, Color("#E5C158"))
	pv.add_child(p_title)

	var total_pow: int = int(gs.call("power_score")) if gs and gs.has_method("power_score") else 0
	var p_val := Label.new()
	p_val.name = "TotalPowerValue"
	p_val.text = str(total_pow)
	p_val.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(p_val, 26, COLOR_GOLD, true)
	p_val.add_theme_color_override("font_outline_color", COLOR_BORDER)
	p_val.add_theme_constant_override("outline_size", 3)
	pv.add_child(p_val)
	h.add_child(pow_box)

	# 右側戰力拆解說明
	var v_breakdown := VBoxContainer.new()
	v_breakdown.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v_breakdown.alignment = BoxContainer.ALIGNMENT_CENTER
	v_breakdown.add_theme_constant_override("separation", 4)
	h.add_child(v_breakdown)

	var b_title := Label.new()
	b_title.text = _t("戰力成長拆解")
	_apply_font(b_title, 13, COLOR_TEXT_DARK, true)
	v_breakdown.add_child(b_title)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 2)
	v_breakdown.add_child(grid)

	var lv: int = int(gs.level) if gs and "level" in gs else 1
	var w_tier: int = int(gs.weapon_tier) if gs and "weapon_tier" in gs else 1
	var e_atk: int = int(gs.call("effective_atk")) if gs and gs.has_method("effective_atk") else 0
	var e_def: int = int(gs.call("effective_def")) if gs and gs.has_method("effective_def") else 0
	var e_crit: float = float(gs.call("effective_crit")) if gs and gs.has_method("effective_crit") else 0.0
	var has_path: bool = (str(gs.path_style) != "") if gs and "path_style" in gs else false

	_add_breakdown_item(grid, _t("等級成長"), "+%d" % (lv * 3))
	_add_breakdown_item(grid, _t("武器階數"), "+%d" % (w_tier * 4))
	_add_breakdown_item(grid, _t("攻防加成"), "+%d" % (e_atk + e_def))
	_add_breakdown_item(grid, _t("暴擊折算"), "+%d" % int(e_crit / 2.0))
	_add_breakdown_item(grid, _t("流派心法"), "+%d" % (2 if has_path else 0))

	return card


func _add_breakdown_item(parent: Container, label_text: String, val_text: String) -> void:
	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 4)
	var l := Label.new()
	l.text = label_text + ":"
	_apply_font(l, 12, COLOR_TEXT_MUTED)
	h.add_child(l)
	var v := Label.new()
	v.text = val_text
	_apply_font(v, 12, COLOR_TEXT_ORANGE, true)
	h.add_child(v)
	parent.add_child(h)


## 基礎六維屬性卡片
func _build_six_stats_card(gs: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "SixStatsCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_SKY, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	var t := Label.new()
	t.text = _t("基礎六維屬性")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	v.add_child(t)

	var grid := GridContainer.new()
	grid.columns = 3
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 10)
	grid.add_theme_constant_override("v_separation", 8)
	v.add_child(grid)

	var cur_hp: int = int(gs.call("effective_max_hp")) if gs and gs.has_method("effective_max_hp") else 100
	var base_hp: int = int(gs.max_hp) if gs and "max_hp" in gs else 100

	var cur_atk: int = int(gs.call("effective_atk")) if gs and gs.has_method("effective_atk") else 10
	var base_atk: int = int(gs.atk) if gs and "atk" in gs else 10

	var cur_def: int = int(gs.call("effective_def")) if gs and gs.has_method("effective_def") else 5
	var base_def: int = int(gs.def_stat) if gs and "def_stat" in gs else 5

	var cur_crit: float = float(gs.call("effective_crit")) if gs and gs.has_method("effective_crit") else 5.0
	var base_crit: float = float(gs.crit_rate) if gs and "crit_rate" in gs else 5.0

	var cur_spd: int = int(gs.call("effective_speed")) if gs and gs.has_method("effective_speed") else 10
	var base_spd: int = int(gs.speed) if gs and "speed" in gs else 10

	var cur_cdmg: float = float(gs.call("effective_crit_dmg")) if gs and gs.has_method("effective_crit_dmg") else 150.0
	var base_cdmg: float = float(gs.crit_dmg) if gs and "crit_dmg" in gs else 150.0

	grid.add_child(_create_stat_cell("Stat_HP", _t("生命力"), str(cur_hp), "(+%d)" % maxi(0, cur_hp - base_hp), Color("#0E8A7A")))
	grid.add_child(_create_stat_cell("Stat_ATK", _t("物理攻擊"), str(cur_atk), "(+%d)" % maxi(0, cur_atk - base_atk), COLOR_TEXT_ORANGE))
	grid.add_child(_create_stat_cell("Stat_DEF", _t("物理防禦"), str(cur_def), "(+%d)" % maxi(0, cur_def - base_def), Color("#2A5580")))
	grid.add_child(_create_stat_cell("Stat_CRIT", _t("暴擊率"), "%.1f%%" % cur_crit, "(+%.1f%%)" % maxf(0.0, cur_crit - base_crit), Color("#B83250")))
	grid.add_child(_create_stat_cell("Stat_SPD", _t("出手速度"), str(cur_spd), "(+%d)" % maxi(0, cur_spd - base_spd), Color("#3E7E1E")))
	grid.add_child(_create_stat_cell("Stat_CDMG", _t("暴擊傷害"), "%.0f%%" % cur_cdmg, "(+%.0f%%)" % maxf(0.0, cur_cdmg - base_cdmg), Color("#8B2A90")))

	return card


func _create_stat_cell(cell_name: String, label_str: String, val_str: String, extra_str: String, color_accent: Color) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = cell_name
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(0, 48)

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 10
	sb.content_margin_right = 10
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	c.add_theme_stylebox_override("panel", sb)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 6)
	c.add_child(h)

	var lbl := Label.new()
	lbl.text = label_str
	_apply_font(lbl, 13, COLOR_TEXT_DARK, true)
	h.add_child(lbl)

	var val_lbl := Label.new()
	val_lbl.name = "ValueLabel"
	val_lbl.text = val_str
	_apply_font(val_lbl, 16, color_accent, true)
	h.add_child(val_lbl)

	if not extra_str.is_empty() and extra_str != "(+0)" and extra_str != "(+0.0%)":
		var ext_lbl := Label.new()
		ext_lbl.text = extra_str
		_apply_font(ext_lbl, 11, COLOR_TEXT_MUTED)
		h.add_child(ext_lbl)

	return c


## 三欄武器裝備貢獻卡片
func _build_weapon_loadout_card(gs: Node, eq: Node) -> PanelContainer:
	var card := PanelContainer.new()
	card.name = "WeaponLoadoutCard"
	card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 14))

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 14)
	m.add_theme_constant_override("margin_right", 14)
	m.add_theme_constant_override("margin_top", 10)
	m.add_theme_constant_override("margin_bottom", 10)
	card.add_child(m)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 8)
	m.add_child(v)

	var t_row := HBoxContainer.new()
	v.add_child(t_row)

	var t := Label.new()
	t.text = _t("三欄武器裝備貢獻")
	_apply_font(t, 14, COLOR_TEXT_DARK, true)
	t_row.add_child(t)

	var eq_bonus: Dictionary = {}
	if eq and eq.has_method("bonus_totals"):
		eq_bonus = eq.call("bonus_totals") as Dictionary

	var b_atk := int(eq_bonus.get("atk", 0))
	var b_def := int(eq_bonus.get("def", 0))
	var b_hp := int(eq_bonus.get("hp", 0))
	var b_crit := float(eq_bonus.get("crit", 0.0))

	var summary_lbl := Label.new()
	summary_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	summary_lbl.text = _t("裝備總加成: 攻+%d · 防+%d · 血+%d · 暴+%.1f%%") % [b_atk, b_def, b_hp, b_crit]
	_apply_font(summary_lbl, 12, COLOR_TEXT_GOLD, true)
	t_row.add_child(summary_lbl)

	# 三槽武器卡片列
	var slots_h := HBoxContainer.new()
	slots_h.add_theme_constant_override("separation", 10)
	v.add_child(slots_h)

	var slot_titles: Array[String] = [
		_t("首選武器"),
		_t("副手武器"),
		_t("絕技武器")
	]

	for i in range(3):
		slots_h.add_child(_create_slot_card(i, slot_titles[i], eq))

	return card


func _create_slot_card(slot_idx: int, slot_title: String, eq: Node) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "SlotCard_%d" % slot_idx
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_GOLD if slot_idx == 0 else COLOR_CARD_SKY
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(10)
	sb.content_margin_left = 8
	sb.content_margin_right = 8
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	c.add_theme_stylebox_override("panel", sb)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	c.add_child(v)

	var t := Label.new()
	t.text = slot_title
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(t, 12, COLOR_TEXT_MUTED)
	v.add_child(t)

	var is_unlocked := true
	if eq and eq.has_method("loadout_slot_unlocked"):
		is_unlocked = bool(eq.call("loadout_slot_unlocked", slot_idx))

	if not is_unlocked:
		var unlock_lv := 10 if slot_idx == 1 else 20
		var lock_lbl := Label.new()
		lock_lbl.text = _t("Lv.%d 解鎖" % unlock_lv)
		lock_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_apply_font(lock_lbl, 13, COLOR_TEXT_DIM)
		v.add_child(lock_lbl)
		return c

	var uid := ""
	if eq and eq.has_method("loadout_uid"):
		uid = str(eq.call("loadout_uid", slot_idx))

	if uid.is_empty():
		var empty_lbl := Label.new()
		empty_lbl.text = _t("未裝備")
		empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		_apply_font(empty_lbl, 13, COLOR_TEXT_DIM)
		v.add_child(empty_lbl)
		return c

	var inst: Dictionary = {}
	if eq and eq.has_method("weapon_inst"):
		inst = eq.call("weapon_inst", uid) as Dictionary

	var w_name := str(inst.get("name", "武器"))
	var w_atk := int(inst.get("atk", 0))
	var w_tier := int(inst.get("tier", 1))

	var name_lbl := Label.new()
	name_lbl.text = _t(w_name)
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(name_lbl, 14, COLOR_TEXT_DARK, true)
	v.add_child(name_lbl)

	var stat_lbl := Label.new()
	stat_lbl.text = _t("T%d · 攻 +%d") % [w_tier, w_atk]
	stat_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_font(stat_lbl, 12, COLOR_TEXT_ORANGE)
	v.add_child(stat_lbl)

	return c


## 寶石孔位與招式心法加成卡片（雙欄）
func _build_gem_and_skill_card(gs: Node, gem: Node, sk: Node) -> HBoxContainer:
	var h := HBoxContainer.new()
	h.name = "GemAndSkillRow"
	h.add_theme_constant_override("separation", 10)

	# 寶石孔位卡片
	var gem_card := PanelContainer.new()
	gem_card.name = "GemBonusCard"
	gem_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	gem_card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_MINT, COLOR_BORDER, 2, 4, 14))
	h.add_child(gem_card)

	var gm := MarginContainer.new()
	gm.add_theme_constant_override("margin_left", 12)
	gm.add_theme_constant_override("margin_right", 12)
	gm.add_theme_constant_override("margin_top", 8)
	gm.add_theme_constant_override("margin_bottom", 8)
	gem_card.add_child(gm)

	var gv := VBoxContainer.new()
	gv.add_theme_constant_override("separation", 4)
	gm.add_child(gv)

	var gt := Label.new()
	gt.text = _t("寶石孔位加成")
	_apply_font(gt, 13, COLOR_TEXT_DARK, true)
	gv.add_child(gt)

	var worn_b: Dictionary = {}
	if gem and gem.has_method("worn_bonuses"):
		worn_b = gem.call("worn_bonuses") as Dictionary

	var g_atk_pct := float(worn_b.get("atk_pct", 0.0)) * 100.0
	var g_def_pct := float(worn_b.get("def_pct", 0.0)) * 100.0
	var g_hp_pct  := float(worn_b.get("hp_pct", 0.0)) * 100.0
	var g_crit    := float(worn_b.get("crit", 0.0))
	var g_hit     := float(worn_b.get("hit", 0.0))
	var g_eva     := float(worn_b.get("eva", 0.0))

	var b_list: Array[String] = []
	if g_atk_pct > 0.01:
		b_list.append("攻 +%.1f%%" % g_atk_pct)
	if g_def_pct > 0.01:
		b_list.append("防 +%.1f%%" % g_def_pct)
	if g_hp_pct > 0.01:
		b_list.append("血 +%.1f%%" % g_hp_pct)
	if g_crit > 0.01:
		b_list.append("暴 +%.1f%%" % g_crit)
	if g_hit > 0.01:
		b_list.append("命中 +%.0f" % g_hit)
	if g_eva > 0.01:
		b_list.append("閃避 +%.0f" % g_eva)

	var g_desc := Label.new()
	if b_list.is_empty():
		g_desc.text = _t("尚未鑲嵌寶石")
		_apply_font(g_desc, 12, COLOR_TEXT_DIM)
	else:
		g_desc.text = " · ".join(b_list)
		_apply_font(g_desc, 12, Color("#1E7538"), true)
	gv.add_child(g_desc)

	# 招式心法卡片
	var sk_card := PanelContainer.new()
	sk_card.name = "SkillBonusCard"
	sk_card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sk_card.add_theme_stylebox_override("panel", _create_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 14))
	h.add_child(sk_card)

	var sm := MarginContainer.new()
	sm.add_theme_constant_override("margin_left", 12)
	sm.add_theme_constant_override("margin_right", 12)
	sm.add_theme_constant_override("margin_top", 8)
	sm.add_theme_constant_override("margin_bottom", 8)
	sk_card.add_child(sm)

	var sv := VBoxContainer.new()
	sv.add_theme_constant_override("separation", 4)
	sm.add_child(sv)

	var st := Label.new()
	st.text = _t("招式心法加成")
	_apply_font(st, 13, COLOR_TEXT_DARK, true)
	sv.add_child(st)

	var patch: Dictionary = {}
	if sk and sk.has_method("battle_player_stats_patch"):
		patch = sk.call("battle_player_stats_patch") as Dictionary

	var sk_name: String = str(patch.get("skill_name", ""))
	var sk_mult: float = float(patch.get("skill_mult", 1.8))
	var sk_hits: int = int(patch.get("skill_hits", 1))

	var sk_desc := Label.new()
	if sk_name.is_empty():
		sk_desc.text = _t("未裝備招式心法")
		_apply_font(sk_desc, 12, COLOR_TEXT_DIM)
	else:
		sk_desc.text = "%s (%s: %.1fx · %s: %d)" % [sk_name, _t("傷害倍率"), sk_mult, _t("連擊段數"), sk_hits]
		_apply_font(sk_desc, 12, COLOR_TEXT_ORANGE, true)
	sv.add_child(sk_desc)

	return h


func _on_close_pressed() -> void:
	closed.emit()
	queue_free()


func _create_card_style(bg: Color, border: Color, b_width: int = 1, b_bottom: int = 3, radius: int = 12) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(b_width)
	sb.border_width_bottom = b_bottom
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)
	return sb


func _style_jelly_btn(btn: Button, bg: Color, text_col: Color, font_sz: int, bottom_px: int = 5, radius: int = 16, border_col: Color = COLOR_BORDER) -> void:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border_col
	sb.set_border_width_all(2)
	sb.border_width_bottom = bottom_px
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	if bottom_px > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = bg.lightened(0.1)

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = maxi(2, bottom_px - 3)

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)
	btn.add_theme_stylebox_override("disabled", sb)

	_apply_font(btn, font_sz, text_col, true)


func _apply_font(node: Control, sz: int, color: Color = COLOR_TEXT_DARK, bold: bool = false) -> void:
	if _cached_font:
		node.add_theme_font_override("font", _cached_font)
	node.add_theme_font_size_override("font_size", sz)
	if node is Label:
		node.add_theme_color_override("font_color", color)
	elif node is Button:
		node.add_theme_color_override("font_color", color)
		node.add_theme_color_override("font_hover_color", color)
		node.add_theme_color_override("font_pressed_color", color)
		node.add_theme_color_override("font_disabled_color", COLOR_TEXT_DIM)


func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


func _eq() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	return null


func _gem() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("GemSystem")
	return null


func _sk() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("SkillSystem")
	return null
