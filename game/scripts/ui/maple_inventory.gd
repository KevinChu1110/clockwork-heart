class_name MapleInventory
extends Control
## 《發條之心》背包物品欄 (MapleInventory)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px（750px），置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上圓形「✕」關閉按鈕尺寸 >= 50px，點擊遮罩空白處亦可關閉。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底板奶油白 #FFFDF8。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)，按鈕高 >= 50px。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 全程 0 系統 emoji。格子／明細／關閉行為維持原功能。
## 7. 只改 maple_inventory.gd 本畫面樣式覆寫，不改 ui_style.gd 共用函式。

signal closed
signal item_used(item_id: String)
signal assign_hotbar(item_id: String)

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const GameInputGate = preload("res://scripts/autoload/game_input_gate.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 彈窗尺寸標準 (橫屏 740~760px)
const DIALOG_WIDTH := 750.0
const DIALOG_HEIGHT := 540.0
const COLS := 4
const ROWS := 6

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
const COLOR_CARD_SKY   := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）

var _dim: ColorRect
var _card: PanelContainer
var _grid: GridContainer
var _cells: Array = []
var _detail: RichTextLabel
var _title: Label
var _use_btn: Button
var _hb_btn: Button
var _tip: Label
var _selected: String = ""
var _bag_ids: Array = []
var _cached_font: Font = null
var _last_click_i: int = -1
var _last_click_t: int = 0


func _ready() -> void:
	visible = false
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_preset(Control.PRESET_FULL_RECT)
	z_index = 60

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build()


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 5, radius: int = 18, border_w: int = 2) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_border
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 10
	if bottom_border > 2:
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
		sb.shadow_size = 5
		sb.shadow_offset = Vector2(0, 3)
	return sb


func _apply_label_style(lbl: Label, size: int, color: Color = COLOR_TEXT_DARK, outline_col: Color = Color(0, 0, 0, 0), outline_sz: int = 0) -> void:
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", color)
	if outline_sz > 0:
		lbl.add_theme_color_override("font_outline_color", outline_col)
		lbl.add_theme_constant_override("outline_size", outline_sz)
	if _cached_font:
		lbl.add_theme_font_override("font", _cached_font)


