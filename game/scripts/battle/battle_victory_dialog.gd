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
const CoreReplaceDialogScript := preload("res://scripts/ui/core_replace_dialog.gd")
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
var _part_break_container: HBoxContainer
var _bag_target: PanelContainer
var _bag_icon: TextureRect
var _fx_layer: Control
var _exp_panel: PanelContainer
var _exp_tag_lbl: Label
var _exp_lbl: Label
var _scrap_panel: PanelContainer
var _scrap_tag_lbl: Label
var _scrap_lbl: Label
var _btn_equip: Button
var _btn_confirm: Button
var _btn_close: Button
var _cached_font: Font = null

# ── 機芯替換比較彈窗 (Compare Modal) ──
var _compare_layer: Control = null
var _compare_card: PanelContainer = null
var _cmp_title_lbl: Label = null
var _cmp_sub_lbl: Label = null
var _cmp_slot_lbl: Label = null
var _cmp_old_tag_lbl: Label = null
var _cmp_old_name_lbl: Label = null
var _cmp_old_tier_lbl: Label = null
var _cmp_old_stats_lbl: Label = null
var _cmp_old_icon: TextureRect = null
var _cmp_new_tag_lbl: Label = null
var _cmp_new_name_lbl: Label = null
var _cmp_new_tier_lbl: Label = null
var _cmp_new_stats_lbl: Label = null
var _cmp_new_icon: TextureRect = null
var _btn_confirm_replace: Button = null
var _btn_cancel_replace: Button = null
var _btn_compare_close: Button = null
var _current_cmp_old_part: Dictionary = {}
var _current_cmp_slot_id: String = ""

var _part: Dictionary = {}
var _on_confirm: Callable = Callable()
var _is_equipped: bool = false
var _exp_gain: int = 0
var _scrap_gain: int = 0
var _is_colossus: bool = false
var _broken_parts: Array[String] = []
var _is_confirming: bool = false


static func show_dialog(parent: Node, part: Dictionary = {}, on_confirm: Callable = Callable(), exp_gain: int = -1, scrap_gain: int = -1, broken_parts: Array = []) -> Control:
	var dlg = load("res://scripts/battle/battle_victory_dialog.gd").new()
	dlg.setup(part, on_confirm, exp_gain, scrap_gain, broken_parts)
	parent.add_child(dlg)
	return dlg


