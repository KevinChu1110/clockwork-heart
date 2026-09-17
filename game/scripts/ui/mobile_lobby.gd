class_name MobileLobby
extends Control
## 勇者之魂 (Clockwork Heart) - 神殿黑曜石 × 古典黃金齒輪手遊大廳
## 視覺特徵：希臘神殿石柱 + 深邃黑曜石地坪 + 古典黃金齒輪 + 白兔多姿態動態待機 (無 Emoji、無系統字型符號)

signal request_battle(mode: String)
signal request_settings()

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ResponsiveUi = preload("res://scripts/ui/responsive_ui.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const FootShadowShader = preload("res://shaders/foot_shadow.gdshader")

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
var _active_hall_index: int = -1
var _char_prev: TextureRect = null
var _equip_schematic: VBoxContainer = null
var _cached_font: Font = null
var _bag_grid: GridContainer = null
var _bag_cells: Array = []
var _bag_ids: Array = []
var _selected_bag_item: String = ""
var _bag_detail: RichTextLabel = null
var _bag_use_btn: Button = null
var _bag_hb_btn: Button = null
var _bag_tip: Label = null
var _last_bag_click_i: int = -1
var _last_bag_click_t: int = 0

## 角色動態與姿態
var _profile_avatar: TextureRect
var _hero_avatar: TextureRect
var _hero_shadow: TextureRect
var _hero_name_tag: Label
var _speech_bubble: PanelContainer
var _speech_label: Label
var _particles_root: Control
var _breathe_tween: Tween
var _bubble_tween: Tween
var _poke_tween: Tween
var _idle_action_timer: float = 0.0
var _is_interacting: bool = false
var enable_idle_breathing: bool = true
var enable_idle_flavor: bool = true

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

## 四地區出征
var _selected_region: int = 1 # 0: 閣樓與堡壘, 1: 白霧之地, 2: 道場與西林, 3: 潮岸與終境
var _stages_container: VBoxContainer
var _region_buttons: Array[Button] = []

## 角色分頁武器槽與戰鬥屬性
var _weapon_slot_buttons: Array[Button] = []
var _selected_weapon_slot: int = 0
var _weapon_slot_hint_label: Label = null
var _char_power_badge: Label = null

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

func _get_hero_name() -> String:
	var gs := _gs()
	if gs and "player_name" in gs:
		var pname: String = str(gs.player_name).strip_edges()
		if not pname.is_empty():
			return pname
	return DEFAULT_HERO_NAME

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	if ResourceLoader.exists(FONT_HUNINN):
		_cached_font = load(FONT_HUNINN) as Font
	var inv := _get_inv_sys()
	if inv and inv.has_signal("inventory_changed"):
		inv.inventory_changed.connect(func():
			if _current_tab == Tab.BAG:
				_refresh_bag_tab()
		)
	_load_hero_poses()
	_build_ui()
	refresh_hud()
	_switch_tab(Tab.VILLAGE)
	call_deferred("_apply_safe")

func _apply_safe() -> void:
	ResponsiveUi.apply_safe_margins(self)

func _get_hero_portrait(race: String) -> Texture2D:
	var r := race.to_lower().strip_edges()
	var p_path := ""
	match r:
		"rabbit": p_path = "res://assets/sprites/portraits/rabbit.png"
		"fox": p_path = "res://assets/sprites/portraits/fox_mage.png"
		"lion": p_path = "res://assets/sprites/portraits/lion_knight.png"
		"boar": p_path = "res://assets/sprites/portraits/boar_warrior.png"
		"macaque": p_path = "res://assets/sprites/portraits/macaque.png"
		"tiger": p_path = "res://assets/sprites/portraits/tiger.png"
		"crane": p_path = "res://assets/sprites/portraits/crane.png"
		"bear": p_path = "res://assets/sprites/portraits/bear.png"
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


func _hero_display_tex() -> Texture2D:
	## 大廳／角色分頁：沒自訂外裝時改讀官方品牌立牌高清待機（LINEAR）；有換裝時有 512 走 512，其餘維持既有 128 紙娃娃 (NEAREST)
	var race := _current_race()
	var slots := _current_paperdoll_slots()
	if _has_custom_paperdoll_outfit(slots):
		var comp_512: Texture2D = PaperdollRenderer.build_composite_texture_512(race, slots)
		if comp_512 != null:
			return comp_512
		var legacy: Texture2D = _get_hero_equipped_idle_texture()
		if legacy != null:
			return legacy
		return _tex_idle

	# 沒自訂外裝時：九族讀取官方品牌立牌高清展示貼圖
	var p := "res://assets/sprites/player/showcase/%s_idle_hd.png" % race
	if ResourceLoader.exists(p):
		return load(p) as Texture2D
	var p256 := "res://assets/sprites/player/paperdoll/%s/showcase_idle_256.png" % race
	if ResourceLoader.exists(p256):
		return load(p256) as Texture2D
	var p512 := "res://assets/sprites/player/paperdoll/%s/proof_paperdoll_%s_composite_512.png" % [race, race]
	if ResourceLoader.exists(p512):
		return load(p512) as Texture2D
	return _tex_idle


func _apply_hero_idle_visual() -> void:
	var hd: Texture2D = _hero_display_tex()
	if hd == null:
		hd = _tex_idle
	if _hero_avatar:
		_hero_avatar.texture = hd
		if hd != null and hd.get_width() >= 256:
			_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		else:
			_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if _char_prev:
		_char_prev.texture = hd
		if hd != null and hd.get_width() >= 256:
			_char_prev.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		else:
			_char_prev.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
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
		return "未裝備"
	var def: Dictionary = PaperdollRenderer.get_slot_def(slot_id)
	var variants: Variant = def.get("sample_variants", [])
	if variants is Array:
		for v in variants:
			if v is Dictionary and str(v.get("id", "")) == iid:
				var n := str(v.get("name", "")).strip_edges()
				if n != "":
					return n
	var clean := iid
	for pfx in ["wpn_", "costume_", "key_", "curio_", "paint_", "ear_", "core_"]:
		if clean.begins_with(pfx):
			clean = clean.trim_prefix(pfx)
			break
	return clean.replace("_", " ")


func _refresh_equip_schematic() -> void:
	if _equip_schematic == null:
		return
	for c in _equip_schematic.get_children():
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
			slot_title = "外裝"
		elif slot_title == "手持武器外觀":
			slot_title = "武器"
		elif slot_title == "背部發條鑰匙":
			slot_title = "發條"
		elif slot_title == "隨身奇玩與尾部機關":
			slot_title = "奇玩"
		var item_id := str(entry.get("chosen_item", ""))
		if item_id.strip_edges().is_empty():
			var tpath := str(entry.get("texture_path", ""))
			item_id = tpath.get_file().get_basename()
		var item_name := _variant_display_name(sid, item_id)
		var tex: Texture2D = entry.get("texture", null)
		_add_equip_chip(_equip_schematic, slot_title, item_name, tex)


func _add_equip_chip(parent: Container, slot_title: String, item_name: String, tex: Texture2D) -> void:
	var btn := Button.new()
	btn.custom_minimum_size = Vector2(0, 52)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
	UiStyle.style_button(btn, false)
	btn.add_theme_font_size_override("font_size", 13)
	if tex != null:
		btn.icon = tex
		btn.expand_icon = true
		btn.add_theme_constant_override("icon_max_width", 36)
		btn.add_theme_constant_override("h_separation", 8)
	btn.text = "%s  %s" % [slot_title, item_name]
	btn.pressed.connect(func(): open_wardrobe())
	parent.add_child(btn)


func _start_breathe_tween() -> void:
	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()
	if _hero_avatar:
		_hero_avatar.scale = Vector2.ONE
	if _hero_shadow:
		_hero_shadow.scale = Vector2.ONE
	if not enable_idle_breathing:
		return
	_breathe_tween = create_tween().set_loops()
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(1.03, 0.97), 1.1).set_trans(Tween.TRANS_SINE)
	_breathe_tween.tween_property(_hero_avatar, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)
	if _hero_shadow:
		_breathe_tween.parallel().tween_property(_hero_shadow, "scale", Vector2(0.98, 1.02), 1.1).set_trans(Tween.TRANS_SINE)


