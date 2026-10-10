class_name MobileLobby
extends Control
## 發條之心 (Clockwork Heart) - 神殿黑曜石 × 古典黃金齒輪手遊大廳
## 視覺特徵：希臘神殿石柱 + 深邃黑曜石地坪 + 古典黃金齒輪 + 白兔多姿態動態待機 (無 Emoji、無系統字型符號)

signal request_battle(mode: String)
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

class LocHelper:
	static func t(k: String) -> String:
		var loop := Engine.get_main_loop()
		if loop is SceneTree:
			var loc = (loop as SceneTree).root.get_node_or_null("Loc")
			if loc != null and loc.has_method("t"):
				return str(loc.t(k))
		return ContentLoc.text("ui", k)

const Loc = LocHelper
const FootShadowShader = preload("res://shaders/foot_shadow.gdshader")
const RimLightShader = preload("res://shaders/rim_light.gdshader")
const SpriteDB = preload("res://scripts/art/sprite_db.gd")
const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")
const WindingKeyAnimator = preload("res://scripts/art/winding_key_animator.gd")

## ── 多巴胺鮮亮色盤標準 (對齊 mobile_settings / maple_hud / review.md) ──
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
const COLOR_GOLD_DARK  := Color("#9A6B00")  ## 壓明度金強調文字
const COLOR_TEXT_ORANGE:= Color("#C2600A")  ## 壓明度暖橘（亮底文字專用）
const FONT_HUNINN      := "res://assets/fonts/jf-openhuninn-2.1.ttf"

## ── 希臘神殿 · 黑曜石 × 古典金標準色盤 (對齊 temple.css 與 docs/LOBBY_UI_REDESIGN.md) ──
const OBSIDIAN_BASE      := Color(0.043, 0.039, 0.055, 1.0)  ## #0B0A0E：黑曜石最深底色
const OBSIDIAN_CARD      := Color(0.078, 0.071, 0.094, 1.0)  ## #141218：黑曜石卡片面色
const OBSIDIAN_WARM      := Color(0.102, 0.090, 0.122, 1.0)  ## #1A171F：微溫黑曜石
const OBSIDIAN_DEEP      := Color(0.027, 0.024, 0.039, 1.0)  ## #07060A：黑曜石凹槽

const GOLD_CLASSICAL     := Color(0.831, 0.686, 0.216, 1.0)  ## #D4AF37：古典金
const GOLD_HOVER         := Color(0.941, 0.843, 0.549, 1.0)  ## #F0D78C：黃金亮色
const BRONZE_ANTIQUE     := Color(0.549, 0.416, 0.102, 1.0)  ## #8C6A1A：仿古黃銅
const BRONZE_WARM        := Color(0.769, 0.573, 0.165, 1.0)  ## #C4922A：暖古銅

const TEAL_CORE          := Color(0.243, 0.812, 0.749, 1.0)  ## #3ECFBF：以太青綠核心
const TEAL_CORE_DARK     := Color(0.122, 0.541, 0.502, 1.0)  ## #1F8A80：以太青綠暗底

const INK_IVORY          := Color(0.957, 0.922, 0.831, 1.0)  ## #F4EBD4：象牙白文字
const INK_IVORY_SOFT     := Color(0.788, 0.749, 0.659, 1.0)  ## #C9BFA8：柔和象牙白
const INK_IVORY_MUTED    := Color(0.541, 0.502, 0.439, 1.0)  ## #8A8070：弱化象牙白

const CORAL_RUST         := Color(0.769, 0.361, 0.290, 1.0)  ## #C45C4A：鐵鏽珊瑚紅
const STEEL_BLUE         := Color(0.420, 0.549, 0.682, 1.0)  ## #6B8CAE：淬火精鋼藍

const LINE_GOLD          := Color(0.831, 0.686, 0.216, 0.38) ## 金線微光邊框
const LINE_GOLD_SOFT     := Color(0.831, 0.686, 0.216, 0.18) ## 輔助分界金線

const DEFAULT_HERO_NAME: String = "新人"

enum Tab {
	VILLAGE,     ## 發條新村大廳 (主城)
	CHARACTER,   ## 角色 / 三欄武器紙娃娃
	ADVENTURE,   ## 四區出征關卡
	SOUL_HALL,   ## 聚魂殿堂 (封靈罐四階)
	BAG          ## 冒險背包
}

var _current_tab: Tab = Tab.VILLAGE

## 頂部數值標籤
var _lv_label: Label
var _name_label: Label
var _power_label: Label
var _energy_label: Label
var _gold_label: Label
var _gem_label: Label

## 容器節點
var _content_root: Control
var _village_layer: Control
var _char_layer: Control
var _adventure_layer: Control
var _soul_layer: Control
var _bag_layer: Control
var _dock_buttons: Array[Button] = []
var _hall_buttons: Array[Button] = []
var _settings_button: Button = null
var _shop_button: Button = null
var _sortie_button: Button = null
var _sortie_title_label: Label = null
var _sortie_stage_label: Label = null
var _energy_title_label: Label = null
var _gold_title_label: Label = null
var _gem_title_label: Label = null
var _hero_title_tag: Label = null
var _active_hall_index: int = -1
var _char_prev: TextureRect = null
var _equip_schematic: GridContainer = null
var _cached_font: Font = null
var _cached_hero_comp_512: Texture2D = null
var _cached_hero_comp_key: String = ""
var _bag_grid: GridContainer = null
var _bag_cells: Array = []
var _bag_ids: Array = []
var _bag_title_lbl: Label = null
var _bag_sub_lbl: Label = null
var _selected_bag_item: String = ""
var _bag_detail: RichTextLabel = null
var _bag_use_btn: Button = null
var _bag_hb_btn: Button = null
var _btn_bag_go_forge: Button = null
var _bag_tip: Label = null
var _last_bag_click_i: int = -1
var _last_bag_click_t: int = 0
var _bag_preview_row: HBoxContainer = null
var _bag_preview_frame: PanelContainer = null
var _bag_detail_icon: TextureRect = null
var _bag_detail_glyph: Label = null
var _bag_detail_name: Label = null
var _bag_detail_count: Label = null
var _bag_detail_kind: Label = null
var _core_bag_panel: PanelContainer = null
var _core_title_lbl: Label = null
var _core_empty_lbl: Label = null
var _core_cards_box: HBoxContainer = null
var _equip_panel_instance: RefCounted = null
const IdleClockworkVault = preload("res://scripts/systems/idle_clockwork_vault.gd")
var _vault_card: PanelContainer = null
var _vault_title_lbl: Label = null
var _vault_time_lbl: Label = null
var _vault_progress_fill: Panel = null
var _vault_progress_bg: PanelContainer = null
var _vault_claim_btn: Button = null

const VAULT_BUBBLE_KEY_FRAME_PATHS: Array[String] = [
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_00.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_01.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_02.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_03.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_04.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_05.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_06.png",
	"res://assets/sprites/player/paperdoll/rabbit/winding_key_frames/hero_winding_key_idle_07.png"
]
var _vault_bubble: Control = null
var _vault_bubble_btn: Button = null
var _vault_bubble_key_icon: TextureRect = null
var _vault_bubble_time_lbl: Label = null
var _vault_bubble_status_lbl: Label = null
var _vault_bubble_glow_panel: Panel = null
var _vault_bubble_key_textures: Array[Texture2D] = []
var _vault_bubble_frame_idx: int = 0
var _vault_bubble_frame_timer: float = 0.0
var _vault_bubble_float_tween: Tween = null
var _vault_bubble_glow_tween: Tween = null
var _vault_bubble_is_full_glow: bool = false
const ITEM_ICON_DIR := "res://assets/icons/items/"
static var _icon_cache: Dictionary = {}

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

## 角色動態與姿態
var _profile_avatar: TextureRect
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _hero_contact_shadow: TextureRect = null
var _hero_name_tag: Label
var _speech_bubble: PanelContainer
var _speech_label: Label
var _sortie_pulse_tween: Tween = null
const HERO_SPEECH_KEYS: Array[String] = [
	"看我的旋風斬～喝！",
	"背後的發條上得剛剛好，出發吧！",
	"聽見神殿齒輪的轉動聲了嗎？",
	"神殿的以太核心正在共鳴……",
	"隨時準備好去挑戰大首領！"
]
var _current_speech_index: int = 1
var _particles_root: Control
var _breathe_tween: Tween
var _bubble_tween: Tween
var _poke_tween: Tween
var _idle_action_timer: float = 0.0
var _is_interacting: bool = false
var enable_idle_breathing: bool = true
var enable_idle_flavor: bool = true

## ── 發條微動、浮空島呼吸與紙娃娃發條鑰匙獨立圖層 ──
var _hero_key_avatar: TextureRect = null
var _bg_rect: TextureRect = null
var _bg_tween: Tween = null
var _stage_anchor: Control = null
var _stage_tween: Tween = null
var _key_wind_tween: Tween = null
var _key_wind_timer: float = 0.0
var _key_rotation_turns: float = 0.0
var _cached_hero_body_comp_512: Texture2D = null
var _cached_hero_body_key: String = ""

const KEY_PIVOTS_320: Dictionary = {
	"rabbit": Vector2(103, 186),
	"macaque": Vector2(103, 186),
	"boar": Vector2(103, 186),
	"lion": Vector2(238, 162),
	"bear": Vector2(66, 98),
	"penguin": Vector2(52, 68),
	"tortoise": Vector2(71, 80),
	"fawn": Vector2(211, 116),
}

## 動作姿態紋理快取
var _tex_idle: Texture2D
var _tex_attack: Texture2D
var _tex_skill: Texture2D
var _tex_telegraph: Texture2D
var _tex_recover: Texture2D
var _tex_hit: Texture2D

## 聚魂殿封靈罐四階狀態
var _gourd_lit: Array[bool] = [true, false, false, false]
var _gourd_btns: Array[Button] = []
var _gourd_btn_absorb: Button = null
var _gourd_btn_draw: Button = null
var _soul_title_label: Label = null
var _soul_desc_label: Label = null

## 四地區出征
const REGION_KEYS: Array[String] = [
	"第一地區 · 閣樓與堡壘",
	"第二地區 · 白霧之地",
	"第三地區 · 道場與西林",
	"第四地區 · 潮岸與終境",
]
var _selected_region: int = 1 # 0: 閣樓與堡壘, 1: 白霧之地, 2: 道場與西林, 3: 潮岸與終境
var _stages_container: VBoxContainer
var _region_buttons: Array[Button] = []

## 出征分頁子模式：0 = 四區主線, 1 = 停擺巨偶
enum AdventureSubMode { REGIONS, COLOSSUS }
var _adventure_submode: int = AdventureSubMode.REGIONS
var _submode_bar: HBoxContainer = null
var _btn_mode_regions: Button = null
var _btn_mode_colossus: Button = null
var _reg_bar: HBoxContainer = null

## 角色分頁武器槽與戰鬥屬性
var _weapon_slot_buttons: Array[Button] = []
var _selected_weapon_slot: int = 0
var _weapon_slot_hint_label: Label = null
var _char_power_badge: Label = null
var _char_level_badge: Label = null
var _char_doll_title_label: Label = null
var _btn_skill_dialog: Button = null
var _btn_wardrobe: Button = null
var _char_weapon_title_label: Label = null
var _char_weapon_sub_label: Label = null
var _btn_change_weapon: Button = null
var _weapon_swap_dialog: Control = null
var _char_stat_title_label: Label = null
var _stat_cards: Array[PanelContainer] = []

const WEAPON_SLOT_TITLES: Array[String] = [
	"首選武器",
	"副手武器",
	"絕技武器",
]

const LINE_HITS: Dictionary = {
	"sword": "4 次打擊",
	"bow": "4 次打擊",
	"fist": "5 連擊",
	"dagger": "4 次打擊",
	"claw": "5 連擊",
	"dart": "4 次打擊",
	"spear": "3 次打擊",
	"axe": "3 次打擊",
	"hammer": "2 次打擊",
	"gun": "3 次打擊",
	"magic": "4 次打擊",
	"crystal": "4 次打擊",
}

const LINE_NAMES: Dictionary = {
	"sword": "劍",
	"spear": "長槍",
	"axe": "斧",
	"hammer": "鎚",
	"dagger": "匕首",
	"dart": "鏢",
	"fist": "拳套",
	"claw": "爪",
	"magic": "法杖",
	"crystal": "靈晶",
	"bow": "弓",
	"gun": "銃",
}

const WEAPON_SLOTS: Array[Dictionary] = [
	{
		"slot_title": "首選武器",
		"weapon_name": "鐵劍",
		"hits": "4 次打擊",
		"full_text": "首選: 鐵劍 (4次)",
		"hint": "首選武器 · 鐵劍：近身迅捷連續 4 次斬擊，戰鬥開局起手輪替順位"
	},
	{
		"slot_title": "副手武器",
		"weapon_name": "獵弓",
		"hits": "4 次打擊",
		"full_text": "副手: 獵弓 (4次)",
		"hint": "副手武器 · 獵弓：中距離精準連續 4 次射擊，壓制敵陣並牽制推進"
	},
	{
		"slot_title": "絕技武器",
		"weapon_name": "拳套",
		"hits": "5 連擊",
		"full_text": "絕技: 拳套 (5連擊)",
		"hint": "絕技武器 · 拳套：重裝近身蓄力 5 連擊，滿怒時超頻運轉爆發絕技"
	}
]

const REGION_STAGES: Array[Array] = [
	[
		{"num": "1-1", "name": "荒路哨站 · 停擺發條鼠", "type": "前哨哨衛", "cost": 1, "power": 220, "mode": "ash_rat"},
		{"num": "1-2", "name": "堡外野原 · 鉚兵哨衛", "type": "精英機關", "cost": 1, "power": 260, "mode": "road_bandit"},
		{"num": "1-3", "name": "堡壘廣場 · 發條機關偶", "type": "精英機關", "cost": 1, "power": 300, "mode": "sewer_slime"},
		{"num": "1-4", "name": "閣樓大門 · 重裝發條衛", "type": "精英機關", "cost": 1, "power": 340, "mode": "road_bandit"},
	],
	[
		{"num": "2-1", "name": "白霧外緣 · 守望機關衛", "type": "前哨哨衛", "cost": 1, "power": 380, "mode": "road_bandit"},
		{"num": "2-2", "name": "市集街道 · 潛伏機關偶", "type": "精英機關", "cost": 1, "power": 420, "mode": "road_bandit"},
		{"num": "2-3", "name": "排水管道 · 黑鏽機關偶", "type": "精英機關", "cost": 1, "power": 450, "mode": "road_bandit"},
		{"num": "2-4", "name": "聖獅內殿 · 守衛泰坦雷歐", "type": "首領部位破壞", "cost": 3, "power": 520, "mode": "leo"},
	],
	[
		{"num": "3-1", "name": "西林外緣 · 霧影機關偶", "type": "前哨哨衛", "cost": 1, "power": 560, "mode": "fog_shade"},
		{"num": "3-2", "name": "霧崖小徑 · 旋風發條偶", "type": "精英機關", "cost": 1, "power": 600, "mode": "forest_sprite"},
		{"num": "3-3", "name": "鏡廊入口 · 鐘擺守衛", "type": "精英機關", "cost": 1, "power": 640, "mode": "mirror_wraith"},
		{"num": "3-4", "name": "白霧核心 · 守衛泰坦白狐", "type": "首領部位破壞", "cost": 3, "power": 720, "mode": "fog"},
	],
	[
		{"num": "4-1", "name": "石岸潮線 · 破浪哨衛", "type": "前哨哨衛", "cost": 1, "power": 760, "mode": "coast_raider"},
		{"num": "4-2", "name": "潮岸沉船 · 舵輪機關衛", "type": "精英機關", "cost": 1, "power": 800, "mode": "wreck_captain"},
		{"num": "4-3", "name": "疤地焰徑 · 熔火發條偶", "type": "精英機關", "cost": 1, "power": 840, "mode": "scar_wisp"},
		{"num": "4-4", "name": "通天塔底 · 終境停擺核", "type": "首領部位破壞", "cost": 3, "power": 920, "mode": "demon"},
	],
]

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

static func _gs() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("GameState")
	return null

static func _get_inv_sys() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("InventorySystem")
	return null

static func _get_equip_sys() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		return (loop as SceneTree).root.get_node_or_null("EquipmentSystem")
	return null

func _get_hero_name() -> String:
	var gs := _gs()
	if gs and "player_name" in gs:
		var pname: String = str(gs.player_name).strip_edges()
		if not pname.is_empty():
			return _t(pname)
	return _t(DEFAULT_HERO_NAME)

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	if ResourceLoader.exists(FONT_HUNINN):
		_cached_font = load(FONT_HUNINN) as Font
	var inv := _get_inv_sys()
	if inv and inv.has_signal("inventory_changed"):
		inv.inventory_changed.connect(func():
			if _current_tab == Tab.BAG:
				_refresh_bag_tab(false)
		)
	var eq := _get_equip_sys()
	if eq and eq.has_signal("equipment_changed"):
		eq.equipment_changed.connect(func():
			if _current_tab == Tab.CHARACTER:
				_refresh_weapon_slot_buttons()
				_refresh_char_tab_stats(false)
				_sync_hero_weapon_paperdoll()
		)
	_load_hero_poses()
	_build_ui()
	_connect_loc_signal()
	_apply_locale_texts()
	refresh_hud()
	_switch_tab(Tab.VILLAGE)
	_refresh_dock_badges()
	var gs := _gs()
	if gs and gs.has_signal("core_drop_notify_changed"):
		gs.core_drop_notify_changed.connect(func(_val):
			_refresh_dock_badges()
		)
	call_deferred("_apply_safe")

func _exit_tree() -> void:
	var loc := _get_loc_node()
	if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
		loc.locale_changed.disconnect(_on_locale_changed)

func _get_loc_node() -> Node:
	if Engine.get_main_loop() is SceneTree:
		var st := Engine.get_main_loop() as SceneTree
		if st.root:
			return st.root.get_node_or_null("Loc")
	return null

func _connect_loc_signal() -> void:
	var loc := _get_loc_node()
	if loc and loc.has_signal("locale_changed"):
		if not loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.connect(_on_locale_changed)

func _on_locale_changed(_new_locale: String = "") -> void:
	_apply_locale_texts()

func _apply_safe() -> void:
	ResponsiveUi.apply_safe_margins(self)

func _get_hero_portrait(race: String) -> Texture2D:
	var r := race.to_lower().strip_edges()
	var p_path := ""
	match r:
		"rabbit": p_path = "res://assets/sprites/portraits/rabbit_hd.png"
		"fox": p_path = "res://assets/sprites/portraits/fox_mage.png"
		"lion": p_path = "res://assets/sprites/portraits/lion_knight.png"
		"boar": p_path = "res://assets/sprites/portraits/boar_warrior.png"
		"macaque": p_path = "res://assets/sprites/portraits/macaque.png"
		"tiger": p_path = "res://assets/sprites/portraits/tiger.png"
		"crane": p_path = "res://assets/sprites/portraits/crane.png"
		"bear": p_path = "res://assets/sprites/portraits/bear.png"
		"tortoise": p_path = "res://assets/sprites/portraits/tortoise.png"
		"elephant": p_path = "res://assets/sprites/portraits/elephant.png"
		"frog": p_path = "res://assets/sprites/portraits/frog.png"
		"panda": p_path = "res://assets/sprites/portraits/panda.png"
		"fawn": p_path = "res://assets/sprites/portraits/fawn.png"
		_: p_path = "res://assets/sprites/portraits/rabbit.png"
	if ResourceLoader.exists(p_path):
		return load(p_path) as Texture2D
	return SpriteDB.player_race_composite(r)


func _get_hero_equipped_idle_texture() -> Texture2D:
	var gs := _gs()
	var race := "rabbit"
	var slots: Dictionary = {}
	if gs and "player_race" in gs:
		race = str(gs.player_race).strip_edges().to_lower()
		if race.is_empty():
			race = "rabbit"
	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		slots = (gs.paperdoll_slots as Dictionary).duplicate()
	if not slots.has("weapon") or str(slots["weapon"]).is_empty():
		if gs and "equip_slots" in gs and gs.equip_slots is Dictionary:
			var wuid: String = str(gs.equip_slots.get("weapon", ""))
			if wuid != "" and "equip_worn" in gs and gs.equip_worn is Dictionary and gs.equip_worn.has(wuid):
				var winst: Dictionary = gs.equip_worn[wuid]
				var base_id: String = str(winst.get("base_id", winst.get("id", "")))
				if base_id != "":
					slots["weapon"] = base_id
	var tex: Texture2D = SpriteDB.player_equipped_idle(race, slots)
	if tex == null:
		tex = SpriteDB.player_idle()
	return tex


func _has_custom_paperdoll_outfit(slots: Dictionary) -> bool:
	if slots.is_empty():
		return false
	for k in slots:
		if k == "race":
			continue
		var v := str(slots[k]).strip_edges().to_lower()
		if not v.is_empty() and not v in ["none", "empty", "bare", "default"]:
			return true
	return false


func _hero_showcase_hd_tex(race: String) -> Texture2D:
	var p := "res://assets/sprites/player/showcase/%s_idle_hd.png" % race
	if ResourceLoader.exists(p):
		return load(p) as Texture2D
	var p256 := "res://assets/sprites/player/paperdoll/%s/showcase_idle_256.png" % race
	if ResourceLoader.exists(p256):
		return load(p256) as Texture2D
	var p512 := "res://assets/sprites/player/paperdoll/%s/proof_paperdoll_%s_composite_512.png" % [race, race]
	if ResourceLoader.exists(p512):
		return load(p512) as Texture2D
	return null


func _hero_display_tex() -> Texture2D:
	## 大廳／角色分頁：全面優先串接 PaperdollRenderer 512 高清即時外裝合成
	var race := _current_race()
	var slots := _current_paperdoll_slots()
	var cache_key := "%s:%s" % [race, str(slots)]
	if _cached_hero_comp_512 != null and _cached_hero_comp_key == cache_key:
		return _cached_hero_comp_512

	# 1. 優先嘗試 512 高清即時外裝合成（白兔預設具備全套胡桃鉗外裝與背插發條等 7 大槽位）
	var comp_512: Texture2D = PaperdollRenderer.build_composite_texture_512(race, slots)
	if comp_512 != null:
		_cached_hero_comp_512 = comp_512
		_cached_hero_comp_key = cache_key
		return comp_512

	# 2. 自訂外裝指定切片 fallback
	var costume := str(slots.get("costume", slots.get("costume_id", ""))).strip_edges()
	if not costume.is_empty():
		var hd_cut := "res://assets/sprites/player/showcase/%s_%s_hd_cut.png" % [race, costume]
		if ResourceLoader.exists(hd_cut):
			return load(hd_cut) as Texture2D

	# 3. 官方展示立牌 fallback (>=256)，不准退回 128 糊圖
	var sc := _hero_showcase_hd_tex(race)
	if sc != null:
		return sc
	return _tex_idle


func _hero_body_display_tex() -> Texture2D:
	var race := _current_race()
	var slots := _current_paperdoll_slots()
	var cache_key := "%s:%s" % [race, str(slots)]
	if _cached_hero_body_comp_512 != null and _cached_hero_body_key == cache_key:
		return _cached_hero_body_comp_512
	var slots_no_key := slots.duplicate()
	slots_no_key["winding_key"] = "none"
	var comp := PaperdollRenderer.build_composite_texture_512(race, slots_no_key)
	if comp != null:
		_cached_hero_body_comp_512 = comp
		_cached_hero_body_key = cache_key
		return comp
	return null


func _get_hero_key_tex(race: String, slots: Dictionary) -> Texture2D:
	var chosen_item := str(slots.get("winding_key", ""))
	var p512 := PaperdollRenderer.resolve_slot_texture_path_512(race, "winding_key", chosen_item)
	if p512 != "":
		if ResourceLoader.exists(p512):
			return load(p512) as Texture2D
		elif FileAccess.file_exists(p512):
			var img := Image.load_from_file(ProjectSettings.globalize_path(p512))
			if img and not img.is_empty():
				return ImageTexture.create_from_image(img)
	return null


func _apply_hero_idle_visual() -> void:
	var race := _current_race()
	var slots := _current_paperdoll_slots()
	var hd: Texture2D = _hero_display_tex()
	if hd == null or hd.get_width() < 256:
		var sc := _hero_showcase_hd_tex(race)
		if sc != null and sc.get_width() >= 256:
			hd = sc
		else:
			hd = null

	if _hero_avatar:
		var anim := WindingKeyAnimator.setup_for(_hero_avatar, race, slots)
		var k_child := _hero_avatar.get_node_or_null("HeroWindingKey") as TextureRect
		if k_child:
			_hero_key_avatar = k_child
			if _hero_key_avatar.material == null:
				var key_rim_mat := ShaderMaterial.new()
				key_rim_mat.shader = RimLightShader
				key_rim_mat.set_shader_parameter("outline_color", Color(0.22, 0.14, 0.09, 1.0))
				key_rim_mat.set_shader_parameter("outline_width", 2.2)
				key_rim_mat.set_shader_parameter("outline_enabled", true)
				key_rim_mat.set_shader_parameter("rim_enabled", true)
				key_rim_mat.set_shader_parameter("rim_color", Color(1.0, 0.85, 0.28, 1.0))
				key_rim_mat.set_shader_parameter("rim_width", 5.0)
				key_rim_mat.set_shader_parameter("rim_intensity", 1.8)
				key_rim_mat.set_shader_parameter("rim_direction", Vector2(0.15, -0.95))
				_hero_key_avatar.material = key_rim_mat
		if anim == null or _hero_avatar.texture == null:
			if hd != null and hd.get_width() >= 256:
				_hero_avatar.texture = hd
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			else:
				_hero_avatar.texture = null

	if _char_prev:
		var anim_char := WindingKeyAnimator.setup_for(_char_prev, race, slots)
		if anim_char == null or _char_prev.texture == null:
			if hd != null and hd.get_width() >= 256:
				_char_prev.texture = hd
				_char_prev.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			else:
				_char_prev.texture = null
	_refresh_equip_schematic()


func _current_race() -> String:
	var gs := _gs()
	var race := "rabbit"
	if gs and "player_race" in gs:
		race = str(gs.player_race).strip_edges().to_lower()
		if race.is_empty():
			race = "rabbit"
	return race


func _current_paperdoll_slots() -> Dictionary:
	var gs := _gs()
	var slots: Dictionary = {}
	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		slots = (gs.paperdoll_slots as Dictionary).duplicate()
	return slots


func _variant_display_name(slot_id: String, item_id: String) -> String:
	var iid := item_id.strip_edges()
	if iid.is_empty() or iid in ["none", "empty", "bare"]:
		return _t("未裝備")
	var def: Dictionary = PaperdollRenderer.get_slot_def(slot_id)
	var variants: Variant = def.get("sample_variants", [])
	if variants is Array:
		for v in variants:
			if v is Dictionary and str(v.get("id", "")) == iid:
				var n := str(v.get("name", "")).strip_edges()
				if n != "":
					return _t(n)
	var clean := iid
	for pfx in ["wpn_", "costume_", "key_", "curio_", "paint_", "ear_", "core_"]:
		if clean.begins_with(pfx):
			clean = clean.trim_prefix(pfx)
			break
	return _t(clean.replace("_", " "))


func _refresh_equip_schematic() -> void:
	if _equip_schematic == null:
		return
	for c in _equip_schematic.get_children():
		_equip_schematic.remove_child(c)
		c.queue_free()
	var race := _current_race()
	var slots := _current_paperdoll_slots()
	var entries: Array = PaperdollRenderer.get_sorted_slot_entries(race, slots)
	var want := ["costume", "weapon", "winding_key", "back_curio"]
	for sid in want:
		var entry: Dictionary = {}
		for e in entries:
			if e is Dictionary and str(e.get("slot_id", "")) == sid:
				entry = e
				break
		var slot_title := str(entry.get("name_zh", sid))
		if slot_title == "玩具外裝與服飾":
			slot_title = _t("外裝")
		elif slot_title == "手持武器外觀":
			slot_title = _t("武器")
		elif slot_title == "背部發條鑰匙":
			slot_title = _t("發條")
		elif slot_title == "隨身奇玩與尾部機關":
			slot_title = _t("奇玩")
		else:
			slot_title = _t(slot_title)
		var item_id := str(entry.get("chosen_item", ""))
		if item_id.strip_edges().is_empty():
			var tpath := str(entry.get("texture_path", ""))
			item_id = tpath.get_file().get_basename()
		var item_name := _variant_display_name(sid, item_id)
		var tex: Texture2D = entry.get("texture", null)
		_add_equip_chip(_equip_schematic, slot_title, item_name, tex, sid)


