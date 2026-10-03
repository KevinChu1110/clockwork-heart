extends Control
## 裝備換裝副詞條比對確認彈窗 (EquipReplaceDialog)
## 依據任務 t_8776e576 規範：
## 1. 整備頁點背包裝備：該部位已有件 -> 彈比較卡，兩邊顯示名稱、品階、rolled 攻/防/血、副詞條全文。
## 2. 確認才覆蓋（舊件回背包）；取消或右上關閉 -> 槽與背包不變。
## 3. 空槽、以及武器欄尚有已解鎖空欄可直裝時 -> 不彈窗，維持現況一鍵。
## 4. 比較卡規格對齊現有機芯替換卡（寬 740~760、按鈕熱區 >= 48px）。
## 5. 零系統 emoji，字體優先使用 Open Huninn 粉圓體，多語系走 ContentLoc。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const ResponsiveUi := preload("res://scripts/ui/responsive_ui.gd")
const UiStyle := preload("res://scripts/ui/ui_style.gd")
const EquipmentSystemScript := preload("res://scripts/systems/equipment_system.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const COLOR_BG_CREAM := Color("#FFFDF8")
const COLOR_CARD_WARM := Color("#FFF8E7")
const COLOR_CARD_GOLD := Color("#FFF3D0")
const COLOR_BORDER := Color("#1F1A3A")
const COLOR_TEXT_DARK := Color("#1F1A3A")
const COLOR_TEXT_MUTED := Color("#6B5E80")
const COLOR_ORANGE := Color("#FFA010")
const COLOR_SKY := Color("#38A0FF")
const COLOR_MINT := Color("#4ED86A")
const COLOR_PURPLE := Color("#A855F7")

signal confirmed
signal cancelled

var _slot_name: String = ""
var _old_inst: Dictionary = {}
var _new_inst: Dictionary = {}
var _on_confirm: Callable = Callable()
var _on_cancel: Callable = Callable()
var _cached_font: Font = null
var _close_mode: String = "free"
var _connected_loc: bool = false

var _compare_card: PanelContainer = null
var _cmp_title_lbl: Label = null
var _cmp_sub_lbl: Label = null
var _btn_close: Button = null
var _cmp_slot_lbl: Label = null

var _cmp_old_tag_lbl: Label = null
var _cmp_old_icon: TextureRect = null
var _cmp_old_name_lbl: Label = null
var _cmp_old_swatch: ColorRect = null
var _cmp_old_tier_lbl: Label = null
var _cmp_old_stats_lbl: Label = null
var _cmp_old_affixes_box: VBoxContainer = null

var _arrow_lbl: Label = null

var _cmp_new_tag_lbl: Label = null
var _cmp_new_icon: TextureRect = null
var _cmp_new_name_lbl: Label = null
var _cmp_new_swatch: ColorRect = null
var _cmp_new_tier_lbl: Label = null
var _cmp_new_stats_lbl: Label = null
var _cmp_new_affixes_box: VBoxContainer = null

var _btn_cancel: Button = null
var _btn_confirm: Button = null


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


static func _sprite_db() -> Object:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var n: Node = (tree as SceneTree).root.get_node_or_null("SpriteDB")
		if n:
			return n
	return load("res://scripts/art/sprite_db.gd")


static func _eq_sys() -> Object:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var n: Node = (tree as SceneTree).root.get_node_or_null("EquipmentSystem")
		if n:
			return n
	return load("res://scripts/systems/equipment_system.gd")


static func show_dialog(
	parent: Node,
	slot_name: String,
	old_inst: Dictionary,
	new_inst: Dictionary,
	on_confirm: Callable = Callable(),
	on_cancel: Callable = Callable(),
	close_mode: String = "free"
) -> Control:
	var ScriptRef = load("res://scripts/ui/equip_replace_dialog.gd")
	var dlg = ScriptRef.new()
	dlg.name = "EquipCompareLayer"
	dlg.set_close_mode(close_mode)
	if parent != null:
		parent.add_child(dlg)
	dlg.setup(slot_name, old_inst, new_inst, on_confirm, on_cancel)
	return dlg


func set_close_mode(mode: String) -> void:
	_close_mode = mode


func setup(
	slot_name: String,
	old_inst: Dictionary,
	new_inst: Dictionary,
	on_confirm: Callable = Callable(),
	on_cancel: Callable = Callable()
) -> void:
	_slot_name = slot_name
	_old_inst = old_inst.duplicate(true)
	_new_inst = new_inst.duplicate(true)
	_on_confirm = on_confirm
	_on_cancel = on_cancel

	if _compare_card == null:
		_build_ui()
	refresh_display()
	visible = true


func _enter_tree() -> void:
	_connect_locale_signal()


func _connect_locale_signal() -> void:
	if _connected_loc:
		return
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var loc: Node = (tree as SceneTree).root.get_node_or_null("Loc")
		if loc != null and loc.has_signal("locale_changed"):
			if not loc.is_connected("locale_changed", Callable(self, "_on_locale_changed")):
				loc.connect("locale_changed", Callable(self, "_on_locale_changed"))
				_connected_loc = true


func _on_locale_changed(_new_loc: String = "") -> void:
	refresh_display()


func _build_ui() -> void:
	name = "EquipCompareLayer"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 85

	if ResourceLoader.exists(FONT_PATH) and _cached_font == null:
		_cached_font = load(FONT_PATH) as Font

	# 1. 全螢幕半透明遮罩
	var scrim := ResponsiveUi.make_scrim(Color(0.05, 0.04, 0.08, 0.6))
	scrim.name = "CompareScrim"
	add_child(scrim)

	# 2. 置中容器
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	# 3. 比較卡片（寬度 740px，在 740~760px 範圍內）
	_compare_card = PanelContainer.new()
	_compare_card.name = "CompareCard"
	ResponsiveUi.apply_dialog_card(_compare_card)
	_compare_card.custom_minimum_size = Vector2(740, 450)
	_compare_card.add_theme_stylebox_override("panel", _create_floating_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_compare_card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 18)
	margin.add_theme_constant_override("margin_bottom", 20)
	_compare_card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 10)
	margin.add_child(v)

	# ── 標題列 + 關閉按鈕 ──
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	v.add_child(head)

	var title_col := VBoxContainer.new()
	title_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_col.add_theme_constant_override("separation", 2)
	head.add_child(title_col)

	_cmp_title_lbl = Label.new()
	_cmp_title_lbl.name = "CompareTitleLabel"
	_cmp_title_lbl.text = _t("裝備替換確認")
	_cmp_title_lbl.add_theme_font_size_override("font_size", 22)
	_cmp_title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_cmp_title_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_cmp_title_lbl)

	_cmp_sub_lbl = Label.new()
	_cmp_sub_lbl.name = "CompareSubtitleLabel"
	_cmp_sub_lbl.text = _t("該部位已有穿戴裝備，是否確認替換？")
	_cmp_sub_lbl.add_theme_font_size_override("font_size", 13)
	_cmp_sub_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_cmp_sub_lbl.add_theme_font_override("font", _cached_font)
	title_col.add_child(_cmp_sub_lbl)

	_btn_close = _create_close_button()
	_btn_close.name = "CompareCloseButton"
	_btn_close.pressed.connect(_on_cancel_pressed)
	head.add_child(_btn_close)

	# ── 槽位提示標籤 ──
	_cmp_slot_lbl = Label.new()
	_cmp_slot_lbl.name = "CompareSlotLabel"
	_cmp_slot_lbl.text = ""
	_cmp_slot_lbl.add_theme_font_size_override("font_size", 15)
	_cmp_slot_lbl.add_theme_color_override("font_color", COLOR_SKY)
	if _cached_font:
		_cmp_slot_lbl.add_theme_font_override("font", _cached_font)
	v.add_child(_cmp_slot_lbl)

	# ── 舊件 vs 新件 並排比較區 ──
	var cmp_row := HBoxContainer.new()
	cmp_row.name = "CompareRow"
	cmp_row.add_theme_constant_override("separation", 14)
	cmp_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(cmp_row)

	# 左側：現有舊件卡片
	var old_panel := PanelContainer.new()
	old_panel.name = "OldPartCard"
	old_panel.custom_minimum_size = Vector2(320, 220)
	old_panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	old_panel.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 16))
	cmp_row.add_child(old_panel)

	var old_margin := MarginContainer.new()
	old_margin.add_theme_constant_override("margin_left", 14)
	old_margin.add_theme_constant_override("margin_right", 14)
	old_margin.add_theme_constant_override("margin_top", 12)
	old_margin.add_theme_constant_override("margin_bottom", 12)
	old_panel.add_child(old_margin)

	var old_vb := VBoxContainer.new()
	old_vb.add_theme_constant_override("separation", 6)
	old_margin.add_child(old_vb)

	_cmp_old_tag_lbl = Label.new()
	_cmp_old_tag_lbl.name = "OldTagLabel"
	_cmp_old_tag_lbl.text = _t("現有裝備")
	_cmp_old_tag_lbl.add_theme_font_size_override("font_size", 13)
	_cmp_old_tag_lbl.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
	if _cached_font:
		_cmp_old_tag_lbl.add_theme_font_override("font", _cached_font)
	old_vb.add_child(_cmp_old_tag_lbl)

	var old_info_row := HBoxContainer.new()
	old_info_row.add_theme_constant_override("separation", 10)
	old_vb.add_child(old_info_row)

	var old_icon_box := PanelContainer.new()
	old_icon_box.custom_minimum_size = Vector2(56, 56)
	var o_icon_st := StyleBoxFlat.new()
	o_icon_st.bg_color = Color(0.96, 0.95, 0.98, 1)
	o_icon_st.border_color = COLOR_BORDER
	o_icon_st.set_border_width_all(2)
	o_icon_st.set_corner_radius_all(12)
	old_icon_box.add_theme_stylebox_override("panel", o_icon_st)
	old_info_row.add_child(old_icon_box)

	_cmp_old_icon = TextureRect.new()
	_cmp_old_icon.name = "OldSlotIcon"
	_cmp_old_icon.custom_minimum_size = Vector2(44, 44)
	_cmp_old_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_cmp_old_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_cmp_old_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_cmp_old_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	old_icon_box.add_child(_cmp_old_icon)

	var old_text_col := VBoxContainer.new()
	old_text_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	old_text_col.add_theme_constant_override("separation", 2)
	old_info_row.add_child(old_text_col)

	_cmp_old_name_lbl = Label.new()
	_cmp_old_name_lbl.name = "OldSlotNameLabel"
	_cmp_old_name_lbl.text = ""
	_cmp_old_name_lbl.add_theme_font_size_override("font_size", 15)
	_cmp_old_name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_cmp_old_name_lbl.add_theme_font_override("font", _cached_font)
	old_text_col.add_child(_cmp_old_name_lbl)

	var old_tier_row := HBoxContainer.new()
	old_tier_row.add_theme_constant_override("separation", 6)
	old_tier_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	old_text_col.add_child(old_tier_row)

	_cmp_old_swatch = ColorRect.new()
	_cmp_old_swatch.name = "OldColorSwatch"
	_cmp_old_swatch.custom_minimum_size = Vector2(10, 18)
	_cmp_old_swatch.mouse_filter = Control.MOUSE_FILTER_IGNORE
	old_tier_row.add_child(_cmp_old_swatch)

	_cmp_old_tier_lbl = Label.new()
	_cmp_old_tier_lbl.name = "OldTierLabel"
	_cmp_old_tier_lbl.text = ""
	_cmp_old_tier_lbl.add_theme_font_size_override("font_size", 13)
	if _cached_font:
		_cmp_old_tier_lbl.add_theme_font_override("font", _cached_font)
	old_tier_row.add_child(_cmp_old_tier_lbl)

	_cmp_old_stats_lbl = Label.new()
	_cmp_old_stats_lbl.name = "OldStatsLabel"
	_cmp_old_stats_lbl.text = ""
	_cmp_old_stats_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_cmp_old_stats_lbl.add_theme_font_size_override("font_size", 13)
	_cmp_old_stats_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_cmp_old_stats_lbl.add_theme_font_override("font", _cached_font)
	old_vb.add_child(_cmp_old_stats_lbl)

	# 舊件副詞條清單
	_cmp_old_affixes_box = VBoxContainer.new()
	_cmp_old_affixes_box.name = "OldAffixesBox"
	_cmp_old_affixes_box.add_theme_constant_override("separation", 2)
	old_vb.add_child(_cmp_old_affixes_box)

	# 中間：箭頭指示
	var mid_box := VBoxContainer.new()
	mid_box.alignment = BoxContainer.ALIGNMENT_CENTER
	_arrow_lbl = Label.new()
	_arrow_lbl.name = "ArrowIndicator"
	_arrow_lbl.text = "➔"
	_arrow_lbl.add_theme_font_size_override("font_size", 24)
	_arrow_lbl.add_theme_color_override("font_color", COLOR_BORDER)
	if _cached_font:
		_arrow_lbl.add_theme_font_override("font", _cached_font)
	mid_box.add_child(_arrow_lbl)
	cmp_row.add_child(mid_box)

	# 右側：新獲戰利品卡片
	var new_panel := PanelContainer.new()
	new_panel.name = "NewPartCard"
	new_panel.custom_minimum_size = Vector2(320, 220)
	new_panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	new_panel.add_theme_stylebox_override("panel", _create_inner_card_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 16))
	cmp_row.add_child(new_panel)

	var new_margin := MarginContainer.new()
	new_margin.add_theme_constant_override("margin_left", 14)
	new_margin.add_theme_constant_override("margin_right", 14)
	new_margin.add_theme_constant_override("margin_top", 12)
	new_margin.add_theme_constant_override("margin_bottom", 12)
	new_panel.add_child(new_margin)

	var new_vb := VBoxContainer.new()
	new_vb.add_theme_constant_override("separation", 6)
	new_margin.add_child(new_vb)

	_cmp_new_tag_lbl = Label.new()
	_cmp_new_tag_lbl.name = "NewTagLabel"
	_cmp_new_tag_lbl.text = _t("新獲戰利品")
	_cmp_new_tag_lbl.add_theme_font_size_override("font_size", 13)
	_cmp_new_tag_lbl.add_theme_color_override("font_color", COLOR_ORANGE)
	if _cached_font:
		_cmp_new_tag_lbl.add_theme_font_override("font", _cached_font)
	new_vb.add_child(_cmp_new_tag_lbl)

	var new_info_row := HBoxContainer.new()
	new_info_row.add_theme_constant_override("separation", 10)
	new_vb.add_child(new_info_row)

	var new_icon_box := PanelContainer.new()
	new_icon_box.custom_minimum_size = Vector2(56, 56)
	var n_icon_st := StyleBoxFlat.new()
	n_icon_st.bg_color = Color(0.96, 0.95, 0.98, 1)
	n_icon_st.border_color = COLOR_BORDER
	n_icon_st.set_border_width_all(2)
	n_icon_st.set_corner_radius_all(12)
	new_icon_box.add_theme_stylebox_override("panel", n_icon_st)
	new_info_row.add_child(new_icon_box)

	_cmp_new_icon = TextureRect.new()
	_cmp_new_icon.name = "NewSlotIcon"
	_cmp_new_icon.custom_minimum_size = Vector2(44, 44)
	_cmp_new_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_cmp_new_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_cmp_new_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_cmp_new_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	new_icon_box.add_child(_cmp_new_icon)

	var new_text_col := VBoxContainer.new()
	new_text_col.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	new_text_col.add_theme_constant_override("separation", 2)
	new_info_row.add_child(new_text_col)

	_cmp_new_name_lbl = Label.new()
	_cmp_new_name_lbl.name = "NewSlotNameLabel"
	_cmp_new_name_lbl.text = ""
	_cmp_new_name_lbl.add_theme_font_size_override("font_size", 15)
	_cmp_new_name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_cmp_new_name_lbl.add_theme_font_override("font", _cached_font)
	new_text_col.add_child(_cmp_new_name_lbl)

	var new_tier_row := HBoxContainer.new()
	new_tier_row.add_theme_constant_override("separation", 6)
	new_tier_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	new_text_col.add_child(new_tier_row)

	_cmp_new_swatch = ColorRect.new()
	_cmp_new_swatch.name = "NewColorSwatch"
	_cmp_new_swatch.custom_minimum_size = Vector2(10, 18)
	_cmp_new_swatch.mouse_filter = Control.MOUSE_FILTER_IGNORE
	new_tier_row.add_child(_cmp_new_swatch)

	_cmp_new_tier_lbl = Label.new()
	_cmp_new_tier_lbl.name = "NewTierLabel"
	_cmp_new_tier_lbl.text = ""
	_cmp_new_tier_lbl.add_theme_font_size_override("font_size", 13)
	if _cached_font:
		_cmp_new_tier_lbl.add_theme_font_override("font", _cached_font)
	new_tier_row.add_child(_cmp_new_tier_lbl)

	_cmp_new_stats_lbl = Label.new()
	_cmp_new_stats_lbl.name = "NewStatsLabel"
	_cmp_new_stats_lbl.text = ""
	_cmp_new_stats_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_cmp_new_stats_lbl.add_theme_font_size_override("font_size", 13)
	_cmp_new_stats_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_cmp_new_stats_lbl.add_theme_font_override("font", _cached_font)
	new_vb.add_child(_cmp_new_stats_lbl)

	# 新件副詞條清單
	_cmp_new_affixes_box = VBoxContainer.new()
	_cmp_new_affixes_box.name = "NewAffixesBox"
	_cmp_new_affixes_box.add_theme_constant_override("separation", 2)
	new_vb.add_child(_cmp_new_affixes_box)

	# ── 底部按鈕區（按鈕熱區 >= 48px）──
	var btn_row := HBoxContainer.new()
	btn_row.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_row.add_theme_constant_override("separation", 20)
	v.add_child(btn_row)

	_btn_cancel = Button.new()
	_btn_cancel.name = "BtnCancelReplace"
	_btn_cancel.text = _t("取消替換")
	_btn_cancel.custom_minimum_size = Vector2(210, 52)
	_btn_cancel.focus_mode = Control.FOCUS_NONE
	_style_button(_btn_cancel, COLOR_CARD_WARM, COLOR_BORDER)
	_btn_cancel.pressed.connect(_on_cancel_pressed)
	btn_row.add_child(_btn_cancel)

	_btn_confirm = Button.new()
	_btn_confirm.name = "BtnConfirmReplace"
	_btn_confirm.text = _t("確認替換")
	_btn_confirm.custom_minimum_size = Vector2(210, 52)
	_btn_confirm.focus_mode = Control.FOCUS_NONE
	_style_button(_btn_confirm, COLOR_SKY, COLOR_BORDER)
	_btn_confirm.pressed.connect(_on_confirm_pressed)
	btn_row.add_child(_btn_confirm)