func _restore_hero_idle() -> void:
	_tex_idle = _get_hero_equipped_idle_texture()
	_apply_hero_idle_visual()
	if _hero_avatar:
		_hero_avatar.position = Vector2(-125, -140)
		_hero_avatar.scale = Vector2.ONE
	if _speech_bubble:
		_speech_bubble.visible = false
	_is_interacting = false
	_start_breathe_tween()


func _load_hero_poses() -> void:
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

	if _tex_idle == null:
		_tex_idle = SpriteDB.player_idle()
	if _tex_attack == null and ResourceLoader.exists("res://assets/sprites/player/poses/attack.png"):
		_tex_attack = load("res://assets/sprites/player/poses/attack.png")
	if _tex_skill == null and ResourceLoader.exists("res://assets/sprites/player/poses/skill.png"):
		_tex_skill = load("res://assets/sprites/player/poses/skill.png")
	if _tex_telegraph == null and ResourceLoader.exists("res://assets/sprites/player/poses/telegraph.png"):
		_tex_telegraph = load("res://assets/sprites/player/poses/telegraph.png")
	if _tex_recover == null and ResourceLoader.exists("res://assets/sprites/player/poses/recover.png"):
		_tex_recover = load("res://assets/sprites/player/poses/recover.png")
	if _tex_hit == null and ResourceLoader.exists("res://assets/sprites/player/poses/hit.png"):
		_tex_hit = load("res://assets/sprites/player/poses/hit.png")

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
	## 1. 背景插畫（神殿黑曜石底圖 / LINEAR 平滑採樣）
	var bg := TextureRect.new()
	bg.name = "TempleLobbyBg"
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	
	var temple_path := "res://assets/sprites/maps/temple_lobby_bg.png"
	var abs_temple_path := ProjectSettings.globalize_path(temple_path)
	if FileAccess.file_exists(abs_temple_path):
		var img := Image.load_from_file(abs_temple_path)
		if img and not img.is_empty():
			bg.texture = ImageTexture.create_from_image(img)
	if bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/sky_kingdom_bg.png"):
		bg.texture = load("res://assets/sprites/maps/sky_kingdom_bg.png")
	elif bg.texture == null and ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	add_child(bg)

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
	## 頂欄／底 Dock 大橫條：暖金玻璃，讓神殿背景透出來
	var s := StyleBoxFlat.new()
	s.bg_color = Color(1.0, 0.94, 0.78, 0.70)
	s.border_color = COLOR_BORDER
	s.set_border_width_all(2)
	s.border_width_bottom = 5
	s.set_corner_radius_all(20)
	s.shadow_color = Color(0.12, 0.10, 0.23, 0.16)
	s.shadow_size = 8
	s.shadow_offset = Vector2(0, 3)
	return s