func _add_equip_chip(parent: Container, slot_title: String, item_name: String, tex: Texture2D, sid: String = "") -> void:
	var btn := Button.new()
	btn.name = "EquipSlot_" + sid if sid != "" else ("EquipSlot_" + slot_title)
	btn.custom_minimum_size = Vector2(114, 82)
	btn.focus_mode = Control.FOCUS_NONE
	btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	btn.tooltip_text = "%s: %s" % [slot_title, item_name]

	# 蒸汽發條金屬板件底色與發條品質強調色
	var bg_color := Color(0.12, 0.09, 0.16, 0.82)
	var accent_color := Color("#D4AF37")
	if sid == "costume" or slot_title in ["外裝", "Outfit", "衣装"]:
		bg_color = Color(0.18, 0.10, 0.14, 0.85) # 蒸氣珊瑚深金屬底
		accent_color = Color("#FF7A59")
	elif sid == "weapon" or slot_title in ["武器", "Weapon"]:
		bg_color = Color(0.18, 0.14, 0.08, 0.85) # 琥珀金屬深底
		accent_color = Color("#FFA010")
	elif sid == "winding_key" or slot_title in ["發條", "Clockwork", "ゼンマイ"]:
		bg_color = Color(0.16, 0.13, 0.08, 0.85) # 發條黃銅深金屬底
		accent_color = Color("#D4AF37")
	elif sid == "back_curio" or slot_title in ["奇玩", "Curio", "骨董品"]:
		bg_color = Color(0.08, 0.15, 0.16, 0.85) # 以太奇玩青綠金屬底
		accent_color = Color("#3ECFBF")

	# 立體果凍厚底 (6px) + 深藍紫描邊 (#1F1A3A)
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg_color
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 6
	sb.set_corner_radius_all(18)
	sb.shadow_color = Color(0.08, 0.06, 0.16, 0.30)
	sb.shadow_size = 8
	sb.shadow_offset = Vector2(0, 4)
	btn.add_theme_stylebox_override("normal", sb)

	var sb_h := sb.duplicate() as StyleBoxFlat
	sb_h.bg_color = bg_color.lightened(0.15)
	sb_h.border_color = accent_color
	btn.add_theme_stylebox_override("hover", sb_h)

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2
	sb_p.shadow_size = 3
	sb_p.shadow_offset = Vector2(0, 1)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb_h)

	# 內嵌黃銅金屬邊框 (Inner metallic brass bevel)
	var inner_rim := Panel.new()
	inner_rim.set_anchors_preset(Control.PRESET_FULL_RECT)
	inner_rim.offset_left = 3
	inner_rim.offset_top = 3
	inner_rim.offset_right = -3
	inner_rim.offset_bottom = -7
	inner_rim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var isb := StyleBoxFlat.new()
	isb.draw_center = false
	isb.border_color = accent_color.lerp(Color(0.83, 0.68, 0.22), 0.5)
	isb.set_border_width_all(1)
	isb.set_corner_radius_all(15)
	inner_rim.add_theme_stylebox_override("panel", isb)
	btn.add_child(inner_rim)

	# 內容垂直排列容器
	var vbox := VBoxContainer.new()
	vbox.set_anchors_preset(Control.PRESET_FULL_RECT)
	vbox.offset_left = 6
	vbox.offset_top = 6
	vbox.offset_right = -6
	vbox.offset_bottom = -10
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.add_theme_constant_override("separation", 2)
	vbox.mouse_filter = Control.MOUSE_FILTER_IGNORE
	btn.add_child(vbox)

	# 1. 槽位精巧標籤 (外裝 / 武器 / 發條 / 奇玩)
	var badge := PanelContainer.new()
	badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = accent_color.lerp(Color(0.12, 0.10, 0.16), 0.5)
	bsb.border_color = Color(0.83, 0.68, 0.22, 0.70)
	bsb.set_border_width_all(1)
	bsb.set_corner_radius_all(8)
	bsb.content_margin_left = 8
	bsb.content_margin_right = 8
	bsb.content_margin_top = 1
	bsb.content_margin_bottom = 2
	badge.add_theme_stylebox_override("panel", bsb)
	badge.size_flags_horizontal = Control.SIZE_SHRINK_CENTER

	var badge_lbl := Label.new()
	badge_lbl.text = slot_title
	if _cached_font:
		badge_lbl.add_theme_font_override("font", _cached_font)
	badge_lbl.add_theme_font_size_override("font_size", 11)
	badge_lbl.add_theme_color_override("font_color", Color("#FFFDF8"))
	badge_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	badge_lbl.add_theme_constant_override("outline_size", 1)
	badge.add_child(badge_lbl)
	vbox.add_child(badge)

	# 2. 裝備 Icon 圖示區
	var icon_box := Control.new()
	icon_box.custom_minimum_size = Vector2(0, 36)
	icon_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(icon_box)

	var icon_rect := TextureRect.new()
	icon_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	icon_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if sid == "winding_key":
		_load_vault_bubble_key_textures()
		if not _vault_bubble_key_textures.is_empty():
			icon_rect.texture = _vault_bubble_key_textures[0]
		elif tex != null:
			icon_rect.texture = tex
	elif tex != null:
		icon_rect.texture = tex
	icon_box.add_child(icon_rect)

	# 3. 裝備名稱 (縮略單行)
	var name_lbl := Label.new()
	name_lbl.text = item_name
	if _cached_font:
		name_lbl.add_theme_font_override("font", _cached_font)
	name_lbl.add_theme_font_size_override("font_size", 11)
	name_lbl.add_theme_color_override("font_color", Color("#FFFDF8"))
	name_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	name_lbl.add_theme_constant_override("outline_size", 2)
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_lbl.clip_text = true
	name_lbl.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	name_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vbox.add_child(name_lbl)

	# 保持 Button.text 相容性（供 i18n 測試與無障礙讀取），文字透明不干擾自定義排版
	btn.text = "%s  %s" % [slot_title, item_name]
	btn.add_theme_color_override("font_color", Color(0, 0, 0, 0))
	btn.add_theme_color_override("font_pressed_color", Color(0, 0, 0, 0))
	btn.add_theme_color_override("font_hover_color", Color(0, 0, 0, 0))
	btn.add_theme_color_override("font_focus_color", Color(0, 0, 0, 0))
	btn.add_theme_constant_override("outline_size", 0)

	btn.pressed.connect(func(): open_wardrobe())
	parent.add_child(btn)


