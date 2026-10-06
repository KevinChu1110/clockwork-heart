class_name WardrobeDialog
extends Control
## 《發條之心》大廳角色換裝衣櫥與紙娃娃工坊彈窗 (WardrobeDialog)
## 依多巴胺亮色盤規範與手遊展示工坊規格：
## 1. 橫屏彈窗寬 740~760px，置中顯示，背景全螢幕半透明遮罩 (Scrim)。
## 2. 右上「✕」關閉按鈕尺寸 >= 50px，點擊遮罩空白處亦可關閉。
## 3. 多巴胺亮色盤：金黃 #FFD028、暖橘 #FFA010、薄荷綠 #4ED86A、天藍 #38A0FF、珊瑚粉 #FF5E8A，描邊深藍紫 #1F1A3A，底板奶油白 #FFFDF8。
## 4. 圓角 18~24px，按鈕立體果凍厚底 (bottom border 5~6px)，按鈕高度均 >= 50px。
## 5. 字級 16~24px 加粗帶深色厚描邊，零小字。
## 6. 左側：立體溫潤木質旋轉展示台 (3D Wooden Rotating Turntable)，微縮玩具展示盒焦點。
## 7. 右側：七大槽位採用果凍厚底色階圓角光框（頭/外裝/武器/發條/核心/奇玩/塗裝）與即時流光。
## 8. 換裝反饋：金色星芒爆散 (Golden Starburst) 與金屬齒輪清脆音效 (Clock ratchet SFX)。
## 9. 部件挑選採 GridContainer 每列 4 格縮圖卡片網格，已裝備格附亮金/暖橘果凍框與『✓ 已選用』標籤。
## 10. 全程 0 系統 emoji，角色待機呼吸動畫持續進行。

signal outfit_saved(race_id: String, selections: Dictionary)
signal cancelled()

@export var creation_mode: bool = false

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const WindingKeyAnimator = preload("res://scripts/art/winding_key_animator.gd")

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

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
const COLOR_PURPLE     := Color("#A259FF")  ## 炫彩紫
const COLOR_BORDER     := Color("#1F1A3A")  ## 深藍紫描邊
const COLOR_BG_CREAM   := Color("#FFFDF8")  ## 陽光童話·奶油米白底
const COLOR_CARD_WARM  := Color("#FFF8E7")  ## 溫暖米黃卡片底
const COLOR_CARD_SKY   := Color("#F0F7FF")  ## 柔和天藍卡片底
const COLOR_CARD_GOLD  := Color("#FFF4D0")  ## 金黃柔和卡片底
const COLOR_TEXT_DARK  := Color("#1F1A3A")  ## 深藍紫加粗文字
const COLOR_TEXT_GOLD  := Color("#9A6B00")  ## 壓明度金黃（亮底文字專用）
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const COLOR_TEXT_PINK  := Color("#D62E5C")  ## 壓明度珊瑚粉（亮底文字專用）

## 七大槽位規格定義
const SEVEN_SLOTS: Array[Dictionary] = [
	{
		"id": "costume",
		"name_zh": "外裝",
		"title_zh": "外裝服飾 (Costume)",
		"icon_asset": "res://assets/icons/core_slots/slot_02_chassis_armor.png",
		"grid_name": "GridCostume"
	},
	{
		"id": "chassis",
		"name_zh": "塗裝",
		"title_zh": "機體塗裝 (Chassis / Paint)",
		"icon_asset": "res://assets/icons/core_slots/slot_01_spring_generator.png",
		"grid_name": "GridChassis"
	},
	{
		"id": "head_unit",
		"name_zh": "頭部",
		"title_zh": "頭部機關 (Head Unit)",
		"icon_asset": "res://assets/icons/core_slots/slot_03_escapement_governor.png",
		"grid_name": "GridHeadUnit"
	},
	{
		"id": "weapon",
		"name_zh": "武器",
		"title_zh": "手持武器 (Weapon)",
		"icon_asset": "res://assets/icons/hud/icon_dock_equip.png",
		"grid_name": "GridWeapon"
	},
	{
		"id": "winding_key",
		"name_zh": "發條",
		"title_zh": "背部發條 (Wind-up Key)",
		"icon_asset": "res://assets/icons/hud/icon_energy_key.png",
		"grid_name": "GridWindingKey"
	},
	{
		"id": "optic_core",
		"name_zh": "核心",
		"title_zh": "光學核心 (Optic Core)",
		"icon_asset": "res://assets/icons/core_slots/slot_05_resonance_core.png",
		"grid_name": "GridOpticCore"
	},
	{
		"id": "back_curio",
		"name_zh": "奇玩",
		"title_zh": "隨身奇玩 (Back Curio)",
		"icon_asset": "res://assets/icons/core_slots/slot_04_transmission_gears.png",
		"grid_name": "GridBackCurio"
	}
]

## UI 節點參照
var _scrim: ColorRect
var _dialog_card: PanelContainer
var _title_label: Label
var _subtitle_label: Label
var _close_btn: Button

var _stage_panel: PanelContainer
var _pedestal_stage: Control
var _preview_rect: TextureRect
var _badge_name_label: Label
var _badge_race_label: Label

var _filter_title_lbl: Label
var _filter_tip_lbl: Label
var _costume_section_title: Label
var _costume_section_tip: Label
var _chassis_section_title: Label
var _chassis_section_tip: Label

var _workshop_scroll: ScrollContainer
var _section_nodes: Dictionary = {} # slot_type -> PanelContainer
var _slot_grids: Dictionary = {}    # slot_type -> GridContainer
var _slot_cards: Dictionary = {}    # slot_type -> Array[Button]
var _displayed_items: Dictionary = {} # slot_type -> Array[Dictionary]

var _costume_grid: GridContainer
var _chassis_grid: GridContainer
var _costume_cards: Array[Button] = []
var _chassis_cards: Array[Button] = []
var _displayed_costumes: Array[Dictionary] = []
var _displayed_chassis: Array[Dictionary] = []

var _slot_btns: Dictionary = {}      # slot_type -> Button
var _slot_sheen_nodes: Dictionary = {} # slot_type -> SheenOverlay
var active_slot_tab: String = "costume"

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
	{"id": "panda", "name_zh": "熊貓"},
	{"id": "fawn", "name_zh": "鹿"},
	{"id": "hound", "name_zh": "犬"},
	{"id": "owl", "name_zh": "鴞"},
	{"id": "cat", "name_zh": "貓"},
	{"id": "pangolin", "name_zh": "穿山甲"},
	{"id": "otter", "name_zh": "海獺"},
	{"id": "raccoon", "name_zh": "浣熊"},
	{"id": "hedgehog", "name_zh": "刺蝟"},
	{"id": "wolf", "name_zh": "鋼狼"},
	{"id": "seahorse", "name_zh": "海馬"},
	{"id": "kangaroo", "name_zh": "袋鼠"},
	{"id": "squirrel", "name_zh": "松鼠"},
	{"id": "salamander", "name_zh": "蜥蜴"},
	{"id": "viper", "name_zh": "青蛇"},
	{"id": "falcon", "name_zh": "神隼"},
	{"id": "ram", "name_zh": "靈羊"},
	{"id": "chameleon", "name_zh": "變色龍"},
	{"id": "sailfish", "name_zh": "旗魚"},
	{"id": "rhino", "name_zh": "犀牛"},
	{"id": "bat", "name_zh": "蝙蝠"},
	{"id": "gorilla", "name_zh": "巨猩"},
	{"id": "peacock", "name_zh": "孔雀"},
	{"id": "meerkat", "name_zh": "狐獴"},
	{"id": "courser", "name_zh": "駿駒"},
	{"id": "beaver", "name_zh": "河狸"},
	{"id": "stoat", "name_zh": "伶鼬"},
	{"id": "seal", "name_zh": "海豹"},
	{"id": "raven", "name_zh": "渡鴉"},
	{"id": "kite", "name_zh": "赤鳶"},
	{"id": "swan", "name_zh": "天鵝"},
	{"id": "bison", "name_zh": "野牛"},
	{"id": "gecko", "name_zh": "守宮"},
	{"id": "badger", "name_zh": "蜜獾"},
	{"id": "capybara", "name_zh": "水豚"},
	{"id": "woodpecker", "name_zh": "啄木鳥"},
	{"id": "armadillo", "name_zh": "犰狳"},
	{"id": "caterpillar", "name_zh": "毛蟲"},
	{"id": "cuttlefish", "name_zh": "烏賊"},
	{"id": "crab", "name_zh": "石蟹"},
	{"id": "camel", "name_zh": "駱駝"},
	{"id": "giraffe", "name_zh": "長頸鹿"},
	{"id": "hippo", "name_zh": "河馬"},
	{"id": "mole", "name_zh": "鼴鼠"},
	{"id": "petaurista", "name_zh": "鼯鼠"},
	{"id": "lynx", "name_zh": "猞猁"},
	{"id": "scarab", "name_zh": "金龜"},
	{"id": "toucan", "name_zh": "巨嘴鳥"},
	{"id": "walrus", "name_zh": "海象"},
	{"id": "takin", "name_zh": "羚牛"},
	{"id": "lemur", "name_zh": "狐猴"},
	{"id": "marmot", "name_zh": "旱獺"},
	{"id": "firefly", "name_zh": "飛螢"},
	{"id": "manta", "name_zh": "蝠魟"},
	{"id": "kingfisher", "name_zh": "翠鳥"},
	{"id": "donkey", "name_zh": "頑驢"},
	{"id": "scorpion", "name_zh": "沙蠍"},
]

