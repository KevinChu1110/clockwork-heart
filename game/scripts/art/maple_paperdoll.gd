class_name MaplePaperdoll
extends Node2D
## 《發條之心》楓之谷 Character.wz 骨骼錨點與部件分層掛載紙娃娃
## 1. 建立角色骨骼與錨點體系（neck/navel/hand/brow/back_key）。
## 2. 眼睛、外裝、武器、發條鑰匙獨立為帶 origin 錨點的部件 Sprite，眼睛不畫死在素體上。
## 3. 動態 Z-Order 層級控制。
## 4. 具備呼吸待機動態（Body 呼吸帶動全身錨點子節點聯動、發條鑰匙自轉、眼睛週期性眨眼）。

signal part_changed(slot_name: String, item_id: String)
signal z_order_changed(slot_name: String, new_z: int)

const DEFAULT_SPEC_PATH := "res://data/tables/maple_paperdoll_rabbit.json"

## 預設錨點常數 (512 畫布基準)
const ANCHOR_ROOT_DEFAULT := Vector2(256, 480)
const ANCHOR_NECK_DEFAULT := Vector2(248, 290)
const ANCHOR_NAVEL_DEFAULT := Vector2(256, 350)
const ANCHOR_HAND_DEFAULT := Vector2(320, 440)
const ANCHOR_BACK_KEY_DEFAULT := Vector2(190, 296)
const ANCHOR_BROW_REL_NECK_DEFAULT := Vector2(2, -60)

## 預設 Z-Index 常數
const Z_WINDING_KEY_DEFAULT := 5
const Z_BACK_CURIO_DEFAULT := 8
const Z_BODY_DEFAULT := 10
const Z_HEAD_UNIT_DEFAULT := 20
const Z_COSTUME_DEFAULT := 25
const Z_EYES_DEFAULT := 30
const Z_WEAPON_DEFAULT := 40

@export var spec_path: String = DEFAULT_SPEC_PATH
@export var breathing_enabled: bool = true
@export var breathing_period: float = 2.4       ## 呼吸週期秒數
@export var breathing_amplitude: float = 2.8    ## 身體起伏像素
@export var key_rotation_speed: float = 1.8     ## 發條鑰匙自轉角速度 (rad/s)
@export var blink_enabled: bool = true

## 骨骼錨點節點引用
var node_body: Node2D = null
var node_neck: Node2D = null
var node_brow: Node2D = null
var node_navel: Node2D = null
var node_hand: Node2D = null
var node_back_key: Node2D = null
var node_tail: Node2D = null

## 各槽位 Sprite2D 節點
var sprite_body: Sprite2D = null
var sprite_head_unit: Sprite2D = null
var sprite_eyes: Sprite2D = null
var sprite_costume: Sprite2D = null
var sprite_weapon: Sprite2D = null
var sprite_winding_key: Sprite2D = null
var sprite_back_curio: Sprite2D = null

## 錨點基準位置快取
var _anchor_neck_base: Vector2 = ANCHOR_NECK_DEFAULT
var _anchor_navel_base: Vector2 = ANCHOR_NAVEL_DEFAULT
var _anchor_hand_base: Vector2 = ANCHOR_HAND_DEFAULT
var _anchor_back_key_base: Vector2 = ANCHOR_BACK_KEY_DEFAULT
var _anchor_brow_base: Vector2 = ANCHOR_BROW_REL_NECK_DEFAULT
var _anchor_tail_base: Vector2 = Vector2(360, 380)

## 規格資料快取
var _spec: Dictionary = {}
## 當前穿戴品項：{slot: item_id}
var _current_loadout: Dictionary = {}
## 各槽位 origin 快取：{slot: Vector2}
var _slot_origins: Dictionary = {}
## 各槽位目前 Z-index：{slot: int}
var _slot_z_indices: Dictionary = {}

## 呼吸動態計時
var _anim_time: float = 0.0
var _blink_timer: float = 0.0
var _is_blinking: bool = false
var _active_eye_item: String = "eyes_cyan_emerald"


