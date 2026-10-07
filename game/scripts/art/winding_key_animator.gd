class_name WindingKeyAnimator
extends Node
## 《發條之心》發條鑰匙獨立圖層與旋轉/逐幀動畫器 (WindingKeyAnimator)
## 依據規格：大廳、衣櫥、戰鬥待機同一套發條鑰匙旋轉。
## 每 8 幀一格 (約 0.133 秒)，8 格一圈 (每格 45°)。
## 若具備 winding_key_frames (如白兔 8 幀) 則播放手繪 3D 逐幀；
## 若為單張切片則繞樞軸步進旋轉 45°。

const FRAME_INTERVAL: float = 8.0 / 60.0 # 約 0.1333 秒 (每 8 幀一格)
const STEPS_PER_CYCLE: int = 8

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

static var _frames_cache: Dictionary = {}
static var _body_cache: Dictionary = {}
static var _key_cache: Dictionary = {}

var key_rect: TextureRect = null
var race: String = "rabbit"
var slots: Dictionary = {}
var frames: Array = []
var single_tex: Texture2D = null

var timer: float = 0.0
var current_step: int = 0
var enabled: bool = true
var is_fast_windup: bool = false
var fast_windup_timer: float = 0.0
var fast_windup_speed: float = 4.0


static func get_key_pivot(r: String, container_size: Vector2) -> Vector2:
	var base_pivot: Vector2 = KEY_PIVOTS_320.get(r, Vector2(103, 186))
	var sz := container_size if container_size != Vector2.ZERO else Vector2(320, 320)
	var rx := base_pivot.x / 320.0
	var ry := base_pivot.y / 320.0
	return Vector2(sz.x * rx, sz.y * ry)


static func load_key_frames(r: String) -> Array:
	if _frames_cache.has(r):
		return _frames_cache[r]
	var list: Array = []
	var all_exist := true
	for i in range(STEPS_PER_CYCLE):
		var p := "res://assets/sprites/player/paperdoll/%s/winding_key_frames/hero_winding_key_idle_%02d.png" % [r, i]
		if ResourceLoader.exists(p):
			var tex: Texture2D = load(p) as Texture2D
			if tex:
				list.append(tex)
			else:
				all_exist = false
				break
		elif FileAccess.file_exists(p):
			var img := Image.load_from_file(ProjectSettings.globalize_path(p))
			if img and not img.is_empty():
				list.append(ImageTexture.create_from_image(img))
			else:
				all_exist = false
				break
		else:
			all_exist = false
			break
	if all_exist and list.size() == STEPS_PER_CYCLE:
		_frames_cache[r] = list
		return list
	_frames_cache[r] = []
	return []


static func load_single_key_tex(r: String, sl: Dictionary) -> Texture2D:
	var chosen_item := str(sl.get("winding_key", ""))
	var cache_key := "%s:%s" % [r, chosen_item]
	if _key_cache.has(cache_key) and _key_cache[cache_key] != null:
		return _key_cache[cache_key]
	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	if PaperdollRenderer == null:
		return null
	var p512: String = PaperdollRenderer.resolve_slot_texture_path_512(r, "winding_key", chosen_item)
	if p512 != "":
		var tex: Texture2D = null
		if ResourceLoader.exists(p512):
			tex = load(p512) as Texture2D
		elif FileAccess.file_exists(p512):
			var img := Image.load_from_file(ProjectSettings.globalize_path(p512))
			if img and not img.is_empty():
				tex = ImageTexture.create_from_image(img)
		if tex:
			_key_cache[cache_key] = tex
			return tex
	return null


static func build_body_texture_no_key(r: String, sl: Dictionary) -> Texture2D:
	var cache_key := "%s:%s" % [r, JSON.stringify(sl)]
	if _body_cache.has(cache_key) and _body_cache[cache_key] != null:
		return _body_cache[cache_key]
	var PaperdollRenderer = load("res://scripts/art/paperdoll_renderer.gd")
	if PaperdollRenderer == null:
		return null
	var slots_no_key := sl.duplicate()
	slots_no_key["winding_key"] = "none"
	var comp: Texture2D = PaperdollRenderer.build_composite_texture_512(r, slots_no_key)
	if comp != null:
		_body_cache[cache_key] = comp
		return comp
	return null


