class_name BattleVictoryDialog
extends Control
## 《發條之心》戰鬥勝利結算卡片 (BattleVictoryDialog)
## 遵循多巴胺鮮亮色盤與手遊人體工學規範：
## 1. 橫屏彈窗寬 750px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，按鈕高度均 >= 50px（熱區 >= 48px）。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底色 #FFFDF8。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 14~28px 加粗帶深色厚描邊，零小字。
## 6. 零系統 emoji、零開發用語。
## 7. 支援 Loc.locale_changed 即時切換六語系。

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
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃卡片底
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_MUTED  := Color("#7A6E8A")  ## 輔助標籤灰紫

var _dialog_card: PanelContainer
var _title_lbl: Label
var _sub_lbl: Label
var _slot_icon: TextureRect
var _slot_name_lbl: Label
var _tier_lbl: Label
var _stats_lbl: Label
var _desc_lbl: Label
var _btn_equip: Button
var _btn_confirm: Button
var _btn_close: Button
var _cached_font: Font = null

var _part: Dictionary = {}
var _on_confirm: Callable = Callable()
var _is_equipped: bool = false


static func show_dialog(parent: Node, part: Dictionary = {}, on_confirm: Callable = Callable()) -> Control:
	var dlg = load("res://scripts/battle/battle_victory_dialog.gd").new()
	dlg.setup(part, on_confirm)
	parent.add_child(dlg)
	return dlg


func setup(part: Dictionary = {}, on_confirm: Callable = Callable()) -> void:
	_part = part.duplicate(true)
	_on_confirm = on_confirm
	if _dialog_card == null:
		_build_ui()
	_refresh_display()


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 100
	_build_ui()
	_refresh_display()

	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.is_connected("locale_changed", Callable(self, "_on_locale_changed")):
				loc.connect("locale_changed", Callable(self, "_on_locale_changed"))


func _exit_tree() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.is_connected("locale_changed", Callable(self, "_on_locale_changed")):
			loc.disconnect("locale_changed", Callable(self, "_on_locale_changed"))


func _on_locale_changed(_new_loc: String = "") -> void:
	_refresh_display()