## ──────────────────────────────────────────
## 黃金以太塵埃微粒 (Golden Ether Motes)
## ──────────────────────────────────────────
func _spawn_floating_ether_motes() -> void:
	var gp: Node = null
	var loop := Engine.get_main_loop()
	if loop is SceneTree:
		gp = (loop as SceneTree).root.get_node_or_null("GraphicsProfile")
	var n := 14
	if gp != null:
		n = int(gp.particle_count(14))
	if n <= 0:
		return
	for i in range(n):
		var star := ColorRect.new()
		var sz := 4.0 + float((i % 3) * 2)
		star.custom_minimum_size = Vector2(sz, sz)
		star.size = Vector2(sz, sz)
		star.pivot_offset = Vector2(sz * 0.5, sz * 0.5)
		star.rotation = PI * 0.25
		var c := Color(0.831, 0.686, 0.216, 0.70) if i % 2 == 0 else Color(0.243, 0.812, 0.749, 0.60)
		star.color = c
		star.position = Vector2(randf_range(40.0, 1240.0), randf_range(100.0, 580.0))
		_particles_root.add_child(star)

		# 緩慢升騰與呼吸淡入淡出
		var tw := create_tween().set_loops()
		var dur := randf_range(2.5, 4.0)
		var dy := randf_range(-15.0, -30.0)
		tw.tween_property(star, "position:y", star.position.y + dy, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.2, dur * 0.5)
		tw.tween_property(star, "position:y", star.position.y, dur).set_trans(Tween.TRANS_SINE)
		tw.parallel().tween_property(star, "modulate:a", 0.85, dur * 0.5)

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
	psb.bg_color = COLOR_CARD_WARM
	psb.border_color = COLOR_BORDER
	psb.set_border_width_all(1)
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
	_lv_label.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	_lv_label.add_theme_font_size_override("font_size", 16)
	row1.add_child(_lv_label)

	_name_label = Label.new()
	_name_label.text = _get_hero_name()
	_name_label.add_theme_font_size_override("font_size", 17)
	_name_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	row1.add_child(_name_label)
	info_v.add_child(row1)

	var pwr_row := HBoxContainer.new()
	pwr_row.add_theme_constant_override("separation", 4)
	_power_label = Label.new()
	_power_label.text = "戰力 0"
	_power_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_power_label.add_theme_font_size_override("font_size", 13)
	pwr_row.add_child(_power_label)
	info_v.add_child(pwr_row)
	p_box.add_child(info_v)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	h.add_child(spacer)

	## 奶油白三寶膠囊（帶對應發條核心圖示與果凍厚底質感）
	_energy_label = _add_clean_capsule(h, "能量", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_energy_key.png")
	var energy_cap: PanelContainer = _energy_label.get_parent().get_parent() as PanelContainer
	if energy_cap:
		energy_cap.mouse_filter = Control.MOUSE_FILTER_STOP
		energy_cap.gui_input.connect(func(ev: InputEvent):
			if ev is InputEventMouseButton and ev.pressed and ev.button_index == MOUSE_BUTTON_LEFT:
				open_energy_dialog()
		)
	_gold_label = _add_clean_capsule(h, "金幣", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_gold_coin.png")
	_gem_label = _add_clean_capsule(h, "星屑", "—", COLOR_GOLD_DARK, "res://assets/icons/hud/icon_gem_stardust.png")

	var set_btn := Button.new()
	set_btn.name = "SettingsButton"
	set_btn.text = "設置"
	UiStyle.style_button(set_btn, false)
	set_btn.custom_minimum_size = Vector2(108, 50)
	set_btn.add_theme_font_size_override("font_size", 15)
	var set_icon := "res://assets/icons/hud/icon_settings_gear.png"
	if ResourceLoader.exists(set_icon):
		set_btn.icon = load(set_icon)
		set_btn.expand_icon = true
		set_btn.add_theme_constant_override("icon_max_width", 22)
		set_btn.add_theme_constant_override("h_separation", 6)
	set_btn.pressed.connect(func():
		var s_scn := load("res://scripts/ui/mobile_settings.gd")
		var s_ui: Control = s_scn.new()
		s_ui.z_index = 80
		add_child(s_ui)
	)
	h.add_child(set_btn)

func _add_clean_capsule(parent: Container, title: String, val: String, accent: Color, icon_path: String = "") -> Label:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = COLOR_CARD_WARM
	csb.border_color = COLOR_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 4
	csb.set_corner_radius_all(16)
	csb.content_margin_left = 12
	csb.content_margin_right = 14
	csb.content_margin_top = 4
	csb.content_margin_bottom = 5
	csb.shadow_color = Color(0.12, 0.10, 0.23, 0.15)
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
	il.text = title
	il.add_theme_font_size_override("font_size", 13)
	il.add_theme_color_override("font_color", accent)
	il.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	h.add_child(il)

	var vl := Label.new()
	vl.text = val
	vl.add_theme_font_size_override("font_size", 15)
	vl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
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
		{"tab": Tab.VILLAGE, "title": _t("發條新村"), "icon": "res://assets/icons/hud/icon_dock_village.png"},
		{"tab": Tab.CHARACTER, "title": _t("角色裝備"), "icon": "res://assets/icons/hud/icon_dock_equip.png"},
		{"tab": Tab.ADVENTURE, "title": _t("四區出征"), "icon": "res://assets/icons/hud/icon_dock_campaign.png"},
		{"tab": Tab.SOUL_HALL, "title": _t("聚魂殿堂"), "icon": "res://assets/icons/hud/icon_dock_soul.png"},
		{"tab": Tab.BAG, "title": _t("冒險背包"), "icon": "res://assets/icons/hud/icon_dock_bag.png"},
	]

	_dock_buttons.clear()
	for d in tabs:
		var btn := Button.new()
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		btn.custom_minimum_size = Vector2(0, 56)
		btn.text = str(d["title"])
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

func _switch_tab(target: Tab) -> void:
	_current_tab = target
	if _village_layer:
		_village_layer.visible = (target == Tab.VILLAGE)
	if _char_layer:
		_char_layer.visible = (target == Tab.CHARACTER)
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

## ──────────────────────────────────────────
## 每幀小動作判定 (動態待機自然活化)
## ──────────────────────────────────────────
func _process(delta: float) -> void:
	if _current_tab != Tab.VILLAGE or _is_interacting or not enable_idle_flavor:
		return

	_idle_action_timer += delta
	if _idle_action_timer > 5.0:
		_idle_action_timer = 0.0
		_play_random_idle_flavor()

func _play_random_idle_flavor() -> void:
	var roll := randi() % 3
	if roll == 0 and _tex_telegraph:
		## 小伸展站姿
		_hero_avatar.texture = _tex_telegraph
		_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		var tw := create_tween()
		tw.tween_interval(1.2)
		tw.tween_callback(func():
			if not _is_interacting:
				_restore_hero_idle()
		)
	elif roll == 1 and _tex_recover:
		## 伸個懶腰
		_hero_avatar.texture = _tex_recover
		_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		var tw := create_tween()
		tw.tween_interval(1.0)
		tw.tween_callback(func():
			if not _is_interacting:
				_restore_hero_idle()
		)

## ──────────────────────────────────────────
## Tab 1: 發條新村 (神殿日晷展台 + 點擊互動 + 黃金以太粒子)
## ──────────────────────────────────────────
func _build_village_tab() -> void:
	_village_layer = Control.new()
	_village_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_content_root.add_child(_village_layer)

	## 中央英雄展台
	var stage_anchor := Control.new()
	stage_anchor.set_anchors_preset(Control.PRESET_CENTER)
	stage_anchor.offset_top = 45
	_village_layer.add_child(stage_anchor)

	## 1. 角色腳底接地軟影 (Foot Soft Shadow / review.md 第 16 條)
	_hero_shadow = TextureRect.new()
	_hero_shadow.name = "HeroFootShadow"
	_hero_shadow.add_to_group("soft_shadow")
	_hero_shadow.offset_left = -62
	_hero_shadow.offset_top = 74
	_hero_shadow.offset_right = 98
	_hero_shadow.offset_bottom = 116
	_hero_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	_hero_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_hero_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hero_shadow.texture = _soft_shadow_tex()
	_hero_shadow.pivot_offset = Vector2(80, 21)

	var shadow_mat := ShaderMaterial.new()
	shadow_mat.shader = FootShadowShader
	shadow_mat.set_shader_parameter("strength", 0.95)
	shadow_mat.set_shader_parameter("shadow_color", Color(0.01, 0.01, 0.02, 1.0))
	_hero_shadow.material = shadow_mat
	stage_anchor.add_child(_hero_shadow)

	## 1.1 緊密接地閉塞陰影 (Contact Occlusion Shadow)
	var contact_shadow := TextureRect.new()
	contact_shadow.name = "HeroContactShadow"
	contact_shadow.add_to_group("soft_shadow")
	contact_shadow.offset_left = -38
	contact_shadow.offset_top = 84
	contact_shadow.offset_right = 74
	contact_shadow.offset_bottom = 104
	contact_shadow.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	contact_shadow.stretch_mode = TextureRect.STRETCH_SCALE
	contact_shadow.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	contact_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	contact_shadow.texture = _soft_shadow_tex()

	var contact_mat := ShaderMaterial.new()
	contact_mat.shader = FootShadowShader
	contact_mat.set_shader_parameter("strength", 0.98)
	contact_mat.set_shader_parameter("shadow_color", Color(0.005, 0.005, 0.01, 1.0))
	contact_shadow.material = contact_mat
	stage_anchor.add_child(contact_shadow)

	## 2. 2.2 頭身白兔主角
	_hero_avatar = TextureRect.new()
	_hero_avatar.offset_left = -125
	_hero_avatar.offset_top = -140
	_hero_avatar.offset_right = 125
	_hero_avatar.offset_bottom = 125
	_hero_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_hero_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_hero_avatar.pivot_offset = Vector2(125, 240)
	_apply_hero_idle_visual()
	stage_anchor.add_child(_hero_avatar)

	var hero_click := Button.new()
	hero_click.set_anchors_preset(Control.PRESET_FULL_RECT)
	hero_click.flat = true
	hero_click.pressed.connect(_on_hero_clicked)
	_hero_avatar.add_child(hero_click)

	## 3. 頭頂稱號與名字（精巧微型名牌，上移避開齒輪中央能量光芒與核心，拿掉重陰影）
	var tag_panel := PanelContainer.new()
	tag_panel.set_anchors_preset(Control.PRESET_CENTER_TOP)
	tag_panel.offset_left = -56
	tag_panel.offset_top = -174
	tag_panel.offset_right = 56
	tag_panel.offset_bottom = -132
	tag_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE

	var tag_sb := StyleBoxFlat.new()
	tag_sb.bg_color = Color(1.0, 0.992, 0.973, 0.92) # 奶油白 #FFFDF8 @ 92%
	tag_sb.border_color = COLOR_BORDER # #1F1A3A 深藍紫
	tag_sb.set_border_width_all(1)
	tag_sb.border_width_bottom = 2
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
	_hero_name_tag.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_hero_name_tag.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.8))
	_hero_name_tag.add_theme_constant_override("outline_size", 2)
	tag_v.add_child(_hero_name_tag)

	var title_l := Label.new()
	title_l.text = "【初出茅廬】"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 11)
	title_l.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	title_l.add_theme_color_override("font_outline_color", Color(1.0, 1.0, 1.0, 0.6))
	title_l.add_theme_constant_override("outline_size", 1)
	tag_v.add_child(title_l)

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
	_speech_label.text = "背後的發條上得剛剛好，出發吧！"
	_speech_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	_speech_label.add_theme_font_size_override("font_size", 14)
	_speech_bubble.add_child(_speech_label)
	_hero_avatar.add_child(_speech_bubble)

	## 呼吸動畫
	_start_breathe_tween()

	## 左側四大殿堂黑曜石金屬浮雕卡牌 (天宮鐵匠、手藝工坊、演武競技、冒險委託) -> 多巴胺果凍厚底卡
	var left_shops := VBoxContainer.new()
	left_shops.name = "HallCardsContainer"
	left_shops.set_anchors_preset(Control.PRESET_LEFT_WIDE)
	left_shops.offset_left = 32
	left_shops.offset_top = 20
	left_shops.offset_right = 248
	left_shops.offset_bottom = -20
	left_shops.add_theme_constant_override("separation", 12)
	_village_layer.add_child(left_shops)

	_hall_buttons.clear()
	_active_hall_index = -1

	_add_hall_card(left_shops, _t("天宮鐵匠"), "品質轉化 · 裝備鍛造", "res://assets/icons/hud/icon_hall_forge.png", func():
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

	## 裝備示意：高清立繪旁列出當前外裝／武器／發條／奇玩
	_equip_schematic = VBoxContainer.new()
	_equip_schematic.name = "EquipSchematic"
	_equip_schematic.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	_equip_schematic.offset_left = -300
	_equip_schematic.offset_top = 16
	_equip_schematic.offset_right = -28
	_equip_schematic.offset_bottom = 250
	_equip_schematic.add_theme_constant_override("separation", 8)
	_village_layer.add_child(_equip_schematic)
	_refresh_equip_schematic()

	## 右側：多巴胺奶油白戰情報告板 (專注於主線推進)
	var right_card := PanelContainer.new()
	right_card.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_card.offset_left = -340
	right_card.offset_top = -170
	right_card.offset_right = -32
	right_card.offset_bottom = -16
	right_card.add_theme_stylebox_override("panel", _create_obsidian_panel(COLOR_BORDER))
	_village_layer.add_child(right_card)

	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 10)
	right_card.add_child(rv)

	var ch_lbl := Label.new()
	ch_lbl.text = "冒險出征 · 當前主線"
	ch_lbl.add_theme_font_size_override("font_size", 14)
	ch_lbl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	rv.add_child(ch_lbl)

	var s_name := Label.new()
	s_name.text = _t("第二地區 · 白霧之地 (2-4 BOSS)")
	s_name.add_theme_font_size_override("font_size", 17)
	s_name.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	rv.add_child(s_name)

	var btn_go := Button.new()
	btn_go.name = "GoCampaignButton"
	btn_go.text = "前往出征"
	UiStyle.style_button(btn_go, true)
	btn_go.custom_minimum_size = Vector2(280, 64)
	btn_go.add_theme_font_size_override("font_size", 20)
	var go_icon := "res://assets/icons/hud/icon_go_campaign.png"
	if ResourceLoader.exists(go_icon):
		btn_go.icon = load(go_icon)
		btn_go.expand_icon = true
		btn_go.add_theme_constant_override("icon_max_width", 28)
		btn_go.add_theme_constant_override("h_separation", 8)
	btn_go.pressed.connect(func(): _switch_tab(Tab.ADVENTURE))
	rv.add_child(btn_go)

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
		sb.border_width_bottom = 5
		sb.set_corner_radius_all(18)
		sb.content_margin_top = 8
		sb.content_margin_bottom = 8
		sb.content_margin_left = 14
		sb.content_margin_right = 14
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
		sb.content_margin_left = 14
		sb.content_margin_right = 14
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
	btn.set_meta("hall_title", title)
	if subtitle_or_cb is String:
		btn.set_meta("hall_subtitle", subtitle_or_cb)
	btn.custom_minimum_size = Vector2(216, 56)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	btn.text = title

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
		btn.add_theme_constant_override("h_separation", 10)
		btn.alignment = HORIZONTAL_ALIGNMENT_CENTER
	btn.add_theme_font_size_override("font_size", 18)

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
func _on_hero_clicked(forced_act: int = -1) -> void:
	_is_interacting = true
	var act_type := forced_act if forced_act >= 0 else (randi() % 3)

	if _breathe_tween and _breathe_tween.is_valid():
		_breathe_tween.kill()

	var speech_lines := [
		"看我的旋風斬～喝！",
		"背後的發條上得剛剛好，出發吧！",
		"聽見神殿齒輪的轉動聲了嗎？",
		"神殿的以太核心正在共鳴……",
		"隨時準備好去挑戰大首領！"
	]
	if _speech_label:
		_speech_label.text = speech_lines[randi() % speech_lines.size()]
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

	## 噴散 8 顆黃金以太星芒微粒
	if _hero_avatar:
		_burst_click_particles(_hero_avatar.global_position + Vector2(125, 120))

	if _poke_tween and _poke_tween.is_valid():
		_poke_tween.kill()
	var tw := create_tween()
	_poke_tween = tw
	match act_type:
		0:
			## 揮劍劈砍姿態 (attack -> recover -> equipped idle)
			if _tex_attack and _hero_avatar:
				_hero_avatar.texture = _tex_attack
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			tw.tween_property(_hero_avatar, "position", Vector2(-110, -165), 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "position", Vector2(-125, -140), 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.tween_interval(0.4)
			tw.tween_callback(func():
				if _tex_recover and _hero_avatar:
					_hero_avatar.texture = _tex_recover
					_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			)
			tw.tween_interval(0.3)
			tw.tween_callback(_restore_hero_idle)
		1:
			## 聚氣勝利姿態 (skill -> equipped idle)
			if _tex_skill and _hero_avatar:
				_hero_avatar.texture = _tex_skill
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			tw.tween_property(_hero_avatar, "scale", Vector2(1.15, 1.15), 0.15).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
			tw.tween_property(_hero_avatar, "scale", Vector2(1.0, 1.0), 0.2).set_trans(Tween.TRANS_SINE)
			tw.tween_interval(0.6)
			tw.tween_callback(_restore_hero_idle)
		2:
			## 靈巧後翻大跳躍 (telegraph -> equipped idle)
			if _tex_telegraph and _hero_avatar:
				_hero_avatar.texture = _tex_telegraph
				_hero_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			tw.tween_property(_hero_avatar, "position:y", -175.0, 0.15).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", -1.0, 0.15)
			tw.tween_property(_hero_avatar, "position:y", -140.0, 0.18).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
			tw.parallel().tween_property(_hero_avatar, "scale:x", 1.0, 0.18)
			tw.tween_interval(0.2)
			tw.tween_callback(_restore_hero_idle)

func _burst_click_particles(center_pos: Vector2) -> void:
	var gp := get_node_or_null("/root/GraphicsProfile")
	var n := 8
	if gp != null:
		n = int(gp.particle_count(8))
	if n <= 0:
		return
	var cols: Array[Color] = [
		GOLD_CLASSICAL,
		GOLD_HOVER,
		TEAL_CORE,
		BRONZE_WARM
	]
	for i in range(n):
		var star := ColorRect.new()
		star.name = "BurstParticle_%d" % i
		star.add_to_group("burst_particles")
		star.custom_minimum_size = Vector2(6, 6)
		star.size = Vector2(6, 6)
		star.pivot_offset = Vector2(3, 3)
		star.rotation = PI * 0.25
		star.color = cols[i % cols.size()]
		star.global_position = center_pos - Vector2(3, 3)
		star.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(star)

		var angle := float(i) * (PI * 2.0 / float(n))
		var dist := randf_range(40.0, 80.0)
		var target := center_pos + Vector2(cos(angle), sin(angle)) * dist

		var tw := create_tween()
		tw.tween_property(star, "global_position", target, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(star, "modulate:a", 0.0, 0.35).set_delay(0.15)
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

	var desc := Label.new()
	desc.text = _t("聚引四大共鳴核心之魂：銳齒(攻) · 固甲(防) · 旋簧(血) · 全衡(衡)。點擊點亮更高階封靈罐！")
	desc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	desc.add_theme_font_size_override("font_size", 13)
	desc.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	v.add_child(desc)

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
	btn_absorb.text = "一鍵吸收灰魂 (換經驗)"
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
		_show_toast("已將廢魂轉化為 480 戰魂經驗值！")
	)
	bot_h.add_child(btn_absorb)

	var btn_draw := Button.new()
	btn_draw.text = "聚魂十連"
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
	nl.add_theme_font_size_override("font_size", 16)
	nl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	v.add_child(nl)

	var cl := Label.new()
	cl.name = "CostLabel"
	cl.text = "金幣 %d" % int(gd["cost"])
	cl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cl.add_theme_font_size_override("font_size", 13)
	cl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	v.add_child(cl)

	btn.pressed.connect(func(): _do_gourd_draw(idx, false))
	return btn

func _refresh_gourds_ui() -> void:
	for i in range(_gourd_btns.size()):
		var b := _gourd_btns[i]
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
		_show_toast("聚魂完畢！獲得了戰魂碎片與戰魂經驗！")
	
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

	var reg_bar := HBoxContainer.new()
	reg_bar.alignment = BoxContainer.ALIGNMENT_CENTER
	reg_bar.add_theme_constant_override("separation", 16)
	v.add_child(reg_bar)

	_region_buttons.clear()
	var regions: Array[String] = [
		_t("第一地區 · 閣樓與堡壘"),
		_t("第二地區 · 白霧之地"),
		_t("第三地區 · 道場與西林"),
		_t("第四地區 · 潮岸與終境"),
	]
	for i in range(regions.size()):
		var rb := Button.new()
		rb.text = regions[i]
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

func _select_region(r: int) -> void:
	_selected_region = r
	for i in range(_region_buttons.size()):
		_style_region_button(_region_buttons[i], i == _selected_region)
	_refresh_region_stages()

func _refresh_region_stages() -> void:
	for c in _stages_container.get_children():
		c.queue_free()

	var all_stages := [
		[
			{"num": "1-1", "name": "荒路哨站 · 發條灰鼠", "type": "前哨雜魚", "cost": 1, "power": 220, "mode": "ash_rat"},
			{"num": "1-2", "name": "堡外野原 · 荒路殘兵", "type": "精英戰鬥", "cost": 1, "power": 260, "mode": "road_bandit"},
			{"num": "1-3", "name": "堡壘廣場 · 守門暗哨", "type": "精英戰鬥", "cost": 1, "power": 300, "mode": "sewer_slime"},
			{"num": "1-4", "name": "閣樓大門 · 大型殘兵", "type": "精英戰鬥", "cost": 1, "power": 340, "mode": "road_bandit"},
		],
		[
			{"num": "2-1", "name": _t("白霧外緣 · 守望關隘"), "type": "前哨雜魚", "cost": 1, "power": 380, "mode": "road_bandit"},
			{"num": "2-2", "name": "市集街道 · 潛伏暗哨", "type": "精英戰鬥", "cost": 1, "power": 420, "mode": "road_bandit"},
			{"num": "2-3", "name": "下水道口 · 腐化黏怪", "type": "精英戰鬥", "cost": 1, "power": 450, "mode": "road_bandit"},
			{"num": "2-4", "name": _t("聖獅內殿 · 狂暴守護者"), "type": "首領部位破壞", "cost": 3, "power": 520, "mode": "leo"},
		],
		[
			{"num": "3-1", "name": "白霧村外 · 霧影遊魂", "type": "前哨雜魚", "cost": 1, "power": 560, "mode": "fog_shade"},
			{"num": "3-2", "name": "霧崖小徑 · 林間風妖", "type": "精英戰鬥", "cost": 1, "power": 600, "mode": "forest_sprite"},
			{"num": "3-3", "name": "鏡廊入口 · 鏡廊殘影", "type": "精英戰鬥", "cost": 1, "power": 640, "mode": "mirror_wraith"},
			{"num": "3-4", "name": "白霧核心 · 白霧", "type": "首領部位破壞", "cost": 3, "power": 720, "mode": "fog"},
		],
		[
			{"num": "4-1", "name": "石岸潮襲 · 潮襲海盜", "type": "前哨雜魚", "cost": 1, "power": 760, "mode": "coast_raider"},
			{"num": "4-2", "name": "潮岸沉船 · 船長殘影", "type": "精英戰鬥", "cost": 1, "power": 800, "mode": "wreck_captain"},
			{"num": "4-3", "name": "疤地焰徑 · 疤地焰靈", "type": "精英戰鬥", "cost": 1, "power": 840, "mode": "scar_wisp"},
			{"num": "4-4", "name": "通天塔底 · 塔底", "type": "首領部位破壞", "cost": 3, "power": 920, "mode": "demon"},
		],
	]

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
	var c := PanelContainer.new()
	c.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	c.custom_minimum_size = Vector2(520, 145)
	var csb := StyleBoxFlat.new()
	var is_boss: bool = str(s["type"]).find("首領") >= 0
	csb.bg_color = Color("#FFF5F0") if is_boss else COLOR_CARD_WARM
	csb.border_color = Color("#D04838") if is_boss else COLOR_BORDER
	csb.set_border_width_all(2)
	csb.border_width_bottom = 6 if is_boss else 5
	csb.set_corner_radius_all(18)
	csb.content_margin_left = 18
	csb.content_margin_right = 18
	csb.content_margin_top = 16
	csb.content_margin_bottom = 16
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
	v.add_theme_constant_override("separation", 8)
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
	num_l.text = str(s["num"])
	# 字級下限：ART_DAILY_CONSTITUTION §「輔助不准再縮去塞字」；t_b8e32048 審核收尾改回 18
	num_l.add_theme_font_size_override("font_size", 18)
	num_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	num_badge.add_child(num_l)
	t_row.add_child(num_badge)

	var name_l := Label.new()
	name_l.text = str(s["name"])
	name_l.add_theme_font_size_override("font_size", 17)
	name_l.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	name_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	t_row.add_child(name_l)
	v.add_child(t_row)

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
	typ_l.text = str(s["type"])
	# 字級下限：ART_DAILY_CONSTITUTION §「輔助不准再縮去塞字」；t_b8e32048 審核收尾改回 13
	typ_l.add_theme_font_size_override("font_size", 13)
	typ_l.add_theme_color_override("font_color", Color("#A02818") if is_boss else COLOR_TEXT_DARK)
	typ_badge.add_child(typ_l)
	inf_row.add_child(typ_badge)

	var pwr_l := Label.new()
	pwr_l.text = "推薦戰力: %d" % int(s["power"])
	pwr_l.add_theme_font_size_override("font_size", 13)
	pwr_l.add_theme_color_override("font_color", COLOR_GOLD_DARK if not is_boss else Color("#A02818"))
	pwr_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	inf_row.add_child(pwr_l)

	var cost_l := Label.new()
	cost_l.text = "消耗能量: %d" % int(s["cost"])
	cost_l.add_theme_font_size_override("font_size", 13)
	cost_l.add_theme_color_override("font_color", Color("#5A5275"))
	cost_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	inf_row.add_child(cost_l)

	v.add_child(inf_row)

	var btn_battle := Button.new()
	btn_battle.custom_minimum_size = Vector2(145, 52)
	btn_battle.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	btn_battle.text = "挑戰首領" if is_boss else "出征"
	btn_battle.add_theme_font_size_override("font_size", 16)
	var bsb := StyleBoxFlat.new()
	if is_boss:
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

	btn_battle.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	btn_battle.add_theme_color_override("font_hover_color", COLOR_TEXT_DARK)
	btn_battle.add_theme_color_override("font_pressed_color", COLOR_TEXT_DARK)

	var bsb_h := bsb.duplicate() as StyleBoxFlat
	bsb_h.bg_color = Color("#FFB84D") if is_boss else Color("#FFE066")
	var bsb_p := bsb.duplicate() as StyleBoxFlat
	bsb_p.border_width_bottom = 2

	btn_battle.add_theme_stylebox_override("normal", bsb)
	btn_battle.add_theme_stylebox_override("hover", bsb_h)
	btn_battle.add_theme_stylebox_override("pressed", bsb_p)
	btn_battle.add_theme_stylebox_override("focus", bsb)
	var m: String = str(s["mode"])
	btn_battle.pressed.connect(func(): request_battle.emit(m))
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
	l_title.add_theme_font_size_override("font_size", 15)
	l_title.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	l_vbox.add_child(l_title)

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

	# 正式更衣按鈕 (手遊防誤觸標準：高度 50px，熱區 >= 50px)
	var btn_wardrobe := Button.new()
	btn_wardrobe.name = "BtnWardrobe"
	btn_wardrobe.text = _t("更衣 · 發條衣櫥")
	btn_wardrobe.custom_minimum_size = Vector2(0, 58)
	btn_wardrobe.size_flags_horizontal = Control.SIZE_EXPAND_FILL
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
	w_title.add_theme_font_size_override("font_size", 18)
	w_title.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	w_hdr.add_child(w_title)

	var w_sub := Label.new()
	w_sub.text = _t("點擊切換輪替順位 · 三段作戰序列")
	w_sub.add_theme_font_size_override("font_size", 13)
	w_sub.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	w_hdr.add_child(w_sub)

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
	_weapon_slot_hint_label.text = WEAPON_SLOTS[_selected_weapon_slot]["hint"]
	_weapon_slot_hint_label.add_theme_font_size_override("font_size", 13)
	_weapon_slot_hint_label.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	hint_p.add_child(_weapon_slot_hint_label)

	# 4. 戰鬥屬性標題列
	var s_hdr := HBoxContainer.new()
	s_hdr.add_theme_constant_override("separation", 12)
	r_v.add_child(s_hdr)

	var s_title := Label.new()
	s_title.text = _t("機體戰鬥屬性")
	s_title.add_theme_font_size_override("font_size", 18)
	s_title.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	s_hdr.add_child(s_title)

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
	_char_power_badge.text = "有效戰力 %d" % cur_pow
	_char_power_badge.add_theme_font_size_override("font_size", 13)
	_char_power_badge.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	pow_capsule.add_child(_char_power_badge)

	# 5. 獨立屬性小卡 (生命／攻擊／防禦／暴擊／怒氣)
	var stats_v := VBoxContainer.new()
	stats_v.add_theme_constant_override("separation", 10)
	stats_v.size_flags_vertical = Control.SIZE_EXPAND_FILL
	r_v.add_child(stats_v)

	var r1 := HBoxContainer.new()
	r1.add_theme_constant_override("separation", 10)
	r1.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	stats_v.add_child(r1)

	r1.add_child(_build_stat_card("生命力 (HP)", "520", "機體核心", Color("#0E8A7A")))
	r1.add_child(_build_stat_card("物理攻擊", "95", "打擊破壞", COLOR_GOLD_DARK))
	r1.add_child(_build_stat_card("物理防禦", "48", "減傷防護", Color("#2A5580")))

	var r2 := HBoxContainer.new()
	r2.add_theme_constant_override("separation", 10)
	r2.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	stats_v.add_child(r2)

	r2.add_child(_build_stat_card("暴擊率", "22%", "弱點致命", Color("#B83250")))
	r2.add_child(_build_stat_card("怒氣量表", "20 點", "滿怒超頻運轉 +25% 性能", Color("#A82B1E")))

func _build_weapon_slot_button(idx: int, slot_data: Dictionary) -> Button:
	var btn := Button.new()
	btn.name = "WeaponSlot_%d" % idx
	btn.custom_minimum_size = Vector2(0, 68)
	btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	var v := VBoxContainer.new()
	v.name = "Content"
	v.set_anchors_preset(Control.PRESET_FULL_RECT)
	v.alignment = BoxContainer.ALIGNMENT_CENTER
	v.mouse_filter = Control.MOUSE_FILTER_IGNORE
	v.add_theme_constant_override("separation", 2)
	btn.add_child(v)

	var slot_title := Label.new()
	slot_title.name = "SlotTitle"
	slot_title.text = slot_data["slot_title"]
	slot_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	slot_title.add_theme_font_size_override("font_size", 13)
	slot_title.add_theme_color_override("font_color", COLOR_GOLD_DARK)
	v.add_child(slot_title)

	var weapon_info := Label.new()
	weapon_info.name = "WeaponInfo"
	weapon_info.text = "%s · %s" % [slot_data["weapon_name"], slot_data["hits"]]
	weapon_info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	weapon_info.add_theme_font_size_override("font_size", 16)
	weapon_info.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	v.add_child(weapon_info)

	_style_weapon_slot_button(btn, idx == _selected_weapon_slot)
	var slot_idx := idx
	btn.pressed.connect(func(): _select_weapon_slot(slot_idx))
	return btn

func _style_weapon_slot_button(btn: Button, is_selected: bool) -> void:
	var sb := StyleBoxFlat.new()
	sb.set_corner_radius_all(18)
	sb.border_color = COLOR_BORDER
	sb.set_border_width_all(2)
	sb.border_width_bottom = 5
	sb.content_margin_left = 12
	sb.content_margin_right = 12
	sb.content_margin_top = 8
	sb.content_margin_bottom = 8

	var title_lbl := btn.get_node_or_null("Content/SlotTitle") as Label
	var info_lbl := btn.get_node_or_null("Content/WeaponInfo") as Label

	if is_selected:
		sb.bg_color = COLOR_ORANGE
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.22)
		sb.shadow_size = 6
		sb.shadow_offset = Vector2(0, 3)
		if title_lbl:
			title_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
		if info_lbl:
			info_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	else:
		sb.bg_color = COLOR_CARD_WARM
		sb.shadow_color = Color(0.12, 0.10, 0.23, 0.12)
		sb.shadow_size = 4
		sb.shadow_offset = Vector2(0, 2)
		if title_lbl:
			title_lbl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
		if info_lbl:
			info_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)

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

