extends Control
## 原生探索宿主（C）：CharacterBody2D + NavigationAgent2D。
## 白名單見 NATIVE_MAPS（村・騎士堡・四舖）；其餘 map_id 仍走 ExploreView。

signal interacted(id: String)
signal hint_changed(text: String)

const WalkMask := preload("res://scripts/world/walk_mask.gd")
const MapCatalog = preload("res://scripts/world/map_catalog.gd")
const MapSceneRegistry = preload("res://scripts/world/map_scene_registry.gd")
const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const PlayerScn := preload("res://scenes/actors/player.tscn")
const UiStyle = preload("res://scripts/ui/ui_style.gd")

const NATIVE_MAPS: PackedStringArray = [
	"village", "town", "town_forge", "town_soul", "town_gem", "town_tutor",
]
const DESIGN_VIEW := Vector2(1280, 720)

var map_id: String = ""
var frozen: bool = false
var player_pos: Vector2 = Vector2.ZERO

var _stage: Node2D
var _player: CharacterBody2D
var _camera: Camera2D
var _subvp: SubViewport
var _vp_box: SubViewportContainer
var _hint: Label
var _bubble: Label
var _catalog: Dictionary = {}
var _pending_interact: String = ""
var _extra_entities: Array = []
var _guide_hint: String = ""
var _near_id: String = ""
var _entity_sprites: Dictionary = {}
var _nameplates: Dictionary = {}
var _plates_layer: Control


static func is_native(p_map_id: String) -> bool:
	return p_map_id in NATIVE_MAPS


func _t(s: String) -> String:
	return ContentLoc.text("ui", s)


func setup(p_map_id: String) -> void:
	map_id = p_map_id
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	_catalog = MapCatalog.build(p_map_id)
	_build_view()
	if not resized.is_connected(_on_host_resized):
		resized.connect(_on_host_resized)
	_spawn_level()
	_spawn_entities()
	_spawn_player()
	_install_navigation()
	if map_id.begins_with("town"):
		_guide_hint = _t("點人說話 · 點店進去")
	else:
		_guide_hint = _t("點人說話 · 點路標出門")
	if _hint:
		_hint.text = _guide_hint
	hint_changed.emit(_guide_hint)


func _build_view() -> void:
	_nameplates.clear()
	_entity_sprites.clear()
	for c in get_children():
		c.queue_free()
	_vp_box = SubViewportContainer.new()
	_vp_box.set_anchors_preset(Control.PRESET_FULL_RECT)
	_vp_box.stretch = true
	_vp_box.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	_vp_box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_vp_box)
	_subvp = SubViewport.new()
	_subvp.disable_3d = true
	_subvp.handle_input_locally = false
	_subvp.physics_object_picking = true
	_subvp.world_2d = World2D.new()
	_subvp.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_LINEAR
	_subvp.size = Vector2i(int(DESIGN_VIEW.x), int(DESIGN_VIEW.y))
	_vp_box.add_child(_subvp)
	## 操作提示：跟 ExploreView 同一張深木提示框。原本是頂端一行沒底的淡字，
	## 壓在城牆／石板上根本讀不出「點人說話 · 點店進去」。
	var hint_bar := PanelContainer.new()
	hint_bar.set_anchors_preset(Control.PRESET_CENTER_TOP)
	hint_bar.grow_horizontal = Control.GROW_DIRECTION_BOTH
	hint_bar.offset_top = 10
	hint_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	hint_bar.add_theme_stylebox_override("panel", UiStyle.hint_bar_style())
	add_child(hint_bar)
	_hint = Label.new()
	_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_hint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_hint.add_theme_font_size_override("font_size", 13)
	_hint.add_theme_color_override("font_color", UiStyle.CAPTION)
	hint_bar.add_child(_hint)
	_plates_layer = Control.new()
	_plates_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
	_plates_layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_plates_layer)
	_bubble = Label.new()
	_bubble.visible = false
	_bubble.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_bubble.add_theme_font_size_override("font_size", 15)
	_bubble.add_theme_color_override("font_color", UiStyle.CAPTION)
	_bubble.add_theme_color_override("font_outline_color", UiStyle.QUEST_PING_OUTLINE)
	_bubble.add_theme_constant_override("outline_size", 4)
	_bubble.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	add_child(_bubble)


func _entity_foot(e: Dictionary) -> Vector2:
	var pos: Vector2 = e.get("pos", Vector2.ZERO)
	var sz: Vector2 = e.get("size", Vector2(48, 48))
	return pos + Vector2(sz.x * 0.5, sz.y)