func _build() -> void:
	## 1. 全螢幕柔和暗幕遮罩 (Scrim)
	_dim = ResponsiveUi.make_scrim(Color(0.08, 0.06, 0.12, 0.65))
	_dim.mouse_filter = Control.MOUSE_FILTER_STOP
	_dim.gui_input.connect(func(ev: InputEvent):
		if GameInputGate.primary_pointer_pressed(ev):
			close()
	)
	add_child(_dim)

	## 2. 居中容器與橫屏手遊彈窗主體 (750x520px，置中大氣)
	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(center)

	_card = PanelContainer.new()
	_card.name = "InventoryCard"
	ResponsiveUi.apply_dialog_card(_card)
	_card.custom_minimum_size = Vector2(DIALOG_WIDTH, DIALOG_HEIGHT)
	_card.mouse_filter = Control.MOUSE_FILTER_STOP
	_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(_card)

	var card_margin := MarginContainer.new()
	card_margin.add_theme_constant_override("margin_left", 20)
	card_margin.add_theme_constant_override("margin_right", 20)
	card_margin.add_theme_constant_override("margin_top", 16)
	card_margin.add_theme_constant_override("margin_bottom", 16)
	_card.add_child(card_margin)

	var outer := VBoxContainer.new()
	outer.add_theme_constant_override("separation", 10)
	card_margin.add_child(outer)

	## ── 頂部標題與關閉列 (高 50px) ──
	var head_row := HBoxContainer.new()
	head_row.custom_minimum_size.y = 50
	head_row.alignment = BoxContainer.ALIGNMENT_CENTER
	head_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	outer.add_child(head_row)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.alignment = BoxContainer.ALIGNMENT_CENTER
	head_row.add_child(title_box)

	_title = Label.new()
	_title.text = "物品欄"
	_apply_label_style(_title, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 4)
	title_box.add_child(_title)

	var sub_title := Label.new()
	sub_title.text = "冒險者背包 · 點選格子查看詳情"
	_apply_label_style(sub_title, 16, COLOR_TEXT_DARK)
	title_box.add_child(sub_title)

	## 右上圓形「✕」關閉按鈕 (50x50，珊瑚粉果凍厚底按鈕)
	var close_btn := Button.new()
	close_btn.name = "CloseButton"
	close_btn.text = "✕"
	close_btn.custom_minimum_size = Vector2(50, 50)
	close_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_PINK, COLOR_BORDER, 5, 20))
	close_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7A9F"), COLOR_BORDER, 5, 20))
	close_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_PINK, COLOR_BORDER, 2, 20))
	close_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	close_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	close_btn.add_theme_constant_override("outline_size", 3)
	close_btn.add_theme_font_size_override("font_size", 22)
	if _cached_font:
		close_btn.add_theme_font_override("font", _cached_font)
	close_btn.pressed.connect(close)
	head_row.add_child(close_btn)

	## 亮橘色立體分隔粗線
	var rule := ColorRect.new()
	rule.custom_minimum_size = Vector2(0, 3)
	rule.color = COLOR_ORANGE
	outer.add_child(rule)

	## ── 主體內容雙欄排列 (左側 4×6 物品格子 + 右側道具詳情與操作按鈕) ──
	var body := HBoxContainer.new()
	body.add_theme_constant_override("separation", 18)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	outer.add_child(body)

	## 左側：物品格子區 (GridContainer 4×6)
	var grid_panel := PanelContainer.new()
	grid_panel.custom_minimum_size = Vector2(320, 0)
	grid_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	body.add_child(grid_panel)

	var grid_margin := MarginContainer.new()
	grid_margin.add_theme_constant_override("margin_left", 12)
	grid_margin.add_theme_constant_override("margin_right", 12)
	grid_margin.add_theme_constant_override("margin_top", 12)
	grid_margin.add_theme_constant_override("margin_bottom", 12)
	grid_panel.add_child(grid_margin)

	_grid = GridContainer.new()
	_grid.columns = COLS
	_grid.add_theme_constant_override("h_separation", 6)
	_grid.add_theme_constant_override("v_separation", 6)
	_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_margin.add_child(_grid)

	_cells.clear()
	for i in COLS * ROWS:
		var cell := PanelContainer.new()
		cell.custom_minimum_size = Vector2(68, 56)
		cell.mouse_filter = Control.MOUSE_FILTER_STOP
		var cs := _create_panel_style(COLOR_CARD_WARM, Color(0.20, 0.16, 0.30, 0.35), 2, 3, 16)
		cell.add_theme_stylebox_override("panel", cs)
		_grid.add_child(cell)
		_cells.append(cell)

		var stack := Control.new()
		stack.set_anchors_preset(Control.PRESET_FULL_RECT)
		stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
		cell.add_child(stack)

		var g := Label.new()
		g.name = "Glyph"
		g.set_anchors_preset(Control.PRESET_FULL_RECT)
		g.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		g.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		_apply_label_style(g, 24, COLOR_TEXT_DARK)
		g.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stack.add_child(g)

		var c := Label.new()
		c.name = "Count"
		c.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_RIGHT)
		c.offset_left = -34
		c.offset_top = -20
		c.offset_right = -4
		c.offset_bottom = -2
		c.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		c.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
		_apply_label_style(c, 16, COLOR_TEXT_DARK, Color("#FFFFFF"), 2)
		c.mouse_filter = Control.MOUSE_FILTER_IGNORE
		stack.add_child(c)

		var idx := i
		cell.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed:
				_on_cell(idx, ev.button_index)
		)

	## 右側：道具明細與操作按鈕區
	var right := VBoxContainer.new()
	right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right.add_theme_constant_override("separation", 10)
	body.add_child(right)

	## 道具詳情卡片 (溫暖米黃底 + 深藍紫立體邊框)
	var detail_panel := PanelContainer.new()
	detail_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	detail_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	right.add_child(detail_panel)

	var detail_margin := MarginContainer.new()
	detail_margin.add_theme_constant_override("margin_left", 16)
	detail_margin.add_theme_constant_override("margin_right", 16)
	detail_margin.add_theme_constant_override("margin_top", 14)
	detail_margin.add_theme_constant_override("margin_bottom", 14)
	detail_panel.add_child(detail_margin)

	_detail = RichTextLabel.new()
	_detail.bbcode_enabled = true
	_detail.fit_content = false
	_detail.scroll_active = true
	_detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_detail.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_detail.add_theme_font_size_override("normal_font_size", 16)
	_detail.add_theme_font_size_override("bold_font_size", 20)
	if _cached_font:
		_detail.add_theme_font_override("normal_font", _cached_font)
		_detail.add_theme_font_override("bold_font", _cached_font)
	_detail.mouse_filter = Control.MOUSE_FILTER_IGNORE
	detail_margin.add_child(_detail)

	## 「使用 / 賣出」按鈕 (薄荷綠果凍厚底按鈕，高 52px)
	_use_btn = Button.new()
	_use_btn.text = "使用 / 賣出"
	_use_btn.custom_minimum_size = Vector2(0, 52)
	_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
	_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
	_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
	_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_use_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_use_btn.add_theme_font_override("font", _cached_font)
	_use_btn.pressed.connect(func():
		if _selected != "":
			item_used.emit(_selected)
			refresh()
	)
	right.add_child(_use_btn)

	## 「放到快捷欄」按鈕 (天藍果凍厚底按鈕，高 52px)
	_hb_btn = Button.new()
	_hb_btn.text = "放到快捷欄"
	_hb_btn.custom_minimum_size = Vector2(0, 52)
	_hb_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18))
	_hb_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5DB3FF"), COLOR_BORDER, 5, 18))
	_hb_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_SKY, COLOR_BORDER, 2, 18))
	_hb_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_hb_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_hb_btn.add_theme_constant_override("outline_size", 3)
	_hb_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_hb_btn.add_theme_font_override("font", _cached_font)
	_hb_btn.pressed.connect(func():
		if _selected != "":
			assign_hotbar.emit(_selected)
	)
	right.add_child(_hb_btn)

	## 操作提示標籤 (字級 16px 加粗，深藍紫文字)
	_tip = Label.new()
	_tip.text = "左鍵點選查看 · 雙擊或右鍵快速使用"
	_tip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(_tip, 16, Color("#6B5E80"))
	right.add_child(_tip)


