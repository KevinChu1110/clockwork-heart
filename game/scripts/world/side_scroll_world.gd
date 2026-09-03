class_name SideScrollWorld
extends Control
## 純 2D 橫向卷軸手遊探索系統 (MapleStory / Tata Style Side-Scrolling Exploration)
## 特色：3 層橫向視差插畫卷軸 + 2.2 頭身大主角橫向跑跳 + 萌系動物夥伴 NPC + 純手機觸控 UI

signal exit_to_lobby()
signal start_battle(mode: String)

const UiStyle = preload("res://scripts/ui/ui_style.gd")
const ContentLoc = preload("res://scripts/systems/content_loc.gd")

## 世界寬度與地面 Y
const WORLD_WIDTH := 2800.0
const GROUND_Y := 530.0
const MOVE_SPEED := 240.0
const JUMP_FORCE := -420.0
const GRAVITY := 980.0

## 攝影機與捲動
var _camera_x: float = 0.0
var _target_camera_x: float = 0.0

## 視差圖層節點
var _far_bg: TextureRect
var _mid_bg: TextureRect
var _ground_root: Control
var _actors_root: Control

## 玩家節點
var _player: Control
var _player_avatar: TextureRect
var _player_shadow: TextureRect
var _player_pos := Vector2(260, GROUND_Y)
var _player_vel := Vector2.ZERO
var _player_dir: int = 1
var _is_on_ground: bool = true
var _anim_timer: float = 0.0
var _walk_frame: int = 0

## NPC 節點列表
var _npcs: Array[Dictionary] = []
var _active_npc: Dictionary = {}

## 手機觸控控制項
var _move_input: float = 0.0
var _btn_left: Button
var _btn_right: Button
var _btn_jump: Button
var _btn_interact: Button

## 對話視窗
var _dialog_card: PanelContainer
var _dialog_npc_name: Label
var _dialog_text: RichTextLabel
var _dialog_options_box: HBoxContainer
var _dialog_portrait: TextureRect

## 頂部資源列
var _top_bar: PanelContainer
var _lv_label: Label
var _power_label: Label
var _energy_label: Label
var _gold_label: Label
var _gem_label: Label

## 奔跑動畫幀紋理快取
var _walk_texs: Array[Texture2D] = []
var _idle_tex: Texture2D

func _ready() -> void:
	custom_minimum_size = Vector2(1280, 720)
	size = Vector2(1280, 720)
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_load_textures()
	_build_world_layers()
	_spawn_npcs()
	_spawn_player()
	_build_mobile_controls()
	_build_top_hud()
	_build_dialog_box()

func _load_textures() -> void:
	if ResourceLoader.exists("res://assets/sprites/player/poses/idle.png"):
		_idle_tex = load("res://assets/sprites/player/poses/idle.png")
	elif ResourceLoader.exists("res://assets/sprites/player/rabbit_idle.png"):
		_idle_tex = load("res://assets/sprites/player/rabbit_idle.png")

	_walk_texs.clear()
	for i in range(4):
		var p := "res://assets/sprites/player/rabbit_walk_%d.png" % i
		if ResourceLoader.exists(p):
			_walk_texs.append(load(p))

