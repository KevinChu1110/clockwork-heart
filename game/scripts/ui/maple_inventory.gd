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
signal items_sorted
signal category_changed(category_id: String)
signal equipment_changed
signal equipment_lock_toggled(uid: String, is_locked: bool)
signal equipment_dismantled(uid: String, result: Dictionary)
signal forge_requested()
signal workshop_requested()

const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const GameInputGate = preload("res://scripts/autoload/game_input_gate.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"
const ITEM_ICON_DIR := "res://assets/icons/items/"
static var _icon_cache: Dictionary = {}

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

static func get_item_icon(id: String) -> Texture2D:
	if id.is_empty():
		return null
	if _icon_cache.has(id):
		return _icon_cache[id]
	var p := ITEM_ICON_DIR + id + ".png"
	if ResourceLoader.exists(p):
		var tex := load(p) as Texture2D
		_icon_cache[id] = tex
		return tex
	_icon_cache[id] = null
	return null

## 彈窗尺寸標準 (橫屏 740~760px)
const DIALOG_WIDTH := 750.0
const DIALOG_HEIGHT := 560.0
const COLS := 4
const ROWS := 6

const CHIP_CATEGORIES: Array = [
	{"id": "all", "label": "全部"},
	{"id": "equip", "label": "裝備"},
	{"id": "consumable", "label": "消耗品"},
	{"id": "material", "label": "素材"},
	{"id": "gem", "label": "寶石"},
]

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

## 戰力差額比對膠囊配色規範 (升攻/升防綠色膠囊 #1E7538、降攻/降防灰色膠囊 #7A7090)
const COLOR_DIFF_POS     := Color("#1E7538")  ## 升攻綠色膠囊主色
const COLOR_DIFF_NEG     := Color("#7A7090")  ## 降攻灰色膠囊主色
const COLOR_DIFF_EQ      := Color("#7A7090")  ## 持平灰色膠囊主色
const COLOR_DIFF_POS_BG  := Color("#1E7538")  ## 升攻綠底
const COLOR_DIFF_POS_TEXT:= Color("#FFFFFF")  ## 升攻白字 (高對比)
const COLOR_DIFF_POS_BD  := Color("#145227")  ## 升攻立體邊框
const COLOR_DIFF_NEG_BG  := Color("#7A7090")  ## 降攻灰底
const COLOR_DIFF_NEG_TEXT:= Color("#FFFFFF")  ## 降攻白字 (高對比)
const COLOR_DIFF_NEG_BD  := Color("#5C5470")  ## 降攻立體邊框
const COLOR_DIFF_EQ_BG   := Color("#7A7090")  ## 持平灰底
const COLOR_DIFF_EQ_TEXT := Color("#FFFFFF")  ## 持平白字
const COLOR_DIFF_EQ_BD   := Color("#5C5470")  ## 持平立體邊框
const COLOR_DIFF_WORN_BG   := Color("#3870B2")  ## 穿戴中專屬藍底膠囊
const COLOR_DIFF_WORN_TEXT := Color("#FFFFFF")  ## 穿戴中白字 (高對比)
const COLOR_DIFF_WORN_BD   := Color("#265288")  ## 穿戴中立體邊框

var _dim: ColorRect
var _card: PanelContainer
var _grid: GridContainer
var _cells: Array = []
var _detail: RichTextLabel
var _title: Label
var _sub_title: Label
var _use_btn: Button
var _hb_btn: Button
var _sort_btn: Button
var _is_sorted: bool = false
var _chip_buttons: Dictionary = {}
var _current_category: String = "all"
var _chip_row: HBoxContainer
var _tip: Label
var _selected: String = ""
var _bag_ids: Array = []
var _cached_font: Font = null
var _last_click_i: int = -1
var _last_click_t: int = 0
var _preview_row: HBoxContainer
var _preview_frame: PanelContainer
var _detail_icon: TextureRect
var _detail_glyph: Label
var _detail_name: Label
var _detail_count: Label
var _detail_kind: Label
var _stat_row: HBoxContainer
var _detail_stat: Label
var _diff_capsule: PanelContainer
var _diff_label: Label
var _lock_capsule: PanelContainer = null
var _lock_label: Label = null
var _lock_btn: Button = null
var _dismantle_btn: Button = null
var _go_forge_btn: Button = null
var _go_workshop_btn: Button = null


func _ready() -> void:
	visible = false
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_preset(Control.PRESET_FULL_RECT)
	z_index = 60

	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font

	_build()
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
		var eq: Node = (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq and eq.has_signal("equipment_changed"):
			if not eq.equipment_changed.is_connected(_on_equipment_changed):
				eq.equipment_changed.connect(_on_equipment_changed)


func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)
		var eq: Node = (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq and eq.has_signal("equipment_changed") and eq.equipment_changed.is_connected(_on_equipment_changed):
			eq.equipment_changed.disconnect(_on_equipment_changed)


func _on_equipment_changed() -> void:
	if visible and _selected != "":
		var inv: Node = null
		if Engine.get_main_loop() is SceneTree:
			inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
		_update_detail(inv)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	refresh()


func _update_ui_texts() -> void:
	if _title and is_instance_valid(_title):
		_title.text = _t("物品欄")
	if _sub_title and is_instance_valid(_sub_title):
		_sub_title.text = _t("冒險者背包 · 點選格子查看詳情")
	_update_action_button()
	_update_lock_ui_texts()
	_update_dismantle_button()
	_update_shortcut_buttons()
	if _go_forge_btn and is_instance_valid(_go_forge_btn):
		_go_forge_btn.text = _t("前往鍛造")
	if _go_workshop_btn and is_instance_valid(_go_workshop_btn):
		_go_workshop_btn.text = _t("前往工坊")
	if _hb_btn and is_instance_valid(_hb_btn):
		_hb_btn.text = _t("放到快捷欄")
	if _sort_btn and is_instance_valid(_sort_btn):
		_sort_btn.text = _t("一鍵整理")
	for cat in CHIP_CATEGORIES:
		var cid: String = cat["id"]
		if _chip_buttons.has(cid):
			var cbtn: Button = _chip_buttons[cid]
			if cbtn and is_instance_valid(cbtn):
				cbtn.text = _t(cat["label"])
	if _tip and is_instance_valid(_tip):
		_tip.text = _t("左鍵點選查看 · 雙擊或右鍵快速使用")


func _create_chip_style(selected: bool, pressed: bool = false, hover: bool = false) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(15)
	sb.set_border_width_all(2)
	sb.content_margin_left = 6
	sb.content_margin_right = 6
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4

	if selected:
		sb.bg_color = COLOR_GOLD if not hover else Color("#FFE066")
		sb.border_color = COLOR_BORDER
		sb.border_width_bottom = 2 if pressed else 5
		sb.shadow_color = Color(1.0, 0.63, 0.06, 0.30)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
	else:
		# 未選中為奶油白/淡紫邊框底
		sb.bg_color = COLOR_BG_CREAM if not hover else Color("#FFF8E7")
		sb.border_color = Color("#7A6899")
		sb.border_width_bottom = 2 if pressed else 3
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.10)
		sb.shadow_size = 3
		sb.shadow_offset = Vector2(0, 1)

	return sb


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


func _create_diff_capsule_style(bg_color: Color, border_color: Color) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg_color
	sb.border_color = border_color
	sb.set_border_width_all(1)
	sb.border_width_bottom = 2
	sb.set_corner_radius_all(13)
	sb.content_margin_left = 8
	sb.content_margin_right = 8
	sb.content_margin_top = 2
	sb.content_margin_bottom = 3
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
	_apply_label_style(_title, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 4)
	title_box.add_child(_title)

	_sub_title = Label.new()
	_apply_label_style(_sub_title, 16, COLOR_TEXT_DARK)
	title_box.add_child(_sub_title)

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

	var grid_vbox := VBoxContainer.new()
	grid_vbox.add_theme_constant_override("separation", 8)
	grid_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_margin.add_child(grid_vbox)

	## 格子區上方配置 5 枚 Chip 按鈕：『全部』、『裝備』、『消耗品』、『素材』、『寶石』
	_chip_row = HBoxContainer.new()
	_chip_row.name = "CategoryChipsRow"
	_chip_row.add_theme_constant_override("separation", 4)
	_chip_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid_vbox.add_child(_chip_row)

	_chip_buttons.clear()
	for cat in CHIP_CATEGORIES:
		var cid: String = cat["id"]
		var btn := Button.new()
		btn.name = "Chip_" + cid
		btn.text = _t(cat["label"])
		btn.custom_minimum_size = Vector2(0, 42)
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn.add_theme_font_size_override("font_size", 13)
		if _cached_font:
			btn.add_theme_font_override("font", _cached_font)
		btn.pressed.connect(func(): set_category(cid))
		_chip_row.add_child(btn)
		_chip_buttons[cid] = btn

	_update_chip_visuals()

	_grid = GridContainer.new()
	_grid.columns = COLS
	_grid.add_theme_constant_override("h_separation", 6)
	_grid.add_theme_constant_override("v_separation", 6)
	_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_vbox.add_child(_grid)

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

		var icon := TextureRect.new()
		icon.name = "Icon"
		icon.set_anchors_preset(Control.PRESET_FULL_RECT)
		icon.offset_left = 6
		icon.offset_top = 4
		icon.offset_right = -6
		icon.offset_bottom = -6
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		icon.visible = false
		stack.add_child(icon)

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

	## 底部置中「一鍵整理」按鈕 (BtnSortItems，尺寸 120x48px，熱區>=48px，金黃果凍厚底 5px)
	var sort_box := HBoxContainer.new()
	sort_box.alignment = BoxContainer.ALIGNMENT_CENTER
	sort_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	grid_vbox.add_child(sort_box)

	_sort_btn = Button.new()
	_sort_btn.name = "BtnSortItems"
	_sort_btn.custom_minimum_size = Vector2(120, 48)
	_sort_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18))
	_sort_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18))
	_sort_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_GOLD, COLOR_BORDER, 2, 18))
	_sort_btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_sort_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_sort_btn.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_sort_btn.add_theme_font_override("font", _cached_font)
	_sort_btn.text = _t("一鍵整理")
	_sort_btn.pressed.connect(sort_items)
	sort_box.add_child(_sort_btn)

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

	var detail_vbox := VBoxContainer.new()
	detail_vbox.add_theme_constant_override("separation", 10)
	detail_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	detail_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	detail_margin.add_child(detail_vbox)

	_preview_row = HBoxContainer.new()
	_preview_row.add_theme_constant_override("separation", 14)
	_preview_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_preview_row.visible = false
	detail_vbox.add_child(_preview_row)

	_preview_frame = PanelContainer.new()
	_preview_frame.custom_minimum_size = Vector2(80, 80)
	_preview_frame.clip_contents = true
	_preview_frame.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 16))
	_preview_row.add_child(_preview_frame)

	var preview_stack := Control.new()
	preview_stack.set_anchors_preset(Control.PRESET_FULL_RECT)
	preview_stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_preview_frame.add_child(preview_stack)

	_detail_icon = TextureRect.new()
	_detail_icon.name = "DetailIcon"
	_detail_icon.set_anchors_preset(Control.PRESET_FULL_RECT)
	_detail_icon.offset_left = 6
	_detail_icon.offset_top = 4
	_detail_icon.offset_right = -6
	_detail_icon.offset_bottom = -6
	_detail_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_detail_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_detail_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_detail_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_detail_icon.visible = false
	preview_stack.add_child(_detail_icon)

	_detail_glyph = Label.new()
	_detail_glyph.name = "DetailGlyph"
	_detail_glyph.set_anchors_preset(Control.PRESET_FULL_RECT)
	_detail_glyph.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_detail_glyph.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_detail_glyph.clip_text = true
	_apply_label_style(_detail_glyph, 36, COLOR_TEXT_DARK)
	_detail_glyph.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_detail_glyph.visible = false
	preview_stack.add_child(_detail_glyph)

	var header_vbox := VBoxContainer.new()
	header_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	header_vbox.add_theme_constant_override("separation", 4)
	_preview_row.add_child(header_vbox)

	var name_row := HBoxContainer.new()
	name_row.add_theme_constant_override("separation", 8)
	header_vbox.add_child(name_row)

	_detail_name = Label.new()
	_detail_name.name = "DetailName"
	_apply_label_style(_detail_name, 20, COLOR_TEXT_DARK)
	name_row.add_child(_detail_name)

	_detail_count = Label.new()
	_detail_count.name = "DetailCount"
	_apply_label_style(_detail_count, 18, COLOR_TEXT_ORANGE)
	name_row.add_child(_detail_count)

	_lock_capsule = PanelContainer.new()
	_lock_capsule.name = "LockCapsule"
	_lock_capsule.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_lock_capsule.visible = false
	name_row.add_child(_lock_capsule)

	_lock_label = Label.new()
	_lock_label.name = "LockStatusLabel"
	_lock_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_lock_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_label_style(_lock_label, 14, COLOR_TEXT_DARK)
	_lock_capsule.add_child(_lock_label)

	_detail_kind = Label.new()
	_detail_kind.name = "DetailKind"
	_apply_label_style(_detail_kind, 16, Color("#6B5E80"))
	header_vbox.add_child(_detail_kind)

	## 裝備屬性預覽與差額比對膠囊列
	_stat_row = HBoxContainer.new()
	_stat_row.name = "StatRow"
	_stat_row.add_theme_constant_override("separation", 8)
	_stat_row.alignment = BoxContainer.ALIGNMENT_BEGIN
	_stat_row.visible = false
	header_vbox.add_child(_stat_row)

	_detail_stat = Label.new()
	_detail_stat.name = "StatPreview"
	_apply_label_style(_detail_stat, 16, COLOR_TEXT_DARK)
	_stat_row.add_child(_detail_stat)

	_diff_capsule = PanelContainer.new()
	_diff_capsule.name = "DiffCapsule"
	_diff_capsule.custom_minimum_size = Vector2(84, 28)
	_diff_capsule.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_diff_capsule.add_theme_stylebox_override("panel", _create_diff_capsule_style(COLOR_DIFF_EQ_BG, COLOR_DIFF_EQ_BD))
	_stat_row.add_child(_diff_capsule)

	_diff_label = Label.new()
	_diff_label.name = "DiffLabel"
	_diff_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_diff_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_label_style(_diff_label, 13, Color.WHITE)
	_diff_capsule.add_child(_diff_label)

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
	detail_vbox.add_child(_detail)

	## 按鈕列 (「鎖定/解鎖」按鈕 + 右側適應性操作按鈕)
	var btn_row := HBoxContainer.new()
	btn_row.name = "ActionBtnRow"
	btn_row.add_theme_constant_override("separation", 10)
	btn_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right.add_child(btn_row)

	## 「鎖定 / 解鎖」按鈕 (多巴胺果凍厚底規格，高 52px，熱區 >= 48px，立體厚底 5px，圓角 18px)
	_lock_btn = Button.new()
	_lock_btn.name = "BtnLock"
	_lock_btn.text = _t("鎖定")
	_lock_btn.custom_minimum_size = Vector2(88, 52)
	_lock_btn.visible = false
	_lock_btn.focus_mode = Control.FOCUS_NONE
	_lock_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_lock_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 5, 18))
	_lock_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFFDF0"), COLOR_BORDER, 5, 18))
	_lock_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 18))
	_lock_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_lock_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_lock_btn.add_theme_font_override("font", _cached_font)
	_lock_btn.pressed.connect(_on_lock_button_pressed)
	btn_row.add_child(_lock_btn)

	## 右側適應性操作按鈕 (預設薄荷綠果凍厚底按鈕，高 52px，熱區 >= 48px，立體厚底 5px)
	_use_btn = Button.new()
	_use_btn.name = "BtnAction"
	_use_btn.custom_minimum_size = Vector2(0, 52)
	_use_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_use_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
	_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
	_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
	_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
	_use_btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	_use_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_use_btn.add_theme_font_override("font", _cached_font)
	_use_btn.pressed.connect(_on_use_button_pressed)
	btn_row.add_child(_use_btn)

	## 裝備拆解回收按鈕 (珊瑚粉果凍厚底按鈕，高 52px，熱區 >= 48px，立體厚底 5px，圓角 18px)
	_dismantle_btn = Button.new()
	_dismantle_btn.name = "BtnDismantle"
	_dismantle_btn.text = _t("拆解回收")
	_dismantle_btn.custom_minimum_size = Vector2(0, 52)
	_dismantle_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_dismantle_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_dismantle_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_PINK, COLOR_BORDER, 5, 18))
	_dismantle_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7B9E"), COLOR_BORDER, 5, 18))
	_dismantle_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_PINK, COLOR_BORDER, 2, 18))
	_dismantle_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
	_dismantle_btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_dismantle_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_dismantle_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_dismantle_btn.add_theme_constant_override("outline_size", 3)
	_dismantle_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	_dismantle_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_dismantle_btn.add_theme_font_override("font", _cached_font)
	_dismantle_btn.pressed.connect(_on_dismantle_button_pressed)
	_dismantle_btn.visible = false
	right.add_child(_dismantle_btn)

	## 『前往鍛造』快捷按鈕 (暖橘果凍厚底按鈕，高 52px，熱區 >= 48px，立體厚底 5px，圓角 18px)
	_go_forge_btn = Button.new()
	_go_forge_btn.name = "BtnGoForge"
	_go_forge_btn.text = _t("前往鍛造")
	_go_forge_btn.custom_minimum_size = Vector2(0, 52)
	_go_forge_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_go_forge_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_go_forge_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 18))
	_go_forge_btn.add_theme_stylebox_override("hover", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18))
	_go_forge_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 18))
	_go_forge_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
	_go_forge_btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_go_forge_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_go_forge_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_go_forge_btn.add_theme_constant_override("outline_size", 3)
	_go_forge_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	_go_forge_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_go_forge_btn.add_theme_font_override("font", _cached_font)
	_go_forge_btn.pressed.connect(_on_go_forge_pressed)
	_go_forge_btn.visible = false
	right.add_child(_go_forge_btn)

	## 『前往工坊』快捷按鈕 (薄荷綠果凍厚底按鈕，高 52px，熱區 >= 48px，立體厚底 5px，圓角 18px)
	_go_workshop_btn = Button.new()
	_go_workshop_btn.name = "BtnGoWorkshop"
	_go_workshop_btn.text = _t("前往工坊")
	_go_workshop_btn.custom_minimum_size = Vector2(0, 52)
	_go_workshop_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_go_workshop_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_go_workshop_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
	_go_workshop_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
	_go_workshop_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
	_go_workshop_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
	_go_workshop_btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
	_go_workshop_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_go_workshop_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_go_workshop_btn.add_theme_constant_override("outline_size", 3)
	_go_workshop_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	_go_workshop_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_go_workshop_btn.add_theme_font_override("font", _cached_font)
	_go_workshop_btn.pressed.connect(_on_go_workshop_pressed)
	_go_workshop_btn.visible = false
	right.add_child(_go_workshop_btn)

	## 「放到快捷欄」按鈕 (天藍果凍厚底按鈕，高 52px)
	_hb_btn = Button.new()
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
	_tip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(_tip, 16, Color("#6B5E80"))
	right.add_child(_tip)

	_update_ui_texts()