func _init() -> void:
	setup()


func setup() -> void:
	if node_body != null:
		return
	load_spec(spec_path)
	_build_skeleton_hierarchy()
	_apply_default_loadout()


func _ready() -> void:
	if node_body == null:
		setup()


func _process(delta: float) -> void:
	if breathing_enabled:
		update_breathing(delta)


## 載入規格設定檔
func load_spec(path: String) -> void:
	spec_path = path
	if FileAccess.file_exists(spec_path):
		var f := FileAccess.open(spec_path, FileAccess.READ)
		if f != null:
			var parsed: Variant = JSON.parse_string(f.get_as_text())
			if parsed is Dictionary:
				_spec = parsed as Dictionary
				_apply_spec_anchors()
				if is_instance_valid(node_body):
					_apply_default_loadout()
				return
	push_warning("[MaplePaperdoll] 無法讀取規格檔 %s，使用內部預設規格" % spec_path)
	_spec = _get_builtin_default_spec()
	_apply_spec_anchors()
	if is_instance_valid(node_body):
		_apply_default_loadout()


## 套用規格定義之錨點
func _apply_spec_anchors() -> void:
	var anchors: Dictionary = _spec.get("anchors", {})
	if anchors.has("neck"):
		var a: Array = anchors["neck"]
		_anchor_neck_base = Vector2(a[0], a[1])
	else:
		_anchor_neck_base = ANCHOR_NECK_DEFAULT

	if anchors.has("navel"):
		var a: Array = anchors["navel"]
		_anchor_navel_base = Vector2(a[0], a[1])
	else:
		_anchor_navel_base = ANCHOR_NAVEL_DEFAULT

	if anchors.has("hand"):
		var a: Array = anchors["hand"]
		_anchor_hand_base = Vector2(a[0], a[1])
	else:
		_anchor_hand_base = ANCHOR_HAND_DEFAULT

	if anchors.has("back_key"):
		var a: Array = anchors["back_key"]
		_anchor_back_key_base = Vector2(a[0], a[1])
	else:
		_anchor_back_key_base = ANCHOR_BACK_KEY_DEFAULT

	if anchors.has("brow_relative_to_neck"):
		var a: Array = anchors["brow_relative_to_neck"]
		_anchor_brow_base = Vector2(a[0], a[1])
	else:
		_anchor_brow_base = ANCHOR_BROW_REL_NECK_DEFAULT

	if anchors.has("tail"):
		var a: Array = anchors["tail"]
		_anchor_tail_base = Vector2(a[0], a[1])
	else:
		_anchor_tail_base = Vector2(360, 380)

	if is_instance_valid(node_neck):
		node_neck.position = _anchor_neck_base
	if is_instance_valid(node_navel):
		node_navel.position = _anchor_navel_base
	if is_instance_valid(node_hand):
		node_hand.position = _anchor_hand_base
	if is_instance_valid(node_back_key):
		node_back_key.position = _anchor_back_key_base
	if is_instance_valid(node_brow):
		node_brow.position = _anchor_brow_base
	if is_instance_valid(node_tail):
		node_tail.position = _anchor_tail_base