func _build_world_layers() -> void:
	## 1. 遠景天空層 (平滑天藍微雲)
	_far_bg = TextureRect.new()
	_far_bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	_far_bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_far_bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_far_bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/illustrations/title_bg.png"):
		_far_bg.texture = load("res://assets/sprites/illustrations/title_bg.png")
	_far_bg.modulate = Color(0.85, 0.90, 1.0, 0.6)
	add_child(_far_bg)

	## 2. 中景王都城堡插畫 (寬 3200px 橫向大畫卷)
	_mid_bg = TextureRect.new()
	_mid_bg.custom_minimum_size = Vector2(3200, 720)
	_mid_bg.size = Vector2(3200, 720)
	_mid_bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_mid_bg.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	_mid_bg.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if ResourceLoader.exists("res://assets/sprites/maps/town_bg.webp"):
		_mid_bg.texture = load("res://assets/sprites/maps/town_bg.webp")
	add_child(_mid_bg)

	## 3. 地面石板與街道裝飾層
	_ground_root = Control.new()
	_ground_root.custom_minimum_size = Vector2(WORLD_WIDTH, 720)
	_ground_root.size = Vector2(WORLD_WIDTH, 720)
	add_child(_ground_root)

	## 綠意花草與石板路基底
	var road_strip := ColorRect.new()
	road_strip.position = Vector2(0, GROUND_Y)
	road_strip.size = Vector2(WORLD_WIDTH, 190)
	road_strip.color = Color(0.24, 0.20, 0.16, 0.88)
	_ground_root.add_child(road_strip)

	var grass_edge := ColorRect.new()
	grass_edge.position = Vector2(0, GROUND_Y - 4)
	grass_edge.size = Vector2(WORLD_WIDTH, 6)
	grass_edge.color = Color(0.48, 0.72, 0.32, 1.0) # 亮綠邊緣
	_ground_root.add_child(grass_edge)

	## 4. 實體與角色層 (支援 Y-Sort 概念)
	_actors_root = Control.new()
	_actors_root.custom_minimum_size = Vector2(WORLD_WIDTH, 720)
	_actors_root.size = Vector2(WORLD_WIDTH, 720)
	add_child(_actors_root)

## ──────────────────────────────────────────
## 萌系 2.2 頭身夥伴 NPC 配置
## ──────────────────────────────────────────
func _spawn_npcs() -> void:
	_npcs.clear()
	var npc_defs := [
		{
			"id": "hamster_forge",
			"name": "咚咚",
			"title": "小倉鼠工匠",
			"icon": "🐹",
			"x": 480.0,
			"bubble": "今天要鍛造神兵嗎！",
			"lines": ["叮叮噹！我的小金鎚隨時準備為你強化裝備喵！", "只要收集到足夠的星之碎片，就能覺醒更強的威力喔～"],
			"color": Color(0.95, 0.80, 0.40)
		},
		{
			"id": "rabbit_bud",
			"name": "小芽",
			"title": "見習冒險兔",
			"icon": "🐰",
			"x": 920.0,
			"bubble": "外面的世界好廣闊喔～",
			"lines": ["小白隊長！聽說城外的巨木森林出現了好多發光的小精靈！", "我也要努力修行，成為保護大家的傳說勇者！"],
			"color": Color(0.95, 0.88, 0.85)
		},
		{
			"id": "owl_tutor",
			"name": "星羽",
			"title": "雪鴞星讀導師",
			"icon": "🦉",
			"x": 1420.0,
			"bubble": "十四主星之魂正在共鳴...",
			"lines": ["星軌流轉，帝星顯現。聚魂殿的星盤今日格外明亮。", "與戰魂締結契約，將賜予你撕裂黑暗的光明之力。"],
			"color": Color(0.65, 0.75, 1.0)
		},
		{
			"id": "squirrel_merchant",
			"name": "栗子",
			"title": "元氣松鼠商人",
			"icon": "🐿️",
			"x": 1920.0,
			"bubble": "剛進了超甜的橡實補給！",
			"lines": ["歡迎光臨栗子小舖！有最棒的紅藥水和稀有琥珀結晶～", "出發前一定要把背包裝得滿滿的，冒險才安心嘛！"],
			"color": Color(0.92, 0.65, 0.35)
		},
		{
			"id": "gate_portal",
			"name": "王國之門",
			"title": "出征傳送祭壇",
			"icon": "⚔️",
			"x": 2420.0,
			"bubble": "通往世界各地關卡",
			"lines": ["這裡連接著聖獅城外圍的各個戰役與裂縫！準備好展開冒險了嗎？"],
			"color": Color(1.0, 0.85, 0.35)
		}
	]

	for d in npc_defs:
		var npc_node := _create_npc_visual(d)
		_actors_root.add_child(npc_node)
		d["node"] = npc_node
		_npcs.append(d)