func open() -> void:
	visible = true
	if _card == null:
		_build()
	_update_ui_texts()
	var inv: Node = null
	if Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
	var list: Array = inv.call("bag_list") if inv else []
	## 若尚未選取且背包有物品，預設選取第一個，確保格子與明細同時呈現
	if _selected == "" and list.size() > 0:
		var first_it = list[0]
		if first_it is Dictionary and first_it.has("id"):
			_selected = str(first_it["id"])
	_update_chip_visuals()
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

	var gs_node: Node = null
	if Engine.get_main_loop() is SceneTree:
		gs_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GameState")
	if gs_node and "equip_bag" in gs_node and gs_node.equip_bag is Array:
		for e in gs_node.equip_bag:
			if e is Dictionary:
				var uid := str(e.get("uid", ""))
				if not uid.is_empty():
					var in_list := false
					for existing in list:
						if str(existing.get("id", "")) == uid:
							in_list = true
							break
					if not in_list:
						list.append({
							"id": uid,
							"count": 1,
							"def": {
								"name": e.get("name", uid),
								"kind": "weapon" if str(e.get("slot", "")) == "weapon" else "equipment",
								"slot": str(e.get("slot", "weapon")),
								"desc": _t("器階：第 %d 階  品質：%s") % [int(e.get("tier", 1)), _t(str(e.get("quality_label", "")))],
								"glyph": "刃" if str(e.get("slot", "")) == "weapon" else "裝"
							}
						})

	if _is_sorted:
		list = sort_item_list(list)

	# 依當前選擇之 Chip 分類過濾物品列表
	if _current_category != "all":
		var filtered: Array = []
		for it in list:
			if it is Dictionary and item_matches_category(it, _current_category):
				filtered.append(it)
		list = filtered

	## 若目前已選取的道具已經不在當前過濾列表中，重設選取狀態
	if _selected != "":
		var found := false
		for it in list:
			if it is Dictionary and str(it.get("id", "")) == _selected:
				found = true
				break
		if not found:
			_selected = ""
	elif list.size() > 0 and _current_category == "all" and not visible:
		_selected = str(list[0].get("id", ""))

	for i in _cells.size():
		var cell: PanelContainer = _cells[i]
		var icon: TextureRect = cell.find_child("Icon", true, false)
		var g: Label = cell.find_child("Glyph", true, false)
		var c: Label = cell.find_child("Count", true, false)
		if i < list.size():
			var it: Dictionary = list[i]
			var id := str(it.get("id", ""))
			_bag_ids.append(id)
			var def: Dictionary = it.get("def", {})
			cell.tooltip_text = str(def.get("name", id))
			var icon_tex := get_item_icon(id)
			if icon_tex != null:
				if icon:
					icon.texture = icon_tex
					icon.visible = true
				if g:
					g.visible = false
			else:
				if icon:
					icon.visible = false
				if g:
					var raw_glyph := str(def.get("glyph", "·"))
					var t_glyph := ContentLoc.text("ui", raw_glyph)
					g.text = t_glyph
					if t_glyph.length() > 2:
						g.add_theme_font_size_override("font_size", 12)
					elif t_glyph.length() > 1:
						g.add_theme_font_size_override("font_size", 16)
					else:
						g.add_theme_font_size_override("font_size", 24)
					g.add_theme_color_override("font_color", def.get("color", COLOR_TEXT_DARK))
					g.visible = true
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
			cell.tooltip_text = ""
			if icon:
				icon.visible = false
			if g:
				g.text = ""
				g.visible = false
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
		if _preview_row:
			_preview_row.visible = false
		if _stat_row:
			_stat_row.visible = false
		if _lock_capsule:
			_lock_capsule.visible = false
		if _lock_btn:
			_lock_btn.visible = false
		if _detail:
			_detail.text = "[color=#1F1A3A][b]%s[/b]\n\n%s\n\n[color=#C2600A]•[/color] %s\n[color=#C2600A]•[/color] %s\n[color=#C2600A]•[/color] %s[/color]" % [
				_t("冒險者背包"),
				_t("請點選左側格子查看道具詳情。"),
				_t("消耗品：使用回復狀態"),
				_t("素材：點擊使用可賣出金幣"),
				_t("重要物：劇情關鍵道具")
			]
		if _use_btn:
			_use_btn.disabled = true
			_use_btn.text = _t("使用 / 賣出")
			_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
			_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
		if _hb_btn:
			_hb_btn.disabled = true
			_hb_btn.text = _t("放到快捷欄")
			_hb_btn.visible = true
		if _dismantle_btn:
			_dismantle_btn.visible = false
		if _go_forge_btn:
			_go_forge_btn.visible = false
		if _go_workshop_btn:
			_go_workshop_btn.visible = false
		return

	_update_action_button(inv)
	_update_dismantle_button()
	_update_shortcut_buttons()
	if _hb_btn and not _is_selected_item_equipment():
		_hb_btn.disabled = false
		_hb_btn.text = _t("放到快捷欄")
		_hb_btn.visible = true

	var def: Dictionary = inv.call("catalog", _selected) as Dictionary
	var eq_inst: Dictionary = {}
	var eq_node: Node = null
	if Engine.get_main_loop() is SceneTree:
		eq_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EquipmentSystem")
	if eq_node and eq_node.has_method("find_bag"):
		eq_inst = eq_node.call("find_bag", _selected) as Dictionary

	if def.is_empty():
		if not eq_inst.is_empty():
			def = {
				"name": eq_inst.get("name", _selected),
				"kind": "equip",
				"slot": eq_inst.get("slot", "weapon"),
				"desc": _t("品質：%s · 部位：%s") % [str(eq_inst.get("quality_label", "")), str(eq_inst.get("slot", ""))],
				"rolled": eq_inst.get("rolled", {}),
			}
		else:
			var gs_node: Node = null
			if Engine.get_main_loop() is SceneTree:
				gs_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GameState")
			if gs_node and "equip_worn" in gs_node and gs_node.equip_worn is Dictionary and gs_node.equip_worn.has(_selected):
				var ew: Dictionary = gs_node.equip_worn[_selected] as Dictionary
				eq_inst = ew
				def = {
					"name": ew.get("name", _selected),
					"kind": "equip",
					"slot": ew.get("slot", "weapon"),
					"desc": _t("品質：%s · 部位：%s") % [str(ew.get("quality_label", "")), str(ew.get("slot", ""))],
					"rolled": ew.get("rolled", {}),
				}
			elif gs_node and "equip_bag" in gs_node and gs_node.equip_bag is Array:
				for e in gs_node.equip_bag:
					if e is Dictionary:
						if str(e.get("uid", "")) == _selected or str(e.get("base_id", "")) == _selected or str(e.get("id", "")) == _selected:
							eq_inst = e
							def = {
								"name": e.get("name", _selected),
								"kind": "equip",
								"slot": e.get("slot", "weapon"),
								"desc": _t("品質：%s · 部位：%s") % [str(e.get("quality_label", "")), str(e.get("slot", ""))],
								"rolled": e.get("rolled", {}),
							}
							break

	if def.is_empty():
		var dt_node: Node = null
		if Engine.get_main_loop() is SceneTree:
			dt_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("DataTables")
		if dt_node and dt_node.has_method("equip_bases"):
			var bases: Dictionary = dt_node.call("equip_bases") as Dictionary
			if bases.has(_selected):
				var b: Dictionary = bases[_selected]
				def = {
					"name": b.get("name", _selected),
					"kind": "equip",
					"slot": b.get("slot", "weapon"),
					"desc": _t("裝備 · 部位：%s") % [str(b.get("slot", ""))],
					"base": b.get("base", {}),
				}
	var n: int = int(inv.call("count", _selected)) if inv.has_method("count") else 1
	var kind: String = str(def.get("kind", ""))
	var slot: String = str(def.get("slot", "")).to_lower()
	if slot.is_empty():
		if not eq_inst.is_empty():
			slot = str(eq_inst.get("slot", "")).to_lower()
		elif kind == "weapon" or _selected in ["rusty_blade", "meager_edge"]:
			slot = "weapon"
		elif kind in ["armor", "shield"] or _selected in ["ash_mail", "knight_plate", "viking_hide"]:
			slot = "armor"

	var kind_s: String = kind
	match kind:
		"consumable":
			kind_s = _t("消耗品")
		"material":
			kind_s = _t("素材（點擊使用可賣出）")
		"key":
			kind_s = _t("重要道具")
		"weapon":
			kind_s = _t("武器")
		"armor":
			kind_s = _t("防具")
		"equipment", "equip":
			if slot == "weapon":
				kind_s = _t("武器")
			elif slot == "armor":
				kind_s = _t("防具")
			else:
				kind_s = _t("裝備")
		"gem", "jewel":
			kind_s = _t("寶石")
		_:
			if slot == "weapon":
				kind_s = _t("武器")
			elif slot == "armor":
				kind_s = _t("防具")
			else:
				kind_s = _t(kind) if kind != "" else ""

	var item_name: String = str(def.get("name", _selected))
	var item_desc: String = str(def.get("desc", ""))

	var icon_tex := get_item_icon(_selected)
	if _preview_row:
		_preview_row.visible = true
		if _detail_name:
			_detail_name.text = item_name
		if _detail_count:
			_detail_count.text = "×%d" % n
		if _detail_kind:
			_detail_kind.text = _t("類型：%s") % kind_s
		if icon_tex != null:
			if _detail_icon:
				_detail_icon.texture = icon_tex
				_detail_icon.visible = true
			if _detail_glyph:
				_detail_glyph.visible = false
		else:
			if _detail_icon:
				_detail_icon.visible = false
			if _detail_glyph:
				var raw_glyph := str(def.get("glyph", "·"))
				var t_glyph := ContentLoc.text("ui", raw_glyph)
				_detail_glyph.text = t_glyph
				if t_glyph.length() > 2:
					_detail_glyph.add_theme_font_size_override("font_size", 16)
				elif t_glyph.length() > 1:
					_detail_glyph.add_theme_font_size_override("font_size", 22)
				else:
					_detail_glyph.add_theme_font_size_override("font_size", 36)
				_detail_glyph.visible = true

	# ── 屬性預覽與差額比對膠囊 ──
	_update_stat_comparison(def, eq_inst, slot, kind)

	# ── 裝備鎖定狀態與按鈕更新 ──
	var item_dict: Dictionary = {"id": _selected, "def": def}
	var is_equip: bool = item_matches_category(item_dict, "equip") or not eq_inst.is_empty() or kind in ["weapon", "equipment", "equip", "armor", "accessory", "shield"] or slot in ["weapon", "armor"]
	if is_equip:
		var uid := _get_selected_equip_uid()
		var locked := is_item_locked(uid)
		_update_lock_ui(locked)
		if locked:
			item_desc += "\n[color=#E05020]%s[/color]" % _t("裝備已鎖定無法出售")
	else:
		if _lock_capsule:
			_lock_capsule.visible = false
		if _lock_btn:
			_lock_btn.visible = false

	if _detail:
		_detail.text = "[color=#4A3E60]%s[/color]" % item_desc

	_update_dismantle_button()
	_update_shortcut_buttons()


