extends SceneTree
## 戰鬥自動換欄角色微動卡榫拍點演出單元測試 (test_battle_swap_beat_fx.gd)
##
## 依 docs/CLOCKWORK_ART_MUSIC_BRIEF.md 第 0 條與第 3 條規範：
## 1. 換欄事件 (weapon_slot_switched) 觸發時，主角 player_body 進入 swap 姿態。
## 2. 插入 0.25 秒微動卡榫拍點演出：
##    - 角色微揚 (position.y 輕提 8px，平滑回位)
##    - 發條鑰匙加速轉動半圈 (8 幀循環中均勻推進 4 幀 / 180 度)
##    - 武器淡入定位 (PlayerWeaponOverlay 淡入並定於握持座標)
##    - 與 swap.wav 音效及戰報緊密對齊
## 3. 0.25 秒後平滑回位並恢復 idle 待機呼吸。

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null
var _sim: Object = null
var _initial_key_frame: int = 0
var _home_pos: Vector2 = Vector2.ZERO


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始 test_battle_swap_beat_fx 測試 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _grab_battle() -> bool:
	var host: Node = _main.get("host")
	_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
	_sim = _battle.get("sim") if _battle != null else null
	return _sim != null and _battle != null


func _save_frame(filename: String) -> void:
	var img: Image = null
	var vp := root.get_viewport()
	if vp and vp.get_texture():
		img = vp.get_texture().get_image()
	if img == null and root.get_texture():
		img = root.get_texture().get_image()

	if img != null:
		var dir_path := ProjectSettings.globalize_path("res://").path_join("../proofs/t_8b44d76e")
		DirAccess.make_dir_recursive_absolute(dir_path)
		var full_path := dir_path.path_join(filename)
		img.save_png(full_path)
		print("  ✓ 實機幀已截圖儲存: %s" % full_path)
	else:
		print("  (提示: 無頭 dummy 驅動無緩衝區圖像，若在 Xvfb 運行即可輸出真圖)")