func setup(part: Dictionary = {}, on_confirm: Callable = Callable(), exp_gain: int = -1, scrap_gain: int = -1, broken_parts: Array = []) -> void:
	_part = part.duplicate(true)
	_on_confirm = on_confirm
	_broken_parts.clear()
	if not broken_parts.is_empty():
		for bp in broken_parts:
			var s := str(bp).strip_edges()
			if not s.is_empty() and not (s in _broken_parts):
				_broken_parts.append(s)
	elif _part.has("broken_parts") and _part["broken_parts"] is Array:
		for bp in _part["broken_parts"]:
			if bp is Dictionary:
				var s := str(bp.get("raw_name", bp.get("name", bp.get("part_name", "")))).strip_edges()
				if not s.is_empty() and not (s in _broken_parts):
					_broken_parts.append(s)
			else:
				var s := str(bp).strip_edges()
				if not s.is_empty() and not (s in _broken_parts):
					_broken_parts.append(s)
	elif _part.has("broken_part") and not str(_part["broken_part"]).strip_edges().is_empty():
		_broken_parts.append(str(_part["broken_part"]).strip_edges())
	if exp_gain >= 0:
		_exp_gain = exp_gain
	elif _part.has("exp_gain"):
		_exp_gain = int(_part["exp_gain"])
	elif _part.has("exp"):
		_exp_gain = int(_part["exp"])
	else:
		_exp_gain = 0

	if scrap_gain >= 0:
		_scrap_gain = scrap_gain
	elif _part.has("scrap_gain"):
		_scrap_gain = int(_part["scrap_gain"])
	elif _part.has("iron_scrap"):
		_scrap_gain = int(_part["iron_scrap"])
	else:
		_scrap_gain = 0
	_is_colossus = bool(_part.get("is_colossus", false)) or str(_part.get("mode", "")).begins_with("colossus_")
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
	if _compare_layer != null and _compare_layer.visible:
		_refresh_compare_display()


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

	# ── 部位破壞徽章展示區 (PartBreakBadgesContainer) ──
	_part_break_container = HBoxContainer.new()
	_part_break_container.name = "PartBreakBadgesContainer"
	_part_break_container.alignment = BoxContainer.ALIGNMENT_CENTER
	_part_break_container.add_theme_constant_override("separation", 10)
	v.add_child(_part_break_container)

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
	_slot_name_lbl.text = ""
	_slot_name_lbl.add_theme_font_size_override("font_size", 18)
	_slot_name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_slot_name_lbl.add_theme_font_override("font", _cached_font)
	name_tier_row.add_child(_slot_name_lbl)

	_tier_lbl = Label.new()
	_tier_lbl.name = "TierLabel"
	_tier_lbl.text = ""
	_tier_lbl.add_theme_font_size_override("font_size", 16)
	_tier_lbl.add_theme_color_override("font_color", COLOR_GOLD)
	if _cached_font:
		_tier_lbl.add_theme_font_override("font", _cached_font)
	name_tier_row.add_child(_tier_lbl)

	_stats_lbl = Label.new()
	_stats_lbl.name = "StatsLabel"
	_stats_lbl.text = ""
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

	# ── 經驗獲得展示列 (ExpRewardPanel) ──
	_exp_panel = PanelContainer.new()
	_exp_panel.name = "ExpRewardPanel"
	_exp_panel.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 14))
	v.add_child(_exp_panel)

	var exp_margin := MarginContainer.new()
	exp_margin.add_theme_constant_override("margin_left", 16)
	exp_margin.add_theme_constant_override("margin_right", 16)
	exp_margin.add_theme_constant_override("margin_top", 6)
	exp_margin.add_theme_constant_override("margin_bottom", 6)
	_exp_panel.add_child(exp_margin)

	var exp_row := HBoxContainer.new()
	exp_row.alignment = BoxContainer.ALIGNMENT_CENTER
	exp_row.add_theme_constant_override("separation", 10)
	exp_margin.add_child(exp_row)

	_exp_tag_lbl = Label.new()
	_exp_tag_lbl.name = "ExpTagLabel"
	_exp_tag_lbl.text = _t("戰鬥經驗")
	_exp_tag_lbl.add_theme_font_size_override("font_size", 14)
	_exp_tag_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_exp_tag_lbl.add_theme_font_override("font", _cached_font)
	exp_row.add_child(_exp_tag_lbl)

	_exp_lbl = Label.new()
	_exp_lbl.name = "ExpLabel"
	_exp_lbl.text = ""
	_exp_lbl.add_theme_font_size_override("font_size", 16)
	_exp_lbl.add_theme_color_override("font_color", COLOR_ORANGE)
	if _cached_font:
		_exp_lbl.add_theme_font_override("font", _cached_font)
	exp_row.add_child(_exp_lbl)

	# ── 部位破壞鐵屑獲得展示列 (ScrapRewardPanel) ──
	_scrap_panel = PanelContainer.new()
	_scrap_panel.name = "ScrapRewardPanel"
	_scrap_panel.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 3, 14))
	v.add_child(_scrap_panel)

	var scrap_margin := MarginContainer.new()
	scrap_margin.add_theme_constant_override("margin_left", 16)
	scrap_margin.add_theme_constant_override("margin_right", 16)
	scrap_margin.add_theme_constant_override("margin_top", 6)
	scrap_margin.add_theme_constant_override("margin_bottom", 6)
	_scrap_panel.add_child(scrap_margin)

	var scrap_row := HBoxContainer.new()
	scrap_row.alignment = BoxContainer.ALIGNMENT_CENTER
	scrap_row.add_theme_constant_override("separation", 10)
	scrap_margin.add_child(scrap_row)

	_scrap_tag_lbl = Label.new()
	_scrap_tag_lbl.name = "ScrapTagLabel"
	_scrap_tag_lbl.text = _t("部位破壞")
	_scrap_tag_lbl.add_theme_font_size_override("font_size", 14)
	_scrap_tag_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_scrap_tag_lbl.add_theme_font_override("font", _cached_font)
	scrap_row.add_child(_scrap_tag_lbl)

	_scrap_lbl = Label.new()
	_scrap_lbl.name = "ScrapLabel"
	_scrap_lbl.text = ""
	_scrap_lbl.add_theme_font_size_override("font_size", 16)
	_scrap_lbl.add_theme_color_override("font_color", COLOR_SKY)
	if _cached_font:
		_scrap_lbl.add_theme_font_override("font", _cached_font)
	scrap_row.add_child(_scrap_lbl)

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

	# 背包圖示目標（多巴胺獎勵入袋流向目標，熱區 >= 48px，零系統 emoji）
	_bag_target = PanelContainer.new()
	_bag_target.name = "BagTarget"
	_bag_target.custom_minimum_size = Vector2(52, 52)
	_bag_target.pivot_offset = Vector2(26, 26)
	var bag_st := StyleBoxFlat.new()
	bag_st.bg_color = COLOR_CARD_WARM
	bag_st.border_color = COLOR_BORDER
	bag_st.set_border_width_all(2)
	bag_st.border_width_bottom = 5
	bag_st.set_corner_radius_all(14)
	_bag_target.add_theme_stylebox_override("panel", bag_st)

	var bag_margin := MarginContainer.new()
	bag_margin.add_theme_constant_override("margin_left", 6)
	bag_margin.add_theme_constant_override("margin_right", 6)
	bag_margin.add_theme_constant_override("margin_top", 6)
	bag_margin.add_theme_constant_override("margin_bottom", 6)
	_bag_target.add_child(bag_margin)

	_bag_icon = TextureRect.new()
	_bag_icon.name = "BagIcon"
	_bag_icon.custom_minimum_size = Vector2(36, 36)
	_bag_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_bag_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_bag_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/icons/hud/icon_dock_bag.png"):
		_bag_icon.texture = load("res://assets/icons/hud/icon_dock_bag.png")
	bag_margin.add_child(_bag_icon)
	btn_row.add_child(_bag_target)

	# 多巴胺特效飛散圖層 (FxLayer)
	_fx_layer = Control.new()
	_fx_layer.name = "FxLayer"
	_fx_layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_fx_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_dialog_card.add_child(_fx_layer)


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
	var tier_name: String = str(_part.get("tier_name", ""))
	var slot_name: String = str(_part.get("slot_name", ""))

	var norm_slot: String = slot_id
	if cs != null:
		norm_slot = cs.normalize_slot_id(slot_id)
		if slot_name.is_empty():
			slot_name = cs.get_slot_name(norm_slot)
		if tier_name.is_empty() and cs.TIER_NAMES.has(tier_id):
			tier_name = str(cs.TIER_NAMES.get(tier_id, "白"))
	if slot_name.is_empty():
		slot_name = "發條發電機"
	if tier_name.is_empty():
		tier_name = "白"

	var tier_color: Color = Color.WHITE
	if cs != null:
		tier_color = cs.get_tier_color(tier_id)

	_slot_name_lbl.text = _t(slot_name)

	var bracket_tier_key := "【%s階】" % tier_name
	_tier_lbl.text = _t(bracket_tier_key) if _t(bracket_tier_key) != bracket_tier_key else (_t("【%s】") % _t(tier_name + "階"))
	_tier_lbl.add_theme_color_override("font_color", tier_color if tier_id != "white" else COLOR_TEXT_DARK)

	if sdb != null and _slot_icon != null:
		var tex: Texture2D = sdb.core_slot_icon(norm_slot)
		if tex:
			_slot_icon.texture = tex
		_slot_icon.modulate = tier_color

	var stat_parts: Array[String] = []
	var pstats := {}
	if cs != null:
		pstats = cs.get_part_stats(_part)
	else:
		var raw_s: Dictionary = _part.get("stats", {})
		pstats = {
			"atk": int(raw_s.get("ATK", raw_s.get("atk", 0))),
			"def": int(raw_s.get("DEF", raw_s.get("def", 0))),
			"hp": int(raw_s.get("HP", raw_s.get("hp", 0))),
			"crit": float(raw_s.get("CRIT", raw_s.get("crit", 0.0))),
			"crit_dmg": float(raw_s.get("CRIT_DMG", raw_s.get("crit_dmg", 0.0)))
		}
	if int(pstats.get("atk", 0)) > 0: stat_parts.append(_t("攻+%d") % int(pstats.atk))
	if int(pstats.get("def", 0)) > 0: stat_parts.append(_t("防+%d") % int(pstats.def))
	if int(pstats.get("hp", 0)) > 0: stat_parts.append(_t("血+%d") % int(pstats.hp))
	if float(pstats.get("crit", 0.0)) > 0.0: stat_parts.append(_t("暴擊+%.1f%%") % float(pstats.crit))
	if float(pstats.get("crit_dmg", 0.0)) > 0.0: stat_parts.append(_t("暴傷+%.0f%%") % float(pstats.crit_dmg))
	_stats_lbl.text = " · ".join(stat_parts) if not stat_parts.is_empty() else _t("標準數值")

	if _is_equipped:
		_desc_lbl.text = _t("已成功替換裝備至【%s】槽位！") % _slot_name_lbl.text
		_desc_lbl.add_theme_color_override("font_color", COLOR_MINT)
	else:
		_desc_lbl.text = _t("可校準 7 次 · 安全彈簧保護不碎裝")
		_desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)

	if _exp_panel != null and _exp_lbl != null:
		if _exp_tag_lbl != null:
			_exp_tag_lbl.text = _t("戰鬥經驗")
		var is_max_lvl := _is_player_max_level()
		if _exp_gain > 0:
			_exp_panel.visible = true
			_exp_lbl.text = _t("經驗 +%d") % _exp_gain
			_exp_lbl.add_theme_color_override("font_color", COLOR_ORANGE)
		elif _is_colossus and is_max_lvl:
			_exp_panel.visible = true
			_exp_lbl.text = _t("經驗 +0（已達上限）")
			_exp_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
		elif _is_colossus:
			_exp_panel.visible = true
			_exp_lbl.text = _t("經驗 +0")
			_exp_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
		else:
			_exp_panel.visible = false
			_exp_lbl.text = _t("經驗 +0")

	if _scrap_panel != null and _scrap_lbl != null:
		if _scrap_tag_lbl != null:
			_scrap_tag_lbl.text = _t("部位破壞")
		if _scrap_gain > 0:
			_scrap_panel.visible = true
			_scrap_lbl.text = _t("鐵屑 +%d") % _scrap_gain
			_scrap_lbl.add_theme_color_override("font_color", COLOR_SKY)
		else:
			_scrap_panel.visible = false
			_scrap_lbl.text = _t("鐵屑 +0")

	# ── 更新頂部部位破壞徽章 ──
	if _part_break_container != null:
		if _broken_parts.is_empty():
			_part_break_container.visible = false
			for c in _part_break_container.get_children():
				_part_break_container.remove_child(c)
				c.queue_free()
		else:
			_part_break_container.visible = true
			if _part_break_container.get_child_count() == _broken_parts.size():
				for i in range(_broken_parts.size()):
					var badge: PanelContainer = _part_break_container.get_child(i) as PanelContainer
					if badge:
						var name_lbl: Label = badge.find_child("PartNameLabel", true, false) as Label
						if name_lbl:
							name_lbl.text = _t(_broken_parts[i])
			else:
				for c in _part_break_container.get_children():
					_part_break_container.remove_child(c)
					c.queue_free()
				for i in range(_broken_parts.size()):
					var bp_name: String = _broken_parts[i]
					var badge := _create_part_break_badge(bp_name, i)
					_part_break_container.add_child(badge)


