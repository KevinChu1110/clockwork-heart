class_name WardrobeDialog
extends Control
## 《發條之心》大廳角色換裝衣櫥彈窗 (WardrobeDialog)
## 依多巴胺亮色盤規範與手遊人體工學：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，點擊遮罩空白處亦可關閉。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底板奶油白 #FFFDF8。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)，按鈕高度均 >= 50px。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 部件挑選採 GridContainer 每列 4 格縮圖卡片網格，已裝備格附亮金/暖橘果凍框與『✓ 已選用』標籤。
## 7. 打開時自動對應玩家當前種族與已裝備的部件 index，確認換裝寫回 GameState 並存檔。
## 8. 全程 0 系統 emoji，角色待機呼吸動畫持續進行。

signal outfit_saved(race_id: String, selections: Dictionary)
signal cancelled()

@export var creation_mode: bool = false

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 彈窗尺寸標準 (review.md 第 28 條: 740~760px)
const DIALOG_WIDTH := 750.0
const DIALOG_HEIGHT := 580.0
const BTN_SIZE := 50.0

## ── 多巴胺鮮亮高飽和色盤 ──
const COLOR_GOLD       := Color("#FFD028")  ## 金黃
const COLOR_ORANGE     := Color("#FFA010")  ## 暖橘
const COLOR_MINT       := Color("#4ED86A")  ## 薄荷綠
const COLOR_SKY        := Color("#38A0FF")  ## 天藍
const COLOR_PINK       := Color("#FF5E8A")  ## 珊瑚粉
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_SKY   := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）

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
var _btn_random: Button

var _breathe_tween: Tween = null

## 種族篩選常數與狀態
const RACE_FILTER_OPTIONS: Array[Dictionary] = [
	{"id": "all", "name_zh": "全部"},
	{"id": "rabbit", "name_zh": "兔"},
	{"id": "fox", "name_zh": "狐"},
	{"id": "lion", "name_zh": "獅"},
	{"id": "boar", "name_zh": "野豬"},
	{"id": "macaque", "name_zh": "猴"},
	{"id": "tiger", "name_zh": "虎"},
	{"id": "bear", "name_zh": "熊"},
	{"id": "crane", "name_zh": "鶴"},
	{"id": "penguin", "name_zh": "企鵝"},
	{"id": "tortoise", "name_zh": "龜"},
	{"id": "elephant", "name_zh": "象"},
	{"id": "frog", "name_zh": "蛙"},
	{"id": "panda", "name_zh": "貓"},
	{"id": "fawn", "name_zh": "鹿"},
]

var current_filter_race: String = "all"
var _filter_chips: Dictionary = {}
var _displayed_costumes: Array[Dictionary] = []
var _displayed_chassis: Array[Dictionary] = []
var selected_costume_id: String = ""
var selected_chassis_id: String = ""

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
	_update_filter_chips_visual()
	_rebuild_cards()
	_update_ui_texts()
	_update_preview()


func _ready() -> void:
	ensure_ui()
	_init_from_game_state()
	_update_filter_chips_visual()
	_rebuild_cards()
	_update_ui_texts()
	_update_preview()
	_start_breathe_tween()


func _exit_tree() -> void:
	_stop_breathe_tween()


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


func _get_race_data(target_race: String = "") -> Dictionary:
	var r := target_race if not target_race.is_empty() else current_race
	var PaperdollSelectClass = load("res://scripts/ui/paperdoll_select_demo.gd")
	if PaperdollSelectClass and "RACES_DATA" in PaperdollSelectClass:
		var all_data: Dictionary = PaperdollSelectClass.RACES_DATA
		if all_data.has(r):
			return all_data[r]
	return {}


func _init_from_game_state() -> void:
	var gs = _get_game_state()
	if gs and "player_race" in gs:
		var r: String = str(gs.player_race).strip_edges().to_lower()
		if not r.is_empty():
			current_race = r

	current_filter_race = current_race

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
	selected_costume_id = ""
	if not equipped_costume.is_empty() and not costumes.is_empty():
		for i in range(costumes.size()):
			if str(costumes[i].get("id", "")) == equipped_costume:
				costume_index = i
				selected_costume_id = equipped_costume
				break
	elif not costumes.is_empty():
		selected_costume_id = str(costumes[0].get("id", ""))

	chassis_index = 0
	selected_chassis_id = ""
	if not equipped_paint.is_empty() and not chassis_list.is_empty():
		for i in range(chassis_list.size()):
			if str(chassis_list[i].get("id", "")) == equipped_paint:
				chassis_index = i
				selected_chassis_id = equipped_paint
				break
	elif not chassis_list.is_empty():
		selected_chassis_id = str(chassis_list[0].get("id", ""))


