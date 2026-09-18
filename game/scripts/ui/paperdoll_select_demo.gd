class_name PaperdollSelectDemo
extends Control
## 《發條之心》紙娃娃五族選角與即時換裝技術驗證面板 (PaperdollSelectDemo)
## 依據規格書 docs/design/paperdoll_slots.json 與手遊人體工學介面規範：
## 1. 橫向 5 大動物族縮圖按鈕（128x128 實體切片縮圖，按鈕熱區 180x108 >= 50px）。
## 2. 中央舞台顯示選取族系之 PaperdollCharacter 節點（7 大槽位疊合渲染）。
## 3. 部件槽即時換裝控制（外裝服飾 costume、機體塗裝 chassis 左右切換）。
## 4. 全程使用開源粉圓體 (OpenHuninn)，嚴禁系統 Emoji，多巴胺鮮亮高飽和配色。

signal character_confirmed(race_id: String, selections: Dictionary)
signal cancelled()

@export var creation_mode: bool = false:
	set(val):
		creation_mode = val
		_update_creation_mode_ui()

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const PaperdollCharacter = preload("res://scripts/art/paperdoll_character.gd")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")

const FONT_PATH := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## 規格書 (res://data/tables/paperdoll_slots.json) 官方部件名稱快取
static var _spec_variant_names: Dictionary = {}

static func _load_spec_names() -> void:
	if not _spec_variant_names.is_empty():
		return
	const SPEC_PATH := "res://data/tables/paperdoll_slots.json"
	if FileAccess.file_exists(SPEC_PATH):
		var file := FileAccess.open(SPEC_PATH, FileAccess.READ)
		if file != null:
			var json_str := file.get_as_text()
			var json = JSON.parse_string(json_str)
			if json is Dictionary and json.has("slots_architecture"):
				var slots: Array = json["slots_architecture"].get("slots", [])
				for slot in slots:
					var variants: Array = slot.get("sample_variants", [])
					for v in variants:
						var vid: String = str(v.get("id", ""))
						var vname: String = str(v.get("name", ""))
						if not vid.is_empty() and not vname.is_empty():
							_spec_variant_names[vid] = vname

static func get_variant_spec_name(id: String, fallback: String = "") -> String:
	_load_spec_names()
	if id == "none":
		return "無外裝 (裸機素體)"
	if _spec_variant_names.has(id):
		return str(_spec_variant_names[id])
	return fallback if not fallback.is_empty() else id