func _is_player_max_level() -> bool:
	if bool(_part.get("is_max_level", false)):
		return true
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var gs: Node = (tree as SceneTree).root.get_node_or_null("GameState")
		if gs:
			var cap: int = int(gs.call("get_level_cap")) if gs.has_method("get_level_cap") else 30
			var cur_lv: int = int(gs.get("level"))
			return cur_lv >= cap
	return false


func _get_slot_name_for(norm_slot: String) -> String:
	var cs = _cs()
	var sname := ""
	if cs != null and cs.has_method("get_slot_name"):
		sname = str(cs.call("get_slot_name", norm_slot))
	if sname.is_empty():
		sname = "發條發電機"
	return sname


func _get_bracket_tier_text(part: Dictionary) -> String:
	var cs = _cs()
	var tier_id: String = str(part.get("tier", "white"))
	var tier_name: String = str(part.get("tier_name", ""))
	if tier_name.is_empty() and cs != null and "TIER_NAMES" in cs and cs.TIER_NAMES.has(tier_id):
		tier_name = str(cs.TIER_NAMES.get(tier_id, "白"))
	if tier_name.is_empty():
		tier_name = "白"
	var bracket_tier_key := "【%s階】" % tier_name
	return _t(bracket_tier_key) if _t(bracket_tier_key) != bracket_tier_key else (_t("【%s】") % _t(tier_name + "階"))