func _create_npc_visual(data: Dictionary) -> Control:
	var c := Control.new()
	c.position = Vector2(float(data["x"]), GROUND_Y - 4)
	c.custom_minimum_size = Vector2(100, 140)

	## 腳底軟陰影
	var shadow := TextureRect.new()
	shadow.position = Vector2(-35, -12)
	shadow.size = Vector2(70, 24)
	var grad := Gradient.new()
	grad.set_color(0, Color(0, 0, 0, 0.4))
	grad.set_color(1, Color(0, 0, 0, 0.0))
	var gtex := GradientTexture2D.new()
	gtex.gradient = grad
	gtex.fill = GradientTexture2D.FILL_RADIAL
	gtex.fill_from = Vector2(0.5, 0.5)
	gtex.fill_to = Vector2(0.5, 0.0)
	shadow.texture = gtex
	shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.add_child(shadow)

	## NPC 可愛頭像/立體卡片標籤
	var body_box := PanelContainer.new()
	body_box.position = Vector2(-45, -100)
	body_box.custom_minimum_size = Vector2(90, 90)
	var bsb := StyleBoxFlat.new()
	bsb.bg_color = Color(0.14, 0.11, 0.09, 0.92)
	bsb.border_color = data["color"] as Color
	bsb.set_border_width_all(2)
	bsb.set_corner_radius_all(18)
	bsb.shadow_color = Color(0, 0, 0, 0.35)
	bsb.shadow_size = 6
	body_box.add_theme_stylebox_override("panel", bsb)
	c.add_child(body_box)

	var icon_l := Label.new()
	icon_l.text = str(data["icon"])
	icon_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	icon_l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	icon_l.add_theme_font_size_override("font_size", 42)
	body_box.add_child(icon_l)

	## 頭頂頭銜與名字
	var name_box := VBoxContainer.new()
	name_box.position = Vector2(-70, -145)
	name_box.custom_minimum_size = Vector2(140, 40)
	name_box.alignment = BoxContainer.ALIGNMENT_CENTER
	name_box.add_theme_constant_override("separation", 2)
	c.add_child(name_box)

	var title_l := Label.new()
	title_l.text = "【%s】" % str(data["title"])
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 11)
	title_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	title_l.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	title_l.add_theme_constant_override("outline_size", 2)
	name_box.add_child(title_l)

	var name_l := Label.new()
	name_l.text = str(data["name"])
	name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_l.add_theme_font_size_override("font_size", 14)
	name_l.add_theme_color_override("font_color", Color.WHITE)
	name_l.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	name_l.add_theme_constant_override("outline_size", 3)
	name_box.add_child(name_l)

	## 萌系果凍說話泡泡 (靠近時彈出)
	var bubble := PanelContainer.new()
	bubble.name = "Bubble"
	bubble.position = Vector2(-75, -195)
	bubble.custom_minimum_size = Vector2(150, 42)
	var bub_sb := StyleBoxFlat.new()
	bub_sb.bg_color = Color(1.0, 0.98, 0.92, 0.98)
	bub_sb.border_color = Color(0.24, 0.18, 0.12, 1.0)
	bub_sb.set_border_width_all(2)
	bub_sb.set_corner_radius_all(12)
	bub_sb.shadow_color = Color(0, 0, 0, 0.25)
	bub_sb.shadow_size = 4
	bub_sb.content_margin_left = 8
	bub_sb.content_margin_right = 8
	bub_sb.content_margin_top = 4
	bub_sb.content_margin_bottom = 4
	bubble.add_theme_stylebox_override("panel", bub_sb)
	bubble.visible = false
	c.add_child(bubble)

	var bl := Label.new()
	bl.text = "💬 " + str(data["bubble"])
	bl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	bl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	bl.add_theme_font_size_override("font_size", 12)
	bl.add_theme_color_override("font_color", Color(0.18, 0.12, 0.08))
	bubble.add_child(bl)

	return c