## 檢查種族是否具備美術立繪與切片資源
func _has_race_assets(race_id: String) -> bool:
	if race_id == "all":
		return true
	var PaperdollSelectClass = load("res://scripts/ui/paperdoll_select_demo.gd")
	if PaperdollSelectClass and PaperdollSelectClass.has_method("has_race_assets"):
		return PaperdollSelectClass.has_race_assets(race_id)
	return true

var current_filter_race: String = "all"
var _filter_chips: Dictionary = {}

## 七大槽位選取狀態與索引
var current_race: String = "rabbit"

var costume_index: int = 0:
	set(v):
		costume_index = v
		if _displayed_costumes.size() > 0 and costume_index < _displayed_costumes.size():
			selected_costume_id = str(_displayed_costumes[costume_index].get("id", ""))
		if _ui_built:
			_update_card_selection_states()

var chassis_index: int = 0:
	set(v):
		chassis_index = v
		if _displayed_chassis.size() > 0 and chassis_index < _displayed_chassis.size():
			selected_chassis_id = str(_displayed_chassis[chassis_index].get("id", ""))
		if _ui_built:
			_update_card_selection_states()

var head_unit_index: int = 0
var winding_key_index: int = 0
var weapon_index: int = 0
var optic_core_index: int = 0
var back_curio_index: int = 0

var selected_costume_id: String = ""
var selected_chassis_id: String = ""
var selected_head_unit_id: String = ""
var selected_winding_key_id: String = ""
var selected_weapon_id: String = ""
var selected_optic_core_id: String = ""
var selected_back_curio_id: String = ""

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
	_update_seven_slots_visual()
	_connect_loc_signal()


func _ready() -> void:
	ensure_ui()
	_init_from_game_state()
	_update_filter_chips_visual()
	_rebuild_cards()
	_update_ui_texts()
	_update_preview()
	_update_seven_slots_visual()
	_connect_loc_signal()
	_start_breathe_tween()


func _exit_tree() -> void:
	_stop_breathe_tween()
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc := (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)


func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var loc := (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)


func _on_locale_changed(_new_locale: String = "") -> void:
	_update_ui_texts()
	_refresh_card_texts()
	_update_card_selection_states()
	_update_seven_slots_visual()


func _refresh_card_texts() -> void:
	for slot_type in _slot_cards.keys():
		var cards: Array = _slot_cards[slot_type]
		for btn in cards:
			if not is_instance_valid(btn):
				continue
			var name_lbl = btn.find_child("NameLabel", true, false)
			if name_lbl is Label and name_lbl.has_meta("raw_name"):
				var raw_name: String = str(name_lbl.get_meta("raw_name", ""))
				var loc_name := _t(raw_name)
				var item_race: String = str(name_lbl.get_meta("item_race", ""))
				if current_filter_race == "all" and not item_race.is_empty():
					var r_short: String = _get_race_short_name(item_race)
					name_lbl.text = "[%s] %s" % [_t(r_short), loc_name]
				else:
					name_lbl.text = loc_name


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
		if not r.is_empty() and _has_race_assets(r):
			current_race = r

	current_filter_race = current_race

	var equipped_costume: String = ""
	var equipped_paint: String = ""
	var equipped_head: String = ""
	var equipped_key: String = ""
	var equipped_weapon: String = ""
	var equipped_core: String = ""
	var equipped_curio: String = ""

	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		var ps: Dictionary = gs.paperdoll_slots
		equipped_costume = str(ps.get("costume_id", ps.get("costume", "")))
		equipped_paint = str(ps.get("paint_id", ps.get("chassis", "")))
		equipped_head = str(ps.get("head_unit", ""))
		equipped_key = str(ps.get("winding_key", ""))
		equipped_weapon = str(ps.get("weapon", ""))
		equipped_core = str(ps.get("optic_core", ""))
		equipped_curio = str(ps.get("back_curio", ""))

	# 預設各部位 fallback
	if equipped_costume.is_empty():
		equipped_costume = str(PaperdollRenderer._get_default_variant_id(current_race, "costume"))
	if equipped_paint.is_empty():
		equipped_paint = str(PaperdollRenderer._get_default_variant_id(current_race, "chassis"))
	if equipped_head.is_empty():
		equipped_head = str(PaperdollRenderer._get_default_variant_id(current_race, "head_unit"))
	if equipped_key.is_empty():
		equipped_key = str(PaperdollRenderer._get_default_variant_id(current_race, "winding_key"))
	if equipped_weapon.is_empty():
		equipped_weapon = str(PaperdollRenderer._get_default_variant_id(current_race, "weapon"))
	if equipped_core.is_empty():
		equipped_core = str(PaperdollRenderer._get_default_variant_id(current_race, "optic_core"))
	if equipped_curio.is_empty():
		equipped_curio = str(PaperdollRenderer._get_default_variant_id(current_race, "back_curio"))

	selected_costume_id = equipped_costume
	selected_chassis_id = equipped_paint
	selected_head_unit_id = equipped_head
	selected_winding_key_id = equipped_key
	selected_weapon_id = equipped_weapon
	selected_optic_core_id = equipped_core
	selected_back_curio_id = equipped_curio

	# 對齊當前種族預設卡片索引
	var data := _get_race_data()
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	costume_index = 0
	for i in range(costumes.size()):
		if str(costumes[i].get("id", "")) == selected_costume_id:
			costume_index = i
			break

	chassis_index = 0
	for i in range(chassis_list.size()):
		if str(chassis_list[i].get("id", "")) == selected_chassis_id:
			chassis_index = i
			break


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
	_title_label.text = _t("發條衣櫥 · 英雄換裝")
	_title_label.add_theme_font_size_override("font_size", 22)
	_title_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_title_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_title_label.add_theme_constant_override("outline_size", 4)
	if _cached_font:
		_title_label.add_theme_font_override("font", _cached_font)
	title_vbox.add_child(_title_label)

	_subtitle_label = Label.new()
	_subtitle_label.text = _t("個人化外觀部件即時切換 · 零數值純視覺展示")
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

	# ── 中間主內容區 (左側3D立體木質展台 + 右側七大槽位光框與卡片網格) ──
	var main_hbox := HBoxContainer.new()
	main_hbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	main_hbox.add_theme_constant_override("separation", 16)
	root_vbox.add_child(main_hbox)

	# ── 左側：立體溫潤木質旋轉展示台 (3D Wooden Rotating Turntable Showroom) ──
	_stage_panel = PanelContainer.new()
	_stage_panel.name = "StagePanel"
	_stage_panel.custom_minimum_size = Vector2(250, 480)
	_stage_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, Color("#D4AF37"), 2, 4, 20))
	main_hbox.add_child(_stage_panel)

	var stage_vbox := VBoxContainer.new()
	stage_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	stage_vbox.add_theme_constant_override("separation", 6)
	_stage_panel.add_child(stage_vbox)

	# 頂部展廳標籤
	var stage_header := Label.new()
	stage_header.text = _t("✦ 玩具工坊 · 旋轉展台 ✦")
	stage_header.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stage_header.add_theme_font_size_override("font_size", 14)
	stage_header.add_theme_color_override("font_color", COLOR_TEXT_GOLD)
	stage_header.add_theme_color_override("font_outline_color", COLOR_BORDER)
	stage_header.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		stage_header.add_theme_font_override("font", _cached_font)
	stage_vbox.add_child(stage_header)

	# 3D 立體木質展示台主體容器
	_pedestal_stage = _create_pedestal_stage_control()
	_pedestal_stage.custom_minimum_size = Vector2(234, 300)
	_pedestal_stage.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	_pedestal_stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stage_vbox.add_child(_pedestal_stage)

	# 角色預覽紋理 (置於立體展示台之上，雙足穩固接地於木質圓盤中心)
	_preview_rect = TextureRect.new()
	_preview_rect.name = "HeroPreviewRect"
	_preview_rect.custom_minimum_size = Vector2(220, 270)
	_preview_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	_preview_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_preview_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_preview_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_preview_rect.pivot_offset = Vector2(110, 240)
	_preview_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_pedestal_stage.add_child(_preview_rect)

	# 底部名牌資訊欄
	var badge_box := VBoxContainer.new()
	badge_box.alignment = BoxContainer.ALIGNMENT_CENTER
	badge_box.add_theme_constant_override("separation", 2)
	stage_vbox.add_child(badge_box)

	_badge_name_label = Label.new()
	_badge_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_name_label.add_theme_font_size_override("font_size", 19)
	_badge_name_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_badge_name_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_name_label)

	_badge_race_label = Label.new()
	_badge_race_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_badge_race_label.add_theme_font_size_override("font_size", 15)
	_badge_race_label.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	_badge_race_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_badge_race_label.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		_badge_race_label.add_theme_font_override("font", _cached_font)
	badge_box.add_child(_badge_race_label)

	# ── 右側：控制區（種族篩選 + 七大槽位果凍色階光框列 + 挑選卡片網格 + 操作鈕）──
	var controls_vbox := VBoxContainer.new()
	controls_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL
	controls_vbox.add_theme_constant_override("separation", 6)
	main_hbox.add_child(controls_vbox)

	# 1. 頂部種族篩選 Chip 列
	var filter_bar := _create_race_filter_bar()
	controls_vbox.add_child(filter_bar)

	# 2. 七大槽位果凍厚底色階圓角光框列 (Seven Slots Bar with Real-time Sheen)
	var slots_bar := _create_seven_slots_bar()
	controls_vbox.add_child(slots_bar)

	# 3. 滾動工坊內容區：容納七大槽位部件網格
	_workshop_scroll = ScrollContainer.new()
	_workshop_scroll.name = "WorkshopScroll"
	_workshop_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_workshop_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_workshop_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	_workshop_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	controls_vbox.add_child(_workshop_scroll)

	var workshop_vbox := VBoxContainer.new()
	workshop_vbox.name = "WorkshopVBox"
	workshop_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	workshop_vbox.add_theme_constant_override("separation", 8)
	_workshop_scroll.add_child(workshop_vbox)

	# 依照順序建立七大槽位區塊 (外裝與塗裝置前，確保舊測項直接在視窗頂端抓取)
	for slot_def in SEVEN_SLOTS:
		var sid: String = str(slot_def.get("id", ""))
		var title: String = str(slot_def.get("title_zh", ""))
		var sec_panel := _create_grid_section(title, sid)
		workshop_vbox.add_child(sec_panel)
		_section_nodes[sid] = sec_panel

	# 4. 底部操作按鈕列
	var actions_hbox := HBoxContainer.new()
	actions_hbox.custom_minimum_size.y = BTN_SIZE
	actions_hbox.add_theme_constant_override("separation", 10)
	controls_vbox.add_child(actions_hbox)

	_btn_reset = Button.new()
	_btn_reset.name = "BtnReset"
	_btn_reset.text = _t("還原預設")
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
	_btn_random.text = _t("隨機")
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
	_btn_confirm.text = _t("確認換裝 · 套用新外觀")
	_btn_confirm.custom_minimum_size = Vector2(0, BTN_SIZE)
	_btn_confirm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_confirm.add_theme_font_size_override("font_size", 18)
	_btn_confirm.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		_btn_confirm.add_theme_font_override("font", _cached_font)
	_btn_confirm.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 6, 20, 2))
	var c_h := _create_button_style(Color("#6CE884"), COLOR_BORDER, 3, 20, 2)
	_btn_confirm.add_theme_stylebox_override("hover", c_h)
	_btn_confirm.add_theme_stylebox_override("pressed", c_h)
	_btn_confirm.pressed.connect(confirm_selection)
	actions_hbox.add_child(_btn_confirm)