func _update_action_button(inv: Node = null) -> void:
	if _use_btn == null or not is_instance_valid(_use_btn):
		return

	if _selected == "":
		_use_btn.disabled = true
		_use_btn.text = _t("使用 / 賣出")
		_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
		_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
		return

	if inv == null and Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")

	var def: Dictionary = inv.call("catalog", _selected) as Dictionary if inv else {}
	if def.is_empty():
		var eq_node: Node = null
		if Engine.get_main_loop() is SceneTree:
			eq_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq_node and eq_node.has_method("find_bag"):
			var eq_inst: Dictionary = eq_node.call("find_bag", _selected) as Dictionary
			if not eq_inst.is_empty():
				def = {
					"name": eq_inst.get("name", _selected),
					"kind": "equip",
					"slot": eq_inst.get("slot", "weapon"),
				}
		if def.is_empty():
			var gs_node: Node = null
			if Engine.get_main_loop() is SceneTree:
				gs_node = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("GameState")
			if gs_node and "equip_worn" in gs_node and gs_node.equip_worn is Dictionary and gs_node.equip_worn.has(_selected):
				var ew: Dictionary = gs_node.equip_worn[_selected] as Dictionary
				def = {
					"name": ew.get("name", _selected),
					"kind": "equip",
					"slot": ew.get("slot", "weapon"),
				}

	var item_dict: Dictionary = {"id": _selected, "def": def}
	var kind: String = str(def.get("kind", "")).to_lower()
	var id: String = _selected.to_lower()

	if kind in ["key", "important", "quest"] or id.begins_with("key_"):
		_use_btn.disabled = true
		_use_btn.text = _t("重要物品")
		_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
		_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	elif item_matches_category(item_dict, "equip"):
		if is_selected_item_equipped():
			_use_btn.disabled = true
			_use_btn.text = _t("已穿戴")
			_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
			_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
		else:
			_use_btn.disabled = false
			_use_btn.text = _t("立即裝備")
			_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 18))
			_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFB642"), COLOR_BORDER, 5, 18))
			_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 18))
			_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	elif item_matches_category(item_dict, "material"):
		if is_item_locked(_selected):
			_use_btn.disabled = true
			_use_btn.text = _t("已鎖定（無法出售）")
			_use_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
			_use_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
		else:
			_use_btn.disabled = false
			_use_btn.text = _t("賣出")
			_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
			_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
			_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
			_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	elif item_matches_category(item_dict, "consumable"):
		_use_btn.disabled = false
		_use_btn.text = _t("使用")
		_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
		_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
		_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
		_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	else:
		_use_btn.disabled = false
		_use_btn.text = _t("使用")
		_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
		_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
		_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
		_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)


