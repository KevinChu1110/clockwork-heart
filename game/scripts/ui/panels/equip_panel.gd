extends RefCounted
## 裝備面板：真正多武器欄（3）＋防具／飾品＋背包。
##
## 從 main.gd 抽出。不走 ui_panel()，自己畫圖示格子。
## 宿主介面見 main.gd「面板宿主介面」。導覽走 ui_goto()。
##
## 刻意不用 class_name（見 AGENTS.md「寫測試的規矩」）。

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const CoreSystem := preload("res://scripts/systems/core_system.gd")

var _host: Node
## 點空武器欄後，等背包選一把裝進去（-1＝無）
var _pending_loadout: int = -1
var _layer: Control = null
var _connected_loc: bool = false
var _core_hint_label: Label = null


static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


static func _weapon_line_name(line: String) -> String:
	if line == "":
		return ""
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var eq: Node = (tree as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq != null and eq.has_method("weapon_line_name"):
			return str(eq.call("weapon_line_name", line))
		var dt: Node = (tree as SceneTree).root.get_node_or_null("DataTables")
		if dt != null and dt.has_method("weapon_class_def"):
			var cdef: Dictionary = dt.call("weapon_class_def", line)
			var nm := str(cdef.get("name", ""))
			if nm != "":
				return nm
	return line


func _init(host: Node) -> void:
	_host = host


func _on_locale_changed(_new_loc: String = "") -> void:
	if is_instance_valid(_layer) and _layer.is_inside_tree():
		open()


func open() -> void:
	if not _connected_loc:
		var tree := Engine.get_main_loop()
		if tree is SceneTree and (tree as SceneTree).root != null:
			var loc: Node = (tree as SceneTree).root.get_node_or_null("Loc")
			if loc and loc.has_signal("locale_changed"):
				if not loc.locale_changed.is_connected(_on_locale_changed):
					loc.locale_changed.connect(_on_locale_changed)
				_connected_loc = true
	EquipmentSystem._ensure_state()
	_host.ui_clear_host()
	_host.ui_reset_fade()

	var layer := Control.new()
	layer.name = "EquipLayer"
	layer.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	layer.mouse_filter = Control.MOUSE_FILTER_STOP
	_layer = layer
	_host.ui_host().add_child(layer)
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.08, 0.06, 0.12, 0.65)
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(bg)
	var scroll := ScrollContainer.new()
	scroll.name = "EquipScroll"
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	layer.add_child(scroll)
	var scroll_margin := MarginContainer.new()
	scroll_margin.name = "ScrollMargin"
	scroll_margin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll_margin.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll_margin.add_theme_constant_override("margin_top", 16)
	scroll_margin.add_theme_constant_override("margin_bottom", 24)
	scroll.add_child(scroll_margin)
	var center := CenterContainer.new()
	center.name = "EquipCenter"
	center.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	center.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll_margin.add_child(center)
	var card := PanelContainer.new()
	card.name = "EquipCard"
	card.custom_minimum_size = Vector2(560, 0)
	card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	center.add_child(card)
	var margin := MarginContainer.new()
	for m in ["margin_left", "margin_right", "margin_top", "margin_bottom"]:
		margin.add_theme_constant_override(m, 12 if m != "margin_top" else 10)
	card.add_child(margin)
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	margin.add_child(root)

	var title := Label.new()
	title.text = _t("裝備")
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(title)

	var b := EquipmentSystem.bonus_totals()
	var cb: Dictionary = CoreSystem.total_core_bonuses() if CoreSystem != null else {}
	var sum := Label.new()
	sum.text = _t("總加成  攻+%d  防+%d  血+%d  ·  暴擊 %.1f%%  暴傷 +%.0f%%") % [
		int(b.atk) + int(cb.get("atk", 0)),
		int(b.def) + int(cb.get("def", 0)),
		int(b.hp) + int(cb.get("hp", 0)),
		GameState.effective_crit(), GameState.effective_crit_dmg(),
	]
	sum.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sum.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	sum.add_theme_font_size_override("font_size", 12)
	sum.add_theme_color_override("font_color", UiStyle.INK_DIM)
	root.add_child(sum)

	## ── 真正多武器欄 ──
	var wh := Label.new()
	wh.text = _t("武器欄（戰鬥耗盡自動切換 · 第2欄 Lv10 · 第3欄 Lv16）")
	wh.add_theme_font_size_override("font_size", 13)
	wh.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(wh)

	if _pending_loadout >= 0:
		var hint := Label.new()
		hint.text = _t("▶ 請點背包中的【武器】裝入第 %d 欄（或點取消）") % [_pending_loadout + 1]
		hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		hint.add_theme_font_size_override("font_size", 12)
		hint.add_theme_color_override("font_color", Color(0.75, 0.35, 0.2))
		root.add_child(hint)
		var cancel := Button.new()
		cancel.text = _t("取消選欄")
		UiStyle.style_button(cancel, false)
		cancel.pressed.connect(func():
			AudioManager.play_ui()
			_pending_loadout = -1
			open()
		)
		root.add_child(cancel)

	var loadout_row := HBoxContainer.new()
	loadout_row.alignment = BoxContainer.ALIGNMENT_CENTER
	loadout_row.add_theme_constant_override("separation", 10)
	root.add_child(loadout_row)
	for i in EquipmentSystem.WEAPON_LOADOUT_SIZE:
		loadout_row.add_child(_loadout_card(i))

	## ── 防具 ──
	var armor_h := Label.new()
	armor_h.text = _t("防具")
	armor_h.add_theme_font_size_override("font_size", 13)
	armor_h.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(armor_h)
	var armor_row := HBoxContainer.new()
	armor_row.alignment = BoxContainer.ALIGNMENT_CENTER
	root.add_child(armor_row)
	armor_row.add_child(_slot_card("armor"))

	## ── 機芯五槽 ──
	var core_h := Label.new()
	core_h.text = _t("機芯五槽")
	core_h.add_theme_font_size_override("font_size", 13)
	core_h.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(core_h)

	var core_row := HBoxContainer.new()
	core_row.name = "CoreSlotsRow"
	core_row.alignment = BoxContainer.ALIGNMENT_CENTER
	core_row.add_theme_constant_override("separation", 8)
	root.add_child(core_row)

	_core_hint_label = Label.new()
	_core_hint_label.name = "CoreHintLabel"
	_core_hint_label.text = _t("點擊機芯部位可檢視構造說明")
	_core_hint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_core_hint_label.add_theme_font_size_override("font_size", 11)
	_core_hint_label.add_theme_color_override("font_color", UiStyle.INK_DIM)

	for def in SpriteDB.CORE_SLOT_DEFS:
		core_row.add_child(_core_slot_card(def))

	root.add_child(_core_hint_label)

	## ── 機芯部件背包 ──
	var core_parts: Array = CoreSystem.get_inventory() if CoreSystem != null else []
	if not core_parts.is_empty():
		var cbag_h := Label.new()
		cbag_h.text = _t("機芯部件背包（點擊替換裝備）")
		cbag_h.add_theme_font_size_override("font_size", 13)
		cbag_h.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
		root.add_child(cbag_h)

		var cbag_grid := GridContainer.new()
		cbag_grid.name = "CoreBagGrid"
		cbag_grid.columns = 4
		cbag_grid.add_theme_constant_override("h_separation", 8)
		cbag_grid.add_theme_constant_override("v_separation", 8)
		root.add_child(cbag_grid)

		var cn := 0
		for cp in core_parts:
			if cn >= 12:
				break
			cbag_grid.add_child(_core_bag_cell(cp))
			cn += 1

	## ── 飾品六槽 ──
	var acc_h := Label.new()
	if EquipmentSystem.accessories_unlocked():
		acc_h.text = _t("飾品六槽")
	else:
		acc_h.text = _t("飾品六槽（Lv%d 開放）") % EquipmentSystem.ACCESSORY_LEVEL_REQ
	acc_h.add_theme_font_size_override("font_size", 13)
	acc_h.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(acc_h)
	var acc_grid := GridContainer.new()
	acc_grid.columns = 3
	acc_grid.add_theme_constant_override("h_separation", 8)
	acc_grid.add_theme_constant_override("v_separation", 8)
	root.add_child(acc_grid)
	for s in EquipmentSystem.ACCESSORY_SLOTS:
		acc_grid.add_child(_slot_card(s, true, EquipmentSystem.accessories_unlocked()))

	## ── 背包 ──
	var bag_h := Label.new()
	if _pending_loadout >= 0:
		bag_h.text = _t("背包（點武器裝入第 %d 欄）") % [_pending_loadout + 1]
	else:
		bag_h.text = _t("背包（點擊裝備）")
	bag_h.add_theme_font_size_override("font_size", 13)
	bag_h.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	root.add_child(bag_h)

	var bag_grid := GridContainer.new()
	bag_grid.columns = 4
	bag_grid.add_theme_constant_override("h_separation", 8)
	bag_grid.add_theme_constant_override("v_separation", 8)
	root.add_child(bag_grid)
	var n := 0
	for e in GameState.equip_bag:
		if n >= 12:
			break
		bag_grid.add_child(_bag_cell(e))
		n += 1
	if n == 0:
		var empty := Label.new()
		empty.text = _t("背包尚無裝備。野外掉落或找釘釘鍛造。")
		empty.add_theme_font_size_override("font_size", 12)
		empty.add_theme_color_override("font_color", UiStyle.INK_DIM)
		root.add_child(empty)

	var actions := HBoxContainer.new()
	actions.alignment = BoxContainer.ALIGNMENT_CENTER
	actions.add_theme_constant_override("separation", 8)
	root.add_child(actions)
	var btn_back := Button.new()
	btn_back.text = _t("返回")
	UiStyle.style_button(btn_back, true)
	btn_back.pressed.connect(func():
		AudioManager.play_ui()
		_pending_loadout = -1
		_host.ui_goto("hub")
	)
	actions.add_child(btn_back)
	_host.ui_refresh_hud()