## 建立立體溫潤木質旋轉展示台 (3D Wooden Rotating Pedestal)
func _create_pedestal_stage_control() -> Control:
	var ctrl := Control.new()
	ctrl.name = "PedestalStage"
	ctrl.set_script(load("res://scripts/ui/wardrobe_dialog.gd").PedestalDrawScript)
	return ctrl


## 建立七大槽位果凍厚底色階圓角光框列
func _create_seven_slots_bar() -> PanelContainer:
	var container := PanelContainer.new()
	container.name = "SevenSlotsContainer"
	container.add_theme_stylebox_override("panel", UiStyle.sub_panel_style(COLOR_CARD_WARM, 16))

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 6)
	margin.add_theme_constant_override("margin_right", 6)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_bottom", 6)
	container.add_child(margin)

	var hbox := HBoxContainer.new()
	hbox.name = "SlotsHBox"
	hbox.add_theme_constant_override("separation", 4)
	margin.add_child(hbox)

	_slot_btns.clear()
	_slot_sheen_nodes.clear()

	for slot_def in SEVEN_SLOTS:
		var sid: String = str(slot_def.get("id", ""))
		var sname: String = str(slot_def.get("name_zh", ""))
		var icon_path: String = str(slot_def.get("icon_asset", ""))

		var btn := Button.new()
		btn.name = "SlotBtn_" + sid
		btn.custom_minimum_size = Vector2(58, 52)
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn.focus_mode = Control.FOCUS_NONE

		# 內置垂直版面
		var btn_vbox := VBoxContainer.new()
		btn_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
		btn_vbox.add_theme_constant_override("separation", 2)
		btn_vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
		btn_vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
		btn.add_child(btn_vbox)

		# 槽位小圖示
		var icon_rect := TextureRect.new()
		icon_rect.name = "SlotIcon"
		icon_rect.custom_minimum_size = Vector2(22, 22)
		icon_rect.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		icon_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		icon_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		if ResourceLoader.exists(icon_path):
			icon_rect.texture = load(icon_path) as Texture2D
		btn_vbox.add_child(icon_rect)

		# 槽位簡稱標籤
		var lbl := Label.new()
		lbl.name = "SlotLabel"
		lbl.text = _t(sname)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		lbl.add_theme_color_override("font_outline_color", Color.WHITE)
		lbl.add_theme_constant_override("outline_size", 2)
		if _cached_font:
			lbl.add_theme_font_override("font", _cached_font)
		lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		btn_vbox.add_child(lbl)

		# 即時流光動畫覆蓋層
		var sheen := Control.new()
		sheen.name = "SheenOverlay"
		sheen.set_anchors_preset(Control.PRESET_FULL_RECT)
		sheen.mouse_filter = Control.MOUSE_FILTER_IGNORE
		sheen.set_script(load("res://scripts/ui/wardrobe_dialog.gd").SheenOverlayScript)
		btn.add_child(sheen)

		btn.pressed.connect(func():
			_select_slot_tab(sid)
		)

		hbox.add_child(btn)
		_slot_btns[sid] = btn
		_slot_sheen_nodes[sid] = sheen

	return container


## 切換當前檢視的槽位分頁
func _select_slot_tab(slot_id: String) -> void:
	active_slot_tab = slot_id
	_play_gear_click_sfx()
	_spawn_golden_stars()
	_turntable_bounce()
	_update_seven_slots_visual()
	_scroll_to_slot_section(slot_id)


## 滾動到對應槽位區塊
func _scroll_to_slot_section(slot_id: String) -> void:
	if not _section_nodes.has(slot_id) or not is_instance_valid(_workshop_scroll):
		return
	var target_node = _section_nodes[slot_id]
	if target_node is Control:
		call_deferred("_do_scroll_to_node", target_node)


func _do_scroll_to_node(ctrl: Control) -> void:
	if not is_instance_valid(_workshop_scroll) or not is_instance_valid(ctrl):
		return
	var target_y: float = ctrl.position.y
	_workshop_scroll.scroll_vertical = int(target_y)


## 取得當前槽位已裝備部件的色階顏色
func _get_equipped_item_tier_color(slot_type: String) -> Color:
	var item_id := ""
	match slot_type:
		"costume": item_id = selected_costume_id
		"chassis": item_id = selected_chassis_id
		"head_unit": item_id = selected_head_unit_id
		"winding_key": item_id = selected_winding_key_id
		"weapon": item_id = selected_weapon_id
		"optic_core": item_id = selected_optic_core_id
		"back_curio": item_id = selected_back_curio_id

	# 預設外裝、武器與發條階級
	var tier := "common"
	if item_id in ["costume_astral_cape", "costume_royal_parade", "key_starlight_cog", "wpn_anvil_greathammer", "core_astral_amethyst", "curio_floating_musicbox", "paint_brass_gold"]:
		tier = "epic"
	elif item_id in ["costume_nutcracker_guard", "costume_viking_ironclad", "key_butterfly_t", "wpn_dawn_blade", "wpn_spring_claws", "wpn_knight_lance", "wpn_astral_staff", "core_amber_sun", "core_pilot_visor", "curio_clockwork_pigeon", "paint_midnight_navy", "paint_fox_orange"]:
		tier = "rare"
	elif item_id in ["key_royal_crown", "key_winged_angel", "paint_emerald_glaze"]:
		tier = "legendary"

	match tier:
		"legendary": return COLOR_GOLD       # 燦爛金
		"epic":      return COLOR_PURPLE     # 炫彩紫
		"rare":      return COLOR_SKY        # 晴空藍
		"mythic":    return COLOR_PINK       # 珊瑚粉
		_:           return Color("#8B949E") # 金屬灰銀