## 五大種族詳細設定與可用部件變體表
const RACES_DATA: Dictionary = {
	"rabbit": {
		"id": "rabbit",
		"name_zh": "白金兔",
		"name_en": "Whitey",
		"archetype": "劍士 (knight)",
		"thumb": "res://assets/sprites/player/showcase/rabbit_idle_hd.png",
		"desc": "發條之心的守護象徵，身形輕巧，搭載高響應晨曦核心與剛性長耳。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "經典紅藍胡桃鉗金屬禮服與黃銅肩章"},
			{"id": "costume_steam_artisan", "name_zh": "蒸氣工匠吊帶工作裝", "desc": "耐磨工匠鍛鐵胸板與工具掛扣"},
			{"id": "costume_royal_parade", "name_zh": "皇家巡遊金屬禮服", "desc": "奢華深藍金屬胸甲與雙排齒輪扣典禮禮服"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現象牙白精密機械軀體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "溫潤微光象牙白高光琺瑯塗層"},
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "古典黃銅金屬原色重拋光鏡面"},
			{"id": "paint_midnight_navy", "name_zh": "午夜深藍烤漆", "desc": "深邃暗夜深藍高光琺瑯防護塗層"}
		]
	},
	"fox": {
		"id": "fox",
		"name_zh": "靈尾狐",
		"name_en": "Fox",
		"archetype": "法師 (mage)",
		"thumb": "res://assets/sprites/player/showcase/fox_idle_hd.png",
		"desc": "掌握星軌共鳴的靈動玩具法師，具備金屬雷達耳與分節發條尾。",
		"costumes": [
			{"id": "costume_astral_cape", "name_zh": "星紋見習占星斗篷", "desc": "深藍琺瑯釉面與星芒金屬扣"},
			{"id": "costume_astral_observer", "name_zh": "星象觀測者金屬儀裝", "desc": "黃銅星軌刻盤護胸與青銅鉚釘金屬儀裝"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現曜橙靈動狐型素體"}
		],
		"chassis": [
			{"id": "paint_fox_orange", "name_zh": "靈狐曜橙烤漆", "desc": "高飽和鮮明暖橘琺瑯烤漆"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "低調優雅素體象牙白烤漆"},
			{"id": "paint_emerald_glaze", "name_zh": "翡翠螢光釉面", "desc": "翡翠深林星光微粒高光琺瑯釉面"}
		]
	},
	"lion": {
		"id": "lion",
		"name_zh": "烈鬃獅",
		"name_en": "Lion",
		"archetype": "騎士 (knight)",
		"thumb": "res://assets/sprites/player/showcase/lion_idle_hd.png",
		"desc": "恪守騎士榮譽的黃銅機甲獅，配備金色板件鬃毛與折疊尾翼。",
		"costumes": [
			{"id": "costume_nutcracker_guard", "name_zh": "胡桃鉗近衛軍裝", "desc": "典禮侍衛金屬胸甲與禮服分件"},
			{"id": "costume_steam_artisan", "name_zh": "蒸氣工匠吊帶工作裝", "desc": "工匠耐磨鍛鐵護胸吊帶與鉚釘金屬搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現全黃銅厚重鍛造素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "皇家黃金尊貴拋光金屬外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "皇家象牙白紀念版典雅塗裝"},
			{"id": "paint_midnight_navy", "name_zh": "午夜深藍烤漆", "desc": "深邃暗夜深藍高光琺瑯防護塗層"}
		]
	},
	"boar": {
		"id": "boar",
		"name_zh": "鋼牙豕",
		"name_en": "Boar",
		"archetype": "戰士 (viking)",
		"thumb": "res://assets/sprites/player/showcase/boar_idle_hd.png",
		"desc": "熔爐鐵匠鋪的重型開拓者，金屬鉚釘獠牙與強韌彈簧衝擊核心。",
		"costumes": [
			{"id": "costume_viking_harness", "name_zh": "粗獷鍛爐護胸鐵束帶", "desc": "鉚釘加固厚重鍛鐵戰士胸甲"},
			{"id": "costume_viking_ironclad", "name_zh": "維京重裝鍛鐵板甲", "desc": "耐高溫重型鍛鐵板甲與雙列鉚釘金屬護肩"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現剛硬生鐵鍛造衝擊素體"}
		],
		"chassis": [
			{"id": "paint_brass_gold", "name_zh": "黃銅原金拋光", "desc": "耐磨耐高溫黃銅金屬強化外殼"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白抗衝擊塗裝"},
			{"id": "paint_molten_crimson", "name_zh": "赤焰熔爐烤漆", "desc": "耐高溫赤焰琺瑯防護塗層"}
		]
	},
	"macaque": {
		"id": "macaque",
		"name_zh": "靈爪猴",
		"name_en": "Macaque",
		"archetype": "武術家 (monk)",
		"thumb": "res://assets/sprites/player/showcase/macaque_idle_hd.png",
		"desc": "敏捷靈活的彈簧行者，同軸金屬耳與伸縮爪刃，機巧多變。",
		"costumes": [
			{"id": "costume_dawn_monk_tunic", "name_zh": "晨曦行者武道短褂", "desc": "輕量合金武道短褂分件"},
			{"id": "costume_zen_striker", "name_zh": "天元演武者機關甲", "desc": "青古銅榫卯護胸板與天元金黃鉚釘搭扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現極簡彈簧骨架素體"}
		],
		"chassis": [
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "高韌性象牙白減震琺瑯"},
			{"id": "paint_bamboo_bronze", "name_zh": "天元青古銅烤漆", "desc": "沉穩青古銅釉面金屬板件與黃銅關節"}
		]
	},
	"tiger": {
		"id": "tiger",
		"name_zh": "烈焰虎",
		"name_en": "Tiger",
		"archetype": "忍者 (ninja)",
		"thumb": "res://assets/sprites/player/showcase/tiger_idle_hd.png",
		"desc": "赤焰熔爐淬火工坊的迅捷玩具，雙短刃高頻暴擊，散熱尾管與熔火核心。",
		"costumes": [
			{"id": "costume_ember_tunic", "name_zh": "餘燼工匠淬火戰褂", "desc": "耐高溫輕量合金戰褂分件"},
			{"id": "costume_ash_ninja_garb", "name_zh": "灰燼夜行機關裝", "desc": "曜黑輕量合金機關戰裝與黃金齒輪暗扣"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現餘燼橙紅機甲素體"}
		],
		"chassis": [
			{"id": "paint_ember_orange", "name_zh": "原廠餘燼橙紅", "desc": "高溫陽極氧化耐熱橙紅烤漆"},
			{"id": "paint_volcano_black", "name_zh": "鍛爐淬火曜黑烤漆", "desc": "曜黑高光耐熱琺瑯與暗金黃銅關節"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光琺瑯塗層"}
		]
	},
	"bear": {
		"id": "bear",
		"name_zh": "玄軸熊",
		"name_en": "Iron Bear",
		"archetype": "戰士 (viking)",
		"thumb": "res://assets/sprites/player/showcase/bear_idle_hd.png",
		"desc": "玄軸工坊重型機甲，剛毅沉穩的發條巨熊，配置重裝外殼與高扭力擺線核心。",
		"costumes": [
			{"id": "costume_ironclad_overalls", "name_zh": "玄軸工坊重裝工作吊帶甲", "desc": "耐衝擊重型鍛造吊帶金屬胸甲"},
			{"id": "costume_berserker_cuirass", "name_zh": "狂戰破陣機關戰鎧", "desc": "重裝鍛鋼胸甲、雙肩鉸鏈護肩與維京鉚釘板甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現重型鍛鐵玄軸素體"}
		],
		"chassis": [
			{"id": "paint_bear_amber", "name_zh": "原廠玄軸琥珀棕", "desc": "沉穩深琥珀琺瑯金屬烤漆"},
			{"id": "paint_iron_quarry", "name_zh": "重裝礦山玄鐵灰", "desc": "沉穩深冷礦山玄鐵高光琺瑯與黃銅球窩關節"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白抗衝擊塗裝"}
		]
	},
	"crane": {
		"id": "crane",
		"name_zh": "雲嵐鶴",
		"name_en": "Cloud Crane",
		"archetype": "遊俠 (ranger)",
		"thumb": "res://assets/sprites/player/showcase/crane_idle_hd.png",
		"desc": "雲嵐機關閣的靈巧玩具，修長纖細的流線身形，搭載輕量雙羽導流翼板與羽翼尾機關。",
		"costumes": [
			{"id": "costume_zephyr_robe", "name_zh": "凌雲羽衣輕鋼道袍", "desc": "輕合金陶瓷薄板與雙羽導流道袍"},
			{"id": "costume_sky_hunter_mail", "name_zh": "晴空巡獵機關羽甲", "desc": "高機動輕合金折疊羽甲與導風肩甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現修長流線機關素體"}
		],
		"chassis": [
			{"id": "paint_crane_porcelain", "name_zh": "原廠冷淬青瓷白", "desc": "清雅雲嵐微光白瓷高光琺瑯"},
			{"id": "paint_zephyr_azure", "name_zh": "晴空凌雲湛藍", "desc": "晴空凌雲深邃湛藍高光琺瑯烤漆"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光塗層"}
		]
	},
	"penguin": {
		"id": "penguin",
		"name_zh": "蒸氣企鵝",
		"name_en": "Steam Penguin",
		"archetype": "遊俠 (ranger)",
		"thumb": "res://assets/sprites/player/showcase/penguin_idle_hd.png",
		"desc": "淵海發條港灣的憨厚重火手，耐高壓鍍鈦燕尾裝甲與防滑金屬腳蹼。",
		"costumes": [
			{"id": "costume_navigator_harness", "name_zh": "深海導航員大衣", "desc": "耐壓鍍鈦深藍大衣與黃銅導航儀扣"},
			{"id": "costume_abyssal_diver_cuirass", "name_zh": "淵海深潛耐壓機關鎧", "desc": "重型深海耐壓合金胸甲、雙肩減壓鉸鏈閥與極地破冰鉚釘護甲"},
			{"id": "none", "name_zh": "無外裝 (裸機素體)", "desc": "卸除外裝，呈現耐壓鍍鈦企鵝素體"}
		],
		"chassis": [
			{"id": "paint_penguin_navy", "name_zh": "原廠深海鍍鈦藍", "desc": "高壓陽極氧化深海鍍鈦藍烤漆"},
			{"id": "paint_polar_frost", "name_zh": "極光冰川銀白", "desc": "極地破冰銀白高光鍍鉻烤漆與耐寒琺瑯"},
			{"id": "paint_ivory_stock", "name_zh": "原廠象牙白", "desc": "標準型象牙白高光琺瑯塗層"}
		]
	}
}

const RACE_KEYS: Array[String] = ["rabbit", "fox", "lion", "boar", "macaque", "tiger", "crane", "bear", "penguin"]

## 節點引用
@onready var character: PaperdollCharacter = $CenterStage/CharacterContainer/PaperdollCharacter as PaperdollCharacter
@onready var race_buttons_container: HBoxContainer = $TopRaceBar/ButtonsHBox as HBoxContainer

@onready var hero_title_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroTitleLabel as Label
@onready var hero_archetype_label: Label = $CenterStage/HeroBadge/Margin/HBox/HeroArchetypeLabel as Label
@onready var hero_desc_label: Label = $CenterStage/DescPanel/HeroDescLabel as Label

@onready var costume_name_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeNameLabel as Label
@onready var costume_desc_label: Label = $RightControlPanel/Margin/VBox/CostumeControl/HBox/CostumeDisplay/VBox/CostumeDescLabel as Label
@onready var btn_costume_prev: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumePrev as Button
@onready var btn_costume_next: Button = $RightControlPanel/Margin/VBox/CostumeControl/HBox/BtnCostumeNext as Button

@onready var chassis_name_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisNameLabel as Label
@onready var chassis_desc_label: Label = $RightControlPanel/Margin/VBox/ChassisControl/HBox/ChassisDisplay/VBox/ChassisDescLabel as Label
@onready var btn_chassis_prev: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisPrev as Button
@onready var btn_chassis_next: Button = $RightControlPanel/Margin/VBox/ChassisControl/HBox/BtnChassisNext as Button

@onready var weapon_name_label: Label = $RightControlPanel/Margin/VBox/WeaponControl/WeaponDisplay/WeaponNameLabel as Label

@onready var slot_summary_label: Label = $RightControlPanel/Margin/VBox/StatusCard/SlotSummaryLabel as Label
@onready var btn_reset_default: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnResetDefault as Button
@onready var btn_capture_proof: Button = $RightControlPanel/Margin/VBox/ActionsRow/BtnCaptureProof as Button

var btn_confirm: Button = null
var btn_back: Button = null

## 執行期狀態
var _current_race_id: String = "rabbit"
var _costume_index: int = 0
var _chassis_index: int = 0
var _race_buttons: Dictionary = {}
var _breathe_tween: Tween = null


var _race_filter_chips: Dictionary = {}
var _current_filter_race: String = "all"


func _ready() -> void:
	_init_race_buttons()
	_init_filter_chips()
	_bind_controls()
	_update_creation_mode_ui()
	select_race("rabbit")
	_start_breathe_tween()


func _exit_tree() -> void:
	_stop_breathe_tween()


## 初始化橫向種族選擇按鈕
func _init_race_buttons() -> void:
	var template_btn: Button = get_node_or_null("TopRaceBar/ButtonsHBox/BtnRace_rabbit") as Button
	for rid in RACE_KEYS:
		var btn_path := "TopRaceBar/ButtonsHBox/BtnRace_" + rid
		var btn: Button = get_node_or_null(btn_path) as Button
		if btn == null and race_buttons_container != null and template_btn != null:
			# 動態補足新種族按鈕
			btn = template_btn.duplicate() as Button
			btn.name = "BtnRace_" + rid
			var name_lbl = btn.get_node_or_null("Margin/VBox/NameLabel")
			if name_lbl is Label:
				name_lbl.text = str(RACES_DATA[rid].get("name_zh", rid))
			var thumb_rect = btn.get_node_or_null("Margin/VBox/Thumb")
			if thumb_rect is TextureRect:
				var thumb_path := str(RACES_DATA[rid].get("thumb", ""))
				if ResourceLoader.exists(thumb_path):
					thumb_rect.texture = load(thumb_path) as Texture2D
				else:
					thumb_rect.texture = null
			race_buttons_container.add_child(btn)
		if btn != null:
			_race_buttons[rid] = btn
			var name_lbl = btn.get_node_or_null("Margin/VBox/NameLabel")
			if name_lbl is Label:
				name_lbl.text = str(RACES_DATA[rid].get("name_zh", rid))
			var check_lbl = btn.get_node_or_null("Margin/VBox/CheckLabel")
			if check_lbl is Label:
				check_lbl.text = ""
				check_lbl.visible = false
			var thumb_rect = btn.get_node_or_null("Margin/VBox/Thumb")
			if thumb_rect is TextureRect:
				thumb_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
				var thumb_path := str(RACES_DATA[rid].get("thumb", ""))
				if ResourceLoader.exists(thumb_path):
					thumb_rect.texture = load(thumb_path) as Texture2D
				else:
					thumb_rect.texture = null
			btn.pressed.connect(func(): select_race(rid))


## 初始化頂部種族篩選 tab/chip 列
func _init_filter_chips() -> void:
	var chip_scroll: ScrollContainer = get_node_or_null("FilterScroll") as ScrollContainer
	if chip_scroll == null:
		chip_scroll = get_node_or_null("TopRaceBar/FilterScroll") as ScrollContainer
	if chip_scroll == null:
		chip_scroll = ScrollContainer.new()
		chip_scroll.name = "FilterScroll"
		chip_scroll.custom_minimum_size = Vector2(0, 56)
		chip_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
		chip_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
		chip_scroll.set_anchors_preset(Control.PRESET_TOP_WIDE)
		chip_scroll.offset_left = 40.0
		chip_scroll.offset_top = 64.0
		chip_scroll.offset_right = -40.0
		chip_scroll.offset_bottom = 120.0
		add_child(chip_scroll)

	var hbox: HBoxContainer = chip_scroll.get_node_or_null("FilterHBox") as HBoxContainer
	if hbox == null:
		hbox = HBoxContainer.new()
		hbox.name = "FilterHBox"
		hbox.add_theme_constant_override("separation", 8)
		chip_scroll.add_child(hbox)

	# 依照 0-ART10：清空既有按鈕防止重複建立
	for child in hbox.get_children():
		child.queue_free()

	# 依照 0-ART10：開端保留微小邊距
	var start_spacer := Control.new()
	start_spacer.name = "StartSpacer"
	start_spacer.custom_minimum_size = Vector2(4, 0)
	hbox.add_child(start_spacer)

	_race_filter_chips.clear()
	var filter_defs: Array[Dictionary] = [
		{"id": "all", "label": "全部"},
		{"id": "rabbit", "label": "白金兔"},
		{"id": "fox", "label": "靈尾狐"},
		{"id": "lion", "label": "烈鬃獅"},
		{"id": "boar", "label": "鋼牙豕"},
		{"id": "macaque", "label": "靈爪猴"},
		{"id": "tiger", "label": "烈焰虎"},
		{"id": "crane", "label": "雲嵐鶴"},
		{"id": "bear", "label": "玄軸熊"},
		{"id": "penguin", "label": "蒸氣企鵝"}
	]

	var font: Font = null
	if ResourceLoader.exists(FONT_PATH):
		font = load(FONT_PATH) as Font

	for def in filter_defs:
		var fid: String = def["id"]
		var flbl: String = def["label"]
		var chip := Button.new()
		chip.name = "Chip_" + fid
		chip.text = flbl
		chip.custom_minimum_size = Vector2(52, 48)
		chip.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		chip.add_theme_font_size_override("font_size", 14)
		if font:
			chip.add_theme_font_override("font", font)
		chip.pressed.connect(func(): filter_race(fid))
		hbox.add_child(chip)
		_race_filter_chips[fid] = chip

	# 依照 0-ART10：末端保留 24px 右邊距，確保最右側 chip 滾動到終點時不被容器邊界裁剪
	var end_spacer := Control.new()
	end_spacer.name = "EndSpacer"
	end_spacer.custom_minimum_size = Vector2(24, 0)
	hbox.add_child(end_spacer)

	_update_filter_chips_visual()


func filter_race(race_id: String) -> void:
	_current_filter_race = race_id
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		if _current_filter_race == "all" or rid == _current_filter_race:
			btn.visible = true
		else:
			btn.visible = false
	if race_id != "all" and RACES_DATA.has(race_id):
		select_race(race_id)
	_update_filter_chips_visual()


func _update_filter_chips_visual() -> void:
	for fid in _race_filter_chips.keys():
		var chip: Button = _race_filter_chips[fid]
		var is_active: bool = (str(fid) == _current_filter_race)
		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(14)
		sb.content_margin_left = 12
		sb.content_margin_right = 12
		sb.content_margin_top = 4
		sb.content_margin_bottom = 4
		if is_active:
			sb.bg_color = Color("#FFD028") # 金黃
			sb.border_color = Color("#FFA010") # 暖橘
			sb.set_border_width_all(2)
			sb.border_width_bottom = 4
			chip.add_theme_color_override("font_color", Color("#1F1A3A"))
		else:
			sb.bg_color = Color("#FFFDF8") # 奶油白
			sb.border_color = Color("#1F1A3A") # 深藍紫
			sb.set_border_width_all(1)
			sb.border_width_bottom = 2
			chip.add_theme_color_override("font_color", Color("#1F1A3A"))
		chip.add_theme_stylebox_override("normal", sb)
		var sb_h = sb.duplicate()
		sb_h.bg_color = Color("#FFF4D0")
		chip.add_theme_stylebox_override("hover", sb_h)
		chip.add_theme_stylebox_override("pressed", sb_h)


## 綁定控制按鈕
func _bind_controls() -> void:
	if btn_costume_prev != null:
		btn_costume_prev.pressed.connect(_on_costume_prev_pressed)
	if btn_costume_next != null:
		btn_costume_next.pressed.connect(_on_costume_next_pressed)
	if btn_chassis_prev != null:
		btn_chassis_prev.pressed.connect(_on_chassis_prev_pressed)
	if btn_chassis_next != null:
		btn_chassis_next.pressed.connect(_on_chassis_next_pressed)
	if btn_reset_default != null:
		btn_reset_default.pressed.connect(reset_to_default)
	if btn_capture_proof != null:
		btn_capture_proof.pressed.connect(func(): save_proof_screenshot())

	var actions_row = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow")
	if actions_row != null:
		btn_confirm = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnConfirm") as Button
		if btn_confirm == null:
			btn_confirm = Button.new()
			btn_confirm.name = "BtnConfirm"
			btn_confirm.custom_minimum_size = Vector2(160, 52)
			btn_confirm.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			btn_confirm.add_theme_font_size_override("font_size", 16)
			btn_confirm.add_theme_color_override("font_color", Color(0.04, 0.22, 0.08, 1.0))
			if btn_capture_proof:
				var sb = btn_capture_proof.get_theme_stylebox("normal")
				if sb:
					btn_confirm.add_theme_stylebox_override("normal", sb.duplicate())
			btn_confirm.text = "確認選擇 · 踏上旅途"
			actions_row.add_child(btn_confirm)
		btn_confirm.pressed.connect(confirm_selection)

		btn_back = get_node_or_null("RightControlPanel/Margin/VBox/ActionsRow/BtnBack") as Button
		if btn_back == null:
			btn_back = Button.new()
			btn_back.name = "BtnBack"
			btn_back.custom_minimum_size = Vector2(90, 52)
			btn_back.add_theme_font_size_override("font_size", 16)
			btn_back.add_theme_color_override("font_color", Color(0.12, 0.1, 0.22, 1.0))
			if btn_reset_default:
				var sb = btn_reset_default.get_theme_stylebox("normal")
				if sb:
					btn_back.add_theme_stylebox_override("normal", sb.duplicate())
			btn_back.text = "返回"
			btn_back.visible = creation_mode
			actions_row.add_child(btn_back)
		btn_back.pressed.connect(func(): close())


func _update_creation_mode_ui() -> void:
	if btn_confirm:
		btn_confirm.text = "確認選擇 · 踏上旅途" if creation_mode else "確認選擇"
	if btn_back:
		btn_back.visible = creation_mode
	if btn_capture_proof:
		btn_capture_proof.visible = not creation_mode


## 確認選擇並同步寫入 GameState
func confirm_selection() -> void:
	var sel := get_current_selections()
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		var gs = (loop as SceneTree).root.get_node_or_null("GameState")
		if gs:
			gs.player_race = _current_race_id
			gs.paperdoll_slots = sel
			match _current_race_id:
				"rabbit": gs.player_name = "小白"
				"lion": gs.player_name = "烈鬃獅"
				"fox": gs.player_name = "靈尾狐"
				"boar": gs.player_name = "鋼牙豕"
				"macaque": gs.player_name = "靈爪猴"
				"tiger": gs.player_name = "烈焰虎"
				"bear": gs.player_name = "玄軸熊"
				"crane": gs.player_name = "雲嵐鶴"
				"penguin": gs.player_name = "蒸氣企鵝"
				_: gs.player_name = "小白"
			if gs.has_method("equip_starter_weapon"):
				gs.call("equip_starter_weapon", _current_race_id)
	character_confirmed.emit(_current_race_id, sel)


## 選取指定種族
func select_race(race_id: String) -> void:
	if not RACES_DATA.has(race_id):
		race_id = "rabbit"
	_current_race_id = race_id
	_costume_index = 0
	_chassis_index = 0

	_update_race_buttons_visual()
	_apply_current_selections()


## 左右切換外裝
func _on_costume_prev_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index - 1 + costumes.size()) % costumes.size()
	_apply_current_selections()


func _on_costume_next_pressed() -> void:
	var costumes: Array = RACES_DATA[_current_race_id].get("costumes", [])
	if costumes.is_empty():
		return
	_costume_index = (_costume_index + 1) % costumes.size()
	_apply_current_selections()


## 左右切換塗裝
func _on_chassis_prev_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index - 1 + chassis_list.size()) % chassis_list.size()
	_apply_current_selections()


func _on_chassis_next_pressed() -> void:
	var chassis_list: Array = RACES_DATA[_current_race_id].get("chassis", [])
	if chassis_list.is_empty():
		return
	_chassis_index = (_chassis_index + 1) % chassis_list.size()
	_apply_current_selections()


## 重設為當前種族預設裝備
func reset_to_default() -> void:
	_costume_index = 0
	_chassis_index = 0
	_apply_current_selections()


## 套用並重新渲染紙娃娃
func _get_character() -> PaperdollCharacter:
	if character == null:
		character = get_node_or_null("CenterStage/CharacterContainer/PaperdollCharacter") as PaperdollCharacter
	return character

func _apply_current_selections() -> void:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])

	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}

	var selections: Dictionary = {}
	if cur_costume.has("id"):
		selections["costume"] = cur_costume["id"]
	if cur_chassis.has("id"):
		selections["chassis"] = cur_chassis["id"]

	# 驅動紙娃娃節點渲染
	var ch := _get_character()
	if ch != null:
		ch.render_character(_current_race_id, selections)

	# 中央舞台九族改讀 512 高清合成（合成失敗改讀立牌／showcase 256，不退回 128）
	_update_stage_512(selections)

	# 更新 UI 顯示文字與標記
	_update_info_ui(data, cur_costume, cur_chassis, selections)