func _on_use_button_pressed() -> void:
	if _selected == "":
		return

	var inv: Node = null
	if Engine.get_main_loop() is SceneTree:
		inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")

	var def: Dictionary = inv.call("catalog", _selected) as Dictionary if inv else {}
	var item_dict: Dictionary = {"id": _selected, "def": def}
	var kind: String = str(def.get("kind", "")).to_lower()
	var id: String = _selected.to_lower()

	if kind in ["key", "important", "quest"] or id.begins_with("key_"):
		return

	if item_matches_category(item_dict, "equip"):
		if is_selected_item_equipped():
			return
		_equip_selected_item()
		return

	if item_matches_category(item_dict, "material") or kind == "material":
		if is_item_locked(_selected):
			_show_tip(_t("裝備已鎖定無法出售"))
			return

	item_used.emit(_selected)
	refresh()


func _equip_selected_item() -> void:
	var loop := Engine.get_main_loop()
	var eq_sys: Node = null
	if loop is SceneTree and (loop as SceneTree).root != null:
		eq_sys = (loop as SceneTree).root.get_node_or_null("EquipmentSystem")

	var uid_to_equip := _selected
	if eq_sys:
		var inst: Dictionary = eq_sys.call("find_bag", _selected) as Dictionary
		if inst.is_empty():
			var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
			if gs and "equip_bag" in gs and gs.equip_bag is Array:
				for e in gs.equip_bag:
					if e is Dictionary:
						if str(e.get("uid", "")) == _selected or str(e.get("base_id", "")) == _selected or str(e.get("id", "")) == _selected:
							inst = e
							uid_to_equip = str(e.get("uid", _selected))
							break

		if inst.is_empty():
			var inv_sys: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
			var it_def: Dictionary = inv_sys.call("catalog", _selected) as Dictionary if inv_sys else {}
			var raw_slot := str(it_def.get("slot", ""))
			if raw_slot.is_empty():
				var k := str(it_def.get("kind", "")).to_lower()
				if k == "weapon":
					raw_slot = "weapon"
				elif k in ["equipment", "equip", "armor"]:
					raw_slot = "armor"
				else:
					raw_slot = "weapon"

			if eq_sys.has_method("roll_instance"):
				inst = eq_sys.call("roll_instance", _selected, "common") as Dictionary
			if inst.is_empty():
				var rolled_stats: Dictionary = {}
				if raw_slot == "armor":
					rolled_stats = {"def": float(it_def.get("def", 5.0)), "hp": float(it_def.get("hp", 15.0))}
				else:
					rolled_stats = {"atk": float(it_def.get("atk", 10.0))}
				inst = {
					"uid": "equip_" + _selected + "_" + str(Time.get_ticks_msec()),
					"base_id": _selected,
					"name": str(it_def.get("name", _selected)),
					"slot": raw_slot,
					"tier": int(it_def.get("tier", 1)),
					"line": str(it_def.get("line", "")),
					"quality": "common",
					"quality_label": "凡品",
					"rolled": rolled_stats,
					"bound": false,
				}
			if eq_sys.has_method("add_to_bag"):
				eq_sys.call("add_to_bag", inst)
			uid_to_equip = str(inst.get("uid", _selected))

		if eq_sys.has_method("equip"):
			eq_sys.call("equip", uid_to_equip)

	if loop is SceneTree and (loop as SceneTree).root != null:
		var am: Node = (loop as SceneTree).root.get_node_or_null("AudioManager")
		if am and am.has_method("play_ui"):
			am.call("play_ui")

	equipment_changed.emit()
	refresh()


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
		_on_use_button_pressed()
		return
	if button == MOUSE_BUTTON_LEFT:
		var now := Time.get_ticks_msec()
		if _last_click_i == idx and now - _last_click_t < 350:
			_selected = id
			_on_use_button_pressed()
			_last_click_i = -1
			return
		_last_click_i = idx
		_last_click_t = now
		_selected = id
		refresh()