func _get_part_tier_color(part: Dictionary) -> Color:
	var cs = _cs()
	var tier_id: String = str(part.get("tier", "white"))
	if cs != null and cs.has_method("get_tier_color"):
		return cs.call("get_tier_color", tier_id)
	return Color.WHITE


func _format_stats_string(part: Dictionary) -> String:
	var cs = _cs()
	var stat_parts: Array[String] = []
	var pstats := {}
	if cs != null and cs.has_method("get_part_stats"):
		pstats = cs.call("get_part_stats", part)
	else:
		var raw_s: Dictionary = part.get("stats", {})
		pstats = {
			"atk": int(raw_s.get("ATK", raw_s.get("atk", 0))),
			"def": int(raw_s.get("DEF", raw_s.get("def", 0))),
			"hp": int(raw_s.get("HP", raw_s.get("hp", 0))),
			"crit": float(raw_s.get("CRIT", raw_s.get("crit", 0.0))),
			"crit_dmg": float(raw_s.get("CRIT_DMG", raw_s.get("crit_dmg", 0.0)))
		}
	if int(pstats.get("atk", 0)) > 0: stat_parts.append(_t("攻+%d") % int(pstats.atk))
	if int(pstats.get("def", 0)) > 0: stat_parts.append(_t("防+%d") % int(pstats.def))
	if int(pstats.get("hp", 0)) > 0: stat_parts.append(_t("血+%d") % int(pstats.hp))
	if float(pstats.get("crit", 0.0)) > 0.0: stat_parts.append(_t("暴擊+%.1f%%") % float(pstats.crit))
	if float(pstats.get("crit_dmg", 0.0)) > 0.0: stat_parts.append(_t("暴傷+%.0f%%") % float(pstats.crit_dmg))
	return " · ".join(stat_parts) if not stat_parts.is_empty() else _t("標準數值")