var _sprite_512: Sprite2D = null
var force_composite_512_fail: bool = false

func _ensure_stage_sprite_512() -> void:
	if _sprite_512 != null and is_instance_valid(_sprite_512):
		return
	var ch := _get_character()
	if ch == null:
		return
	_sprite_512 = ch.get_node_or_null("Sprite512") as Sprite2D
	if _sprite_512 == null:
		_sprite_512 = Sprite2D.new()
		_sprite_512.name = "Sprite512"
		_sprite_512.centered = false
		_sprite_512.position = Vector2(-64, -120)
		_sprite_512.scale = Vector2(0.25, 0.25)
		_sprite_512.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		ch.add_child(_sprite_512)

func _update_stage_512(selections: Dictionary) -> void:
	var ch := _get_character()
	if ch == null:
		return
	_ensure_stage_sprite_512()

	var tex_512: Texture2D = null
	if not force_composite_512_fail:
		tex_512 = PaperdollRenderer.build_composite_texture_512(_current_race_id, selections)
		if tex_512 == null:
			var idle_candidate: Texture2D = SpriteDB.player_equipped_idle(_current_race_id, selections)
			if idle_candidate != null and idle_candidate.get_width() >= 256:
				tex_512 = idle_candidate

	# 合成失敗改讀官方立牌或本族 showcase idle 256，不准退回 128 模組切片 (0-ART26)
	if tex_512 == null or tex_512.get_width() < 256:
		var sc := SpriteDB.hero_showcase_hd_tex(_current_race_id)
		if sc != null and sc.get_width() >= 256:
			tex_512 = sc

	var layers := ch.get_node_or_null("Layers") as CanvasItem
	if tex_512 != null and tex_512.get_width() >= 256:
		_sprite_512.texture = tex_512
		_sprite_512.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var tw := float(tex_512.get_width())
		var th := float(tex_512.get_height())
		var s := 128.0 / tw if tw > 0.0 else 0.25
		_sprite_512.scale = Vector2(s, s)
		_sprite_512.position = Vector2(-64.0, 8.0 - th * s)
		_sprite_512.visible = true
		if layers != null:
			layers.visible = false
	else:
		_sprite_512.texture = null
		_sprite_512.visible = false
		if layers != null:
			layers.visible = false

