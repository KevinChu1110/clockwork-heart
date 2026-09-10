class_name WardrobeDialog
extends Control
## 《發條之心》大廳角色換裝衣櫥彈窗 (WardrobeDialog)
## 依據手遊人體工學規範與 review.md 第 28 條、第 28a 條：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景附全螢幕遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，點擊遮罩空白處亦可關閉。
## 3. 部件挑選採 GridContainer 每列 4 格縮圖卡片網格，一次呈現全部已解鎖選項。
##    每格顯示部件縮圖＋名稱，已裝備格附亮金框與『✓ 已選用』標籤；多於一頁採 ScrollContainer 捲動。
##    嚴禁垂直長條文字按鈕，嚴禁左右箭頭分頁輪播。
## 4. creation_mode 預設為 false，作為大廳隨時開合的正式衣櫥。
## 5. 打開時自動對應玩家當前種族與已裝備的部件 index，不從 0 開始重置。
## 6. 確認換裝寫回 GameState (costume_id, paint_id) 並自動存檔。

signal outfit_saved(race_id: String, selections: Dictionary)
signal cancelled()

@export var creation_mode: bool = false

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 彈窗尺寸標準 (review.md 第 28 條: 740~760px)
const DIALOG_WIDTH := 750.0
const DIALOG_HEIGHT := 530.0
const BTN_SIZE := 50.0

## 色盤常數 (希臘神殿黑曜石 x 多巴胺古典金)
const OBSIDIAN_BASE   := Color(0.043, 0.039, 0.055, 1.0)
const OBSIDIAN_CARD   := Color(0.078, 0.071, 0.094, 0.98)
const OBSIDIAN_WARM   := Color(0.102, 0.090, 0.122, 1.0)
const OBSIDIAN_DEEP   := Color(0.027, 0.024, 0.039, 1.0)
const GOLD_CLASSICAL  := Color(0.831, 0.686, 0.216, 1.0)
const GOLD_HOVER      := Color(0.941, 0.843, 0.549, 1.0)
const INK_IVORY       := Color(0.957, 0.922, 0.831, 1.0)
const INK_MUTED       := Color(0.65, 0.60, 0.52, 1.0)
const LINE_GOLD       := Color(0.831, 0.686, 0.216, 0.5)
const LINE_GOLD_SOFT  := Color(0.831, 0.686, 0.216, 0.25)
const BTN_CONFIRM_BG  := Color(0.22, 0.68, 0.38, 1.0)
const BTN_CONFIRM_TXT := Color(0.04, 0.20, 0.08, 1.0)

## UI 節點參照
var _scrim: ColorRect
var _dialog_card: PanelContainer
var _title_label: Label
var _subtitle_label: Label
var _close_btn: Button

var _preview_rect: TextureRect
var _badge_name_label: Label
var _badge_race_label: Label

var _costume_grid: GridContainer
var _chassis_grid: GridContainer
var _costume_cards: Array[Button] = []
var _chassis_cards: Array[Button] = []

var _btn_confirm: Button
var _btn_reset: Button

## 執行期狀態
var current_race: String = "rabbit"
var costume_index: int = 0
var chassis_index: int = 0

var _cached_font: Font = null
var _ui_built: bool = false


func _init() -> void:
	name = "WardrobeDialog"
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	ensure_ui()
	_init_from_game_state()
	_rebuild_cards()
	_update_ui_texts()
	_update_preview()


func _ready() -> void:
	ensure_ui()
	_init_from_game_state()
	_rebuild_cards()
	_update_ui_texts()
	_update_preview()


func ensure_ui() -> void:
	if _ui_built:
		return
	_ui_built = true
	if ResourceLoader.exists(FONT_PATH):
		_cached_font = load(FONT_PATH) as Font
	_build_ui()


func _get_game_state() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null


func _get_save_manager() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("SaveManager")
	return null


func _get_race_data() -> Dictionary:
	var PaperdollSelectClass = load("res://scripts/ui/paperdoll_select_demo.gd")
	if PaperdollSelectClass and "RACES_DATA" in PaperdollSelectClass:
		var all_data: Dictionary = PaperdollSelectClass.RACES_DATA
		if all_data.has(current_race):
			return all_data[current_race]
	return {}