## 建立角色骨骼/錨點體系（neck/navel/hand/brow/back_key/tail）
func _build_skeleton_hierarchy() -> void:
	_apply_spec_anchors()

	# 建立 Body 根節點
	if node_body == null:
		node_body = Node2D.new()
		node_body.name = "BodySlot"
		add_child(node_body)

	if sprite_body == null:
		sprite_body = Sprite2D.new()
		sprite_body.name = "BodySprite"
		sprite_body.centered = false
		sprite_body.z_as_relative = false
		sprite_body.z_index = Z_BODY_DEFAULT
		node_body.add_child(sprite_body)

	# 1. 建立 BackKey 錨點
	if node_back_key == null:
		node_back_key = Node2D.new()
		node_back_key.name = "AnchorBackKey"
		node_back_key.position = _anchor_back_key_base
		node_body.add_child(node_back_key)

	if sprite_winding_key == null:
		sprite_winding_key = Sprite2D.new()
		sprite_winding_key.name = "WindingKeySprite"
		sprite_winding_key.centered = false
		sprite_winding_key.z_as_relative = false
		sprite_winding_key.z_index = Z_WINDING_KEY_DEFAULT
		node_back_key.add_child(sprite_winding_key)

	# 2. 建立 Navel（肚臍/外裝）錨點
	if node_navel == null:
		node_navel = Node2D.new()
		node_navel.name = "AnchorNavel"
		node_navel.position = _anchor_navel_base
		node_body.add_child(node_navel)

	if sprite_costume == null:
		sprite_costume = Sprite2D.new()
		sprite_costume.name = "CostumeSprite"
		sprite_costume.centered = false
		sprite_costume.z_as_relative = false
		sprite_costume.z_index = Z_COSTUME_DEFAULT
		node_navel.add_child(sprite_costume)

	# 3. 建立 Hand（手部/武器）錨點
	if node_hand == null:
		node_hand = Node2D.new()
		node_hand.name = "AnchorHand"
		node_hand.position = _anchor_hand_base
		node_body.add_child(node_hand)

	if sprite_weapon == null:
		sprite_weapon = Sprite2D.new()
		sprite_weapon.name = "WeaponSprite"
		sprite_weapon.centered = false
		sprite_weapon.z_as_relative = false
		sprite_weapon.z_index = Z_WEAPON_DEFAULT
		node_hand.add_child(sprite_weapon)

	# 4. 建立 Neck（脖子/頭部）錨點
	if node_neck == null:
		node_neck = Node2D.new()
		node_neck.name = "AnchorNeck"
		node_neck.position = _anchor_neck_base
		node_body.add_child(node_neck)

	if sprite_head_unit == null:
		sprite_head_unit = Sprite2D.new()
		sprite_head_unit.name = "HeadUnitSprite"
		sprite_head_unit.centered = false
		sprite_head_unit.z_as_relative = false
		sprite_head_unit.z_index = Z_HEAD_UNIT_DEFAULT
		node_neck.add_child(sprite_head_unit)

	# 5. 建立 Brow（眉毛/眼睛光學核心）錨點（掛在 Neck 下）
	if node_brow == null:
		node_brow = Node2D.new()
		node_brow.name = "AnchorBrow"
		node_brow.position = _anchor_brow_base
		node_neck.add_child(node_brow)

	if sprite_eyes == null:
		sprite_eyes = Sprite2D.new()
		sprite_eyes.name = "EyesSprite"
		sprite_eyes.centered = false
		sprite_eyes.z_as_relative = false
		sprite_eyes.z_index = Z_EYES_DEFAULT
		node_brow.add_child(sprite_eyes)

	# 6. 建立 Tail（尾部/背飾）錨點（掛在 Body 下）
	if node_tail == null:
		node_tail = Node2D.new()
		node_tail.name = "AnchorTail"
		node_tail.position = _anchor_tail_base
		node_body.add_child(node_tail)

	if sprite_back_curio == null:
		sprite_back_curio = Sprite2D.new()
		sprite_back_curio.name = "BackCurioSprite"
		sprite_back_curio.centered = false
		sprite_back_curio.z_as_relative = false
		sprite_back_curio.z_index = Z_BACK_CURIO_DEFAULT
		node_tail.add_child(sprite_back_curio)

	# 初始化 Z-Index 字典
	_slot_z_indices["winding_key"] = Z_WINDING_KEY_DEFAULT
	_slot_z_indices["back_curio"] = Z_BACK_CURIO_DEFAULT
	_slot_z_indices["body"] = Z_BODY_DEFAULT
	_slot_z_indices["head_unit"] = Z_HEAD_UNIT_DEFAULT
	_slot_z_indices["costume"] = Z_COSTUME_DEFAULT
	_slot_z_indices["eyes"] = Z_EYES_DEFAULT
	_slot_z_indices["weapon"] = Z_WEAPON_DEFAULT


