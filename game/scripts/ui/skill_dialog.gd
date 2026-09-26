class_name SkillDialog
extends Control
## 《發條之心》招式與技能體系彈窗 (SkillDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 760px、高 540px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，底部按鈕高 >= 50px。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A。
## 4. 圓角 16~22px，主要按鈕立體果凍厚底 (bottom border 5~6px)。
## 5. 字級 14~22px 加粗帶深色厚描邊，零 13px 以下小字。
## 6. 零系統 Emoji、零字元圖示。
## 7. 六語系多國語言支援 (ContentLoc / Loc.locale_changed 即時切換)。

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
const COLOR_GOLD        := Color("#FFD028")  ## 金黃
const COLOR_ORANGE      := Color("#FFA010")  ## 暖橘
const COLOR_MINT        := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY         := Color("#38A0FF")  ## 天藍
const COLOR_PINK        := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER      := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM    := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM   := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_GOLD   := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_CARD_SKY    := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_MUTED  := Color("#EFEBE0")  ## 壓暗奶油底（未解鎖專用）
const COLOR_BORDER_MUTED:= Color("#D2CCC0")  ## 壓暗淡邊框

## ── 亮底合規文字色 ──
const COLOR_TEXT_DARK   := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD   := Color("#9A6B00")  ## 壓明度金黃
const COLOR_TEXT_ORANGE := Color("#C2600A")  ## 壓明度暖橘
const COLOR_TEXT_MUTED  := Color("#6B6680")  ## 次要輔助文字
const COLOR_TEXT_DIM    := Color("#888294")  ## 壓暗提示文字

const PROF_ORDER := ["knight", "viking", "ninja", "monk", "mage", "ranger"]

var _dialog_card: PanelContainer
var _title_lbl: Label
var _sub_title_lbl: Label
var _close_x_btn: Button
var _bottom_close_btn: Button

## 戰鬥優先區塊
var _priority_card: PanelContainer
var _prio_title_lbl: Label
var _prio_normal_lbl: Label
var _prio_panic_lbl: Label

## 職業切換 Tab
var _tab_row: HBoxContainer
var _tab_buttons: Dictionary = {}  ## prof_key -> Button
var _selected_prof: String = "knight"

## 招式卡片清單
var _scroll_box: ScrollContainer
var _skill_cards_box: VBoxContainer
var _card_nodes: Dictionary = {}  ## skill_id -> Dictionary of nodes

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
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	_refresh_display()


func _ready() -> void:
	name = "SkillDialog"
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	z_index = 80

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_detect_default_profession()

	if not _built:
		_build_ui()
	_update_ui_texts()
	_refresh_display()


func _detect_default_profession() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var sk: Node = (loop as SceneTree).root.get_node_or_null("SkillSystem")
		if sk != null and sk.has_method("profession_of") and sk.has_method("_path_id"):
			var pid: String = str(sk.call("_path_id"))
			var p: String = str(sk.call("profession_of", pid))
			if p in PROF_ORDER:
				_selected_prof = p


