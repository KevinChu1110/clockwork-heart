extends SceneTree
## 原生探索（C）哨兵：godot --headless -s res://scripts/world/test_explore_native.gd
## 走遊戲會用的 ExploreHost + Player + village.tscn，不重寫移動迴圈。


const HOST_PATH := "res://scripts/world/explore_host.gd"
const MAISUI := "maisui"

var _ok := true
var _step := 0
var _wait := 0
var _host: Control = null
var _start: Vector2 = Vector2.ZERO
var _dest: Vector2 = Vector2.ZERO
var _got_id: String = ""
var _physics_left := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL ", msg)
	_ok = false


func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var Host = load(HOST_PATH)
	if Host == null:
		_fail("載不到 ExploreHost")
		return _finish()
	_host = Host.new()
	root.add_child(_host)
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.setup("village")
	if _host.has_signal("interacted"):
		_host.interacted.connect(func(id: String): _got_id = id)


func _process(_d: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 24:
				return false
			if _host == null or not _host.has_method("get_nav_agent"):
				_fail("宿主沒有 get_nav_agent")
				return _finish()
			var player: Node = _host.call("get_player")
			if player == null:
				_fail("沒有生出 CharacterBody2D 玩家")
				return _finish()
			if not (player is CharacterBody2D):
				_fail("玩家不是 CharacterBody2D")
				return _finish()
			var body := player as CharacterBody2D
			if body.motion_mode != CharacterBody2D.MOTION_MODE_FLOATING:
				_fail("玩家 motion_mode 不是 FLOATING")
				return _finish()
			_start = body.global_position
			_dest = _host.call("marker_position", MAISUI) as Vector2
			if _dest == Vector2.ZERO:
				_fail("村場景沒有 maisui Marker")
				return _finish()
			## 先點一塊可走地面（Marker 與出生之間），確認導航有路且 move_and_slide 在走
			var mid: Vector2 = _start.lerp(_dest, 0.45)
			_host.call("tap_world", mid)
			_step = 1
			_wait = 0
		1:
			if _wait < 8:
				return false
			var agent: NavigationAgent2D = _host.call("get_nav_agent")
			if agent == null:
				_fail("沒有 NavigationAgent2D")
				return _finish()
			var path: PackedVector2Array = agent.get_current_navigation_path()
			if path.size() < 2:
				## 再等導航伺服器一拍
				if _wait < 40:
					return false
				_fail("點擊可走點後導航路徑是空的 size=%d" % path.size())
				return _finish()
			print("  ok nav path points=", path.size())
			if _host.has_method("has_entity_sprite") and bool(_host.call("has_entity_sprite", "exit_east")):
				_fail("exit_east 不該再畫黃箭頭")
				return _finish()
			if _host.has_method("has_nameplate") and not bool(_host.call("has_nameplate", "maisui")):
				_fail("麥穗沒有名稱牌")
				return _finish()
			if _host.has_method("has_nameplate") and not bool(_host.call("has_nameplate", "sword")):
				_fail("鏽劍沒有名稱牌")
				return _finish()
			print("  ok nameplates + no exit arrow")
			_physics_left = 90
			_step = 2
			_wait = 0
		2:
			if _wait < 90:
				return false
			var player2: CharacterBody2D = _host.call("get_player")
			var now: Vector2 = player2.global_position
			var closer := now.distance_to(_dest) < _start.distance_to(_dest) - 8.0 \
				or now.distance_to(_start) > 24.0
			if not closer:
				_fail("物理幀後人沒有沿路前進 start=%s now=%s dest=%s" % [_start, now, _dest])
				return _finish()
			print("  ok moved dist=", now.distance_to(_start))
			if int(player2.get("walk_frames_played")) <= 0:
				_fail("原生玩家走路沒有播走路幀（兔子在滑行）")
				return _finish()
			print("  ok walk frames played=", int(player2.get("walk_frames_played")))
			_got_id = ""
			_host.call("tap_entity", MAISUI)
			_step = 3
			_wait = 0
		3:
			if _got_id == MAISUI:
				print("  ok interacted ", _got_id)
				return _finish()
			if _wait < 180:
				return false
			_fail("點麥穗後沒收到 interacted('maisui') 實際='%s'" % _got_id)
			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("EXPLORE_NATIVE_OK")
		quit(0)
	else:
		print("EXPLORE_NATIVE_FAIL")
		quit(1)
	return true
