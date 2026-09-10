class_name MapleHud
extends Control
## 據點狀態板：陽光童話·多巴胺亮色盤（奶油白底 · 糖果三條 · 深藍紫立體描邊）

## battle_view 每幀用這個群組把戰鬥單位的 HP 推回畫面
const VITALS_GROUP := "hud_vitals"

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const WindowDrag = preload("res://scripts/ui/window_drag.gd")
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
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字

var _panel: PanelContainer
var _name_l: Label
var _lv_l: Label
var _hp_bar: ProgressBar
var _mp_bar: ProgressBar
var _exp_bar: ProgressBar
var _hp_val: Label
var _gold_l: Label
var _tip_l: Label
var _acc_row: HBoxContainer
var _acc_cells: Array = []
var _drag_handle: Control
var _cached_font: Font = null


func _get_font() -> Font:
	if _cached_font == null and ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	return _cached_font


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 5, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 10
	sb.content_margin_bottom = 12
	return sb


func _style_progress_bar(bar: ProgressBar, fill: Color, bg: Color, radius: int = 10) -> void:
	var bg_s := StyleBoxFlat.new()
	bg_s.bg_color = bg
	bg_s.border_color = COLOR_BORDER
	bg_s.set_border_width_all(2)
	bg_s.border_width_bottom = 3
	bg_s.set_corner_radius_all(radius)

	var fill_s := StyleBoxFlat.new()
	fill_s.bg_color = fill
	fill_s.border_color = COLOR_BORDER
	fill_s.set_border_width_all(1)
	fill_s.border_width_bottom = 2
	fill_s.set_corner_radius_all(maxi(2, radius - 2))

	bar.add_theme_stylebox_override("background", bg_s)
	bar.add_theme_stylebox_override("fill", fill_s)
	bar.show_percentage = false


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_anchors_preset(Control.PRESET_TOP_LEFT)
	anchor_right = 0
	anchor_bottom = 0
	var m := ResponsiveUi.safe_margin(self)
	position = Vector2(m.x, m.y)
	size = Vector2(300, 220)
	custom_minimum_size = Vector2(300, 220)
	_build()
	## 戰鬥中 HP 由 BattleSim 的戰鬥單位當權威，變動不經過任何訊號。
	## 加進群組讓 battle_view 每幀推一次，兩條血條才不會各說各話。
	add_to_group(VITALS_GROUP)
	WindowDrag.attach(self, _drag_handle, "hud")
	call_deferred("_restore_layout")


func _restore_layout() -> void:
	if Engine.get_main_loop() is SceneTree:
		var ul: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("UiLayout")
		if ul and ul.has_method("apply_to"):
			var m := ResponsiveUi.safe_margin(self)
			ul.call("apply_to", self, "hud", Vector2(m.x, m.y))