func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if _hero_avatar:
		_hero_avatar.scale = Vector2.ONE
	if _hero_shadow:
		_hero_shadow.scale = Vector2.ONE
	if _hero_contact_shadow:
		_hero_contact_shadow.scale = Vector2.ONE
	if not enable_idle_breathing:
		return
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_contact_shadow:
		_breathe_tween.parallel().tween_property(_hero_contact_shadow, "scale", Vector2(1.02, 0.98), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_contact_shadow:
		_breathe_tween.parallel().tween_property(_hero_contact_shadow, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _start_sortie_glow_tween() -> void:
	if _sortie_pulse_tween and _sortie_pulse_tween.is_valid():
		_sortie_pulse_tween.kill()
	if _sortie_button == null or not is_instance_valid(_sortie_button):
		return
	_sortie_button.pivot_offset = Vector2(140, 32)
	_sortie_button.scale = Vector2.ONE
	var sb := _sortie_button.get_theme_stylebox("normal") as StyleBoxFlat
	if sb == null:
		return
	_sortie_pulse_tween = create_tween().set_loops()
	_sortie_pulse_tween.tween_property(_sortie_button, "scale", Vector2(1.022, 1.022), 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_sortie_pulse_tween.parallel().tween_property(sb, "shadow_size", 16, 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_sortie_pulse_tween.parallel().tween_property(sb, "shadow_color", Color(1.0, 0.82, 0.18, 0.70), 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_sortie_pulse_tween.tween_property(_sortie_button, "scale", Vector2(1.0, 1.0), 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_sortie_pulse_tween.parallel().tween_property(sb, "shadow_size", 8, 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_sortie_pulse_tween.parallel().tween_property(sb, "shadow_color", Color(0.83, 0.68, 0.22, 0.35), 1.0).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _restore_hero_idle() -> void:
	_tex_idle = _get_hero_equipped_idle_texture()
	_apply_hero_idle_visual()
	if _hero_avatar:
		_hero_avatar.position = Vector2(-160, -150)
		_hero_avatar.scale = Vector2.ONE
	if _speech_bubble:
		_speech_bubble.visible = false
	_is_interacting = false
	_start_breathe_tween()


func _load_hero_poses() -> void:
	_cached_hero_comp_512 = null
	_cached_hero_comp_key = ""
	_cached_hero_body_comp_512 = null
	_cached_hero_body_key = ""
	var gs := _gs()
	var race := "rabbit"
	if gs and "player_race" in gs:
		race = str(gs.player_race).strip_edges().to_lower()
		if race.is_empty():
			race = "rabbit"

	_tex_idle = _get_hero_equipped_idle_texture()
	_tex_attack = SpriteDB.player_pose("attack", race)
	_tex_skill = SpriteDB.player_pose("skill", race)
	_tex_telegraph = SpriteDB.player_pose("telegraph", race)
	_tex_recover = SpriteDB.player_pose("recover", race)
	_tex_hit = SpriteDB.player_pose("hit", race)

	# 0-ART26 / 0-QA22: 動作姿態貼圖寬度必須 >= 256，否則視為無效，絕不退回 128 糊圖
	if _tex_attack != null and _tex_attack.get_width() < 256:
		_tex_attack = null
	if _tex_skill != null and _tex_skill.get_width() < 256:
		_tex_skill = null
	if _tex_telegraph != null and _tex_telegraph.get_width() < 256:
		_tex_telegraph = null
	if _tex_recover != null and _tex_recover.get_width() < 256:
		_tex_recover = null
	if _tex_hit != null and _tex_hit.get_width() < 256:
		_tex_hit = null

	if _tex_idle == null:
		_tex_idle = SpriteDB.player_idle()

	if _hero_avatar and _tex_idle and not _is_interacting:
		_apply_hero_idle_visual()
	elif _char_prev and _tex_idle:
		_apply_hero_idle_visual()

static var _shadow_tex_cache: Texture2D = null

static func _soft_shadow_tex() -> Texture2D:
	if _shadow_tex_cache != null:
		return _shadow_tex_cache
	## 寬核平台＋柔邊：核接近不透明，邊緣才衰減（review.md 第 16 條 / 腳底軟影）
	var w := 256
	var h := 96
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	var cx := (w - 1) * 0.5
	var cy := (h - 1) * 0.5
	var rx := cx * 0.98
	var ry := cy * 0.96
	for y in h:
		for x in w:
			var dx := (float(x) - cx) / rx
			var dy := (float(y) - cy) / ry
			var d2 := dx * dx + dy * dy
			if d2 >= 1.0:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
			else:
				var d := sqrt(d2)
				var a := 1.0
				if d > 0.40:
					var t := (d - 0.40) / 0.60
					t = t * t * (3.0 - 2.0 * t)
					a = 1.0 - t
				img.set_pixel(x, y, Color(1, 1, 1, a))
	_shadow_tex_cache = ImageTexture.create_from_image(img)
	return _shadow_tex_cache

func _build_ui() -> void:
	if _content_root != null:
		return
	## 1. 背景插畫（陽光浮空島天空王國 / LINEAR 平滑採樣）
	var bg := TextureRect.new()
	bg.name = "TempleLobbyBg"
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.offset_left = -8
	bg.offset_right = 8
	bg.offset_top = -8
	bg.offset_bottom = 8
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	
	var sky_path := "res://assets/sprites/maps/sky_kingdom_bg.png"
	var abs_sky_path := ProjectSettings.globalize_path(sky_path)
	if FileAccess.file_exists(abs_sky_path):
		var img := Image.load_from_file(abs_sky_path)
		if img and not img.is_empty():
			bg.texture = ImageTexture.create_from_image(img)
	if bg.texture == null and ResourceLoader.exists(sky_path):
		bg.texture = load(sky_path)
	elif bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/temple_lobby_bg.png"):
		bg.texture = load("res://assets/sprites/maps/temple_lobby_bg.png")
	elif bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	add_child(bg)
	_bg_rect = bg
	_start_bg_floating_tween()

	## 2. 飄散的黃金以太塵埃微光粒子 (Golden Ether Motes)
	_particles_root = Control.new()
	_particles_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_particles_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_particles_root)
	_spawn_floating_ether_motes()

	## 3. 內容掛載層
	_content_root = Control.new()
	_content_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.offset_top = 80
	_content_root.offset_bottom = -90
	add_child(_content_root)

	_build_village_tab()
	_build_character_tab()
	_build_adventure_tab()
	_build_soul_hall_tab()
	_build_bag_tab()

	## 4. 頂部狀態列 (神殿黑曜石 HUD，無 Emoji、無符號)
	_build_top_hud()

	## 5. 底部黑曜石神殿導航欄 (無 Emoji、無符號，古典黃金雕飾)
	_build_bottom_dock()

## ──────────────────────────────────────────
## 通用多巴胺奶油白面板 (Cream Dopamine Panel)
## ──────────────────────────────────────────
func _create_obsidian_panel(accent: Color = COLOR_BORDER) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(1.0, 0.956, 0.815, 0.90)  ## 暖金奶油半透明，避免死白 PPT 橫條
	s.border_color = accent
	s.set_border_width_all(2)
	s.border_width_bottom = 5
	s.set_corner_radius_all(20)
	s.content_margin_left = 20
	s.content_margin_right = 20
	s.content_margin_top = 16
	s.content_margin_bottom = 16
	s.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	s.shadow_size = 10
	s.shadow_offset = Vector2(0, 4)
	return s


func _create_banner_panel() -> StyleBoxFlat:
	## 頂欄／底 Dock 大橫條：蒸汽發條暖金玻璃，讓神殿背景透出來
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.98, 0.92, 0.80, 0.72)
	s.border_color = Color(0.83, 0.68, 0.22, 0.85)
	s.set_border_width_all(2)
	s.border_width_bottom = 5
	s.set_corner_radius_all(20)
	s.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
	s.shadow_size = 8
	s.shadow_offset = Vector2(0, 3)
	return s

func _start_bg_floating_tween() -> void:
	if _bg_tween and _bg_tween.is_valid():
		_bg_tween.kill()
	if _bg_rect == null or not is_instance_valid(_bg_rect):
		return
	_bg_rect.position.y = 0.0
	_bg_rect.position.x = 0.0
	_bg_tween = create_tween().set_loops()
	## 天宮遠景背景視差浮動：長週期 (5.6s) 悠揚平滑 Sine 呼吸浮動 (y: ±2.2px, x: ±1.0px)
	_bg_tween.tween_property(_bg_rect, "position:y", -2.2, 2.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_bg_tween.parallel().tween_property(_bg_rect, "position:x", 1.0, 3.2).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_bg_tween.tween_property(_bg_rect, "position:y", 2.2, 2.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_bg_tween.parallel().tween_property(_bg_rect, "position:x", -1.0, 3.2).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _start_stage_parallax_tween(stage: Control) -> void:
	if _stage_tween and _stage_tween.is_valid():
		_stage_tween.kill()
	if stage == null or not is_instance_valid(stage):
		return
	_stage_anchor = stage
	var base_top: float = stage.offset_top
	_stage_tween = create_tween().set_loops()
	## 中央展台視差浮動：中景不同頻率 (3.8s) 浮動 (offset_top: ±1.4px)，與遠景天空形成立體景深視差
	_stage_tween.tween_property(stage, "offset_top", base_top - 1.4, 1.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_stage_tween.tween_property(stage, "offset_top", base_top + 1.4, 1.9).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


## ──────────────────────────────────────────
## 黃金以太塵埃微粒與發條微光 (Golden Ether Motes)
## ──────────────────────────────────────────
func _spawn_floating_ether_motes() -> void:
	var gp: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		gp = (loop as SceneTree).root.get_node_or_null("GraphicsProfile")
	var n := 20
	if gp != null:
		n = int(gp.particle_count(20))
	if n <= 0:
		return
	for i in range(n):
		var star := ColorRect.new()
		star.name = "EtherMote_%d" % i
		var sz := 3.2 + float((i % 4) * 1.6)
		star.custom_minimum_size = Vector2(sz, sz)
		star.size = Vector2(sz, sz)
		star.pivot_offset = Vector2(sz * 0.5, sz * 0.5)
		star.rotation = PI * 0.25
		## 金色微光星屑粒子色盤：金黃、暖橘、亮香檳金、以太青綠
		var c := COLOR_GOLD if (i % 3 == 0) else (COLOR_ORANGE if (i % 3 == 1) else Color(1.0, 0.94, 0.70, 0.90))
		if i % 5 == 0:
			c = Color(0.243, 0.812, 0.749, 0.75) # 以太微光
		star.color = c
		star.position = Vector2(randf_range(40.0, 1240.0), randf_range(80.0, 600.0))
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE

		## 雙層微光星屑：外圈微光光暈
		if i % 2 == 0:
			var halo := ColorRect.new()
			halo.name = "Halo"
			var hsz := sz * 2.2
			halo.size = Vector2(hsz, hsz)
			halo.position = Vector2(-sz * 0.6, -sz * 0.6)
			halo.pivot_offset = Vector2(hsz * 0.5, hsz * 0.5)
			halo.rotation = PI * 0.25
			var hc := c
			hc.a = 0.28
			halo.color = hc
			halo.mouse_filter = Control.MOUSE_FILTER_IGNORE
			star.add_child(halo)

		_particles_root.add_child(star)

		# 緩慢升騰、微幅左右飄動與柔和呼吸閃爍
		var tw := create_tween().set_loops()
		var dur := randf_range(3.2, 5.4)
		var dy := randf_range(-22.0, -42.0)
		var dx := randf_range(-10.0, 10.0)
		tw.tween_property(star, "position:y", star.position.y + dy, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "position:x", star.position.x + dx, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "rotation", star.rotation + PI * 0.5, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.25, dur * 0.5)
		tw.tween_property(star, "position:y", star.position.y, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "position:x", star.position.x, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "rotation", star.rotation + PI, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.95, dur * 0.5)

## ──────────────────────────────────────────
## ──────────────────────────────────────────
## 頂部多巴胺 HUD (Top Dopamine HUD)
## ──────────────────────────────────────────
func _build_top_hud() -> void:
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.offset_left = 16
	top_bar.offset_right = -16
	top_bar.offset_top = 10
	top_bar.offset_bottom = 74
	
	top_bar.add_theme_stylebox_override("panel", _create_banner_panel())
	add_child(top_bar)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 18)
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	top_bar.add_child(h)

	## 玩家個人檔案
	var p_box := HBoxContainer.new()
	p_box.add_theme_constant_override("separation", 10)
	h.add_child(p_box)

	var p_frame := PanelContainer.new()
	var psb := StyleBoxFlat.new()
	psb.bg_color = Color(0.14, 0.11, 0.18, 0.85)
	psb.border_color = Color(0.83, 0.68, 0.22, 0.85)
	psb.set_border_width_all(1)
	psb.border_width_bottom = 3
	psb.set_corner_radius_all(26)
	p_frame.custom_minimum_size = Vector2(52, 52)
	p_frame.add_theme_stylebox_override("panel", psb)
	var p_tex := TextureRect.new()
	p_tex.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	p_tex.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	p_tex.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	var init_gs := _gs()
	var init_race := str(init_gs.player_race).strip_edges().to_lower() if init_gs and "player_race" in init_gs else "rabbit"
	p_tex.texture = _get_hero_portrait(init_race)
	_profile_avatar = p_tex
	p_frame.add_child(p_tex)
	p_box.add_child(p_frame)

	var info_v := VBoxContainer.new()
	info_v.alignment = BoxContainer.ALIGNMENT_CENTER
	info_v.add_theme_constant_override("separation", 2)
	
	var row1 := HBoxContainer.new()
	row1.add_theme_constant_override("separation", 8)
	_lv_label = Label.new()
	_lv_label.text = "Lv.1"
	_lv_label.add_theme_color_override("font_color", COLOR_GOLD)
	_lv_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_lv_label.add_theme_constant_override("outline_size", 2)
	_lv_label.add_theme_font_size_override("font_size", 16)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = _get_hero_name()
	_name_label.add_theme_font_size_override("font_size", 17)
	_name_label.add_theme_color_override("font_color", Color("#FFFDF8"))
	_name_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_name_label.add_theme_constant_override("outline_size", 3)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	_power_label = Label.new()
	_power_label.text = _t("戰力 %d") % 0
	_power_label.add_theme_color_override("font_color", Color("#E5C158"))
	_power_label.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_power_label.add_theme_constant_override("outline_size", 2)
	_power_label.add_theme_font_size_override("font_size", 13)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 蒸汽發條黃銅金屬三寶儀表槽（帶對應發條核心圖示與立體厚底）
	_energy_label = _add_clean_capsule(h, "能量", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_energy_key.png")
	if _energy_label.has_meta("title_label"):
		_energy_title_label = _energy_label.get_meta("title_label") as Label
	var energy_cap: PanelContainer = _energy_label.get_parent().get_parent() as PanelContainer
	if energy_cap:
		energy_cap.mouse_filter = Control.MOUSE_FILTER_STOP
		energy_cap.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
				open_energy_dialog()
		)
	_gold_label = _add_clean_capsule(h, "金幣", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_gold_coin.png")
	if _gold_label.has_meta("title_label"):
		_gold_title_label = _gold_label.get_meta("title_label") as Label
	var gold_cap: PanelContainer = _gold_label.get_parent().get_parent() as PanelContainer
	if gold_cap:
		gold_cap.mouse_filter = Control.MOUSE_FILTER_STOP
		gold_cap.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
				open_shop()
		)
	_gem_label = _add_clean_capsule(h, "星屑", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_gem_stardust.png")
	if _gem_label.has_meta("title_label"):
		_gem_title_label = _gem_label.get_meta("title_label") as Label
	var gem_cap: PanelContainer = _gem_label.get_parent().get_parent() as PanelContainer
	if gem_cap:
		gem_cap.mouse_filter = Control.MOUSE_FILTER_STOP
		gem_cap.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
				open_shop()
		)

	var shop_btn := Button.new()
	shop_btn.name = "ShopButton"
	shop_btn.text = _t("商城")
	var shop_icon_path := "res://assets/icons/hud/icon_btn_shop.png"
	if ResourceLoader.exists(shop_icon_path):
		shop_btn.icon = load(shop_icon_path)
		shop_btn.expand_icon = true
		shop_btn.add_theme_constant_override("icon_max_width", 26)
		shop_btn.add_theme_constant_override("h_separation", 6)
		shop_btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	shop_btn.custom_minimum_size = Vector2(104, 50)
	var shop_sb := StyleBoxFlat.new()
	shop_sb.bg_color = Color("#FFA010")
	shop_sb.border_color = COLOR_BORDER
	shop_sb.set_border_width_all(2)
	shop_sb.border_width_bottom = 5
	shop_sb.set_corner_radius_all(18)
	shop_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	shop_sb.shadow_size = 6
	shop_sb.shadow_offset = Vector2(0, 3)
	shop_btn.add_theme_stylebox_override("normal", shop_sb)
	var shop_sb_h := shop_sb.duplicate() as StyleBoxFlat
	shop_sb_h.bg_color = Color(1.0, 0.72, 0.20, 1.0)
	shop_btn.add_theme_stylebox_override("hover", shop_sb_h)
	shop_btn.add_theme_stylebox_override("focus", shop_sb_h)
	var shop_sb_p := shop_sb.duplicate() as StyleBoxFlat
	shop_sb_p.border_width_bottom = 2
	shop_btn.add_theme_stylebox_override("pressed", shop_sb_p)
	shop_btn.add_theme_font_size_override("font_size", 16)
	shop_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	shop_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	shop_btn.add_theme_constant_override("outline_size", 3)
	shop_btn.pressed.connect(func():
		open_shop()
	)
	_shop_button = shop_btn
	h.add_child(shop_btn)

	var set_btn := Button.new()
	set_btn.name = "SettingsButton"
	set_btn.text = _t("設置")
	var settings_icon_path := "res://assets/icons/hud/icon_btn_settings.png"
	if ResourceLoader.exists(settings_icon_path):
		set_btn.icon = load(settings_icon_path)
		set_btn.expand_icon = true
		set_btn.add_theme_constant_override("icon_max_width", 26)
		set_btn.add_theme_constant_override("h_separation", 6)
		set_btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	set_btn.custom_minimum_size = Vector2(104, 50)
	var set_sb := StyleBoxFlat.new()
	set_sb.bg_color = Color("#38A0FF")
	set_sb.border_color = COLOR_BORDER
	set_sb.set_border_width_all(2)
	set_sb.border_width_bottom = 5
	set_sb.set_corner_radius_all(18)
	set_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	set_sb.shadow_size = 6
	set_sb.shadow_offset = Vector2(0, 3)
	set_btn.add_theme_stylebox_override("normal", set_sb)
	var set_sb_h := set_sb.duplicate() as StyleBoxFlat
	set_sb_h.bg_color = Color(0.35, 0.72, 1.0, 1.0)
	set_btn.add_theme_stylebox_override("hover", set_sb_h)
	set_btn.add_theme_stylebox_override("focus", set_sb_h)
	var set_sb_p := set_sb.duplicate() as StyleBoxFlat
	set_sb_p.border_width_bottom = 2
	set_btn.add_theme_stylebox_override("pressed", set_sb_p)
	set_btn.add_theme_font_size_override("font_size", 16)
	set_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	set_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	set_btn.add_theme_constant_override("outline_size", 3)
	set_btn.pressed.connect(func():
		var s_scn := load("res://scripts/ui/mobile_settings.gd")
		var s_ui: Control = s_scn.new()
		s_ui.z_index = 80
		add_child(s_ui)
	)
	_settings_button = set_btn
	h.add_child(set_btn)

func _add_clean_capsule(parent: Container, title: String, val: String, accent: Color, icon_path: String = "") -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.14, 0.11, 0.18, 0.82)
	csb.border_color = Color(0.83, 0.68, 0.22, 0.75)
	csb.set_border_width_all(1)
	csb.border_width_bottom = 4
	csb.set_corner_radius_all(16)
	csb.content_margin_left = 12
	csb.content_margin_right = 14
	csb.content_margin_top = 4
	csb.content_margin_bottom = 5
	csb.shadow_color = Color(0.08, 0.06, 0.14, 0.20)
	csb.shadow_size = 4
	csb.shadow_offset = Vector2(0, 2)
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 6)
	h.alignment = BoxContainer.ALIGNMENT_CENTER

	if not icon_path.is_empty() and ResourceLoader.exists(icon_path):
		var icon_rect := TextureRect.new()
		icon_rect.texture = load(icon_path)
		icon_rect.custom_minimum_size = Vector2(22, 22)
		icon_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon_rect.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		h.add_child(icon_rect)

	var il := Label.new()
	il.text = _t(title)
	il.set_meta("key", title)
	il.add_theme_font_size_override("font_size", 13)
	il.add_theme_color_override("font_color", accent.lerp(Color("#FFD028"), 0.35))
	il.add_theme_color_override("font_outline_color", COLOR_BORDER)
	il.add_theme_constant_override("outline_size", 2)
	il.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.set_meta("title_label", il)
	vl.add_theme_font_size_override("font_size", 15)
	vl.add_theme_color_override("font_color", Color("#FFFDF8"))
	vl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	vl.add_theme_constant_override("outline_size", 2)
	vl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	h.add_child(vl)

	cap.add_child(h)
	parent.add_child(cap)
	return vl

## ──────────────────────────────────────────
## 底部多巴胺導航欄 (Bottom Dopamine Dock)
## ──────────────────────────────────────────
func _build_bottom_dock() -> void:
	var dock := PanelContainer.new()
	dock.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	dock.offset_left = 24
	dock.offset_right = -24
	dock.offset_top = -88
	dock.offset_bottom = -12
	
	var dsb := _create_banner_panel()
	dsb.content_margin_left = 10
	dsb.content_margin_right = 10
	dsb.content_margin_top = 6
	dsb.content_margin_bottom = 7
	dsb.shadow_size = 12
	dsb.shadow_offset = Vector2(0, 4)
	dock.add_theme_stylebox_override("panel", dsb)
	add_child(dock)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 14)
	dock.add_child(h)

	var tabs := [
		{"tab": Tab.VILLAGE, "title": "發條新村", "icon": "res://assets/icons/hud/icon_dock_village.png"},
		{"tab": Tab.CHARACTER, "title": "角色裝備", "icon": "res://assets/icons/hud/icon_dock_equip.png"},
		{"tab": Tab.ADVENTURE, "title": "四區出征", "icon": "res://assets/icons/hud/icon_dock_campaign.png"},
		{"tab": Tab.SOUL_HALL, "title": "聚魂殿堂", "icon": "res://assets/icons/hud/icon_dock_soul.png"},
		{"tab": Tab.BAG, "title": "冒險背包", "icon": "res://assets/icons/hud/icon_dock_bag.png"},
	]

	_dock_buttons.clear()
	for d in tabs:
		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(0, 56)
		btn.set_meta("dock_key", str(d["title"]))
		btn.text = _t(str(d["title"]))
		var icon_path := str(d["icon"])
		if ResourceLoader.exists(icon_path):
			btn.icon = load(icon_path)
			btn.expand_icon = true
			btn.add_theme_constant_override("icon_max_width", 32)
			btn.add_theme_constant_override("h_separation", 8)
			btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
		btn.add_theme_font_size_override("font_size", 18)
		var t: Tab = d["tab"]
		btn.pressed.connect(func(): _switch_tab(t))
		h.add_child(btn)
		_dock_buttons.append(btn)
	_refresh_dock_badges()


func _attach_dock_badge(btn: Button) -> Control:
	var existing = btn.get_node_or_null("DopamineBadge")
	if existing != null and is_instance_valid(existing):
		return existing
	var badge := Panel.new()
	badge.name = "DopamineBadge"
	badge.custom_minimum_size = Vector2(16, 16)
	badge.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	badge.offset_left = -20
	badge.offset_top = 4
	badge.offset_right = -4
	badge.offset_bottom = 20
	badge.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var bsb := StyleBoxFlat.new()
	bsb.bg_color = COLOR_PINK # #FF5E8A 多巴胺鮮亮珊瑚粉
	bsb.border_color = COLOR_GOLD # #FFD028 亮金高光邊框
	bsb.set_border_width_all(2)
	bsb.set_corner_radius_all(8)
	bsb.shadow_color = Color(1.0, 0.37, 0.54, 0.6)
	bsb.shadow_size = 4
	bsb.shadow_offset = Vector2(0, 1)
	badge.add_theme_stylebox_override("panel", bsb)

	var dot := Panel.new()
	dot.name = "GoldCenter"
	dot.custom_minimum_size = Vector2(6, 6)
	dot.set_anchors_preset(Control.PRESET_CENTER)
	dot.offset_left = -3
	dot.offset_top = -3
	dot.offset_right = 3
	dot.offset_bottom = 3
	dot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = COLOR_GOLD
	dsb.set_corner_radius_all(3)
	dot.add_theme_stylebox_override("panel", dsb)
	badge.add_child(dot)

	btn.add_child(badge)
	return badge


func _has_new_core_drop() -> bool:
	var gs := _gs()
	if gs and gs.has_method("has_new_core_part"):
		return bool(gs.call("has_new_core_part"))
	var cs := preload("res://scripts/systems/core_system.gd") if ResourceLoader.exists("res://scripts/systems/core_system.gd") else null
	if cs != null:
		return cs.has_new_core_drop()
	return false


func _clear_new_core_drop_notification() -> void:
	var gs := _gs()
	if gs and gs.has_method("clear_new_core_drop"):
		gs.call("clear_new_core_drop")
	var cs := preload("res://scripts/systems/core_system.gd") if ResourceLoader.exists("res://scripts/systems/core_system.gd") else null
	if cs != null:
		cs.clear_new_core_drop()
	_refresh_dock_badges()


func _refresh_dock_badges() -> void:
	var has_new := _has_new_core_drop()
	for i in range(_dock_buttons.size()):
		var btn: Button = _dock_buttons[i]
		if i == int(Tab.CHARACTER) or i == int(Tab.BAG):
			var badge = _attach_dock_badge(btn)
			badge.visible = has_new
		else:
			var b = btn.get_node_or_null("DopamineBadge")
			if b:
				b.visible = false

func _style_dock_button(btn: Button, is_active: bool) -> void:
	var sb := StyleBoxFlat.new()
	if is_active:
		sb.bg_color = COLOR_ORANGE
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 5
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 12
		sb.content_margin_right = 12
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	else:
		sb.bg_color = COLOR_CARD_WARM
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 4
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 12
		sb.content_margin_right = 12
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.10)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_ORANGE)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var sb_h := sb.duplicate() as StyleBoxFlat
	if not is_active:
		sb_h.bg_color = COLOR_CARD_GOLD
	else:
		sb_h.bg_color = Color("#FFB84D")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)

func switch_tab(target: int) -> void:
	_switch_tab(target as Tab)

func _switch_tab(target: Tab) -> void:
	_current_tab = target
	if target == Tab.CHARACTER or target == Tab.BAG:
		_clear_new_core_drop_notification()
	if _village_layer:
		_village_layer.visible = (target == Tab.VILLAGE)
	if _char_layer:
		_char_layer.visible = (target == Tab.CHARACTER)
		if target == Tab.CHARACTER:
			_refresh_weapon_slot_buttons()
			_refresh_char_tab_stats(false)
	if _adventure_layer:
		_adventure_layer.visible = (target == Tab.ADVENTURE)
	if _soul_layer:
		_soul_layer.visible = (target == Tab.SOUL_HALL)
	if _bag_layer:
		_bag_layer.visible = (target == Tab.BAG)
		if target == Tab.BAG:
			_refresh_bag_tab()

	for i in range(_dock_buttons.size()):
		var is_active := (i == int(target))
		_style_dock_button(_dock_buttons[i], is_active)
	_refresh_dock_badges()

## ──────────────────────────────────────────
## 每幀小動作與發條微動判定 (動態待機自然活化)
## ──────────────────────────────────────────
func _process(delta: float) -> void:
	if _current_tab != Tab.VILLAGE or _is_interacting:
		return

	# 背後發條鑰匙每隔 4~6 秒微轉半圈並伴隨微小抖動反饋
	_key_wind_timer += delta
	if _key_wind_timer >= 4.5:
		_key_wind_timer = 0.0
		_trigger_key_half_turn()

	# 發條儲能庫微動氣泡 8 幀發條旋轉小動效推進
	if _vault_bubble and is_instance_valid(_vault_bubble) and _vault_bubble.visible and not _vault_bubble_key_textures.is_empty():
		_vault_bubble_frame_timer += delta
		if _vault_bubble_frame_timer >= 0.12:
			_vault_bubble_frame_timer = 0.0
			step_vault_bubble_frame()

	if not enable_idle_flavor:
		return

	_idle_action_timer += delta
	if _idle_action_timer > 5.0:
		_idle_action_timer = 0.0
		_play_random_idle_flavor()


func trigger_key_half_turn() -> void:
	_trigger_key_half_turn()


func _trigger_key_half_turn() -> void:
	if _hero_key_avatar == null or not is_instance_valid(_hero_key_avatar) or not _hero_key_avatar.visible:
		return
	if _is_interacting:
		return
	_key_rotation_turns += PI
	var tw := create_tween()
	# 微轉半圈 (180度, PI 弧度)，帶機械卡榫回彈
	tw.tween_property(_hero_key_avatar, "rotation", _key_rotation_turns, 0.30).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	# 伴隨微小抖動反饋 (內部齒輪嚙合的震顫)
	if _hero_avatar and is_instance_valid(_hero_avatar):
		tw.parallel().tween_property(_hero_avatar, "position:x", -158.5, 0.05).set_delay(0.20)
		tw.parallel().tween_property(_hero_avatar, "position:x", -161.5, 0.05).set_delay(0.25)
		tw.parallel().tween_property(_hero_avatar, "position:x", -160.0, 0.05).set_delay(0.30)
	# 發條自身回彈卡位微抖動
	tw.tween_property(_hero_key_avatar, "rotation", _key_rotation_turns + 0.05, 0.04)
	tw.tween_property(_hero_key_avatar, "rotation", _key_rotation_turns, 0.04)
	tw.tween_callback(func():
		if is_inside_tree() and visible:
			_burst_tiny_key_sparks()
	)


func _burst_tiny_key_sparks() -> void:
	if _hero_avatar == null or not is_inside_tree():
		return
	var center := _hero_avatar.global_position + Vector2(100, 175)
	for i in range(3):
		var spark := ColorRect.new()
		spark.name = "KeySpark_%d" % i
		spark.custom_minimum_size = Vector2(3, 3)
		spark.size = Vector2(3, 3)
		spark.pivot_offset = Vector2(1.5, 1.5)
		spark.rotation = PI * 0.25
		spark.color = COLOR_GOLD if i % 2 == 0 else Color("#FFF4B8")
		spark.global_position = center
		spark.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(spark)

		var angle := randf_range(-PI * 0.8, -PI * 0.2)
		var dist := randf_range(15.0, 30.0)
		var target := center + Vector2(cos(angle), sin(angle)) * dist

		var tw := create_tween()
		tw.tween_property(spark, "global_position", target, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(spark, "modulate:a", 0.0, 0.25).set_delay(0.08)
		tw.tween_callback(spark.queue_free)


func _play_random_idle_flavor() -> void:
	var roll := randi() % 3
	if roll == 0 and _tex_telegraph:
		## 小伸展站姿
		if _hero_key_avatar:
			_hero_key_avatar.visible = false
		_hero_avatar.texture = _tex_telegraph
		_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var tw := create_tween()
		tw.tween_interval(1.2)
		tw.tween_callback(func():
			if not _is_interacting:
				_restore_hero_idle()
		)
	elif roll == 1 and _tex_recover:
		## 伸個懶腰
		if _hero_key_avatar:
			_hero_key_avatar.visible = false
		_hero_avatar.texture = _tex_recover
		_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		var tw := create_tween()
		tw.tween_interval(1.0)
		tw.tween_callback(func():
			if not _is_interacting:
				_restore_hero_idle()
		)

## ──────────────────────────────────────────
## Tab 1: 發條新村 (神殿日晷展台 + 點擊互動 + 黃金以太粒子)
## ──────────────────────────────────────────
class SundialPedestal extends Control:
	func _init() -> void:
		name = "HeroStagePedestal"
		mouse_filter = Control.MOUSE_FILTER_IGNORE

	func _draw() -> void:
		var c := Vector2(10, 106)
		var rx := 168.0
		var ry := 38.0
		# 1. 底部接地微影 (Ambient Floor Shadow)
		draw_set_transform(Vector2(0, 10), 0.0, Vector2.ONE)
		draw_colored_polygon(_ellipse_pts(c, rx + 12.0, ry + 5.0), Color(0.08, 0.06, 0.12, 0.35))

		# 2. 展台側面黃銅金屬厚度 (3D Bevel Height 10px)
		draw_set_transform(Vector2(0, 6), 0.0, Vector2.ONE)
		draw_colored_polygon(_ellipse_pts(c, rx, ry), Color(0.24, 0.17, 0.10, 0.95))

		# 3. 頂部發條日晷大理石檯面 (Top Dial Platform)
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
		draw_colored_polygon(_ellipse_pts(c, rx, ry), Color(0.98, 0.93, 0.83, 0.96))

		# 黃銅外邊框
		draw_polyline(_ellipse_pts(c, rx, ry), Color(0.83, 0.68, 0.22, 1.0), 3.0, true)
		# 內圈古典發條日晷齒輪刻度同心光環
		draw_polyline(_ellipse_pts(c, rx * 0.78, ry * 0.78), Color(0.83, 0.68, 0.22, 0.50), 1.5, true)
		draw_polyline(_ellipse_pts(c, rx * 0.48, ry * 0.48), Color(0.83, 0.68, 0.22, 0.35), 1.0, true)

	func _ellipse_pts(center: Vector2, r_x: float, r_y: float) -> PackedVector2Array:
		var pts := PackedVector2Array()
		var segs := 56
		for i in range(segs):
			var a := float(i) * TAU / float(segs)
			pts.append(Vector2(center.x + cos(a) * r_x, center.y + sin(a) * r_y))
		return pts


func _build_village_tab() -> void:
	_village_layer = Control.new()
	_village_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_village_layer)

	## 中央英雄展台
	var stage_anchor := Control.new()
	stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	stage_anchor.offset_top = 45
	_village_layer.add_child(stage_anchor)
	_start_stage_parallax_tween(stage_anchor)

	## 0. 地面舞台日晷展台 (Ground Sunken Dial Pedestal / 消除浮空貼紙感)
	var stage_pedestal := SundialPedestal.new()
	stage_anchor.add_child(stage_pedestal)

	## 0.1 發條儲能庫微動氣泡 (Vault Bubble / 伴隨中央展台微浮動)
	_build_vault_bubble(stage_anchor)

	## 1. 角色腳底接地軟影 (Foot Soft Shadow / 漸層軟影漫反射)
	_hero_shadow = TextureRect.new()
	_hero_shadow.name = "HeroFootShadow"
	_hero_shadow.add_to_group("soft_shadow")
	_hero_shadow.offset_left = -110
	_hero_shadow.offset_top = 78
	_hero_shadow.offset_right = 130
	_hero_shadow.offset_bottom = 128
	_hero_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	_hero_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hero_shadow.texture = _soft_shadow_tex()
	_hero_shadow.pivot_offset = Vector2(120, 25)

	var shadow_mat := ShaderMaterial.new()
	shadow_mat.shader = FootShadowShader
	shadow_mat.set_shader_parameter("strength", 0.55)
	shadow_mat.set_shader_parameter("smooth_gradient", true)
	shadow_mat.set_shader_parameter("is_contact_shadow", false)
	shadow_mat.set_shader_parameter("shadow_color", Color(0.015, 0.012, 0.025, 1.0))
	_hero_shadow.material = shadow_mat
	stage_anchor.add_child(_hero_shadow)

	## 1.1 緊密接地閉塞陰影 (Contact Occlusion Shadow / 深色接觸硬影)
	var contact_shadow := TextureRect.new()
	contact_shadow.name = "HeroContactShadow"
	contact_shadow.add_to_group("soft_shadow")
	contact_shadow.offset_left = -46
	contact_shadow.offset_top = 99
	contact_shadow.offset_right = 66
	contact_shadow.offset_bottom = 113
	contact_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	contact_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	contact_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	contact_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	contact_shadow.texture = _soft_shadow_tex()
	contact_shadow.pivot_offset = Vector2(56, 7)

	var contact_mat := ShaderMaterial.new()
	contact_mat.shader = FootShadowShader
	contact_mat.set_shader_parameter("strength", 0.98)
	contact_mat.set_shader_parameter("is_contact_shadow", true)
	contact_mat.set_shader_parameter("smooth_gradient", false)
	contact_mat.set_shader_parameter("shadow_color", Color(0.005, 0.005, 0.01, 1.0))
	contact_shadow.material = contact_mat
	stage_anchor.add_child(contact_shadow)
	_hero_contact_shadow = contact_shadow

	## 2. 2.2 頭身白兔主角 (512 高清紙娃娃外裝合成 + 金色邊緣輪廓光著色器)
	_hero_avatar = TextureRect.new()
	_hero_avatar.name = "HeroAvatar"
	_hero_avatar.offset_left = -160
	_hero_avatar.offset_top = -150
	_hero_avatar.offset_right = 160
	_hero_avatar.offset_bottom = 170
	_hero_avatar.custom_minimum_size = Vector2(320, 320)
	_hero_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_avatar.pivot_offset = Vector2(160, 260)

	var hero_rim_mat := ShaderMaterial.new()
	hero_rim_mat.shader = RimLightShader
	hero_rim_mat.set_shader_parameter("outline_color", Color(0.22, 0.14, 0.09, 1.0))
	hero_rim_mat.set_shader_parameter("outline_width", 2.6)
	hero_rim_mat.set_shader_parameter("outline_enabled", true)
	hero_rim_mat.set_shader_parameter("rim_enabled", true)
	hero_rim_mat.set_shader_parameter("rim_color", Color(1.0, 0.85, 0.28, 1.0))
	hero_rim_mat.set_shader_parameter("rim_width", 6.2)
	hero_rim_mat.set_shader_parameter("rim_intensity", 2.0)
	hero_rim_mat.set_shader_parameter("rim_direction", Vector2(0.15, -0.95))
	_hero_avatar.material = hero_rim_mat

	## 2.1 背後發條鑰匙 (Winding Key 獨立圖層：show_behind_parent 隨軀幹同步待機微轉 + 金色反光)
	_hero_key_avatar = TextureRect.new()
	_hero_key_avatar.name = "HeroWindingKey"
	_hero_key_avatar.set_anchors_preset(Control.PRESET_FULL_RECT)
	_hero_key_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_key_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_key_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_key_avatar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hero_key_avatar.show_behind_parent = true
	_hero_key_avatar.pivot_offset = KEY_PIVOTS_320.get("rabbit", Vector2(103, 186))

	var key_rim_mat := ShaderMaterial.new()
	key_rim_mat.shader = RimLightShader
	key_rim_mat.set_shader_parameter("outline_color", Color(0.22, 0.14, 0.09, 1.0))
	key_rim_mat.set_shader_parameter("outline_width", 2.2)
	key_rim_mat.set_shader_parameter("outline_enabled", true)
	key_rim_mat.set_shader_parameter("rim_enabled", true)
	key_rim_mat.set_shader_parameter("rim_color", Color(1.0, 0.85, 0.28, 1.0))
	key_rim_mat.set_shader_parameter("rim_width", 5.0)
	key_rim_mat.set_shader_parameter("rim_intensity", 1.8)
	key_rim_mat.set_shader_parameter("rim_direction", Vector2(0.15, -0.95))
	_hero_key_avatar.material = key_rim_mat
	_hero_avatar.add_child(_hero_key_avatar)

	_apply_hero_idle_visual()
	stage_anchor.add_child(_hero_avatar)

	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	## 3. 頭頂稱號與名字（精巧微型黃銅銘牌，上移避開齒輪中央能量光芒與核心）
	var tag_panel := PanelContainer.new()
	tag_panel.set_anchors_preset(Control.PRESET_CENTER_TOP)
	tag_panel.offset_left = -56
	tag_panel.offset_top = -142
	tag_panel.offset_right = 56
	tag_panel.offset_bottom = -100
	tag_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var tag_sb := StyleBoxFlat.new()
	tag_sb.bg_color = Color(0.14, 0.11, 0.18, 0.85) # 蒸汽發條半透深金屬板件
	tag_sb.border_color = Color(0.83, 0.68, 0.22, 0.85) # 古典黃銅邊飾
	tag_sb.set_border_width_all(1)
	tag_sb.border_width_bottom = 3
	tag_sb.set_corner_radius_all(12)
	tag_sb.content_margin_left = 8
	tag_sb.content_margin_right = 8
	tag_sb.content_margin_top = 2
	tag_sb.content_margin_bottom = 2
	tag_sb.shadow_size = 0
	tag_panel.add_theme_stylebox_override("panel", tag_sb)

	var tag_v := VBoxContainer.new()
	tag_v.alignment = BoxContainer.ALIGNMENT_CENTER
	tag_v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tag_v.add_theme_constant_override("separation", 1)

	_hero_name_tag = Label.new()
	_hero_name_tag.text = _get_hero_name()
	_hero_name_tag.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hero_name_tag.add_theme_font_size_override("font_size", 18)
	_hero_name_tag.add_theme_color_override("font_color", Color("#FFFDF8"))
	_hero_name_tag.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_hero_name_tag.add_theme_constant_override("outline_size", 2)
	tag_v.add_child(_hero_name_tag)

	var title_l := Label.new()
	title_l.text = "【%s】" % _t("初出茅廬")
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 11)
	title_l.add_theme_color_override("font_color", COLOR_GOLD)
	title_l.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_l.add_theme_constant_override("outline_size", 1)
	tag_v.add_child(title_l)
	_hero_title_tag = title_l

	tag_panel.add_child(tag_v)
	_hero_avatar.add_child(tag_panel)

	## 4. 點擊彈出的多巴胺對話氣泡
	_speech_bubble = PanelContainer.new()
	_speech_bubble.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_speech_bubble.offset_left = -110
	_speech_bubble.offset_top = -110
	_speech_bubble.offset_right = 150
	_speech_bubble.offset_bottom = -60
	_speech_bubble.visible = false
	var bub_sb := StyleBoxFlat.new()
	bub_sb.bg_color = COLOR_BG_CREAM
	bub_sb.border_color = COLOR_BORDER
	bub_sb.set_border_width_all(2)
	bub_sb.border_width_bottom = 4
	bub_sb.set_corner_radius_all(18)
	bub_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	bub_sb.shadow_size = 6
	bub_sb.content_margin_left = 14
	bub_sb.content_margin_right = 14
	bub_sb.content_margin_top = 6
	bub_sb.content_margin_bottom = 6
	_speech_bubble.add_theme_stylebox_override("panel", bub_sb)

	_speech_label = Label.new()
	_speech_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_speech_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_speech_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_speech_label.add_theme_font_size_override("font_size", 14)
	_speech_bubble.add_child(_speech_label)
	_hero_avatar.add_child(_speech_bubble)
	_update_speech_bubble_text()

	## 呼吸動畫
	_start_breathe_tween()

	## 左側四大殿堂：收斂尺寸與半透明金屬板件，將視覺焦點100%讓給中央主角
	var left_shops := VBoxContainer.new()
	left_shops.name = "HallCardsContainer"
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 28
	left_shops.offset_top = 24
	left_shops.offset_right = 224
	left_shops.offset_bottom = -24
	left_shops.add_theme_constant_override("separation", 10)
	_village_layer.add_child(left_shops)

	_hall_buttons.clear()
	_active_hall_index = -1

	_add_hall_card(left_shops, "天宮鐵匠", "品質轉化 · 裝備鍛造", "res://assets/icons/hud/icon_hall_forge.png", func():
		open_forge()
	)
	_add_hall_card(left_shops, "手藝工坊", "紅黃藍石 · 三合一熔煉", "res://assets/icons/hud/icon_hall_gem.png", func():
		open_gem_workshop()
	)
	_add_hall_card(left_shops, "演武競技", "挑戰對手 · 雙倍抽獎", "res://assets/icons/hud/icon_hall_arena.png", func():
		request_battle.emit("arena")
	)
	_add_hall_card(left_shops, "冒險委託", "每日簽到 · 懸賞領獎", "res://assets/icons/hud/icon_hall_quest.png", func():
		open_windup_daily()
	)

	## 裝備示意：2x2 立體方形裝備 Icon 槽位（外裝／武器／發條／奇玩）
	_equip_schematic = GridContainer.new()
	_equip_schematic.name = "EquipSchematic"
	_equip_schematic.columns = 2
	_equip_schematic.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_equip_schematic.offset_left = -260
	_equip_schematic.offset_top = 10
	_equip_schematic.offset_right = -20
	_equip_schematic.offset_bottom = 180
	_equip_schematic.add_theme_constant_override("h_separation", 10)
	_equip_schematic.add_theme_constant_override("v_separation", 6)
	_equip_schematic.z_index = 2
	_village_layer.add_child(_equip_schematic)
	_refresh_equip_schematic()

	## 右側：多巴胺奶油白戰情報告板 (專注於主線推進)
	var right_card := PanelContainer.new()
	right_card.name = "RightSortieCard"
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -336
	right_card.offset_top = -216
	right_card.offset_right = -20
	right_card.offset_bottom = -16

	# 升級為半透明黑曜黃銅板件與立體果凍厚底質感
	var rsb := StyleBoxFlat.new()
	rsb.bg_color = Color(0.12, 0.09, 0.16, 0.82)
	rsb.border_color = COLOR_BORDER
	rsb.set_border_width_all(2)
	rsb.border_width_bottom = 6
	rsb.set_corner_radius_all(22)
	rsb.content_margin_left = 18
	rsb.content_margin_right = 18
	rsb.content_margin_top = 14
	rsb.content_margin_bottom = 14
	rsb.shadow_color = Color(0.08, 0.06, 0.16, 0.35)
	rsb.shadow_size = 12
	rsb.shadow_offset = Vector2(0, 5)
	right_card.add_theme_stylebox_override("panel", rsb)
	_village_layer.add_child(right_card)

	# 蒸汽發條黃銅雙層內飾邊 (Brass Inner Rim)
	var r_trim := Panel.new()
	r_trim.set_anchors_preset(Control.PRESET_FULL_RECT)
	r_trim.offset_left = 3
	r_trim.offset_top = 3
	r_trim.offset_right = -3
	r_trim.offset_bottom = -7
	r_trim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var rtsb := StyleBoxFlat.new()
	rtsb.draw_center = false
	rtsb.border_color = Color(0.83, 0.68, 0.22, 0.65)
	rtsb.set_border_width_all(1)
	rtsb.set_corner_radius_all(19)
	r_trim.add_theme_stylebox_override("panel", rtsb)
	right_card.add_child(r_trim)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 8)
	right_card.add_child(rv)

	# 標題欄：黃銅金屬小標牌 (Brass Header Badge)
	var ch_badge := PanelContainer.new()
	ch_badge.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	var cbsb := StyleBoxFlat.new()
	cbsb.bg_color = Color(0.83, 0.68, 0.22, 0.22)
	cbsb.border_color = Color(0.83, 0.68, 0.22, 0.85)
	cbsb.set_border_width_all(1)
	cbsb.set_corner_radius_all(8)
	cbsb.content_margin_left = 8
	cbsb.content_margin_right = 8
	cbsb.content_margin_top = 2
	cbsb.content_margin_bottom = 2
	ch_badge.add_theme_stylebox_override("panel", cbsb)
	rv.add_child(ch_badge)

	var ch_lbl := Label.new()
	ch_lbl.text = _t("冒險出征 · 當前主線")
	if _cached_font:
		ch_lbl.add_theme_font_override("font", _cached_font)
	ch_lbl.add_theme_font_size_override("font_size", 13)
	ch_lbl.add_theme_color_override("font_color", Color("#FFF5E0"))
	ch_badge.add_child(ch_lbl)
	_sortie_title_label = ch_lbl

	var s_name := Label.new()
	var stage_name_text := _t("第二地區 · 白霧之地 (2-4 BOSS)")
	s_name.text = stage_name_text
	s_name.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	if _cached_font:
		s_name.add_theme_font_override("font", _cached_font)
	s_name.add_theme_color_override("font_color", Color("#FFFDF8"))
	s_name.add_theme_color_override("font_outline_color", COLOR_BORDER)
	s_name.add_theme_constant_override("outline_size", 3)
	if stage_name_text.length() > 30:
		s_name.add_theme_font_size_override("font_size", 15)
	else:
		s_name.add_theme_font_size_override("font_size", 16)
	rv.add_child(s_name)
	_sortie_stage_label = s_name

	var btn_go := Button.new()
	btn_go.name = "SortieButton"
	btn_go.text = _t("前往出征")
	var sortie_icon_path := "res://assets/icons/hud/icon_btn_sortie.png"
	if ResourceLoader.exists(sortie_icon_path):
		btn_go.icon = load(sortie_icon_path)
		btn_go.expand_icon = true
		btn_go.add_theme_constant_override("icon_max_width", 36)
		btn_go.add_theme_constant_override("h_separation", 10)
		btn_go.alignment = HORIZONTAL_ALIGNMENT_CENTER
	btn_go.custom_minimum_size = Vector2(280, 64)

	var s_btn_normal := StyleBoxFlat.new()
	s_btn_normal.bg_color = Color("#FFD028")
	s_btn_normal.border_color = COLOR_BORDER
	s_btn_normal.set_border_width_all(2)
	s_btn_normal.border_width_bottom = 6
	s_btn_normal.set_corner_radius_all(20)
	s_btn_normal.shadow_color = Color(0.83, 0.68, 0.22, 0.40)
	s_btn_normal.shadow_size = 8
	s_btn_normal.shadow_offset = Vector2(0, 4)
	btn_go.add_theme_stylebox_override("normal", s_btn_normal)

	var s_btn_hover := s_btn_normal.duplicate() as StyleBoxFlat
	s_btn_hover.bg_color = Color(1.0, 0.88, 0.32, 1.0)
	s_btn_hover.border_color = Color("#FFA010")
	btn_go.add_theme_stylebox_override("hover", s_btn_hover)

	var s_btn_pressed := s_btn_normal.duplicate() as StyleBoxFlat
	s_btn_pressed.bg_color = Color(0.95, 0.72, 0.12, 1.0)
	s_btn_pressed.border_width_bottom = 2
	s_btn_pressed.content_margin_top = 14
	s_btn_pressed.content_margin_bottom = 10
	btn_go.add_theme_stylebox_override("pressed", s_btn_pressed)
	btn_go.add_theme_stylebox_override("focus", s_btn_hover)

	# 內嵌黃銅高光邊飾
	var s_trim := Panel.new()
	s_trim.set_anchors_preset(Control.PRESET_FULL_RECT)
	s_trim.offset_left = 3
	s_trim.offset_top = 3
	s_trim.offset_right = -3
	s_trim.offset_bottom = -7
	s_trim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var stsb := StyleBoxFlat.new()
	stsb.draw_center = false
	stsb.border_color = Color(1.0, 0.95, 0.65, 0.70)
	stsb.set_border_width_all(1)
	stsb.set_corner_radius_all(17)
	s_trim.add_theme_stylebox_override("panel", stsb)
	btn_go.add_child(s_trim)

	if _cached_font:
		btn_go.add_theme_font_override("font", _cached_font)
	btn_go.add_theme_font_size_override("font_size", 22)
	btn_go.add_theme_color_override("font_color", Color("#FFFFFF"))
	btn_go.add_theme_color_override("font_outline_color", COLOR_BORDER)
	btn_go.add_theme_constant_override("outline_size", 4)
	btn_go.pressed.connect(func(): _switch_tab(Tab.ADVENTURE))
	_sortie_button = btn_go
	rv.add_child(btn_go)
	_start_sortie_glow_tween()

	## 發條儲能庫放置收益入口卡片 (對齊右側戰情報告板上方)
	_build_vault_entry_card()

func _build_vault_entry_card() -> void:
	if _village_layer == null:
		return
	_vault_card = PanelContainer.new()
	_vault_card.name = "ClockworkVaultCard"
	_vault_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	_vault_card.offset_left = -336
	_vault_card.offset_top = -342
	_vault_card.offset_right = -20
	_vault_card.offset_bottom = -224
	_vault_card.z_index = 5

	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.12, 0.09, 0.16, 1.0)
	csb.border_color = COLOR_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 14
	csb.content_margin_right = 14
	csb.content_margin_top = 10
	csb.content_margin_bottom = 10
	csb.shadow_color = Color(0.08, 0.06, 0.16, 0.35)
	csb.shadow_size = 10
	csb.shadow_offset = Vector2(0, 4)
	_vault_card.add_theme_stylebox_override("panel", csb)
	_village_layer.add_child(_vault_card)

	var v_trim := Panel.new()
	v_trim.set_anchors_preset(Control.PRESET_FULL_RECT)
	v_trim.offset_left = 3
	v_trim.offset_top = 3
	v_trim.offset_right = -3
	v_trim.offset_bottom = -6
	v_trim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var vtsb := StyleBoxFlat.new()
	vtsb.draw_center = false
	vtsb.border_color = Color(0.83, 0.68, 0.22, 0.50)
	vtsb.set_border_width_all(1)
	vtsb.set_corner_radius_all(15)
	v_trim.add_theme_stylebox_override("panel", vtsb)
	_vault_card.add_child(v_trim)

	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 6)
	_vault_card.add_child(vb)

	var top_h := HBoxContainer.new()
	vb.add_child(top_h)

	_vault_title_lbl = Label.new()
	_vault_title_lbl.name = "VaultTitle"
	_vault_title_lbl.text = Loc.t("vault.title")
	_vault_title_lbl.add_theme_color_override("font_color", COLOR_GOLD)
	_vault_title_lbl.add_theme_font_size_override("font_size", 14)
	if _cached_font:
		_vault_title_lbl.add_theme_font_override("font", _cached_font)
	top_h.add_child(_vault_title_lbl)

	var sp := Control.new()
	sp.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_h.add_child(sp)

	_vault_time_lbl = Label.new()
	_vault_time_lbl.name = "VaultTime"
	_vault_time_lbl.text = "00:00 / 08:00 (0%)"
	_vault_time_lbl.add_theme_color_override("font_color", Color("#C9BFA8"))
	_vault_time_lbl.add_theme_font_size_override("font_size", 12)
	if _cached_font:
		_vault_time_lbl.add_theme_font_override("font", _cached_font)
	top_h.add_child(_vault_time_lbl)

	_vault_progress_bg = PanelContainer.new()
	_vault_progress_bg.name = "VaultProgressBg"
	_vault_progress_bg.custom_minimum_size = Vector2(0, 10)
	var bg_sb := StyleBoxFlat.new()
	bg_sb.bg_color = Color(0.04, 0.03, 0.06, 0.95)
	bg_sb.border_color = COLOR_BORDER
	bg_sb.set_border_width_all(1)
	bg_sb.border_width_bottom = 2
	bg_sb.set_corner_radius_all(5)
	_vault_progress_bg.add_theme_stylebox_override("panel", bg_sb)
	vb.add_child(_vault_progress_bg)

	var fill_clip := Control.new()
	fill_clip.set_anchors_preset(Control.PRESET_FULL_RECT)
	fill_clip.clip_contents = true
	_vault_progress_bg.add_child(fill_clip)

	_vault_progress_fill = Panel.new()
	_vault_progress_fill.name = "VaultProgressFill"
	_vault_progress_fill.custom_minimum_size = Vector2(0, 8)
	var fill_sb := StyleBoxFlat.new()
	fill_sb.bg_color = COLOR_GOLD
	fill_sb.border_color = Color("#FFA010")
	fill_sb.set_border_width_all(1)
	fill_sb.set_corner_radius_all(4)
	_vault_progress_fill.add_theme_stylebox_override("panel", fill_sb)
	fill_clip.add_child(_vault_progress_fill)

	_vault_claim_btn = Button.new()
	_vault_claim_btn.name = "VaultClaimBtn"
	_vault_claim_btn.custom_minimum_size = Vector2(280, 48)
	_vault_claim_btn.focus_mode = Control.FOCUS_NONE
	var btn_sb := StyleBoxFlat.new()
	btn_sb.bg_color = COLOR_GOLD
	btn_sb.border_color = COLOR_BORDER
	btn_sb.set_border_width_all(2)
	btn_sb.border_width_bottom = 5
	btn_sb.set_corner_radius_all(14)
	_vault_claim_btn.add_theme_stylebox_override("normal", btn_sb)
	_vault_claim_btn.add_theme_stylebox_override("hover", btn_sb)
	_vault_claim_btn.add_theme_stylebox_override("pressed", btn_sb)
	_vault_claim_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_vault_claim_btn.add_theme_font_size_override("font_size", 15)
	if _cached_font:
		_vault_claim_btn.add_theme_font_override("font", _cached_font)
	_vault_claim_btn.pressed.connect(func():
		open_clockwork_vault()
	)
	vb.add_child(_vault_claim_btn)
	refresh_vault_display()