func _loadout_card(index: int) -> Control:
	var unlocked := EquipmentSystem.loadout_slot_unlocked(index)
	var uid := EquipmentSystem.loadout_uid(index) if unlocked else ""
	var inst := EquipmentSystem.weapon_inst(uid)
	var active := unlocked and index == EquipmentSystem.active_loadout_index() and uid != ""
	var picking := _pending_loadout == index

	var box := VBoxContainer.new()
	box.custom_minimum_size = Vector2(150, 0)
	box.add_theme_constant_override("separation", 4)

	var lab := Label.new()
	if not unlocked:
		lab.text = _t("欄 %d · Lv%d") % [index + 1, EquipmentSystem.loadout_unlock_level(index)]
	elif active:
		lab.text = _t("欄 %d · 使用中") % [index + 1]
	else:
		lab.text = _t("欄 %d") % [index + 1]
	lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lab.add_theme_font_size_override("font_size", 12)
	lab.add_theme_color_override("font_color", UiStyle.KEY_STRONG if active else UiStyle.INK_DIM)
	box.add_child(lab)

	var cell := PanelContainer.new()
	cell.custom_minimum_size = Vector2(130, 130)
	var st := StyleBoxFlat.new()
	if not unlocked:
		st.bg_color = Color(0.88, 0.88, 0.9, 1)
		st.border_color = Color(0.6, 0.6, 0.65, 0.7)
	elif picking:
		st.bg_color = Color(1.0, 0.95, 0.88, 1)
		st.border_color = Color(0.9, 0.55, 0.2, 1)
	elif active:
		st.bg_color = Color(0.92, 0.96, 1.0, 1)
		st.border_color = Color(0.25, 0.55, 0.9, 1)
	else:
		st.bg_color = Color(0.94, 0.92, 0.95, 1)
		st.border_color = UiStyle.WOOD
	st.set_border_width_all(3 if active or picking else 2)
	st.set_corner_radius_all(8)
	cell.add_theme_stylebox_override("panel", st)
	box.add_child(cell)

	var inner := VBoxContainer.new()
	inner.alignment = BoxContainer.ALIGNMENT_CENTER
	cell.add_child(inner)

	if not unlocked:
		var lock_l := Label.new()
		lock_l.text = _t("未解鎖")
		lock_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lock_l.add_theme_font_size_override("font_size", 12)
		lock_l.add_theme_color_override("font_color", UiStyle.INK_DIM)
		inner.add_child(lock_l)
		var need := Label.new()
		need.text = _t("需要 Lv%d") % EquipmentSystem.loadout_unlock_level(index)
		need.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		need.add_theme_font_size_override("font_size", 11)
		need.add_theme_color_override("font_color", UiStyle.INK_DIM)
		inner.add_child(need)
		return box

	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(64, 64)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if not inst.is_empty():
		var t: Texture2D = SpriteDB.equip_icon_for_inst(inst)
		if t:
			icon.texture = t
	inner.add_child(icon)

	var name_l := Label.new()
	name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_l.add_theme_font_size_override("font_size", 11)
	if inst.is_empty():
		name_l.text = _t("（空）· 點此裝填")
		name_l.add_theme_color_override("font_color", UiStyle.INK_DIM)
	else:
		var line := str(inst.get("line", ""))
		name_l.text = EquipmentSystem.display_name(inst)
		if line != "":
			name_l.text += "\n[%s]" % _weapon_line_name(line)
		name_l.add_theme_color_override("font_color", UiStyle.INK)
	inner.add_child(name_l)

	if not inst.is_empty():
		var row := HBoxContainer.new()
		row.alignment = BoxContainer.ALIGNMENT_CENTER
		row.add_theme_constant_override("separation", 4)
		box.add_child(row)
		if not active:
			var use_btn := Button.new()
			use_btn.text = _t("使用")
			UiStyle.style_button(use_btn, true)
			use_btn.pressed.connect(func():
				AudioManager.play_ui()
				var r2: Dictionary = EquipmentSystem.switch_weapon_loadout(index)
				_host.ui_toast(str(r2.get("msg", "")))
				_pending_loadout = -1
				open()
			)
			row.add_child(use_btn)
		var ue := Button.new()
		ue.text = _t("卸下")
		UiStyle.style_button(ue, false)
		ue.pressed.connect(func():
			AudioManager.play_ui()
			var r3: Dictionary = EquipmentSystem.unequip_loadout_slot(index)
			_host.ui_toast(str(r3.get("msg", "")))
			_pending_loadout = -1
			open()
		)
		row.add_child(ue)
	else:
		var fill := Button.new()
		fill.text = _t("裝填")
		UiStyle.style_button(fill, true)
		fill.pressed.connect(func():
			AudioManager.play_ui()
			_pending_loadout = index
			open()
		)
		box.add_child(fill)

	return box