func open() -> void:
	visible = true
	var inv: Node = null
	if Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
	var list: Array = inv.call("bag_list") if inv else []
	## 若尚未選取且背包有物品，預設選取第一個，確保格子與明細同時呈現
	if _selected == "" and list.size() > 0:
		var first_it = list[0]
		if first_it is Dictionary and first_it.has("id"):
			_selected = str(first_it["id"])
	refresh()


func close() -> void:
	visible = false
	closed.emit()


func toggle() -> void:
	if visible:
		close()
	else:
		open()


func refresh() -> void:
	var inv: Node = null
	if Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
	_bag_ids.clear()
	var list: Array = inv.call("bag_list") if inv else []

	## 若目前已選取的道具已經不在背包內，且背包還有道具，重選第一個
	if _selected != "":
		var found := false
		for it in list:
			if it is Dictionary and str(it.get("id", "")) == _selected:
				found = true
				break
		if not found:
			_selected = str(list[0].get("id", "")) if list.size() > 0 else ""
	elif list.size() > 0:
		_selected = str(list[0].get("id", ""))

	for i in _cells.size():
		var cell: PanelContainer = _cells[i]
		var g: Label = cell.find_child("Glyph", true, false)
		var c: Label = cell.find_child("Count", true, false)
		if i < list.size():
			var it: Dictionary = list[i]
			var id := str(it.get("id", ""))
			_bag_ids.append(id)
			var def: Dictionary = it.get("def", {})
			if g:
				g.text = str(def.get("glyph", "·"))
				g.add_theme_color_override("font_color", def.get("color", COLOR_TEXT_DARK))
			if c:
				var n := int(it.get("count", 0))
				c.text = str(n) if n > 1 else ""

			var sel := (id == _selected)
			if sel:
				## 選取中：金黃柔和底 + 亮金橘厚邊框 (5px 厚底) + 金黃光暈
				var asb := StyleBoxFlat.new()
				asb.bg_color = COLOR_CARD_GOLD
				asb.border_color = COLOR_ORANGE
				asb.set_border_width_all(3)
				asb.border_width_bottom = 5
				asb.set_corner_radius_all(16)
				asb.shadow_color = Color(1.0, 0.63, 0.06, 0.35)
				asb.shadow_size = 6
				asb.shadow_offset = Vector2(0, 3)
				cell.add_theme_stylebox_override("panel", asb)
			else:
				## 未選取有道具：柔和天藍底 + 深藍紫立體邊框
				var nsb := StyleBoxFlat.new()
				nsb.bg_color = COLOR_CARD_SKY
				nsb.border_color = COLOR_BORDER
				nsb.set_border_width_all(2)
				nsb.border_width_bottom = 4
				nsb.set_corner_radius_all(16)
				nsb.shadow_color = Color(0.12, 0.10, 0.23, 0.15)
				nsb.shadow_size = 4
				nsb.shadow_offset = Vector2(0, 2)
				cell.add_theme_stylebox_override("panel", nsb)
		else:
			_bag_ids.append("")
			if g:
				g.text = ""
			if c:
				c.text = ""
			## 空格：溫暖米黃底 + 淡深藍紫邊框
			var empty := StyleBoxFlat.new()
			empty.bg_color = COLOR_CARD_WARM
			empty.border_color = Color(0.20, 0.16, 0.30, 0.35)
			empty.set_border_width_all(2)
			empty.border_width_bottom = 3
			empty.set_corner_radius_all(16)
			cell.add_theme_stylebox_override("panel", empty)

	_update_detail(inv)