func _on_equip_pressed() -> void:
	if _part.is_empty():
		return
	var a = _audio()
	if a != null:
		a.play_ui()
	var slot_id: String = str(_part.get("slot", "mainspring"))
	var cs = _cs()
	var norm_slot: String = slot_id
	if cs != null and cs.has_method("normalize_slot_id"):
		norm_slot = str(cs.call("normalize_slot_id", slot_id))

	var old_part: Dictionary = {}
	if cs != null and cs.has_method("get_equipped_part"):
		old_part = cs.call("get_equipped_part", norm_slot)

	if old_part.is_empty():
		_do_equip(norm_slot)
	else:
		_show_replace_comparison(norm_slot, old_part)


func _do_equip(norm_slot: String) -> void:
	var cs = _cs()
	if cs != null:
		cs.equip_part(norm_slot, _part)
	_is_equipped = true
	_btn_equip.text = _t("已裝備")
	_btn_equip.disabled = true
	_desc_lbl.text = _t("已成功替換裝備至【%s】槽位！") % _slot_name_lbl.text
	_desc_lbl.add_theme_color_override("font_color", COLOR_MINT)
	if _compare_layer != null:
		_compare_layer.visible = false


func _show_replace_comparison(norm_slot: String, old_part: Dictionary) -> void:
	_current_cmp_slot_id = norm_slot
	_current_cmp_old_part = old_part.duplicate(true)
	if _compare_layer == null:
		_build_compare_ui()
	else:
		_compare_layer.setup(norm_slot, old_part, _part, _on_confirm_replace, _on_cancel_replace)
	_refresh_compare_display()
	_compare_layer.visible = true