func select_weapon_slot(idx: int) -> void:
	_select_weapon_slot(idx)

func get_selected_weapon_slot() -> int:
	return _selected_weapon_slot

func get_weapon_slot_buttons() -> Array[Button]:
	return _weapon_slot_buttons

func _select_weapon_slot(idx: int) -> void:
	if idx < 0 or idx >= _weapon_slot_buttons.size():
		return
	_selected_weapon_slot = idx
	for i in range(_weapon_slot_buttons.size()):
		_style_weapon_slot_button(_weapon_slot_buttons[i], i == _selected_weapon_slot)
	if _weapon_slot_hint_label and idx < WEAPON_SLOTS.size():
		_weapon_slot_hint_label.text = WEAPON_SLOTS[idx]["hint"]

func _build_stat_card(title: String, val_str: String, subtitle: String, val_color: Color) -> PanelContainer:
	var c := PanelContainer.new()
	c.name = "StatCard"
	c.set_meta("is_stat_card", true)
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
	t_lbl.text = title
	t_lbl.add_theme_font_size_override("font_size", 14)
	t_lbl.add_theme_color_override("font_color", COLOR_TEXT_DARK)
	top_row.add_child(t_lbl)

	if not subtitle.is_empty():
		var sub_lbl := Label.new()
		sub_lbl.name = "SubLabel"
		sub_lbl.text = subtitle
		sub_lbl.add_theme_font_size_override("font_size", 12)
		sub_lbl.add_theme_color_override("font_color", COLOR_GOLD_DARK)
		top_row.add_child(sub_lbl)

	var val_row := HBoxContainer.new()
	val_row.add_theme_constant_override("separation", 6)
	v.add_child(val_row)

	var v_lbl := Label.new()
	v_lbl.name = "ValLabel"
	v_lbl.text = val_str
	v_lbl.add_theme_font_size_override("font_size", 22)
	v_lbl.add_theme_color_override("font_color", val_color)
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

	var title_lbl := Label.new()
	title_lbl.text = _t("冒險者背包")
	_apply_label_style(title_lbl, 22, COLOR_TEXT_ORANGE, COLOR_BORDER, 4)
	title_v.add_child(title_lbl)

	var sub_lbl := Label.new()
	sub_lbl.text = _t("道具與戰魂倉庫 · 點選格子查看詳情")
	_apply_label_style(sub_lbl, 16, COLOR_TEXT_DARK)
	title_v.add_child(sub_lbl)

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

	var detail_margin := MarginContainer.new()
	detail_margin.add_theme_constant_override("margin_left", 16)
	detail_margin.add_theme_constant_override("margin_right", 16)
	detail_margin.add_theme_constant_override("margin_top", 14)
	detail_margin.add_theme_constant_override("margin_bottom", 14)
	detail_panel.add_child(detail_margin)

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
	detail_margin.add_child(_bag_detail)

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

	# 操作提示
	_bag_tip = Label.new()
	_bag_tip.text = _t("點選格子查看詳情 · 雙擊或點擊按鈕使用")
	_bag_tip.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_apply_label_style(_bag_tip, 16, Color("#6B5E80"))
	right.add_child(_bag_tip)

	_refresh_bag_tab()