func get_stage_texture() -> Texture2D:
	if _sprite_512 != null and _sprite_512.visible and _sprite_512.texture != null:
		return _sprite_512.texture
	return null

func get_stage_sprite_512() -> Sprite2D:
	return _sprite_512

func is_stage_512() -> bool:
	var t := get_stage_texture()
	return t != null and t.get_width() >= 256


## 更新 UI 資訊
func _update_info_ui(race_data: Dictionary, cur_costume: Dictionary, cur_chassis: Dictionary, selections: Dictionary = {}) -> void:
	var name_zh: String = str(race_data.get("name_zh", ""))
	var name_en: String = str(race_data.get("name_en", ""))
	var archetype: String = str(race_data.get("archetype", ""))
	var desc: String = str(race_data.get("desc", ""))

	if hero_title_label != null:
		hero_title_label.text = "%s (%s)" % [name_zh, name_en]
	if hero_archetype_label != null:
		if archetype == "未定案":
			hero_archetype_label.text = "【未定案】"
		elif archetype.is_empty():
			hero_archetype_label.text = ""
		else:
			hero_archetype_label.text = "【%s】" % archetype
	if hero_desc_label != null:
		hero_desc_label.text = desc

	# 外裝顯示
	if costume_name_label != null:
		var c_id := str(cur_costume.get("id", "none"))
		var c_name := get_variant_spec_name(c_id, str(cur_costume.get("name_zh", "未裝備")))
		costume_name_label.text = "%s [%s]" % [c_name, c_id]
	if costume_desc_label != null:
		costume_desc_label.text = str(cur_costume.get("desc", "標準外觀"))

	# 塗裝顯示
	if chassis_name_label != null:
		var ch_id := str(cur_chassis.get("id", "paint_ivory_stock"))
		var ch_name := get_variant_spec_name(ch_id, str(cur_chassis.get("name_zh", "原廠塗裝")))
		chassis_name_label.text = "%s [%s]" % [ch_name, ch_id]
	if chassis_desc_label != null:
		chassis_desc_label.text = str(cur_chassis.get("desc", "外殼拋光烤漆"))

	# 武器顯示
	if weapon_name_label != null:
		var default_wpn := str(PaperdollRenderer._get_default_variant_id(_current_race_id, "weapon"))
		var wpn_name := get_variant_spec_name(default_wpn, default_wpn)
		weapon_name_label.text = "%s (%s)" % [wpn_name, default_wpn]

	# 槽位總結
	if slot_summary_label != null:
		var total_slots := 7
		var loaded_count := 0
		if is_stage_512():
			var entries := PaperdollRenderer.get_sorted_slot_entries_512(_current_race_id, selections)
			for e in entries:
				var p: String = str(e.get("texture_path", ""))
				if p != "" and bool(e.get("is_loaded", false)):
					loaded_count += 1
			slot_summary_label.text = "7 大槽位狀態：512 高清合成就緒 (渲染: %d/%d)" % [loaded_count, total_slots]
		elif character != null:
			var entries := character.get_rendered_entries()
			for e in entries:
				if bool(e.get("is_loaded", false)):
					loaded_count += 1
			slot_summary_label.text = "7 大槽位狀態：全部 %d 槽疊合就緒 (載入: %d/%d)" % [entries.size(), loaded_count, entries.size()]