func _build() -> void:
	var f := _get_font()

	_panel = PanelContainer.new()
	_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 2, 5, 20))
	add_child(_panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 6)
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_panel.add_child(v)

	## 標題列 / 拖曳把手
	_drag_handle = PanelContainer.new()
	_drag_handle.mouse_filter = Control.MOUSE_FILTER_STOP
	var hb_s := StyleBoxFlat.new()
	hb_s.bg_color = COLOR_CARD_WARM
	hb_s.border_color = COLOR_BORDER
	hb_s.set_border_width_all(2)
	hb_s.border_width_bottom = 3
	hb_s.set_corner_radius_all(14)
	hb_s.content_margin_left = 10
	hb_s.content_margin_right = 10
	hb_s.content_margin_top = 4
	hb_s.content_margin_bottom = 6
	_drag_handle.add_theme_stylebox_override("panel", hb_s)
	v.add_child(_drag_handle)

	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 8)
	row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_drag_handle.add_child(row)

	_lv_l = Label.new()
	_lv_l.add_theme_font_size_override("font_size", 16)
	_lv_l.add_theme_color_override("font_color", COLOR_ORANGE)
	_lv_l.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_lv_l.add_theme_constant_override("outline_size", 3)
	if f:
		_lv_l.add_theme_font_override("font", f)
	_lv_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(_lv_l)

	_name_l = Label.new()
	_name_l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_name_l.add_theme_font_size_override("font_size", 16)
	_name_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_name_l.add_theme_color_override("font_outline_color", COLOR_BG_CREAM)
	_name_l.add_theme_constant_override("outline_size", 2)
	if f:
		_name_l.add_theme_font_override("font", f)
	_name_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(_name_l)

	var drag_hint := Label.new()
	drag_hint.text = "⠿"
	drag_hint.add_theme_font_size_override("font_size", 16)
	drag_hint.add_theme_color_override("font_color", COLOR_ORANGE)
	drag_hint.add_theme_color_override("font_outline_color", COLOR_BORDER)
	drag_hint.add_theme_constant_override("outline_size", 2)
	if f:
		drag_hint.add_theme_font_override("font", f)
	drag_hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(drag_hint)

	# HP Bar (奶油白槽底 + 深藍紫描邊 + 珊瑚粉填充條)
	_hp_bar = _make_bar(24)
	_style_progress_bar(_hp_bar, COLOR_PINK, COLOR_BG_CREAM, 10)
	v.add_child(_hp_bar)

	_hp_val = Label.new()
	_hp_val.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_hp_val.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hp_val.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_hp_val.add_theme_font_size_override("font_size", 16)
	_hp_val.add_theme_color_override("font_color", Color.WHITE)
	_hp_val.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_hp_val.add_theme_constant_override("outline_size", 4)
	if f:
		_hp_val.add_theme_font_override("font", f)
	_hp_val.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hp_bar.add_child(_hp_val)

	# MP Bar / Stardust (奶油白槽底 + 深藍紫描邊 + 天藍填充條)
	_mp_bar = _make_bar(18)
	_style_progress_bar(_mp_bar, COLOR_SKY, COLOR_BG_CREAM, 8)
	v.add_child(_mp_bar)

	# EXP Bar (奶油白槽底 + 深藍紫描邊 + 金黃填充條)
	_exp_bar = _make_bar(14)
	_style_progress_bar(_exp_bar, COLOR_GOLD, COLOR_BG_CREAM, 6)
	v.add_child(_exp_bar)

	# Gold / Energy / Power Label
	_gold_l = Label.new()
	_gold_l.add_theme_font_size_override("font_size", 16)
	_gold_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_gold_l.add_theme_color_override("font_outline_color", COLOR_BG_CREAM)
	_gold_l.add_theme_constant_override("outline_size", 2)
	if f:
		_gold_l.add_theme_font_override("font", f)
	_gold_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(_gold_l)

	# Accessory Slots
	_acc_row = HBoxContainer.new()
	_acc_row.add_theme_constant_override("separation", 6)
	_acc_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(_acc_row)
	_acc_cells.clear()
	for i in 6:
		var slot_box := PanelContainer.new()
		slot_box.custom_minimum_size = Vector2(28, 28)
		var ssb := StyleBoxFlat.new()
		ssb.bg_color = COLOR_CARD_WARM
		ssb.border_color = COLOR_BORDER
		ssb.set_border_width_all(1)
		ssb.border_width_bottom = 2
		ssb.set_corner_radius_all(6)
		slot_box.add_theme_stylebox_override("panel", ssb)
		slot_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_acc_row.add_child(slot_box)

		var cell := TextureRect.new()
		cell.set_anchors_preset(Control.PRESET_FULL_RECT)
		cell.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		cell.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		cell.mouse_filter = Control.MOUSE_FILTER_IGNORE
		slot_box.add_child(cell)
		_acc_cells.append(cell)

	# Tip Label
	_tip_l = Label.new()
	_tip_l.add_theme_font_size_override("font_size", 16)
	_tip_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_tip_l.add_theme_color_override("font_outline_color", COLOR_BG_CREAM)
	_tip_l.add_theme_constant_override("outline_size", 2)
	if f:
		_tip_l.add_theme_font_override("font", f)
	_tip_l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_child(_tip_l)


func _make_bar(h: float = 10) -> ProgressBar:
	var b := ProgressBar.new()
	b.custom_minimum_size = Vector2(0, h)
	b.max_value = 100
	b.value = 100
	b.show_percentage = false
	b.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return b