func get_vault_card() -> Control:
	return _vault_card

func get_vault_claim_button() -> Button:
	return _vault_claim_btn

func refresh_vault_display() -> void:
	var st: Dictionary = IdleClockworkVault.get_status()
	var sec: float = float(st.get("elapsed_seconds", 0.0))
	var gold: int = int(st.get("gold", 0))
	var scrap: int = int(st.get("iron_scrap", 0))
	var ratio: float = float(st.get("progress_ratio", 0.0))
	var is_full: bool = bool(st.get("is_full", false))

	var hrs_i := int(sec / 3600.0)
	var mins_i := int(fmod(sec, 3600.0) / 60.0)

	# 1. 更新右側發條儲能庫入口卡片
	if _vault_card and is_instance_valid(_vault_card):
		var time_str := "%02d:%02d / 08:00" % [hrs_i, mins_i]
		var pct_str := "(%d%%)" % int(ratio * 100.0)
		if is_full:
			pct_str = "[%s]" % Loc.t("vault.max_cap")

		if _vault_time_lbl and is_instance_valid(_vault_time_lbl):
			_vault_time_lbl.text = "%s %s" % [time_str, pct_str]

		if _vault_progress_fill and _vault_progress_bg and is_instance_valid(_vault_progress_fill):
			var total_w := _vault_progress_bg.size.x
			if total_w <= 1.0:
				total_w = 280.0
			_vault_progress_fill.visible = (ratio > 0.001)
			_vault_progress_fill.size = Vector2(total_w * ratio, 8)

		if _vault_claim_btn and is_instance_valid(_vault_claim_btn):
			if gold > 0 or scrap > 0:
				_vault_claim_btn.text = "%s (+%d金 +%d鐵)" % [Loc.t("vault.btn_claim"), gold, scrap]
			else:
				_vault_claim_btn.text = Loc.t("vault.charging")

	# 2. 更新中央日晷展台旁微動氣泡 (Vault Bubble)
	if _vault_bubble and is_instance_valid(_vault_bubble):
		if _vault_bubble_time_lbl and is_instance_valid(_vault_bubble_time_lbl):
			var tmpl: String = Loc.t("vault.bubble_accumulated")
			if "%d" in tmpl:
				_vault_bubble_time_lbl.text = tmpl % [hrs_i, 8]
			else:
				_vault_bubble_time_lbl.text = "已累積 %dh / %dh" % [hrs_i, 8]
		if _vault_bubble_status_lbl and is_instance_valid(_vault_bubble_status_lbl):
			if is_full:
				_vault_bubble_status_lbl.text = Loc.t("vault.bubble_claim_ready")
				_vault_bubble_status_lbl.add_theme_color_override("font_color", COLOR_GOLD)
			elif gold > 0 or scrap > 0:
				_vault_bubble_status_lbl.text = Loc.t("vault.btn_claim")
				_vault_bubble_status_lbl.add_theme_color_override("font_color", Color("#4ED86A"))
			else:
				_vault_bubble_status_lbl.text = Loc.t("vault.charging")
				_vault_bubble_status_lbl.add_theme_color_override("font_color", Color("#C9BFA8"))

		if is_full:
			_start_vault_bubble_full_glow()
		else:
			_stop_vault_bubble_full_glow()

## 建立中央日晷展台旁發條儲能庫微動氣泡 (Vault Bubble)
func _build_vault_bubble(parent_anchor: Control) -> void:
	if parent_anchor == null:
		return

	_load_vault_bubble_key_textures()

	_vault_bubble = Control.new()
	_vault_bubble.name = "VaultBubble"
	_vault_bubble.custom_minimum_size = Vector2(160, 52)
	_vault_bubble.size = Vector2(160, 52)
	_vault_bubble.z_index = 6
	# 放置在中央英雄日晷展台右側旁，自然懸浮於展台與主角右側 (x=115, y=10)
	_vault_bubble.position = Vector2(115, 10)
	parent_anchor.add_child(_vault_bubble)

	# 0. 金黃呼吸光暈底板 (滿 8 小時時呼吸發光)
	_vault_bubble_glow_panel = Panel.new()
	_vault_bubble_glow_panel.name = "VaultBubbleGlow"
	_vault_bubble_glow_panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	_vault_bubble_glow_panel.offset_left = -4
	_vault_bubble_glow_panel.offset_top = -4
	_vault_bubble_glow_panel.offset_right = 4
	_vault_bubble_glow_panel.offset_bottom = 4
	_vault_bubble_glow_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_vault_bubble_glow_panel.visible = false
	var glow_sb := StyleBoxFlat.new()
	glow_sb.bg_color = Color(1.0, 0.82, 0.2, 0.20)
	glow_sb.border_color = Color(1.0, 0.85, 0.28, 0.95)
	glow_sb.set_border_width_all(2)
	glow_sb.set_corner_radius_all(20)
	glow_sb.shadow_color = Color(1.0, 0.82, 0.2, 0.75)
	glow_sb.shadow_size = 14
	_vault_bubble_glow_panel.add_theme_stylebox_override("panel", glow_sb)
	_vault_bubble.add_child(_vault_bubble_glow_panel)

	# 1. 氣泡主體按鈕（果凍厚底，熱區 >= 48px）
	_vault_bubble_btn = Button.new()
	_vault_bubble_btn.name = "VaultBubbleBtn"
	_vault_bubble_btn.set_anchors_preset(Control.PRESET_FULL_RECT)
	_vault_bubble_btn.custom_minimum_size = Vector2(160, 52)
	_vault_bubble_btn.focus_mode = Control.FOCUS_NONE

	var normal_sb := StyleBoxFlat.new()
	normal_sb.bg_color = Color(0.13, 0.10, 0.18, 0.92) # 蒸汽黑曜金屬板件
	normal_sb.border_color = Color(0.83, 0.68, 0.22, 0.90) # 古典黃銅邊飾
	normal_sb.set_border_width_all(2)
	normal_sb.border_width_bottom = 5 # 果凍厚底 5px
	normal_sb.set_corner_radius_all(18)
	normal_sb.content_margin_left = 10
	normal_sb.content_margin_right = 12
	normal_sb.content_margin_top = 4
	normal_sb.content_margin_bottom = 8
	normal_sb.shadow_color = Color(0.08, 0.06, 0.16, 0.40)
	normal_sb.shadow_size = 8
	normal_sb.shadow_offset = Vector2(0, 3)

	var pressed_sb := StyleBoxFlat.new()
	pressed_sb.bg_color = Color(0.18, 0.14, 0.24, 0.95)
	pressed_sb.border_color = Color(1.0, 0.85, 0.28, 1.0)
	pressed_sb.set_border_width_all(2)
	pressed_sb.border_width_bottom = 2
	pressed_sb.set_corner_radius_all(18)
	pressed_sb.content_margin_left = 10
	pressed_sb.content_margin_right = 12
	pressed_sb.content_margin_top = 6
	pressed_sb.content_margin_bottom = 6

	_vault_bubble_btn.add_theme_stylebox_override("normal", normal_sb)
	_vault_bubble_btn.add_theme_stylebox_override("hover", normal_sb)
	_vault_bubble_btn.add_theme_stylebox_override("pressed", pressed_sb)

	_vault_bubble_btn.pressed.connect(func():
		open_clockwork_vault()
	)
	_vault_bubble.add_child(_vault_bubble_btn)

	# 2. 氣泡內容容器 (水平排列: 8幀發條圖示 + 垂直時數/狀態)
	var hb := HBoxContainer.new()
	hb.set_anchors_preset(Control.PRESET_FULL_RECT)
	hb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hb.add_theme_constant_override("separation", 8)
	hb.alignment = BoxContainer.ALIGNMENT_CENTER
	_vault_bubble.add_child(hb)

	# 2.1 8 幀發條旋轉圖示
	_vault_bubble_key_icon = TextureRect.new()
	_vault_bubble_key_icon.name = "VaultBubbleKeyIcon"
	_vault_bubble_key_icon.custom_minimum_size = Vector2(32, 32)
	_vault_bubble_key_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_vault_bubble_key_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_vault_bubble_key_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_vault_bubble_key_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	if not _vault_bubble_key_textures.is_empty():
		_vault_bubble_key_icon.texture = _vault_bubble_key_textures[0]
	hb.add_child(_vault_bubble_key_icon)

	# 2.2 垂直文字區塊 (時間 + 狀態)
	var vb := VBoxContainer.new()
	vb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vb.add_theme_constant_override("separation", 1)
	vb.alignment = BoxContainer.ALIGNMENT_CENTER
	hb.add_child(vb)

	_vault_bubble_time_lbl = Label.new()
	_vault_bubble_time_lbl.name = "BubbleTimeLabel"
	_vault_bubble_time_lbl.text = "0h / 8h"
	_vault_bubble_time_lbl.add_theme_font_size_override("font_size", 12)
	_vault_bubble_time_lbl.add_theme_color_override("font_color", Color("#FFFDF8"))
	if _cached_font:
		_vault_bubble_time_lbl.add_theme_font_override("font", _cached_font)
	vb.add_child(_vault_bubble_time_lbl)

	_vault_bubble_status_lbl = Label.new()
	_vault_bubble_status_lbl.name = "BubbleStatusLabel"
	_vault_bubble_status_lbl.text = Loc.t("vault.charging")
	_vault_bubble_status_lbl.add_theme_font_size_override("font_size", 11)
	_vault_bubble_status_lbl.add_theme_color_override("font_color", Color("#C9BFA8"))
	if _cached_font:
		_vault_bubble_status_lbl.add_theme_font_override("font", _cached_font)
	vb.add_child(_vault_bubble_status_lbl)

	_start_vault_bubble_float_tween()

func _load_vault_bubble_key_textures() -> void:
	if not _vault_bubble_key_textures.is_empty():
		return
	for p in VAULT_BUBBLE_KEY_FRAME_PATHS:
		if ResourceLoader.exists(p):
			var base_tex: Texture2D = load(p) as Texture2D
			if base_tex:
				var atlas := AtlasTexture.new()
				atlas.atlas = base_tex
				atlas.region = Rect2(138, 256, 58, 80)
				_vault_bubble_key_textures.append(atlas)

func step_vault_bubble_frame() -> void:
	if _vault_bubble_key_textures.is_empty():
		return
	_vault_bubble_frame_idx = (_vault_bubble_frame_idx + 1) % _vault_bubble_key_textures.size()
	if _vault_bubble_key_icon and is_instance_valid(_vault_bubble_key_icon):
		_vault_bubble_key_icon.texture = _vault_bubble_key_textures[_vault_bubble_frame_idx]

func _start_vault_bubble_float_tween() -> void:
	if _vault_bubble_float_tween and _vault_bubble_float_tween.is_valid():
		_vault_bubble_float_tween.kill()
	if _vault_bubble == null or not is_instance_valid(_vault_bubble):
		return
	var base_y := _vault_bubble.position.y
	_vault_bubble_float_tween = create_tween().set_loops()
	_vault_bubble_float_tween.tween_property(_vault_bubble, "position:y", base_y - 3.5, 1.2).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_vault_bubble_float_tween.tween_property(_vault_bubble, "position:y", base_y + 3.5, 1.2).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

func _start_vault_bubble_full_glow() -> void:
	if _vault_bubble_is_full_glow:
		return
	_vault_bubble_is_full_glow = true
	if _vault_bubble_glow_panel and is_instance_valid(_vault_bubble_glow_panel):
		_vault_bubble_glow_panel.visible = true
	if _vault_bubble_glow_tween and _vault_bubble_glow_tween.is_valid():
		_vault_bubble_glow_tween.kill()
	if _vault_bubble_glow_panel == null or not is_instance_valid(_vault_bubble_glow_panel):
		return
	_vault_bubble_glow_tween = create_tween().set_loops()
	_vault_bubble_glow_tween.tween_property(_vault_bubble_glow_panel, "modulate:a", 1.0, 0.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_vault_bubble_glow_tween.tween_property(_vault_bubble_glow_panel, "modulate:a", 0.35, 0.8).set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)

func _stop_vault_bubble_full_glow() -> void:
	_vault_bubble_is_full_glow = false
	if _vault_bubble_glow_tween and _vault_bubble_glow_tween.is_valid():
		_vault_bubble_glow_tween.kill()
	if _vault_bubble_glow_panel and is_instance_valid(_vault_bubble_glow_panel):
		_vault_bubble_glow_panel.visible = false
		_vault_bubble_glow_panel.modulate.a = 1.0

func get_vault_bubble() -> Control:
	return _vault_bubble

func get_vault_bubble_button() -> Button:
	return _vault_bubble_btn

func get_vault_bubble_key_icon() -> TextureRect:
	return _vault_bubble_key_icon

func get_vault_bubble_time_label() -> Label:
	return _vault_bubble_time_lbl

func get_vault_bubble_status_label() -> Label:
	return _vault_bubble_status_lbl

func get_vault_bubble_glow_panel() -> Panel:
	return _vault_bubble_glow_panel

func get_vault_bubble_key_textures() -> Array[Texture2D]:
	return _vault_bubble_key_textures

func get_vault_bubble_frame_index() -> int:
	return _vault_bubble_frame_idx

func is_vault_bubble_full_glow() -> bool:
	return _vault_bubble_is_full_glow

## 開啟發條儲能庫放置收益彈窗
func open_clockwork_vault() -> Control:
	var existing = get_node_or_null("ClockworkVaultDialog")
	if existing != null:
		return existing
	var VaultClass: GDScript = load("res://scripts/ui/clockwork_vault_dialog.gd")
	if VaultClass == null:
		push_error("無法載入 ClockworkVaultDialog")
		return null
	var dlg: Control = VaultClass.new() as Control
	dlg.z_index = 80
	if _equip_schematic and is_instance_valid(_equip_schematic):
		_equip_schematic.visible = false
	dlg.rewards_claimed.connect(func(g: int, s: int):
		refresh_hud()
		refresh_vault_display()
		_show_toast(Loc.t("vault.claimed_toast") % [g, s])
	)
	dlg.tree_exited.connect(func():
		if _equip_schematic and is_instance_valid(_equip_schematic):
			_equip_schematic.visible = true
		refresh_hud()
		refresh_vault_display()
	)
	add_child(dlg)
	return dlg

func get_settings_button() -> Button:
	return _settings_button

func get_shop_button() -> Button:
	return _shop_button

func get_sortie_button() -> Button:
	return _sortie_button

func get_hall_buttons() -> Array[Button]:
	return _hall_buttons

func select_hall_card(idx: int) -> void:
	_select_hall_card(idx)

func _select_hall_card(idx: int) -> void:
	_active_hall_index = idx
	for i in range(_hall_buttons.size()):
		_style_hall_card(_hall_buttons[i], i == idx)

func _style_hall_card(btn: Button, is_active: bool) -> void:
	var sb := StyleBoxFlat.new()
	if is_active:
		sb.bg_color = COLOR_ORANGE
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 6
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 6
		sb.content_margin_bottom = 8
		sb.content_margin_left = 12
		sb.content_margin_right = 12
		sb.shadow_color = Color(0.83, 0.68, 0.22, 0.35)
		sb.shadow_size = 8
		sb.shadow_offset = Vector2(0, 4)
		btn.add_theme_color_override("font_color", Color("#FFFFFF"))
		btn.add_theme_color_override("font_hover_color", Color("#FFFFFF"))
		btn.add_theme_color_override("font_pressed_color", Color("#FFFFFF"))
	else:
		# 半透明蒸汽發條黃銅金屬板件 (淘汰純白高光，視覺焦點100%讓給中央主角)
		sb.bg_color = Color(0.12, 0.10, 0.16, 0.78)
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 4
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 6
		sb.content_margin_bottom = 8
		sb.content_margin_left = 12
		sb.content_margin_right = 12
		sb.shadow_color = Color(0.08, 0.06, 0.14, 0.25)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		btn.add_theme_color_override("font_color", Color("#FFF5E0"))
		btn.add_theme_color_override("font_hover_color", Color("#FFD028"))
		btn.add_theme_color_override("font_pressed_color", Color("#FFF5E0"))

	var sb_h := sb.duplicate() as StyleBoxFlat
	if not is_active:
		sb_h.bg_color = Color(0.20, 0.16, 0.26, 0.85)
		sb_h.border_color = Color("#D4AF37")
	else:
		sb_h.bg_color = Color("#FFB84D")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2
	sb_p.content_margin_top = 8
	sb_p.content_margin_bottom = 6
	sb_p.shadow_size = 2
	sb_p.shadow_offset = Vector2(0, 1)

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb_h)

	var t_lbl := btn.get_node_or_null("TextContainer/TitleLabel") as Label
	var s_lbl := btn.get_node_or_null("TextContainer/SubtitleLabel") as Label
	if t_lbl:
		if _cached_font:
			t_lbl.add_theme_font_override("font", _cached_font)
		t_lbl.add_theme_font_size_override("font_size", 15)
		if is_active:
			t_lbl.add_theme_color_override("font_color", Color("#FFFFFF"))
			t_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
			t_lbl.add_theme_constant_override("outline_size", 3)
		else:
			t_lbl.add_theme_color_override("font_color", Color("#FFF5E0"))
			t_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
			t_lbl.add_theme_constant_override("outline_size", 3)
	if s_lbl:
		if _cached_font:
			s_lbl.add_theme_font_override("font", _cached_font)
		s_lbl.add_theme_font_size_override("font_size", 10)
		if is_active:
			s_lbl.add_theme_color_override("font_color", Color("#4A240A"))
			s_lbl.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.95))
			s_lbl.add_theme_constant_override("outline_size", 1)
		else:
			s_lbl.add_theme_color_override("font_color", Color("#D4AF37"))
			s_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
			s_lbl.add_theme_constant_override("outline_size", 1)

func _add_hall_card(parent: Container, title: String, subtitle_or_cb = null, icon_res_or_symbol: String = "", cb_fallback: Callable = Callable()) -> Button:
	var cb: Callable
	if subtitle_or_cb is Callable:
		cb = subtitle_or_cb
	elif cb_fallback.is_valid():
		cb = cb_fallback
	else:
		cb = Callable()

	var btn := Button.new()
	btn.name = "HallCard_" + title
	btn.add_to_group("hall_cards")
	btn.set_meta("hall_title", _t(title))
	btn.set_meta("hall_title_key", title)
	var sub_str := ""
	if subtitle_or_cb is String:
		sub_str = subtitle_or_cb
		btn.set_meta("hall_subtitle", _t(sub_str))
		btn.set_meta("hall_subtitle_key", sub_str)
	btn.custom_minimum_size = Vector2(196, 50)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.text = ""

	# 依 title 或 icon_res_or_symbol 掛載自繪圖示
	var icon_path := icon_res_or_symbol
	if icon_path.is_empty() or not icon_path.begins_with("res://"):
		var icon_map := {
			"鐵匠": "res://assets/icons/hud/icon_hall_forge.png",
			"工坊": "res://assets/icons/hud/icon_hall_gem.png",
			"演武": "res://assets/icons/hud/icon_hall_arena.png",
			"委託": "res://assets/icons/hud/icon_hall_quest.png",
		}
		for k in icon_map:
			if title.find(k) >= 0:
				icon_path = icon_map[k]
				break

	if not icon_path.is_empty() and ResourceLoader.exists(icon_path):
		btn.icon = load(icon_path)
		btn.expand_icon = true
		btn.add_theme_constant_override("icon_max_width", 32)
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT

	# 蒸汽發條黃銅雙層內飾邊 (Brass Trim)
	var metal_trim := Panel.new()
	metal_trim.name = "MetalTrim"
	metal_trim.set_anchors_preset(Control.PRESET_FULL_RECT)
	metal_trim.offset_left = 3
	metal_trim.offset_top = 3
	metal_trim.offset_right = -3
	metal_trim.offset_bottom = -5
	metal_trim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var mtsb := StyleBoxFlat.new()
	mtsb.draw_center = false
	mtsb.border_color = Color(0.83, 0.68, 0.22, 0.55)
	mtsb.set_border_width_all(1)
	mtsb.set_corner_radius_all(16)
	metal_trim.add_theme_stylebox_override("panel", mtsb)
	btn.add_child(metal_trim)

	# 內部文字排版：主標題 + 副標題
	var tc := VBoxContainer.new()
	tc.name = "TextContainer"
	tc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tc.set_anchors_preset(Control.PRESET_FULL_RECT)
	tc.offset_left = 50
	tc.offset_right = -6
	tc.offset_top = 3
	tc.offset_bottom = -5
	tc.alignment = BoxContainer.ALIGNMENT_CENTER
	tc.add_theme_constant_override("separation", 1)
	btn.add_child(tc)

	var cur_loc := ContentLoc.locale()
	var t_translated := _t(title)
	var s_translated := _t(sub_str) if not sub_str.is_empty() else ""

	var t_lbl := Label.new()
	t_lbl.name = "TitleLabel"
	t_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	t_lbl.text = t_translated
	t_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if _cached_font:
		t_lbl.add_theme_font_override("font", _cached_font)
	if cur_loc in ["en", "es"] and t_translated.length() > 14:
		t_lbl.add_theme_font_size_override("font_size", 13)
	else:
		t_lbl.add_theme_font_size_override("font_size", 15)
	t_lbl.add_theme_color_override("font_color", Color("#FFF5E0"))
	t_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	t_lbl.add_theme_constant_override("outline_size", 3)
	tc.add_child(t_lbl)

	var s_lbl := Label.new()
	s_lbl.name = "SubtitleLabel"
	s_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	s_lbl.text = s_translated
	s_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if _cached_font:
		s_lbl.add_theme_font_override("font", _cached_font)
	s_lbl.add_theme_font_size_override("font_size", 10)
	s_lbl.add_theme_color_override("font_color", Color("#D4AF37"))
	s_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	s_lbl.add_theme_constant_override("outline_size", 1)
	tc.add_child(s_lbl)

	var card_idx := _hall_buttons.size()
	_hall_buttons.append(btn)
	_style_hall_card(btn, false)

	btn.pressed.connect(func():
		_select_hall_card(card_idx)
		if cb.is_valid():
			cb.call()
	)

	parent.add_child(btn)
	return btn

func _add_texture_button(parent: Container, tex_path: String, sz: Vector2, cb: Callable) -> void:
	var tb := TextureButton.new()
	tb.custom_minimum_size = sz
	tb.ignore_texture_size = true
	tb.stretch_mode = TextureButton.STRETCH_KEEP_ASPECT_CENTERED
	if ResourceLoader.exists(tex_path):
		tb.texture_normal = load(tex_path)
	tb.pressed.connect(cb)
	parent.add_child(tb)

## ──────────────────────────────────────────
## 點擊主角：切換動態姿態 + 爆發黃金以太粒子 + 氣泡
## ──────────────────────────────────────────
func _update_speech_bubble_text() -> void:
	if not _speech_label or not is_instance_valid(_speech_label):
		return
	if _current_speech_index < 0 or _current_speech_index >= HERO_SPEECH_KEYS.size():
		_current_speech_index = 1
	var cur_loc := ContentLoc.locale()
	if cur_loc in ["en", "es"]:
		_speech_label.add_theme_font_size_override("font_size", 13)
	else:
		_speech_label.add_theme_font_size_override("font_size", 14)
	_speech_label.text = _t(HERO_SPEECH_KEYS[_current_speech_index])