func get_use_button() -> Button:
	return _use_btn


func sort_items() -> void:
	_is_sorted = true
	_play_sort_feedback()
	refresh()
	items_sorted.emit()


func get_sort_button() -> Button:
	return _sort_btn


func is_sorted() -> bool:
	return _is_sorted


func get_chip_buttons() -> Dictionary:
	return _chip_buttons


func get_chip_button(category: String) -> Button:
	return _chip_buttons.get(category, null)


func get_current_category() -> String:
	return _current_category


func set_category(cat_id: String) -> void:
	var changed := (_current_category != cat_id)
	_current_category = cat_id

	if changed:
		var loop := Engine.get_main_loop()
		if loop is SceneTree and (loop as SceneTree).root != null:
			var am: Node = (loop as SceneTree).root.get_node_or_null("AudioManager")
			if am and am.has_method("play_ui"):
				am.call("play_ui")

	# 若目前選取的道具不在新分類中，重設選取狀態
	if _selected != "":
		var inv: Node = null
		if Engine.get_main_loop() is SceneTree:
			inv = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("InventorySystem")
		var it_def: Dictionary = inv.call("catalog", _selected) if inv else {}
		var it_dict: Dictionary = {"id": _selected, "def": it_def}
		if not item_matches_category(it_dict, _current_category):
			_selected = ""

	_update_chip_visuals()
	refresh()
	if changed:
		category_changed.emit(_current_category)


func _update_chip_visuals() -> void:
	for cat in CHIP_CATEGORIES:
		var cid: String = cat["id"]
		if _chip_buttons.has(cid):
			var btn: Button = _chip_buttons[cid]
			if btn and is_instance_valid(btn):
				var is_sel := (cid == _current_category)
				btn.add_theme_stylebox_override("normal", _create_chip_style(is_sel, false, false))
				btn.add_theme_stylebox_override("hover", _create_chip_style(is_sel, false, true))
				btn.add_theme_stylebox_override("pressed", _create_chip_style(is_sel, true, false))
				btn.add_theme_stylebox_override("focus", StyleBoxEmpty.new())
				if is_sel:
					btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
					btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
					btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
				else:
					btn.add_theme_color_override("font_color", Color("#4D456B"))
					btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
					btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)


static func item_matches_category(item: Dictionary, category: String) -> bool:
	if category == "all" or category.is_empty():
		return true
	var def: Dictionary = item.get("def", {})
	var kind: String = str(def.get("kind", item.get("kind", ""))).to_lower()
	var id: String = str(item.get("id", "")).to_lower()

	match category:
		"equip":
			return kind in ["weapon", "equipment", "equip", "armor", "accessory", "shield", "helm", "boots"] or id.begins_with("wpn_") or id.begins_with("equip_") or id.begins_with("arm_")
		"gem":
			return kind in ["gem", "jewel", "stone"] or id.begins_with("gem_")
		"consumable":
			return kind in ["consumable", "potion", "food", "scroll"] or id.begins_with("pot_")
		"material":
			return kind in ["material", "mat", "ore", "craft"] or id.begins_with("mat_")
		_:
			return kind == category


func _play_sort_feedback() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var am: Node = (loop as SceneTree).root.get_node_or_null("AudioManager")
		if am and am.has_method("play_ui"):
			am.call("play_ui")
	if _sort_btn and is_instance_valid(_sort_btn):
		var tw := _sort_btn.create_tween()
		if tw:
			_sort_btn.pivot_offset = _sort_btn.size / 2.0
			tw.tween_property(_sort_btn, "scale", Vector2(1.06, 1.06), 0.08)
			tw.tween_property(_sort_btn, "scale", Vector2(1.0, 1.0), 0.08)
	for cell in _cells:
		if cell is Control and is_instance_valid(cell):
			var tw_c: Tween = (cell as Control).create_tween()
			if tw_c:
				tw_c.tween_property(cell, "modulate", Color(1.15, 1.15, 1.0, 1.0), 0.08)
				tw_c.tween_property(cell, "modulate", Color.WHITE, 0.12)


static func get_item_category_priority(item: Dictionary) -> int:
	var def: Dictionary = item.get("def", {})
	var kind: String = str(def.get("kind", item.get("kind", ""))).to_lower()
	var id: String = str(item.get("id", "")).to_lower()

	# 1. 裝備 (weapon, equipment, equip, armor, accessory, shield, etc.)
	if kind in ["weapon", "equipment", "equip", "armor", "accessory", "shield", "helm", "boots"] or id.begins_with("wpn_") or id.begins_with("equip_") or id.begins_with("arm_"):
		return 1

	# 2. 寶石 (gem, jewel, stone, etc.)
	if kind in ["gem", "jewel", "stone"] or id.begins_with("gem_"):
		return 2

	# 3. 消耗品 (consumable, potion, food, etc.)
	if kind in ["consumable", "potion", "food", "scroll"]:
		return 3

	# 4. 材料 (material, mat, ore, ingredient, etc.)
	if kind in ["material", "mat", "ore", "craft"]:
		return 4

	# 5. 其他（如 key/重要道具）
	return 5


static func get_item_quality_score(item: Dictionary) -> int:
	var def: Dictionary = item.get("def", {})
	var q = def.get("quality", item.get("quality", null))
	if q is int or q is float:
		return int(q)
	if q is String and not str(q).is_empty():
		match str(q).to_lower():
			"mythic", "legendary", "神話", "傳奇", "秘寶":
				return 5
			"epic", "史詩", "極品":
				return 4
			"rare", "稀有", "上品":
				return 3
			"uncommon", "優秀", "良品":
				return 2
			"common", "普通", "凡品":
				return 1
	var q_lbl: String = str(def.get("quality_label", item.get("quality_label", "")))
	if not q_lbl.is_empty():
		match q_lbl:
			"秘寶", "神話", "傳奇", "Legendary", "Mythic":
				return 5
			"極品", "史詩", "Epic":
				return 4
			"上品", "稀有", "Rare":
				return 3
			"良品", "優秀", "Uncommon":
				return 2
			"凡品", "普通", "Common":
				return 1
	var lvl = def.get("level", item.get("level", def.get("tier", item.get("tier", 0))))
	if lvl is int or lvl is float:
		if int(lvl) > 0:
			return int(lvl)
	return 1


static func sort_items_comparator(a: Dictionary, b: Dictionary) -> bool:
	var cat_a := get_item_category_priority(a)
	var cat_b := get_item_category_priority(b)
	if cat_a != cat_b:
		return cat_a < cat_b

	var qual_a := get_item_quality_score(a)
	var qual_b := get_item_quality_score(b)
	if qual_a != qual_b:
		return qual_a > qual_b

	return str(a.get("id", "")) < str(b.get("id", ""))


static func sort_item_list(items: Array) -> Array:
	var sorted := items.duplicate()
	sorted.sort_custom(sort_items_comparator)
	return sorted