func _build_ui() -> void:
	_built = true
	for c in get_children():
		c.queue_free()

	# 1. 全螢幕半透明遮罩
	var scrim := ColorRect.new()
	scrim.name = "ModalScrim"
	scrim.set_anchors_preset(Control.PRESET_FULL_RECT)
	scrim.color = Color(0.12, 0.10, 0.15, 0.75)
	scrim.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(scrim)

	# 2. 置中卡片 (760 x 540)
	var card := PanelContainer.new()
	card.name = "DialogCard"
	card.set_anchors_preset(Control.PRESET_CENTER)
	card.offset_left = -380
	card.offset_top = -270
	card.offset_right = 380
	card.offset_bottom = 270
	card.custom_minimum_size = Vector2(760, 540)
	card.mouse_filter = Control.MOUSE_FILTER_STOP

	var card_sb := StyleBoxFlat.new()
	card_sb.bg_color = COLOR_BG_CREAM
	card_sb.border_color = COLOR_BORDER
	card_sb.set_border_width_all(2)
	card_sb.border_width_bottom = 6
	card_sb.set_corner_radius_all(22)
	card_sb.content_margin_left = 22
	card_sb.content_margin_right = 22
	card_sb.content_margin_top = 18
	card_sb.content_margin_bottom = 18
	card_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	card_sb.shadow_size = 8
	card_sb.shadow_offset = Vector2(0, 4)
	card.add_theme_stylebox_override("panel", card_sb)
	add_child(card)
	_dialog_card = card

	var root_v := VBoxContainer.new()
	root_v.add_theme_constant_override("separation", 10)
	root_v.set_anchors_preset(Control.PRESET_FULL_RECT)
	card.add_child(root_v)

	# 3. 頂部列（標題 + 右上✕）
	var top_h := HBoxContainer.new()
	top_h.add_theme_constant_override("separation", 8)
	root_v.add_child(top_h)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.add_theme_constant_override("separation", 2)
	top_h.add_child(title_box)

	_title_lbl = Label.new()
	_title_lbl.name = "TitleLabel"
	_apply_font(_title_lbl, 22, COLOR_TEXT_DARK, true)
	title_box.add_child(_title_lbl)

	_sub_title_lbl = Label.new()
	_sub_title_lbl.name = "SubTitleLabel"
	_apply_font(_sub_title_lbl, 13, COLOR_TEXT_MUTED)
	title_box.add_child(_sub_title_lbl)

	_close_x_btn = Button.new()
	_close_x_btn.name = "BtnCloseX"
	_close_x_btn.text = "✕"
	_close_x_btn.custom_minimum_size = Vector2(50, 50)
	_style_jelly_btn(_close_x_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 18, 5)
	_close_x_btn.pressed.connect(_on_close_pressed)
	top_h.add_child(_close_x_btn)

	# 4. 戰鬥優先摘要條
	_priority_card = PanelContainer.new()
	_priority_card.name = "PriorityCard"
	var prio_sb := StyleBoxFlat.new()
	prio_sb.bg_color = COLOR_CARD_GOLD
	prio_sb.border_color = COLOR_BORDER
	prio_sb.set_border_width_all(2)
	prio_sb.border_width_bottom = 4
	prio_sb.set_corner_radius_all(14)
	prio_sb.content_margin_left = 16
	prio_sb.content_margin_right = 16
	prio_sb.content_margin_top = 8
	prio_sb.content_margin_bottom = 8
	_priority_card.add_theme_stylebox_override("panel", prio_sb)
	root_v.add_child(_priority_card)

	var prio_h := HBoxContainer.new()
	prio_h.add_theme_constant_override("separation", 16)
	_priority_card.add_child(prio_h)

	_prio_title_lbl = Label.new()
	_prio_title_lbl.name = "PrioTitleLabel"
	_apply_font(_prio_title_lbl, 15, COLOR_TEXT_ORANGE, true)
	prio_h.add_child(_prio_title_lbl)

	_prio_normal_lbl = Label.new()
	_prio_normal_lbl.name = "PrioNormalLabel"
	_apply_font(_prio_normal_lbl, 14, COLOR_TEXT_DARK)
	prio_h.add_child(_prio_normal_lbl)

	_prio_panic_lbl = Label.new()
	_prio_panic_lbl.name = "PrioPanicLabel"
	_apply_font(_prio_panic_lbl, 14, COLOR_TEXT_DARK)
	prio_h.add_child(_prio_panic_lbl)

	# 5. 職業分頁按鈕群 (2x3 或單列橫滑)
	_tab_row = HBoxContainer.new()
	_tab_row.name = "TabRow"
	_tab_row.add_theme_constant_override("separation", 8)
	root_v.add_child(_tab_row)

	_tab_buttons.clear()
	for prof_key in PROF_ORDER:
		var tbtn := Button.new()
		tbtn.name = "TabBtn_" + prof_key
		tbtn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		tbtn.custom_minimum_size = Vector2(0, 48)
		tbtn.pressed.connect(func(): _select_profession(prof_key))
		_tab_row.add_child(tbtn)
		_tab_buttons[prof_key] = tbtn

	# 6. 招式卡片滾動區
	_scroll_box = ScrollContainer.new()
	_scroll_box.name = "SkillScrollBox"
	_scroll_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_scroll_box.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root_v.add_child(_scroll_box)

	_skill_cards_box = VBoxContainer.new()
	_skill_cards_box.name = "SkillCardsBox"
	_skill_cards_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_skill_cards_box.add_theme_constant_override("separation", 10)
	_scroll_box.add_child(_skill_cards_box)

	# 7. 底部關閉按鈕
	var bot_h := HBoxContainer.new()
	bot_h.alignment = BoxContainer.ALIGNMENT_END
	root_v.add_child(bot_h)

	_bottom_close_btn = Button.new()
	_bottom_close_btn.name = "BtnCloseBottom"
	_bottom_close_btn.custom_minimum_size = Vector2(140, 50)
	_style_jelly_btn(_bottom_close_btn, COLOR_CARD_WARM, COLOR_TEXT_DARK, 16, 5)
	_bottom_close_btn.pressed.connect(_on_close_pressed)
	bot_h.add_child(_bottom_close_btn)