## 更新按鈕選取高亮樣式
const COLOR_BORDER := Color("#1F1A3A")      ## 深藍紫描邊
const COLOR_ORANGE := Color("#FFA010")      ## 暖橘選中果凍厚底
const COLOR_CARD_WARM := Color("#FFF8E7")   ## 奶油未選底
const COLOR_TEXT_DARK := Color("#1F1A3A")   ## 深色文字

func _update_race_buttons_visual() -> void:
	for rid in _race_buttons.keys():
		var btn: Button = _race_buttons[rid]
		var is_selected: bool = (rid == _current_race_id)

		# 依 review.md 31d：零系統 Emoji、零字元當圖示
		var check_lbl = btn.get_node_or_null("Margin/VBox/CheckLabel")
		if check_lbl is Label:
			check_lbl.text = ""
			check_lbl.visible = false

		var name_lbl = btn.get_node_or_null("Margin/VBox/NameLabel")
		if name_lbl is Label:
			name_lbl.text = str(RACES_DATA[rid].get("name_zh", rid))
			name_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)

		# 依日常憲法 §3 & review.md 0-QA11 / 0-UI1:
		# 未選取＝奶油卡＋深藍紫描邊底框 ≥3px (設為 4px)
		# 選中＝暖橘 #FFA010 果凍厚底 5~6px (設為 5px)
		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(16)
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		if is_selected:
			sb.bg_color = COLOR_ORANGE
			sb.border_width_bottom = 5
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
			sb.shadow_size = 6
			sb.shadow_offset = Vector2(0, 3)
		else:
			sb.bg_color = COLOR_CARD_WARM
			sb.border_width_bottom = 4
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.10)
			sb.shadow_size = 4
			sb.shadow_offset = Vector2(0, 2)

		var sb_h := sb.duplicate() as StyleBoxFlat
		sb_h.bg_color = Color("#FFB84D") if is_selected else Color("#FFF4D0")

		var sb_p := sb.duplicate() as StyleBoxFlat
		sb_p.border_width_bottom = max(1, sb.border_width_bottom - 2)

		btn.add_theme_stylebox_override("normal", sb)
		btn.add_theme_stylebox_override("hover", sb_h)
		btn.add_theme_stylebox_override("pressed", sb_p)
		btn.add_theme_stylebox_override("focus", sb)

		btn.modulate = Color.WHITE

		if is_selected:
			_scroll_to_race_btn(btn)