func refresh_display() -> void:
	if _compare_card == null:
		return

	if _cmp_title_lbl:
		_cmp_title_lbl.text = _t("裝備替換確認")
	if _cmp_sub_lbl:
		_cmp_sub_lbl.text = _t("該部位已有穿戴裝備，是否確認替換？")
	if _cmp_old_tag_lbl:
		_cmp_old_tag_lbl.text = _t("現有裝備")
	if _cmp_new_tag_lbl:
		_cmp_new_tag_lbl.text = _t("新獲戰利品")
	if _btn_cancel:
		_btn_cancel.text = _t("取消替換")
	if _btn_confirm:
		_btn_confirm.text = _t("確認替換")

	# 槽位名稱
	if _cmp_slot_lbl:
		_cmp_slot_lbl.text = _t("部位：%s") % _t(_slot_name)

	# 填寫舊件
	_fill_part_view(
		_old_inst,
		_cmp_old_name_lbl,
		_cmp_old_icon,
		_cmp_old_swatch,
		_cmp_old_tier_lbl,
		_cmp_old_stats_lbl,
		_cmp_old_affixes_box
	)

	# 填寫新件
	_fill_part_view(
		_new_inst,
		_cmp_new_name_lbl,
		_cmp_new_icon,
		_cmp_new_swatch,
		_cmp_new_tier_lbl,
		_cmp_new_stats_lbl,
		_cmp_new_affixes_box
	)