func _build_ui() -> void:
	# 1. 全螢幕柔和遮罩 (Scrim)
	_scrim = ResponsiveUi.make_scrim(Color(0.08, 0.06, 0.12, 0.65))
	_scrim.gui_input.connect(func(event: InputEvent):
		if event is InputEventMouseButton and event.pressed:
			close()
	)
	add_child(_scrim)

	# 2. 彈窗主體容器 Card (740~760px 橫屏彈窗標準)
	_dialog_card = PanelContainer.new()
	_dialog_card.name = "DialogCard"
	ResponsiveUi.apply_dialog_card(_dialog_card)
	_dialog_card.custom_minimum_size = Vector2(DIALOG_WIDTH, DIALOG_HEIGHT)
	_dialog_card.set_anchors_preset(Control.PRESET_CENTER)
	_dialog_card.grow_horizontal = Control.GROW_DIRECTION_BOTH
	_dialog_card.grow_vertical = Control.GROW_DIRECTION_BOTH
	_dialog_card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	add_child(_dialog_card)

	var card_margin := MarginContainer.new()
	card_margin.add_theme_constant_override("margin_left", 20)
	card_margin.add_theme_constant_override("margin_top", 16)
	card_margin.add_theme_constant_override("margin_right", 20)
	card_margin.add_theme_constant_override("margin_bottom", 16)
	_dialog_card.add_child(card_margin)

	var root_vbox := VBoxContainer.new()
	root_vbox.add_theme_constant_override("separation", 10)
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
	_title_label.add_theme_font_size_override("font_size", 22)
	_title_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_title_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_label.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_title_label.add_theme_font_override("font", _cached_font)
	title_vbox.add_child(_title_label)

	_subtitle_label = Label.new()
	_subtitle_label.text = "個人化外觀部件即時切換 · 零數值純視覺展示"
	_subtitle_label.add_theme_font_size_override("font_size", 16)
	_subtitle_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_subtitle_label.add_theme_font_override("font", _cached_font)
	title_vbox.add_child(_subtitle_label)

	# 右上角「✕」關閉按鈕，尺寸 >= 50px
	_close_btn = ResponsiveUi.make_close_button(Callable(self, "close"))
	top_bar.add_child(_close_btn)

	# 亮橘色分隔線
	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	root_vbox.add_child(sep)

	# ── 中間主內容區 (左側展台 + 右側卡片網格挑選) ──
	var main_hbox := HBoxContainer.new()
	main_hbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_hbox.add_theme_constant_override("separation", 16)
	root_vbox.add_child(main_hbox)

	# 左側角色展示展台 (溫暖米黃卡片底)
	var stage_panel := PanelContainer.new()
	stage_panel.custom_minimum_size = Vector2(250, 370)
	stage_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 20))
	main_hbox.add_child(stage_panel)

	var stage_vbox := VBoxContainer.new()
	stage_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	stage_vbox.add_theme_constant_override("separation", 8)
	stage_panel.add_child(stage_vbox)

	_preview_rect = TextureRect.new()
	_preview_rect.custom_minimum_size = Vector2(220, 280)
	_preview_rect.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_preview_rect.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_preview_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_preview_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_preview_rect.pivot_offset = Vector2(110, 250)
	stage_vbox.add_child(_preview_rect)

	var badge_box := VBoxContainer.new()
	badge_box.alignment = BoxContainer.ALIGNMENT_CENTER
	badge_box.add_theme_constant_override("separation", 4)
	stage_vbox.add_child(badge_box)

	_badge_name_label = Label.new()
	_badge_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_name_label.add_theme_font_size_override("font_size", 20)
	_badge_name_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_badge_name_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_name_label)

	_badge_race_label = Label.new()
	_badge_race_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_race_label.add_theme_font_size_override("font_size", 16)
	_badge_race_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_badge_race_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_badge_race_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_badge_race_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_race_label)

	# 右側部件挑選區 (卡片網格)
	var controls_vbox := VBoxContainer.new()
	controls_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	controls_vbox.add_theme_constant_override("separation", 8)
	main_hbox.add_child(controls_vbox)

	# ── 頂部種族篩選 Chip 列 (支援全部/兔/狐/獅/豬/猴/虎/熊/鶴/企鵝) ──
	var filter_bar := _create_race_filter_bar()
	controls_vbox.add_child(filter_bar)

	# ── 槽位 1：外裝服飾 (Costume) 卡片網格 ──
	var costume_box := _create_grid_section("外裝服飾 (Costume)", "costume")
	controls_vbox.add_child(costume_box)

	# ── 槽位 2：機體塗裝 (Paint / Chassis) 卡片網格 ──
	var chassis_box := _create_grid_section("機體塗裝 (Chassis / Paint)", "chassis")
	controls_vbox.add_child(chassis_box)

	# ── 底部操作按鈕列 ──
	var actions_hbox := HBoxContainer.new()
	actions_hbox.custom_minimum_size.y = BTN_SIZE
	actions_hbox.add_theme_constant_override("separation", 10)
	controls_vbox.add_child(actions_hbox)

	_btn_reset = Button.new()
	_btn_reset.name = "BtnReset"
	_btn_reset.text = "還原預設"
	_btn_reset.custom_minimum_size = Vector2(100, BTN_SIZE)
	_btn_reset.add_theme_font_size_override("font_size", 16)
	_btn_reset.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_btn_reset.add_theme_font_override("font", _cached_font)
	_btn_reset.add_theme_stylebox_override("normal", _create_button_style(COLOR_CARD_WARM, COLOR_BORDER, 5, 18, 2))
	var r_h := _create_button_style(Color("#FFFDF0"), COLOR_BORDER, 3, 18, 2)
	_btn_reset.add_theme_stylebox_override("hover", r_h)
	_btn_reset.add_theme_stylebox_override("pressed", r_h)
	_btn_reset.pressed.connect(_on_reset_pressed)
	actions_hbox.add_child(_btn_reset)

	_btn_random = Button.new()
	_btn_random.name = "BtnRandom"
	_btn_random.text = "隨機"
	_btn_random.custom_minimum_size = Vector2(80, BTN_SIZE)
	_btn_random.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	_btn_random.add_theme_font_size_override("font_size", 16)
	_btn_random.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_btn_random.add_theme_font_override("font", _cached_font)
	_btn_random.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18, 2))
	var rand_h := _create_button_style(Color("#62B6FF"), COLOR_BORDER, 3, 18, 2)
	_btn_random.add_theme_stylebox_override("hover", rand_h)
	_btn_random.add_theme_stylebox_override("pressed", rand_h)
	_btn_random.pressed.connect(_on_random_pressed)
	actions_hbox.add_child(_btn_random)

	_btn_confirm = Button.new()
	_btn_confirm.name = "BtnConfirm"
	_btn_confirm.text = "確認換裝 · 套用新外觀"
	_btn_confirm.custom_minimum_size = Vector2(0, BTN_SIZE)
	_btn_confirm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_confirm.add_theme_font_size_override("font_size", 18)
	_btn_confirm.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_btn_confirm.add_theme_font_override("font", _cached_font)
	_btn_confirm.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 18, 2))
	var c_h := _create_button_style(Color("#5EED7C"), COLOR_BORDER, 3, 18, 2)
	_btn_confirm.add_theme_stylebox_override("hover", c_h)
	_btn_confirm.add_theme_stylebox_override("pressed", c_h)
	_btn_confirm.pressed.connect(confirm_selection)
	actions_hbox.add_child(_btn_confirm)