# ── 裝備戰力差額比對與屬性預覽邏輯 ──
func _update_stat_comparison(def: Dictionary, eq_inst: Dictionary, slot: String, kind: String) -> void:
	if _stat_row == null or _diff_capsule == null or _diff_label == null or _detail_stat == null:
		return

	var is_weapon := (slot == "weapon" or kind == "weapon" or _selected in ["rusty_blade", "meager_edge"])
	var is_armor := (slot == "armor" or kind == "armor" or _selected in ["ash_mail", "knight_plate", "viking_hide"])

	if not (is_weapon or is_armor):
		_stat_row.visible = false
		return

	_stat_row.visible = true

	if is_weapon:
		var atk: int = _get_item_atk(_selected, def, eq_inst)
		var stat_text: String = "%s +%d" % [_t("攻擊"), atk]
		var crit: float = _get_item_crit(_selected, def, eq_inst)
		if crit > 0.0:
			stat_text += " · %s +%.1f%%" % [_t("暴擊"), crit]
		_detail_stat.text = stat_text

		if is_selected_item_equipped():
			_apply_equipped_capsule()
		else:
			var cur_atk: int = _get_current_equipped_weapon_atk()
			var diff: int = atk - cur_atk
			_apply_diff_capsule(diff, _t("攻擊"))
	elif is_armor:
		var def_val: int = _get_item_def(_selected, def, eq_inst)
		var stat_text: String = "%s +%d" % [_t("防禦"), def_val]
		var hp: int = _get_item_hp(_selected, def, eq_inst)
		if hp > 0:
			stat_text += " · %s +%d" % [_t("生命"), hp]
		_detail_stat.text = stat_text

		if is_selected_item_equipped():
			_apply_equipped_capsule()
		else:
			var cur_def: int = _get_current_equipped_armor_def()
			var diff: int = def_val - cur_def
			_apply_diff_capsule(diff, _t("防禦"))


func _apply_equipped_capsule() -> void:
	if _diff_capsule == null or _diff_label == null:
		return

	_diff_capsule.visible = true
	_diff_label.text = _t("穿戴中")
	_diff_capsule.add_theme_stylebox_override("panel", _create_diff_capsule_style(COLOR_DIFF_WORN_BG, COLOR_DIFF_WORN_BD))
	_diff_label.add_theme_color_override("font_color", COLOR_DIFF_WORN_TEXT)


func is_selected_item_equipped() -> bool:
	if _selected.is_empty():
		return false
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return false
	var root_node := (loop as SceneTree).root

	# 1. EquipmentSystem.is_equipped 檢查
	var eq_node: Node = root_node.get_node_or_null("EquipmentSystem")
	if eq_node and eq_node.has_method("is_equipped"):
		if bool(eq_node.call("is_equipped", _selected)):
			return true

	# 2. GameState equip_worn 與 equip_slots / weapon_loadout 檢查
	var gs_node: Node = root_node.get_node_or_null("GameState")
	if gs_node:
		if "equip_worn" in gs_node and gs_node.equip_worn is Dictionary:
			if gs_node.equip_worn.has(_selected):
				return true
		if "equip_slots" in gs_node and gs_node.equip_slots is Dictionary:
			for slot_key in gs_node.equip_slots:
				if str(gs_node.equip_slots[slot_key]) == _selected and _selected != "":
					return true
		if "weapon_loadout" in gs_node and gs_node.weapon_loadout is Array:
			for w_uid in gs_node.weapon_loadout:
				if str(w_uid) == _selected and _selected != "":
					return true

	return false


func _apply_diff_capsule(diff: int, stat_name: String) -> void:
	if _diff_capsule == null or _diff_label == null:
		return

	_diff_capsule.visible = true

	if diff > 0:
		_diff_label.text = "+%d %s" % [diff, stat_name]
		_diff_capsule.add_theme_stylebox_override("panel", _create_diff_capsule_style(COLOR_DIFF_POS_BG, COLOR_DIFF_POS_BD))
		_diff_label.add_theme_color_override("font_color", COLOR_DIFF_POS_TEXT)
	elif diff < 0:
		_diff_label.text = "-%d %s" % [absi(diff), stat_name]
		_diff_capsule.add_theme_stylebox_override("panel", _create_diff_capsule_style(COLOR_DIFF_NEG_BG, COLOR_DIFF_NEG_BD))
		_diff_label.add_theme_color_override("font_color", COLOR_DIFF_NEG_TEXT)
	else:
		_diff_label.text = "--"
		_diff_capsule.add_theme_stylebox_override("panel", _create_diff_capsule_style(COLOR_DIFF_EQ_BG, COLOR_DIFF_EQ_BD))
		_diff_label.add_theme_color_override("font_color", COLOR_DIFF_EQ_TEXT)


func _get_current_equipped_weapon_atk() -> int:
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return 0
	var root_node := (loop as SceneTree).root
	var eq_node: Node = root_node.get_node_or_null("EquipmentSystem")
	var cur_w: Dictionary = {}
	if eq_node and eq_node.has_method("active_weapon_inst"):
		cur_w = eq_node.call("active_weapon_inst") as Dictionary
	if cur_w.is_empty() and eq_node and eq_node.has_method("loadout_uid"):
		var idx: int = eq_node.call("active_loadout_index") if eq_node.has_method("active_loadout_index") else 0
		var uid: String = eq_node.call("loadout_uid", idx)
		if uid != "" and eq_node.has_method("weapon_inst"):
			cur_w = eq_node.call("weapon_inst", uid) as Dictionary
	if cur_w.is_empty():
		var gs: Node = root_node.get_node_or_null("GameState")
		if gs and "equip_slots" in gs and "equip_worn" in gs and gs.equip_slots is Dictionary and gs.equip_worn is Dictionary:
			var w_uid: String = str(gs.equip_slots.get("weapon", ""))
			if w_uid != "" and gs.equip_worn.has(w_uid):
				cur_w = gs.equip_worn[w_uid] as Dictionary
			elif w_uid != "":
				for k in gs.equip_worn:
					var inst: Dictionary = gs.equip_worn[k] as Dictionary
					if str(inst.get("uid", "")) == w_uid or str(inst.get("base_id", "")) == w_uid:
						cur_w = inst
						break
				if cur_w.is_empty():
					var inv_node: Node = root_node.get_node_or_null("InventorySystem")
					var c_def: Dictionary = inv_node.call("catalog", w_uid) as Dictionary if inv_node else {}
					if not c_def.is_empty():
						cur_w = c_def

	if cur_w.is_empty():
		return 0
	return _get_item_atk(cur_w.get("uid", cur_w.get("base_id", "")), cur_w, cur_w)


func _get_current_equipped_armor_def() -> int:
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return 0
	var root_node := (loop as SceneTree).root
	var cur_arm: Dictionary = {}
	var gs: Node = root_node.get_node_or_null("GameState")
	if gs and "equip_slots" in gs and "equip_worn" in gs and gs.equip_slots is Dictionary and gs.equip_worn is Dictionary:
		var arm_uid: String = str(gs.equip_slots.get("armor", ""))
		if arm_uid != "" and gs.equip_worn.has(arm_uid):
			cur_arm = gs.equip_worn[arm_uid] as Dictionary
		elif arm_uid != "":
			for k in gs.equip_worn:
				var inst: Dictionary = gs.equip_worn[k] as Dictionary
				if str(inst.get("uid", "")) == arm_uid or str(inst.get("base_id", "")) == arm_uid:
					cur_arm = inst
					break
			if cur_arm.is_empty():
				var inv_node: Node = root_node.get_node_or_null("InventorySystem")
				var c_def: Dictionary = inv_node.call("catalog", arm_uid) as Dictionary if inv_node else {}
				if not c_def.is_empty():
					cur_arm = c_def

	if cur_arm.is_empty():
		return 0
	return _get_item_def(cur_arm.get("uid", cur_arm.get("base_id", "")), cur_arm, cur_arm)


func _get_item_atk(id: String, def: Dictionary = {}, inst: Dictionary = {}) -> int:
	if not inst.is_empty():
		if inst.has("weapon_atk"):
			return int(inst["weapon_atk"])
		var r: Dictionary = inst.get("rolled", {})
		if r.has("atk") and int(r["atk"]) > 0:
			return int(r["atk"])
		var b: Dictionary = inst.get("base", {})
		if b.has("atk") and int(b["atk"]) > 0:
			return int(b["atk"])

	if not def.is_empty():
		if def.has("weapon_atk"):
			return int(def["weapon_atk"])
		var r2: Dictionary = def.get("rolled", {})
		if r2.has("atk") and int(r2["atk"]) > 0:
			return int(r2["atk"])
		var b2: Dictionary = def.get("base", {})
		if b2.has("atk") and int(b2["atk"]) > 0:
			return int(b2["atk"])
		if def.has("atk") and int(def["atk"]) > 0:
			return int(def["atk"])

	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("equip_bases"):
			var bases: Dictionary = dt.call("equip_bases") as Dictionary
			var base_id: String = id
			if not inst.is_empty() and inst.has("base_id"):
				base_id = str(inst["base_id"])
			elif not def.is_empty() and def.has("base_id"):
				base_id = str(def["base_id"])
			if bases.has(base_id):
				return int(bases[base_id].get("base", {}).get("atk", 0))

	return 0