func _select_profession(prof_key: String) -> void:
	if prof_key != _selected_prof:
		_selected_prof = prof_key
		_refresh_display()


func _on_close_pressed() -> void:
	closed.emit()
	queue_free()


func _update_ui_texts() -> void:
	if _title_lbl:
		_title_lbl.text = _t("旅途 · 招式心法")
	if _sub_title_lbl:
		_sub_title_lbl.text = _t("鐵匠養器 · 星途養魂 · 旅途養招 · 出招隨裝備武器流轉")
	if _close_x_btn:
		_close_x_btn.text = "✕"
	if _bottom_close_btn:
		_bottom_close_btn.text = _t("關閉")

	if _prio_title_lbl:
		_prio_title_lbl.text = _t("戰鬥優先")

	# 更新職業按鈕文字
	var sk := _get_skill_system()
	for prof_key in PROF_ORDER:
		if _tab_buttons.has(prof_key):
			var btn: Button = _tab_buttons[prof_key]
			var raw_pname: String = str(sk.PROFESSION_NAME.get(prof_key, prof_key)) if sk else prof_key
			var loc_pname: String = ContentLoc.text("ui", raw_pname)
			btn.text = loc_pname


func _refresh_display() -> void:
	var sk := _get_skill_system()
	if sk == null:
		return

	# 1. 更新戰鬥優先資訊
	var kit_full: Dictionary = sk.pick_battle_skill(1.0)
	var kit_panic: Dictionary = sk.pick_battle_skill(0.35)
	var normal_name: String = str(kit_full.get("name", "—"))
	var panic_name: String = str(kit_panic.get("name", "—"))

	if _prio_normal_lbl:
		_prio_normal_lbl.text = _t("平常出招：%s") % normal_name
	if _prio_panic_lbl:
		_prio_panic_lbl.text = _t("危急治療：%s") % panic_name

	# 2. 更新 Tab 樣式
	for prof_key in PROF_ORDER:
		if _tab_buttons.has(prof_key):
			var btn: Button = _tab_buttons[prof_key]
			var is_sel: bool = (prof_key == _selected_prof)
			if is_sel:
				_style_jelly_btn(btn, COLOR_GOLD, COLOR_TEXT_DARK, 16, 5)
			else:
				_style_jelly_btn(btn, COLOR_CARD_WARM, COLOR_TEXT_MUTED, 15, 3)

	# 3. 重新構建當前職業招式卡片
	for c in _skill_cards_box.get_children():
		c.queue_free()
	_card_nodes.clear()

	var weapon_lines: Array = sk.weapons_of_profession(_selected_prof)
	for w in weapon_lines:
		var wline := str(w)
		var wlabel := _weapon_label(wline)

		var line_hdr := Label.new()
		_apply_font(line_hdr, 16, COLOR_TEXT_ORANGE, true)
		line_hdr.text = "【%s】" % wlabel
		_skill_cards_box.add_child(line_hdr)

		for d in sk.CATALOG:
			if str(d.get("line", "")) != wline:
				continue
			var sid := str(d.get("id", ""))
			var card := _build_skill_card(sid, d, sk)
			_skill_cards_box.add_child(card)