## ── 種族篩選 tab/chip 列建置 ──
func _create_race_filter_bar() -> Control:
	var container := VBoxContainer.new()
	container.name = "RaceFilterContainer"
	container.add_theme_constant_override("separation", 4)

	var header_hbox := HBoxContainer.new()
	header_hbox.add_theme_constant_override("separation", 6)
	container.add_child(header_hbox)

	var label := Label.new()
	label.text = "外裝庫"
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	label.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		label.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(label)

	var tip := Label.new()
	tip.text = "點「全部」可跨族穿：騎士／法師／遊俠／格鬥／維京"
	tip.add_theme_font_size_override("font_size", 14)
	tip.add_theme_color_override("font_color", Color("#5E5475"))
	if _cached_font:
		tip.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(tip)

	var chip_scroll := ScrollContainer.new()
	chip_scroll.name = "FilterScroll"
	chip_scroll.custom_minimum_size = Vector2(0, 54)
	chip_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	chip_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	container.add_child(chip_scroll)

	var hbox := HBoxContainer.new()
	hbox.name = "ChipsHBox"
	hbox.add_theme_constant_override("separation", 4)
	chip_scroll.add_child(hbox)

	_filter_chips.clear()
	for opt in RACE_FILTER_OPTIONS:
		var rid: String = str(opt.get("id", ""))
		var rname: String = str(opt.get("name_zh", rid))
		var btn := Button.new()
		btn.name = "Chip_" + rid
		btn.text = rname
		# ⚠️ 觸控熱區下限 48px，寬度 46px 確保九族＋全部（共10顆標籤）在各螢幕寬度下完整容納不被切半
		btn.custom_minimum_size = Vector2(46, 48)
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn.add_theme_font_size_override("font_size", 14)
		if _cached_font:
			btn.add_theme_font_override("font", _cached_font)
		btn.pressed.connect(func(): set_race_filter(rid))
		hbox.add_child(btn)
		_filter_chips[rid] = btn

	# 末端保留右邊距，確保最右側 chip 滾動到終點時不被容器邊界裁剪
	var end_spacer := Control.new()
	end_spacer.name = "EndSpacer"
	end_spacer.custom_minimum_size = Vector2(8, 0)
	hbox.add_child(end_spacer)

	_update_filter_chips_visual()
	return container