## ──────────────────────────────────────────
## 主角生成 (2.2 頭身白兔展示)
## ──────────────────────────────────────────
func _spawn_player() -> void:
	_player = Control.new()
	_player.custom_minimum_size = Vector2(120, 140)
	_player.position = _player_pos
	_actors_root.add_child(_player)

	## 腳底投影
	_player_shadow = TextureRect.new()
	_player_shadow.position = Vector2(-40, -14)
	_player_shadow.size = Vector2(80, 28)
	var grad := Gradient.new()
	grad.set_color(0, Color(0, 0, 0, 0.55))
	grad.set_color(1, Color(0, 0, 0, 0.0))
	var gtex := GradientTexture2D.new()
	gtex.gradient = grad
	gtex.fill = GradientTexture2D.FILL_RADIAL
	gtex.fill_from = Vector2(0.5, 0.5)
	gtex.fill_to = Vector2(0.5, 0.0)
	_player_shadow.texture = gtex
	_player_shadow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_player.add_child(_player_shadow)

	## 2.2 頭身大主角展示 (高 130px，清晰看清領巾與神態)
	_player_avatar = TextureRect.new()
	_player_avatar.position = Vector2(-60, -125)
	_player_avatar.size = Vector2(120, 130)
	_player_avatar.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_player_avatar.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_player_avatar.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_player_avatar.pivot_offset = Vector2(60, 125)
	if _idle_tex:
		_player_avatar.texture = _idle_tex
	_player.add_child(_player_avatar)

	## 玩家頭頂稱號與暱稱
	var tag_v := VBoxContainer.new()
	tag_v.position = Vector2(-75, -170)
	tag_v.custom_minimum_size = Vector2(150, 40)
	tag_v.alignment = BoxContainer.ALIGNMENT_CENTER
	tag_v.add_theme_constant_override("separation", 2)
	_player.add_child(tag_v)

	var title_l := Label.new()
	title_l.text = "【初出茅廬】"
	title_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title_l.add_theme_font_size_override("font_size", 11)
	title_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	title_l.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	title_l.add_theme_constant_override("outline_size", 2)
	tag_v.add_child(title_l)

	var name_l := Label.new()
	name_l.text = "Capoo"
	name_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name_l.add_theme_font_size_override("font_size", 15)
	name_l.add_theme_color_override("font_color", Color.WHITE)
	name_l.add_theme_color_override("font_outline_color", Color(0.18, 0.12, 0.08))
	name_l.add_theme_constant_override("outline_size", 3)
	tag_v.add_child(name_l)

## ──────────────────────────────────────────
## 每幀移動與橫向視差推軌 (60 FPS Smooth Dolly)
## ──────────────────────────────────────────
func _process(delta: float) -> void:
	## 1. 玩家水平移動
	var move_x := _move_input
	if Input.is_action_pressed("ui_left"): move_x = -1.0
	elif Input.is_action_pressed("ui_right"): move_x = 1.0

	if move_x != 0.0:
		_player_dir = 1 if move_x > 0 else -1
		_player_avatar.flip_h = (_player_dir < 0)
		_player_pos.x += move_x * MOVE_SPEED * delta
		_player_pos.x = clampf(_player_pos.x, 60.0, WORLD_WIDTH - 60.0)

		## 奔跑序列幀切換
		_anim_timer += delta
		if _anim_timer > 0.12:
			_anim_timer = 0.0
			_walk_frame = (_walk_frame + 1) % 4
			if _walk_frame < _walk_texs.size() and _walk_texs[_walk_frame]:
				_player_avatar.texture = _walk_texs[_walk_frame]
	else:
		_anim_timer = 0.0
		if _idle_tex:
			_player_avatar.texture = _idle_tex
		## 閒置輕微呼吸
		var breathe := sin(Time.get_ticks_msec() * 0.005) * 0.02
		_player_avatar.scale = Vector2(1.0 + breathe, 1.0 - breathe)

	## 2. 玩家跳躍物理
	if not _is_on_ground:
		_player_vel.y += GRAVITY * delta
		_player_pos.y += _player_vel.y * delta
		if _player_pos.y >= GROUND_Y:
			_player_pos.y = GROUND_Y
			_player_vel.y = 0.0
			_is_on_ground = true

	_player.position = _player_pos

	## 3. 鏡頭橫向追蹤平滑推軌 (Horizontal Camera Dolly)
	_target_camera_x = _player_pos.x - 640.0
	_target_camera_x = clampf(_target_camera_x, 0.0, WORLD_WIDTH - 1280.0)
	_camera_x = lerpf(_camera_x, _target_camera_x, 10.0 * delta)

	## 更新視差層位移
	_far_bg.position.x = -_camera_x * 0.15
	_mid_bg.position.x = -_camera_x * 0.55
	_ground_root.position.x = -_camera_x
	_actors_root.position.x = -_camera_x

	## 4. NPC 靠近偵測
	_check_npc_proximity()

