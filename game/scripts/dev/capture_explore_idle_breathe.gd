extends SceneTree
## 《發條之心》探索站立呼吸與換裝實機截圖產生器 (xvfb 驗證用)
## 依據任務規範：
## 1. 站立兩張間隔 >= 1.0s (證明在呼吸，scale/影子有可見差異)
## 2. 走路一張 (scale 必須為 1, 1)
## 3. 兩套外裝各截一張站立圖 (diff > 10000 px，證明換裝有效且非焊死)

var _out_dir: String = ""
var _time: float = 0.0
var _step: int = 0
var _host: Control = null
var _gs: Node = null
var _player: CharacterBody2D = null

var scale_t0: Vector2 = Vector2.ZERO
var shadow_scale_t0: Vector2 = Vector2.ZERO
var scale_t1: Vector2 = Vector2.ZERO
var shadow_scale_t1: Vector2 = Vector2.ZERO
var scale_walk: Vector2 = Vector2.ZERO
var shadow_scale_walk: Vector2 = Vector2.ZERO


func _initialize() -> void:
	print("=== 開始產生探索站立呼吸與換裝實機截圖 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

	var base := ProjectSettings.globalize_path("res://")
	_out_dir = base.path_join("../screenshots")
	DirAccess.make_dir_recursive_absolute(_out_dir)

	_gs = root.get_node_or_null("GameState")
	if _gs:
		_gs.player_race = "rabbit"
		_gs.player_name = "小白"
		_gs.chapter = "c0"
		# 第一套外裝：胡桃鉗近衛軍裝 (costume_nutcracker_guard)
		_gs.paperdoll_slots = {
			"race": "rabbit",
			"costume": "costume_nutcracker_guard",
			"chassis": "paint_ivory_stock",
			"costume_id": "costume_nutcracker_guard",
			"paint_id": "paint_ivory_stock"
		}

	var Host = load("res://scripts/world/explore_host.gd")
	if Host == null:
		push_error("無法載入 ExploreHost")
		quit(1)
		return

	_host = Host.new()
	root.add_child(_host)
	_host.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_host.setup("village")
	_step = 1
	_time = 0.0


func _process(delta: float) -> bool:
	_time += delta

	if _host and "get_player" in _host:
		_player = _host.call("get_player")

	if _host and "_camera" in _host:
		var cam: Camera2D = _host._camera
		if cam:
			cam.zoom = Vector2(3.5, 3.5)

	match _step:
		1:
			# 等待呼吸 Tween 運行至第一個波峰 (1.1s，scale 為 1.03, 0.97)
			if _time >= 1.1:
				if _player:
					var pbody: Sprite2D = _player.get("body")
					var pshadow: Sprite2D = _player.get("shadow")
					if pbody:
						scale_t0 = pbody.scale
					if pshadow:
						shadow_scale_t0 = pshadow.scale
				_save_screenshot("proof_explore_idle_breathe_t0.png")
				_save_screenshot("proof_explore_equipped_costume_a.png")
				print("  ✓ [t0=1.1s] 截取站立呼吸波峰 1 (Costume A): body scale=%s, shadow scale=%s" % [scale_t0, shadow_scale_t0])
				_step = 2
				_time = 0.0
		2:
			# 再等待 1.1s (間隔 1.1s >= 1.0s)，呼吸 Tween 運行至反向波峰 (2.2s，scale 為 0.98, 1.02)
			if _time >= 1.1:
				if _player:
					var pbody: Sprite2D = _player.get("body")
					var pshadow: Sprite2D = _player.get("shadow")
					if pbody:
						scale_t1 = pbody.scale
					if pshadow:
						shadow_scale_t1 = pshadow.scale
				_save_screenshot("proof_explore_idle_breathe_t1.png")
				print("  ✓ [t1=2.2s] 截取站立呼吸波峰 2 (間隔 1.1s): body scale=%s, shadow scale=%s" % [scale_t1, shadow_scale_t1])
				# 切換為第二套外裝：皇家巡遊金屬禮服 (costume_royal_parade)
				if _gs:
					_gs.paperdoll_slots = {
						"race": "rabbit",
						"costume": "costume_royal_parade",
						"chassis": "paint_ivory_stock",
						"costume_id": "costume_royal_parade",
						"paint_id": "paint_ivory_stock"
					}
				_step = 3
				_time = 0.0
		3:
			# 等待第二套外裝載入並穩定渲染 (0.5s)
			if _time >= 0.5:
				_save_screenshot("proof_explore_equipped_costume_b.png")
				print("  ✓ 截取 [第二套外裝: 皇家巡遊金屬禮服] 探索待機畫面")
				# 指令角色移動走向 maisui Marker
				if _host and _host.has_method("marker_position") and _player:
					var dest: Vector2 = _host.call("marker_position", "maisui")
					_host.call("tap_world", dest)
				_step = 4
				_time = 0.0
		4:
			# 等待角色實際起步移動 (_moving == true)
			var is_moving: bool = bool(_player.get("_moving")) if _player else false
			if is_moving and _time >= 0.1: # 確保在移動中穩定採集
				if _player:
					var pbody: Sprite2D = _player.get("body")
					var pshadow: Sprite2D = _player.get("shadow")
					if pbody:
						scale_walk = pbody.scale
					if pshadow:
						shadow_scale_walk = pshadow.scale
				_save_screenshot("proof_explore_walking.png")
				print("  ✓ 截取走路中畫面: moving=%s, body scale=%s, shadow scale=%s" % [
					is_moving,
					scale_walk,
					shadow_scale_walk
				])
				print("=== 實機截圖全部完成 ===")
				quit(0)
				return true
			elif _time > 3.0:
				push_error("等待角色移動逾時")
				quit(1)
				return true

	return false


func _save_screenshot(filename: String) -> void:
	var vp := root.get_viewport()
	if vp == null:
		return
	var tex := vp.get_texture()
	if tex == null:
		return
	var img := tex.get_image()
	if img == null or img.is_empty():
		return

	var file_path := _out_dir.path_join(filename)
	var err := img.save_png(file_path)
	if err == OK:
		print("  [截圖成功] -> ", file_path)
	else:
		push_error("儲存截圖失敗: %s, 錯誤代碼: %d" % [file_path, err])