func set_race_filter(race_id: String) -> void:
	current_filter_race = race_id
	if race_id != "all":
		current_race = race_id
		costume_index = 0
		chassis_index = 0
		selected_costume_id = ""
		selected_chassis_id = ""
	_update_filter_chips_visual()
	_rebuild_cards()
	_update_preview()
	_update_ui_texts()


func _update_filter_chips_visual() -> void:
	for rid in _filter_chips.keys():
		var btn: Button = _filter_chips[rid]
		var is_selected: bool = (str(rid) == current_filter_race)
		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(14)
		sb.content_margin_left = 6
		sb.content_margin_right = 6
		sb.content_margin_top = 4
		sb.content_margin_bottom = 4
		if is_selected:
			sb.bg_color = COLOR_GOLD
			sb.border_color = COLOR_ORANGE
			sb.set_border_width_all(2)
			sb.border_width_bottom = 5
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
			sb.shadow_size = 4
			sb.shadow_offset = Vector2(0, 2)
			btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
			_scroll_to_chip(btn)
		else:
			# 次級膠囊補齊立體厚底質感，對齊規格下限 (>=3px)
			sb.bg_color = Color(0.92, 0.90, 0.86, 0.85)
			sb.border_color = COLOR_BORDER
			sb.set_border_width_all(1)
			sb.border_width_bottom = 3
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.10)
			sb.shadow_size = 3
			sb.shadow_offset = Vector2(0, 1)
			btn.add_theme_color_override("font_color", Color("#4D456B"))
		btn.add_theme_stylebox_override("normal", sb)

		var sb_h := sb.duplicate()
		sb_h.bg_color = Color("#FFF4D0")
		btn.add_theme_stylebox_override("hover", sb_h)

		var sb_p := sb.duplicate()
		sb_p.border_width_bottom = max(1, sb.border_width_bottom - 2)
		sb_p.shadow_size = max(0, sb.shadow_size - 2)
		btn.add_theme_stylebox_override("pressed", sb_p)


func _scroll_to_chip(btn: Button) -> void:
	call_deferred("_do_scroll_to_chip", btn)


func _do_scroll_to_chip(btn: Button) -> void:
	var scroll := find_child("FilterScroll", true, false) as ScrollContainer
	if not scroll or not is_instance_valid(scroll) or not is_instance_valid(btn):
		return
	var hbar := scroll.get_h_scroll_bar()
	var view_w: float = scroll.size.x
	var btn_left: float = btn.position.x
	var btn_right: float = btn_left + btn.size.x
	var pad: float = 16.0 # 邊界緩衝，確保左右均不被裁剪

	if btn_right + pad > scroll.scroll_horizontal + view_w:
		var target := int(ceil(btn_right + pad - view_w))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value))
		scroll.scroll_horizontal = target
	elif btn_left - pad < scroll.scroll_horizontal:
		var target := int(floor(max(0.0, btn_left - pad)))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value))
		scroll.scroll_horizontal = target