## 只更新三條量條。可以每幀呼叫 —— 刻意不碰下面那行金幣／待領，
## 因為 claimable_count() 會把所有里程碑跑一遍，不是每幀該做的事。
func refresh_vitals() -> void:
	if not is_inside_tree() or _hp_bar == null:
		return
	var max_hp: int = GameState.effective_max_hp()
	var hp: int = mini(GameState.hp, max_hp)
	_hp_bar.max_value = maxi(1, max_hp)
	_hp_bar.value = hp
	_hp_bar.tooltip_text = "HP %d / %d" % [hp, max_hp]
	if _hp_val:
		_hp_val.text = "%d / %d" % [hp, max_hp]

	var dust: int = int(GameState.stardust)
	var dust_cap: int = maxi(30, dust)
	_mp_bar.max_value = dust_cap
	_mp_bar.value = dust
	_mp_bar.tooltip_text = Loc.t("hud.stardust", {"n": dust})

	var need_xp: int = maxi(1, GameState.xp_to_next())
	_exp_bar.max_value = 100
	_exp_bar.value = clampf(float(GameState.xp) / float(need_xp) * 100.0, 0.0, 100.0)
	_exp_bar.tooltip_text = Loc.t("hud.xp", {"cur": GameState.xp, "need": need_xp})


func refresh() -> void:
	if not is_inside_tree():
		return
	var name_s := str(GameState.player_name)
	if name_s == "":
		name_s = Loc.t("hud.default_name")
	var lv_real: int = maxi(1, int(GameState.level))
	_lv_l.text = Loc.t("common.level", {"n": lv_real})
	_name_l.text = name_s

	refresh_vitals()

	## 紅點優先顯示「今日可領」（簽到／委託），不含長遠里程碑
	var claim := 0
	if Engine.get_main_loop() is SceneTree:
		var q: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("QuestSystem")
		if q and q.has_method("starpath_reward_count"):
			claim = int(q.call("starpath_reward_count"))
		elif q and q.has_method("claimable_count"):
			claim = int(q.call("claimable_count"))
	var claim_s := Loc.t("hud.claim", {"n": claim}) if claim > 0 else ""
	var week := Loc.t("pause.week1")
	var es: Node = null
	if Engine.get_main_loop() is SceneTree:
		es = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EnergySystem")
	var energy_s := ""
	if es and es.has_method("current"):
		energy_s = Loc.t("hud.energy", {
			"cur": int(es.call("current")),
			"max": int(es.get("MAX_ENERGY")) if es.get("MAX_ENERGY") != null else 15,
		})
	_gold_l.text = Loc.t("hud.gold_power", {
		"gold": GameState.gold, "pow": GameState.power_score(), "week": week, "claim": claim_s,
	})
	if energy_s != "":
		_gold_l.text += " · " + energy_s
	_gold_l.tooltip_text = _gold_l.text + (claim_s if claim_s != "" else "")
	_refresh_acc_row()

	var path_s := GameState.path_display() if GameState.path_style != "" else Loc.t("hud.no_path")
	_tip_l.text = Loc.t("hud.tip", {"weapon": GameState.weapon_display(), "path": path_s})
	## 三條量條都是 MOUSE_FILTER_IGNORE，各自的 tooltip 永遠不會冒出來；
	## 星屑條、經驗條又沒有字，玩家只看得到兩條空槽。整塊板的 tooltip 一次把
	## HP／星屑／經驗／能量列齊，滑過去就有答案。
	_panel.tooltip_text = "\n".join(PackedStringArray([
		_hp_bar.tooltip_text, _mp_bar.tooltip_text, _exp_bar.tooltip_text,
		_gold_l.tooltip_text,
	]))


func _refresh_acc_row() -> void:
	if _acc_cells.is_empty():
		return
	var unlocked := false
	if Engine.get_main_loop() is SceneTree:
		var eq: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq and eq.has_method("accessories_unlocked"):
			unlocked = bool(eq.call("accessories_unlocked"))
	var slots: Array[String] = ["ring", "necklace", "bracelet", "earring", "amulet", "belt"]
	for i in _acc_cells.size():
		var cell: TextureRect = _acc_cells[i]
		cell.modulate = Color(0.45, 0.45, 0.5, 0.7) if not unlocked else Color.WHITE
		cell.texture = null
		if not unlocked or i >= slots.size():
			continue
		var slot := slots[i]
		var uid := str(GameState.equip_slots.get(slot, ""))
		if uid == "" or not GameState.equip_worn.has(uid):
			continue
		var inst: Dictionary = GameState.equip_worn[uid]
		cell.texture = SpriteDB.equip_icon_for_inst(inst)
		cell.modulate = Color.WHITE