func _on_cancel_replace() -> void:
	var a = _audio()
	if a != null:
		a.play_ui()
	if _compare_layer != null:
		_compare_layer.visible = false
	_desc_lbl.text = _t("新部件已保留在機芯背包中")
	_desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)


func _on_confirm_replace() -> void:
	var a = _audio()
	if a != null:
		a.play_ui()
	_do_equip(_current_cmp_slot_id)


func _build_compare_ui() -> void:
	if _compare_layer != null:
		return
	_compare_layer = CoreReplaceDialogScript.show_dialog(self, _current_cmp_slot_id, _current_cmp_old_part, _part, _on_confirm_replace, _on_cancel_replace, "hide")


func _refresh_compare_display() -> void:
	if _compare_layer != null and _compare_layer.has_method("refresh_display"):
		_compare_layer.refresh_display()


func _create_part_break_badge(part_name: String, index: int) -> PanelContainer:
	var badge := PanelContainer.new()
	badge.name = "PartBreakBadge_%d" % index
	var st := StyleBoxFlat.new()
	st.bg_color = Color("#FFF0F4")
	st.border_color = COLOR_BORDER
	st.set_border_width_all(2)
	st.border_width_bottom = 4
	st.set_corner_radius_all(14)
	st.shadow_color = Color(0.12, 0.1, 0.22, 0.12)
	st.shadow_size = 3
	st.shadow_offset = Vector2(0, 2)
	badge.add_theme_stylebox_override("panel", st)

	var m := MarginContainer.new()
	m.add_theme_constant_override("margin_left", 12)
	m.add_theme_constant_override("margin_right", 12)
	m.add_theme_constant_override("margin_top", 4)
	m.add_theme_constant_override("margin_bottom", 4)
	badge.add_child(m)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 8)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	m.add_child(h)

	# PART BREAK 標籤小膠囊
	var tag_box := PanelContainer.new()
	tag_box.name = "TagBox"
	var tag_st := StyleBoxFlat.new()
	tag_st.bg_color = COLOR_PINK
	tag_st.border_color = COLOR_BORDER
	tag_st.set_border_width_all(1)
	tag_st.border_width_bottom = 2
	tag_st.set_corner_radius_all(8)
	tag_box.add_theme_stylebox_override("panel", tag_st)

	var tm := MarginContainer.new()
	tm.add_theme_constant_override("margin_left", 6)
	tm.add_theme_constant_override("margin_right", 6)
	tm.add_theme_constant_override("margin_top", 2)
	tm.add_theme_constant_override("margin_bottom", 2)
	tag_box.add_child(tm)

	var tag_lbl := Label.new()
	tag_lbl.name = "BreakTagLabel"
	tag_lbl.text = "PART BREAK"
	tag_lbl.add_theme_font_size_override("font_size", 11)
	tag_lbl.add_theme_color_override("font_color", Color.WHITE)
	if _cached_font:
		tag_lbl.add_theme_font_override("font", _cached_font)
	tm.add_child(tag_lbl)
	h.add_child(tag_box)

	# 部位名稱標籤
	var name_lbl := Label.new()
	name_lbl.name = "PartNameLabel"
	name_lbl.text = _t(part_name)
	name_lbl.add_theme_font_size_override("font_size", 14)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	h.add_child(name_lbl)

	return badge


