extends CharacterBody2D
## 俯視探索玩家：點擊只改導航目標，移動只在 _physics_process + move_and_slide。

signal arrived
signal interacted(id: String)

const SPEED := 240.0
const FRICTION := 1800.0
const INTERACT_DIST := 64.0
## 走路循環：4 格、8 FPS（與舊 ExploreView 一致）。格數不夠拉 FPS 只是快轉，
## 流暢靠格間連續性；rabbit_walk_0–3 是同尺寸同錨的一組，首尾能接。
const WALK_FPS := 8.0
const WALK_FRAMES := 4

var frozen: bool = false
var pending_interact_id: String = ""
## 測試哨兵：走路期間實際切過幾次走路幀（0 = 兔子在滑行）
var walk_frames_played: int = 0

var _walk_t: float = 0.0
var _last_walk_frame: int = -1
var _moving: bool = false
var _facing_left: bool = false
var _action_pose: String = ""
var _action_pose_left: float = 0.0
var _action_tween: Tween

@onready var nav: NavigationAgent2D = $NavigationAgent2D
@onready var body: Sprite2D = $Visuals/Body


const OutlineShader = preload("res://shaders/outline.gdshader")

static var _shadow_tex_cache: Texture2D = null

static func _get_soft_shadow_tex() -> Texture2D:
	if _shadow_tex_cache != null:
		return _shadow_tex_cache
	var img := Image.create(64, 24, false, Image.FORMAT_RGBA8)
	var cx := 32.0
	var cy := 12.0
	var rx := 28.0
	var ry := 10.0
	for y in range(24):
		for x in range(64):
			var dx := (float(x) - cx) / rx
			var dy := (float(y) - cy) / ry
			var d := sqrt(dx * dx + dy * dy)
			if d <= 1.0:
				var a := clampf(pow(1.0 - d, 0.8) * 0.50, 0.0, 0.50)
				img.set_pixel(x, y, Color(0.12, 0.08, 0.14, a))
			else:
				img.set_pixel(x, y, Color(0, 0, 0, 0))
	_shadow_tex_cache = ImageTexture.create_from_image(img)
	return _shadow_tex_cache


func _ready() -> void:
	motion_mode = MOTION_MODE_FLOATING
	floor_block_on_wall = false
	nav.path_desired_distance = 8.0
	nav.target_desired_distance = 16.0
	nav.radius = 12.0
	nav.avoidance_enabled = false
	if body:
		body.centered = true
		body.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		body.scale = Vector2.ONE
		var mat := ShaderMaterial.new()
		mat.shader = OutlineShader
		body.material = mat
	var vis := get_node_or_null("Visuals")
	if vis:
		var shadow := vis.get_node_or_null("Shadow") as Sprite2D
		if shadow == null:
			shadow = Sprite2D.new()
			shadow.name = "Shadow"
			shadow.texture = _get_soft_shadow_tex()
			shadow.centered = true
			shadow.position = Vector2(0, 4)
			shadow.scale = Vector2.ONE
			shadow.z_index = -1
			vis.add_child(shadow)
			vis.move_child(shadow, 0)
	_update_visual()
	nav.navigation_finished.connect(_on_nav_finished)


func _set_body_tex(tex: Texture2D) -> void:
	if tex == null or body == null:
		return
	if body.texture != tex:
		body.texture = tex
	## 錨點固定在腳底：每格同高，offset 只跟貼圖高度走，不會上下抖
	body.offset = Vector2(0, -tex.get_height() * 0.5 + 8.0)


func _update_visual() -> void:
	if body == null:
		return
	var tex: Texture2D = null
	if _action_pose != "":
		tex = SpriteDB.player_pose(_action_pose)
	elif _moving:
		var frame := int(_walk_t) % WALK_FRAMES
		if frame != _last_walk_frame:
			_last_walk_frame = frame
			walk_frames_played += 1
		tex = SpriteDB.player_walk(frame)
	else:
		_last_walk_frame = -1
		tex = SpriteDB.player_idle()
	if tex == null:
		tex = SpriteDB.player_idle()
	_set_body_tex(tex)
	body.flip_h = _facing_left
	## 受擊短暫偏紅，其餘維持防具染色
	if _action_pose == "hit":
		body.modulate = SpriteDB.player_armor_modulate() * Color(1.15, 0.75, 0.75, 1)
	else:
		body.modulate = SpriteDB.player_armor_modulate()


func _physics_process(delta: float) -> void:
	if _action_pose_left > 0.0:
		_action_pose_left -= delta
		if _action_pose_left <= 0.0:
			_action_pose = ""
	var was_moving := _moving
	if frozen or nav.is_navigation_finished():
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		move_and_slide()
		_moving = false
	else:
		var next_pos: Vector2 = nav.get_next_path_position()
		var to_next: Vector2 = next_pos - global_position
		if to_next.length() < 2.0:
			move_and_slide()
			_moving = false
		else:
			velocity = to_next.normalized() * SPEED
			move_and_slide()
			_moving = true
			if velocity.x < -8.0:
				_facing_left = true
			elif velocity.x > 8.0:
				_facing_left = false
	if _moving:
		_walk_t += delta * WALK_FPS
		AudioManager.play_step()
	elif was_moving:
		_walk_t = 0.0
	_update_visual()


func go_to(world_pos: Vector2) -> void:
	call_deferred("_set_target", world_pos)


func _set_target(world_pos: Vector2) -> void:
	if not is_inside_tree():
		return
	nav.target_position = world_pos


func _on_nav_finished() -> void:
	arrived.emit()
	var iid := pending_interact_id
	pending_interact_id = ""
	if iid != "":
		interacted.emit(iid)


## 與戰鬥一致的 chibi 姿態（短暫覆蓋 walk／idle），含 punch 感
func play_action_pose(pose: String, duration: float = 0.4) -> void:
	if pose == "" or pose == "idle":
		_action_pose = ""
		_action_pose_left = 0.0
		_update_visual()
		return
	_action_pose = pose
	_action_pose_left = maxf(0.12, duration)
	if body == null:
		return
	if _action_tween and _action_tween.is_valid():
		_action_tween.kill()
	match pose:
		"attack", "skill":
			body.scale = Vector2(1.1, 0.94)
		"hit":
			body.scale = Vector2(0.92, 1.06)
		"telegraph":
			body.scale = Vector2(0.97, 1.05)
		_:
			body.scale = Vector2.ONE
	_action_tween = create_tween()
	_action_tween.tween_property(body, "scale", Vector2.ONE, 0.14)
	_update_visual()
