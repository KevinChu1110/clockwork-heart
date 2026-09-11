class_name MapleHotbar
extends Control
## 楓式底部快捷欄 1–8；陽光童話·多巴胺亮色盤（奶油白底 · 果凍槽位 · 深藍紫立體邊框）

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const WindowDrag = preload("res://scripts/ui/window_drag.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const GameInputGate = preload("res://scripts/autoload/game_input_gate.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

const SLOT_N := 8
const SLOT_SIZE := Vector2(50, 50)

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃（選中高亮框）
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和米底（選中格轉亮底）
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫文字

signal slot_clicked(index: int)
signal slot_right_clicked(index: int)

var _bar: PanelContainer
var _slots: Array = []
var _glyphs: Array = []
var _counts: Array = []
var _keys: Array = []
var _flash: Array = []
var _cached_font: Font = null


func _get_font() -> Font:
	if _cached_font == null and ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	return _cached_font


func _create_bar_style() -> StyleBoxFlat:
	var bs := StyleBoxFlat.new()
	bs.bg_color = COLOR_BG_CREAM
	bs.border_color = COLOR_BORDER
	bs.set_border_width_all(2)
	bs.border_width_bottom = 5
	bs.set_corner_radius_all(22)
	bs.content_margin_left = 12
	bs.content_margin_right = 12
	bs.content_margin_top = 8
	bs.content_margin_bottom = 10
	bs.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	bs.shadow_size = 8
	bs.shadow_offset = Vector2(0, 4)
	return bs


func _style_slot_empty() -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 4
	sb.set_corner_radius_all(18)
	return sb


func _style_slot_filled() -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_GOLD
	sb.border_color = COLOR_GOLD
	sb.set_border_width_all(3)
	sb.border_width_bottom = 5
	sb.set_corner_radius_all(18)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.2)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)
	return sb


func _style_slot_menu() -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.set_corner_radius_all(18)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.2)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)
	return sb


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_anchors_preset(Control.PRESET_TOP_LEFT)
	anchor_right = 0
	anchor_bottom = 0
	## 初始置底中（之後可拖）；尾端多一格「選單」鈕。槽 50px 防誤觸。
	custom_minimum_size = Vector2(520, 72)
	size = Vector2(520, 72)
	_build()
	call_deferred("_place_default")
	if Engine.get_main_loop() is SceneTree:
		var inv: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
		if inv:
			if inv.has_signal("inventory_changed"):
				inv.inventory_changed.connect(refresh)
			if inv.has_signal("hotbar_changed"):
				inv.hotbar_changed.connect(refresh)
	refresh()
	WindowDrag.attach(self, _bar, "hotbar")


func _place_default() -> void:
	var vp := get_viewport().get_visible_rect().size
	var m := ResponsiveUi.safe_margin(self)
	var fallback := Vector2((vp.x - size.x) * 0.5, vp.y - size.y - m.w)
	if Engine.get_main_loop() is SceneTree:
		var ul: Node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("UiLayout")
		if ul and ul.has_method("has_pos") and ul.call("has_pos", "hotbar"):
			ul.call("apply_to", self, "hotbar", fallback)
			return
	position = fallback