## 更新七大槽位按鈕視覺樣式（果凍厚底、色階光框、即時流光）
func _update_seven_slots_visual() -> void:
	for slot_def in SEVEN_SLOTS:
		var sid: String = str(slot_def.get("id", ""))
		if not _slot_btns.has(sid):
			continue
		var btn: Button = _slot_btns[sid]
		if not is_instance_valid(btn):
			continue

		var is_active := (sid == active_slot_tab)
		var tier_color := _get_equipped_item_tier_color(sid)

		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(14)
		sb.content_margin_left = 4
		sb.content_margin_right = 4
		sb.content_margin_top = 4
		sb.content_margin_bottom = 6

		if is_active:
			sb.bg_color = COLOR_CARD_GOLD
			sb.border_color = COLOR_GOLD
			sb.set_border_width_all(2)
			sb.border_width_bottom = 6 # 果凍厚底
			sb.shadow_color = Color(1.0, 0.82, 0.18, 0.45)
			sb.shadow_size = 8
			sb.shadow_offset = Vector2(0, 3)
		else:
			sb.bg_color = COLOR_BG_CREAM
			sb.border_color = tier_color
			sb.set_border_width_all(2)
			sb.border_width_bottom = 5 # 果凍厚底
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.15)
			sb.shadow_size = 4
			sb.shadow_offset = Vector2(0, 2)

		btn.add_theme_stylebox_override("normal", sb)

		var sb_h := sb.duplicate() as StyleBoxFlat
		sb_h.bg_color = Color("#FFF9E6")
		btn.add_theme_stylebox_override("hover", sb_h)

		var sb_p := sb.duplicate() as StyleBoxFlat
		sb_p.border_width_bottom = 2
		btn.add_theme_stylebox_override("pressed", sb_p)

		# 槽位流光啟用
		if _slot_sheen_nodes.has(sid):
			var sheen: Control = _slot_sheen_nodes[sid]
			if is_instance_valid(sheen) and sheen.has_method("set_active"):
				sheen.call("set_active", is_active)


## 建立種族切換篩選列
func _create_race_filter_bar() -> PanelContainer:
	var container := PanelContainer.new()
	container.add_theme_stylebox_override("panel", UiStyle.sub_panel_style(COLOR_CARD_WARM, 16))

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 8)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_right", 8)
	margin.add_theme_constant_override("margin_bottom", 4)
	container.add_child(margin)

	var outer_hbox := HBoxContainer.new()
	outer_hbox.add_theme_constant_override("separation", 6)
	margin.add_child(outer_hbox)

	var title_lbl := Label.new()
	title_lbl.name = "FilterTitle"
	title_lbl.text = _t("外裝庫")
	title_lbl.add_theme_font_size_override("font_size", 14)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		title_lbl.add_theme_font_override("font", _cached_font)
	outer_hbox.add_child(title_lbl)
	_filter_title_lbl = title_lbl

	var chip_scroll := ScrollContainer.new()
	chip_scroll.name = "FilterScroll"
	chip_scroll.custom_minimum_size.y = 44
	chip_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	chip_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	chip_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	outer_hbox.add_child(chip_scroll)

	var hbox := HBoxContainer.new()
	hbox.name = "ChipsHBox"
	hbox.add_theme_constant_override("separation", 4)
	chip_scroll.add_child(hbox)

	_filter_chips.clear()
	for opt in RACE_FILTER_OPTIONS:
		if opt.get("hidden", false):
			continue
		var rid: String = str(opt.get("id", ""))
		if not _has_race_assets(rid):
			continue
		var rname: String = str(opt.get("name_zh", rid))
		var btn := Button.new()
		btn.name = "Chip_" + rid
		btn.text = _t(rname)
		btn.custom_minimum_size = Vector2(46, 42)
		btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		btn.add_theme_font_size_override("font_size", 14)
		if _cached_font:
			btn.add_theme_font_override("font", _cached_font)
		btn.pressed.connect(func(): set_race_filter(rid))
		hbox.add_child(btn)
		_filter_chips[rid] = btn

	var end_spacer := Control.new()
	end_spacer.name = "EndSpacer"
	end_spacer.custom_minimum_size = Vector2(8, 0)
	hbox.add_child(end_spacer)

	_update_filter_chips_visual()
	return container


func set_race_filter(race_id: String) -> void:
	if race_id != "all" and not _has_race_assets(race_id):
		return
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
	_update_seven_slots_visual()


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
	var view_w: float = hbar.page if (hbar and hbar.page > 0.0) else scroll.size.x
	var btn_left: float = btn.position.x
	var btn_right: float = btn_left + btn.size.x
	var pad: float = 24.0

	if btn_right + pad > scroll.scroll_horizontal + view_w:
		var target := int(ceil(btn_right + pad - view_w))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value - hbar.page))
		scroll.scroll_horizontal = target
	elif btn_left - pad < scroll.scroll_horizontal:
		var target := int(floor(max(0.0, btn_left - pad)))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value - hbar.page))
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
		"panda": return "熊貓"
		"fawn": return "鹿"
		"hound": return "犬"
		"owl": return "鴞"
		"cat": return "貓"
		"pangolin": return "穿山甲"
		"otter": return "海獺"
		"raccoon": return "浣熊"
		"hedgehog": return "刺蝟"
		"wolf": return "鋼狼"
		"seahorse": return "海馬"
		"kangaroo": return "袋鼠"
		"squirrel": return "松鼠"
		"salamander": return "蜥蜴"
		"viper": return "青蛇"
		"falcon": return "神隼"
		"ram": return "靈羊"
		"chameleon": return "變色龍"
		"sailfish": return "旗魚"
		"rhino": return "犀牛"
		"bat": return "蝙蝠"
		"gorilla": return "巨猩"
		"peacock": return "孔雀"
		"meerkat": return "狐獴"
		"courser": return "駿駒"
		"beaver": return "河狸"
		"stoat": return "伶鼬"
		"seal": return "海豹"
		"raven": return "渡鴉"
		"kite": return "赤鳶"
		"swan": return "天鵝"
		"bison": return "野牛"
		"gecko": return "守宮"
		"badger": return "蜜獾"
		"capybara": return "水豚"
		"woodpecker": return "啄木鳥"
		"armadillo": return "犰狳"
		"caterpillar": return "毛蟲"
		"cuttlefish": return "烏賊"
		"crab": return "石蟹"
		"camel": return "駱駝"
		"giraffe": return "長頸鹿"
		"hippo": return "河馬"
		"mole": return "鼴鼠"
		"petaurista": return "鼯鼠"
		"lynx": return "猞猁"
		"scarab": return "金龜"
		"toucan": return "巨嘴鳥"
		"walrus": return "海象"
		"takin": return "羚牛"
		"lemur": return "狐猴"
		"marmot": return "旱獺"
		"firefly": return "飛螢"
		"manta": return "蝠魟"
		"kingfisher": return "翠鳥"
		"donkey": return "頑驢"
		"scorpion": return "沙蠍"
		_: return rid


## 建立卡片網格區塊 (卡片網格＋果凍框『✓ 已選用』)
func _create_grid_section(section_title: String, slot_type: String) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.name = "Section_" + slot_type
	panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
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
	title_lbl.text = _t(section_title)
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
	tip_lbl.text = _t("點擊卡片即時預覽")
	tip_lbl.add_theme_font_size_override("font_size", 14)
	tip_lbl.add_theme_color_override("font_color", COLOR_SKY)
	tip_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	tip_lbl.add_theme_constant_override("outline_size", 2)
	if _cached_font:
		tip_lbl.add_theme_font_override("font", _cached_font)
	header_hbox.add_child(tip_lbl)

	if slot_type == "costume":
		_costume_section_title = title_lbl
		_costume_section_tip = tip_lbl
	elif slot_type == "chassis":
		_chassis_section_title = title_lbl
		_chassis_section_tip = tip_lbl

	var scroll_margin := MarginContainer.new()
	scroll_margin.name = "ScrollMargin"
	scroll_margin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll_margin.add_theme_constant_override("margin_left", 2)
	scroll_margin.add_theme_constant_override("margin_right", 8)
	scroll_margin.add_theme_constant_override("margin_top", 2)
	scroll_margin.add_theme_constant_override("margin_bottom", 4)
	vbox.add_child(scroll_margin)

	var grid := GridContainer.new()
	grid.name = "Grid" + slot_type.capitalize().replace(" ", "")
	if slot_type == "costume":
		grid.name = "GridCostume"
		_costume_grid = grid
	elif slot_type == "chassis":
		grid.name = "GridChassis"
		_chassis_grid = grid

	grid.columns = 4
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	scroll_margin.add_child(grid)

	_slot_grids[slot_type] = grid
	_slot_cards[slot_type] = []
	_displayed_items[slot_type] = []

	return panel