func _init_from_game_state() -> void:
	var gs = _get_game_state()
	if gs and "player_race" in gs:
		var r: String = str(gs.player_race).strip_edges().to_lower()
		if not r.is_empty():
			current_race = r

	var data := _get_race_data()
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	var equipped_costume: String = ""
	var equipped_paint: String = ""
	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		equipped_costume = str(gs.paperdoll_slots.get("costume_id", gs.paperdoll_slots.get("costume", "")))
		equipped_paint = str(gs.paperdoll_slots.get("paint_id", gs.paperdoll_slots.get("chassis", "")))

	# 正確對應當前已裝備部件，不從 index 0 開始強制重置
	costume_index = 0
	if not equipped_costume.is_empty() and not costumes.is_empty():
		for i in range(costumes.size()):
			if str(costumes[i].get("id", "")) == equipped_costume:
				costume_index = i
				break

	chassis_index = 0
	if not equipped_paint.is_empty() and not chassis_list.is_empty():
		for i in range(chassis_list.size()):
			if str(chassis_list[i].get("id", "")) == equipped_paint:
				chassis_index = i
				break


func _build_ui() -> void:
	# 1. 全螢幕遮罩 (Scrim)
	_scrim = ResponsiveUi.make_scrim(Color(0.02, 0.02, 0.03, 0.75))
	_scrim.gui_input.connect(func(event: InputEvent):
		if event is InputEventMouseButton and event.pressed:
			close()
	)
	add_child(_scrim)

	# 2. 彈窗主體容器 Card (740~760px 橫屏彈窗標準)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "DialogCard"
	_dialog_card.custom_minimum_size = Vector2(DIALOG_WIDTH, DIALOG_HEIGHT)
	_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
	_dialog_card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_dialog_card.grow_vertical = Control.GROW_DIRECTION_BOTH

	var card_sb := StyleBoxFlat.new()
	card_sb.bg_color = OBSIDIAN_CARD
	card_sb.border_color = GOLD_CLASSICAL
	card_sb.set_border_width_all(2)
	card_sb.border_width_bottom = 5
	card_sb.set_corner_radius_all(18)
	card_sb.shadow_color = Color(0, 0, 0, 0.6)
	card_sb.shadow_size = 20
	card_sb.shadow_offset = Vector2(0, 8)
	_dialog_card.add_theme_stylebox_override("panel", card_sb)
	add_child(_dialog_card)

	var card_margin := MarginContainer.new()
	card_margin.add_theme_constant_override("margin_left", 20)
	card_margin.add_theme_constant_override("margin_top", 16)
	card_margin.add_theme_constant_override("margin_right", 20)
	card_margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(card_margin)

	var root_vbox := VBoxContainer.new()
	root_vbox.add_theme_constant_override("separation", 12)
	card_margin.add_child(root_vbox)

	# ── 頂部標題列 ──
	var top_bar := HBoxContainer.new()
	top_bar.custom_minimum_size.y = 50
	root_vbox.add_child(top_bar)

	var title_vbox := VBoxContainer.new()
	title_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_bar.add_child(title_vbox)

	_title_label = Label.new()
	_title_label.text = "發條衣櫥 · 英雄換裝"
	_title_label.add_theme_font_size_override("font_size", 20)
	_title_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		_title_label.add_theme_font_override("font", _cached_font)
	title_vbox.add_child(_title_label)

	_subtitle_label = Label.new()
	_subtitle_label.text = "個人化外觀部件即時切換 · 零數值純視覺展示 (手遊人體工學標準)"
	_subtitle_label.add_theme_font_size_override("font_size", 12)
	_subtitle_label.add_theme_color_override("font_color", INK_MUTED)
	if _cached_font:
		_subtitle_label.add_theme_font_override("font", _cached_font)
	title_vbox.add_child(_subtitle_label)

	# 右上角「✕」關閉按鈕，尺寸 >= 50px
	_close_btn = ResponsiveUi.make_close_button(Callable(self, "close"))
	top_bar.add_child(_close_btn)

	# ── 中間主內容區 (左側展台 + 右側卡片網格挑選) ──
	var main_hbox := HBoxContainer.new()
	main_hbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_hbox.add_theme_constant_override("separation", 16)
	root_vbox.add_child(main_hbox)

	# 左側角色展示展台
	var stage_panel := PanelContainer.new()
	stage_panel.custom_minimum_size = Vector2(250, 360)
	var stage_sb := StyleBoxFlat.new()
	stage_sb.bg_color = OBSIDIAN_DEEP
	stage_sb.border_color = LINE_GOLD
	stage_sb.set_border_width_all(1)
	stage_sb.border_width_bottom = 3
	stage_sb.set_corner_radius_all(14)
	stage_panel.add_theme_stylebox_override("panel", stage_sb)
	main_hbox.add_child(stage_panel)

	var stage_vbox := VBoxContainer.new()
	stage_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	stage_vbox.add_theme_constant_override("separation", 8)
	stage_panel.add_child(stage_vbox)

	_preview_rect = TextureRect.new()
	_preview_rect.custom_minimum_size = Vector2(210, 210)
	_preview_rect.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_preview_rect.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	_preview_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_preview_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	stage_vbox.add_child(_preview_rect)

	var badge_box := VBoxContainer.new()
	badge_box.alignment = BoxContainer.ALIGNMENT_CENTER
	badge_box.add_theme_constant_override("separation", 2)
	stage_vbox.add_child(badge_box)

	_badge_name_label = Label.new()
	_badge_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_name_label.add_theme_font_size_override("font_size", 16)
	_badge_name_label.add_theme_color_override("font_color", INK_IVORY)
	if _cached_font:
		_badge_name_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_name_label)

	_badge_race_label = Label.new()
	_badge_race_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_race_label.add_theme_font_size_override("font_size", 12)
	_badge_race_label.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		_badge_race_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_race_label)

	# 右側部件挑選區 (卡片網格)
	var controls_vbox := VBoxContainer.new()
	controls_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	controls_vbox.add_theme_constant_override("separation", 10)
	main_hbox.add_child(controls_vbox)

	# ── 槽位 1：外裝服飾 (Costume) 卡片網格 ──
	var costume_box := _create_grid_section("外裝服飾 (Costume)", "costume")
	controls_vbox.add_child(costume_box)

	# ── 槽位 2：機體塗裝 (Paint / Chassis) 卡片網格 ──
	var chassis_box := _create_grid_section("機體塗裝 (Chassis / Paint)", "chassis")
	controls_vbox.add_child(chassis_box)

	# ── 底部操作按鈕列 ──
	var actions_hbox := HBoxContainer.new()
	actions_hbox.custom_minimum_size.y = BTN_SIZE
	actions_hbox.add_theme_constant_override("separation", 12)
	controls_vbox.add_child(actions_hbox)

	_btn_reset = Button.new()
	_btn_reset.name = "BtnReset"
	_btn_reset.text = "還原預設"
	_btn_reset.custom_minimum_size = Vector2(110, BTN_SIZE)
	_btn_reset.add_theme_font_size_override("font_size", 15)
	if _cached_font:
		_btn_reset.add_theme_font_override("font", _cached_font)
	var rsb := StyleBoxFlat.new()
	rsb.bg_color = OBSIDIAN_WARM
	rsb.border_color = LINE_GOLD
	rsb.set_border_width_all(1)
	rsb.border_width_bottom = 3
	rsb.set_corner_radius_all(12)
	_btn_reset.add_theme_stylebox_override("normal", rsb)
	_btn_reset.add_theme_color_override("font_color", INK_IVORY)
	_btn_reset.pressed.connect(_on_reset_pressed)
	actions_hbox.add_child(_btn_reset)

	_btn_confirm = Button.new()
	_btn_confirm.name = "BtnConfirm"
	_btn_confirm.text = "確認換裝 · 套用新外觀"
	_btn_confirm.custom_minimum_size = Vector2(0, BTN_SIZE)
	_btn_confirm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_confirm.add_theme_font_size_override("font_size", 16)
	if _cached_font:
		_btn_confirm.add_theme_font_override("font", _cached_font)
	var csb := StyleBoxFlat.new()
	csb.bg_color = BTN_CONFIRM_BG
	csb.border_color = GOLD_CLASSICAL
	csb.set_border_width_all(2)
	csb.border_width_bottom = 5
	csb.set_corner_radius_all(12)
	_btn_confirm.add_theme_stylebox_override("normal", csb)
	var csb_h := csb.duplicate()
	csb_h.bg_color = Color(0.28, 0.78, 0.44, 1.0)
	_btn_confirm.add_theme_stylebox_override("hover", csb_h)
	_btn_confirm.add_theme_stylebox_override("pressed", csb_h)
	_btn_confirm.add_theme_color_override("font_color", BTN_CONFIRM_TXT)
	_btn_confirm.pressed.connect(confirm_selection)
	actions_hbox.add_child(_btn_confirm)