func _on_bag_cell_input(idx: int, ev: InputEvent) -> void:
	if not (ev is InputEventMouseButton and ev.pressed):
		return
	var button := (ev as InputEventMouseButton).button_index
	if idx < 0 or idx >= _bag_ids.size():
		return
	var id := str(_bag_ids[idx])
	if id == "":
		_selected_bag_item = ""
		_refresh_bag_tab()
		return
	if button == MOUSE_BUTTON_RIGHT:
		_selected_bag_item = id
		var inv := _get_inv_sys()
		if inv and inv.has_method("use_item"):
			inv.call("use_item", id)
		refresh_hud()
		_refresh_bag_tab()
		return
	if button == MOUSE_BUTTON_LEFT:
		var now := Time.get_ticks_msec()
		if _last_bag_click_i == idx and now - _last_bag_click_t < 350:
			_selected_bag_item = id
			var inv := _get_inv_sys()
			if inv and inv.has_method("use_item"):
				inv.call("use_item", id)
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
		inv.call("use_item", _selected_bag_item)
	refresh_hud()
	_refresh_bag_tab()

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

func _refresh_bag_tab() -> void:
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
			_selected_bag_item = str(list[0].get("id", "")) if list.size() > 0 else ""
	elif list.size() > 0:
		_selected_bag_item = str(list[0].get("id", ""))

	for i in range(_bag_cells.size()):
		var cell: PanelContainer = _bag_cells[i]
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
			if g:
				g.text = ""
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