func _build_ui() -> void:
	if _dialog_card != null:
		return

	if ResourceLoader.exists(FONT_PATH) and _cached_font == null:
		_cached_font = load(FONT_PATH) as Font

	# 1. 全螢幕半透明遮罩 (Scrim)
	var scrim := ResponsiveUi.make_scrim(Color(0.05, 0.04, 0.08, 0.45))
	add_child(scrim)

	# 2. 置中容器
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	# 3. 彈窗主卡片 (寬 750px，奶油米白底，深藍紫描邊)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "VictoryCard"
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
	v.add_theme_constant_override("separation", 12)
	margin.add_child(v)

	# ── 標題列 + 關閉按鈕 ──
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_col := VBoxContainer.new()
	title_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_col.add_theme_constant_override("separation", 2)
	head.add_child(title_col)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_title_lbl.text = _t("戰鬥勝利")
	_title_lbl.add_theme_font_size_override("font_size", 24)
	_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_title_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_title_lbl)

	_sub_lbl = Label.new()
	_sub_lbl.name = "SubtitleLabel"
	_sub_lbl.text = _t("關卡討伐成功！獲得戰利品機芯部件")
	_sub_lbl.add_theme_font_size_override("font_size", 13)
	_sub_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_sub_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_sub_lbl)

	# 右上角關閉按鈕 (尺寸 >= 50px，熱區 >= 48px)
	_btn_close = _create_close_button()
	_btn_close.name = "CloseButton"
	_btn_close.pressed.connect(_on_confirm_pressed)
	head.add_child(_btn_close)

	# ── 機芯掉落展示卡 (CorePartDropCard) ──
	var drop_panel := PanelContainer.new()
	drop_panel.name = "CorePartDropCard"
	drop_panel.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 18))
	v.add_child(drop_panel)

	var drop_margin := MarginContainer.new()
	drop_margin.add_theme_constant_override("margin_left", 20)
	drop_margin.add_theme_constant_override("margin_right", 20)
	drop_margin.add_theme_constant_override("margin_top", 16)
	drop_margin.add_theme_constant_override("margin_bottom", 16)
	drop_panel.add_child(drop_margin)

	var drop_row := HBoxContainer.new()
	drop_row.add_theme_constant_override("separation", 20)
	drop_row.alignment = BoxContainer.ALIGNMENT_CENTER
	drop_margin.add_child(drop_row)

	# 圖示外框
	var icon_box := PanelContainer.new()
	icon_box.custom_minimum_size = Vector2(88, 88)
	var icon_st := StyleBoxFlat.new()
	icon_st.bg_color = Color(0.96, 0.95, 0.98, 1)
	icon_st.border_color = COLOR_BORDER
	icon_st.set_border_width_all(2)
	icon_st.set_corner_radius_all(14)
	icon_box.add_theme_stylebox_override("panel", icon_st)
	drop_row.add_child(icon_box)

	_slot_icon = TextureRect.new()
	_slot_icon.name = "SlotIcon"
	_slot_icon.custom_minimum_size = Vector2(72, 72)
	_slot_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_slot_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_slot_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_slot_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	icon_box.add_child(_slot_icon)

	# 資訊列
	var info_col := VBoxContainer.new()
	info_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info_col.add_theme_constant_override("separation", 4)
	drop_row.add_child(info_col)

	var name_tier_row := HBoxContainer.new()
	name_tier_row.add_theme_constant_override("separation", 10)
	info_col.add_child(name_tier_row)

	_slot_name_lbl = Label.new()
	_slot_name_lbl.name = "SlotNameLabel"
	_slot_name_lbl.text = "發條發電機"
	_slot_name_lbl.add_theme_font_size_override("font_size", 18)
	_slot_name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_slot_name_lbl.add_theme_font_override("font", _cached_font)
	name_tier_row.add_child(_slot_name_lbl)

	_tier_lbl = Label.new()
	_tier_lbl.name = "TierLabel"
	_tier_lbl.text = "【白階】"
	_tier_lbl.add_theme_font_size_override("font_size", 16)
	_tier_lbl.add_theme_color_override("font_color", COLOR_GOLD)
	if _cached_font:
		_tier_lbl.add_theme_font_override("font", _cached_font)
	name_tier_row.add_child(_tier_lbl)

	_stats_lbl = Label.new()
	_stats_lbl.name = "StatsLabel"
	_stats_lbl.text = "攻+10 · 血+30"
	_stats_lbl.add_theme_font_size_override("font_size", 14)
	_stats_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_stats_lbl.add_theme_font_override("font", _cached_font)
	info_col.add_child(_stats_lbl)

	_desc_lbl = Label.new()
	_desc_lbl.name = "DescLabel"
	_desc_lbl.text = _t("可校準 7 次 · 安全彈簧保護不碎裝")
	_desc_lbl.add_theme_font_size_override("font_size", 12)
	_desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_desc_lbl.add_theme_font_override("font", _cached_font)
	info_col.add_child(_desc_lbl)

	# ── 底部按鈕區（橫屏雙拇指操作，高度 >= 50px）──
	var btn_row := HBoxContainer.new()
	btn_row.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_row.add_theme_constant_override("separation", 16)
	v.add_child(btn_row)

	_btn_equip = Button.new()
	_btn_equip.name = "BtnEquip"
	_btn_equip.text = _t("立即裝備")
	_btn_equip.custom_minimum_size = Vector2(200, 52)
	_btn_equip.focus_mode = Control.FOCUS_NONE
	_style_button(_btn_equip, COLOR_SKY, COLOR_BORDER)
	_btn_equip.pressed.connect(_on_equip_pressed)
	btn_row.add_child(_btn_equip)

	_btn_confirm = Button.new()
	_btn_confirm.name = "BtnConfirm"
	_btn_confirm.text = _t("收下完成")
	_btn_confirm.custom_minimum_size = Vector2(200, 52)
	_btn_confirm.focus_mode = Control.FOCUS_NONE
	_style_button(_btn_confirm, COLOR_GOLD, COLOR_BORDER)
	_btn_confirm.pressed.connect(_on_confirm_pressed)
	btn_row.add_child(_btn_confirm)


func _refresh_display() -> void:
	if _title_lbl == null:
		return

	_title_lbl.text = _t("戰鬥勝利")
	_sub_lbl.text = _t("關卡討伐成功！獲得戰利品機芯部件")
	_btn_confirm.text = _t("收下完成")
	_btn_equip.text = _t("已裝備") if _is_equipped else _t("立即裝備")

	if _part.is_empty():
		_slot_name_lbl.text = _t("機芯部件")
		_tier_lbl.text = _t("【白階】")
		_stats_lbl.text = ""
		_desc_lbl.text = _t("已收進機芯背包")
		return

	var cs = _cs()
	var sdb = _sprite_db()

	var slot_id: String = str(_part.get("slot", "mainspring"))
	var tier_id: String = str(_part.get("tier", "white"))
	var tier_name: String = str(_part.get("tier_name", "白"))
	var slot_name: String = str(_part.get("slot_name", ""))
	if slot_name.is_empty() and cs != null:
		slot_name = cs.get_slot_name(slot_id)

	var tier_color: Color = Color.WHITE
	if cs != null:
		tier_color = cs.get_tier_color(tier_id)

	_slot_name_lbl.text = _t(slot_name)
	_tier_lbl.text = "【%s】" % _t(tier_name + "階")
	_tier_lbl.add_theme_color_override("font_color", tier_color if tier_id != "white" else COLOR_TEXT_DARK)

	if sdb != null and _slot_icon != null:
		var tex: Texture2D = sdb.core_slot_icon(slot_id)
		if tex:
			_slot_icon.texture = tex
		_slot_icon.modulate = tier_color

	var stat_parts: Array[String] = []
	if cs != null:
		var pstats: Dictionary = cs.get_part_stats(_part)
		if int(pstats.get("atk", 0)) > 0: stat_parts.append("攻+%d" % int(pstats.atk))
		if int(pstats.get("def", 0)) > 0: stat_parts.append("防+%d" % int(pstats.def))
		if int(pstats.get("hp", 0)) > 0: stat_parts.append("血+%d" % int(pstats.hp))
		if float(pstats.get("crit", 0.0)) > 0.0: stat_parts.append("暴擊+%.1f%%" % float(pstats.crit))
		if float(pstats.get("crit_dmg", 0.0)) > 0.0: stat_parts.append("暴傷+%.0f%%" % float(pstats.crit_dmg))
	_stats_lbl.text = " · ".join(stat_parts) if not stat_parts.is_empty() else _t("標準數值")
	_desc_lbl.text = _t("可校準 7 次 · 安全彈簧保護不碎裝")