func _on_hero_clicked(forced_act: int = -1, forced_speech: int = -1) -> void:
	_is_interacting = true
	var act_type := forced_act if forced_act >= 0 else (randi() % 3)

	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()

	if _hero_key_avatar:
		_hero_key_avatar.visible = false

	if forced_speech >= 0 and forced_speech < HERO_SPEECH_KEYS.size():
		_current_speech_index = forced_speech
	else:
		_current_speech_index = randi() % HERO_SPEECH_KEYS.size()
	_update_speech_bubble_text()
	if _speech_bubble:
		_speech_bubble.visible = true
		_speech_bubble.modulate.a = 0.0

		if _bubble_tween and _bubble_tween.is_valid():
			_bubble_tween.kill()
		_bubble_tween = create_tween()
		_bubble_tween.tween_property(_speech_bubble, "modulate:a", 1.0, 0.15)
		_bubble_tween.tween_interval(0.7)
		_bubble_tween.tween_property(_speech_bubble, "modulate:a", 0.0, 0.15)
		_bubble_tween.tween_callback(func(): _speech_bubble.visible = false)

	## 噴散喜悅星芒與發條火花微粒
	if _hero_avatar:
		_burst_click_particles(_hero_avatar.global_position + Vector2(160, 160))

	if _poke_tween and _poke_tween.is_valid():
		_poke_tween.kill()
	var tw := create_tween()
	_poke_tween = tw

	# 先賦予動作姿態貼圖 (確保測試同步讀取到 512x512 貼圖)
	match act_type:
		0:
			if _tex_attack and _hero_avatar:
				_hero_avatar.texture = _tex_attack
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		1:
			if _tex_skill and _hero_avatar:
				_hero_avatar.texture = _tex_skill
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		2:
			if _tex_telegraph and _hero_avatar:
				_hero_avatar.texture = _tex_telegraph
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR

	# 觸發果凍擠壓彈跳動效 (Squash & Stretch: Scale 稍微壓扁再彈高回正)
	_hero_avatar.pivot_offset = Vector2(160, 260)
	# 1. 壓扁 (Squash)
	tw.tween_property(_hero_avatar, "scale", Vector2(1.18, 0.82), 0.08).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	if _hero_shadow:
		tw.parallel().tween_property(_hero_shadow, "scale", Vector2(1.18, 1.18), 0.08)
	if _hero_contact_shadow:
		tw.parallel().tween_property(_hero_contact_shadow, "scale", Vector2(1.22, 1.22), 0.08)
	# 2. 彈高 (Stretch)
	tw.tween_property(_hero_avatar, "scale", Vector2(0.88, 1.16), 0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	if _hero_shadow:
		tw.parallel().tween_property(_hero_shadow, "scale", Vector2(0.85, 0.85), 0.14)
	if _hero_contact_shadow:
		tw.parallel().tween_property(_hero_contact_shadow, "scale", Vector2(0.68, 0.68), 0.14)
	# 3. 微微回彈
	tw.tween_property(_hero_avatar, "scale", Vector2(1.04, 0.96), 0.10).set_trans(Tween.TRANS_SINE)
	# 4. 回正
	tw.tween_property(_hero_avatar, "scale", Vector2(1.0, 1.0), 0.08).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		tw.parallel().tween_property(_hero_shadow, "scale", Vector2(1.0, 1.0), 0.08)
	if _hero_contact_shadow:
		tw.parallel().tween_property(_hero_contact_shadow, "scale", Vector2(1.0, 1.0), 0.08)

	match act_type:
		0:
			## 揮劍劈砍姿態位移
			tw.parallel().tween_property(_hero_avatar, "position", Vector2(-110, -165), 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT).set_delay(0.08)
			tw.tween_property(_hero_avatar, "position", Vector2(-125, -140), 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.tween_interval(0.3)
			tw.tween_callback(func():
				if _tex_recover and _hero_avatar:
					_hero_avatar.texture = _tex_recover
					_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			)
			tw.tween_interval(0.3)
			tw.tween_callback(_restore_hero_idle)
		1:
			## 聚氣勝利姿態
			tw.tween_interval(0.6)
			tw.tween_callback(_restore_hero_idle)
		2:
			## 靈巧後翻大跳躍
			tw.parallel().tween_property(_hero_avatar, "position:y", -175.0, 0.15).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT).set_delay(0.08)
			tw.parallel().tween_property(_hero_avatar, "scale:x", -1.0, 0.15).set_delay(0.08)
			tw.tween_property(_hero_avatar, "position:y", -140.0, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", 1.0, 0.18)
			tw.tween_interval(0.2)
			tw.tween_callback(_restore_hero_idle)

func _burst_click_particles(center_pos: Vector2) -> void:
	var gp := get_node_or_null("/root/GraphicsProfile")
	var n := 10
	if gp != null:
		n = int(gp.particle_count(10))
	if n <= 0:
		return
	var cols: Array[Color] = [
		COLOR_GOLD,
		COLOR_ORANGE,
		COLOR_PINK,
		COLOR_SKY,
		Color(0.98, 0.92, 0.55),
		TEAL_CORE
	]
	for i in range(n):
		var star := ColorRect.new()
		star.name = "BurstParticle_%d" % i
		star.add_to_group("burst_particles")
		var sz := 6.0
		star.custom_minimum_size = Vector2(sz, sz)
		star.size = Vector2(sz, sz)
		star.pivot_offset = Vector2(sz * 0.5, sz * 0.5)
		star.rotation = PI * 0.25
		star.color = cols[i % cols.size()]
		star.global_position = center_pos - Vector2(sz * 0.5, sz * 0.5)
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(star)

		var angle := float(i) * (PI * 2.0 / float(n)) + randf_range(-0.15, 0.15)
		var dist := randf_range(50.0, 95.0)
		var target := center_pos + Vector2(cos(angle), sin(angle)) * dist

		var tw := create_tween()
		star.scale = Vector2(0.4, 0.4)
		tw.tween_property(star, "scale", Vector2(1.3, 1.3), 0.10).set_trans(Tween.TRANS_BACK)
		tw.parallel().tween_property(star, "global_position", target, 0.38).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(star, "rotation", star.rotation + PI * 0.75, 0.38)
		tw.tween_property(star, "scale", Vector2(0.2, 0.2), 0.20)
		tw.parallel().tween_property(star, "modulate:a", 0.0, 0.20).set_delay(0.10)
		tw.tween_callback(star.queue_free)

## ──────────────────────────────────────────
## Tab 4: 聚魂殿堂 (以太祭壇封靈罐四階)
## ──────────────────────────────────────────
func _build_soul_hall_tab() -> void:
	_soul_layer = Control.new()
	_soul_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_soul_layer.visible = false
	_content_root.add_child(_soul_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	var psb := StyleBoxFlat.new()
	psb.bg_color = COLOR_CARD_WARM
	psb.border_color = COLOR_BORDER
	psb.set_border_width_all(2)
	psb.border_width_bottom = 5
	psb.set_corner_radius_all(20)
	psb.content_margin_left = 20
	psb.content_margin_right = 20
	psb.content_margin_top = 16
	psb.content_margin_bottom = 16
	psb.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
	psb.shadow_size = 8
	psb.shadow_offset = Vector2(0, 4)
	panel.add_theme_stylebox_override("panel", psb)
	_soul_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 16)
	panel.add_child(v)

	var t := Label.new()
	t.text = _t("聚魂殿 · 封靈罐四階")
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	t.add_theme_font_size_override("font_size", 24)
	t.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	v.add_child(t)
	_soul_title_label = t

	var desc := Label.new()
	desc.text = _t("聚引四大共鳴核心之魂：銳齒(攻) · 固甲(防) · 旋簧(血) · 全衡(衡)。點擊點亮更高階封靈罐！")
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 13)
	desc.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	v.add_child(desc)
	_soul_desc_label = desc

	var gourd_row := HBoxContainer.new()
	gourd_row.alignment = BoxContainer.ALIGNMENT_CENTER
	gourd_row.add_theme_constant_override("separation", 14)
	v.add_child(gourd_row)

	var gourds_data := [
		{"name": _t("綠階封靈罐"), "cost": 80, "color": TEAL_CORE},
		{"name": _t("藍階封靈罐"), "cost": 200, "color": STEEL_BLUE},
		{"name": _t("紫階封靈罐"), "cost": 500, "color": Color(0.68, 0.45, 0.90)},
		{"name": _t("橙階封靈罐"), "cost": 1000, "color": GOLD_CLASSICAL}
	]

	_gourd_btns.clear()
	for i in range(gourds_data.size()):
		var gd: Dictionary = gourds_data[i]
		var gb := _build_gourd_card(gd, i)
		gourd_row.add_child(gb)
		_gourd_btns.append(gb)

	_refresh_gourds_ui()

	var bot_h := HBoxContainer.new()
	bot_h.alignment = BoxContainer.ALIGNMENT_CENTER
	bot_h.add_theme_constant_override("separation", 28)
	v.add_child(bot_h)

	var btn_absorb := Button.new()
	btn_absorb.name = "BtnAbsorb"
	btn_absorb.text = _t("一鍵吸收灰魂")
	btn_absorb.custom_minimum_size = Vector2(210, 52)
	btn_absorb.add_theme_font_size_override("font_size", 16)
	var asb := StyleBoxFlat.new()
	asb.bg_color = COLOR_ORANGE
	asb.border_color = COLOR_BORDER
	asb.set_border_width_all(2)
	asb.border_width_bottom = 5
	asb.set_corner_radius_all(18)
	asb.content_margin_top = 8
	asb.content_margin_bottom = 8
	asb.content_margin_left = 14
	asb.content_margin_right = 14
	asb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	asb.shadow_size = 6
	asb.shadow_offset = Vector2(0, 3)
	var asb_h := asb.duplicate() as StyleBoxFlat
	asb_h.bg_color = Color("#FFB84D")
	var asb_p := asb.duplicate() as StyleBoxFlat
	asb_p.border_width_bottom = 2
	btn_absorb.add_theme_stylebox_override("normal", asb)
	btn_absorb.add_theme_stylebox_override("hover", asb_h)
	btn_absorb.add_theme_stylebox_override("pressed", asb_p)
	btn_absorb.add_theme_stylebox_override("focus", asb)
	btn_absorb.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_absorb.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_absorb.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	btn_absorb.pressed.connect(func():
		_show_toast(_t("已將廢魂轉化為 480 戰魂經驗值！"))
	)
	bot_h.add_child(btn_absorb)
	_gourd_btn_absorb = btn_absorb

	var btn_draw := Button.new()
	btn_draw.name = "BtnDrawTen"
	btn_draw.text = _t("聚魂十連")
	btn_draw.custom_minimum_size = Vector2(220, 56)
	btn_draw.add_theme_font_size_override("font_size", 18)
	var dsb := StyleBoxFlat.new()
	dsb.bg_color = COLOR_GOLD
	dsb.border_color = COLOR_BORDER
	dsb.set_border_width_all(2)
	dsb.border_width_bottom = 5
	dsb.set_corner_radius_all(18)
	dsb.content_margin_top = 8
	dsb.content_margin_bottom = 8
	dsb.content_margin_left = 16
	dsb.content_margin_right = 16
	dsb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
	dsb.shadow_size = 6
	dsb.shadow_offset = Vector2(0, 3)
	var dsb_h := dsb.duplicate() as StyleBoxFlat
	dsb_h.bg_color = Color("#FFE066")
	var dsb_p := dsb.duplicate() as StyleBoxFlat
	dsb_p.border_width_bottom = 2
	btn_draw.add_theme_stylebox_override("normal", dsb)
	btn_draw.add_theme_stylebox_override("hover", dsb_h)
	btn_draw.add_theme_stylebox_override("pressed", dsb_p)
	btn_draw.add_theme_stylebox_override("focus", dsb)
	btn_draw.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_draw.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_draw.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	btn_draw.pressed.connect(func(): _do_gourd_draw(0, true))
	bot_h.add_child(btn_draw)
	_gourd_btn_draw = btn_draw

func _build_gourd_card(gd: Dictionary, idx: int) -> Button:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(145, 170)
	btn.name = "GourdBtn_%d" % idx

	var v := VBoxContainer.new()
	v.name = "Content"
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 10)
	btn.add_child(v)

	var circle := PanelContainer.new()
	circle.custom_minimum_size = Vector2(56, 56)
	circle.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	circle.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var csb := StyleBoxFlat.new()
	csb.bg_color = gd["color"] as Color
	csb.set_corner_radius_all(28)
	csb.border_color = COLOR_BORDER
	csb.set_border_width_all(2)
	circle.add_theme_stylebox_override("panel", csb)
	v.add_child(circle)

	var nl := Label.new()
	nl.name = "NameLabel"
	nl.text = str(gd["name"])
	nl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	nl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	nl.custom_minimum_size = Vector2(130, 36)
	nl.add_theme_font_size_override("font_size", 13)
	nl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	v.add_child(nl)

	var cl := Label.new()
	cl.name = "CostLabel"
	cl.text = "%s %d" % [_t("金幣"), int(gd["cost"])]
	cl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cl.add_theme_font_size_override("font_size", 13)
	cl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	const GOURD_NAMES := ["綠階封靈罐", "藍階封靈罐", "紫階封靈罐", "橙階封靈罐"]
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
		if i < GOURD_NAMES.size():
			var nl: Label = b.find_child("NameLabel", true, false) as Label
			if nl:
				nl.text = _t(GOURD_NAMES[i])
			var cl: Label = b.find_child("CostLabel", true, false) as Label
			if cl:
				var costs := [80, 200, 500, 1000]
				cl.text = "%s %d" % [_t("金幣"), costs[i]]
		var is_lit := _gourd_lit[i]
		var sb := StyleBoxFlat.new()
		sb.set_corner_radius_all(18)
		var v_content := b.get_node_or_null("Content") as Control
		if is_lit:
			sb.bg_color = COLOR_CARD_GOLD
			sb.border_color = COLOR_BORDER
			sb.set_border_width_all(2)
			sb.border_width_bottom = 5
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
			sb.shadow_size = 6
			sb.shadow_offset = Vector2(0, 3)
			b.disabled = false
			if v_content:
				v_content.modulate = Color(1.0, 1.0, 1.0, 1.0)
			var sb_h := sb.duplicate() as StyleBoxFlat
			sb_h.bg_color = Color("#FFEAA0")
			var sb_p := sb.duplicate() as StyleBoxFlat
			sb_p.border_width_bottom = 2
			b.add_theme_stylebox_override("normal", sb)
			b.add_theme_stylebox_override("hover", sb_h)
			b.add_theme_stylebox_override("pressed", sb_p)
			b.add_theme_stylebox_override("focus", sb)
		else:
			sb.bg_color = Color("#EDE7D8")
			sb.border_color = Color(0.12, 0.10, 0.23, 0.45)
			sb.set_border_width_all(2)
			sb.border_width_bottom = 3
			sb.shadow_color = Color(0.12, 0.10, 0.23, 0.08)
			sb.shadow_size = 4
			sb.shadow_offset = Vector2(0, 2)
			b.disabled = true
			if v_content:
				v_content.modulate = Color(1.0, 1.0, 1.0, 0.5)
			b.add_theme_stylebox_override("disabled", sb)
			b.add_theme_stylebox_override("normal", sb)

func _do_gourd_draw(idx: int, is_ten: bool) -> void:
	if not _gourd_lit[idx] and not is_ten:
		return

	var roll := randf()
	if roll < 0.35 and idx < 3:
		_gourd_lit[idx + 1] = true
		_show_toast(_t("靈光閃爍！成功點亮更高階的封靈罐！"))
	else:
		for i in range(1, 4):
			_gourd_lit[i] = false
		_show_toast(_t("聚魂完畢！獲得了戰魂碎片與戰魂經驗！"))
	
	_refresh_gourds_ui()

## ──────────────────────────────────────────
## Tab 3: 四地區出征 (神殿戰情報告板)
## ──────────────────────────────────────────
func _build_adventure_tab() -> void:
	_adventure_layer = Control.new()
	_adventure_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_adventure_layer.visible = false
	_content_root.add_child(_adventure_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 40
	panel.offset_right = -40
	panel.offset_top = 16
	panel.offset_bottom = -16
	panel.add_theme_stylebox_override("panel", _create_obsidian_panel(LINE_GOLD))
	_adventure_layer.add_child(panel)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 14)
	panel.add_child(v)

	## 頂部出征子模式導航（四區主線 / 停擺巨偶入口）
	var mode_bar := HBoxContainer.new()
	mode_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	mode_bar.add_theme_constant_override("separation", 20)
	v.add_child(mode_bar)
	_submode_bar = mode_bar

	_btn_mode_regions = Button.new()
	_btn_mode_regions.name = "BtnModeRegions"
	_btn_mode_regions.text = _t("四區主線")
	_btn_mode_regions.custom_minimum_size = Vector2(240, 50)
	_btn_mode_regions.add_theme_font_size_override("font_size", 16)
	_btn_mode_regions.pressed.connect(func(): _switch_adventure_submode(AdventureSubMode.REGIONS))
	mode_bar.add_child(_btn_mode_regions)

	_btn_mode_colossus = Button.new()
	_btn_mode_colossus.name = "BtnModeColossus"
	_btn_mode_colossus.custom_minimum_size = Vector2(380, 50)
	_btn_mode_colossus.add_theme_font_size_override("font_size", 16)
	_btn_mode_colossus.pressed.connect(func(): _switch_adventure_submode(AdventureSubMode.COLOSSUS))
	mode_bar.add_child(_btn_mode_colossus)
	_refresh_colossus_mode_btn_text()

	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)
	_reg_bar = reg_bar

	_region_buttons.clear()
	for i in range(REGION_KEYS.size()):
		var rb := Button.new()
		rb.name = "RegionBtn_%d" % i
		rb.text = _t(REGION_KEYS[i])
		rb.custom_minimum_size = Vector2(230, 52)
		rb.add_theme_font_size_override("font_size", 16)
		_style_region_button(rb, i == _selected_region)
		var r_idx := i
		rb.pressed.connect(func(): _select_region(r_idx))
		reg_bar.add_child(rb)
		_region_buttons.append(rb)

	_stages_container = VBoxContainer.new()
	_stages_container.add_theme_constant_override("separation", 14)
	_stages_container.size_flags_vertical = Control.SIZE_EXPAND_FILL
	v.add_child(_stages_container)

	_refresh_adventure_submode_ui()
	_refresh_region_stages()

func _style_region_button(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	if is_selected:
		sb.bg_color = COLOR_ORANGE
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 5
		sb.set_corner_radius_all(20)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 16
		sb.content_margin_right = 16
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	else:
		sb.bg_color = COLOR_CARD_WARM
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 4
		sb.set_corner_radius_all(20)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 16
		sb.content_margin_right = 16
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_ORANGE)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var sb_h := sb.duplicate() as StyleBoxFlat
	if not is_selected:
		sb_h.bg_color = COLOR_CARD_GOLD
	else:
		sb_h.bg_color = Color("#FFB84D")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)

func _style_submode_button(btn: Button, is_selected: bool) -> void:
	if btn == null or not is_instance_valid(btn):
		return
	var sb := StyleBoxFlat.new()
	if is_selected:
		sb.bg_color = COLOR_ORANGE
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 5
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 18
		sb.content_margin_right = 18
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)
	else:
		sb.bg_color = COLOR_CARD_WARM
		sb.border_color = COLOR_BORDER
		sb.set_border_width_all(2)
		sb.border_width_bottom = 4
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 18
		sb.content_margin_right = 18
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn.add_theme_color_override("font_hover_color", COLOR_ORANGE)
		btn.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var sb_h := sb.duplicate() as StyleBoxFlat
	if not is_selected:
		sb_h.bg_color = COLOR_CARD_GOLD
	else:
		sb_h.bg_color = Color("#FFB84D")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)

func switch_adventure_submode(mode: int) -> void:
	_switch_adventure_submode(mode)

func _switch_adventure_submode(mode: int) -> void:
	_adventure_submode = mode
	_refresh_adventure_submode_ui()
	_refresh_region_stages()

func _refresh_adventure_submode_ui() -> void:
	if _reg_bar and is_instance_valid(_reg_bar):
		_reg_bar.visible = (_adventure_submode == AdventureSubMode.REGIONS)
	if _btn_mode_regions and is_instance_valid(_btn_mode_regions):
		_btn_mode_regions.text = _t("四區主線")
		_style_submode_button(_btn_mode_regions, _adventure_submode == AdventureSubMode.REGIONS)
	if _btn_mode_colossus and is_instance_valid(_btn_mode_colossus):
		_refresh_colossus_mode_btn_text()
		_style_submode_button(_btn_mode_colossus, _adventure_submode == AdventureSubMode.COLOSSUS)

func _refresh_colossus_mode_btn_text() -> void:
	if _btn_mode_colossus == null or not is_instance_valid(_btn_mode_colossus):
		return
	var left := 3
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var CDS: Node = (loop as SceneTree).root.get_node_or_null("ColossusDailySystem")
		if CDS and CDS.has_method("get_remaining_entries"):
			left = int(CDS.call("get_remaining_entries"))
	_btn_mode_colossus.text = _t("停擺巨偶 · 今日剩餘: %d/3") % left

func _on_colossus_card_pressed(s: Dictionary) -> void:
	var loop := Engine.get_main_loop()
	if not (loop is SceneTree and (loop as SceneTree).root != null):
		return
	var CDS: Node = (loop as SceneTree).root.get_node_or_null("ColossusDailySystem")
	if CDS == null:
		return
	var gs := _gs()
	var player_lv := int(gs.get("level")) if (gs and "level" in gs) else 1
	var sug_lv := int(s.get("level", 0))
	var req_lv := int(s.get("req_level", sug_lv - 10))
	if player_lv < req_lv:
		_show_toast(_t("等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！") % req_lv)
		return
	var res: Dictionary = CDS.call("try_enter", str(s.get("id", "")), player_lv)
	if bool(res.get("ok", false)):
		if gs:
			gs.set("current_suggest_lv", sug_lv)
		_show_toast(_t("今日剩餘: %d 次") % int(res.get("remaining", 0)))
		_refresh_adventure_submode_ui()
		_refresh_region_stages()
		var boss_key: String = str(s.get("boss_key", s.get("id", "")))
		request_battle.emit(boss_key)
	elif str(res.get("reason", "")) == "level_too_low":
		_show_toast(_t("等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！") % req_lv)
	else:
		_show_colossus_limit_dialog()

func _show_colossus_limit_dialog() -> Control:
	var existing = get_node_or_null("ColossusLimitDialog")
	if existing != null:
		return existing
	var dlg := Control.new()
	dlg.name = "ColossusLimitDialog"
	dlg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	dlg.mouse_filter = Control.MOUSE_FILTER_STOP
	dlg.z_index = 90

	var scrim := ResponsiveUi.make_scrim(ResponsiveUi.SCRIM_COLOR)
	dlg.add_child(scrim)
	var scrim_btn := Button.new()
	scrim_btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scrim_btn.flat = true
	var esb := StyleBoxEmpty.new()
	scrim_btn.add_theme_stylebox_override("normal", esb)
	scrim_btn.pressed.connect(func(): dlg.queue_free())
	scrim.add_child(scrim_btn)

	var center := CenterContainer.new()
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	dlg.add_child(center)

	var card := PanelContainer.new()
	card.name = "ColossusLimitCard"
	ResponsiveUi.apply_dialog_card(card)
	card.custom_minimum_size = Vector2(720, 360)
	card.add_theme_stylebox_override("panel", _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 3, 6, 22))
	center.add_child(card)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 28)
	margin.add_theme_constant_override("margin_right", 28)
	margin.add_theme_constant_override("margin_top", 24)
	margin.add_theme_constant_override("margin_bottom", 24)
	card.add_child(margin)

	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 18)
	margin.add_child(v)

	var head := HBoxContainer.new()
	v.add_child(head)

	var title_lbl := Label.new()
	title_lbl.name = "ColossusLimitTitle"
	title_lbl.text = _t("停擺巨偶挑戰")
	title_lbl.add_theme_font_size_override("font_size", 22)
	title_lbl.add_theme_color_override("font_color", COLOR_TEXT_ORANGE)
	title_lbl.add_theme_color_override("font_outline_color", COLOR_BORDER)
	title_lbl.add_theme_constant_override("outline_size", 3)
	title_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title_lbl)

	var close_btn := ResponsiveUi.make_close_button(func(): dlg.queue_free())
	head.add_child(close_btn)

	var sep := ColorRect.new()
	sep.custom_minimum_size = Vector2(0, 3)
	sep.color = COLOR_ORANGE
	v.add_child(sep)

	var desc_lbl := Label.new()
	desc_lbl.name = "ColossusLimitDesc"
	desc_lbl.text = _t("今日挑戰次數已用盡，請明天再來！") + "\n\n" + _t("每日挑戰上限 3 次，每日 00:00 自動重置挑戰次數。")
	desc_lbl.add_theme_font_size_override("font_size", 16)
	desc_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	desc_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	v.add_child(desc_lbl)

	var btn_row := HBoxContainer.new()
	btn_row.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_child(btn_row)

	var ok_btn := Button.new()
	ok_btn.name = "ConfirmButton"
	ok_btn.text = _t("確定")
	ok_btn.custom_minimum_size = Vector2(200, 52)
	ok_btn.add_theme_font_size_override("font_size", 18)
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = COLOR_GOLD
	bsb.border_color = COLOR_BORDER
	bsb.set_border_width_all(2)
	bsb.border_width_bottom = 5
	bsb.set_corner_radius_all(18)
	ok_btn.add_theme_stylebox_override("normal", bsb)
	ok_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	ok_btn.pressed.connect(func(): dlg.queue_free())
	btn_row.add_child(ok_btn)

	add_child(dlg)
	return dlg

func _select_region(r: int) -> void:
	_selected_region = r
	for i in range(_region_buttons.size()):
		_style_region_button(_region_buttons[i], i == _selected_region)
	_refresh_region_stages()

func _refresh_region_stages() -> void:
	if _stages_container == null or not is_instance_valid(_stages_container):
		return
	for c in _stages_container.get_children():
		_stages_container.remove_child(c)
		c.queue_free()

	if _adventure_submode == AdventureSubMode.COLOSSUS:
		var grid := GridContainer.new()
		grid.name = "ColossusStagesGrid"
		grid.columns = 2
		grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		grid.add_theme_constant_override("h_separation", 20)
		grid.add_theme_constant_override("v_separation", 18)
		_stages_container.add_child(grid)

		var bosses: Array = []
		var loop := Engine.get_main_loop()
		if loop is SceneTree and (loop as SceneTree).root != null:
			var CDS: Node = (loop as SceneTree).root.get_node_or_null("ColossusDailySystem")
			if CDS and CDS.has_method("get_bosses"):
				bosses = CDS.call("get_bosses")
		if bosses.is_empty():
			var ColossusClass: GDScript = load("res://scripts/systems/colossus_daily.gd")
			if ColossusClass:
				bosses = ColossusClass.BOSSES
		for b in bosses:
			var sc := _build_stage_card(b)
			grid.add_child(sc)
		return

	var all_stages := REGION_STAGES

	var stages_data: Array = []
	if _selected_region >= 0 and _selected_region < all_stages.size():
		stages_data = all_stages[_selected_region]
	else:
		stages_data = all_stages[0]

	var grid := GridContainer.new()
	grid.columns = 2
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 20)
	grid.add_theme_constant_override("v_separation", 18)
	_stages_container.add_child(grid)

	for s in stages_data:
		var sc := _build_stage_card(s)
		grid.add_child(sc)

func _build_stage_card(s: Dictionary) -> PanelContainer:
	var is_colossus: bool = bool(s.get("is_colossus", false))
	var c := PanelContainer.new()
	c.name = "StageCard_%s" % str(s.get("num", "")).replace("-", "_")
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(520, 185) if is_colossus else Vector2(520, 145)
	var csb := StyleBoxFlat.new()
	var is_boss: bool = str(s.get("type", "")).find("首領") >= 0 or is_colossus
	csb.bg_color = Color("#FFF5F0") if is_boss else COLOR_CARD_WARM
	csb.border_color = Color("#D04838") if is_boss else COLOR_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 6 if is_boss else 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 18
	csb.content_margin_right = 18
	csb.content_margin_top = 14
	csb.content_margin_bottom = 14
	csb.shadow_color = Color(0.63, 0.22, 0.16, 0.18) if is_boss else Color(0.12, 0.10, 0.23, 0.14)
	csb.shadow_size = 8
	csb.shadow_offset = Vector2(0, 3)
	c.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.alignment = BoxContainer.ALIGNMENT_CENTER
	h.add_theme_constant_override("separation", 16)
	c.add_child(h)

	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.add_theme_constant_override("separation", 6)
	h.add_child(v)

	var t_row := HBoxContainer.new()
	t_row.add_theme_constant_override("separation", 10)
	t_row.alignment = BoxContainer.ALIGNMENT_BEGIN

	var num_badge := PanelContainer.new()
	var nsb := StyleBoxFlat.new()
	nsb.bg_color = COLOR_ORANGE if is_boss else COLOR_GOLD
	nsb.border_color = COLOR_BORDER
	nsb.set_border_width_all(2)
	nsb.border_width_bottom = 3
	nsb.set_corner_radius_all(10)
	nsb.content_margin_left = 8
	nsb.content_margin_right = 8
	nsb.content_margin_top = 2
	nsb.content_margin_bottom = 2
	num_badge.add_theme_stylebox_override("panel", nsb)

	var num_l := Label.new()
	# 審核收尾 t_70cfb681：徽章編號也要過翻譯層，否則英/韓/西語會露出「巨偶-1」中文
	num_l.text = _t(str(s["num"]))
	# 字級下限：ART_DAILY_CONSTITUTION §「輔助不准再縮去塞字」；t_b8e32048 審核收尾改回 18
	num_l.add_theme_font_size_override("font_size", 18)
	num_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	num_badge.add_child(num_l)
	t_row.add_child(num_badge)

	var name_l := Label.new()
	name_l.name = "StageNameLabel"
	var stage_name := _t(str(s["name"]))
	name_l.text = stage_name
	if stage_name.length() > 32:
		name_l.add_theme_font_size_override("font_size", 14)
	elif stage_name.length() > 22:
		name_l.add_theme_font_size_override("font_size", 15)
	else:
		name_l.add_theme_font_size_override("font_size", 17)
	name_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	name_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	t_row.add_child(name_l)
	v.add_child(t_row)

	## 停擺巨偶世界觀副標（20–40 字，不截字、不換行壓住出征鈕）
	if is_colossus and s.has("blurb") and not str(s["blurb"]).is_empty():
		var blurb_l := Label.new()
		blurb_l.name = "StageBlurbLabel"
		var blurb_text := _t(str(s["blurb"]))
		blurb_l.text = blurb_text
		blurb_l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		blurb_l.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		blurb_l.add_theme_font_size_override("font_size", 12)
		blurb_l.add_theme_color_override("font_color", Color("#8C4426"))
		v.add_child(blurb_l)

	## 區域抗性門檻（綠黃紅三檔，熱區 >= 48px，多巴胺果凍厚底）
	var stage_num := str(s.get("num", ""))
	var RC = load("res://scripts/world/region_catalog.gd")
	var sug_lv := int(s.get("level", 0)) if is_colossus else (int(RC.call("expedition_suggest_lv", stage_num)) if RC else 0)
	var req_lv := int(s.get("req_level", sug_lv - 10)) if is_colossus else 0
	var player_lv := 1
	var gs := _gs()
	if gs and "level" in gs:
		player_lv = int(gs.get("level"))
	var is_locked: bool = is_colossus and (player_lv < req_lv)
	var F = load("res://scripts/battle/formulas.gd")
	var tier_info: Dictionary = F.call("resistance_tier", player_lv, sug_lv) if F else {}
	var tier: String = str(tier_info.get("tier", "safe"))
	var tier_name: String = str(tier_info.get("tier_name", "安全"))

	var res_row := HBoxContainer.new()
	res_row.add_theme_constant_override("separation", 10)
	res_row.alignment = BoxContainer.ALIGNMENT_BEGIN

	var res_badge := Button.new()
	res_badge.name = "ResistBadge"
	res_badge.custom_minimum_size = Vector2(90, 48)
	res_badge.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	res_badge.text = _t("未達標") if is_locked else _t(tier_name)
	res_badge.add_theme_font_size_override("font_size", 14)

	var rsb := StyleBoxFlat.new()
	rsb.set_border_width_all(2)
	rsb.border_width_bottom = 4
	rsb.border_color = COLOR_BORDER
	rsb.set_corner_radius_all(14)
	rsb.content_margin_left = 10
	rsb.content_margin_right = 10
	rsb.content_margin_top = 4
	rsb.content_margin_bottom = 4
	if is_locked:
		rsb.bg_color = Color("#7D7588")  ## 深灰紫（未達門檻）
	elif tier == "safe":
		rsb.bg_color = Color("#4ED86A")  ## 薄荷綠（安全）
	elif tier == "strained":
		rsb.bg_color = Color("#FFD028")  ## 金黃（吃力）
	else:
		rsb.bg_color = Color("#FF5E8A")  ## 珊瑚粉紅（過載）

	var rsb_h := rsb.duplicate() as StyleBoxFlat
	rsb_h.bg_color = rsb.bg_color.lightened(0.12)
	var rsb_p := rsb.duplicate() as StyleBoxFlat
	rsb_p.border_width_bottom = 2

	res_badge.add_theme_stylebox_override("normal", rsb)
	res_badge.add_theme_stylebox_override("hover", rsb_h)
	res_badge.add_theme_stylebox_override("pressed", rsb_p)
	res_badge.add_theme_stylebox_override("focus", rsb)
	if is_locked:
		res_badge.add_theme_color_override("font_color", Color("#F5F3F8"))
		res_badge.add_theme_color_override("font_hover_color", Color("#FFFFFF"))
		res_badge.add_theme_color_override("font_pressed_color", Color("#E0DCE8"))
	else:
		res_badge.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		res_badge.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
		res_badge.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var toast_msg := ""
	if is_locked:
		toast_msg = _t("等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！") % req_lv
	elif tier == "safe":
		toast_msg = _t("區域抗性安全：等級達標，受傷正常 (×1.0)")
	elif tier == "strained":
		toast_msg = _t("區域抗性吃力：未達建議 Lv%d，受到傷害 ×1.2") % sug_lv
	else:
		toast_msg = _t("區域抗性過載：低於建議 Lv%d 超過 5 級，受到傷害 ×1.5！") % sug_lv
	res_badge.pressed.connect(func(): _show_toast(toast_msg))
	res_row.add_child(res_badge)

	var res_hint_l := Label.new()
	res_hint_l.name = "ResistHintLabel"
	res_hint_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	res_hint_l.add_theme_font_size_override("font_size", 13)
	if is_locked:
		res_hint_l.text = (_t("推薦 Lv.%d") % sug_lv) + " · " + (_t("未達 Lv.%d 不可出征") % req_lv)
		res_hint_l.add_theme_color_override("font_color", Color("#A03828"))
	elif is_colossus:
		if tier == "safe":
			res_hint_l.text = _t("推薦 Lv.%d") % sug_lv
			res_hint_l.add_theme_color_override("font_color", Color("#2E7D32"))
		elif tier == "strained":
			res_hint_l.text = (_t("推薦 Lv.%d") % sug_lv) + " · " + _t("受傷 ×1.2")
			res_hint_l.add_theme_color_override("font_color", Color("#9A6200"))
		else:
			res_hint_l.text = (_t("推薦 Lv.%d") % sug_lv) + " · " + _t("受傷 ×1.5")
			res_hint_l.add_theme_color_override("font_color", Color("#C0392B"))
	else:
		if tier == "safe":
			res_hint_l.text = _t("建議 Lv.%d") % sug_lv
			res_hint_l.add_theme_color_override("font_color", Color("#2E7D32"))
		elif tier == "strained":
			res_hint_l.text = (_t("建議 Lv.%d") % sug_lv) + " · " + _t("受傷 ×1.2")
			res_hint_l.add_theme_color_override("font_color", Color("#9A6200"))
		else:
			res_hint_l.text = (_t("建議 Lv.%d") % sug_lv) + " · " + _t("受傷 ×1.5")
			res_hint_l.add_theme_color_override("font_color", Color("#C0392B"))
	res_row.add_child(res_hint_l)
	v.add_child(res_row)

	var inf_row := HBoxContainer.new()
	inf_row.add_theme_constant_override("separation", 12)

	var typ_badge := PanelContainer.new()
	var tsb := StyleBoxFlat.new()
	tsb.bg_color = Color("#FFE4D6") if is_boss else Color("#EDE7D8")
	tsb.border_color = Color("#D04838") if is_boss else Color(0.12, 0.10, 0.23, 0.35)
	tsb.set_border_width_all(1)
	tsb.border_width_bottom = 2
	tsb.set_corner_radius_all(8)
	tsb.content_margin_left = 8
	tsb.content_margin_right = 8
	tsb.content_margin_top = 2
	tsb.content_margin_bottom = 2
	typ_badge.add_theme_stylebox_override("panel", tsb)

	var typ_l := Label.new()
	typ_l.name = "StageTypeLabel"
	typ_l.text = _t(str(s["type"]))
	# 字級下限：ART_DAILY_CONSTITUTION §「輔助不准再縮去塞字」；t_b8e32048 審核收尾改回 13
	typ_l.add_theme_font_size_override("font_size", 13)
	typ_l.add_theme_color_override("font_color", Color("#A02818") if is_boss else COLOR_TEXT_DARK)
	typ_badge.add_child(typ_l)
	inf_row.add_child(typ_badge)

	var pwr_l := Label.new()
	pwr_l.name = "PowerLabel"
	pwr_l.text = _t("推薦戰力: %d") % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 13)
	pwr_l.add_theme_color_override("font_color", COLOR_GOLD_DARK if not is_boss else Color("#A02818"))
	pwr_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	inf_row.add_child(pwr_l)

	var cost_l := Label.new()
	cost_l.name = "CostLabel"
	if is_colossus:
		cost_l.text = _t("消耗: 1 次")
	else:
		cost_l.text = _t("消耗能量: %d") % int(s["cost"])
	cost_l.add_theme_font_size_override("font_size", 13)
	cost_l.add_theme_color_override("font_color", Color("#5A5275"))
	cost_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	inf_row.add_child(cost_l)

	v.add_child(inf_row)

	var btn_battle := Button.new()
	btn_battle.name = "BattleButton"
	btn_battle.custom_minimum_size = Vector2(145, 52)
	btn_battle.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var colossus_left := 3
	if is_colossus:
		var loop := Engine.get_main_loop()
		if loop is SceneTree and (loop as SceneTree).root != null:
			var CDS: Node = (loop as SceneTree).root.get_node_or_null("ColossusDailySystem")
			if CDS and CDS.has_method("get_remaining_entries"):
				colossus_left = int(CDS.call("get_remaining_entries"))
		if is_locked:
			btn_battle.text = _t("需達 Lv.%d") % req_lv
		elif colossus_left > 0:
			btn_battle.text = _t("出征")
		else:
			btn_battle.text = _t("明天再來")
	else:
		btn_battle.text = _t("挑戰首領") if is_boss else _t("出征")
	btn_battle.add_theme_font_size_override("font_size", 16)
	var bsb := StyleBoxFlat.new()
	if is_locked:
		bsb.bg_color = Color("#8E8898")  ## 灰色厚底立體按鈕（灰掉）
		bsb.border_color = COLOR_BORDER
		bsb.set_border_width_all(2)
		bsb.border_width_bottom = 5
		bsb.set_corner_radius_all(18)
		bsb.shadow_color = Color(0.12, 0.10, 0.23, 0.18)
		bsb.shadow_size = 6
		bsb.shadow_offset = Vector2(0, 3)
	elif is_boss:
		bsb.bg_color = COLOR_ORANGE
		bsb.border_color = COLOR_BORDER
		bsb.set_border_width_all(2)
		bsb.border_width_bottom = 5
		bsb.set_corner_radius_all(18)
		bsb.shadow_color = Color(0.12, 0.10, 0.23, 0.25)
		bsb.shadow_size = 6
		bsb.shadow_offset = Vector2(0, 3)
	else:
		bsb.bg_color = COLOR_GOLD
		bsb.border_color = COLOR_BORDER
		bsb.set_border_width_all(2)
		bsb.border_width_bottom = 5
		bsb.set_corner_radius_all(18)
		bsb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
		bsb.shadow_size = 6
		bsb.shadow_offset = Vector2(0, 3)

	if is_locked:
		btn_battle.add_theme_color_override("font_color", Color("#F5F3F8"))
		btn_battle.add_theme_color_override("font_hover_color", Color("#FFFFFF"))
		btn_battle.add_theme_color_override("font_pressed_color", Color("#E0DCE8"))
	else:
		btn_battle.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		btn_battle.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
		btn_battle.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var bsb_h := bsb.duplicate() as StyleBoxFlat
	bsb_h.bg_color = Color("#A09AA8") if is_locked else (Color("#FFB84D") if is_boss else Color("#FFE066"))
	var bsb_p := bsb.duplicate() as StyleBoxFlat
	bsb_p.bg_color = Color("#7A7484") if is_locked else bsb.bg_color
	bsb_p.border_width_bottom = 2

	btn_battle.add_theme_stylebox_override("normal", bsb)
	btn_battle.add_theme_stylebox_override("hover", bsb_h)
	btn_battle.add_theme_stylebox_override("pressed", bsb_p)
	btn_battle.add_theme_stylebox_override("focus", bsb)

	if is_colossus:
		btn_battle.pressed.connect(func():
			if is_locked:
				_show_toast(_t("等級未達 Lv.%d，低於推薦等級 10 級以上不可出征！") % req_lv)
			else:
				_on_colossus_card_pressed(s)
		)
	else:
		var m: String = str(s["mode"])
		btn_battle.pressed.connect(func():
			var g := _gs()
			if g:
				g.set("current_expedition_stage", stage_num)
				g.set("current_suggest_lv", sug_lv)
			request_battle.emit(m)
		)
	h.add_child(btn_battle)

	return c

