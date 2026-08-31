extends CharacterBody2D
## 俯視探索玩家：點擊只改導航目標，移動只在 _physics_process + move_and_slide。

signal arrived
signal interacted(id: String)

const SPEED := 240.0
const FRICTION := 1800.0
const INTERACT_DIST := 64.0

var frozen: bool = false
var pending_interact_id: String = ""

@onready var nav: NavigationAgent2D = $NavigationAgent2D
@onready var body: Sprite2D = $Visuals/Body


func _ready() -> void:
	motion_mode = MOTION_MODE_FLOATING
	floor_block_on_wall = false
	nav.path_desired_distance = 8.0
	nav.target_desired_distance = 16.0
	nav.radius = 12.0
	nav.avoidance_enabled = false
	_apply_idle_tex()
	nav.navigation_finished.connect(_on_nav_finished)


func _apply_idle_tex() -> void:
	var tex: Texture2D = SpriteDB.player_idle()
	if tex and body:
		body.texture = tex
		body.centered = true
		body.offset = Vector2(0, -tex.get_height() * 0.5 + 8.0)
		body.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST


func _physics_process(delta: float) -> void:
	if frozen:
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		move_and_slide()
		return
	if nav.is_navigation_finished():
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		move_and_slide()
		return
	var next_pos: Vector2 = nav.get_next_path_position()
	var to_next: Vector2 = next_pos - global_position
	if to_next.length() < 2.0:
		move_and_slide()
		return
	velocity = to_next.normalized() * SPEED
	move_and_slide()
	if body and absf(velocity.x) > 8.0:
		body.flip_h = velocity.x < 0.0


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


func play_action_pose(_pose: String, _duration: float = 0.4) -> void:
	pass