func _update_bag_detail(inv: Node) -> void:
	if _bag_detail == null:
		return
	if _selected_bag_item == "" or inv == null:
		_bag_detail.text = "[color=#1F1A3A][b][font_size=20]冒險者背包[/font_size][/b]\n\n請點選左側格子查看道具詳情。\n\n[color=#C2600A]•[/color] 消耗品：使用回復狀態\n[color=#C2600A]•[/color] 素材：點擊使用可賣出金幣\n[color=#C2600A]•[/color] 重要物：劇情關鍵道具[/color]"
		if _bag_use_btn:
			_bag_use_btn.disabled = true
			_bag_use_btn.text = _t("使用 / 賣出")
		if _bag_hb_btn:
			_bag_hb_btn.disabled = true
		return

	if _bag_hb_btn:
		_bag_hb_btn.disabled = false

	var def: Dictionary = inv.call("catalog", _selected_bag_item) as Dictionary if inv.has_method("catalog") else {}
	var n: int = int(inv.call("count", _selected_bag_item)) if inv.has_method("count") else 0
	var kind: String = str(def.get("kind", ""))
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
				_bag_use_btn.text = _t("賣出 (+%d金)" % int(def.get("sell", 1)))
		"key":
			kind_s = _t("重要道具")
			if _bag_use_btn:
				_bag_use_btn.disabled = true
				_bag_use_btn.text = _t("無法使用")
		_:
			kind_s = _t("道具")
			if _bag_use_btn:
				_bag_use_btn.disabled = false
				_bag_use_btn.text = _t("使用 / 賣出")

	var item_name: String = str(def.get("name", _selected_bag_item))
	var item_desc: String = str(def.get("desc", ""))

	_bag_detail.text = "[color=#1F1A3A][b][font_size=20]%s[/font_size][/b]  [color=#C2600A]×%d[/color]\n\n[color=#4A3E60]%s[/color]\n\n[color=#C2600A]類型：[/color][color=#1F1A3A]%s[/color][/color]" % [
		item_name,
		n,
		item_desc,
		kind_s,
	]

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
		s += " %d分" % maxi(1, m)
	return s