## 建立卡片網格區塊 (第 28a 條：卡片網格＋亮金框『✓ 已選用』，多於一頁採 ScrollContainer)
func _create_grid_section(section_title: String, slot_type: String) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var sb := StyleBoxFlat.new()
	sb.bg_color = OBSIDIAN_WARM
	sb.border_color = LINE_GOLD_SOFT
	sb.set_border_width_all(1)
	sb.border_width_bottom = 3
	sb.set_corner_radius_all(12)
	panel.add_theme_stylebox_override("panel", sb)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 12)
	margin.add_theme_constant_override("margin_top", 8)
	margin.add_theme_constant_override("margin_right", 12)
	margin.add_theme_constant_override("margin_bottom", 8)
	panel.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	margin.add_child(vbox)

	# 標題列
	var header_hbox := HBoxContainer.new()
	vbox.add_child(header_hbox)

	var title_lbl := Label.new()
	title_lbl.text = section_title
	title_lbl.add_theme_font_size_override("font_size", 13)
	title_lbl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(title_lbl)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_hbox.add_child(spacer)

	var tip_lbl := Label.new()
	tip_lbl.text = "點擊卡片即時預覽"
	tip_lbl.add_theme_font_size_override("font_size", 11)
	tip_lbl.add_theme_color_override("font_color", INK_MUTED)
	if _cached_font:
		tip_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(tip_lbl)

	# 捲動容器包覆 GridContainer (每列 4 格)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.y = 96
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	vbox.add_child(scroll)

	var grid := GridContainer.new()
	grid.name = "GridCostume" if slot_type == "costume" else "GridChassis"
	grid.columns = 4
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	scroll.add_child(grid)

	if slot_type == "costume":
		_costume_grid = grid
	else:
		_chassis_grid = grid

	return panel