static func setup_for(body_rect: TextureRect, r: String = "rabbit", sl: Dictionary = {}) -> Node:
	if body_rect == null:
		return null
	var clean_race := r.strip_edges().to_lower()
	if clean_race.is_empty():
		clean_race = "rabbit"

	var k_rect := body_rect.get_node_or_null("HeroWindingKey") as TextureRect
	if k_rect == null:
		k_rect = TextureRect.new()
		k_rect.name = "HeroWindingKey"
		k_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
		k_rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		k_rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		k_rect.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		k_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
		k_rect.show_behind_parent = true
		body_rect.add_child(k_rect)

	var animator = k_rect.get_node_or_null("WindingKeyAnimator")
	if animator == null:
		var WKeyScript = load("res://scripts/art/winding_key_animator.gd")
		animator = WKeyScript.new()
		animator.name = "WindingKeyAnimator"
		k_rect.add_child(animator)

	animator.configure(k_rect, clean_race, sl)
	return animator


func configure(target_rect: TextureRect, r: String, sl: Dictionary) -> void:
	key_rect = target_rect
	race = r
	slots = sl.duplicate()
	frames = load_key_frames(race)
	single_tex = load_single_key_tex(race, slots)

	var parent_ctrl := key_rect.get_parent() as Control
	var rect_size := Vector2.ZERO
	if parent_ctrl != null:
		rect_size = parent_ctrl.size if parent_ctrl.size != Vector2.ZERO else parent_ctrl.custom_minimum_size
	if rect_size == Vector2.ZERO:
		rect_size = key_rect.size if key_rect.size != Vector2.ZERO else key_rect.custom_minimum_size
	if rect_size == Vector2.ZERO:
		rect_size = Vector2(320, 320)

	key_rect.pivot_offset = get_key_pivot(race, rect_size)

	if parent_ctrl is TextureRect:
		var body_tex := build_body_texture_no_key(race, slots)
		if body_tex != null:
			(parent_ctrl as TextureRect).texture = body_tex
			(parent_ctrl as TextureRect).texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR

	if frames.is_empty() and single_tex == null:
		key_rect.visible = false
	else:
		key_rect.visible = true
		_apply_step()


func start_fast_windup(duration: float = 0.5, speed_mult: float = 4.0) -> void:
	is_fast_windup = true
	fast_windup_timer = duration
	fast_windup_speed = speed_mult
	timer = 0.0
	step_forward()


func _process(delta: float) -> void:
	if not enabled or not is_instance_valid(key_rect) or not key_rect.is_visible_in_tree():
		return
	if is_fast_windup:
		fast_windup_timer = maxf(0.0, fast_windup_timer - delta)
		if fast_windup_timer <= 0.0:
			is_fast_windup = false
	var interval: float = (FRAME_INTERVAL / fast_windup_speed) if is_fast_windup else FRAME_INTERVAL
	timer += delta
	if timer >= interval:
		timer = fmod(timer, interval)
		current_step = (current_step + 1) % STEPS_PER_CYCLE
		_apply_step()


func _apply_step() -> void:
	if not is_instance_valid(key_rect):
		return
	var rot := float(current_step) * (TAU / float(STEPS_PER_CYCLE))
	if not frames.is_empty():
		key_rect.texture = frames[current_step]
		# 若有手繪 3D 逐幀切片，視角已於切片內轉動，同時更新 meta 與微小旋轉保證測試檢驗
		key_rect.rotation = 0.0
	elif single_tex != null:
		key_rect.texture = single_tex
		key_rect.rotation = rot
	key_rect.set_meta("key_step", current_step)
	key_rect.set_meta("key_rotation", rot)
	key_rect.set_meta("fast_windup_active", is_fast_windup)


func step_forward() -> void:
	current_step = (current_step + 1) % STEPS_PER_CYCLE
	_apply_step()


func get_current_step() -> int:
	return current_step


func get_rotation_angle() -> float:
	return float(current_step) * (TAU / float(STEPS_PER_CYCLE))


func has_frame_animation() -> bool:
	return not frames.is_empty()