func refresh_hud() -> void:
	var gs := _gs()
	var lv := 1
	var gold := 0
	var dust := 0
	var pow := 0
	if gs:
		lv = maxi(1, int(gs.level))
		gold = int(gs.gold)
		dust = int(gs.stardust)
		if gs.has_method("power_score"):
			pow = int(gs.call("power_score"))
	if _lv_label:
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
		_power_label.text = "戰力 %d" % pow
	if _char_power_badge:
		_char_power_badge.text = "有效戰力 %d" % (pow if pow > 0 else 482)
	if _energy_label:
		_energy_label.text = _energy_hud_text()
	if _gold_label:
		_gold_label.text = _fmt_int(gold)
	if _gem_label:
		_gem_label.text = _fmt_int(dust)

func _show_toast(msg: String) -> void:
	var toast := Label.new()
	toast.text = msg
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	toast.set_anchors_preset(Control.PRESET_CENTER_TOP)
	toast.offset_left = -200
	toast.offset_right = 200
	toast.offset_top = 80
	toast.offset_bottom = 126
	var tsb := StyleBoxFlat.new()
	tsb.bg_color = Color(0.043, 0.039, 0.055, 0.95)
	tsb.border_color = GOLD_CLASSICAL
	tsb.set_border_width_all(1)
	tsb.border_width_bottom = 3
	tsb.set_corner_radius_all(8)
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
func open_forge() -> Control:
	var existing = get_node_or_null("ForgeDialog")
	if existing != null:
		return existing
	var ForgeClass: GDScript = load("res://scripts/ui/forge_dialog.gd")
	if ForgeClass == null:
		push_error("無法載入 ForgeDialog")
		return null
	var dlg: Control = ForgeClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


## 開啟手藝工坊寶石彈窗
func open_gem_workshop() -> Control:
	var existing = get_node_or_null("GemWorkshopDialog")
	if existing != null:
		return existing
	var GemClass: GDScript = load("res://scripts/ui/gem_workshop_dialog.gd")
	if GemClass == null:
		push_error("無法載入 GemWorkshopDialog")
		return null
	var dlg: Control = GemClass.new() as Control
	dlg.z_index = 80
	dlg.tree_exited.connect(func():
		refresh_hud()
	)
	add_child(dlg)
	return dlg


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