## 重新建置全部卡片
func _rebuild_cards() -> void:
	if _costume_grid == null or _chassis_grid == null:
		return

	# 清空舊卡片
	for c in _costume_grid.get_children():
		c.queue_free()
	for c in _chassis_grid.get_children():
		c.queue_free()
	_costume_cards.clear()
	_chassis_cards.clear()

	var data := _get_race_data()
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	for i in range(costumes.size()):
		var card := _create_item_card("costume", i, costumes[i])
		_costume_grid.add_child(card)
		_costume_cards.append(card)

	for i in range(chassis_list.size()):
		var card := _create_item_card("chassis", i, chassis_list[i])
		_chassis_grid.add_child(card)
		_chassis_cards.append(card)

	_update_card_selection_states()


## 建立單張縮圖卡片按鈕
func _create_item_card(slot_type: String, idx: int, item_data: Dictionary) -> Button:
	var btn := Button.new()
	btn.name = "Card_%s_%d" % [slot_type, idx]
	btn.custom_minimum_size = Vector2(92, 108)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND

	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 4)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_right", 4)
	margin.add_theme_constant_override("margin_bottom", 4)
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	btn.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 2)
	vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_child(vbox)

	# 部件縮圖
	var thumb := TextureRect.new()
	thumb.custom_minimum_size = Vector2(38, 38)
	thumb.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	thumb.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	thumb.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	thumb.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	thumb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	thumb.texture = _get_item_thumbnail(slot_type, str(item_data.get("id", "")))
	vbox.add_child(thumb)

	# 部件名稱
	var name_lbl := Label.new()
	name_lbl.text = str(item_data.get("name_zh", ""))
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 11)
	name_lbl.add_theme_color_override("font_color", INK_IVORY)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	# 商品名一律完整顯示，⛔ 不截斷成「…」（收費點面板玩家要看得到全名）
	name_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
	name_lbl.custom_minimum_size.y = 28
	name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(name_lbl)

	# 選取狀態標籤 (『✓ 已選用』)
	var badge_lbl := Label.new()
	badge_lbl.name = "BadgeLabel"
	badge_lbl.text = ""
	badge_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	badge_lbl.add_theme_font_size_override("font_size", 10)
	badge_lbl.add_theme_color_override("font_color", GOLD_CLASSICAL)
	if _cached_font:
		badge_lbl.add_theme_font_override("font", _cached_font)
	badge_lbl.custom_minimum_size.y = 14
	badge_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(badge_lbl)

	# 點擊即時套用預覽與選取狀態
	btn.pressed.connect(func():
		if slot_type == "costume":
			costume_index = idx
		else:
			chassis_index = idx
		_update_card_selection_states()
		_update_preview()
		_update_ui_texts()
	)

	return btn


## 取得部件對應之縮圖貼圖
func _get_item_thumbnail(slot_type: String, item_id: String) -> Texture2D:
	if slot_type == "costume":
		if item_id == "none":
			var bare_path := "res://assets/sprites/player/paperdoll/%s/composite_preview_bare.png" % current_race
			if ResourceLoader.exists(bare_path):
				return load(bare_path) as Texture2D
			var stock_chassis := "res://assets/sprites/player/paperdoll/%s/chassis/paint_ivory_stock.png" % current_race
			if ResourceLoader.exists(stock_chassis):
				return load(stock_chassis) as Texture2D
		else:
			var path := "res://assets/sprites/player/paperdoll/%s/costume/%s.png" % [current_race, item_id]
			if ResourceLoader.exists(path):
				return load(path) as Texture2D
	elif slot_type == "chassis":
		var path := "res://assets/sprites/player/paperdoll/%s/chassis/%s.png" % [current_race, item_id]
		if ResourceLoader.exists(path):
			return load(path) as Texture2D
	return null