func _check_npc_proximity() -> void:
	var closest_dist := 9999.0
	var found_npc: Dictionary = {}
	for d in _npcs:
		var n_x: float = float(d["x"])
		var dist := absf(_player_pos.x - n_x)
		var bubble: Control = (d["node"] as Control).get_node_or_null("Bubble")
		if dist < 120.0:
			if bubble: bubble.visible = true
			if dist < closest_dist:
				closest_dist = dist
				found_npc = d
		else:
			if bubble: bubble.visible = false

	_active_npc = found_npc
	if _btn_interact:
		_btn_interact.visible = not _active_npc.is_empty()
		if not _active_npc.is_empty():
			_btn_interact.text = "💬 談話"

## ──────────────────────────────────────────
## 純手機觸控控制列 (Touch Controls)
## ──────────────────────────────────────────
func _build_mobile_controls() -> void:
	## 1. 左下角：左右橫向大移動按鈕 (大拇指舒適觸控)
	var left_box := HBoxContainer.new()
	left_box.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	left_box.offset_left = 32
	left_box.offset_bottom = -28
	left_box.add_theme_constant_override("separation", 18)
	add_child(left_box)

	_btn_left = _make_control_btn("◀", Vector2(76, 68), func(pressed):
		_move_input = -1.0 if pressed else 0.0
	)
	left_box.add_child(_btn_left)

	_btn_right = _make_control_btn("▶", Vector2(76, 68), func(pressed):
		_move_input = 1.0 if pressed else 0.0
	)
	left_box.add_child(_btn_right)

	## 2. 右下角：跳躍與互動圓形按鈕
	var right_box := HBoxContainer.new()
	right_box.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	right_box.offset_right = -32
	right_box.offset_bottom = -28
	right_box.add_theme_constant_override("separation", 20)
	add_child(right_box)

	_btn_interact = Button.new()
	_btn_interact.text = "💬 談話"
	_btn_interact.custom_minimum_size = Vector2(96, 68)
	_btn_interact.add_theme_font_size_override("font_size", 16)
	var isb := StyleBoxFlat.new()
	isb.bg_color = Color(0.92, 0.76, 0.28, 1.0)
	isb.border_color = Color(1.0, 0.95, 0.65, 1.0)
	isb.set_border_width_all(2)
	isb.set_corner_radius_all(20)
	isb.shadow_color = Color(0.92, 0.76, 0.28, 0.5)
	isb.shadow_size = 8
	_btn_interact.add_theme_stylebox_override("normal", isb)
	_btn_interact.add_theme_stylebox_override("hover", isb)
	_btn_interact.add_theme_color_override("font_color", Color(0.18, 0.12, 0.05))
	_btn_interact.visible = false
	_btn_interact.pressed.connect(_on_interact_pressed)
	right_box.add_child(_btn_interact)

	_btn_jump = Button.new()
	_btn_jump.text = "🦘 跳躍"
	_btn_jump.custom_minimum_size = Vector2(88, 68)
	_btn_jump.add_theme_font_size_override("font_size", 16)
	var jsb := StyleBoxFlat.new()
	jsb.bg_color = Color(0.18, 0.14, 0.10, 0.92)
	jsb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	jsb.set_border_width_all(2)
	jsb.set_corner_radius_all(20)
	jsb.shadow_color = Color(0, 0, 0, 0.35)
	jsb.shadow_size = 6
	_btn_jump.add_theme_stylebox_override("normal", jsb)
	_btn_jump.add_theme_stylebox_override("hover", jsb)
	_btn_jump.add_theme_color_override("font_color", Color(1.0, 0.90, 0.75))
	_btn_jump.pressed.connect(_do_jump)
	right_box.add_child(_btn_jump)

	## 3. 右上角：區域地標膠囊與回大廳按鈕
	var top_right_box := HBoxContainer.new()
	top_right_box.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	top_right_box.offset_left = -340
	top_right_box.offset_top = 76
	top_right_box.offset_right = -16
	top_right_box.alignment = BoxContainer.ALIGNMENT_END
	top_right_box.add_theme_constant_override("separation", 10)
	add_child(top_right_box)

	var loc_tag := PanelContainer.new()
	var lsb := StyleBoxFlat.new()
	lsb.bg_color = Color(0.10, 0.08, 0.06, 0.88)
	lsb.border_color = Color(0.85, 0.70, 0.35, 0.9)
	lsb.set_border_width_all(1)
	lsb.set_corner_radius_all(14)
	lsb.content_margin_left = 12
	lsb.content_margin_right = 12
	lsb.content_margin_top = 4
	lsb.content_margin_bottom = 4
	loc_tag.add_theme_stylebox_override("panel", lsb)
	var loc_l := Label.new()
	loc_l.text = "🏰 聖獅王城 · 冒險者大街"
	loc_l.add_theme_font_size_override("font_size", 13)
	loc_l.add_theme_color_override("font_color", Color(1.0, 0.88, 0.50))
	loc_tag.add_child(loc_l)
	top_right_box.add_child(loc_tag)

	var hub_btn := Button.new()
	hub_btn.text = "🏛️ 回大廳"
	hub_btn.custom_minimum_size = Vector2(80, 32)
	hub_btn.add_theme_font_size_override("font_size", 12)
	UiStyle.style_button(hub_btn, false)
	hub_btn.pressed.connect(func(): exit_to_lobby.emit())
	top_right_box.add_child(hub_btn)