func _get_race_short_name(rid: String) -> String:
	match rid:
		"rabbit": return "兔"
		"fox": return "狐"
		"lion": return "獅"
		"boar": return "野豬"
		"macaque": return "猴"
		"tiger": return "虎"
		"bear": return "熊"
		"crane": return "鶴"
		"penguin": return "企鵝"
		"tortoise": return "龜"
		"elephant": return "象"
		"frog": return "蛙"
		"panda": return "貓"
		"fawn": return "鹿"
		_: return rid


## 建立卡片網格區塊 (卡片網格＋果凍框『✓ 已選用』，多於一頁採 ScrollContainer)
func _create_grid_section(section_title: String, slot_type: String) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	# 次級容器不重複加框：採用純背景色分隔，邊框寬度為 0 且拿掉陰影，避免框中框
	panel.add_theme_stylebox_override("panel", UiStyle.sub_panel_style(COLOR_CARD_WARM, 16))

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
	title_lbl.add_theme_font_size_override("font_size", 16)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(title_lbl)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_hbox.add_child(spacer)

	var tip_lbl := Label.new()
	tip_lbl.text = "點擊卡片即時預覽"
	tip_lbl.add_theme_font_size_override("font_size", 14)
	tip_lbl.add_theme_color_override("font_color", COLOR_SKY)
	tip_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	tip_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		tip_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(tip_lbl)

	# 捲動容器包覆 GridContainer (每列 4 格)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.y = 135
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	vbox.add_child(scroll)

	# 透過 ScrollMargin 邊距隔離垂直捲軸，確保捲軸不覆蓋最右側卡片邊框與內容 (對齊 t_1db22c2d 規範)
	var scroll_margin := MarginContainer.new()
	scroll_margin.name = "ScrollMargin"
	scroll_margin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll_margin.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll_margin.add_theme_constant_override("margin_left", 2)
	scroll_margin.add_theme_constant_override("margin_right", 18)
	scroll_margin.add_theme_constant_override("margin_top", 2)
	scroll_margin.add_theme_constant_override("margin_bottom", 6)
	scroll_margin.mouse_filter = Control.MOUSE_FILTER_PASS
	scroll.add_child(scroll_margin)

	var grid := GridContainer.new()
	grid.name = "GridCostume" if slot_type == "costume" else "GridChassis"
	grid.columns = 4
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	scroll_margin.add_child(grid)

	if slot_type == "costume":
		_costume_grid = grid
	else:
		_chassis_grid = grid

	return panel


## 重新建置全部卡片 (支援種族篩選)
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
	_displayed_costumes.clear()
	_displayed_chassis.clear()

	var PaperdollSelectClass = load("res://scripts/ui/paperdoll_select_demo.gd")
	var all_data: Dictionary = {}
	if PaperdollSelectClass and "RACES_DATA" in PaperdollSelectClass:
		all_data = PaperdollSelectClass.RACES_DATA

	var target_races: Array[String] = []
	if current_filter_race == "all":
		target_races = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn"]
	else:
		target_races = [current_filter_race]

	for rid in target_races:
		if not all_data.has(rid):
			continue
		var r_data: Dictionary = all_data[rid]
		var costumes: Array = r_data.get("costumes", [])
		for c in costumes:
			var item := (c as Dictionary).duplicate()
			item["race_id"] = rid
			_displayed_costumes.append(item)
		var chassis_list: Array = r_data.get("chassis", [])
		for p in chassis_list:
			var item := (p as Dictionary).duplicate()
			item["race_id"] = rid
			_displayed_chassis.append(item)

	for i in range(_displayed_costumes.size()):
		var card := _create_item_card("costume", i, _displayed_costumes[i])
		_costume_grid.add_child(card)
		_costume_cards.append(card)

	for i in range(_displayed_chassis.size()):
		var card := _create_item_card("chassis", i, _displayed_chassis[i])
		_chassis_grid.add_child(card)
		_chassis_cards.append(card)

	_update_card_selection_states()