func _fill_part_view(
	inst: Dictionary,
	name_lbl: Label,
	icon_rect: TextureRect,
	swatch: ColorRect,
	tier_lbl: Label,
	stats_lbl: Label,
	affixes_box: VBoxContainer
) -> void:
	if inst.is_empty():
		if name_lbl: name_lbl.text = _t("（空）")
		if tier_lbl: tier_lbl.text = ""
		if stats_lbl: stats_lbl.text = ""
		return

	var eq = _eq_sys()
	var sdb = _sprite_db()

	# 名稱
	if name_lbl:
		var dname: String = ""
		if eq != null and eq.has_method("display_name"):
			dname = str(eq.call("display_name", inst))
		else:
			dname = str(inst.get("name", ""))
		name_lbl.text = dname

	# 圖示
	if icon_rect:
		if sdb != null and sdb.has_method("equip_icon_for_inst"):
			var tex: Texture2D = sdb.call("equip_icon_for_inst", inst)
			icon_rect.texture = tex
		else:
			icon_rect.texture = null

	# 品質與顏色
	var q_id := str(inst.get("quality", "common"))
	var q_lbl := str(inst.get("quality_label", ""))
	if q_lbl.is_empty():
		match q_id:
			"uncommon": q_lbl = "良品"
			"rare": q_lbl = "上品"
			"epic": q_lbl = "秘寶"
			_: q_lbl = "凡品"
	var q_color := _get_quality_color(q_id)

	if swatch:
		swatch.color = q_color

	if tier_lbl:
		tier_lbl.text = _t("【%s】") % _t(q_lbl)
		tier_lbl.add_theme_color_override("font_color", q_color if q_id != "common" else COLOR_TEXT_DARK)

	# rolled 數值
	if stats_lbl:
		stats_lbl.text = _format_rolled_stats(inst)

	# 副詞條全文
	if affixes_box:
		for c in affixes_box.get_children():
			c.queue_free()

		var aff_list: Array = inst.get("affixes", [])
		if aff_list.is_empty():
			var no_aff := Label.new()
			no_aff.name = "NoAffixesLabel"
			no_aff.text = _t("無副詞條")
			no_aff.add_theme_font_size_override("font_size", 12)
			no_aff.add_theme_color_override("font_color", COLOR_TEXT_MUTED)
			if _cached_font:
				no_aff.add_theme_font_override("font", _cached_font)
			affixes_box.add_child(no_aff)
		else:
			for aff in aff_list:
				if aff is Dictionary:
					var text_line := ""
					if eq != null and eq.has_method("format_affix"):
						text_line = str(eq.call("format_affix", aff as Dictionary))
					else:
						text_line = str((aff as Dictionary).get("name", ""))
					if not text_line.is_empty():
						var aff_lbl := Label.new()
						aff_lbl.text = "• " + text_line
						aff_lbl.add_theme_font_size_override("font_size", 12)
						aff_lbl.add_theme_color_override("font_color", Color(0.18, 0.45, 0.8))
						if _cached_font:
							aff_lbl.add_theme_font_override("font", _cached_font)
						affixes_box.add_child(aff_lbl)