func _build_skill_card(sid: String, raw_d: Dictionary, sk: Node) -> PanelContainer:
	var loc_d: Dictionary = sk.def_of(sid)
	var s_name := str(loc_d.get("name", str(raw_d.get("name", sid))))
	var s_desc := str(loc_d.get("desc", str(raw_d.get("desc", ""))))
	var s_unlock := str(loc_d.get("unlock_hint", str(raw_d.get("unlock_hint", _t("未解鎖")))))
	var slv: int = sk.get_lv(sid)
	var is_learned: bool = sk.is_learned(sid)
	var is_unlocked: bool = sk.is_unlocked(sid)
	var cur_m: int = sk.get_mastery(sid)
	var need_m: int = sk.mastery_need_for_next(sid)

	var card := PanelContainer.new()
	card.name = "SkillCard_" + sid
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var csb := StyleBoxFlat.new()
	if is_learned:
		csb.bg_color = COLOR_CARD_WARM
		csb.border_color = COLOR_BORDER
	else:
		csb.bg_color = COLOR_CARD_MUTED
		csb.border_color = COLOR_BORDER_MUTED
	csb.set_border_width_all(2)
	csb.border_width_bottom = 4
	csb.set_corner_radius_all(16)
	csb.content_margin_left = 16
	csb.content_margin_right = 16
	csb.content_margin_top = 10
	csb.content_margin_bottom = 10
	card.add_theme_stylebox_override("panel", csb)

	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	card.add_child(vbox)

	# 頂行：招式名稱 + 階位標籤
	var top_row := HBoxContainer.new()
	top_row.add_theme_constant_override("separation", 10)
	vbox.add_child(top_row)

	var name_lbl := Label.new()
	name_lbl.name = "SkillName"
	name_lbl.text = s_name
	_apply_font(name_lbl, 17, COLOR_TEXT_DARK, true)
	name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_row.add_child(name_lbl)

	var status_lbl := Label.new()
	status_lbl.name = "SkillStatus"
	if not is_learned:
		if is_unlocked:
			status_lbl.text = _t("可體悟")
			_apply_font(status_lbl, 13, COLOR_TEXT_GOLD, true)
		else:
			status_lbl.text = _t("未解鎖")
			_apply_font(status_lbl, 13, COLOR_TEXT_DIM)
	elif slv >= sk.MAX_LV:
		status_lbl.text = _t("Lv.%d · 極階") % slv
		_apply_font(status_lbl, 13, COLOR_TEXT_ORANGE, true)
	else:
		status_lbl.text = "Lv.%d" % slv
		_apply_font(status_lbl, 13, COLOR_TEXT_DARK, true)
	top_row.add_child(status_lbl)

	# 熟練度文字
	if is_learned and slv < sk.MAX_LV:
		var m_lbl := Label.new()
		m_lbl.name = "MasteryLabel"
		m_lbl.text = _t("熟練 %d/%d") % [cur_m, need_m]
		_apply_font(m_lbl, 13, COLOR_TEXT_MUTED)
		top_row.add_child(m_lbl)

	# 說明行
	var desc_lbl := Label.new()
	desc_lbl.name = "SkillDesc"
	desc_lbl.text = s_desc
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_apply_font(desc_lbl, 14, COLOR_TEXT_DARK)
	vbox.add_child(desc_lbl)

	# 下級預覽句（若已習得且未滿級）
	var preview_lbl: Label = null
	if is_learned and slv < sk.MAX_LV:
		var next_key := "lv%d" % (slv + 1)
		var preview: String = str(loc_d.get(next_key, str(raw_d.get(next_key, _t("下級：效果↑")))))
		preview_lbl = Label.new()
		preview_lbl.name = "SkillPreview"
		preview_lbl.text = _t("下級預覽：%s") % preview
		_apply_font(preview_lbl, 13, COLOR_TEXT_GOLD)
		vbox.add_child(preview_lbl)

	# 解鎖提示（若未習得）
	var hint_lbl: Label = null
	if not is_learned:
		hint_lbl = Label.new()
		hint_lbl.name = "SkillHint"
		hint_lbl.text = _t("解鎖條件：%s") % s_unlock
		_apply_font(hint_lbl, 13, COLOR_TEXT_MUTED)
		vbox.add_child(hint_lbl)

	_card_nodes[sid] = {
		"card": card,
		"name": name_lbl,
		"status": status_lbl,
		"desc": desc_lbl,
		"preview": preview_lbl,
		"hint": hint_lbl,
	}

	return card