func _all_entities() -> Array:
	var out: Array = []
	out.append_array(_catalog.get("entities", []))
	out.append_array(_extra_entities)
	return out


func _spawn_entities() -> void:
	if _stage == null:
		return
	var actors: Node = _stage.get_node_or_null("Actors")
	var markers: Node = _stage.get_node_or_null("Markers")
	for e in _all_entities():
		var id := str(e.get("id", ""))
		if id == "" or id == "Spawn":
			continue
		var foot := _entity_foot(e)
		if markers and markers.get_node_or_null(id) == null:
			var mk := Marker2D.new()
			mk.name = id
			mk.position = foot
			markers.add_child(mk)
		## 底圖已畫過的景物只留熱區；黃箭頭／黃條也不再疊上去。
		var skip_sprite := (SpriteDB.is_scenery_prop(id) and id.find("fire") < 0) \
			or SpriteDB.is_arrow_marker(id)
		if not skip_sprite and not (_entity_sprites.has(id) and is_instance_valid(_entity_sprites[id])):
			var tex: Texture2D = SpriteDB.explore_entity_tex(id)
			if tex == null and e.has("art_boss"):
				tex = SpriteDB.boss(str(e.get("art_boss", "")))
			if tex != null and actors != null:
				var spr := Sprite2D.new()
				spr.name = "ent_%s" % id
				spr.texture = tex
				spr.centered = true
				spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
				spr.offset = Vector2(0, -tex.get_height() * 0.5 + 8.0)
				spr.position = foot
				spr.z_index = 1
				actors.add_child(spr)
				_entity_sprites[id] = spr
		_ensure_nameplate(id, e)


func _spawn_level() -> void:
	var path := MapSceneRegistry.scene_path(map_id)
	if path == "" or not ResourceLoader.exists(path):
		push_error("ExploreHost: 沒有場景 %s" % map_id)
		return
	_stage = (load(path) as PackedScene).instantiate()
	_subvp.add_child(_stage)
	var actors := _stage.get_node_or_null("Actors")
	if actors == null:
		actors = Node2D.new()
		actors.name = "Actors"
		actors.y_sort_enabled = true
		_stage.add_child(actors)


func _spawn_player() -> void:
	var actors: Node = _stage.get_node_or_null("Actors")
	_player = PlayerScn.instantiate()
	actors.add_child(_player)
	var spawn := marker_position("Spawn")
	if spawn == Vector2.ZERO:
		spawn = _catalog.get("spawn", Vector2(200, 400)) as Vector2
	_player.global_position = spawn
	player_pos = spawn
	_player.arrived.connect(_on_player_arrived)
	_player.interacted.connect(func(id: String): interacted.emit(id))
	_camera = Camera2D.new()
	_camera.name = "Camera2D"
	_camera.position_smoothing_enabled = false
	_camera.ignore_rotation = true
	## 據點鏡頭掛在地圖上，不跟人跑——整張村當一屏點選。
	_stage.add_child(_camera)
	_camera.enabled = true
	call_deferred("_activate_camera")


func _on_host_resized() -> void:
	_fit_camera_zoom()


func _activate_camera() -> void:
	if _camera == null or not _camera.is_inside_tree():
		return
	_camera.make_current()
	_fit_camera_zoom()


func _fit_camera_zoom() -> void:
	if _camera == null or _subvp == null:
		return
	var origin: Vector2 = _catalog.get("origin", Vector2(40, 80))
	var msize: Vector2 = _catalog.get("size", Vector2(1600, 900))
	var vs := Vector2(_subvp.size)
	if vs.x < 64.0 or vs.y < 64.0:
		vs = DESIGN_VIEW
	## 據點鏡頭 0.4 → 0.6 跟人走，角色佔比接近參考
	var z := 0.6
	_camera.zoom = Vector2(z, z)
	if _player:
		_camera.global_position = _player.global_position
	else:
		_camera.global_position = origin + msize * 0.5
	_camera.limit_left = int(origin.x)
	_camera.limit_top = int(origin.y)
	_camera.limit_right = int(origin.x + msize.x)
	_camera.limit_bottom = int(origin.y + msize.y)