## 建立單張縮圖卡片按鈕
func _create_item_card(slot_type: String, idx: int, item_data: Dictionary) -> Button:
	var btn := Button.new()
	btn.name = "Card_%s_%d" % [slot_type, idx]
	btn.custom_minimum_size = Vector2(110, 148)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND

	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 4)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_right", 4)
	margin.add_theme_constant_override("margin_bottom", 6)
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	btn.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 2)
	vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_child(vbox)

	var item_race: String = str(item_data.get("race_id", current_race))
	var item_id: String = str(item_data.get("id", ""))

	# 部件縮圖
	var thumb := TextureRect.new()
	thumb.custom_minimum_size = Vector2(72, 72)
	thumb.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	thumb.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	thumb.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	thumb.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	thumb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	thumb.texture = _get_item_thumbnail(slot_type, item_id, item_race)
	vbox.add_child(thumb)

	# 部件名稱
	var name_lbl := Label.new()
	var raw_name: String = str(item_data.get("name_zh", ""))
	if current_filter_race == "all":
		var r_short: String = _get_race_short_name(item_race)
		name_lbl.text = "[%s] %s" % [r_short, raw_name]
	else:
		name_lbl.text = raw_name
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 13)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	# 商品名一律完整顯示，⛔ 不截斷成「…」（收費點面板玩家要看得到全名）
	name_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
	name_lbl.custom_minimum_size.y = 34
	name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(name_lbl)

	# 選取狀態標籤 (『✓ 已選用』)
	var badge_lbl := Label.new()
	badge_lbl.name = "BadgeLabel"
	badge_lbl.text = ""
	badge_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	badge_lbl.add_theme_font_size_override("font_size", 12)
	badge_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	badge_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	badge_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		badge_lbl.add_theme_font_override("font", _cached_font)
	badge_lbl.custom_minimum_size.y = 16
	badge_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(badge_lbl)

	# 點擊即時套用預覽：外裝／塗裝跨種族穿，不改動物本體
	btn.pressed.connect(func():
		if slot_type == "costume":
			costume_index = idx
			selected_costume_id = item_id
		else:
			chassis_index = idx
			selected_chassis_id = item_id
		_update_card_selection_states()
		_update_preview()
		_update_ui_texts()
	)

	return btn


## 取得部件對應之縮圖貼圖（優先 512 高清切片，禁止把 128 像素切片塞進小格）
func _get_item_thumbnail(slot_type: String, item_id: String, item_race: String = "") -> Texture2D:
	var r := item_race if not item_race.is_empty() else current_race

	if slot_type == "costume":
		if item_id in ["none", "bare", "empty"]:
			var bare_part_512 := "res://assets/sprites/player/paperdoll/%s/costume/costume_none_512.png" % r
			if not ResourceLoader.exists(bare_part_512):
				bare_part_512 = "res://assets/sprites/player/paperdoll/%s/costume/costume_bare_512.png" % r
			if ResourceLoader.exists(bare_part_512):
				return load(bare_part_512) as Texture2D
			var bare_512 := "res://assets/sprites/player/paperdoll/%s/composite_preview_bare_512.png" % r
			if ResourceLoader.exists(bare_512):
				return load(bare_512) as Texture2D
			var bare_comp := PaperdollRenderer.build_composite_texture_512(r, {"costume": "none"})
			if bare_comp != null:
				return bare_comp
			return null

		# 1. 優先 512 切片 (本族 512 -> 通用 common/costume/ -> 去前綴 512)
		var path512 := "res://assets/sprites/player/paperdoll/%s/costume/%s_512.png" % [r, item_id]
		if ResourceLoader.exists(path512):
			return load(path512) as Texture2D

		var p_common_512 := "res://assets/sprites/player/paperdoll/common/costume/%s_512.png" % item_id
		if ResourceLoader.exists(p_common_512):
			return load(p_common_512) as Texture2D

		var clean_id := item_id.trim_prefix("costume_")
		var p_common_512_clean := "res://assets/sprites/player/paperdoll/common/costume/%s_512.png" % clean_id
		if ResourceLoader.exists(p_common_512_clean):
			return load(p_common_512_clean) as Texture2D

		# 2. 檢查高清展示立牌裁切 (showcase/*_hd_cut.png, 長邊 >= 512，僅限本族)
		var hd_cut := "res://assets/sprites/player/showcase/%s_%s_hd_cut.png" % [r, item_id]
		if ResourceLoader.exists(hd_cut):
			return load(hd_cut) as Texture2D

		# 3. 跨族 512 衣服切片共用（同件衣服若在別族目錄下）
		var all_races := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn"]
		for other in all_races:
			if other == r:
				continue
			var cross_512 := "res://assets/sprites/player/paperdoll/%s/costume/%s_512.png" % [other, item_id]
			if ResourceLoader.exists(cross_512):
				return load(cross_512) as Texture2D

		# 4. 找不到任何 512 切片時回 null（UI 顯示無縮圖佔位，禁止拿另一件衣服冒充）
		return null

	elif slot_type == "chassis":
		# 1. 優先 512 底盤切片 (本族 chassis/*_512.png，長邊 512)
		var path512 := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [r, item_id]
		if ResourceLoader.exists(path512):
			return load(path512) as Texture2D

		# 2. 跨族 512 底盤共用
		var all_races := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn"]
		for other in all_races:
			if other == r:
				continue
			var cross_ch_512 := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [other, item_id]
			if ResourceLoader.exists(cross_ch_512):
				return load(cross_ch_512) as Texture2D

		var clean_id := item_id.trim_prefix("paint_")
		for other in all_races:
			var cross_clean := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [other, clean_id]
			if ResourceLoader.exists(cross_clean):
				return load(cross_clean) as Texture2D

	return null