func _weapon_label(wid: String) -> String:
	match wid:
		"sword": return _t("劍")
		"spear": return _t("槍")
		"axe": return _t("斧")
		"hammer": return _t("鎚")
		"dagger": return _t("匕首")
		"dart": return _t("鏢")
		"fist": return _t("拳")
		"claw": return _t("爪")
		"magic": return _t("杖")
		"crystal": return _t("水晶")
		"bow": return _t("弓")
		"gun": return _t("火槍")
		_: return wid


func _get_skill_system() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("SkillSystem")
	return null


func _apply_font(lbl: Label, size: int, color: Color, bold: bool = false) -> void:
	if _cached_font != null:
		lbl.add_theme_font_override("font", _cached_font)
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	if bold:
		lbl.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.95))
		lbl.add_theme_constant_override("outline_size", 2)


func _style_jelly_btn(btn: Button, bg_col: Color, text_col: Color, font_sz: int, bottom_border: int = 5) -> void:
	if _cached_font != null:
		btn.add_theme_font_override("font", _cached_font)
	btn.add_theme_font_size_override("font_size", font_sz)
	btn.add_theme_color_override("font_color", text_col)
	btn.add_theme_color_override("font_hover_color", text_col)
	btn.add_theme_color_override("font_pressed_color", text_col)
	btn.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.8))
	btn.add_theme_constant_override("outline_size", 1)

	var sb := StyleBoxFlat.new()
	sb.bg_color = bg_col
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(16)
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.15)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = bg_col.lightened(0.08)

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2
	sb_p.content_margin_top = 8
	sb_p.content_margin_bottom = 4

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb_h)


## ── 供單元測試與自動化驗證的查詢 API ──
func get_skill_card(sid: String) -> PanelContainer:
	if _card_nodes.has(sid):
		return _card_nodes[sid].get("card")
	return null


func get_skill_name_text(sid: String) -> String:
	if _card_nodes.has(sid) and _card_nodes[sid].get("name"):
		return (_card_nodes[sid]["name"] as Label).text
	return ""


func get_skill_desc_text(sid: String) -> String:
	if _card_nodes.has(sid) and _card_nodes[sid].get("desc"):
		return (_card_nodes[sid]["desc"] as Label).text
	return ""


func get_skill_hint_text(sid: String) -> String:
	if _card_nodes.has(sid) and _card_nodes[sid].get("hint"):
		return (_card_nodes[sid]["hint"] as Label).text
	return ""


func get_skill_preview_text(sid: String) -> String:
	if _card_nodes.has(sid) and _card_nodes[sid].get("preview"):
		return (_card_nodes[sid]["preview"] as Label).text
	return ""


func get_title_text() -> String:
	return _title_lbl.text if _title_lbl else ""