## 預設穿戴初始化
func _apply_default_loadout() -> void:
	if _spec.has("default_loadout"):
		var dl: Dictionary = _spec["default_loadout"]
		for slot in dl.keys():
			set_part_item(str(slot), str(dl[slot]))
	else:
		set_part_item("body", "paint_ivory_stock")
		set_part_item("head_unit", "ear_rabbit_straight")
		set_part_item("eyes", "eyes_cyan_emerald")
		set_part_item("costume", "costume_nutcracker_guard")
		set_part_item("weapon", "wpn_dawn_blade")
		set_part_item("winding_key", "key_classic_brass")


## 取得錨點節點
func get_anchor_node(anchor_name: String) -> Node2D:
	match anchor_name:
		"root": return node_body
		"neck": return node_neck
		"brow": return node_brow
		"navel": return node_navel
		"hand": return node_hand
		"back_key": return node_back_key
		"tail": return node_tail
		_: return null


## 取得槽位 Sprite2D
func get_slot_sprite(slot_name: String) -> Sprite2D:
	match slot_name:
		"body": return sprite_body
		"head_unit": return sprite_head_unit
		"eyes": return sprite_eyes
		"costume": return sprite_costume
		"weapon": return sprite_weapon
		"winding_key": return sprite_winding_key
		"back_curio": return sprite_back_curio
		_: return null


## 動態 Z-Order 層級控制
func set_part_z_index(slot_name: String, new_z: int) -> void:
	var sprite := get_slot_sprite(slot_name)
	if sprite != null:
		sprite.z_index = new_z
		_slot_z_indices[slot_name] = new_z
		z_order_changed.emit(slot_name, new_z)


func get_part_z_index(slot_name: String) -> int:
	return _slot_z_indices.get(slot_name, 0)


func get_layer_order() -> Dictionary:
	return _slot_z_indices.duplicate()


## 更換部件（獨立為帶 origin 錨點的部件 Sprite）
func set_part_item(slot_name: String, item_id: String) -> void:
	_current_loadout[slot_name] = item_id
	var sprite := get_slot_sprite(slot_name)
	if sprite == null:
		return

	if slot_name == "eyes" and item_id != "eyes_blink":
		_active_eye_item = item_id

	if item_id in ["none", "empty", "bare", ""]:
		sprite.visible = false
		sprite.texture = null
		_slot_origins[slot_name] = Vector2.ZERO
		part_changed.emit(slot_name, item_id)
		return

	var item_def := _get_item_def(slot_name, item_id)
	var tex_path: String = str(item_def.get("path", ""))
	var origin_arr: Array = item_def.get("origin", [0, 0])
	var origin := Vector2(origin_arr[0], origin_arr[1])
	_slot_origins[slot_name] = origin

	if tex_path != "" and ResourceLoader.exists(tex_path):
		var tex: Texture2D = load(tex_path)
		sprite.texture = tex
		sprite.visible = true
		# 依 origin 對齊：令 sprite 在 anchor 點處的位移為 -origin
		sprite.position = -origin
	else:
		push_warning("[MaplePaperdoll] 找不到部件貼圖：%s (slot: %s, item: %s)" % [tex_path, slot_name, item_id])
		sprite.texture = null
		sprite.visible = false

	part_changed.emit(slot_name, item_id)


func get_part_item(slot_name: String) -> String:
	return _current_loadout.get(slot_name, "")


func get_current_loadout() -> Dictionary:
	return _current_loadout.duplicate()


## 快捷部件設定方法
func set_body(item_id: String) -> void:
	set_part_item("body", item_id)

func set_head_unit(item_id: String) -> void:
	set_part_item("head_unit", item_id)

func set_eyes(item_id: String) -> void:
	set_part_item("eyes", item_id)

func set_costume(item_id: String) -> void:
	set_part_item("costume", item_id)

func set_weapon(item_id: String) -> void:
	set_part_item("weapon", item_id)

func set_winding_key(item_id: String) -> void:
	set_part_item("winding_key", item_id)

func set_back_curio(item_id: String) -> void:
	set_part_item("back_curio", item_id)