func _slot_card(slot: String, compact: bool = false, unlocked: bool = true) -> Control:
	var slot_name := EquipmentSystem.slot_label(slot)
	var box := VBoxContainer.new()
	box.custom_minimum_size = Vector2(100 if compact else 140, 0)
	box.add_theme_constant_override("separation", 4)
	var lab := Label.new()
	lab.text = slot_name
	lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lab.add_theme_font_size_override("font_size", 11 if compact else 12)
	lab.add_theme_color_override("font_color", UiStyle.INK_DIM)
	box.add_child(lab)
	var cell := PanelContainer.new()
	cell.custom_minimum_size = Vector2(88 if compact else 120, 88 if compact else 120)
	var st := StyleBoxFlat.new()
	st.bg_color = Color(0.88, 0.88, 0.9, 1) if not unlocked else Color(0.94, 0.92, 0.95, 1)
	st.border_color = Color(0.6, 0.6, 0.65, 0.7) if not unlocked else UiStyle.WOOD
	st.set_border_width_all(2)
	st.set_corner_radius_all(8)
	cell.add_theme_stylebox_override("panel", st)
	box.add_child(cell)
	var inner := VBoxContainer.new()
	inner.alignment = BoxContainer.ALIGNMENT_CENTER
	cell.add_child(inner)
	if not unlocked:
		var lock_l := Label.new()
		lock_l.text = _t("Lv%d") % EquipmentSystem.ACCESSORY_LEVEL_REQ
		lock_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lock_l.add_theme_font_size_override("font_size", 11)
		lock_l.add_theme_color_override("font_color", UiStyle.INK_DIM)
		inner.add_child(lock_l)
		return box
	var uid := str(GameState.equip_slots.get(slot, ""))
	var inst: Dictionary = {}
	if uid != "" and GameState.equip_worn.has(uid):
		inst = GameState.equip_worn[uid]
	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(48 if compact else 72, 48 if compact else 72)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if not inst.is_empty():
		var t: Texture2D = SpriteDB.equip_icon_for_inst(inst)
		if t:
			icon.texture = t
	inner.add_child(icon)
	var name_l := Label.new()
	name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_l.add_theme_font_size_override("font_size", 10 if compact else 11)
	if inst.is_empty():
		name_l.text = _t("（空）")
		name_l.add_theme_color_override("font_color", UiStyle.INK_DIM)
	else:
		name_l.text = EquipmentSystem.display_name(inst)
		name_l.add_theme_color_override("font_color", UiStyle.INK)
	inner.add_child(name_l)
	if not inst.is_empty():
		var btn := Button.new()
		btn.text = _t("卸下")
		UiStyle.style_button(btn, false)
		btn.pressed.connect(func():
			AudioManager.play_ui()
			unequip(slot)
		)
		box.add_child(btn)
	return box