func _make_control_btn(label_txt: String, min_sz: Vector2, cb: Callable) -> Button:
	var b := Button.new()
	b.text = label_txt
	b.custom_minimum_size = min_sz
	b.add_theme_font_size_override("font_size", 22)
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.14, 0.11, 0.09, 0.85)
	csb.border_color = Color(0.85, 0.70, 0.35, 0.9)
	csb.set_border_width_all(2)
	csb.set_corner_radius_all(18)
	csb.shadow_color = Color(0, 0, 0, 0.35)
	csb.shadow_size = 6
	b.add_theme_stylebox_override("normal", csb)
	b.add_theme_stylebox_override("hover", csb)
	b.add_theme_color_override("font_color", Color(1.0, 0.90, 0.75))

	b.button_down.connect(func(): cb.call(true))
	b.button_up.connect(func(): cb.call(false))
	return b

func _do_jump() -> void:
	if _is_on_ground:
		_is_on_ground = false
		_player_vel.y = JUMP_FORCE

func _on_interact_pressed() -> void:
	if _active_npc.is_empty():
		return
	var id: String = str(_active_npc.get("id", ""))
	if id == "gate_portal":
		start_battle.emit("road_bandit")
		return

	_show_npc_dialog(_active_npc)

## ──────────────────────────────────────────
## 手機萌系對話卡片視窗
## ──────────────────────────────────────────
func _build_dialog_box() -> void:
	_dialog_card = PanelContainer.new()
	_dialog_card.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	_dialog_card.offset_left = 60
	_dialog_card.offset_right = -60
	_dialog_card.offset_top = -180
	_dialog_card.offset_bottom = -20
	_dialog_card.add_theme_stylebox_override("panel", UiStyle.panel_style())
	_dialog_card.visible = false
	add_child(_dialog_card)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 20)
	_dialog_card.add_child(h)

	## 左側 NPC 大頭肖像
	_dialog_portrait = TextureRect.new()
	_dialog_portrait.custom_minimum_size = Vector2(100, 100)
	_dialog_portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_dialog_portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	h.add_child(_dialog_portrait)

	var v := VBoxContainer.new()
	v.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	v.add_theme_constant_override("separation", 6)
	h.add_child(v)

	_dialog_npc_name = Label.new()
	_dialog_npc_name.text = "NPC"
	_dialog_npc_name.add_theme_font_size_override("font_size", 16)
	_dialog_npc_name.add_theme_color_override("font_color", Color(1.0, 0.88, 0.45))
	v.add_child(_dialog_npc_name)

	_dialog_text = RichTextLabel.new()
	_dialog_text.bbcode_enabled = true
	_dialog_text.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_dialog_text.add_theme_font_size_override("normal_font_size", 14)
	_dialog_text.add_theme_color_override("default_color", Color(0.95, 0.92, 0.88))
	v.add_child(_dialog_text)

	_dialog_options_box = HBoxContainer.new()
	_dialog_options_box.alignment = BoxContainer.ALIGNMENT_END
	_dialog_options_box.add_theme_constant_override("separation", 12)
	v.add_child(_dialog_options_box)