## 取得指定槽位之部件選項清單
func _get_raw_slot_variants(slot_type: String) -> Array[Dictionary]:
	var spec: Dictionary = PaperdollRenderer.get_spec()
	var slots: Array = spec.get("slots_architecture", {}).get("slots", [])
	for s in slots:
		if str(s.get("slot_id", "")) == slot_type:
			var vars: Array = s.get("sample_variants", [])
			var res: Array[Dictionary] = []
			for v in vars:
				res.append((v as Dictionary).duplicate())
			return res
	return []


## 重新建置全部卡片
func _rebuild_cards() -> void:
	for slot_type in _slot_grids.keys():
		var grid: GridContainer = _slot_grids[slot_type]
		if not is_instance_valid(grid):
			continue
		for c in grid.get_children():
			c.queue_free()
		_slot_cards[slot_type] = []
		_displayed_items[slot_type] = []

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
		var candidates: Array[String] = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "kangaroo", "squirrel", "salamander", "viper", "falcon", "ram", "chameleon", "sailfish", "rhino", "bat", "gorilla", "peacock", "meerkat", "courser", "beaver", "stoat", "seal", "raven", "kite", "swan", "bison", "gecko", "badger", "capybara", "woodpecker", "armadillo", "caterpillar", "cuttlefish", "crab", "camel", "giraffe", "hippo", "mole", "petaurista", "lynx", "scarab", "toucan", "walrus", "takin", "lemur", "marmot", "firefly", "manta", "kingfisher", "donkey", "scorpion"]
		for cr in candidates:
			if _has_race_assets(cr):
				target_races.append(cr)
	else:
		if _has_race_assets(current_filter_race):
			target_races = [current_filter_race]

	# 1. 建立外裝與機體塗裝
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

	_displayed_items["costume"] = _displayed_costumes
	_displayed_items["chassis"] = _displayed_chassis

	# 2. 建立其他五大槽位（頭部、武器、發條、核心、奇玩）
	for slot_def in SEVEN_SLOTS:
		var sid: String = str(slot_def.get("id", ""))
		if sid in ["costume", "chassis"]:
			continue
		var raw_vars := _get_raw_slot_variants(sid)
		var filtered_vars: Array[Dictionary] = []
		for v in raw_vars:
			var v_race: String = str(v.get("race", "universal"))
			if current_filter_race == "all" or v_race == "universal" or v_race == current_race:
				var item := v.duplicate()
				item["name_zh"] = item.get("name", item.get("name_zh", ""))
				item["race_id"] = v_race
				filtered_vars.append(item)
		_displayed_items[sid] = filtered_vars

	# 3. 實例化所有槽位之卡片
	for sid in _slot_grids.keys():
		var grid: GridContainer = _slot_grids[sid]
		var items: Array = _displayed_items[sid]
		var cards: Array[Button] = []
		for i in range(items.size()):
			var card := _create_item_card(sid, i, items[i])
			grid.add_child(card)
			cards.append(card)
		_slot_cards[sid] = cards
		if sid == "costume":
			_costume_cards = cards
		elif sid == "chassis":
			_chassis_cards = cards

	_update_card_selection_states()


## 建立單張縮圖卡片按鈕
func _create_item_card(slot_type: String, idx: int, item_data: Dictionary) -> Button:
	var btn := Button.new()
	btn.name = "Card_%s_%d" % [slot_type, idx]
	btn.custom_minimum_size = Vector2(105, 142)
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
	var item_tier: String = str(item_data.get("tier", "common"))

	# 部件縮圖
	var thumb := TextureRect.new()
	thumb.name = "Thumbnail"
	thumb.custom_minimum_size = Vector2(68, 68)
	thumb.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	thumb.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	thumb.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	thumb.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	thumb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	thumb.texture = _get_item_thumbnail(slot_type, item_id, item_race)
	vbox.add_child(thumb)

	# 部件名稱
	var name_lbl := Label.new()
	name_lbl.name = "NameLabel"
	var raw_name: String = str(item_data.get("name_zh", item_data.get("name", "")))
	name_lbl.set_meta("raw_name", raw_name)
	name_lbl.set_meta("item_race", item_race)
	name_lbl.set_meta("tier", item_tier)
	var loc_name := _t(raw_name)
	if current_filter_race == "all" and not item_race.is_empty() and item_race != "universal":
		var r_short: String = _get_race_short_name(item_race)
		name_lbl.text = "[%s] %s" % [_t(r_short), loc_name]
	else:
		name_lbl.text = loc_name
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.add_theme_font_size_override("font_size", 12)
	name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	name_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
	name_lbl.custom_minimum_size.y = 32
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

	# 點擊換裝回饋：音效、星芒、木質展示台微轉、預覽刷新
	btn.pressed.connect(func():
		_on_slot_item_selected(slot_type, idx, item_id)
	)

	return btn


## 點選任意槽位部件
func _on_slot_item_selected(slot_type: String, idx: int, item_id: String) -> void:
	match slot_type:
		"costume":
			costume_index = idx
			selected_costume_id = item_id
		"chassis":
			chassis_index = idx
			selected_chassis_id = item_id
		"head_unit":
			head_unit_index = idx
			selected_head_unit_id = item_id
		"winding_key":
			winding_key_index = idx
			selected_winding_key_id = item_id
		"weapon":
			weapon_index = idx
			selected_weapon_id = item_id
		"optic_core":
			optic_core_index = idx
			selected_optic_core_id = item_id
		"back_curio":
			back_curio_index = idx
			selected_back_curio_id = item_id

	_play_gear_click_sfx()
	_spawn_golden_stars()
	_turntable_bounce()
	_update_card_selection_states()
	_update_seven_slots_visual()
	_update_preview()
	_update_ui_texts()


## 播放金屬齒輪清脆音效回饋
func _play_gear_click_sfx() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var am = (loop as SceneTree).root.get_node_or_null("AudioManager")
		if am and am.has_method("play"):
			am.call("play", "clock", 1.25, -2.0)


## 爆發金色星芒粒子特效
func _spawn_golden_stars(instant_burst: bool = false) -> void:
	if _pedestal_stage and is_instance_valid(_pedestal_stage) and _pedestal_stage.has_method("spawn_stars"):
		_pedestal_stage.call("spawn_stars", instant_burst)


## 展示台微轉彈跳回饋
func _turntable_bounce() -> void:
	if _pedestal_stage and is_instance_valid(_pedestal_stage) and _pedestal_stage.has_method("kick_bounce"):
		_pedestal_stage.call("kick_bounce")


static func _load_texture_safe(path: String) -> Texture2D:
	if path.is_empty():
		return null
	if ResourceLoader.exists(path):
		return load(path) as Texture2D
	if FileAccess.file_exists(path):
		var img := Image.load_from_file(path)
		if img != null and not img.is_empty():
			return ImageTexture.create_from_image(img)
	return null