## 更新所有卡片的亮金邊框與『✓ 已選用』狀態
func _update_card_selection_states() -> void:
	for i in range(_costume_cards.size()):
		var item: Dictionary = _displayed_costumes[i] if i < _displayed_costumes.size() else {}
		var item_id: String = str(item.get("id", ""))
		var item_race: String = str(item.get("race_id", current_race))
		var is_selected := false
		if not selected_costume_id.is_empty():
			if current_filter_race == "all":
				is_selected = (i == costume_index)
			else:
				is_selected = (item_id == selected_costume_id)
		else:
			is_selected = (i == costume_index)
		_apply_card_style(_costume_cards[i], is_selected)

	for i in range(_chassis_cards.size()):
		var item: Dictionary = _displayed_chassis[i] if i < _displayed_chassis.size() else {}
		var item_id: String = str(item.get("id", ""))
		var item_race: String = str(item.get("race_id", current_race))
		var is_selected := false
		if not selected_chassis_id.is_empty():
			if current_filter_race == "all":
				is_selected = (i == chassis_index)
			else:
				is_selected = (item_id == selected_chassis_id)
		else:
			is_selected = (i == chassis_index)
		_apply_card_style(_chassis_cards[i], is_selected)


## 套用單張卡片之視覺樣式 (選中時果凍金黃底 + 暖橘框 + 『✓ 已選用』)
func _apply_card_style(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(14)
	if is_selected:
		sb.bg_color = COLOR_CARD_GOLD         ## 金黃柔和卡片底
		sb.border_color = COLOR_ORANGE        ## 暖橘立體邊框
		sb.set_border_width_all(2)
		sb.border_width_bottom = 6           ## 立體果凍厚底 (5~6px)
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
	else:
		sb.bg_color = COLOR_BG_CREAM         ## 陽光童話奶油米白底
		sb.border_color = COLOR_BORDER       ## 深藍紫描邊
		sb.set_border_width_all(1)
		sb.border_width_bottom = 3           ## 對齊 ART_DAILY_CONSTITUTION.md §3 規格下限 (>=3px)
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12) ## 保留較淺陰影
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
	btn.add_theme_stylebox_override("normal", sb)

	var sb_h := sb.duplicate()
	if is_selected:
		sb_h.bg_color = Color("#FFF8DC")
		sb_h.border_color = COLOR_GOLD
	else:
		sb_h.bg_color = COLOR_CARD_WARM
		sb_h.border_color = COLOR_ORANGE
	btn.add_theme_stylebox_override("hover", sb_h)

	var sb_p := sb.duplicate()
	sb_p.border_width_bottom = max(1, sb.border_width_bottom - 2)
	sb_p.shadow_size = max(0, sb.shadow_size - 2)
	btn.add_theme_stylebox_override("pressed", sb_p)

	var badge = btn.find_child("BadgeLabel", true, false)
	if badge is Label:
		badge.text = "✓ 已選用" if is_selected else ""