## ──────────────────────────────────────────
## Tab 2 & Tab 5: 角色紙娃娃與背包 (奶油果凍資訊卡)
## ──────────────────────────────────────────
func _build_character_tab() -> void:
	_char_layer = Control.new()
	_char_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_char_layer.visible = false
	_content_root.add_child(_char_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	var panel_sb := StyleBoxFlat.new()
	panel_sb.bg_color = COLOR_BG_CREAM
	panel_sb.border_color = COLOR_BORDER
	panel_sb.set_border_width_all(2)
	panel_sb.border_width_bottom = 5
	panel_sb.set_corner_radius_all(20)
	panel_sb.content_margin_left = 20
	panel_sb.content_margin_right = 20
	panel_sb.content_margin_top = 16
	panel_sb.content_margin_bottom = 16
	panel_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	panel_sb.shadow_size = 8
	panel_sb.shadow_offset = Vector2(0, 4)
	panel.add_theme_stylebox_override("panel", panel_sb)
	_char_layer.add_child(panel)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 24)
	panel.add_child(h)

	var l_card := PanelContainer.new()
	l_card.custom_minimum_size = Vector2(340, 0)
	l_card.size_flags_horizontal = Control.SIZE_FILL
	var l_sb := StyleBoxFlat.new()
	l_sb.bg_color = COLOR_CARD_WARM
	l_sb.border_color = COLOR_BORDER
	l_sb.set_border_width_all(2)
	l_sb.border_width_bottom = 5
	l_sb.set_corner_radius_all(20)
	l_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
	l_sb.shadow_size = 6
	l_sb.shadow_offset = Vector2(0, 3)
	l_card.add_theme_stylebox_override("panel", l_sb)
	h.add_child(l_card)

	var l_margin := MarginContainer.new()
	l_margin.add_theme_constant_override("margin_left", 14)
	l_margin.add_theme_constant_override("margin_top", 14)
	l_margin.add_theme_constant_override("margin_right", 14)
	l_margin.add_theme_constant_override("margin_bottom", 14)
	l_card.add_child(l_margin)

	var l_vbox := VBoxContainer.new()
	l_vbox.add_theme_constant_override("separation", 10)
	l_margin.add_child(l_vbox)

	var l_title := Label.new()
	l_title.text = _t("機體外觀 · 發條紙娃娃")
	l_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(l_title, 15, COLOR_GOLD_DARK)
	l_vbox.add_child(l_title)
	_char_doll_title_label = l_title

	_char_prev = TextureRect.new()
	_char_prev.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_char_prev.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_char_prev.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_char_prev.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_char_prev.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_apply_hero_idle_visual()
	_char_prev.mouse_filter = Control.MOUSE_FILTER_PASS
	l_vbox.add_child(_char_prev)

	# 點擊預覽卡可直接開啟更衣
	var click_card_btn := Button.new()
	click_card_btn.flat = true
	click_card_btn.set_anchors_preset(Control.PRESET_FULL_RECT)
	click_card_btn.mouse_filter = Control.MOUSE_FILTER_PASS
	click_card_btn.pressed.connect(open_wardrobe)
	_char_prev.add_child(click_card_btn)

	# 招式心法按鈕 (手遊防誤觸標準：高度 50px，熱區 >= 48px，立體厚底 5px)
	var btn_skill := Button.new()
	btn_skill.name = "BtnSkillDialog"
	btn_skill.text = _t("招式 · 核心心法")
	btn_skill.custom_minimum_size = Vector2(0, 50)
	btn_skill.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	if _cached_font != null:
		btn_skill.add_theme_font_override("font", _cached_font)
	btn_skill.add_theme_font_size_override("font_size", 16)
	btn_skill.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_skill.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_skill.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var ssb := StyleBoxFlat.new()
	ssb.bg_color = COLOR_SKY
	ssb.border_color = COLOR_BORDER
	ssb.set_border_width_all(2)
	ssb.border_width_bottom = 5
	ssb.set_corner_radius_all(18)
	ssb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	ssb.shadow_size = 5
	ssb.shadow_offset = Vector2(0, 2)
	var ssb_h := ssb.duplicate() as StyleBoxFlat
	ssb_h.bg_color = Color("#5EB5FF")
	var ssb_p := ssb.duplicate() as StyleBoxFlat
	ssb_p.border_width_bottom = 2
	btn_skill.add_theme_stylebox_override("normal", ssb)
	btn_skill.add_theme_stylebox_override("hover", ssb_h)
	btn_skill.add_theme_stylebox_override("pressed", ssb_p)
	btn_skill.add_theme_stylebox_override("focus", ssb)
	btn_skill.pressed.connect(open_skill_dialog)
	l_vbox.add_child(btn_skill)
	_btn_skill_dialog = btn_skill

	# 正式更衣按鈕 (手遊防誤觸標準：高度 50px，熱區 >= 50px)
	var btn_wardrobe := Button.new()
	btn_wardrobe.name = "BtnWardrobe"
	btn_wardrobe.text = _t("更衣 · 發條衣櫥")
	btn_wardrobe.custom_minimum_size = Vector2(0, 50)
	btn_wardrobe.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	if _cached_font != null:
		btn_wardrobe.add_theme_font_override("font", _cached_font)
	btn_wardrobe.add_theme_font_size_override("font_size", 16)
	btn_wardrobe.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_wardrobe.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_wardrobe.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var wsb := StyleBoxFlat.new()
	wsb.bg_color = COLOR_ORANGE
	wsb.border_color = COLOR_BORDER
	wsb.set_border_width_all(2)
	wsb.border_width_bottom = 5
	wsb.set_corner_radius_all(18)
	wsb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	wsb.shadow_size = 5
	wsb.shadow_offset = Vector2(0, 2)
	var wsb_h := wsb.duplicate() as StyleBoxFlat
	wsb_h.bg_color = Color("#FFB84D")
	var wsb_p := wsb.duplicate() as StyleBoxFlat
	wsb_p.border_width_bottom = 2
	btn_wardrobe.add_theme_stylebox_override("normal", wsb)
	btn_wardrobe.add_theme_stylebox_override("hover", wsb_h)
	btn_wardrobe.add_theme_stylebox_override("pressed", wsb_p)
	btn_wardrobe.add_theme_stylebox_override("focus", wsb)
	btn_wardrobe.pressed.connect(open_wardrobe)
	l_vbox.add_child(btn_wardrobe)
	_btn_wardrobe = btn_wardrobe

	var r_v := VBoxContainer.new()
	r_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	r_v.add_theme_constant_override("separation", 12)
	h.add_child(r_v)

	# 1. 武器輪替配置標題
	var w_hdr := HBoxContainer.new()
	w_hdr.add_theme_constant_override("separation", 12)
	r_v.add_child(w_hdr)

	var w_title := Label.new()
	w_title.text = _t("武器輪替配置")
	_apply_label_style(w_title, 18, COLOR_TEXT_DARK)
	w_hdr.add_child(w_title)
	_char_weapon_title_label = w_title

	var w_sub := Label.new()
	w_sub.text = _t("點擊切換輪替順位 · 三段作戰序列")
	_apply_label_style(w_sub, 13, COLOR_GOLD_DARK)
	w_hdr.add_child(w_sub)
	_char_weapon_sub_label = w_sub

	var w_hdr_spacer := Control.new()
	w_hdr_spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	w_hdr.add_child(w_hdr_spacer)

	var btn_change_weapon := Button.new()
	btn_change_weapon.name = "BtnChangeWeapon"
	btn_change_weapon.text = _t("更換裝備")
	btn_change_weapon.custom_minimum_size = Vector2(104, 48)
	if _cached_font != null:
		btn_change_weapon.add_theme_font_override("font", _cached_font)
	btn_change_weapon.add_theme_font_size_override("font_size", 14)
	btn_change_weapon.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_change_weapon.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_change_weapon.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var ce_sb := StyleBoxFlat.new()
	ce_sb.bg_color = COLOR_SKY
	ce_sb.border_color = COLOR_BORDER
	ce_sb.set_border_width_all(2)
	ce_sb.border_width_bottom = 5
	ce_sb.set_corner_radius_all(16)
	ce_sb.shadow_color = Color(0.12, 0.10, 0.23, 0.20)
	ce_sb.shadow_size = 5
	ce_sb.shadow_offset = Vector2(0, 2)
	var ce_sb_h := ce_sb.duplicate() as StyleBoxFlat
	ce_sb_h.bg_color = Color("#5EB5FF")
	var ce_sb_p := ce_sb.duplicate() as StyleBoxFlat
	ce_sb_p.border_width_bottom = 2
	btn_change_weapon.add_theme_stylebox_override("normal", ce_sb)
	btn_change_weapon.add_theme_stylebox_override("hover", ce_sb_h)
	btn_change_weapon.add_theme_stylebox_override("pressed", ce_sb_p)
	btn_change_weapon.add_theme_stylebox_override("focus", ce_sb)
	btn_change_weapon.pressed.connect(func():
		open_weapon_swap_dialog(_selected_weapon_slot)
	)
	w_hdr.add_child(btn_change_weapon)
	_btn_change_weapon = btn_change_weapon

	# 2. 三個武器槽果凍卡
	var w_row := HBoxContainer.new()
	w_row.add_theme_constant_override("separation", 12)
	r_v.add_child(w_row)

	_weapon_slot_buttons.clear()
	for i in range(WEAPON_SLOTS.size()):
		var slot_btn := _build_weapon_slot_button(i, WEAPON_SLOTS[i])
		w_row.add_child(slot_btn)
		_weapon_slot_buttons.append(slot_btn)

	# 3. 武器槽提示卡
	var hint_p := PanelContainer.new()
	hint_p.custom_minimum_size = Vector2(0, 36)
	var hsb := StyleBoxFlat.new()
	hsb.bg_color = COLOR_CARD_WARM
	hsb.border_color = COLOR_BORDER
	hsb.set_border_width_all(1)
	hsb.border_width_bottom = 3
	hsb.set_corner_radius_all(10)
	hsb.content_margin_left = 14
	hsb.content_margin_right = 14
	hsb.content_margin_top = 6
	hsb.content_margin_bottom = 6
	hint_p.add_theme_stylebox_override("panel", hsb)
	r_v.add_child(hint_p)

	_weapon_slot_hint_label = Label.new()
	var init_hint := _t(WEAPON_SLOTS[_selected_weapon_slot]["hint"])
	_weapon_slot_hint_label.text = init_hint
	var init_h_sz := 12 if init_hint.length() > 70 else 13
	_apply_label_style(_weapon_slot_hint_label, init_h_sz, COLOR_TEXT_DARK)
	hint_p.add_child(_weapon_slot_hint_label)

	# 4. 戰鬥屬性標題列
	var s_hdr := HBoxContainer.new()
	s_hdr.add_theme_constant_override("separation", 12)
	r_v.add_child(s_hdr)

	var s_title := Label.new()
	s_title.text = _t("機體戰鬥屬性")
	_apply_label_style(s_title, 18, COLOR_TEXT_DARK)
	s_hdr.add_child(s_title)
	_char_stat_title_label = s_title

	var pow_capsule := PanelContainer.new()
	var pcsb := StyleBoxFlat.new()
	pcsb.bg_color = COLOR_CARD_GOLD
	pcsb.border_color = COLOR_BORDER
	pcsb.set_border_width_all(2)
	pcsb.border_width_bottom = 3
	pcsb.set_corner_radius_all(12)
	pcsb.content_margin_left = 12
	pcsb.content_margin_right = 12
	pcsb.content_margin_top = 2
	pcsb.content_margin_bottom = 2
	pow_capsule.add_theme_stylebox_override("panel", pcsb)
	s_hdr.add_child(pow_capsule)

	_char_power_badge = Label.new()
	var gs := _gs()
	var cur_pow := 482
	if gs and gs.has_method("power_score") and int(gs.call("power_score")) > 0:
		cur_pow = int(gs.call("power_score"))
	_char_power_badge.text = _t("有效戰力 %d") % cur_pow
	_apply_label_style(_char_power_badge, 13, COLOR_TEXT_DARK)
	pow_capsule.add_child(_char_power_badge)

	var lv_capsule := PanelContainer.new()
	var lcsb := StyleBoxFlat.new()
	lcsb.bg_color = COLOR_CARD_WARM
	lcsb.border_color = COLOR_BORDER
	lcsb.set_border_width_all(2)
	lcsb.border_width_bottom = 3
	lcsb.set_corner_radius_all(12)
	lcsb.content_margin_left = 12
	lcsb.content_margin_right = 12
	lcsb.content_margin_top = 2
	lcsb.content_margin_bottom = 2
	lv_capsule.add_theme_stylebox_override("panel", lcsb)
	s_hdr.add_child(lv_capsule)

	_char_level_badge = Label.new()
	_update_char_level_badge()
	_apply_label_style(_char_level_badge, 13, COLOR_TEXT_DARK)
	lv_capsule.add_child(_char_level_badge)

	# 5. 獨立屬性小卡 (生命／攻擊／防禦／暴擊／怒氣)
	var stats_v := VBoxContainer.new()
	stats_v.add_theme_constant_override("separation", 10)
	stats_v.size_flags_vertical = Control.SIZE_EXPAND_FILL
	r_v.add_child(stats_v)

	_stat_cards.clear()
	var r1 := HBoxContainer.new()
	r1.add_theme_constant_override("separation", 10)
	r1.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	stats_v.add_child(r1)

	var sc1 := _build_stat_card("生命力 (HP)", "520", "機體核心", Color("#0E8A7A"))
	r1.add_child(sc1)
	_stat_cards.append(sc1)

	var sc2 := _build_stat_card("物理攻擊", "95", "打擊破壞", COLOR_GOLD_DARK)
	r1.add_child(sc2)
	_stat_cards.append(sc2)

	var sc3 := _build_stat_card("物理防禦", "48", "減傷防護", Color("#2A5580"))
	r1.add_child(sc3)
	_stat_cards.append(sc3)

	var r2 := HBoxContainer.new()
	r2.add_theme_constant_override("separation", 10)
	r2.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	stats_v.add_child(r2)

	var sc4 := _build_stat_card("暴擊率", "22%", "弱點致命", Color("#B83250"))
	r2.add_child(sc4)
	_stat_cards.append(sc4)

	var sc5 := _build_stat_card("怒氣量表", "20 點", "滿怒超頻運轉 +25% 性能", Color("#A82B1E"))
	r2.add_child(sc5)
	_stat_cards.append(sc5)

func _get_weapon_slot_info(slot_idx: int) -> Dictionary:
	var eq := _get_equip_sys()
	var gs := _gs()
	var title := WEAPON_SLOT_TITLES[slot_idx] if slot_idx >= 0 and slot_idx < WEAPON_SLOT_TITLES.size() else "首選武器"

	var fallback: Dictionary = WEAPON_SLOTS[slot_idx] if slot_idx >= 0 and slot_idx < WEAPON_SLOTS.size() else {}
	var fb_name: String = str(fallback.get("weapon_name", "鐵劍"))
	var fb_hits: String = str(fallback.get("hits", "4 次打擊"))
	var fb_hint: String = str(fallback.get("hint", ""))

	if eq == null:
		return {
			"slot_title": title,
			"weapon_name": fb_name,
			"hits": fb_hits,
			"quality": "common",
			"quality_label": "凡品",
			"quality_color": Color("#8E8A9F"),
			"hint": fb_hint,
			"unlocked": true,
			"empty": false,
			"is_active": (slot_idx == _selected_weapon_slot),
			"uid": "",
			"atk": 0,
		}

	var snap: Array = []
	if eq.has_method("loadout_snapshot_for_battle"):
		snap = eq.loadout_snapshot_for_battle()

	var entry: Dictionary = {}
	if slot_idx >= 0 and slot_idx < snap.size():
		entry = snap[slot_idx]

	var unlocked := true
	if eq.has_method("loadout_slot_unlocked"):
		unlocked = eq.loadout_slot_unlocked(slot_idx)
	elif not entry.is_empty():
		unlocked = bool(entry.get("unlocked", true))

	if not unlocked:
		var req_lv := 10 if slot_idx == 1 else 16
		if eq.has_method("loadout_unlock_level"):
			req_lv = int(eq.loadout_unlock_level(slot_idx))
		return {
			"slot_title": title,
			"weapon_name": "未解鎖",
			"hits": "需達 Lv%d" % req_lv,
			"quality": "locked",
			"quality_label": "未解鎖",
			"quality_color": Color("#A09CAE"),
			"hint": "武器欄位未解鎖（角色等級需達到 Lv%d）" % req_lv,
			"unlocked": false,
			"empty": true,
			"is_active": false,
			"uid": "",
			"atk": 0,
		}

	var uid: String = str(entry.get("uid", ""))
	if uid.is_empty() and gs and "weapon_loadout" in gs and slot_idx < gs.weapon_loadout.size():
		uid = str(gs.weapon_loadout[slot_idx])

	if uid.is_empty():
		return {
			"slot_title": title,
			"weapon_name": "空槽",
			"hits": "未裝備",
			"quality": "none",
			"quality_label": "未裝備",
			"quality_color": Color("#A09CAE"),
			"hint": "備用武器槽位：可於冒險者背包或兵器架中裝備武器",
			"unlocked": true,
			"empty": true,
			"is_active": false,
			"uid": "",
			"atk": 0,
		}

	var inst: Dictionary = {}
	if eq.has_method("weapon_inst"):
		inst = eq.weapon_inst(uid)
	if inst.is_empty() and gs and "equip_worn" in gs and gs.equip_worn is Dictionary:
		inst = gs.equip_worn.get(uid, {})

	var wname: String = str(inst.get("name", entry.get("name", fb_name)))
	if wname.is_empty():
		wname = fb_name
	var line: String = str(inst.get("line", entry.get("line", "sword")))
	var hits: String = LINE_HITS.get(line, "4 次打擊")
	var quality: String = str(inst.get("quality", "common"))
	var quality_label: String = str(inst.get("quality_label", "凡品"))

	var q_col := Color("#8E8A9F")
	match quality:
		"common": q_col = Color("#8E8A9F")
		"uncommon": q_col = Color("#2E9E4A")
		"rare": q_col = Color("#2575FC")
		"epic": q_col = Color("#9B51E0")
		_: q_col = Color("#8E8A9F")

	var atk: int = int(entry.get("weapon_atk", 0))
	if atk <= 0 and inst.has("rolled") and inst["rolled"] is Dictionary:
		atk = int(inst["rolled"].get("atk", 0))

	var hint_str := fb_hint
	if wname != fb_name:
		var line_name: String = LINE_NAMES.get(line, line)
		hint_str = "%s · %s：流派「%s」，%s，基礎攻擊 +%d" % [title, wname, line_name, hits, atk]

	return {
		"slot_title": title,
		"weapon_name": wname,
		"hits": hits,
		"quality": quality,
		"quality_label": quality_label,
		"quality_color": q_col,
		"hint": hint_str,
		"unlocked": true,
		"empty": false,
		"is_active": (slot_idx == _selected_weapon_slot),
		"uid": uid,
		"atk": atk,
	}

func _build_weapon_slot_button(idx: int, slot_data: Dictionary) -> Button:
	var btn := Button.new()
	btn.name = "WeaponSlot_%d" % idx
	btn.custom_minimum_size = Vector2(0, 68)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.set_meta("quality_color", slot_data.get("quality_color", COLOR_GOLD_DARK))

	var v := VBoxContainer.new()
	v.name = "Content"
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 1)
	btn.add_child(v)

	var slot_title := Label.new()
	slot_title.name = "SlotTitle"
	var t_text := _t(slot_data["slot_title"])
	slot_title.text = t_text
	slot_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var t_sz := 11 if t_text.length() > 14 else 12
	_apply_label_style(slot_title, t_sz, COLOR_GOLD_DARK)
	v.add_child(slot_title)

	var weapon_info := Label.new()
	weapon_info.name = "WeaponInfo"
	var w_text := "%s · %s" % [_t(slot_data["weapon_name"]), _t(slot_data["hits"])]
	weapon_info.text = w_text
	weapon_info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var w_sz := 12 if w_text.length() > 22 else (13 if w_text.length() > 18 else 14)
	_apply_label_style(weapon_info, w_sz, COLOR_TEXT_DARK)
	v.add_child(weapon_info)

	var quality_lbl := Label.new()
	quality_lbl.name = "QualityLabel"
	var q_text := _t(str(slot_data.get("quality_label", "")))
	quality_lbl.text = q_text
	quality_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	var q_col: Color = slot_data.get("quality_color", COLOR_GOLD_DARK)
	_apply_label_style(quality_lbl, 10, q_col)
	v.add_child(quality_lbl)

	_style_weapon_slot_button(btn, idx == _selected_weapon_slot)
	var slot_idx := idx
	btn.pressed.connect(func(): _on_weapon_slot_clicked(slot_idx))
	return btn