func _show_npc_dialog(npc: Dictionary) -> void:
	_dialog_card.visible = true
	_dialog_npc_name.text = "【%s】 %s" % [npc["title"], npc["name"]]
	var lines: Array = npc.get("lines", [])
	var line_txt: String = str(lines[randi() % lines.size()]) if not lines.is_empty() else "你好冒險者！"
	_dialog_text.text = line_txt

	for child in _dialog_options_box.get_children():
		child.queue_free()

	var ok_btn := Button.new()
	ok_btn.text = "✨ 了解"
	ok_btn.custom_minimum_size = Vector2(100, 36)
	UiStyle.style_button(ok_btn, true)
	ok_btn.pressed.connect(func(): _dialog_card.visible = false)
	_dialog_options_box.add_child(ok_btn)

## ──────────────────────────────────────────
## 頂部手遊資源條 (與 Lobby 一致)
## ──────────────────────────────────────────
func _build_top_hud() -> void:
	_top_bar = PanelContainer.new()
	_top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	_top_bar.offset_left = 16
	_top_bar.offset_right = -16
	_top_bar.offset_top = 10
	_top_bar.offset_bottom = 66
	
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.12, 0.09, 0.07, 0.90)
	sb.border_color = Color(0.85, 0.70, 0.35, 1.0)
	sb.set_border_width_all(2)
	sb.set_corner_radius_all(14)
	sb.shadow_color = Color(0, 0, 0, 0.35)
	sb.shadow_size = 6
	sb.content_margin_left = 14
	sb.content_margin_right = 14
	sb.content_margin_top = 4
	sb.content_margin_bottom = 4
	_top_bar.add_theme_stylebox_override("panel", sb)
	add_child(_top_bar)

	var hbox := HBoxContainer.new()
	hbox.add_theme_constant_override("separation", 16)
	_top_bar.add_child(hbox)

	var name_box := HBoxContainer.new()
	name_box.add_theme_constant_override("separation", 6)
	var lv_l := Label.new()
	lv_l.text = "Lv.12"
	lv_l.add_theme_color_override("font_color", Color(1.0, 0.82, 0.25))
	lv_l.add_theme_font_size_override("font_size", 14)
	name_box.add_child(lv_l)

	var n_l := Label.new()
	n_l.text = "Capoo"
	n_l.add_theme_font_size_override("font_size", 15)
	n_l.add_theme_color_override("font_color", Color.WHITE)
	name_box.add_child(n_l)
	hbox.add_child(name_box)

	var p_l := Label.new()
	p_l.text = "⚔️ 482"
	p_l.add_theme_font_size_override("font_size", 13)
	p_l.add_theme_color_override("font_color", Color(1.0, 0.75, 0.25))
	hbox.add_child(p_l)

	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hbox.add_child(spacer)

	_add_hud_item(hbox, "⚡", "15/15", Color(0.3, 0.85, 0.45))
	_add_hud_item(hbox, "🪙", "12,500", Color(1.0, 0.85, 0.3))
	_add_hud_item(hbox, "💎", "350", Color(0.45, 0.75, 1.0))

func _add_hud_item(parent: Container, sym: String, val: String, col: Color) -> void:
	var cap := PanelContainer.new()
	var csb := StyleBoxFlat.new()
	csb.bg_color = Color(0.08, 0.06, 0.05, 0.90)
	csb.border_color = Color(0.55, 0.45, 0.30, 0.9)
	csb.set_border_width_all(1)
	csb.set_corner_radius_all(14)
	csb.content_margin_left = 8
	csb.content_margin_right = 8
	csb.content_margin_top = 2
	csb.content_margin_bottom = 2
	cap.add_theme_stylebox_override("panel", csb)

	var h := HBoxContainer.new()
	h.add_theme_constant_override("separation", 6)
	var icon_l := Label.new()
	icon_l.text = sym
	icon_l.add_theme_font_size_override("font_size", 14)
	h.add_child(icon_l)
	var val_l := Label.new()
	val_l.text = val
	val_l.add_theme_font_size_override("font_size", 13)
	val_l.add_theme_color_override("font_color", Color(0.96, 0.95, 0.92))
	h.add_child(val_l)
	cap.add_child(h)
	parent.add_child(cap)