## 更新所有卡片的亮金邊框與『✓ 已選用』狀態
func _update_card_selection_states() -> void:
	for i in range(_costume_cards.size()):
		var is_selected := (i == costume_index)
		_apply_card_style(_costume_cards[i], is_selected)

	for i in range(_chassis_cards.size()):
		var is_selected := (i == chassis_index)
		_apply_card_style(_chassis_cards[i], is_selected)


## 套用單張卡片之視覺樣式 (選中時亮金框 + 『✓ 已選用』)
func _apply_card_style(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(10)
	if is_selected:
		sb.bg_color = Color(0.14, 0.12, 0.08, 0.98) # 溫潤金褐底
		sb.border_color = GOLD_CLASSICAL           # 亮金邊框
		sb.set_border_width_all(2)
		sb.border_width_bottom = 3
	else:
		sb.bg_color = OBSIDIAN_DEEP                 # 深黑曜底
		sb.border_color = LINE_GOLD_SOFT            # 柔和淡金框
		sb.set_border_width_all(1)
	btn.add_theme_stylebox_override("normal", sb)

	var sb_h := sb.duplicate()
	if is_selected:
		sb_h.border_color = GOLD_HOVER
	else:
		sb_h.bg_color = OBSIDIAN_WARM
		sb_h.border_color = GOLD_HOVER
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_h)

	var badge = btn.find_child("BadgeLabel", true, false)
	if badge is Label:
		badge.text = "✓ 已選用" if is_selected else ""


func _on_reset_pressed() -> void:
	costume_index = 0
	chassis_index = 0
	_update_card_selection_states()
	_update_ui_texts()
	_update_preview()


func get_current_selections() -> Dictionary:
	var data := _get_race_data()
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	var cur_costume: Dictionary = costumes[costume_index] if costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[chassis_index] if chassis_index < chassis_list.size() else {}

	var c_id := str(cur_costume.get("id", "none"))
	var p_id := str(cur_chassis.get("id", "paint_ivory_stock"))

	return {
		"race": current_race,
		"costume": c_id,
		"chassis": p_id,
		"costume_id": c_id,
		"paint_id": p_id
	}


func _update_ui_texts() -> void:
	var data := _get_race_data()
	var race_name_zh := str(data.get("name_zh", current_race))
	var archetype := str(data.get("archetype", ""))

	var gs = _get_game_state()
	var p_name := "小白"
	if gs and "player_name" in gs:
		p_name = str(gs.player_name)

	if _badge_name_label:
		_badge_name_label.text = "%s" % p_name
	if _badge_race_label:
		_badge_race_label.text = "【%s · %s】" % [race_name_zh, archetype]


func _update_preview() -> void:
	if _preview_rect == null:
		return
	var sel := get_current_selections()
	var img := PaperdollRenderer.build_composite_image(current_race, sel)
	if img != null and not img.is_empty():
		# 高解析度超取樣 (256x256 LANCZOS)：對齊 UI 顯示密度，徹底消除 128x128 放大模糊與鋸齒
		var hires := img.duplicate()
		hires.resize(256, 256, Image.INTERPOLATE_LANCZOS)
		_preview_rect.texture = ImageTexture.create_from_image(hires)
	else:
		var tex := PaperdollRenderer.get_race_composite_texture(current_race, sel)
		if tex != null:
			_preview_rect.texture = tex


## 確認換裝並寫入 GameState 與存檔
func confirm_selection() -> void:
	var sel := get_current_selections()
	var gs = _get_game_state()
	if gs:
		if not (gs.paperdoll_slots is Dictionary):
			gs.paperdoll_slots = {}
		gs.paperdoll_slots["race"] = current_race
		gs.paperdoll_slots["costume"] = sel["costume"]
		gs.paperdoll_slots["chassis"] = sel["chassis"]
		gs.paperdoll_slots["costume_id"] = sel["costume_id"]
		gs.paperdoll_slots["paint_id"] = sel["paint_id"]

		# 自動觸發存檔保全
		var sm = _get_save_manager()
		if sm and sm.has_method("save_game"):
			sm.call("save_game")

	outfit_saved.emit(current_race, sel)
	close()


func close() -> void:
	cancelled.emit()
	queue_free()