func _style_weapon_slot_button(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(18)
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 6
	sb.content_margin_bottom = 6

	var title_lbl := btn.get_node_or_null("Content/SlotTitle") as Label
	var info_lbl := btn.get_node_or_null("Content/WeaponInfo") as Label
	var q_lbl := btn.get_node_or_null("Content/QualityLabel") as Label

	if is_selected:
		sb.bg_color = COLOR_ORANGE
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		if title_lbl:
			title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		if info_lbl:
			info_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		if q_lbl:
			q_lbl.add_theme_color_override("font_color", Color(0.22, 0.18, 0.38))
	else:
		sb.bg_color = COLOR_CARD_WARM
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		if title_lbl:
			title_lbl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
		if info_lbl:
			info_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		if q_lbl:
			var q_col: Color = btn.get_meta("quality_color", COLOR_GOLD_DARK)
			q_lbl.add_theme_color_override("font_color", q_col)

	var sb_h := sb.duplicate() as StyleBoxFlat
	if not is_selected:
		sb_h.bg_color = COLOR_CARD_GOLD
	else:
		sb_h.bg_color = Color("#FFB84D")

	var sb_p := sb.duplicate() as StyleBoxFlat
	sb_p.border_width_bottom = 2

	btn.add_theme_stylebox_override("normal", sb)
	btn.add_theme_stylebox_override("hover", sb_h)
	btn.add_theme_stylebox_override("pressed", sb_p)
	btn.add_theme_stylebox_override("focus", sb)

func _on_weapon_slot_clicked(idx: int) -> void:
	_select_weapon_slot(idx)
	open_weapon_swap_dialog(idx)

func select_weapon_slot(idx: int) -> void:
	_select_weapon_slot(idx)

func get_selected_weapon_slot() -> int:
	return _selected_weapon_slot

func get_weapon_slot_buttons() -> Array[Button]:
	return _weapon_slot_buttons

func refresh_weapon_slots() -> void:
	_refresh_weapon_slot_buttons()

func _refresh_weapon_slot_buttons() -> void:
	for i in range(_weapon_slot_buttons.size()):
		if not is_instance_valid(_weapon_slot_buttons[i]):
			continue
		var btn := _weapon_slot_buttons[i]
		var data := _get_weapon_slot_info(i)
		btn.set_meta("quality_color", data.get("quality_color", COLOR_GOLD_DARK))

		var title_lbl := btn.get_node_or_null("Content/SlotTitle") as Label
		if title_lbl:
			var t_text := _t(str(data["slot_title"]))
			title_lbl.text = t_text
			if t_text.length() > 14:
				title_lbl.add_theme_font_size_override("font_size", 11)
			else:
				title_lbl.add_theme_font_size_override("font_size", 12)

		var info_lbl := btn.get_node_or_null("Content/WeaponInfo") as Label
		if info_lbl:
			var w_text := "%s · %s" % [_t(str(data["weapon_name"])), _t(str(data["hits"]))]
			info_lbl.text = w_text
			if w_text.length() > 22:
				info_lbl.add_theme_font_size_override("font_size", 12)
			elif w_text.length() > 18:
				info_lbl.add_theme_font_size_override("font_size", 13)
			else:
				info_lbl.add_theme_font_size_override("font_size", 14)

		var q_lbl := btn.get_node_or_null("Content/QualityLabel") as Label
		if q_lbl:
			var q_text := _t(str(data.get("quality_label", "")))
			q_lbl.text = q_text
			var q_col: Color = data.get("quality_color", COLOR_GOLD_DARK)
			q_lbl.add_theme_color_override("font_color", q_col)

		_style_weapon_slot_button(btn, i == _selected_weapon_slot)

	if _weapon_slot_hint_label and is_instance_valid(_weapon_slot_hint_label):
		var cur_data := _get_weapon_slot_info(_selected_weapon_slot)
		var hint_text := _t(str(cur_data.get("hint", "")))
		_weapon_slot_hint_label.text = hint_text
		if hint_text.length() > 70:
			_weapon_slot_hint_label.add_theme_font_size_override("font_size", 12)
		else:
			_weapon_slot_hint_label.add_theme_font_size_override("font_size", 13)

const WEAPON_LINE_TO_PAPERDOLL: Dictionary = {
	"sword": "wpn_dawn_blade",
	"spear": "wpn_knight_lance",
	"claw": "wpn_spring_claws",
	"magic": "wpn_astral_staff",
	"hammer": "wpn_anvil_greathammer",
	"dagger": "wpn_twin_ember_sabers",
	"bow": "wpn_zephyr_wing_bow",
	"fist": "wpn_panda_taiji_cestus",
	"gun": "wpn_twin_harpoon_gun",
	"axe": "wpn_colossus_cleaver_axe",
	"dart": "wpn_lotus_cog_dart",
	"crystal": "wpn_bagua_astrolabe",
}

func _resolve_hero_weapon_paperdoll_id(race: String, winst: Dictionary) -> String:
	if winst.is_empty():
		return "none"
	var base_id := str(winst.get("base_id", "")).strip_edges()
	var line := str(winst.get("line", "")).strip_edges()
	var raw_id := str(winst.get("id", "")).strip_edges()

	var candidates: Array[String] = []
	if not base_id.is_empty():
		candidates.append(base_id)
	if WEAPON_LINE_TO_PAPERDOLL.has(line):
		candidates.append(WEAPON_LINE_TO_PAPERDOLL[line])
	if WEAPON_LINE_TO_PAPERDOLL.has(base_id):
		candidates.append(WEAPON_LINE_TO_PAPERDOLL[base_id])
	if not raw_id.is_empty() and raw_id != base_id:
		candidates.append(raw_id)

	for cid in candidates:
		if cid.is_empty() or cid in ["none", "empty", "bare"]:
			continue
		var p512 := PaperdollRenderer.resolve_slot_texture_path_512(race, "weapon", cid)
		if p512 != "" and p512.ends_with("_512.png") and (ResourceLoader.exists(p512) or FileAccess.file_exists(p512)):
			return cid

	return "none"

func _sync_hero_weapon_paperdoll() -> void:
	var gs := _gs()
	var eq := _get_equip_sys()
	var race := _current_race()
	var winst: Dictionary = {}
	if eq and eq.has_method("active_weapon_inst"):
		winst = eq.active_weapon_inst()
	elif gs and "equip_slots" in gs and gs.equip_slots is Dictionary:
		var wuid: String = str(gs.equip_slots.get("weapon", ""))
		if wuid != "" and "equip_worn" in gs and gs.equip_worn is Dictionary and gs.equip_worn.has(wuid):
			winst = gs.equip_worn[wuid]

	var w_id := "none"
	if not winst.is_empty():
		w_id = _resolve_hero_weapon_paperdoll_id(race, winst)

	if gs and "paperdoll_slots" in gs and gs.paperdoll_slots is Dictionary:
		gs.paperdoll_slots["weapon"] = w_id

	_cached_hero_comp_512 = null
	_cached_hero_comp_key = ""
	_cached_hero_body_comp_512 = null
	_cached_hero_body_key = ""
	_load_hero_poses()
	_apply_hero_idle_visual()
	_refresh_equip_schematic()

func _refresh_char_tab_stats(dynamic_atk: bool = true) -> void:
	var gs := _gs()
	if gs == null:
		return

	var cur_pow := 482
	if gs.has_method("power_score") and int(gs.call("power_score")) > 0:
		cur_pow = int(gs.call("power_score"))
	if _char_power_badge and is_instance_valid(_char_power_badge):
		_char_power_badge.text = _t("有效戰力 %d") % cur_pow

	if _stat_cards.size() > 1 and is_instance_valid(_stat_cards[1]):
		var atk_card := _stat_cards[1]
		var cur_atk := 95
		if dynamic_atk and gs.has_method("effective_atk"):
			var eff: int = int(gs.effective_atk())
			if eff > 0:
				cur_atk = eff
			atk_card.set_meta("stat_val_key", str(cur_atk))
		else:
			cur_atk = int(atk_card.get_meta("stat_val_key", "95"))
		var v_lbl := atk_card.find_child("ValLabel", true, false) as Label
		if v_lbl:
			v_lbl.text = str(cur_atk)

func _select_weapon_slot(idx: int) -> void:
	if idx < 0 or idx >= _weapon_slot_buttons.size():
		return
	_selected_weapon_slot = idx

	var eq := _get_equip_sys()
	if eq and eq.has_method("switch_weapon_loadout"):
		var sw_res: Dictionary = eq.switch_weapon_loadout(idx)
		if not bool(sw_res.get("ok", false)):
			var reason_msg: String = str(sw_res.get("msg", ""))
			if not reason_msg.is_empty():
				_show_toast(reason_msg)
		else:
			var toast_msg: String = str(sw_res.get("msg", ""))
			if not toast_msg.is_empty():
				_show_toast(toast_msg)

	_sync_hero_weapon_paperdoll()
	_refresh_char_tab_stats(true)
	_refresh_weapon_slot_buttons()

func _build_stat_card(title: String, val_str: String, subtitle: String, val_color: Color) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "StatCard"
	c.set_meta("is_stat_card", true)
	c.set_meta("stat_title_key", title)
	c.set_meta("stat_val_key", val_str)
	c.set_meta("stat_subtitle_key", subtitle)
	c.custom_minimum_size = Vector2(0, 80)
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var sb := StyleBoxFlat.new()
	sb.bg_color = COLOR_CARD_WARM
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.set_corner_radius_all(18)
	sb.content_margin_left = 16
	sb.content_margin_right = 16
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8
	sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
	sb.shadow_size = 4
	sb.shadow_offset = Vector2(0, 2)
	c.add_theme_stylebox_override("panel", sb)

	var v := VBoxContainer.new()
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.add_theme_constant_override("separation", 2)
	c.add_child(v)

	var top_row := HBoxContainer.new()
	top_row.add_theme_constant_override("separation", 6)
	v.add_child(top_row)

	var t_lbl := Label.new()
	t_lbl.name = "TitleLabel"
	var t_text := _t(title)
	t_lbl.text = t_text
	var t_sz := 12 if t_text.length() > 14 else 14
	_apply_label_style(t_lbl, t_sz, COLOR_TEXT_DARK)
	top_row.add_child(t_lbl)

	if not subtitle.is_empty():
		var sub_lbl := Label.new()
		sub_lbl.name = "SubLabel"
		var sub_text := _t(subtitle)
		sub_lbl.text = sub_text
		var sub_sz := 10 if sub_text.length() > 24 else (11 if sub_text.length() > 16 else 12)
		_apply_label_style(sub_lbl, sub_sz, COLOR_GOLD_DARK)
		top_row.add_child(sub_lbl)

	var val_row := HBoxContainer.new()
	val_row.add_theme_constant_override("separation", 6)
	v.add_child(val_row)

	var v_lbl := Label.new()
	v_lbl.name = "ValLabel"
	v_lbl.text = _t(val_str)
	_apply_label_style(v_lbl, 22, val_color)
	val_row.add_child(v_lbl)

	return c

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

func _build_bag_tab() -> void:
	_bag_layer = Control.new()
	_bag_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bag_layer.visible = false
	_content_root.add_child(_bag_layer)

	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_FULL_RECT)
	panel.offset_left = 50
	panel.offset_right = -50
	panel.offset_top = 16
	panel.offset_bottom = -16
	var psb := _create_panel_style(COLOR_BG_CREAM, COLOR_BORDER, 2, 5, 20)
	panel.add_theme_stylebox_override("panel", psb)
	_bag_layer.add_child(panel)

	var panel_margin := MarginContainer.new()
	panel_margin.add_theme_constant_override("margin_left", 20)
	panel_margin.add_theme_constant_override("margin_right", 20)
	panel_margin.add_theme_constant_override("margin_top", 16)
	panel_margin.add_theme_constant_override("margin_bottom", 16)
	panel.add_child(panel_margin)

	var outer_vbox := VBoxContainer.new()
	outer_vbox.add_theme_constant_override("separation", 10)
	panel_margin.add_child(outer_vbox)

	# ── 頂部標題與裝飾分隔線 ──
	var head_row := HBoxContainer.new()
	head_row.custom_minimum_size.y = 44
	head_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	outer_vbox.add_child(head_row)

	var title_v := VBoxContainer.new()
	title_v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head_row.add_child(title_v)

	_bag_title_lbl = Label.new()
	_bag_title_lbl.text = _t("冒險者背包")
	_apply_label_style(_bag_title_lbl, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 4)
	title_v.add_child(_bag_title_lbl)

	_bag_sub_lbl = Label.new()
	_bag_sub_lbl.text = _t("道具與戰魂倉庫 · 點選格子查看詳情")
	_apply_label_style(_bag_sub_lbl, 16, COLOR_TEXT_DARK)
	title_v.add_child(_bag_sub_lbl)

	var rule := ColorRect.new()
	rule.custom_minimum_size = Vector2(0, 3)
	rule.color = COLOR_ORANGE
	outer_vbox.add_child(rule)

	# ── 主體內容雙欄排列 (左側 4×6 物品果凍格 + 右側道具詳情與操作按鈕) ──
	var body := HBoxContainer.new()
	body.add_theme_constant_override("separation", 20)
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	outer_vbox.add_child(body)

	# 左側：物品格子區 (GridContainer 4×6 = 24 格)
	var grid_panel := PanelContainer.new()
	grid_panel.custom_minimum_size = Vector2(340, 0)
	grid_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	body.add_child(grid_panel)

	var grid_margin := MarginContainer.new()
	grid_margin.add_theme_constant_override("margin_left", 12)
	grid_margin.add_theme_constant_override("margin_right", 12)
	grid_margin.add_theme_constant_override("margin_top", 12)
	grid_margin.add_theme_constant_override("margin_bottom", 12)
	grid_panel.add_child(grid_margin)

	_bag_grid = GridContainer.new()
	_bag_grid.columns = 4
	_bag_grid.add_theme_constant_override("h_separation", 8)
	_bag_grid.add_theme_constant_override("v_separation", 6)
	_bag_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bag_grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_margin.add_child(_bag_grid)

	_bag_cells.clear()
	for i in range(24):
		var cell := PanelContainer.new()
		cell.custom_minimum_size = Vector2(68, 56)
		cell.mouse_filter = Control.MOUSE_FILTER_STOP
		var cs := _create_panel_style(COLOR_CARD_WARM, Color(0.20, 0.16, 0.30, 0.35), 2, 3, 16)
		cell.add_theme_stylebox_override("panel", cs)
		_bag_grid.add_child(cell)
		_bag_cells.append(cell)

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
			_on_bag_cell_input(idx, ev)
		)

	# 右側：道具明細與操作按鈕區
	var right := VBoxContainer.new()
	right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	right.size_flags_vertical = Control.SIZE_EXPAND_FILL
	right.add_theme_constant_override("separation", 10)
	body.add_child(right)

	# 道具詳情卡片 (溫暖米黃底 + 深藍紫立體邊框)
	var detail_panel := PanelContainer.new()
	detail_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	detail_panel.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	right.add_child(detail_panel)

	# 未裝備機芯部件區塊 (既有機芯背包)
	var core_panel := _build_core_bag_section()
	right.add_child(core_panel)

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

	_bag_preview_row = HBoxContainer.new()
	_bag_preview_row.add_theme_constant_override("separation", 14)
	_bag_preview_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bag_preview_row.visible = false
	detail_vbox.add_child(_bag_preview_row)

	_bag_preview_frame = PanelContainer.new()
	_bag_preview_frame.custom_minimum_size = Vector2(80, 80)
	_bag_preview_frame.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_GOLD, COLOR_BORDER, 2, 4, 16))
	_bag_preview_row.add_child(_bag_preview_frame)

	var preview_stack := Control.new()
	preview_stack.set_anchors_preset(Control.PRESET_FULL_RECT)
	preview_stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bag_preview_frame.add_child(preview_stack)

	_bag_detail_icon = TextureRect.new()
	_bag_detail_icon.name = "DetailIcon"
	_bag_detail_icon.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bag_detail_icon.offset_left = 6
	_bag_detail_icon.offset_top = 4
	_bag_detail_icon.offset_right = -6
	_bag_detail_icon.offset_bottom = -6
	_bag_detail_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_bag_detail_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_bag_detail_icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_bag_detail_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bag_detail_icon.visible = false
	preview_stack.add_child(_bag_detail_icon)

	_bag_detail_glyph = Label.new()
	_bag_detail_glyph.name = "DetailGlyph"
	_bag_detail_glyph.set_anchors_preset(Control.PRESET_FULL_RECT)
	_bag_detail_glyph.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_bag_detail_glyph.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_apply_label_style(_bag_detail_glyph, 36, COLOR_TEXT_DARK)
	_bag_detail_glyph.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bag_detail_glyph.visible = false
	preview_stack.add_child(_bag_detail_glyph)

	var header_vbox := VBoxContainer.new()
	header_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header_vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	header_vbox.add_theme_constant_override("separation", 4)
	_bag_preview_row.add_child(header_vbox)

	var name_row := HBoxContainer.new()
	name_row.add_theme_constant_override("separation", 8)
	header_vbox.add_child(name_row)

	_bag_detail_name = Label.new()
	_bag_detail_name.name = "DetailName"
	_apply_label_style(_bag_detail_name, 20, COLOR_TEXT_DARK)
	name_row.add_child(_bag_detail_name)

	_bag_detail_count = Label.new()
	_bag_detail_count.name = "DetailCount"
	_apply_label_style(_bag_detail_count, 18, COLOR_TEXT_ORANGE)
	name_row.add_child(_bag_detail_count)

	_bag_detail_kind = Label.new()
	_bag_detail_kind.name = "DetailKind"
	_apply_label_style(_bag_detail_kind, 16, Color("#4A3E60"))
	header_vbox.add_child(_bag_detail_kind)

	_bag_detail = RichTextLabel.new()
	_bag_detail.bbcode_enabled = true
	_bag_detail.scroll_active = true
	_bag_detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bag_detail.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_bag_detail.add_theme_font_size_override("normal_font_size", 16)
	_bag_detail.add_theme_font_size_override("bold_font_size", 20)
	if _cached_font:
		_bag_detail.add_theme_font_override("normal_font", _cached_font)
		_bag_detail.add_theme_font_override("bold_font", _cached_font)
	_bag_detail.mouse_filter = Control.MOUSE_FILTER_IGNORE
	detail_vbox.add_child(_bag_detail)

	# 按鈕列 (「使用 / 賣出」薄荷綠 + 「放到快捷欄」天藍)
	var btn_row := HBoxContainer.new()
	btn_row.add_theme_constant_override("separation", 14)
	right.add_child(btn_row)

	_bag_use_btn = Button.new()
	_bag_use_btn.text = _t("使用 / 賣出")
	_bag_use_btn.custom_minimum_size = Vector2(0, 52)
	_bag_use_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bag_use_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_MINT, COLOR_BORDER, 5, 18))
	_bag_use_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#6BE082"), COLOR_BORDER, 5, 18))
	_bag_use_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_MINT, COLOR_BORDER, 2, 18))
	_bag_use_btn.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_bag_use_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_bag_use_btn.add_theme_font_override("font", _cached_font)
	_bag_use_btn.pressed.connect(_on_bag_use_pressed)
	btn_row.add_child(_bag_use_btn)

	_bag_hb_btn = Button.new()
	_bag_hb_btn.text = _t("放到快捷欄")
	_bag_hb_btn.custom_minimum_size = Vector2(0, 52)
	_bag_hb_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_bag_hb_btn.add_theme_stylebox_override("normal", _create_button_style(COLOR_SKY, COLOR_BORDER, 5, 18))
	_bag_hb_btn.add_theme_stylebox_override("hover", _create_button_style(Color("#5DB3FF"), COLOR_BORDER, 5, 18))
	_bag_hb_btn.add_theme_stylebox_override("pressed", _create_button_style(COLOR_SKY, COLOR_BORDER, 2, 18))
	_bag_hb_btn.add_theme_color_override("font_color", Color("#FFFFFF"))
	_bag_hb_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_bag_hb_btn.add_theme_constant_override("outline_size", 3)
	_bag_hb_btn.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_bag_hb_btn.add_theme_font_override("font", _cached_font)
	_bag_hb_btn.pressed.connect(_on_bag_hotbar_pressed)
	btn_row.add_child(_bag_hb_btn)

	_btn_bag_go_forge = Button.new()
	_btn_bag_go_forge.name = "BtnBagGoForge"
	_btn_bag_go_forge.text = _t("前往鍛造")
	_btn_bag_go_forge.custom_minimum_size = Vector2(0, 52)
	_btn_bag_go_forge.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_btn_bag_go_forge.add_theme_stylebox_override("normal", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 5, 18))
	_btn_bag_go_forge.add_theme_stylebox_override("hover", _create_button_style(COLOR_GOLD, COLOR_BORDER, 5, 18))
	_btn_bag_go_forge.add_theme_stylebox_override("pressed", _create_button_style(COLOR_ORANGE, COLOR_BORDER, 2, 18))
	_btn_bag_go_forge.add_theme_color_override("font_color", Color("#FFFFFF"))
	_btn_bag_go_forge.add_theme_color_override("font_outline_color", COLOR_BORDER)
	_btn_bag_go_forge.add_theme_constant_override("outline_size", 3)
	_btn_bag_go_forge.add_theme_font_size_override("font_size", 18)
	if _cached_font:
		_btn_bag_go_forge.add_theme_font_override("font", _cached_font)
	_btn_bag_go_forge.pressed.connect(_on_bag_go_forge_pressed)
	_btn_bag_go_forge.visible = false
	btn_row.add_child(_btn_bag_go_forge)

	# 操作提示
	_bag_tip = Label.new()
	_bag_tip.text = _t("點選格子查看詳情 · 雙擊或點擊按鈕使用")
	_bag_tip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(_bag_tip, 16, Color("#6B5E80"))
	right.add_child(_bag_tip)

	_refresh_bag_tab()


func _build_core_bag_section() -> PanelContainer:
	var cp := PanelContainer.new()
	cp.name = "CoreBagPanel"
	cp.custom_minimum_size = Vector2(0, 204)
	cp.add_theme_stylebox_override("panel", _create_panel_style(COLOR_CARD_WARM, COLOR_BORDER, 2, 4, 18))
	_core_bag_panel = cp

	var c_margin := MarginContainer.new()
	c_margin.add_theme_constant_override("margin_left", 12)
	c_margin.add_theme_constant_override("margin_right", 12)
	c_margin.add_theme_constant_override("margin_top", 8)
	c_margin.add_theme_constant_override("margin_bottom", 8)
	cp.add_child(c_margin)

	var c_vbox := VBoxContainer.new()
	c_vbox.add_theme_constant_override("separation", 6)
	c_margin.add_child(c_vbox)

	# 標題行
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	c_vbox.add_child(head)

	_core_title_lbl = Label.new()
	_core_title_lbl.name = "CoreTitleLabel"
	_core_title_lbl.text = _t("機芯部件背包（點擊替換裝備）")
	_apply_label_style(_core_title_lbl, 16, COLOR_TEXT_ORANGE, COLOR_BORDER, 3)
	head.add_child(_core_title_lbl)

	# 空狀態提示（當無未裝備機芯時防破版）
	_core_empty_lbl = Label.new()
	_core_empty_lbl.name = "CoreEmptyLabel"
	_core_empty_lbl.text = _t("背包暫無未裝備機芯部件")
	_apply_label_style(_core_empty_lbl, 14, Color("#6B5E80"))
	_core_empty_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_core_empty_lbl.visible = false
	c_vbox.add_child(_core_empty_lbl)

	# 卡片橫向滾動容器
	var scroll := ScrollContainer.new()
	scroll.name = "CoreScroll"
	scroll.custom_minimum_size = Vector2(0, 156)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	c_vbox.add_child(scroll)

	_core_cards_box = HBoxContainer.new()
	_core_cards_box.name = "CoreCardsBox"
	_core_cards_box.add_theme_constant_override("separation", 10)
	scroll.add_child(_core_cards_box)

	return cp


func _refresh_core_bag() -> void:
	if _core_bag_panel == null or _core_cards_box == null:
		return

	for c in _core_cards_box.get_children():
		_core_cards_box.remove_child(c)
		c.queue_free()

	var CoreSys := preload("res://scripts/systems/core_system.gd") if ResourceLoader.exists("res://scripts/systems/core_system.gd") else null
	var core_parts: Array = []
	if CoreSys != null:
		core_parts = CoreSys.get_inventory()

	if core_parts.is_empty():
		_core_bag_panel.visible = false
		if _core_empty_lbl:
			_core_empty_lbl.visible = true
		return

	_core_bag_panel.visible = true
	if _core_empty_lbl:
		_core_empty_lbl.visible = false

	var idx := 0
	for part in core_parts:
		if not (part is Dictionary):
			continue
		var card := _create_lobby_core_card(part, idx)
		if card:
			_core_cards_box.add_child(card)
		idx += 1


func _create_lobby_core_card(part: Dictionary, card_idx: int = 0) -> Control:
	var CoreSys := preload("res://scripts/systems/core_system.gd") if ResourceLoader.exists("res://scripts/systems/core_system.gd") else null
	var slot_id: String = str(part.get("slot", "mainspring"))
	var tier_id: String = str(part.get("tier", "white"))
	var tier_name: String = str(part.get("tier_name", "白"))
	var slot_name: String = str(part.get("slot_name", ""))
	if slot_name.is_empty() and CoreSys != null:
		slot_name = CoreSys.get_slot_name(slot_id)

	var tier_color: Color = CoreSys.get_tier_color(tier_id) if CoreSys != null else Color.WHITE

	var card := PanelContainer.new()
	var uid: String = str(part.get("uid", ""))
	if uid.is_empty():
		uid = str(card_idx)
	card.name = "CoreCard_" + uid
	card.custom_minimum_size = Vector2(146, 154)
	card.mouse_filter = Control.MOUSE_FILTER_STOP

	var cs := StyleBoxFlat.new()
	cs.bg_color = COLOR_CARD_WARM
	cs.border_color = tier_color
	cs.set_border_width_all(2)
	cs.border_width_bottom = 4
	cs.set_corner_radius_all(14)
	cs.shadow_color = Color(tier_color.r, tier_color.g, tier_color.b, 0.25)
	cs.shadow_size = 4
	cs.shadow_offset = Vector2(0, 2)
	card.add_theme_stylebox_override("panel", cs)

	# 全卡點擊換裝按鈕（底層），供點擊卡片換裝
	var btn := Button.new()
	btn.name = "CardButton"
	btn.flat = true
	btn.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	btn.mouse_filter = Control.MOUSE_FILTER_STOP
	btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	btn.focus_mode = Control.FOCUS_NONE
	btn.pressed.connect(func():
		_play_ui_sound()
		open_equip_panel(true)
	)
	card.add_child(btn)

	var margin := MarginContainer.new()
	margin.mouse_filter = Control.MOUSE_FILTER_IGNORE
	margin.add_theme_constant_override("margin_left", 8)
	margin.add_theme_constant_override("margin_right", 8)
	margin.add_theme_constant_override("margin_top", 4)
	margin.add_theme_constant_override("margin_bottom", 6)
	card.add_child(margin)

	var vb := VBoxContainer.new()
	vb.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vb.alignment = BoxContainer.ALIGNMENT_CENTER
	vb.add_theme_constant_override("separation", 2)
	margin.add_child(vb)

	var top_row := HBoxContainer.new()
	top_row.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top_row.alignment = BoxContainer.ALIGNMENT_CENTER
	top_row.add_theme_constant_override("separation", 6)
	vb.add_child(top_row)

	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(26, 26)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sdb = preload("res://scripts/art/sprite_db.gd")
	if sdb != null:
		var tex: Texture2D = sdb.core_slot_icon(slot_id)
		if tex:
			icon.texture = tex
	icon.modulate = tier_color
	top_row.add_child(icon)

	var swatch := ColorRect.new()
	swatch.name = "ColorSwatch"
	swatch.custom_minimum_size = Vector2(8, 16)
	swatch.color = tier_color
	swatch.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top_row.add_child(swatch)

	var tier_lbl := Label.new()
	tier_lbl.name = "TierLabel"
	var t_key := tier_name if tier_name.ends_with("階") else (tier_name + "階")
	tier_lbl.text = _t(t_key)
	_apply_label_style(tier_lbl, 14, tier_color if tier_id != "white" else COLOR_TEXT_DARK, COLOR_BORDER, 2)
	tier_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	top_row.add_child(tier_lbl)

	var slot_lbl := Label.new()
	slot_lbl.name = "SlotLabel"
	slot_lbl.text = _t(slot_name)
	slot_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(slot_lbl, 14, COLOR_TEXT_DARK)
	slot_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vb.add_child(slot_lbl)

	var action_lbl := Label.new()
	action_lbl.name = "ActionLabel"
	action_lbl.text = _t("更換裝備")
	action_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(action_lbl, 12, COLOR_TEXT_ORANGE)
	action_lbl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	vb.add_child(action_lbl)

	# 「拆解」果凍厚底按鈕（高 ≥ 50px，零系統 emoji）
	var dismantle_btn := Button.new()
	dismantle_btn.name = "DismantleButton"
	dismantle_btn.text = _t("拆解")
	dismantle_btn.custom_minimum_size = Vector2(126, 50)
	dismantle_btn.mouse_filter = Control.MOUSE_FILTER_STOP
	dismantle_btn.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	dismantle_btn.focus_mode = Control.FOCUS_NONE

	# 果凍厚底樣式 (多巴胺鮮亮珊瑚粉色 #FF5E8A, 5px 果凍厚底)
	var dis_normal := _create_button_style(Color("#FF5E8A"), COLOR_BORDER, 5, 14, 2)
	var dis_pressed := _create_button_style(Color("#E04E78"), COLOR_BORDER, 2, 14, 2)
	var dis_hover := _create_button_style(Color("#FF7096"), COLOR_BORDER, 5, 14, 2)
	dismantle_btn.add_theme_stylebox_override("normal", dis_normal)
	dismantle_btn.add_theme_stylebox_override("pressed", dis_pressed)
	dismantle_btn.add_theme_stylebox_override("hover", dis_hover)

	dismantle_btn.add_theme_font_size_override("font_size", 16)
	dismantle_btn.add_theme_color_override("font_color", Color.WHITE)
	dismantle_btn.add_theme_color_override("font_outline_color", COLOR_BORDER)
	dismantle_btn.add_theme_constant_override("outline_size", 3)
	if _cached_font:
		dismantle_btn.add_theme_font_override("font", _cached_font)

	var target_uid := uid
	dismantle_btn.pressed.connect(func():
		_play_ui_sound()
		var res: Dictionary = {}
		if CoreSys != null:
			res = CoreSys.dismantle_part(target_uid)
		else:
			var gs := _gs()
			if gs and gs.has_method("dismantle_core_part"):
				res = gs.dismantle_core_part(target_uid)

		if bool(res.get("ok", false)):
			var scrap_gain: int = int(res.get("iron_scrap", 0))
			_show_toast(_t("已拆解機芯，獲得 %d 鐵屑") % scrap_gain)
			_refresh_core_bag()
			_refresh_bag_tab(false)
			refresh_hud()
		else:
			var reason_k: String = str(res.get("message", "已裝備槽上的機芯不可拆"))
			_show_toast(_t(reason_k))
	)
	vb.add_child(dismantle_btn)

	return card


func _play_ui_sound() -> void:
	var tree := Engine.get_main_loop()
	if tree is SceneTree and (tree as SceneTree).root != null:
		var am: Node = (tree as SceneTree).root.get_node_or_null("AudioManager")
		if am and am.has_method("play_ui"):
			am.call("play_ui")


func _on_bag_cell_input(idx: int, ev: InputEvent) -> void:
	if not (ev is InputEventMouseButton and ev.pressed):
		return
	var button := (ev as InputEventMouseButton).button_index
	if idx < 0 or idx >= _bag_ids.size():
		return
	var id := str(_bag_ids[idx])
	if id == "":
		_selected_bag_item = ""
		_refresh_bag_tab(false)
		return
	if button == MOUSE_BUTTON_RIGHT:
		_selected_bag_item = id
		var inv := _get_inv_sys()
		if inv and inv.has_method("use_item"):
			var res: Dictionary = inv.call("use_item", id)
			_show_bag_msg(res)
		refresh_hud()
		_refresh_bag_tab()
		return
	if button == MOUSE_BUTTON_LEFT:
		var now := Time.get_ticks_msec()
		if _last_bag_click_i == idx and now - _last_bag_click_t < 350:
			_selected_bag_item = id
			var inv := _get_inv_sys()
			if inv and inv.has_method("use_item"):
				var res: Dictionary = inv.call("use_item", id)
				_show_bag_msg(res)
			refresh_hud()
			_last_bag_click_i = -1
			_refresh_bag_tab()
			return
		_last_bag_click_i = idx
		_last_bag_click_t = now
		_selected_bag_item = id
		_refresh_bag_tab()

func _on_bag_use_pressed() -> void:
	if _selected_bag_item == "":
		return
	var inv := _get_inv_sys()
	if inv and inv.has_method("use_item"):
		var res: Dictionary = inv.call("use_item", _selected_bag_item)
		_show_bag_msg(res)
	refresh_hud()
	_refresh_bag_tab()

func _show_bag_msg(res: Dictionary) -> void:
	var msg := str(res.get("msg", ""))
	if msg == "":
		return
	var main_node = get_parent()
	while main_node != null and not main_node.has_method("_show_toast"):
		main_node = main_node.get_parent()
	if main_node != null and bool(res.get("ok", false)):
		return
	_show_toast(msg)