func _core_slot_card(def: Dictionary) -> Control:
	var slot_id := str(def.get("id", ""))
	var slot_name := _t(str(def.get("name", "")))
	var slot_desc := _t(str(def.get("desc", "")))

	var box := VBoxContainer.new()
	box.name = "CoreSlot_" + slot_id
	box.custom_minimum_size = Vector2(104, 0)
	box.add_theme_constant_override("separation", 3)

	var lab := Label.new()
	lab.name = "SlotNameLabel"
	lab.text = slot_name
	lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lab.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	lab.add_theme_font_size_override("font_size", 11)
	lab.add_theme_color_override("font_color", UiStyle.INK_DIM)
	box.add_child(lab)

	var norm_slot := CoreSystem.normalize_slot_id(slot_id) if CoreSystem != null else slot_id
	var part: Dictionary = CoreSystem.get_player_part(norm_slot) if CoreSystem != null else {}
	var tier_id: String = str(part.get("tier", "white"))
	var tier_name: String = str(part.get("tier_name", "白"))
	var tier_color: Color = CoreSystem.get_tier_color(tier_id) if CoreSystem != null else Color(0.72, 0.62, 0.82, 0.9)
	var count: int = int(part.get("calibration_count", 0))
	var max_cnt: int = int(part.get("max_calibrations", 7))
	var remains: int = maxi(0, max_cnt - count)

	var cell := PanelContainer.new()
	cell.name = "Cell"
	cell.custom_minimum_size = Vector2(88, 88)
	var st := StyleBoxFlat.new()
	st.bg_color = Color(0.96, 0.95, 0.98, 1)
	st.border_color = tier_color
	st.set_border_width_all(2)
	st.set_corner_radius_all(10)
	cell.add_theme_stylebox_override("panel", st)
	box.add_child(cell)

	var inner := VBoxContainer.new()
	inner.alignment = BoxContainer.ALIGNMENT_CENTER
	inner.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cell.add_child(inner)

	var icon := TextureRect.new()
	icon.name = "SlotIcon"
	icon.custom_minimum_size = Vector2(56, 56)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var t: Texture2D = SpriteDB.core_slot_icon(slot_id)
	if t:
		icon.texture = t
	icon.modulate = tier_color
	inner.add_child(icon)

	var btn := Button.new()
	btn.name = "SlotButton"
	btn.flat = true
	btn.custom_minimum_size = Vector2(88, 88)
	btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var tt_desc := slot_desc
	if not part.is_empty() and CoreSystem != null:
		var pstats: Dictionary = CoreSystem.get_part_stats(part)
		var stat_parts: Array[String] = []
		if int(pstats.get("atk", 0)) > 0: stat_parts.append("攻+%d" % int(pstats.atk))
		if int(pstats.get("def", 0)) > 0: stat_parts.append("防+%d" % int(pstats.def))
		if int(pstats.get("hp", 0)) > 0: stat_parts.append("血+%d" % int(pstats.hp))
		if float(pstats.get("crit", 0.0)) > 0.0: stat_parts.append("暴擊+%.1f%%" % float(pstats.crit))
		if float(pstats.get("crit_dmg", 0.0)) > 0.0: stat_parts.append("暴傷+%.0f%%" % float(pstats.crit_dmg))
		tt_desc = "%s (%s階)\n%s\n%s" % [slot_name, tier_name, slot_desc, " · ".join(stat_parts)]
	else:
		tt_desc = "%s\n%s" % [slot_name, slot_desc]
	btn.tooltip_text = tt_desc
	cell.add_child(btn)

	# 色階名稱與剩餘校準次數
	var tier_lbl := Label.new()
	tier_lbl.name = "TierLabel"
	tier_lbl.text = _t(tier_name + "階")
	tier_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tier_lbl.add_theme_font_size_override("font_size", 11)
	tier_lbl.add_theme_color_override("font_color", tier_color if tier_id != "white" else UiStyle.KEY_STRONG)
	box.add_child(tier_lbl)

	var count_lbl := Label.new()
	count_lbl.name = "CountLabel"
	count_lbl.text = _t("剩餘 %d 次") % remains
	count_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	count_lbl.add_theme_font_size_override("font_size", 10)
	count_lbl.add_theme_color_override("font_color", UiStyle.INK_DIM)
	box.add_child(count_lbl)

	# 單次校準按鈕（單手拇指點擊，熱區 >= 48px）
	var btn_cal := Button.new()
	btn_cal.name = "BtnCalibrate"
	btn_cal.text = _t("校準") if remains > 0 else _t("已達上限")
	btn_cal.disabled = (remains <= 0)
	UiStyle.style_button(btn_cal, remains > 0)
	btn_cal.custom_minimum_size = Vector2(88, 50)
	btn_cal.add_theme_font_size_override("font_size", 12)
	box.add_child(btn_cal)

	var update_card_ui = func():
		var p = CoreSystem.get_player_part(slot_id)
		var tid: String = str(p.get("tier", "white"))
		var tnm: String = str(p.get("tier_name", "白"))
		var tc: Color = CoreSystem.get_tier_color(tid)
		var cnt: int = int(p.get("calibration_count", 0))
		var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - cnt)
		icon.modulate = tc
		tier_lbl.text = _t(tnm + "階")
		tier_lbl.add_theme_color_override("font_color", tc if tid != "white" else UiStyle.KEY_STRONG)
		count_lbl.text = _t("剩餘 %d 次") % rem
		btn_cal.disabled = (rem <= 0)
		btn_cal.text = _t("校準") if rem > 0 else _t("已達上限")
		UiStyle.style_button(btn_cal, rem > 0)
		btn_cal.custom_minimum_size = Vector2(88, 50)
		btn_cal.add_theme_font_size_override("font_size", 12)
		return {"tier_name": tnm, "remains": rem, "part": p}

	btn_cal.pressed.connect(func():
		AudioManager.play_ui()
		var res: Dictionary = CoreSystem.calibrate_player_part(slot_id)
		var info: Dictionary = update_card_ui.call()
		if is_instance_valid(_core_hint_label):
			var tnm: String = str(info.get("tier_name", ""))
			var rem: int = int(info.get("remains", 0))
			_core_hint_label.text = _t("【%s】%s（目前色階：%s階 · 剩餘校準：%d 次）") % [slot_name, res.get("message", ""), tnm, rem]
			_core_hint_label.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	)

	btn.pressed.connect(func():
		AudioManager.play_ui()
		var p = CoreSystem.get_player_part(slot_id)
		var tnm: String = str(p.get("tier_name", "白"))
		var rem: int = maxi(0, int(p.get("max_calibrations", 7)) - int(p.get("calibration_count", 0)))
		if is_instance_valid(_core_hint_label):
			var stat_parts: Array[String] = []
			if not p.is_empty() and CoreSystem != null:
				var pstats: Dictionary = CoreSystem.get_part_stats(p)
				if int(pstats.get("atk", 0)) > 0: stat_parts.append("攻+%d" % int(pstats.atk))
				if int(pstats.get("def", 0)) > 0: stat_parts.append("防+%d" % int(pstats.def))
				if int(pstats.get("hp", 0)) > 0: stat_parts.append("血+%d" % int(pstats.hp))
				if float(pstats.get("crit", 0.0)) > 0.0: stat_parts.append("暴擊+%.1f%%" % float(pstats.crit))
				if float(pstats.get("crit_dmg", 0.0)) > 0.0: stat_parts.append("暴傷+%.0f%%" % float(pstats.crit_dmg))
			var s_stat := " · ".join(stat_parts)
			if not s_stat.is_empty():
				_core_hint_label.text = _t("【%s · %s階】%s（%s · 剩餘校準：%d 次）") % [slot_name, tnm, slot_desc, s_stat, rem]
			else:
				_core_hint_label.text = _t("【%s】%s（目前色階：%s階 · 剩餘校準：%d 次）") % [slot_name, slot_desc, tnm, rem]
			_core_hint_label.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	)

	return box