func _create_panel_style(bg: Color, border: Color, border_w: int = 2, bottom_w: int = 4, radius: int = 20) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = border
	sb.set_border_width_all(border_w)
	sb.border_width_bottom = bottom_w
	sb.set_corner_radius_all(radius)
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	sb.shadow_size = 10
	sb.shadow_offset = Vector2(0, 5)
	return sb


func _create_button_style(bg: Color, border: Color = COLOR_BORDER, bottom_border: int = 6, radius: int = 18, border_w: int = 2) -> StyleBoxFlat:
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
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.30)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 4)
	return sb


func _on_reset_pressed() -> void:
	costume_index = 0
	chassis_index = 0
	selected_costume_id = ""
	selected_chassis_id = ""
	_update_card_selection_states()
	_update_ui_texts()
	_update_preview()


func _on_random_pressed() -> void:
	randomize_selection()


## 隨機挑選一組外觀（在 current_filter_race 篩選範圍內，純預覽不寫存檔）
func randomize_selection() -> void:
	if _displayed_costumes.is_empty() and _displayed_chassis.is_empty():
		return

	if not _displayed_costumes.is_empty():
		var new_c_idx := randi() % _displayed_costumes.size()
		if _displayed_costumes.size() > 1 and new_c_idx == costume_index:
			new_c_idx = (new_c_idx + 1 + (randi() % (_displayed_costumes.size() - 1))) % _displayed_costumes.size()
		costume_index = new_c_idx
		selected_costume_id = str(_displayed_costumes[costume_index].get("id", ""))

	if not _displayed_chassis.is_empty():
		var new_p_idx := randi() % _displayed_chassis.size()
		if _displayed_chassis.size() > 1 and new_p_idx == chassis_index:
			new_p_idx = (new_p_idx + 1 + (randi() % (_displayed_chassis.size() - 1))) % _displayed_chassis.size()
		chassis_index = new_p_idx
		selected_chassis_id = str(_displayed_chassis[chassis_index].get("id", ""))

	_update_card_selection_states()
	_update_preview()
	_update_ui_texts()


func get_current_selections() -> Dictionary:
	var cur_costume: Dictionary = {}
	if costume_index < _displayed_costumes.size():
		cur_costume = _displayed_costumes[costume_index]
	var cur_chassis: Dictionary = {}
	if chassis_index < _displayed_chassis.size():
		cur_chassis = _displayed_chassis[chassis_index]

	if cur_costume.is_empty() or cur_chassis.is_empty():
		var data := _get_race_data()
		var costumes: Array = data.get("costumes", [])
		var chassis_list: Array = data.get("chassis", [])
		if cur_costume.is_empty() and costume_index < costumes.size():
			cur_costume = costumes[costume_index]
		if cur_chassis.is_empty() and chassis_index < chassis_list.size():
			cur_chassis = chassis_list[chassis_index]

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
	var idle_tex: Texture2D = SpriteDB.player_equipped_idle(current_race, sel)
	if idle_tex != null:
		_preview_rect.texture = idle_tex
		_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		return
	var tex_512: Texture2D = PaperdollRenderer.get_race_composite_texture_512(current_race, sel)
	if tex_512 != null:
		_preview_rect.texture = tex_512
		_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		return
	var img := PaperdollRenderer.build_composite_image(current_race, sel)
	if img != null and not img.is_empty():
		_preview_rect.texture = ImageTexture.create_from_image(img)
		_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		return
	var costume := str(sel.get("costume", sel.get("costume_id", "")))
	var hd_cut := "res://assets/sprites/player/showcase/%s_%s_hd_cut.png" % [current_race, costume]
	if ResourceLoader.exists(hd_cut):
		_preview_rect.texture = load(hd_cut) as Texture2D
		_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR


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
	_stop_breathe_tween()
	cancelled.emit()
	queue_free()


## 待機呼吸小動作 (對齊大廳人體工學規範：scale 在 (1.03, 0.97) ↔ (0.98, 1.02)、約 1.1s、TRANS_SINE、loop)
func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid() and _breathe_tween.is_running():
		return
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if _preview_rect:
		_preview_rect.scale = Vector2.ONE
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_preview_rect, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_preview_rect, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _stop_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
		_breathe_tween = null
	if _preview_rect:
		_preview_rect.scale = Vector2.ONE


func is_breathe_running() -> bool:
	return _breathe_tween != null and _breathe_tween.is_valid() and _breathe_tween.is_running()