## 呼吸待機動態更新 (Breathing Idle Dynamic Motion)
## 依據楓之谷骨骼階層概念：
## 1. Body 呼吸起伏帶動所有掛在 Body 上的子錨點 (Navel, Neck, Hand, BackKey)
## 2. Head 在 Neck 上具備微幅跟隨延遲 (Secondary Follow-Through)
## 3. Eyes 在 Brow 上跟隨 Head
## 4. Winding Key 在 BackKey 錨點上平滑旋轉
## 5. 眼睛週期性眨眼 (Blink Cycle)
func update_breathing(delta: float) -> void:
	_anim_time += delta
	var phase := _anim_time * TAU / breathing_period

	# 1. Body 垂直呼吸波與微量擠壓伸展 (Squash & Stretch)
	var body_bob_y := sin(phase) * breathing_amplitude
	var body_scale_y := 1.0 + sin(phase) * 0.008
	var body_scale_x := 1.0 - sin(phase) * 0.004

	if is_instance_valid(node_body):
		node_body.position.y = body_bob_y
		node_body.scale = Vector2(body_scale_x, body_scale_y)

	# 2. Neck 處頭部的微幅次級慣性旋轉與俯仰
	if is_instance_valid(node_neck):
		var neck_lag_phase := phase - 0.25
		node_neck.position = _anchor_neck_base + Vector2(0, sin(neck_lag_phase) * 0.8)
		node_neck.rotation = sin(neck_lag_phase) * 0.015

	# 3. Hand 處武器的微幅持握呼吸律動
	if is_instance_valid(node_hand):
		var hand_lag_phase := phase - 0.15
		node_hand.position = _anchor_hand_base + Vector2(0, sin(hand_lag_phase) * 0.5)

	# 4. 發條鑰匙自轉
	if is_instance_valid(node_back_key):
		# 以鑰匙插入點為支點旋轉/擺動
		node_back_key.rotation += key_rotation_speed * delta

	# 5. 眼睛自然眨眼動畫
	if blink_enabled:
		_blink_timer += delta
		if not _is_blinking:
			if _blink_timer >= 3.2:
				_is_blinking = true
				_blink_timer = 0.0
				set_part_item("eyes", "eyes_blink")
		else:
			if _blink_timer >= 0.14:
				_is_blinking = false
				_blink_timer = 0.0
				set_part_item("eyes", _active_eye_item)


## 從快取規格中取得部件定義
func _get_item_def(slot_name: String, item_id: String) -> Dictionary:
	var parts: Dictionary = _spec.get("parts", {})
	var slot_def: Dictionary = parts.get(slot_name, {})
	var items: Dictionary = slot_def.get("items", {})
	return items.get(item_id, {})


## 取得內部備援預設規格
func _get_builtin_default_spec() -> Dictionary:
	return {
		"race": "rabbit",
		"canvas_size": [512, 512],
		"root_anchor": [256, 480],
		"anchors": {
			"neck": [248, 290],
			"navel": [256, 350],
			"hand": [320, 440],
			"back_key": [190, 296],
			"brow_relative_to_neck": [2, -60]
		},
		"parts": {}
	}