func _on_confirm_pressed() -> void:
	if _is_confirming:
		return
	_is_confirming = true

	var a = _audio()
	if a != null:
		if a.has_method("play_craft_success"):
			a.play_craft_success()
		elif a.has_method("play_ui"):
			a.play_ui()

	if DisplayServer.get_name() == "headless" or not is_inside_tree() or _fx_layer == null:
		_finish_confirm()
		return

	play_reward_particles_to_bag(Callable(self, "_finish_confirm"))


func play_reward_particles_to_bag(on_finished: Callable = Callable()) -> void:
	if _fx_layer == null:
		if on_finished.is_valid():
			on_finished.call()
		return

	var start_pos: Vector2 = _btn_confirm.global_position + _btn_confirm.size * 0.5 if _btn_confirm else _dialog_card.size * 0.5
	var target_pos: Vector2 = _bag_target.global_position + _bag_target.size * 0.5 if _bag_target else start_pos + Vector2(100, 0)
	var local_start: Vector2 = start_pos - _fx_layer.global_position
	var local_target: Vector2 = target_pos - _fx_layer.global_position

	var particle_count := 14
	var gold_tex: Texture2D = null
	if ResourceLoader.exists("res://assets/icons/hud/icon_gold_coin.png"):
		gold_tex = load("res://assets/icons/hud/icon_gold_coin.png") as Texture2D

	for i in range(particle_count):
		var p: Control = null
		var is_gold: bool = (i % 2 == 0)

		if is_gold and gold_tex != null:
			var trect := TextureRect.new()
			trect.texture = gold_tex
			trect.custom_minimum_size = Vector2(16, 16)
			trect.size = Vector2(16, 16)
			trect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			trect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
			p = trect
		else:
			var cbox := PanelContainer.new()
			cbox.custom_minimum_size = Vector2(12, 12)
			cbox.size = Vector2(12, 12)
			var sb := StyleBoxFlat.new()
			sb.bg_color = COLOR_GOLD if is_gold else COLOR_SKY
			sb.border_color = COLOR_BORDER
			sb.set_border_width_all(1)
			sb.set_corner_radius_all(3)
			cbox.add_theme_stylebox_override("panel", sb)
			p = cbox

		p.position = local_start
		p.pivot_offset = p.size * 0.5
		p.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_fx_layer.add_child(p)

		var angle := randf_range(0.0, TAU)
		var burst_dist := randf_range(35.0, 80.0)
		var burst_pos := local_start + Vector2(cos(angle), sin(angle) - 0.3) * burst_dist

		var tw := p.create_tween()
		tw.tween_property(p, "position", burst_pos, 0.16).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(p, "scale", Vector2(1.3, 1.3), 0.16)

		var flight_time := randf_range(0.20, 0.30)
		tw.tween_property(p, "position", local_target, flight_time).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_IN)
		tw.parallel().tween_property(p, "scale", Vector2(0.5, 0.5), flight_time)
		tw.parallel().tween_property(p, "modulate:a", 0.2, flight_time)
		tw.tween_callback(p.queue_free)

	if _bag_target != null:
		var btw := _bag_target.create_tween()
		btw.tween_interval(0.24)
		btw.tween_property(_bag_target, "scale", Vector2(1.25, 1.25), 0.1).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		btw.tween_property(_bag_target, "scale", Vector2(1.0, 1.0), 0.12).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)

	var end_tw := create_tween()
	end_tw.tween_interval(0.48)
	if on_finished.is_valid():
		end_tw.tween_callback(on_finished)


func _finish_confirm() -> void:
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
	btn.text = "X"
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