func _get_item_def(id: String, def: Dictionary = {}, inst: Dictionary = {}) -> int:
	if not inst.is_empty():
		if inst.has("armor_def"):
			return int(inst["armor_def"])
		var r: Dictionary = inst.get("rolled", {})
		if r.has("def") and int(r["def"]) > 0:
			return int(r["def"])
		var b: Dictionary = inst.get("base", {})
		if b.has("def") and int(b["def"]) > 0:
			return int(b["def"])

	if not def.is_empty():
		if def.has("armor_def"):
			return int(def["armor_def"])
		var r2: Dictionary = def.get("rolled", {})
		if r2.has("def") and int(r2["def"]) > 0:
			return int(r2["def"])
		var b2: Dictionary = def.get("base", {})
		if b2.has("def") and int(b2["def"]) > 0:
			return int(b2["def"])
		if def.has("def") and int(def["def"]) > 0:
			return int(def["def"])

	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var dt: Node = (loop as SceneTree).root.get_node_or_null("DataTables")
		if dt and dt.has_method("equip_bases"):
			var bases: Dictionary = dt.call("equip_bases") as Dictionary
			var base_id: String = id
			if not inst.is_empty() and inst.has("base_id"):
				base_id = str(inst["base_id"])
			elif not def.is_empty() and def.has("base_id"):
				base_id = str(def["base_id"])
			if bases.has(base_id):
				return int(bases[base_id].get("base", {}).get("def", 0))

	return 0


func _get_item_crit(_id: String, def: Dictionary = {}, inst: Dictionary = {}) -> float:
	var r: Dictionary = inst.get("rolled", def.get("rolled", {}))
	if r.has("crit"):
		return float(r["crit"])
	var b: Dictionary = inst.get("base", def.get("base", {}))
	if b.has("crit"):
		return float(b["crit"])
	return 0.0


func _get_item_hp(_id: String, def: Dictionary = {}, inst: Dictionary = {}) -> int:
	var r: Dictionary = inst.get("rolled", def.get("rolled", {}))
	if r.has("hp"):
		return int(r["hp"])
	var b: Dictionary = inst.get("base", def.get("base", {}))
	if b.has("hp"):
		return int(b["hp"])
	return 0


func get_stat_row() -> HBoxContainer:
	return _stat_row


func get_stat_preview() -> Label:
	return _detail_stat


func get_diff_capsule() -> PanelContainer:
	return _diff_capsule


func get_diff_label() -> Label:
	return _diff_label


# ── 裝備鎖定與解鎖切換邏輯 ──
func _update_lock_ui(locked: bool) -> void:
	if _lock_capsule and _lock_label:
		_lock_capsule.visible = true
		var csb := StyleBoxFlat.new()
		csb.set_border_width_all(1)
		csb.border_width_bottom = 3
		csb.set_corner_radius_all(10)
		csb.content_margin_left = 8
		csb.content_margin_right = 8
		csb.content_margin_top = 2
		csb.content_margin_bottom = 2
		if locked:
			_lock_label.text = _t("已鎖定")
			csb.bg_color = COLOR_GOLD
			csb.border_color = COLOR_BORDER
			_apply_label_style(_lock_label, 14, COLOR_TEXT_DARK)
		else:
			_lock_label.text = _t("未鎖定")
			csb.bg_color = Color("#7A7090")
			csb.border_color = Color("#5C5470")
			_apply_label_style(_lock_label, 14, Color.WHITE)
		_lock_capsule.add_theme_stylebox_override("panel", csb)

	if _lock_btn:
		_lock_btn.visible = true
		if locked:
			_lock_btn.text = _t("解鎖")
			_lock_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18))
			_lock_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFE066"), COLOR_BORDER, 5, 18))
			_lock_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_GOLD, COLOR_BORDER, 2, 18))
		else:
			_lock_btn.text = _t("鎖定")
			_lock_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 5, 18))
			_lock_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FFFDF0"), COLOR_BORDER, 5, 18))
			_lock_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 18))


func _update_lock_ui_texts() -> void:
	if _selected.is_empty() or not _is_selected_item_equipment():
		if _lock_capsule:
			_lock_capsule.visible = false
		if _lock_btn:
			_lock_btn.visible = false
		return
	var uid := _get_selected_equip_uid()
	var locked := is_item_locked(uid)
	_update_lock_ui(locked)


func _is_selected_item_equipment() -> bool:
	if _selected.is_empty():
		return false
	var inst := _get_selected_equip_inst()
	if not inst.is_empty():
		return true
	var loop := Engine.get_main_loop()
	var inv: Node = null
	if loop is SceneTree and (loop as SceneTree).root != null:
		inv = (loop as SceneTree).root.get_node_or_null("InventorySystem")
	var def: Dictionary = inv.call("catalog", _selected) as Dictionary if inv else {}
	var item_dict := {"id": _selected, "def": def}
	var kind := str(def.get("kind", "")).to_lower()
	var slot := str(def.get("slot", "")).to_lower()
	return item_matches_category(item_dict, "equip") or kind in ["weapon", "equipment", "equip", "armor", "accessory", "shield"] or slot in ["weapon", "armor"]


func _get_selected_equip_inst() -> Dictionary:
	if _selected.is_empty():
		return {}
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return {}
	var root_node := (loop as SceneTree).root
	var eq_sys: Node = root_node.get_node_or_null("EquipmentSystem")
	if eq_sys:
		if eq_sys.has_method("find_bag"):
			var inst: Dictionary = eq_sys.call("find_bag", _selected) as Dictionary
			if not inst.is_empty():
				return inst
		if eq_sys.has_method("find_any"):
			var inst2: Dictionary = eq_sys.call("find_any", _selected) as Dictionary
			if not inst2.is_empty():
				return inst2
	var gs: Node = root_node.get_node_or_null("GameState")
	if gs and "equip_bag" in gs and gs.equip_bag is Array:
		for e in gs.equip_bag:
			if e is Dictionary:
				if str(e.get("uid", "")) == _selected or str(e.get("base_id", "")) == _selected or str(e.get("id", "")) == _selected:
					return e
	if gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
		if gs.equip_worn.has(_selected) and gs.equip_worn[_selected] is Dictionary:
			return gs.equip_worn[_selected]
		for k in gs.equip_worn.keys():
			var w = gs.equip_worn[k]
			if w is Dictionary:
				if str(w.get("uid", "")) == _selected or str(w.get("base_id", "")) == _selected or str(w.get("id", "")) == _selected:
					return w
	return {}


func _get_selected_equip_uid() -> String:
	var inst := _get_selected_equip_inst()
	if not inst.is_empty():
		return str(inst.get("uid", _selected))
	return _selected


func is_item_locked(uid: String = "") -> bool:
	if uid.is_empty():
		uid = _get_selected_equip_uid()
	if uid.is_empty():
		return false
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var eq_sys: Node = (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
		if eq_sys and eq_sys.has_method("is_locked"):
			return bool(eq_sys.call("is_locked", uid))
		elif eq_sys and eq_sys.has_method("is_equip_locked"):
			return bool(eq_sys.call("is_equip_locked", uid))
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_method("has_flag") and gs.call("has_flag", "equip_locked." + uid):
			return bool(gs.call("get_flag", "equip_locked." + uid))
	var inst := _get_selected_equip_inst()
	if not inst.is_empty():
		return bool(inst.get("locked", false)) or bool(inst.get("is_locked", false))
	return false


func _on_lock_button_pressed() -> void:
	if _selected.is_empty():
		return
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return
	var eq_sys: Node = (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	var uid := _get_selected_equip_uid()
	if uid.is_empty():
		return

	var new_locked := false
	if eq_sys and eq_sys.has_method("toggle_lock"):
		eq_sys.call("toggle_lock", uid)
		new_locked = is_item_locked(uid)
	elif eq_sys and eq_sys.has_method("set_locked"):
		var cur := is_item_locked(uid)
		new_locked = not cur
		eq_sys.call("set_locked", uid, new_locked)
	else:
		var cur2 := is_item_locked(uid)
		new_locked = not cur2
		var inst := _get_selected_equip_inst()
		if not inst.is_empty():
			inst["locked"] = new_locked
		var gs: Node = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs and gs.has_method("set_flag"):
			gs.call("set_flag", "equip_locked." + uid, new_locked)

	var am: Node = (loop as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")

	equipment_lock_toggled.emit(uid, new_locked)

	var inv: Node = (loop as SceneTree).root.get_node_or_null("InventorySystem")
	_update_detail(inv)


func _show_tip(msg: String) -> void:
	if _tip and is_instance_valid(_tip):
		_tip.text = msg


func get_lock_button() -> Button:
	return _lock_btn


func get_lock_capsule() -> PanelContainer:
	return _lock_capsule


func get_lock_label() -> Label:
	return _lock_label


func get_bag_lock_button() -> Button:
	return _lock_btn


func get_bag_lock_capsule() -> PanelContainer:
	return _lock_capsule


func get_bag_lock_label() -> Label:
	return _lock_label


func _update_dismantle_button() -> void:
	if _dismantle_btn == null or not is_instance_valid(_dismantle_btn):
		return
	if not _is_selected_item_equipment():
		_dismantle_btn.visible = false
		if _hb_btn and is_instance_valid(_hb_btn):
			_hb_btn.visible = true
			_hb_btn.disabled = (_selected == "")
		return

	# 是裝備類物品：隱藏快捷欄按鈕，顯示拆解回收按鈕
	_dismantle_btn.visible = true
	if _hb_btn and is_instance_valid(_hb_btn):
		_hb_btn.visible = false

	var uid := _get_selected_equip_uid()
	var locked := is_item_locked(uid)
	var worn := is_selected_item_equipped()

	if locked:
		_dismantle_btn.disabled = true
		_dismantle_btn.text = _t("已鎖定無法拆解")
		_dismantle_btn.tooltip_text = _t("已鎖定無法拆解")
		_dismantle_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
		_dismantle_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	elif worn:
		_dismantle_btn.disabled = true
		_dismantle_btn.text = _t("已穿戴無法拆解")
		_dismantle_btn.tooltip_text = _t("已穿戴無法拆解")
		_dismantle_btn.add_theme_stylebox_override("disabled", _create_button_style(Color("#E8E4EC"), Color("#9E96AF"), 3, 18))
		_dismantle_btn.add_theme_color_override("font_disabled_color", Color("#7A7090"))
	else:
		_dismantle_btn.disabled = false
		_dismantle_btn.text = _t("拆解回收")
		_dismantle_btn.tooltip_text = _t("拆解裝備回收鐵屑與金幣")
		_dismantle_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_PINK, COLOR_BORDER, 5, 18))
		_dismantle_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#FF7B9E"), COLOR_BORDER, 5, 18))
		_dismantle_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_PINK, COLOR_BORDER, 2, 18))
		_dismantle_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
		_dismantle_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
		_dismantle_btn.add_theme_constant_override("outline_size", 3)