func _on_bag_hotbar_pressed() -> void:
	if _selected_bag_item == "":
		return
	var inv := _get_inv_sys()
	if inv:
		if inv.has_method("ensure_hotbar"):
			inv.call("ensure_hotbar")
		var placed := false
		var gs := _gs()
		if gs and gs.get("hotbar") is Array:
			var hb: Array = gs.hotbar
			for i in range(hb.size()):
				if str(hb[i]) == "" or str(hb[i]) == _selected_bag_item:
					inv.call("set_hotbar", i, _selected_bag_item)
					placed = true
					break
		if not placed:
			inv.call("set_hotbar", 0, _selected_bag_item)
	_refresh_bag_tab()


func get_bag_go_forge_button() -> Button:
	return _btn_bag_go_forge


func _on_bag_go_forge_pressed() -> void:
	var am = get_tree().root.get_node_or_null("AudioManager") if get_tree() else null
	if am and am.has_method("play_ui"):
		am.call("play_ui")
	var target_item := _selected_bag_item
	_switch_tab(Tab.VILLAGE)
	open_forge(target_item)

func _refresh_bag_tab(allow_auto_select: bool = true) -> void:
	if _bag_layer == null:
		return
	var inv := _get_inv_sys()
	if inv and inv.has_method("grant_starter"):
		var gs := _gs()
		if gs and not gs.has_flag("inv.starter_given"):
			inv.call("grant_starter")

	_bag_ids.clear()
	var list: Array = inv.call("bag_list") if (inv and inv.has_method("bag_list")) else []

	# 若目前已選取的道具已經不在背包內，且背包還有道具，重選第一個
	if _selected_bag_item != "":
		var found := false
		for it in list:
			if it is Dictionary and str(it.get("id", "")) == _selected_bag_item:
				found = true
				break
		if not found:
			_selected_bag_item = str(list[0].get("id", "")) if (list.size() > 0 and allow_auto_select) else ""
	elif list.size() > 0 and allow_auto_select:
		_selected_bag_item = str(list[0].get("id", ""))


	for i in range(_bag_cells.size()):
		var cell: PanelContainer = _bag_cells[i]
		var icon: TextureRect = cell.find_child("Icon", true, false)
		var g: Label = cell.find_child("Glyph", true, false)
		var c: Label = cell.find_child("Count", true, false)
		if i < list.size():
			var it: Dictionary = list[i]
			var id := str(it.get("id", ""))
			_bag_ids.append(id)
			var def: Dictionary = it.get("def", {})
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
					g.text = str(def.get("glyph", "·"))
					g.add_theme_color_override("font_color", def.get("color", COLOR_TEXT_DARK))
					g.visible = true
			if c:
				var n := int(it.get("count", 0))
				c.text = str(n) if n > 1 else ""

			var sel := (id == _selected_bag_item)
			if sel:
				# 選取中：金黃柔和底 + 亮金橘厚邊框 (5px 厚底) + 金黃光暈
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
				# 未選取有道具：柔和天藍底 + 深藍紫立體邊框
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
			if icon:
				icon.visible = false
			if g:
				g.text = ""
				g.visible = false
			if c:
				c.text = ""
			# 空格：溫暖米黃底 + 淡深藍紫邊框
			var empty := StyleBoxFlat.new()
			empty.bg_color = COLOR_CARD_WARM
			empty.border_color = Color(0.20, 0.16, 0.30, 0.35)
			empty.set_border_width_all(2)
			empty.border_width_bottom = 3
			empty.set_corner_radius_all(16)
			cell.add_theme_stylebox_override("panel", empty)

	_update_bag_detail(inv)
	_refresh_core_bag()

func _update_bag_detail(inv: Node) -> void:
	if _bag_detail == null:
		return
	if _selected_bag_item == "" or inv == null:
		if _bag_preview_row:
			_bag_preview_row.visible = false
		_bag_detail.text = "[color=#1F1A3A][b][font_size=20]%s[/font_size][/b]\n\n%s\n\n[color=#C2600A]•[/color] %s\n[color=#C2600A]•[/color] %s\n[color=#C2600A]•[/color] %s[/color]" % [
			_t("冒險者背包"),
			_t("請點選左側格子查看道具詳情。"),
			_t("消耗品：使用回復狀態"),
			_t("素材：點擊使用可賣出金幣"),
			_t("重要物：劇情關鍵道具")
		]
		if _bag_use_btn:
			_bag_use_btn.disabled = true
			_bag_use_btn.text = _t("使用 / 賣出")
		if _bag_hb_btn:
			_bag_hb_btn.disabled = true
			_bag_hb_btn.text = _t("放到快捷欄")
		if _btn_bag_go_forge:
			_btn_bag_go_forge.visible = false
		return

	if _bag_hb_btn:
		_bag_hb_btn.disabled = false
		_bag_hb_btn.text = _t("放到快捷欄")

	var def: Dictionary = inv.call("catalog", _selected_bag_item) as Dictionary if inv.has_method("catalog") else {}
	var n: int = int(inv.call("count", _selected_bag_item)) if inv.has_method("count") else 0
	var kind: String = str(def.get("kind", ""))

	# 若 def 內無 kind 或未在 catalog，但為裝備系統內之武器裝備
	if kind.is_empty() and not _selected_bag_item.is_empty():
		var eq := _get_equip_sys()
		if eq != null:
			var eq_inst: Dictionary = eq.call("find_any", _selected_bag_item) if eq.has_method("find_any") else {}
			if not eq_inst.is_empty():
				var eq_slot := str(eq_inst.get("slot", ""))
				kind = "weapon" if eq_slot == "weapon" else "equipment"
			elif eq.has_method("base_def") and not (eq.call("base_def", _selected_bag_item) as Dictionary).is_empty():
				kind = "weapon"

	var is_equipment: bool = (kind == "equipment" or kind == "weapon")
	if _btn_bag_go_forge:
		_btn_bag_go_forge.visible = is_equipment
		_btn_bag_go_forge.text = _t("前往鍛造")

	if is_equipment and _bag_hb_btn:
		_bag_hb_btn.disabled = true

	var kind_s: String = kind
	match kind:
		"consumable":
			kind_s = _t("消耗品")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("使用道具")
		"material":
			kind_s = _t("素材（點擊使用可賣出）")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("賣出 (+%d金)") % int(def.get("sell", 1))
		"key":
			kind_s = _t("重要道具")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("無法使用")
		"equipment":
			kind_s = _t("裝備")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("使用 / 賣出")
		"weapon":
			kind_s = _t("武器")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("使用 / 賣出")
		_:
			kind_s = _t("道具")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("使用 / 賣出")

	var item_name: String = _t(str(def.get("name", _selected_bag_item)))
	var item_desc: String = _t(str(def.get("desc", "")))
	if is_equipment and (item_desc.is_empty() or def.is_empty()):
		var eq := _get_equip_sys()
		if eq != null:
			var eq_inst: Dictionary = eq.call("find_any", _selected_bag_item) if eq.has_method("find_any") else {}
			if not eq_inst.is_empty():
				item_name = _t(str(eq_inst.get("name", _selected_bag_item)))
				var tier := int(eq_inst.get("tier", 1))
				var q_label := str(eq_inst.get("quality_label", ""))
				item_desc = _t("器階：第 %d 階  品質：%s") % [tier, q_label]
			elif eq.has_method("base_def"):
				var bdef: Dictionary = eq.call("base_def", _selected_bag_item)
				if not bdef.is_empty():
					item_name = _t(str(bdef.get("name", _selected_bag_item)))
					item_desc = _t("基礎武器 · 點擊前往鍛造可進行強化")

	var icon_tex := get_item_icon(_selected_bag_item)
	if _bag_preview_row:
		_bag_preview_row.visible = true
		if _bag_detail_name:
			_bag_detail_name.text = item_name
		if _bag_detail_count:
			_bag_detail_count.text = "×%d" % n
		if _bag_detail_kind:
			_bag_detail_kind.text = _t("類型：%s") % kind_s
		if icon_tex != null:
			if _bag_detail_icon:
				_bag_detail_icon.texture = icon_tex
				_bag_detail_icon.visible = true
			if _bag_detail_glyph:
				_bag_detail_glyph.visible = false
		else:
			if _bag_detail_icon:
				_bag_detail_icon.visible = false
			if _bag_detail_glyph:
				_bag_detail_glyph.text = str(def.get("glyph", "·"))
				_bag_detail_glyph.visible = true

	_bag_detail.text = "[color=#4A3E60]%s[/color]" % item_desc

func _fmt_int(n: int) -> String:
	var neg := n < 0
	var s := str(absi(n))
	var out := ""
	while s.length() > 3:
		out = "," + s.substr(s.length() - 3, 3) + out
		s = s.substr(0, s.length() - 3)
	return ("-" if neg else "") + s + out

func _energy_hud_text() -> String:
	var es: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		es = (loop as SceneTree).root.get_node_or_null("EnergySystem")
	var cur := 0
	var mx := 15
	if es:
		if es.has_method("current"):
			cur = int(es.call("current"))
		if es.get("MAX_ENERGY") != null:
			mx = int(es.get("MAX_ENERGY"))
	var s := "%d/%d" % [cur, mx]
	if cur < mx and es and es.has_method("seconds_to_next"):
		var m := int(ceil(float(es.call("seconds_to_next")) / 60.0))
		s += " " + (_t("%d分") % maxi(1, m))
	return s

func _update_char_level_badge() -> void:
	if not _char_level_badge or not is_instance_valid(_char_level_badge):
		return
	var gs := _gs()
	var cur_lv := 1
	var cap := 30
	if gs:
		cur_lv = maxi(1, int(gs.level))
		if gs.has_method("get_level_cap"):
			cap = int(gs.call("get_level_cap"))
	if cur_lv >= cap:
		_char_level_badge.text = "Lv.%d · %s" % [cur_lv, _t("本季上限")]
	else:
		_char_level_badge.text = "Lv.%d" % cur_lv


func refresh_hud() -> void:
	var gs := _gs()
	var lv := 1
	var cap := 30
	var gold := 0
	var dust := 0
	var pow := 0
	if gs:
		lv = maxi(1, int(gs.level))
		if gs.has_method("get_level_cap"):
			cap = int(gs.call("get_level_cap"))
		gold = int(gs.gold)
		dust = int(gs.stardust)
		if gs.has_method("power_score"):
			pow = int(gs.call("power_score"))
	if _lv_label:
		if lv >= cap:
			_lv_label.text = "Lv.%d · %s" % [lv, _t("本季上限")]
		else:
			_lv_label.text = "Lv.%d" % lv
	if _name_label:
		_name_label.text = _get_hero_name()
	if _hero_name_tag:
		_hero_name_tag.text = _get_hero_name()
	if _profile_avatar:
		var cur_r := str(gs.player_race).strip_edges().to_lower() if gs and "player_race" in gs else "rabbit"
		_profile_avatar.texture = _get_hero_portrait(cur_r)
	if _hero_avatar:
		_load_hero_poses()
		if not _is_interacting and _tex_idle:
			_apply_hero_idle_visual()
	if _char_prev and _tex_idle:
		_apply_hero_idle_visual()
	if _power_label:
		_power_label.text = _t("戰力 %d") % pow
	if _char_power_badge:
		_char_power_badge.text = _t("有效戰力 %d") % (pow if pow > 0 else 482)
	_update_char_level_badge()
	if _energy_label:
		_energy_label.text = _energy_hud_text()
	if _gold_label:
		_gold_label.text = _fmt_int(gold)
	if _gem_label:
		_gem_label.text = _fmt_int(dust)
	refresh_vault_display()

func _apply_locale_texts() -> void:
	if _vault_title_lbl and is_instance_valid(_vault_title_lbl):
		_vault_title_lbl.text = Loc.t("vault.title")
	if _energy_title_label and is_instance_valid(_energy_title_label):
		_energy_title_label.text = _t("能量")
	if _gold_title_label and is_instance_valid(_gold_title_label):
		_gold_title_label.text = _t("金幣")
	if _gem_title_label and is_instance_valid(_gem_title_label):
		_gem_title_label.text = _t("星屑")
	if _shop_button and is_instance_valid(_shop_button):
		_shop_button.text = _t("商城")
	if _settings_button and is_instance_valid(_settings_button):
		_settings_button.text = _t("設置")

	var cur_loc := ContentLoc.locale()
	for btn in _hall_buttons:
		if is_instance_valid(btn):
			var title_k := str(btn.get_meta("hall_title_key", ""))
			var sub_k := str(btn.get_meta("hall_subtitle_key", ""))
			var title_t := _t(title_k) if not title_k.is_empty() else ""
			var sub_t := _t(sub_k) if not sub_k.is_empty() else ""

			btn.set_meta("hall_title", title_t)
			btn.set_meta("hall_subtitle", sub_t)
			btn.text = ""

			var t_lbl := btn.get_node_or_null("TextContainer/TitleLabel") as Label
			if t_lbl:
				t_lbl.text = title_t
				if cur_loc in ["en", "es"] and title_t.length() > 14:
					t_lbl.add_theme_font_size_override("font_size", 13)
				else:
					t_lbl.add_theme_font_size_override("font_size", 15)

			var s_lbl := btn.get_node_or_null("TextContainer/SubtitleLabel") as Label
			if s_lbl:
				s_lbl.text = sub_t
				if cur_loc in ["en", "es"]:
					s_lbl.add_theme_font_size_override("font_size", 9)
				else:
					s_lbl.add_theme_font_size_override("font_size", 10)

	if _sortie_title_label and is_instance_valid(_sortie_title_label):
		_sortie_title_label.text = _t("冒險出征 · 當前主線")
	if _sortie_stage_label and is_instance_valid(_sortie_stage_label):
		var cur_stage_text := _t("第二地區 · 白霧之地 (2-4 BOSS)")
		_sortie_stage_label.text = cur_stage_text
		if cur_stage_text.length() > 30:
			_sortie_stage_label.add_theme_font_size_override("font_size", 15)
		else:
			_sortie_stage_label.add_theme_font_size_override("font_size", 16)
	if _sortie_button and is_instance_valid(_sortie_button):
		_sortie_button.text = _t("前往出征")

	if _btn_mode_regions and is_instance_valid(_btn_mode_regions):
		_btn_mode_regions.text = _t("四區主線")
	if _btn_mode_colossus and is_instance_valid(_btn_mode_colossus):
		_refresh_colossus_mode_btn_text()

	for i in range(_region_buttons.size()):
		if i < REGION_KEYS.size() and is_instance_valid(_region_buttons[i]):
			_region_buttons[i].text = _t(REGION_KEYS[i])
	if _stages_container and is_instance_valid(_stages_container):
		_refresh_region_stages()

	if _soul_title_label and is_instance_valid(_soul_title_label):
		_soul_title_label.text = _t("聚魂殿 · 封靈罐四階")
	if _soul_desc_label and is_instance_valid(_soul_desc_label):
		_soul_desc_label.text = _t("聚引四大共鳴核心之魂：銳齒(攻) · 固甲(防) · 旋簧(血) · 全衡(衡)。點擊點亮更高階封靈罐！")
	if _gourd_btn_absorb and is_instance_valid(_gourd_btn_absorb):
		_gourd_btn_absorb.text = _t("一鍵吸收灰魂")
	if _gourd_btn_draw and is_instance_valid(_gourd_btn_draw):
		_gourd_btn_draw.text = _t("聚魂十連")
	_refresh_gourds_ui()

	for btn in _dock_buttons:
		if is_instance_valid(btn):
			var k := str(btn.get_meta("dock_key", ""))
			if not k.is_empty():
				btn.text = _t(k)

	_update_speech_bubble_text()

	if _hero_title_tag and is_instance_valid(_hero_title_tag):
		_hero_title_tag.text = "【%s】" % _t("初出茅廬")

	if _char_doll_title_label and is_instance_valid(_char_doll_title_label):
		_char_doll_title_label.text = _t("機體外觀 · 發條紙娃娃")
	if _btn_skill_dialog and is_instance_valid(_btn_skill_dialog):
		_btn_skill_dialog.text = _t("招式 · 核心心法")
	if _btn_wardrobe and is_instance_valid(_btn_wardrobe):
		_btn_wardrobe.text = _t("更衣 · 發條衣櫥")
	if _char_weapon_title_label and is_instance_valid(_char_weapon_title_label):
		_char_weapon_title_label.text = _t("武器輪替配置")
	if _char_weapon_sub_label and is_instance_valid(_char_weapon_sub_label):
		_char_weapon_sub_label.text = _t("點擊切換輪替順位 · 三段作戰序列")
	if _btn_change_weapon and is_instance_valid(_btn_change_weapon):
		_btn_change_weapon.text = _t("更換裝備")
	if _char_stat_title_label and is_instance_valid(_char_stat_title_label):
		_char_stat_title_label.text = _t("機體戰鬥屬性")
	if _char_power_badge and is_instance_valid(_char_power_badge):
		var gs := _gs()
		var cur_pow := 482
		if gs and gs.has_method("power_score") and int(gs.call("power_score")) > 0:
			cur_pow = int(gs.call("power_score"))
		_char_power_badge.text = _t("有效戰力 %d") % cur_pow
	_update_char_level_badge()

	_refresh_weapon_slot_buttons()
	_refresh_char_tab_stats(false)

	for card in _stat_cards:
		if is_instance_valid(card):
			var t_lbl := card.find_child("TitleLabel", true, false) as Label
			if t_lbl:
				var t_text := _t(str(card.get_meta("stat_title_key", "")))
				t_lbl.text = t_text
				if t_text.length() > 14:
					t_lbl.add_theme_font_size_override("font_size", 12)
				else:
					t_lbl.add_theme_font_size_override("font_size", 14)
			var sub_lbl := card.find_child("SubLabel", true, false) as Label
			if sub_lbl:
				var sub_text := _t(str(card.get_meta("stat_subtitle_key", "")))
				sub_lbl.text = sub_text
				if sub_text.length() > 24:
					sub_lbl.add_theme_font_size_override("font_size", 10)
				elif sub_text.length() > 16:
					sub_lbl.add_theme_font_size_override("font_size", 11)
				else:
					sub_lbl.add_theme_font_size_override("font_size", 12)
			var v_lbl := card.find_child("ValLabel", true, false) as Label
			if v_lbl:
				var v_k := str(card.get_meta("stat_val_key", ""))
				if not v_k.is_empty():
					v_lbl.text = _t(v_k)

	_refresh_equip_schematic()

	if _bag_title_lbl and is_instance_valid(_bag_title_lbl):
		_bag_title_lbl.text = _t("冒險者背包")
	if _bag_sub_lbl and is_instance_valid(_bag_sub_lbl):
		_bag_sub_lbl.text = _t("道具與戰魂倉庫 · 點選格子查看詳情")
	if _bag_tip and is_instance_valid(_bag_tip):
		_bag_tip.text = _t("點選格子查看詳情 · 雙擊或點擊按鈕使用")
	if _core_title_lbl and is_instance_valid(_core_title_lbl):
		_core_title_lbl.text = _t("機芯部件背包（點擊替換裝備）")
	if _core_empty_lbl and is_instance_valid(_core_empty_lbl):
		_core_empty_lbl.text = _t("背包暫無未裝備機芯部件")
	if _btn_bag_go_forge and is_instance_valid(_btn_bag_go_forge):
		_btn_bag_go_forge.text = _t("前往鍛造")
	if _bag_layer and is_instance_valid(_bag_layer):
		_update_bag_detail(_get_inv_sys())
		_refresh_core_bag()

	refresh_hud()

var _current_toast: Label = null

func _show_toast(msg: String) -> void:
	if _current_toast and is_instance_valid(_current_toast):
		_current_toast.queue_free()
		_current_toast = null
	var toast := Label.new()
	_current_toast = toast
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	var toast_w := clampi(int(msg.length() * 11) + 48, 360, 800)
	toast.offset_left = -int(toast_w / 2)
	toast.offset_right = int(toast_w / 2)
	toast.offset_top = 80
	toast.offset_bottom = 126
	var tsb := StyleBoxFlat.new()
	tsb.bg_color = Color(0.043, 0.039, 0.055, 0.95)
	tsb.border_color = GOLD_CLASSICAL
	tsb.set_border_width_all(1)
	tsb.border_width_bottom = 3
	tsb.set_corner_radius_all(8)
	tsb.content_margin_left = 16
	tsb.content_margin_right = 16
	toast.add_theme_stylebox_override("normal", tsb)
	toast.add_theme_color_override("font_color", INK_IVORY)
	toast.add_theme_font_size_override("font_size", 15)
	add_child(toast)

	var tw := create_tween()
	tw.tween_property(toast, "position:y", toast.position.y - 12, 0.3)
	tw.tween_interval(1.5)
	tw.tween_property(toast, "modulate:a", 0.0, 0.4)
	tw.tween_callback(toast.queue_free)


## 開啟換裝衣櫥彈窗 (非開局選角，是隨時可重複開合的衣櫥)
func open_wardrobe() -> void:
	var existing = get_node_or_null("WardrobeDialog")
	if existing != null:
		return

	var wardrobe_scn := load("res://scenes/ui/wardrobe_dialog.tscn")
	var dlg: Control = null
	if wardrobe_scn != null:
		dlg = wardrobe_scn.instantiate() as Control
	else:
		var WardrobeClass: GDScript = load("res://scripts/ui/wardrobe_dialog.gd")
		if WardrobeClass != null:
			dlg = WardrobeClass.new() as Control

	if dlg == null:
		push_error("無法載入 WardrobeDialog")
		return

	if "creation_mode" in dlg:
		dlg.creation_mode = false

	if dlg.has_signal("outfit_saved"):
		dlg.connect("outfit_saved", func(_race: String, _selections: Dictionary):
			_load_hero_poses()
			refresh_hud()
			_apply_hero_idle_visual()
			_show_toast(_t("換裝完成！新外裝已生效"))
		)

	# 開啟衣櫥時隱藏底層角色預覽，避免高亮剪影穿透全螢幕半透明遮罩 (review.md / 視覺品質標準)
	if _char_prev:
		_char_prev.visible = false
	var restore_prev := func():
		_load_hero_poses()
		if _hero_avatar and _tex_idle and not _is_interacting:
			_apply_hero_idle_visual()
		elif _char_prev and _tex_idle:
			_apply_hero_idle_visual()
		if _char_prev:
			_char_prev.visible = true
	dlg.tree_exited.connect(restore_prev)

	add_child(dlg)


## 開啟天宮鐵匠彈窗
func open_forge(target_weapon: Variant = null) -> Control:
	var existing = get_node_or_null("ForgeDialog")
	if existing != null and not existing.is_queued_for_deletion():
		if target_weapon != null and existing.has_method("select_target_equipment"):
			existing.call("select_target_equipment", target_weapon)
		return existing
	var existing_workshop = get_node_or_null("GemWorkshopDialog")
	if existing_workshop != null:
		if existing_workshop.get_parent() == self:
			remove_child(existing_workshop)
		existing_workshop.queue_free()
	var ForgeClass: GDScript = load("res://scripts/ui/forge_dialog.gd")
	if ForgeClass == null:
		push_error("無法載入 ForgeDialog")
		return null
	var dlg: Control = ForgeClass.new() as Control
	dlg.name = "ForgeDialog"
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	if dlg.has_signal("workshop_requested"):
		dlg.connect("workshop_requested", func():
			open_gem_workshop()
		)
	add_child(dlg)
	if target_weapon != null and dlg.has_method("select_target_equipment"):
		dlg.call("select_target_equipment", target_weapon)
	return dlg


## 開啟手藝工坊寶石彈窗
func open_gem_workshop() -> Control:
	var existing = get_node_or_null("GemWorkshopDialog")
	if existing != null and not existing.is_queued_for_deletion():
		return existing
	var existing_forge = get_node_or_null("ForgeDialog")
	if existing_forge != null:
		if existing_forge.get_parent() == self:
			remove_child(existing_forge)
		existing_forge.queue_free()
	var GemClass: GDScript = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemClass == null:
		push_error("無法載入 GemWorkshopDialog")
		return null
	var dlg: Control = GemClass.new() as Control
	dlg.name = "GemWorkshopDialog"
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	if dlg.has_signal("forge_requested"):
		dlg.connect("forge_requested", func():
			open_forge()
		)
	add_child(dlg)
	return dlg


## 開啟招式心法彈窗
func open_skill_dialog() -> Control:
	var existing = get_node_or_null("SkillDialog")
	if existing != null:
		return existing
	var SkillClass: GDScript = load("res://scripts/ui/skill_dialog.gd")
	if SkillClass == null:
		push_error("無法載入 SkillDialog")
		return null
	var dlg: Control = SkillClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	if dlg.has_signal("practice_dummy_requested"):
		dlg.practice_dummy_requested.connect(func():
			request_battle.emit("training_dummy")
		)
	add_child(dlg)
	return dlg


## 開啟更換裝備武器庫彈窗
func open_weapon_swap_dialog(slot_idx: int = -1) -> Control:
	var existing = get_node_or_null("WeaponSwapDialog")
	if existing != null and not existing.is_queued_for_deletion():
		return existing
	var target: int = slot_idx if slot_idx >= 0 else _selected_weapon_slot
	var DlgClass: GDScript = load("res://scripts/ui/weapon_swap_dialog.gd")
	if DlgClass == null:
		push_error("無法載入 WeaponSwapDialog")
		return null
	var dlg: Control = DlgClass.new() as Control
	dlg.name = "WeaponSwapDialog"
	dlg.z_index = 85
	dlg.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if dlg.has_method("setup"):
		dlg.call("setup", target)
	dlg.tree_exited.connect(func():
		_weapon_swap_dialog = null
		_sync_hero_weapon_paperdoll()
		_refresh_char_tab_stats(true)
		_refresh_weapon_slot_buttons()
		refresh_hud()
	)
	if dlg.has_signal("weapon_swapped"):
		dlg.connect("weapon_swapped", func(_s_idx: int, _uid: String):
			_sync_hero_weapon_paperdoll()
			_refresh_char_tab_stats(true)
			_refresh_weapon_slot_buttons()
			refresh_hud()
		)
	if dlg.has_signal("slot_unequipped"):
		dlg.connect("slot_unequipped", func(_s_idx: int):
			_sync_hero_weapon_paperdoll()
			_refresh_char_tab_stats(true)
			_refresh_weapon_slot_buttons()
			refresh_hud()
		)
	if dlg.has_signal("forge_requested"):
		dlg.connect("forge_requested", func():
			open_forge()
		)
	add_child(dlg)
	_weapon_swap_dialog = dlg
	return dlg


## 切換至出征分頁（與右側看板「前往出征」按鈕同一條入口）
func go_to_sortie() -> void:
	_switch_tab(Tab.ADVENTURE)
	_switch_adventure_submode(AdventureSubMode.REGIONS)


## 切換至出征分頁並開啟停擺巨偶模式
func go_to_colossus() -> void:
	_switch_tab(Tab.ADVENTURE)
	_switch_adventure_submode(AdventureSubMode.COLOSSUS)


## 開啟冒險委託每日上發條彈窗
func open_windup_daily() -> Control:
	var existing = get_node_or_null("WindupDailyDialog")
	if existing != null:
		return existing
	var WindupClass: GDScript = load("res://scripts/ui/windup_daily_dialog.gd")
	if WindupClass == null:
		push_error("無法載入 WindupDailyDialog")
		return null
	var dlg: Control = WindupClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	if dlg.has_signal("sortie_requested"):
		dlg.sortie_requested.connect(func():
			go_to_sortie()
		)
	if dlg.has_signal("colossus_requested"):
		dlg.colossus_requested.connect(func():
			go_to_colossus()
		)
	add_child(dlg)
	return dlg


## 開啟能量/體力補充彈窗（看廣告拿能量）
func open_energy_dialog() -> Control:
	var existing = get_node_or_null("EnergyLackDialog")
	if existing != null:
		return existing
	var EnergyLackClass: GDScript = load("res://scripts/ui/energy_lack_dialog.gd")
	if EnergyLackClass == null:
		push_error("無法載入 EnergyLackDialog")
		return null
	var dlg: Control = EnergyLackClass.new() as Control
	dlg.z_index = 85
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


## 開啟商城/儲值彈窗
func open_shop() -> Control:
	var existing = get_node_or_null("ShopDialog")
	if existing != null:
		return existing
	var ShopClass: GDScript = load("res://scripts/ui/shop_dialog.gd")
	if ShopClass == null:
		push_error("無法載入 ShopDialog")
		return null
	var dlg: Control = ShopClass.new() as Control
	dlg.z_index = 85
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


## 開啟角色裝備/整備面板並滾動至機芯五槽
func open_equip_panel(scroll_to_core: bool = false) -> Control:
	_clear_new_core_drop_notification()
	var existing = get_node_or_null("EquipLayer")
	if existing != null and is_instance_valid(existing):
		existing.queue_free()
	var EquipPanelScn: GDScript = load("res://scripts/ui/panels/equip_panel.gd")
	if EquipPanelScn == null:
		push_error("無法載入 EquipPanel")
		return null
	_equip_panel_instance = EquipPanelScn.new(self)
	_equip_panel_instance.open("core" if scroll_to_core else "")
	var layer: Control = _equip_panel_instance._layer
	if layer != null:
		layer.z_index = 85
		if scroll_to_core:
			call_deferred("_do_scroll_to_core", layer)
	return layer


func _do_scroll_to_core(layer: Control) -> void:
	if not is_instance_valid(layer):
		return
	var scroll := layer.find_child("EquipScroll", true, false) as ScrollContainer
	if scroll:
		scroll.scroll_vertical = 240


func close_equip_panel() -> void:
	var layer = get_node_or_null("EquipLayer")
	if layer != null and is_instance_valid(layer):
		if layer.get_parent() != null:
			layer.get_parent().remove_child(layer)
		layer.queue_free()
	_equip_panel_instance = null
	_refresh_bag_tab()
	refresh_hud()


# EquipPanel host 介面支援
func ui_clear_host() -> void:
	var old = get_node_or_null("EquipLayer")
	if old != null and is_instance_valid(old):
		if old.get_parent() != null:
			old.get_parent().remove_child(old)
		old.queue_free()


func ui_reset_fade() -> void:
	pass


func ui_host() -> Control:
	return self


func ui_refresh_hud() -> void:
	refresh_hud()


func ui_toast(msg: String) -> void:
	_show_toast(msg)


func ui_goto(target: String) -> bool:
	if target == "hub":
		close_equip_panel()
		return true
	var p := get_parent()
	if p != null and p.has_method("ui_goto"):
		return bool(p.call("ui_goto", target))
	return false