func _build() -> void:
	var f := _get_font()

	_bar = PanelContainer.new()
	_bar.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bar.mouse_filter = Control.MOUSE_FILTER_STOP
	_bar.add_theme_stylebox_override("panel", _create_bar_style())
	add_child(_bar)

	var col := VBoxContainer.new()
	col.add_theme_constant_override("separation", 0)
	col.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bar.add_child(col)

	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 6)
	row.mouse_filter = Control.MOUSE_FILTER_STOP
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	col.add_child(row)

	for i in SLOT_N:
		var slot := PanelContainer.new()
		slot.custom_minimum_size = SLOT_SIZE
		slot.mouse_filter = Control.MOUSE_FILTER_STOP
		slot.add_theme_stylebox_override("panel", _style_slot_empty())
		row.add_child(slot)
		_slots.append(slot)

		var stack := Control.new()
		stack.set_anchors_preset(Control.PRESET_FULL_RECT)
		stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
		slot.add_child(stack)

		var flash := ColorRect.new()
		flash.set_anchors_preset(Control.PRESET_FULL_RECT)
		flash.color = Color(1, 0.85, 0.3, 0)
		flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stack.add_child(flash)
		_flash.append(flash)

		var glyph := Label.new()
		glyph.set_anchors_preset(Control.PRESET_FULL_RECT)
		glyph.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		glyph.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		glyph.add_theme_font_size_override("font_size", 20)
		glyph.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		glyph.add_theme_color_override("font_outline_color", Color.WHITE)
		glyph.add_theme_constant_override("outline_size", 2)
		if f:
			glyph.add_theme_font_override("font", f)
		glyph.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stack.add_child(glyph)
		_glyphs.append(glyph)

		var cnt := Label.new()
		cnt.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_RIGHT)
		cnt.offset_left = -32
		cnt.offset_top = -20
		cnt.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		cnt.add_theme_font_size_override("font_size", 16)
		cnt.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		cnt.add_theme_color_override("font_outline_color", Color.WHITE)
		cnt.add_theme_constant_override("outline_size", 3)
		if f:
			cnt.add_theme_font_override("font", f)
		cnt.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stack.add_child(cnt)
		_counts.append(cnt)

		var key := Label.new()
		key.text = str(i + 1)
		key.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
		key.offset_left = 4
		key.offset_top = 2
		key.add_theme_font_size_override("font_size", 14)
		key.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		key.add_theme_color_override("font_outline_color", Color.WHITE)
		key.add_theme_constant_override("outline_size", 2)
		if f:
			key.add_theme_font_override("font", f)
		key.mouse_filter = Control.MOUSE_FILTER_IGNORE
		## 觸控裝置沒鍵盤，1–8 快捷鍵標籤只會造成困惑
		key.visible = not DisplayServer.is_touchscreen_available()
		stack.add_child(key)
		_keys.append(key)

		var idx := i
		slot.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed:
				if ev.button_index == MOUSE_BUTTON_LEFT:
					slot_clicked.emit(idx)
					get_viewport().set_input_as_handled()
				elif ev.button_index == MOUSE_BUTTON_RIGHT:
					slot_right_clicked.emit(idx)
					get_viewport().set_input_as_handled()
		)

	## 尾端「選單」鈕送 Cancel，與右側鎖定／換武／技能同一套米黃厚底風格
	var menu_btn := PanelContainer.new()
	menu_btn.custom_minimum_size = SLOT_SIZE
	menu_btn.mouse_filter = Control.MOUSE_FILTER_STOP
	menu_btn.add_theme_stylebox_override("panel", _style_slot_menu())
	row.add_child(menu_btn)
	var ml := Label.new()
	ml.text = ContentLoc.text("ui", "選單")
	ml.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ml.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	ml.add_theme_font_size_override("font_size", 16)
	ml.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	ml.add_theme_color_override("font_outline_color", Color.WHITE)
	ml.add_theme_constant_override("outline_size", 2)
	if f:
		ml.add_theme_font_override("font", f)
	ml.mouse_filter = Control.MOUSE_FILTER_IGNORE
	menu_btn.add_child(ml)
	menu_btn.gui_input.connect(func(ev: InputEvent):
		if GameInputGate.primary_pointer_pressed(ev):
			get_viewport().set_input_as_handled()
			GameInputGate.inject(GameInputGate.CANCEL)
	)


func refresh() -> void:
	var inv: Node = null
	if Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
	if inv == null or not inv.has_method("ensure_hotbar"):
		return
	inv.call("ensure_hotbar")
	var bar: Array = GameState.hotbar
	for i in SLOT_N:
		var id := str(bar[i]) if i < bar.size() else ""
		var glyph: Label = _glyphs[i]
		var cnt: Label = _counts[i]
		var slot: PanelContainer = _slots[i]
		if id == "" or int(GameState.inventory.get(id, 0)) <= 0:
			glyph.text = ""
			cnt.text = ""
			slot.add_theme_stylebox_override("panel", _style_slot_empty())
			continue
		var def: Dictionary = inv.call("catalog", id)
		glyph.text = str(def.get("glyph", "·"))
		glyph.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		var n := int(GameState.inventory.get(id, 0))
		cnt.text = str(n) if n > 1 else ""
		slot.add_theme_stylebox_override("panel", _style_slot_filled())


func pulse_slot(index: int) -> void:
	if index < 0 or index >= _flash.size():
		return
	var f: ColorRect = _flash[index]
	f.color = Color(1, 0.85, 0.3, 0.6)
	var tw := create_tween()
	tw.tween_property(f, "color:a", 0.0, 0.25)