func _scroll_to_race_btn(btn: Button) -> void:
	call_deferred("_do_scroll_to_race_btn", btn)


func _do_scroll_to_race_btn(btn: Button) -> void:
	var scroll := get_node_or_null("TopRaceBar") as ScrollContainer
	if not scroll or not is_instance_valid(scroll) or not is_instance_valid(btn):
		return
	var hbar := scroll.get_h_scroll_bar()
	var view_w: float = scroll.size.x
	if view_w <= 0.0:
		return
	var btn_left: float = btn.position.x
	var btn_right: float = btn.position.x + btn.size.x
	var pad: float = 24.0
	if btn_right + pad > scroll.scroll_horizontal + view_w:
		var target: int = int(ceil(btn_right + pad - view_w))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value))
		scroll.scroll_horizontal = target
	elif btn_left - pad < scroll.scroll_horizontal:
		var target: int = int(floor(max(0.0, btn_left - pad)))
		if hbar:
			target = clampi(target, 0, int(hbar.max_value))
		scroll.scroll_horizontal = target


## 取得當前種族
func get_current_race() -> String:
	return _current_race_id


## 取得當前選取的部件組合
func get_current_selections() -> Dictionary:
	var data: Dictionary = RACES_DATA[_current_race_id]
	var costumes: Array = data.get("costumes", [])
	var chassis_list: Array = data.get("chassis", [])
	var cur_costume: Dictionary = costumes[_costume_index] if _costume_index < costumes.size() else {}
	var cur_chassis: Dictionary = chassis_list[_chassis_index] if _chassis_index < chassis_list.size() else {}
	return {
		"race": _current_race_id,
		"costume": cur_costume.get("id", ""),
		"chassis": cur_chassis.get("id", "")
	}