func _bag_cell(inst: Dictionary) -> Control:
	var cell := PanelContainer.new()
	cell.custom_minimum_size = Vector2(110, 118)
	var is_weapon := EquipmentSystem.normalize_slot(str(inst.get("slot", ""))) == "weapon"
	var highlight := _pending_loadout >= 0 and is_weapon
	var st := StyleBoxFlat.new()
	st.bg_color = Color(1.0, 0.96, 0.9, 1) if highlight else Color(0.97, 0.95, 0.93, 1)
	st.border_color = Color(0.9, 0.5, 0.2, 0.9) if highlight else Color(0.76, 0.37, 0.45, 0.55)
	st.set_border_width_all(2)
	st.set_corner_radius_all(8)
	cell.add_theme_stylebox_override("panel", st)

	var margin := MarginContainer.new()
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_theme_constant_override("margin_left", 6)
	margin.add_theme_constant_override("margin_right", 6)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_bottom", 6)
	cell.add_child(margin)

	var col := VBoxContainer.new()
	col.mouse_filter = Control.MOUSE_FILTER_IGNORE
	col.alignment = BoxContainer.ALIGNMENT_CENTER
	col.add_theme_constant_override("separation", 2)
	margin.add_child(col)

	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(48, 48)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var t: Texture2D = SpriteDB.equip_icon_for_inst(inst)
	if t:
		icon.texture = t
	col.add_child(icon)

	var nl := Label.new()
	nl.text = EquipmentSystem.display_name(inst)
	nl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nl.autowrap_mode = TextServer.AUTOWRAP_WORD
	nl.add_theme_font_size_override("font_size", 10)
	nl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	col.add_child(nl)

	var ql := Label.new()
	ql.text = _t(str(inst.get("quality_label", "")))
	if is_weapon:
		var line := str(inst.get("line", ""))
		if line != "":
			ql.text = "%s · %s" % [ql.text, _weapon_line_name(line)]
	ql.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ql.add_theme_font_size_override("font_size", 10)
	ql.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	ql.mouse_filter = Control.MOUSE_FILTER_IGNORE
	col.add_child(ql)

	var btn := Button.new()
	btn.flat = true
	btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	btn.mouse_filter = Control.MOUSE_FILTER_STOP
	var uid := str(inst.get("uid", ""))
	btn.tooltip_text = EquipmentSystem.label(inst)
	btn.pressed.connect(func():
		AudioManager.play_ui()
		wear(uid)
	)
	cell.add_child(btn)

	return cell