func _install_navigation() -> void:
	if _stage == null:
		return
	var region: NavigationRegion2D = _stage.get_node_or_null("Navigation") as NavigationRegion2D
	if region == null:
		region = NavigationRegion2D.new()
		region.name = "Navigation"
		_stage.add_child(region)
	var origin: Vector2 = _catalog.get("origin", Vector2(40, 80))
	var msize: Vector2 = _catalog.get("size", Vector2(1600, 900))
	var art := str(_catalog.get("art", map_id))
	var np: NavigationPolygon = WalkMask.build_navigation_polygon(art, origin, msize)
	if np.vertices.is_empty():
		## 沒有 walkmask 時給一塊能走的矩形，避免人釘死
		var fallback := NavigationPolygon.new()
		var rect := PackedVector2Array([
			origin + Vector2(40, 40),
			origin + Vector2(msize.x - 40, 40),
			origin + Vector2(msize.x - 40, msize.y - 40),
			origin + Vector2(40, msize.y - 40),
		])
		fallback.vertices = rect
		fallback.add_polygon(PackedInt32Array([0, 1, 2, 3]))
		np = fallback
	region.navigation_polygon = np


func marker_position(id: String) -> Vector2:
	if _stage == null:
		return Vector2.ZERO
	var markers := _stage.get_node_or_null("Markers")
	if markers == null:
		return Vector2.ZERO
	var node := markers.get_node_or_null(id)
	if node == null:
		node = markers.get_node_or_null(id.capitalize())
	if node is Node2D:
		return (node as Node2D).global_position
	return Vector2.ZERO


func tap_world(world_pos: Vector2) -> void:
	_pending_interact = ""
	_spawn_tap_fx(world_pos)
	if _player and _player.has_method("go_to"):
		_player.call("go_to", world_pos)
		_player.pending_interact_id = ""


func tap_entity(id: String) -> void:
	## 原作據點：點人／點出口就互動，不繞路。
	_pending_interact = ""
	if _player:
		_player.pending_interact_id = ""
	for e in _all_entities():
		if str(e.get("id", "")) == id:
			_spawn_tap_fx(_entity_foot(e))
			break
	interacted.emit(id)


## 點地光圈：ExploreView 早就有，原生宿主一直沒有——點下去人要半秒後才起步，
## 沒有落點記號的話玩家會以為沒點到再點一次。畫在場景 Actors 之上、跟鏡頭縮放。
static var _ring_tex_cache: Texture2D = null


static func _ring_tex() -> Texture2D:
	if _ring_tex_cache != null:
		return _ring_tex_cache
	var s := 48
	var img := Image.create(s, s, false, Image.FORMAT_RGBA8)
	var c := (s - 1) * 0.5
	for y in s:
		for x in s:
			var d := Vector2(x - c, y - c).length() / c
			var a := clampf(1.0 - absf(d - 0.78) / 0.17, 0.0, 1.0)
			a = a * a * (3.0 - 2.0 * a)
			img.set_pixel(x, y, Color(1, 1, 1, a))
	_ring_tex_cache = ImageTexture.create_from_image(img)
	return _ring_tex_cache


func _spawn_tap_fx(world: Vector2) -> void:
	if _stage == null or not is_inside_tree():
		return
	var fx := Sprite2D.new()
	fx.texture = _ring_tex()
	fx.centered = true
	fx.position = world
	fx.scale = Vector2(0.35, 0.35)
	fx.modulate = UiStyle.TAP_RING
	fx.z_index = 50
	_stage.add_child(fx)
	var tw := fx.create_tween()
	tw.set_parallel(true)
	tw.tween_property(fx, "scale", Vector2(0.95, 0.95), 0.32).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.tween_property(fx, "modulate:a", 0.0, 0.34)
	tw.chain().tween_callback(fx.queue_free)


func _on_player_arrived() -> void:
	player_pos = _player.global_position if _player else player_pos
	var iid := _pending_interact
	_pending_interact = ""
	if iid != "" and _player and _player.pending_interact_id == "":
		## 玩家腳本已 emit；這裡只清宿主狀態
		pass


func _gui_input(event: InputEvent) -> void:
	if frozen:
		return
	if event is InputEventMouseButton:
		var mb := event as InputEventMouseButton
		if not mb.pressed or mb.button_index != MOUSE_BUTTON_LEFT:
			return
		var world := _screen_to_world(mb.position)
		var hit := _hit_entity_id(world)
		if hit != "":
			tap_entity(hit)
		else:
			tap_world(world)
		accept_event()


func _screen_to_world(local_pos: Vector2) -> Vector2:
	if _camera == null:
		return local_pos
	var vp_size := Vector2(_subvp.size) if _subvp else size
	var center := _camera.get_screen_center_position()
	var zoom := _camera.zoom
	return center + (local_pos - vp_size * 0.5) / zoom