## 儲存驗證截圖
func save_proof_screenshot(target_path: String = "") -> String:
	var path := target_path
	if path == "":
		path = "res://../screenshots/proof_paperdoll_select_demo.png"

	var global_path := ProjectSettings.globalize_path(path)
	var dir_path := global_path.get_base_dir()
	if not DirAccess.dir_exists_absolute(dir_path):
		DirAccess.make_dir_recursive_absolute(dir_path)

	# 透過 Viewport 截取 1280x720 完整高畫質畫面
	var vp := get_viewport()
	if vp != null:
		var tex := vp.get_texture()
		if tex != null:
			var img := tex.get_image()
			if img != null and not img.is_empty():
				var err := img.save_png(global_path)
				if err == OK:
					print("[PaperdollSelectDemo] 成功儲存 Viewport 畫面截圖至：%s" % global_path)
					return global_path

	# Fallback: 若在無頭純合成模式，儲存中心角色合成圖
	if character != null:
		var char_path := global_path.replace(".png", "_character.png")
		if _sprite_512 != null and _sprite_512.visible and _sprite_512.texture != null:
			var img512 := _sprite_512.texture.get_image()
			if img512 != null and not img512.is_empty():
				img512.save_png(char_path)
				print("[PaperdollSelectDemo] 儲存角色 512 高清合成圖備用截圖至：%s" % char_path)
				return char_path
		character.save_composite_png(char_path)
		print("[PaperdollSelectDemo] 儲存角色合成圖備用截圖至：%s" % char_path)
		return char_path

	return ""


## 關閉面板並釋放
func close() -> void:
	_stop_breathe_tween()
	cancelled.emit()
	queue_free()


## 待機呼吸小動作 (對齊大廳／衣櫥／探索規範：scale 在 (1.03, 0.97) ↔ (0.98, 1.02)、週期約 1.1s、TRANS_SINE、loop)
func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid() and _breathe_tween.is_running():
		return
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if character:
		character.scale = Vector2.ONE
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(character, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(character, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _stop_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
		_breathe_tween = null
	if character:
		character.scale = Vector2.ONE


func is_breathe_running() -> bool:
	return _breathe_tween != null and _breathe_tween.is_valid() and _breathe_tween.is_running()