func _get_quality_color(q: String) -> Color:
	match q:
		"common":
			return Color("#888888")
		"uncommon":
			return COLOR_MINT
		"rare":
			return COLOR_SKY
		"epic":
			return COLOR_PURPLE
		_:
			return COLOR_BORDER


func _format_rolled_stats(inst: Dictionary) -> String:
	var r: Dictionary = inst.get("rolled", {})
	var parts: Array[String] = []
	var atk: int = int(r.get("atk", 0))
	var def: int = int(r.get("def", 0))
	var hp: int = int(r.get("hp", 0))
	var crit: float = float(r.get("crit", 0.0))
	var crit_dmg: float = float(r.get("crit_dmg", 0.0))

	if atk > 0: parts.append(_t("攻+%d") % atk)
	if def > 0: parts.append(_t("防+%d") % def)
	if hp > 0: parts.append(_t("血+%d") % hp)
	if crit > 0.0: parts.append(_t("暴擊+%.1f%%") % crit)
	if crit_dmg > 0.0: parts.append(_t("暴傷+%.0f%%") % crit_dmg)

	if parts.is_empty():
		return _t("基礎屬性")
	return " · ".join(parts)


static func _play_ui_audio() -> void:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var am = (tree as SceneTree).root.get_node_or_null("AudioManager")
		if am and am.has_method("play_ui"):
			am.call("play_ui")


func _on_confirm_pressed() -> void:
	_play_ui_audio()
	confirmed.emit()
	if _on_confirm.is_valid():
		_on_confirm.call()
	if _close_mode == "free":
		queue_free()
	else:
		visible = false


func _on_cancel_pressed() -> void:
	_play_ui_audio()
	cancelled.emit()
	if _on_cancel.is_valid():
		_on_cancel.call()
	if _close_mode == "free":
		queue_free()
	else:
		visible = false


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