func _hit_entity_id(world: Vector2) -> String:
	var markers := _stage.get_node_or_null("Markers") if _stage else null
	if markers:
		for c in markers.get_children():
			if c is Marker2D and str(c.name) != "Spawn":
				if world.distance_to((c as Marker2D).global_position) <= 72.0:
					return str(c.name).to_lower()
	for e in _all_entities():
		var r := Rect2(e.get("pos", Vector2.ZERO), e.get("size", Vector2(48, 48)))
		r = r.grow(20.0)
		if r.has_point(world):
			return str(e.get("id", ""))
	return ""


func set_frozen(v: bool) -> void:
	frozen = v
	if _player:
		_player.frozen = v
		if v:
			_player.pending_interact_id = ""
			_pending_interact = ""


func show_guide_hint(text: String) -> void:
	_guide_hint = text
	if _hint and _near_id == "":
		_hint.text = text


func play_action_pose(pose: String, duration: float = 0.4) -> void:
	if _player and _player.has_method("play_action_pose"):
		_player.call("play_action_pose", pose, duration)


func entity_label(id: String) -> String:
	for e in _all_entities():
		if str(e.get("id", "")) == id:
			return str(e.get("label", id))
	return id


func show_player_bubble(text: String, dur: float = 2.0) -> void:
	if _bubble == null:
		return
	_bubble.text = text
	_bubble.visible = true
	_bubble.modulate.a = 1.0
	var tw := create_tween()
	tw.tween_interval(dur)
	tw.tween_property(_bubble, "modulate:a", 0.0, 0.25)
	tw.tween_callback(func():
		if _bubble:
			_bubble.visible = false
	)


func add_entities(ents: Array) -> void:
	for e in ents:
		_extra_entities.append(e)
	_spawn_entities()


func remove_entity(id: String) -> void:
	var keep: Array = []
	for e in _extra_entities:
		if str(e.get("id", "")) != id:
			keep.append(e)
	_extra_entities = keep
	var spr: Node = _entity_sprites.get(id)
	if spr and is_instance_valid(spr):
		spr.queue_free()
	_entity_sprites.erase(id)
	var plate: Dictionary = _nameplates.get(id, {})
	for k in plate:
		var n: Node = plate[k]
		if n and is_instance_valid(n):
			n.queue_free()
	_nameplates.erase(id)


func has_entity_sprite(id: String) -> bool:
	return _entity_sprites.has(id) and is_instance_valid(_entity_sprites[id])


func has_nameplate(id: String) -> bool:
	return _nameplates.has(id)


func get_player() -> CharacterBody2D:
	return _player


func get_nav_agent() -> NavigationAgent2D:
	if _player:
		return _player.get_node_or_null("NavigationAgent2D") as NavigationAgent2D
	return null


func _process(_delta: float) -> void:
	if _player:
		player_pos = _player.global_position
		if _camera:
			_camera.global_position = _player.global_position
	_update_near()
	_sync_nameplates()
	if _bubble and _bubble.visible and _player:
		## 跟 ExploreView 一樣掛在玩家頭上（「撿到東西了！」是他說的），
		## 不再釘在畫面頂端——那裡現在是操作提示框，兩行字會疊在一起。
		var head_h := 96.0
		var body: Node = _player.get_node_or_null("Visuals/Body")
		if body is Sprite2D and (body as Sprite2D).texture:
			head_h = float((body as Sprite2D).texture.get_height()) - 8.0
		var head := _player.global_position + Vector2(0, -head_h - 6.0)
		var hs := _world_to_host(head)
		_bubble.size = Vector2(240, 28)
		var bp := hs - Vector2(120.0, 28.0)
		if size.x > 8.0 and size.y > 8.0:
			bp.x = clampf(bp.x, PLATE_SIDE_PAD, maxf(PLATE_SIDE_PAD, size.x - 240.0 - PLATE_SIDE_PAD))
			bp.y = clampf(bp.y, 56.0, maxf(56.0, size.y - PLATE_BOTTOM_RESERVE - 28.0))
		_bubble.position = bp