## 取得部件對應之縮圖貼圖
func _get_item_thumbnail(slot_type: String, item_id: String, item_race: String = "") -> Texture2D:
	var r := item_race if not item_race.is_empty() and item_race != "universal" else current_race

	if slot_type == "costume":
		if item_id in ["none", "bare", "empty"]:
			var bare_part_512 := "res://assets/sprites/player/paperdoll/%s/costume/costume_none_512.png" % r
			if not (ResourceLoader.exists(bare_part_512) or FileAccess.file_exists(bare_part_512)):
				bare_part_512 = "res://assets/sprites/player/paperdoll/%s/costume/costume_bare_512.png" % r
			if ResourceLoader.exists(bare_part_512) or FileAccess.file_exists(bare_part_512):
				return _load_texture_safe(bare_part_512)
			var bare_512 := "res://assets/sprites/player/paperdoll/%s/composite_preview_bare_512.png" % r
			if ResourceLoader.exists(bare_512) or FileAccess.file_exists(bare_512):
				return _load_texture_safe(bare_512)
			var bare_comp := PaperdollRenderer.build_composite_texture_512(r, {"costume": "none"})
			if bare_comp != null:
				return bare_comp
			return null

		var path512 := "res://assets/sprites/player/paperdoll/%s/costume/%s_512.png" % [r, item_id]
		if ResourceLoader.exists(path512) or FileAccess.file_exists(path512):
			return _load_texture_safe(path512)

		var p_common_512 := "res://assets/sprites/player/paperdoll/common/costume/%s_512.png" % item_id
		if ResourceLoader.exists(p_common_512) or FileAccess.file_exists(p_common_512):
			return _load_texture_safe(p_common_512)

		var clean_id := item_id.trim_prefix("costume_")
		var p_common_512_clean := "res://assets/sprites/player/paperdoll/common/costume/%s_512.png" % clean_id
		if ResourceLoader.exists(p_common_512_clean) or FileAccess.file_exists(p_common_512_clean):
			return _load_texture_safe(p_common_512_clean)

		var hd_cut := "res://assets/sprites/player/showcase/%s_%s_hd_cut.png" % [r, item_id]
		if ResourceLoader.exists(hd_cut) or FileAccess.file_exists(hd_cut):
			return _load_texture_safe(hd_cut)

		var all_races := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "kangaroo", "squirrel", "salamander", "viper", "falcon", "ram", "chameleon", "sailfish", "rhino", "bat", "gorilla", "peacock", "meerkat", "courser", "beaver", "stoat", "seal", "raven", "kite", "swan", "bison", "gecko", "badger", "capybara", "woodpecker", "armadillo", "caterpillar", "cuttlefish", "crab", "camel", "giraffe", "hippo", "mole", "petaurista", "lynx", "scarab", "toucan", "walrus", "takin", "lemur", "marmot", "firefly", "manta", "kingfisher", "donkey", "scorpion"]
		for other in all_races:
			if other == r:
				continue
			var cross_512 := "res://assets/sprites/player/paperdoll/%s/costume/%s_512.png" % [other, item_id]
			if ResourceLoader.exists(cross_512) or FileAccess.file_exists(cross_512):
				return _load_texture_safe(cross_512)

		return null

	elif slot_type == "chassis":
		var path512 := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [r, item_id]
		if ResourceLoader.exists(path512) or FileAccess.file_exists(path512):
			return _load_texture_safe(path512)

		var all_races := ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "tortoise", "elephant", "frog", "panda", "fawn", "hound", "owl", "cat", "pangolin", "otter", "raccoon", "hedgehog", "wolf", "seahorse", "kangaroo", "squirrel", "salamander", "viper", "falcon", "ram", "chameleon", "sailfish", "rhino", "bat", "gorilla", "peacock", "meerkat", "courser", "beaver", "stoat", "seal", "raven", "kite", "swan", "bison", "gecko", "badger", "capybara", "woodpecker", "armadillo", "caterpillar", "cuttlefish", "crab", "camel", "giraffe", "hippo", "mole", "petaurista", "lynx", "scarab", "toucan", "walrus", "takin", "lemur", "marmot", "firefly", "manta", "kingfisher", "donkey", "scorpion"]
		for other in all_races:
			if other == r:
				continue
			var cross_ch_512 := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [other, item_id]
			if ResourceLoader.exists(cross_ch_512) or FileAccess.file_exists(cross_ch_512):
				return _load_texture_safe(cross_ch_512)

		var clean_id := item_id.trim_prefix("paint_")
		for other in all_races:
			var cross_clean := "res://assets/sprites/player/paperdoll/%s/chassis/%s_512.png" % [other, clean_id]
			if ResourceLoader.exists(cross_clean) or FileAccess.file_exists(cross_clean):
				return _load_texture_safe(cross_clean)

		return null

	else:
		# 通用切片與其他五大槽位 (head_unit, winding_key, weapon, optic_core, back_curio)
		var p512 := "res://assets/sprites/player/paperdoll/%s/%s/%s_512.png" % [r, slot_type, item_id]
		if ResourceLoader.exists(p512) or FileAccess.file_exists(p512):
			return _load_texture_safe(p512)

		var p_normal := "res://assets/sprites/player/paperdoll/%s/%s/%s.png" % [r, slot_type, item_id]
		if ResourceLoader.exists(p_normal) or FileAccess.file_exists(p_normal):
			return _load_texture_safe(p_normal)

		var p_com512 := "res://assets/sprites/player/paperdoll/common/%s/%s_512.png" % [slot_type, item_id]
		if ResourceLoader.exists(p_com512) or FileAccess.file_exists(p_com512):
			return _load_texture_safe(p_com512)

		var p_com := "res://assets/sprites/player/paperdoll/common/%s/%s.png" % [slot_type, item_id]
		if ResourceLoader.exists(p_com) or FileAccess.file_exists(p_com):
			return _load_texture_safe(p_com)

		# 跨族尋找
		for other in ["rabbit", "fox", "lion", "tiger", "macaque", "crane", "bear"]:
			var cross_p := "res://assets/sprites/player/paperdoll/%s/%s/%s_512.png" % [other, slot_type, item_id]
			if ResourceLoader.exists(cross_p) or FileAccess.file_exists(cross_p):
				return _load_texture_safe(cross_p)

		return null


## 更新所有卡片的亮金邊框與『✓ 已選用』狀態
func _update_card_selection_states() -> void:
	for slot_type in _slot_cards.keys():
		var cards: Array = _slot_cards[slot_type]
		var items: Array = _displayed_items[slot_type]
		var cur_sel_id := ""
		var cur_idx := 0

		match slot_type:
			"costume":
				cur_sel_id = selected_costume_id
				cur_idx = costume_index
			"chassis":
				cur_sel_id = selected_chassis_id
				cur_idx = chassis_index
			"head_unit":
				cur_sel_id = selected_head_unit_id
				cur_idx = head_unit_index
			"winding_key":
				cur_sel_id = selected_winding_key_id
				cur_idx = winding_key_index
			"weapon":
				cur_sel_id = selected_weapon_id
				cur_idx = weapon_index
			"optic_core":
				cur_sel_id = selected_optic_core_id
				cur_idx = optic_core_index
			"back_curio":
				cur_sel_id = selected_back_curio_id
				cur_idx = back_curio_index

		for i in range(cards.size()):
			var item: Dictionary = items[i] if i < items.size() else {}
			var item_id: String = str(item.get("id", ""))
			var is_selected := false
			if not cur_sel_id.is_empty():
				if current_filter_race == "all":
					is_selected = (i == cur_idx)
				else:
					is_selected = (item_id == cur_sel_id)
			else:
				is_selected = (i == cur_idx)
			_apply_card_style(cards[i], is_selected)


## 套用單張卡片之視覺樣式
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
		sb.border_width_bottom = 3           ## 對齊規格下限 (>=3px)
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
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
		badge.text = _t("✓ 已選用") if is_selected else ""


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
	head_unit_index = 0
	winding_key_index = 0
	weapon_index = 0
	optic_core_index = 0
	back_curio_index = 0

	selected_costume_id = ""
	selected_chassis_id = ""
	selected_head_unit_id = ""
	selected_winding_key_id = ""
	selected_weapon_id = ""
	selected_optic_core_id = ""
	selected_back_curio_id = ""

	_play_gear_click_sfx()
	_turntable_bounce()
	_update_card_selection_states()
	_update_seven_slots_visual()
	_update_ui_texts()
	_update_preview()


func _on_random_pressed() -> void:
	randomize_selection()


## 隨機挑選一組外觀（在 current_filter_race 篩選範圍內，純預覽不寫存檔）
func randomize_selection() -> void:
	for slot_type in _displayed_items.keys():
		var items: Array = _displayed_items[slot_type]
		if items.is_empty():
			continue
		var rand_idx := randi() % items.size()
		var rand_id: String = str(items[rand_idx].get("id", ""))
		match slot_type:
			"costume":
				costume_index = rand_idx
				selected_costume_id = rand_id
			"chassis":
				chassis_index = rand_idx
				selected_chassis_id = rand_id
			"head_unit":
				head_unit_index = rand_idx
				selected_head_unit_id = rand_id
			"winding_key":
				winding_key_index = rand_idx
				selected_winding_key_id = rand_id
			"weapon":
				weapon_index = rand_idx
				selected_weapon_id = rand_id
			"optic_core":
				optic_core_index = rand_idx
				selected_optic_core_id = rand_id
			"back_curio":
				back_curio_index = rand_idx
				selected_back_curio_id = rand_id

	_play_gear_click_sfx()
	_spawn_golden_stars()
	_turntable_bounce()
	_update_card_selection_states()
	_update_seven_slots_visual()
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

	var c_id := selected_costume_id if not selected_costume_id.is_empty() else str(cur_costume.get("id", "none"))
	var p_id := selected_chassis_id if not selected_chassis_id.is_empty() else str(cur_chassis.get("id", "paint_ivory_stock"))

	var h_id := selected_head_unit_id if not selected_head_unit_id.is_empty() else PaperdollRenderer._get_default_variant_id(current_race, "head_unit")
	var k_id := selected_winding_key_id if not selected_winding_key_id.is_empty() else PaperdollRenderer._get_default_variant_id(current_race, "winding_key")
	var w_id := selected_weapon_id if not selected_weapon_id.is_empty() else PaperdollRenderer._get_default_variant_id(current_race, "weapon")
	var o_id := selected_optic_core_id if not selected_optic_core_id.is_empty() else PaperdollRenderer._get_default_variant_id(current_race, "optic_core")
	var b_id := selected_back_curio_id if not selected_back_curio_id.is_empty() else PaperdollRenderer._get_default_variant_id(current_race, "back_curio")

	return {
		"race": current_race,
		"costume": c_id,
		"chassis": p_id,
		"costume_id": c_id,
		"paint_id": p_id,
		"head_unit": h_id,
		"winding_key": k_id,
		"weapon": w_id,
		"optic_core": o_id,
		"back_curio": b_id
	}


