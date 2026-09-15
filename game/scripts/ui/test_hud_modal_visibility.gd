extends SceneTree
## 驗證全域 HUD 在大廳與彈窗時的穿透遮蓋修復，以及獅族換裝資源 import 正確性

var _main: Node = null
var _step: int = 0
var _wait: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始 HUD 遮蓋修復與獅族換裝資源驗證測試 ===")

	# 1. 驗證獅族換裝資源能否正確載入（非空白、無報錯）
	var lion_costume_tex = load("res://assets/sprites/player/paperdoll/lion/costume/costume_steam_artisan.png")
	if lion_costume_tex == null:
		printerr("FAIL: lion costume_steam_artisan.png load failed!")
		quit(1)
		return
	print("  ✓ lion costume_steam_artisan.png 載入成功: ", lion_costume_tex.get_size())

	var lion_paint_tex = load("res://assets/sprites/player/paperdoll/lion/chassis/paint_midnight_navy.png")
	if lion_paint_tex == null:
		printerr("FAIL: lion paint_midnight_navy.png load failed!")
		quit(1)
		return
	print("  ✓ lion paint_midnight_navy.png 載入成功: ", lion_paint_tex.get_size())

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait >= 30 and current_scene != null:
				_main = current_scene
				print("  ✓ main.tscn 載入完成")
				
				# 測試 1: 在大廳時 HUD 與 hotbar 應為 hidden
				_main.call("_go_mobile_lobby")
				_step = 1
				_wait = 0
		1:
			if _wait >= 20:
				var maple_hud = _main.get("_maple_hud")
				var hotbar = _main.get("_hotbar")
				if maple_hud.visible:
					printerr("FAIL: 大廳中 _maple_hud 應該為 hidden，但 visible == true")
					quit(1)
					return false
				if hotbar.visible:
					printerr("FAIL: 大廳中 _hotbar 應該為 hidden，但 visible == true")
					quit(1)
					return false
				print("  ✓ 測試 1 通過: 大廳中 _maple_hud 與 _hotbar 皆為 hidden")
				
				# 測試 2: 探索畫面時 HUD 與 hotbar 應為 visible
				_main.call("proof_jump_explore", "village")
				_step = 2
				_wait = 0
		2:
			if _wait >= 20:
				var maple_hud = _main.get("_maple_hud")
				var hotbar = _main.get("_hotbar")
				if not maple_hud.visible:
					printerr("FAIL: 探索中 _maple_hud 應該為 visible，但 visible == false")
					quit(1)
					return false
				if not hotbar.visible:
					printerr("FAIL: 探索中 _hotbar 應該為 visible，但 visible == false")
					quit(1)
					return false
				print("  ✓ 測試 2 通過: 探索畫面中 _maple_hud 與 _hotbar 皆為 visible")

				# 測試 3: 探索畫面中開啟彈窗，HUD 與 hotbar 應為 hidden
				var ForgeClass = load("res://scripts/ui/forge_dialog.gd")
				var dlg = ForgeClass.new()
				_main.add_child(dlg)
				_step = 3
				_wait = 0
		3:
			if _wait >= 10:
				var maple_hud = _main.get("_maple_hud")
				var hotbar = _main.get("_hotbar")
				if maple_hud.visible:
					printerr("FAIL: 探索中開啟 ForgeDialog 時 _maple_hud 應該隱藏，但 visible == true")
					quit(1)
					return false
				if hotbar.visible:
					printerr("FAIL: 探索中開啟 ForgeDialog 時 _hotbar 應該隱藏，但 visible == true")
					quit(1)
					return false
				print("  ✓ 測試 3 通過: 彈窗開啟時 _maple_hud 與 _hotbar 成功隱藏")

				# 關閉彈窗
				for c in _main.get_children():
					if c.name == "ForgeDialog" or c.has_method("open_forge"):
						c.queue_free()
				_step = 4
				_wait = 0
		4:
			if _wait >= 10:
				# 測試 4: 戰鬥中 _maple_hud 隱藏，但 _hotbar 保持顯示
				_main.call("proof_show_battle", "road_bandit")
				_step = 5
				_wait = 0
		5:
			if _wait >= 20:
				var maple_hud = _main.get("_maple_hud")
				var hotbar = _main.get("_hotbar")
				if maple_hud.visible:
					printerr("FAIL: 戰鬥中 _maple_hud 應該為 hidden，但 visible == true")
					quit(1)
					return false
				if not hotbar.visible:
					printerr("FAIL: 戰鬥中 _hotbar 應該維持 visible，但 visible == false")
					quit(1)
					return false
				print("  ✓ 測試 4 通過: 戰鬥中 _maple_hud 隱藏且 _hotbar 維持顯示")

				print("HUD_MODAL_VISIBILITY_OK")
				quit(0)
				return true
	return false