## 產生無頭 512x512 RGBA8 記憶體合成 Image（依 Z-Order 完整疊合）
## 可用於 Headless 測試斷言、實機截圖與無邊框檢驗
func get_composite_image(canvas_width: int = 512, canvas_height: int = 512) -> Image:
	var base_img := Image.create(canvas_width, canvas_height, false, Image.FORMAT_RGBA8)
	base_img.fill(Color(0, 0, 0, 0))

	# 蒐集所有當前可見的 Sprite2D 與其世界變換
	var entries: Array[Dictionary] = []
	var slots := ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]

	for sid in slots:
		var sprite := get_slot_sprite(sid)
		if sprite != null and sprite.visible and sprite.texture != null:
			var tex_img: Image = sprite.texture.get_image()
			if tex_img != null and not tex_img.is_empty():
				entries.append({
					"slot": sid,
					"z_index": sprite.z_index,
					"sprite": sprite,
					"img": tex_img
				})

	# 依 Z-Index 由小到大排序 (ASCENDING)
	entries.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return int(a["z_index"]) < int(b["z_index"])
	)

	for entry in entries:
		var sprite: Sprite2D = entry["sprite"]
		var layer_img: Image = entry["img"]
		if layer_img.get_format() != Image.FORMAT_RGBA8:
			layer_img.convert(Image.FORMAT_RGBA8)

		# 計算 Sprite 在 MaplePaperdoll 座標系中的原點位置 (對齊 anchor - origin)
		var g_pos: Vector2 = sprite.global_position - global_position
		var dest_x := int(round(g_pos.x))
		var dest_y := int(round(g_pos.y))
		var rot: float = sprite.global_rotation - global_rotation

		if abs(rot) < 0.001:
			# 無旋轉：直接使用高效 blend_rect
			var src_w := layer_img.get_width()
			var src_h := layer_img.get_height()
			var src_rect := Rect2i(0, 0, src_w, src_h)
			base_img.blend_rect(layer_img, src_rect, Vector2i(dest_x, dest_y))
		else:
			# 有微幅旋轉（例如發條鑰匙或頭部呼吸傾斜）：進行像素採樣疊合
			_blend_rotated_layer(base_img, layer_img, sprite)

	return base_img


## 支援旋轉的圖層混色
func _blend_rotated_layer(target: Image, src: Image, sprite: Sprite2D) -> void:
	var sw := src.get_width()
	var sh := src.get_height()
	var xform: Transform2D = global_transform.affine_inverse() * sprite.global_transform
	var inv_xform := xform.affine_inverse()

	var tw := target.get_width()
	var th := target.get_height()

	# 計算 AABB 範圍以加速像素混色
	var p0 := xform * Vector2(0, 0)
	var p1 := xform * Vector2(sw, 0)
	var p2 := xform * Vector2(sw, sh)
	var p3 := xform * Vector2(0, sh)
	var min_x := int(clamp(floor(min(min(p0.x, p1.x), min(p2.x, p3.x))), 0, tw - 1))
	var max_x := int(clamp(ceil(max(max(p0.x, p1.x), max(p2.x, p3.x))), 0, tw - 1))
	var min_y := int(clamp(floor(min(min(p0.y, p1.y), min(p2.y, p3.y))), 0, th - 1))
	var max_y := int(clamp(ceil(max(max(p0.y, p1.y), max(p2.y, p3.y))), 0, th - 1))

	for y in range(min_y, max_y + 1):
		for x in range(min_x, max_x + 1):
			var src_pt := inv_xform * Vector2(x, y)
			var sx := int(floor(src_pt.x))
			var sy := int(floor(src_pt.y))
			if sx >= 0 and sx < sw and sy >= 0 and sy < sh:
				var c_src := src.get_pixel(sx, sy)
				if c_src.a > 0.01:
					var c_dst := target.get_pixel(x, y)
					# 標準 Alpha 混合
					var out_a := c_src.a + c_dst.a * (1.0 - c_src.a)
					if out_a > 0.001:
						var out_r := (c_src.r * c_src.a + c_dst.r * c_dst.a * (1.0 - c_src.a)) / out_a
						var out_g := (c_src.g * c_src.a + c_dst.g * c_dst.a * (1.0 - c_src.a)) / out_a
						var out_b := (c_src.b * c_src.a + c_dst.b * c_dst.a * (1.0 - c_src.a)) / out_a
						target.set_pixel(x, y, Color(out_r, out_g, out_b, out_a))


## 儲存合成圖為 PNG 檔案
func save_composite_png(output_path: String) -> Error:
	var img := get_composite_image()
	if img == null or img.is_empty():
		return ERR_CANT_CREATE
	var dir_path := output_path.get_base_dir()
	if dir_path != "" and not DirAccess.dir_exists_absolute(dir_path):
		DirAccess.make_dir_recursive_absolute(dir_path)
	return img.save_png(output_path)