func _ensure_nameplate(id: String, e: Dictionary) -> void:
	if _plates_layer == null:
		return
	if not SpriteDB.is_map_named(id):
		return
	if _nameplates.has(id):
		return
	## 同名去重：村口木牌「往東」與出口「往東」貼在一起，只留一張牌。
	var label := str(e.get("label", id))
	for other in _nameplates:
		var oe: Dictionary = _nameplates[other].get("ent", {})
		if str(oe.get("label", other)) == label \
			and _entity_foot(oe).distance_to(_entity_foot(e)) < 160.0:
			return
	var chip := PanelContainer.new()
	chip.mouse_filter = Control.MOUSE_FILTER_IGNORE
	chip.add_theme_stylebox_override("panel", UiStyle.interact_name_style())
	var lab := Label.new()
	lab.text = label
	lab.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lab.add_theme_font_size_override("font_size", 13)
	lab.add_theme_color_override("font_color", UiStyle.KEY_SOFT)
	lab.mouse_filter = Control.MOUSE_FILTER_IGNORE
	chip.add_child(lab)
	_plates_layer.add_child(chip)
	var bang: Label = null
	if SpriteDB.is_quest_ping(id):
		bang = Label.new()
		bang.text = "！"
		bang.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		bang.add_theme_font_size_override("font_size", 20)
		bang.add_theme_color_override("font_color", UiStyle.QUEST_PING)
		bang.add_theme_color_override("font_outline_color", UiStyle.QUEST_PING_OUTLINE)
		bang.add_theme_constant_override("outline_size", 5)
		bang.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_plates_layer.add_child(bang)
	_nameplates[id] = {"chip": chip, "bang": bang, "ent": e}


func _world_to_host(world: Vector2) -> Vector2:
	if _camera == null or _subvp == null:
		return world
	var xform := _camera.get_canvas_transform()
	var vp_pt := xform * world
	var vs := Vector2(_subvp.size)
	if vs.x < 1.0 or vs.y < 1.0 or size.x < 1.0 or size.y < 1.0:
		return vp_pt
	return Vector2(vp_pt.x * size.x / vs.x, vp_pt.y * size.y / vs.y)


## 名牌不准被快捷欄蓋掉。四舖的「回廣場」出口貼在底圖最下緣，牌子掛在腳下 6px
## 剛好落進快捷欄後面——玩家進了鐵匠鋪找不到怎麼出去。底邊留這麼多給快捷欄，
## 牌子會掉進去就翻到腳上方；左右也夾在畫面內。
const PLATE_BOTTOM_RESERVE := 44.0
const PLATE_SIDE_PAD := 6.0


func _sync_nameplates() -> void:
	if _plates_layer == null:
		return
	var host_w := size.x
	var host_h := size.y
	for id in _nameplates:
		var pack: Dictionary = _nameplates[id]
		var e: Dictionary = pack.get("ent", {})
		var foot := _entity_foot(e)
		var spr: Node = _entity_sprites.get(id)
		if spr is Node2D:
			foot = (spr as Node2D).global_position
		var screen := _world_to_host(foot)
		var chip: Control = pack.get("chip")
		if chip and is_instance_valid(chip):
			chip.reset_size()
			var p := screen - Vector2(chip.size.x * 0.5, -6.0)
			if host_w > 8.0 and host_h > 8.0:
				if p.y + chip.size.y > host_h - PLATE_BOTTOM_RESERVE:
					p.y = screen.y - chip.size.y - 8.0
				p.x = clampf(p.x, PLATE_SIDE_PAD, maxf(PLATE_SIDE_PAD, host_w - chip.size.x - PLATE_SIDE_PAD))
				p.y = clampf(p.y, PLATE_SIDE_PAD, maxf(PLATE_SIDE_PAD, host_h - PLATE_BOTTOM_RESERVE - chip.size.y))
			chip.position = p
		var bang: Control = pack.get("bang")
		if bang and is_instance_valid(bang):
			var head := foot
			if spr is Sprite2D and (spr as Sprite2D).texture:
				var th := float((spr as Sprite2D).texture.get_height())
				head = foot + Vector2(0, -th + 12.0)
			var hs := _world_to_host(head)
			bang.reset_size()
			bang.position = hs - Vector2(bang.size.x * 0.5, bang.size.y + 2.0)


func _update_near() -> void:
	if _player == null:
		return
	var best := ""
	var best_d := 64.0
	var pc: Vector2 = _player.global_position
	for e in _all_entities():
		var d := pc.distance_to(_entity_foot(e))
		if d < best_d:
			best_d = d
			best = str(e.get("id", ""))
	if best == _near_id:
		return
	_near_id = best
	if _hint == null:
		return
	if best == "":
		_hint.text = _guide_hint if _guide_hint != "" else _t("點地上走過去 · 點人或物互動")
	else:
		_hint.text = _t("點一下 · %s") % entity_label(best)
	hint_changed.emit(_hint.text)