func _update_ui_texts() -> void:
	if _title_label:
		_title_label.text = _t("發條衣櫥 · 英雄換裝")
	if _subtitle_label:
		_subtitle_label.text = _t("個人化外觀部件即時切換 · 零數值純視覺展示")
	if _filter_title_lbl:
		_filter_title_lbl.text = _t("外裝庫")
	if _costume_section_title:
		_costume_section_title.text = _t("外裝服飾 (Costume)")
	if _costume_section_tip:
		_costume_section_tip.text = _t("點擊卡片即時預覽")
	if _chassis_section_title:
		_chassis_section_title.text = _t("機體塗裝 (Chassis / Paint)")
	if _chassis_section_tip:
		_chassis_section_tip.text = _t("點擊卡片即時預覽")
	if _btn_reset:
		_btn_reset.text = _t("還原預設")
	if _btn_random:
		_btn_random.text = _t("隨機")
	if _btn_confirm:
		_btn_confirm.text = _t("確認換裝 · 套用新外觀")

	for opt in RACE_FILTER_OPTIONS:
		var rid: String = str(opt.get("id", ""))
		if _filter_chips.has(rid):
			var btn: Button = _filter_chips[rid]
			if is_instance_valid(btn):
				var rname: String = str(opt.get("name_zh", rid))
				btn.text = _t(rname)

	var data := _get_race_data()
	var race_name_zh := str(data.get("name_zh", current_race))
	var archetype := str(data.get("archetype", ""))

	var gs = _get_game_state()
	var p_name := "小白"
	if gs and "player_name" in gs:
		p_name = str(gs.player_name)

	if _badge_name_label:
		_badge_name_label.text = "%s" % _t(p_name)
	if _badge_race_label:
		var loc_race := _t(race_name_zh)
		var clean_arch := archetype
		if "(" in clean_arch:
			clean_arch = clean_arch.split("(")[0].strip_edges()
		var loc_arch := _t(clean_arch)
		if ContentLoc.locale() == "zh_TW":
			_badge_race_label.text = "【%s · %s】" % [race_name_zh, archetype]
		else:
			_badge_race_label.text = "【%s · %s】" % [loc_race, loc_arch]


func _update_preview() -> void:
	if _preview_rect == null:
		return
	var sel := get_current_selections()
	var anim := WindingKeyAnimator.setup_for(_preview_rect, current_race, sel)
	if anim != null and _preview_rect.texture != null:
		return
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
		gs.paperdoll_slots["head_unit"] = sel["head_unit"]
		gs.paperdoll_slots["winding_key"] = sel["winding_key"]
		gs.paperdoll_slots["weapon"] = sel["weapon"]
		gs.paperdoll_slots["optic_core"] = sel["optic_core"]
		gs.paperdoll_slots["back_curio"] = sel["back_curio"]

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