func wear(uid: String) -> void:
	var inst := EquipmentSystem.find_bag(uid)
	if inst.is_empty():
		_host.ui_toast(_t("背包沒有此裝。"))
		open()
		return
	var is_weapon := EquipmentSystem.normalize_slot(str(inst.get("slot", ""))) == "weapon"
	if _pending_loadout >= 0:
		if not is_weapon:
			_host.ui_toast(_t("請選擇武器裝入武器欄。"))
			return
		var r: Dictionary = EquipmentSystem.equip_weapon_to_loadout(uid, _pending_loadout)
		_host.ui_toast(str(r.get("msg", "")))
		_pending_loadout = -1
		open()
		return
	var r2: Dictionary = EquipmentSystem.equip(uid)
	_host.ui_toast(str(r2.get("msg", "")))
	open()


func unequip(slot: String) -> void:
	var r: Dictionary = EquipmentSystem.unequip(slot)
	_host.ui_toast(str(r.get("msg", "")))
	open()


func _core_bag_cell(part: Dictionary) -> Control:
	var cell := PanelContainer.new()
	cell.name = "CoreBagCell_" + str(part.get("uid", ""))
	cell.custom_minimum_size = Vector2(110, 118)

	var slot_id: String = str(part.get("slot", "mainspring"))
	var tier_id: String = str(part.get("tier", "white"))
	var tier_name: String = str(part.get("tier_name", "白"))
	var slot_name: String = str(part.get("slot_name", ""))
	if slot_name.is_empty() and CoreSystem != null:
		slot_name = CoreSystem.get_slot_name(slot_id)

	var tier_color: Color = CoreSystem.get_tier_color(tier_id) if CoreSystem != null else Color.WHITE

	var st := StyleBoxFlat.new()
	st.bg_color = Color(0.97, 0.96, 0.98, 1)
	st.border_color = tier_color
	st.set_border_width_all(2)
	st.set_corner_radius_all(10)
	cell.add_theme_stylebox_override("panel", st)

	var vb := VBoxContainer.new()
	vb.alignment = BoxContainer.ALIGNMENT_CENTER
	vb.add_theme_constant_override("separation", 2)
	cell.add_child(vb)

	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(40, 40)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if SpriteDB != null:
		var tex: Texture2D = SpriteDB.core_slot_icon(slot_id)
		if tex:
			icon.texture = tex
	icon.modulate = tier_color
	vb.add_child(icon)

	var name_lbl := Label.new()
	name_lbl.text = _t(slot_name)
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 11)
	name_lbl.add_theme_color_override("font_color", UiStyle.KEY_STRONG)
	vb.add_child(name_lbl)

	var tier_lbl := Label.new()
	tier_lbl.text = "【%s】" % _t(tier_name + "階")
	tier_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tier_lbl.add_theme_font_size_override("font_size", 10)
	tier_lbl.add_theme_color_override("font_color", tier_color if tier_id != "white" else UiStyle.KEY_STRONG)
	vb.add_child(tier_lbl)

	var btn := Button.new()
	btn.name = "EquipButton"
	btn.text = _t("裝備")
	btn.custom_minimum_size = Vector2(64, 30)
	btn.focus_mode = Control.FOCUS_NONE
	UiStyle.style_button(btn, true)
	btn.add_theme_font_size_override("font_size", 10)
	btn.pressed.connect(func():
		AudioManager.play_ui()
		if CoreSystem != null:
			var old_part: Dictionary = CoreSystem.get_player_part(slot_id)
			CoreSystem.remove_part_from_inventory(str(part.get("uid", "")))
			if not old_part.is_empty():
				CoreSystem.add_part_to_inventory(old_part)
			CoreSystem.equip_part(slot_id, part)
		open()
	)
	vb.add_child(btn)

	return cell