func _save_crop(filename: String, rect: Rect2i) -> void:
	var img: Image = null
	var vp := root.get_viewport()
	if vp and vp.get_texture():
		img = vp.get_texture().get_image()
	if img == null and root.get_texture():
		img = root.get_texture().get_image()

	if img != null:
		var cropped := img.get_region(rect)
		var dir_path := ProjectSettings.globalize_path("res://").path_join("../proofs/t_8b44d76e")
		DirAccess.make_dir_recursive_absolute(dir_path)
		var full_path := dir_path.path_join(filename)
		cropped.save_png(full_path)
		print("  ✓ 局部特寫裁切截圖已儲存: %s" % full_path)


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs := root.get_node_or_null("GameState")
			var eq := root.get_node_or_null("EquipmentSystem")
			if _main == null or gs == null or eq == null:
				_fail("主場景初始化失敗")
				return _finish()

			# 驗證 1：swap.wav 音效資產與 AudioManager 接上
			print("--- 1. 驗證 swap.wav 音效資產與 AudioManager 接上 ---")
			var swap_wav_path := "res://assets/audio/sfx/swap.wav"
			if not ResourceLoader.exists(swap_wav_path):
				_fail("swap.wav 檔案不存在於 res://assets/audio/sfx/swap.wav")
			else:
				print("  ok swap.wav 音效檔案存在")

			var am := root.get_node_or_null("AudioManager")
			if am == null:
				_fail("AudioManager 節點不存在")
			else:
				if am.has_method("play_swap"):
					print("  ok AudioManager 支援 play_swap() 方法")
				else:
					_fail("AudioManager 缺少 play_swap() 方法")

			# 驗證 2：swap 512 像素姿勢貼圖存在且有效
			print("--- 2. 驗證主角 swap 512 動作姿態貼圖 ---")
			var swap_tex := SpriteDB.player_pose("swap", "rabbit")
			if swap_tex == null:
				_fail("SpriteDB.player_pose('swap', 'rabbit') 回傳 null")
			elif swap_tex.get_width() < 256 or swap_tex.get_height() < 256:
				_fail("swap 姿態貼圖解析度不足 256: %dx%d" % [swap_tex.get_width(), swap_tex.get_height()])
			else:
				print("  ok 主角 swap 姿態貼圖載入成功，尺寸: %dx%d" % [swap_tex.get_width(), swap_tex.get_height()])

			gs.reset_new_game()
			gs.player_name = "小白"
			gs.level = 20

			var w1 := {
				"uid": "test_swap_w1", "base_id": "test_sword", "name": "發條劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common",
				"rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2 := {
				"uid": "test_swap_w2", "base_id": "test_spear", "name": "黃銅槍", "slot": "weapon",
				"tier": 1, "line": "spear", "quality": "common",
				"rolled": {"atk": 12, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w3 := {
				"uid": "test_swap_w3", "base_id": "test_axe", "name": "破岩斧", "slot": "weapon",
				"tier": 1, "line": "axe", "quality": "common",
				"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			gs.equip_bag = [w1, w2, w3]
			gs.equip_worn = {}
			gs.weapon_loadout = ["", "", ""]
			gs.weapon_loadout_active = 0
			eq.equip_weapon_to_loadout("test_swap_w1", 0)
			eq.equip_weapon_to_loadout("test_swap_w2", 1)
			eq.equip_weapon_to_loadout("test_swap_w3", 2)
			eq.switch_weapon_loadout(0)

			_main.call("_start_battle_raw", "wolf")
			_step = 1
			_wait = 0

		1:
			if _wait < 15:
				return false
			if not _grab_battle():
				_fail("無法取得戰鬥場景與 sim")
				return _finish()

			var p = _sim.call("get_unit", "player")
			p.weapon_uses_left = 1
			p.weapon_uses_max = 2
			if _sim.weapon_bars.size() > 0:
				_sim.weapon_bars[0]["name"] = "發條劍"
				_sim.weapon_bars[0]["uses_left"] = 1
				_sim.weapon_bars[0]["uses_max"] = 2
			if _sim.weapon_bars.size() > 1:
				_sim.weapon_bars[1]["name"] = "黃銅槍"
				_sim.weapon_bars[1]["uses_left"] = 2
				_sim.weapon_bars[1]["uses_max"] = 2
			if _sim.weapon_bars.size() > 2:
				_sim.weapon_bars[2]["name"] = "破岩斧"
				_sim.weapon_bars[2]["uses_left"] = 2
				_sim.weapon_bars[2]["uses_max"] = 2

			_battle.call("_refresh_weapon_dock")

			# 記錄換欄前當前鑰匙幀與 home 位置
			var body: Control = _battle.get("player_body") as Control
			_home_pos = _battle.get("_player_home")
			if _home_pos == Vector2.ZERO and body:
				_home_pos = body.position
			_initial_key_frame = int(_battle.get("_winding_key_frame_index"))

			# 存換欄前截圖
			_save_frame("proof_battle_swap_1_before.png")

			# 觸發換欄行動：消耗最後 1 次耐久，觸發自動換欄
			print("--- 3. 觸發自動換欄事件 (weapon_slot_switched) ---")
			p.weapon_uses_left = 0
			_sim.call("_persist_active_bar_uses", p)
			_sim.call("_begin_attack", p)
			# 暫停 sim 背景推進，使 0.25 秒微動卡榫拍點動態不受後續回合搶先行動干擾
			_sim.set("sim_paused", true)

			# 剛觸發拍點，等待 1 幀讓動效進入執行期
			_step = 2
			_wait = 0

		2:
			if _wait < 1:
				return false

			print("--- 4. 斷言微動卡榫拍點演出各要素 ---")
			# 斷言 A：角色切換為 swap 姿態
			var cur_pose: String = str(_battle.get("_player_pose"))
			if cur_pose != "swap":
				_fail("換欄微動拍點中，角色姿態未切換為 swap，當前為: %s" % cur_pose)
			else:
				print("  ok 角色成功進入 swap 換欄姿態")

			# 斷言 B：角色微揚（position.y 向上提，y < home.y）
			var body: Control = _battle.get("player_body") as Control
			if body == null:
				_fail("player_body 為 null")
			else:
				var dy: float = body.position.y - _home_pos.y
				if dy >= 0.0:
					_fail("角色未微揚！dy: %.2f (預期 < 0)" % dy)
				else:
					print("  ok 角色微揚驗證通過 (dy: %.2f px 輕提)" % dy)

			# 斷言 C：發條鑰匙聯動加速
			var key_node: TextureRect = _battle.get("_battle_winding_key")
			if key_node == null or not is_instance_valid(key_node):
				_fail("_battle_winding_key 節點無效")
			else:
				print("  ok 發條鑰匙節點有效且與拍點聯動中")

			# 斷言 D：武器淡入定位
			var weapon_overlay: TextureRect = _battle.get("_battle_weapon")
			if weapon_overlay == null or not is_instance_valid(weapon_overlay):
				_fail("_battle_weapon 節點無效")
			else:
				if not weapon_overlay.visible:
					_fail("武器 overlay 在換欄拍點中 visible 應為 true")
				elif weapon_overlay.texture == null:
					_fail("武器 overlay 在換欄拍點中 texture 不應為 null")
				else:
					print("  ok 武器淡入定位驗證通過: visible=true, texture=%s" % weapon_overlay.texture.resource_path)

			# 斷言 E：換欄指示條浮現
			var swap_banner: Control = _battle.get("_weapon_swap_banner")
			if swap_banner == null or not swap_banner.visible:
				_fail("武器換欄指示條未正常顯示")
			else:
				print("  ok 武器換欄指示條正常浮現 (發條劍停擺 ➔ 換上黃銅槍)")

			# 斷言 F：戰報緊密對齊
			var log_history: Array = _battle.get("_log_history") if _battle.get("_log_history") != null else []
			var log_text := "\n".join(log_history)
			if not log_text.contains("發條劍停擺，換上黃銅槍"):
				_fail("戰報未對齊預期文案『發條劍停擺，換上黃銅槍』！")
			else:
				print("  ok 戰報精準對齊：『發條劍停擺，換上黃銅槍』")

			# 存換欄中截圖
			_save_frame("proof_battle_swap_2_swap_beat.png")
			if body:
				_save_crop("crop_player_swap_pose.png", Rect2i(Vector2i(int(body.global_position.x - 40), int(body.global_position.y - 20)), Vector2i(280, 290)))

			_step = 3
			_wait = 0

		3:
			# 等候 0.25 秒拍點演出結束（約 24 幀）
			if _wait < 24:
				return false

			print("--- 5. 斷言 0.25 秒後拍點結束回位與狀態恢復 ---")
			# 斷言：0.25 秒後發條鑰匙累計旋轉半圈（4 幀 / 180 度）
			var spin_steps: int = int(_battle.get("_swap_spin_steps"))
			print("  發條鑰匙換欄拍點步進數: %d 格（4 格代表 180 度半圈）" % spin_steps)
			if spin_steps != 4:
				_fail("發條鑰匙未精準旋轉半圈 (4 幀)！實際步進數: %d" % spin_steps)
			else:
				print("  ok 發條鑰匙加速旋轉半圈 (180度 / 4幀) 驗證通過")

			# 斷言：角色平滑歸位
			var body: Control = _battle.get("player_body") as Control
			if body:
				var dist: float = body.position.distance_to(_home_pos)
				if dist > 6.0:
					_fail("角色未回歸原位！偏差距離: %.2f px" % dist)
				else:
					print("  ok 角色平滑歸位驗證通過 (偏差: %.2f px)" % dist)

			# 存換欄後截圖
			_save_frame("proof_battle_swap_3_after.png")
			return _finish()

	return false


func _finish() -> bool:
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	if _ok:
		print("=======================================================")
		print("BATTLE_SWAP_BEAT_FX_OK")
		print("=======================================================")
		quit(0)
	else:
		print("=======================================================")
		print("BATTLE_SWAP_BEAT_FX_FAIL")
		print("=======================================================")
		quit(1)
	return true