func _update_detail(inv: Node) -> void:
	if _selected == "" or inv == null:
		_detail.text = "[color=#1F1A3A][b]冒險者背包[/b]\n\n請點選左側格子查看道具詳情。\n\n[color=#C2600A]•[/color] 消耗品：使用回復狀態\n[color=#C2600A]•[/color] 素材：點擊使用可賣出金幣\n[color=#C2600A]•[/color] 重要物：劇情關鍵道具[/color]"
		if _use_btn:
			_use_btn.disabled = true
		if _hb_btn:
			_hb_btn.disabled = true
		return

	if _use_btn:
		_use_btn.disabled = false
	if _hb_btn:
		_hb_btn.disabled = false

	var def: Dictionary = inv.call("catalog", _selected) as Dictionary
	var n: int = int(inv.call("count", _selected))
	var kind: String = str(def.get("kind", ""))
	var kind_s: String = kind
	match kind:
		"consumable":
			kind_s = "消耗品"
		"material":
			kind_s = "素材（點擊使用可賣出）"
		"key":
			kind_s = "重要道具"

	var item_name: String = str(def.get("name", _selected))
	var item_desc: String = str(def.get("desc", ""))

	_detail.text = "[color=#1F1A3A][b][font_size=20]%s[/font_size][/b]  [color=#C2600A]×%d[/color]\n\n[color=#4A3E60]%s[/color]\n\n[color=#C2600A]類型：[/color][color=#1F1A3A]%s[/color][/color]" % [
		item_name,
		n,
		item_desc,
		kind_s,
	]


func _on_cell(idx: int, button: int) -> void:
	if idx < 0 or idx >= _bag_ids.size():
		return
	var id := str(_bag_ids[idx])
	if id == "":
		_selected = ""
		refresh()
		return
	if button == MOUSE_BUTTON_RIGHT:
		_selected = id
		item_used.emit(id)
		refresh()
		return
	if button == MOUSE_BUTTON_LEFT:
		var now := Time.get_ticks_msec()
		if _last_click_i == idx and now - _last_click_t < 350:
			_selected = id
			item_used.emit(id)
			_last_click_i = -1
			refresh()
			return
		_last_click_i = idx
		_last_click_t = now
		_selected = id
		refresh()