func _on_equip_pressed() -> void:
	if _part.is_empty():
		return
	var a = _audio()
	if a != null:
		a.play_ui()
	var slot_id: String = str(_part.get("slot", ""))
	var cs = _cs()
	if cs != null:
		cs.equip_part(slot_id, _part)
	_is_equipped = true
	_btn_equip.text = _t("已裝備")
	_btn_equip.disabled = true
	_desc_lbl.text = _t("已成功替換裝備至【%s】槽位！") % _slot_name_lbl.text
	_desc_lbl.add_theme_color_override("font_color", COLOR_MINT)


func _on_confirm_pressed() -> void:
	var a = _audio()
	if a != null:
		a.play_ui()
	confirmed.emit()
	if _on_confirm.is_valid():
		_on_confirm.call()
	queue_free()


func _cs() -> Object:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var n: Node = (tree as SceneTree).root.get_node_or_null("CoreSystem")
		if n:
			return n
	return load("res://scripts/systems/core_system.gd")


func _sprite_db() -> Object:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var n: Node = (tree as SceneTree).root.get_node_or_null("SpriteDB")
		if n:
			return n
	return load("res://scripts/art/sprite_db.gd")


func _audio() -> Object:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		return (tree as SceneTree).root.get_node_or_null("AudioManager")
	return null


## ── 樣式建構輔助 ──
func _create_floating_panel_style(bg: Color, border: Color, bw: int, sh: int, cr: int) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(bw)
	sb.set_corner_radius_all(cr)
	sb.shadow_color = Color(0.12, 0.1, 0.22, 0.3)
	sb.shadow_size = sh
	sb.shadow_offset = Vector2(0, sh / 2)
	return sb


func _create_inner_card_style(bg: Color, border: Color, bw: int, sh: int, cr: int) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(bw)
	sb.set_corner_radius_all(cr)
	sb.shadow_color = Color(0.12, 0.1, 0.22, 0.15)
	sb.shadow_size = sh
	sb.shadow_offset = Vector2(0, sh / 2)
	return sb


func _style_button(btn: Button, bg: Color, border: Color) -> void:
	var normal := StyleBoxFlat.new()
	normal.bg_color = bg
	normal.border_color = border
	normal.set_border_width_all(2)
	normal.border_width_bottom = 5
	normal.set_corner_radius_all(14)

	var pressed := StyleBoxFlat.new()
	pressed.bg_color = bg.darkened(0.12)
	pressed.border_color = border
	pressed.set_border_width_all(2)
	pressed.border_width_bottom = 2
	pressed.border_width_top = 4
	pressed.set_corner_radius_all(14)

	var disabled := StyleBoxFlat.new()
	disabled.bg_color = Color(0.85, 0.84, 0.88, 1)
	disabled.border_color = border.lerp(Color.WHITE, 0.4)
	disabled.set_border_width_all(2)
	disabled.border_width_bottom = 3
	disabled.set_corner_radius_all(14)

	btn.add_theme_stylebox_override("normal", normal)
	btn.add_theme_stylebox_override("hover", normal)
	btn.add_theme_stylebox_override("pressed", pressed)
	btn.add_theme_stylebox_override("disabled", disabled)

	btn.add_theme_font_size_override("font_size", 16)
	btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn.add_theme_color_override("font_disabled_color", COLOR_TEXT_MUTED)
	if _cached_font:
		btn.add_theme_font_override("font", _cached_font)


func _create_close_button() -> Button:
	var btn := Button.new()
	btn.text = "✕"
	btn.custom_minimum_size = Vector2(52, 52)
	btn.focus_mode = Control.FOCUS_NONE

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 4
	sb.set_corner_radius_all(14)

	var sbp := StyleBoxFlat.new()
	sbp.bg_color = COLOR_CARD_WARM.darkened(0.1)
	sbp.border_color = COLOR_BORDER
	sbp.set_border_width_all(2)
	sbp.border_width_bottom = 2
	sbp.set_corner_radius_all(14)

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb)
	btn.add_theme_stylebox_override("pressed", sbp)

	btn.add_theme_font_size_override("font_size", 20)
	btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		btn.add_theme_font_override("font", _cached_font)
	return btn