func dismantle_selected() -> Dictionary:
	if _selected.is_empty():
		return {"ok": false, "msg": _t("未選取裝備。")}
	if not _is_selected_item_equipment():
		return {"ok": false, "msg": _t("非裝備類物品無法拆解。")}

	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return {"ok": false, "msg": _t("場景樹無效。")}
	var root_node := (loop as SceneTree).root
	var eq_sys: Node = root_node.get_node_or_null("EquipmentSystem")
	if eq_sys == null:
		return {"ok": false, "msg": _t("缺少裝備系統。")}

	var uid := _get_selected_equip_uid()
	if is_item_locked(uid):
		var msg_lock := _t("裝備已鎖定，無法拆解。")
		_show_tip(msg_lock)
		return {"ok": false, "msg": msg_lock}
	if is_selected_item_equipped():
		var msg_worn := _t("裝備中無法拆解，請先卸下。")
		_show_tip(msg_worn)
		return {"ok": false, "msg": msg_worn}

	var res: Dictionary = eq_sys.call("dismantle", uid) if eq_sys.has_method("dismantle") else {}
	if bool(res.get("ok", false)):
		var am: Node = root_node.get_node_or_null("AudioManager")
		if am and am.has_method("play_ui"):
			am.call("play_ui")

		var toast_msg := str(res.get("msg", ""))
		if toast_msg.is_empty():
			var item_name: String = str(res.get("name", uid))
			var scrap_n: int = int(res.get("iron_scrap", 0))
			var gold_n: int = int(res.get("gold", 0))
			var refunded_gem: Dictionary = res.get("refunded_gem", {})
			if not refunded_gem.is_empty():
				var gem_sys: Node = root_node.get_node_or_null("GemSystem")
				var g_name := str(gem_sys.call("gem_label", refunded_gem)) if gem_sys and gem_sys.has_method("gem_label") else _t("寶石")
				toast_msg = _t("拆解【%s】：獲得鐵屑 ×%d、金幣 +%d、返還寶石【%s】") % [item_name, scrap_n, gold_n, g_name]
			else:
				toast_msg = _t("拆解【%s】：獲得鐵屑 ×%d、金幣 +%d") % [item_name, scrap_n, gold_n]

		_show_tip(toast_msg)
		var ml: Node = root_node.get_node_or_null("MobileLobby")
		if ml:
			if ml.has_method("_show_toast"):
				ml.call("_show_toast", toast_msg)
			elif ml.has_method("show_toast"):
				ml.call("show_toast", toast_msg)
			if ml.has_method("refresh_hud"):
				ml.call("refresh_hud")

		equipment_changed.emit()
		equipment_dismantled.emit(uid, res)
		refresh()
	else:
		var err_msg := str(res.get("msg", _t("無法拆解此物品。")))
		_show_tip(err_msg)

	return res


func _on_dismantle_button_pressed() -> void:
	dismantle_selected()


func get_dismantle_button() -> Button:
	return _dismantle_btn


func get_bag_dismantle_button() -> Button:
	return _dismantle_btn


func _is_selected_item_gem_or_material() -> bool:
	if _selected.is_empty():
		return false
	if _is_selected_item_equipment():
		return false
	var loop := Engine.get_main_loop()
	var inv: Node = null
	if loop is SceneTree and (loop as SceneTree).root != null:
		inv = (loop as SceneTree).root.get_node_or_null("InventorySystem")
	var def: Dictionary = inv.call("catalog", _selected) as Dictionary if inv else {}
	var item_dict := {"id": _selected, "def": def}
	var kind := str(def.get("kind", "")).to_lower()
	var id := _selected.to_lower()
	if item_matches_category(item_dict, "gem") or item_matches_category(item_dict, "material"):
		return true
	if kind in ["gem", "jewel", "stone", "material", "mat", "ore", "craft"]:
		return true
	if id.contains("gem") or id.contains("dust") or id.begins_with("mat_") or id.contains("scrap") or id.contains("ore"):
		return true
	return false


func _update_shortcut_buttons() -> void:
	if _go_forge_btn == null or not is_instance_valid(_go_forge_btn):
		return
	if _go_workshop_btn == null or not is_instance_valid(_go_workshop_btn):
		return

	if _selected.is_empty():
		_go_forge_btn.visible = false
		_go_workshop_btn.visible = false
		return

	if _is_selected_item_equipment():
		_go_forge_btn.visible = true
		_go_forge_btn.text = _t("前往鍛造")
		_go_workshop_btn.visible = false
	elif _is_selected_item_gem_or_material():
		_go_forge_btn.visible = false
		_go_workshop_btn.visible = true
		_go_workshop_btn.text = _t("前往工坊")
	else:
		_go_forge_btn.visible = false
		_go_workshop_btn.visible = false


func _on_go_forge_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	var target_item := _selected
	forge_requested.emit()
	open_forge(target_item)


func _on_go_workshop_pressed() -> void:
	var am: Node = null
	if Engine.get_main_loop() is SceneTree:
		am = (Engine.get_main_loop() as SceneTree).root.get_node_or_null("AudioManager")
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	var target_item := _selected
	workshop_requested.emit()
	var target_tab := 0
	if _is_selected_item_equipment():
		target_tab = 1
	open_gem_workshop(target_tab)


func open_forge(target_weapon: Variant = null) -> Control:
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		close()
		return null
	var root_node := (loop as SceneTree).root
	var ml: Node = root_node.get_node_or_null("MobileLobby")
	if ml and ml.has_method("open_forge"):
		close()
		return ml.call("open_forge", target_weapon) as Control
	var p := get_parent()
	if p and p.has_method("open_forge"):
		close()
		return p.call("open_forge", target_weapon) as Control

	var ForgeClass: GDScript = load("res://scripts/ui/forge_dialog.gd")
	if ForgeClass:
		var dlg: Control = ForgeClass.new() as Control
		dlg.name = "ForgeDialog"
		dlg.z_index = z_index + 10
		if p != null:
			p.add_child(dlg)
		else:
			root_node.add_child(dlg)
		if target_weapon != null and dlg.has_method("select_target_equipment"):
			dlg.call("select_target_equipment", target_weapon)
		close()
		return dlg
	close()
	return null


func open_gem_workshop(target_tab: int = 0) -> Control:
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		close()
		return null
	var root_node := (loop as SceneTree).root
	var ml: Node = root_node.get_node_or_null("MobileLobby")
	if ml and ml.has_method("open_gem_workshop"):
		close()
		return ml.call("open_gem_workshop", target_tab) as Control
	var p := get_parent()
	if p and p.has_method("open_gem_workshop"):
		close()
		return p.call("open_gem_workshop", target_tab) as Control

	var GemClass: GDScript = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemClass:
		var dlg: Control = GemClass.new() as Control
		dlg.name = "GemWorkshopDialog"
		dlg.z_index = z_index + 10
		if p != null:
			p.add_child(dlg)
		else:
			root_node.add_child(dlg)
		if target_tab != 0 and dlg.has_method("set_tab"):
			dlg.call("set_tab", target_tab)
		close()
		return dlg
	close()
	return null


func get_go_forge_button() -> Button:
	return _go_forge_btn


func get_bag_go_forge_button() -> Button:
	return _go_forge_btn


func get_go_workshop_button() -> Button:
	return _go_workshop_btn


func get_bag_go_workshop_button() -> Button:
	return _go_workshop_btn