# ─────────────────────────────────────────────────────────────
# 輔助內部類別：3D立體溫潤木質旋轉展示台繪製節點 (PedestalDrawScript)
# ─────────────────────────────────────────────────────────────
class PedestalDrawScript extends Control:
	var turntable_angle: float = 0.0
	var bounce_offset: float = 0.0
	var active_stars: Array[Dictionary] = []

	func _ready() -> void:
		set_process(true)
		mouse_filter = Control.MOUSE_FILTER_IGNORE

	func _process(delta: float) -> void:
		turntable_angle = wrapf(turntable_angle + delta * 0.35, 0.0, TAU)
		# 更新活躍星芒粒子
		var i := active_stars.size() - 1
		while i >= 0:
			var st: Dictionary = active_stars[i]
			st["pos"] = Vector2(st["pos"]) + Vector2(st["vel"]) * delta
			st["rot"] = float(st["rot"]) + float(st["rot_speed"]) * delta
			st["life"] = float(st["life"]) - delta
			if float(st["life"]) <= 0.0:
				active_stars.remove_at(i)
			i -= 1
		queue_redraw()

	func kick_bounce() -> void:
		var tw := create_tween()
		bounce_offset = 0.35
		tw.tween_property(self, "bounce_offset", 0.0, 0.45).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

	func spawn_stars(instant_burst: bool = false) -> void:
		active_stars.clear()
		var w: float = size.x if size.x > 0 else custom_minimum_size.x
		var h: float = size.y if size.y > 0 else custom_minimum_size.y
		var origin := Vector2(w * 0.5, h * 0.45)

		var colors: Array[Color] = [
			Color("#FFD028"), # 金黃
			Color("#FFA010"), # 暖橘
			Color("#FFE57F"), # 香檳金
			Color("#FFFFFF"), # 晨曦白
			Color("#4ED86A"), # 薄荷綠
			Color("#38A0FF")  # 晴空藍
		]

		var star_count := 18
		for i in range(star_count):
			var angle: float = (float(i) / float(star_count)) * TAU + (randf() * 0.2 - 0.1)
			var spd: float = 65.0 + randf() * 80.0
			var dist: float = 45.0 + (i % 3) * 25.0 if instant_burst else 0.0
			var p := origin + Vector2(cos(angle), sin(angle)) * dist
			var vel := Vector2(cos(angle), sin(angle)) * spd

			active_stars.append({
				"pos": p,
				"vel": vel if not instant_burst else Vector2.ZERO,
				"rot": randf() * TAU,
				"rot_speed": randf_range(1.5, 4.0),
				"size": 14.0 + (i % 3) * 6.0,
				"color": colors[i % colors.size()],
				"life": 0.85 if not instant_burst else 999.0,
				"max_life": 0.85
			})
		queue_redraw()

	func _draw() -> void:
		var w: float = size.x if size.x > 0 else custom_minimum_size.x
		var h: float = size.y if size.y > 0 else custom_minimum_size.y
		if w <= 0 or h <= 0:
			return

		# 1. 展廳聚光光暈 (Showcase Spotlight Glow)
		var spot_center := Vector2(w * 0.5, h * 0.42)
		var spot_rx := w * 0.48
		var spot_ry := h * 0.45
		var spot_pts := PackedVector2Array()
		var spot_colors := PackedColorArray()
		spot_pts.append(spot_center)
		spot_colors.append(Color(1.0, 0.96, 0.85, 0.30))
		var segs := 36
		for i in range(segs + 1):
			var th := (float(i % segs) / float(segs)) * TAU
			spot_pts.append(spot_center + Vector2(cos(th) * spot_rx, sin(th) * spot_ry))
			spot_colors.append(Color(1.0, 0.96, 0.85, 0.0))
		draw_polygon(spot_pts, spot_colors)

		# 2. 地面環境遮蔽軟影 (Ambient Floor Shadow)
		var shadow_center := Vector2(w * 0.5, h - 36.0)
		var sh_pts := _calc_ellipse_pts(shadow_center, 98.0, 24.0, 32)
		draw_colored_polygon(sh_pts, Color(0.12, 0.08, 0.22, 0.32))

		# 3. 3D立體溫潤木質展示台 (3D Wooden Rotating Turntable)
		var center_top := Vector2(w * 0.5, h - 56.0)
		var rx := 88.0
		var ry := 24.0
		var depth := 20.0
		var center_bot := center_top + Vector2(0.0, depth)

		# 3a. 底座側身圓柱面 (3D Cylinder Side - Dark Walnut & Mahogany)
		var half_segs := 24
		for i in range(1, half_segs + 1):
			var prev_th := (float(i - 1) / float(half_segs)) * PI
			var th := (float(i) / float(half_segs)) * PI
			var p_top_prev := center_top + Vector2(cos(prev_th) * rx, sin(prev_th) * ry)
			var p_bot_prev := center_bot + Vector2(cos(prev_th) * rx, sin(prev_th) * ry)
			var pt_top := center_top + Vector2(cos(th) * rx, sin(th) * ry)
			var pt_bot := center_bot + Vector2(cos(th) * rx, sin(th) * ry)

			var center_blend := sin((prev_th + th) * 0.5)
			var col := Color("#3D1B0A").lerp(Color("#633418"), center_blend * 0.85)
			var quad := PackedVector2Array([p_top_prev, pt_top, pt_bot, p_bot_prev])
			draw_colored_polygon(quad, col)

		# 3b. 底座底緣雙重黃銅飾邊 (Brass Base Trim)
		var bot_rim_pts := _calc_arc_pts(center_bot, rx, ry, 0.0, PI, 32)
		draw_polyline(bot_rim_pts, Color("#E69A28"), 3.0)
		draw_polyline(bot_rim_pts, Color("#FFD028"), 1.2)

		# 3c. 側身立體黃銅齒輪鉚釘 (Rotating Brass Gear Rivets)
		var num_rivets := 12
		var cur_rot := turntable_angle + bounce_offset
		for r_i in range(num_rivets):
			var th := wrapf(float(r_i) / float(num_rivets) * TAU + cur_rot, 0.0, TAU)
			if th >= 0.0 and th <= PI:
				var rivet_center := center_top + Vector2(cos(th) * rx, sin(th) * ry) + Vector2(0.0, depth * 0.5)
				draw_circle(rivet_center + Vector2(0, 1), 3.2, Color("#1F1A3A"))
				draw_circle(rivet_center, 2.8, Color("#FFA010"))
				draw_circle(rivet_center, 1.8, Color("#FFD028"))
				draw_circle(rivet_center + Vector2(-0.6, -0.6), 0.8, Color("#FFFDF8"))

		# 3d. 頂部拋光溫潤木質表面 (Polished Honey Oak Turntable Top Face)
		var top_pts := _calc_ellipse_pts(center_top, rx, ry, 36)
		draw_colored_polygon(top_pts, Color("#C68642"))

		# 木紋同心年輪質感
		var ring1_pts := _calc_ellipse_pts(center_top, rx * 0.72, ry * 0.72, 32)
		draw_colored_polygon(ring1_pts, Color("#D49A58"))
		var ring2_pts := _calc_ellipse_pts(center_top, rx * 0.45, ry * 0.45, 28)
		draw_colored_polygon(ring2_pts, Color("#BA7A36"))
		var ring3_pts := _calc_ellipse_pts(center_top, rx * 0.20, ry * 0.20, 24)
		draw_colored_polygon(ring3_pts, Color("#C68642"))

		# 頂部黃銅鑲嵌雙重金邊 (Gilded Inlay Brass Rims)
		draw_polyline(top_pts, Color("#E69A28"), 3.0)
		var inner_brass_pts := _calc_ellipse_pts(center_top, rx - 2.5, ry - 1.2, 36)
		draw_polyline(inner_brass_pts, Color("#FFD028"), 1.5)

		# 3e. 角色腳底軟影 (Character Foot Shadow on Pedestal)
		var foot_sh_pts := _calc_ellipse_pts(center_top + Vector2(0.0, 2.0), 42.0, 11.0, 24)
		draw_colored_polygon(foot_sh_pts, Color(0.20, 0.12, 0.08, 0.45))

		# 4. 展廳四角巴洛克古典金邊裝飾線
		_draw_corner_filigree(w, h)

		# 5. 繪製金色星芒爆散粒子 (8-pointed Golden Starbursts)
		for st in active_stars:
			var pos: Vector2 = st["pos"]
			var sz: float = st["size"]
			var rot: float = st["rot"]
			var col: Color = st["color"]
			var alpha: float = clampf(float(st["life"]) / float(st["max_life"]), 0.0, 1.0) if float(st["life"]) <= 1.0 else 1.0
			col.a *= alpha
			_draw_golden_star(pos, sz, rot, col)

	func _draw_golden_star(p: Vector2, s: float, rot: float, c: Color) -> void:
		# 主菱形 1 (直向拉伸)
		var ray_len := s * 1.0
		var ray_thick := s * 0.22
		var p_top := p + Vector2(0, -ray_len).rotated(rot)
		var p_bot := p + Vector2(0, ray_len).rotated(rot)
		var p_left := p + Vector2(-ray_thick, 0).rotated(rot)
		var p_right := p + Vector2(ray_thick, 0).rotated(rot)
		draw_colored_polygon(PackedVector2Array([p_top, p_right, p_bot, p_left]), c)

		# 主菱形 2 (橫向拉伸)
		var p2_top := p + Vector2(-ray_len, 0).rotated(rot)
		var p2_bot := p + Vector2(ray_len, 0).rotated(rot)
		var p2_left := p + Vector2(0, -ray_thick).rotated(rot)
		var p2_right := p + Vector2(0, ray_thick).rotated(rot)
		draw_colored_polygon(PackedVector2Array([p2_top, p2_right, p2_bot, p2_left]), c)

		# 45度斜向次級星芒 (8芒立體星)
		var diag_len := s * 0.58
		var diag_thick := s * 0.14
		var d_rot := rot + PI * 0.25
		var d1_top := p + Vector2(0, -diag_len).rotated(d_rot)
		var d1_bot := p + Vector2(0, diag_len).rotated(d_rot)
		var d1_left := p + Vector2(-diag_thick, 0).rotated(d_rot)
		var d1_right := p + Vector2(diag_thick, 0).rotated(d_rot)
		draw_colored_polygon(PackedVector2Array([d1_top, d1_right, d1_bot, d1_left]), c * Color(1, 1, 1, 0.85))

		var d2_top := p + Vector2(-diag_len, 0).rotated(d_rot)
		var d2_bot := p + Vector2(diag_len, 0).rotated(d_rot)
		var d2_left := p + Vector2(0, -diag_thick).rotated(d_rot)
		var d2_right := p + Vector2(0, diag_thick).rotated(d_rot)
		draw_colored_polygon(PackedVector2Array([d2_top, d2_right, d2_bot, d2_left]), c * Color(1, 1, 1, 0.85))

		# 星芒高光晶核
		draw_circle(p, s * 0.24, Color.WHITE)

	func _draw_corner_filigree(w: float, h: float) -> void:
		var col := Color("#D4AF37", 0.55)
		var col_hi := Color("#FFD028", 0.75)
		var pad := 8.0
		var length := 16.0
		# Top-left
		draw_line(Vector2(pad, pad), Vector2(pad + length, pad), col, 2.0)
		draw_line(Vector2(pad, pad), Vector2(pad, pad + length), col, 2.0)
		draw_circle(Vector2(pad + 2, pad + 2), 2.0, col_hi)
		# Top-right
		draw_line(Vector2(w - pad, pad), Vector2(w - pad - length, pad), col, 2.0)
		draw_line(Vector2(w - pad, pad), Vector2(w - pad, pad + length), col, 2.0)
		draw_circle(Vector2(w - pad - 2, pad + 2), 2.0, col_hi)
		# Bottom-left
		draw_line(Vector2(pad, h - pad), Vector2(pad + length, h - pad), col, 2.0)
		draw_line(Vector2(pad, h - pad), Vector2(pad, h - pad - length), col, 2.0)
		draw_circle(Vector2(pad + 2, h - pad - 2), 2.0, col_hi)
		# Bottom-right
		draw_line(Vector2(w - pad, h - pad), Vector2(w - pad - length, h - pad), col, 2.0)
		draw_line(Vector2(w - pad, h - pad), Vector2(w - pad, h - pad - length), col, 2.0)
		draw_circle(Vector2(w - pad - 2, h - pad - 2), 2.0, col_hi)

	static func _calc_ellipse_pts(center: Vector2, rx: float, ry: float, segs: int) -> PackedVector2Array:
		var pts := PackedVector2Array()
		for i in range(segs):
			var th := (float(i) / float(segs)) * TAU
			pts.append(center + Vector2(cos(th) * rx, sin(th) * ry))
		pts.append(pts[0])
		return pts

	static func _calc_arc_pts(center: Vector2, rx: float, ry: float, from_th: float, to_th: float, segs: int) -> PackedVector2Array:
		var pts := PackedVector2Array()
		for i in range(segs + 1):
			var th := from_th + (float(i) / float(segs)) * (to_th - from_th)
			pts.append(center + Vector2(cos(th) * rx, sin(th) * ry))
		return pts


# ─────────────────────────────────────────────────────────────
# 輔助內部類別：槽位即時流光動畫覆蓋層 (SheenOverlayScript)
# ─────────────────────────────────────────────────────────────
class SheenOverlayScript extends Control:
	var _is_active: bool = false
	var _phase: float = 0.0

	func _ready() -> void:
		set_process(true)
		mouse_filter = Control.MOUSE_FILTER_IGNORE

	func set_active(active: bool) -> void:
		_is_active = active
		visible = active
		queue_redraw()

	func _process(delta: float) -> void:
		if not _is_active:
			return
		_phase = wrapf(_phase + delta * 0.65, 0.0, 1.0)
		queue_redraw()

	func _draw() -> void:
		if not _is_active or size.x <= 0 or size.y <= 0:
			return

		# 繪製對角微光流帶 (Diagonal Luminous Sheen)
		var total_sweep := size.x + size.y + 40.0
		var cur_x := -20.0 + _phase * total_sweep
		var sheen_w := 18.0

		var col := Color(1.0, 0.95, 0.75, 0.35)
		var pts := PackedVector2Array([
			Vector2(cur_x, 0),
			Vector2(cur_x + sheen_w, 0),
			Vector2(cur_x + sheen_w - 20, size.y),
			Vector2(cur_x - 20, size.y)
		])
		draw_colored_polygon(pts, col)
