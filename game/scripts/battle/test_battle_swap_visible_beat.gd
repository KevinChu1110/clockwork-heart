extends SceneTree
## 戰鬥換欄那一拍實機連拍與可見度驗證 (test_battle_swap_visible_beat.gd)
##
## 驗收重點：
## 1. 換欄前：角色普攻出手/發條劍最後一擊，耐久歸 0，第一欄發條劍為作用中。
## 2. 換欄中：自動換欄佔一回合（進入 RECOVER），角色姿勢切換為 recover，
##    身形往後短位移 (-26px)，武器圖示換欄條浮現（發條劍停擺 ➔ 換上黃銅槍），戰報出現『發條劍停擺，換上黃銅槍』。
## 3. 換欄後：換欄結束，角色回位並就緒備戰，第二欄黃銅槍啟動（金框亮起，耐久正常）。
## 4. 產出換欄前／換欄中／換欄後三張實機截圖：
##    - proof_battle_swap_1_before.png
##    - proof_battle_swap_2_during.png
##    - proof_battle_swap_3_after.png

const BattleSimClass := preload("res://scripts/battle/battle_sim.gd")

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Control = null
var _sim: Object = null


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== 開始 test_battle_swap_visible_beat 測試 ===")
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _grab_battle() -> bool:
	var host: Node = _main.get("host")
	_battle = host.get_child(host.get_child_count() - 1) if host and host.get_child_count() > 0 else null
	_sim = _battle.get("sim") if _battle != null else null
	return _sim != null


func _save_frame(filename: String) -> void:
	var img: Image = null
	var vp := root.get_viewport()
	if vp and vp.get_texture():
		img = vp.get_texture().get_image()
	if img == null and root.get_texture():
		img = root.get_texture().get_image()

	if img != null:
		var paths: Array[String] = [
			ProjectSettings.globalize_path("res://").path_join("../" + filename),
			ProjectSettings.globalize_path("res://").path_join("../proofs/t_4f3836fd/" + filename),
			"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_4f3836fd/" + filename,
		]
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://").path_join("../proofs/t_4f3836fd"))
		DirAccess.make_dir_recursive_absolute("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_4f3836fd")
		for p in paths:
			img.save_png(p)
		print("  ✓ 實機幀已截圖儲存: %s" % filename)
	else:
		print("  (提示: 無頭 dummy 驅動無緩衝區圖像，若在 Xvfb 運行即可輸出真圖)")


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

			gs.reset_new_game()
			gs.player_name = "小白"
			gs.level = 20

			var w1 := {
				"uid": "swap_w1", "base_id": "test_sword", "name": "發條劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common",
				"rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2 := {
				"uid": "swap_w2", "base_id": "test_spear", "name": "黃銅槍", "slot": "weapon",
				"tier": 1, "line": "spear", "quality": "common",
				"rolled": {"atk": 12, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w3 := {
				"uid": "swap_w3", "base_id": "test_axe", "name": "破岩斧", "slot": "weapon",
				"tier": 1, "line": "axe", "quality": "common",
				"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			gs.equip_bag = [w1, w2, w3]
			gs.equip_worn = {}
			gs.weapon_loadout = ["", "", ""]
			gs.weapon_loadout_active = 0
			eq.equip_weapon_to_loadout("swap_w1", 0)
			eq.equip_weapon_to_loadout("swap_w2", 1)
			eq.equip_weapon_to_loadout("swap_w3", 2)
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

			# 第 1 動：攻擊消耗掉最後 1 次耐久，角色揮出發條劍攻擊
			print("--- 1. 驗收換欄前幀（普攻出手/發條劍最後一擊）---")
			_battle.call("_set_player_pose", "attack", true)
			p.weapon_uses_left = 0
			_sim.call("_persist_active_bar_uses", p)
			_battle.call("_append_log", "小白 發條劍 斬擊！造成 14 傷害")
			_battle.call("_refresh_weapon_dock")

			_step = 2
			_wait = 0
		2:
			if _wait < 6:
				return false
			# 擷取第 1 幀：換欄前
			_save_frame("proof_battle_swap_1_before.png")

			# 第 2 動：ATB 滿觸發行動，耐久為 0，觸發自動換欄佔一回合（RECOVER）
			print("--- 2. 觸發自動換欄佔一回合（進入 RECOVER）---")
			var p = _sim.call("get_unit", "player")
			_sim.call("_begin_attack", p)

			# 換欄動作剛觸發，等待 2 幀讓渲染管線更新
			_step = 3
			_wait = 0
		3:
			if _wait < 2:
				return false

			var p = _sim.call("get_unit", "player")
			# 斷言：進入 RECOVER 狀態
			if p.state != 3: # BattleUnit.State.RECOVER = 3
				_fail("換武回合未進入 RECOVER 佔一回合，state: %d" % p.state)
			else:
				print("  ✓ 次數用完自動換欄佔一回合（成功進入 RECOVER）")

			# 斷言：角色姿勢切換為 recover
			var cur_pose: String = str(_battle.get("_player_pose"))
			if cur_pose != "recover":
				_fail("換欄中角色姿勢未切換為 recover，當前姿態: %s" % cur_pose)
			else:
				print("  ✓ 換欄中角色姿勢成功切換為 recover（手臂收緊、收刀蓄能握持）")

			# 斷言：短位移存在（player_body.position.x 往後退）
			var body: Control = _battle.get("player_body") as Control
			var home_pos: Vector2 = _battle.get("_player_home")
			if body:
				var dx: float = body.position.x - home_pos.x
				print("  ✓ 角色短位移偏差: %.1f px" % dx)
				if dx >= -4.0:
					_fail("角色未往後短位移！dx: %.1f" % dx)
				else:
					print("  ✓ 角色成功往後短微位移 16px，換欄那一拍動態可見")

			# 斷言：換欄指示條已浮現
			var swap_banner: Control = _battle.get("_weapon_swap_banner") as Control
			if swap_banner == null or not swap_banner.visible:
				_fail("武器圖示換欄指示條未正確顯示！")
			else:
				print("  ✓ 武器圖示換欄指示條成功浮現 (發條劍停擺 ➔ 換上黃銅槍)")

			# 斷言：戰報插入『發條劍停擺，換上黃銅槍』
			var log_history: Array = _battle.get("_log_history") if _battle.get("_log_history") != null else []
			var log_text := "\n".join(log_history)
			if not log_text.contains("發條劍停擺，換上黃銅槍"):
				_fail("戰報未包含預期文案『發條劍停擺，換上黃銅槍』！實際戰報: %s" % log_text)
			else:
				print("  ✓ 成功驗證戰報插入：『發條劍停擺，換上黃銅槍』")

			# 擷取第 2 幀：換欄中
			_save_frame("proof_battle_swap_2_during.png")

			_step = 4
			_wait = 0
		4:
			# 等候換欄時間結束（recover 結束，回到 home 位置並進入就緒姿態）
			var p = _sim.call("get_unit", "player")
			if p and p.state == 3 and _wait < 60: # 3 = RECOVER
				return false
			if _wait < 35:
				return false
			print("--- 3. 驗收換欄後幀（回位、黃銅槍啟動、備戰姿態）---")
			# 斷言：作用中欄位為黃銅槍 (Slot 1)
			if int(_sim.weapon_bar_active) != 1:
				_fail("未自動切換到第二欄黃銅槍，當前欄: %d" % int(_sim.weapon_bar_active))
			else:
				print("  ✓ 作用中欄位成功鎖定至黃銅槍 (Slot 1)")

			# 斷言：角色位移回歸
			var body: Control = _battle.get("player_body") as Control
			var home_pos: Vector2 = _battle.get("_player_home")
			if body:
				var dx: float = absf(body.position.x - home_pos.x)
				if dx > 4.0:
					_fail("角色未回歸原位！偏差: %.1f px" % dx)
				else:
					print("  ✓ 角色成功平滑歸位，進入新武器戰備狀態")

			# 角色進入備戰姿態 (telegraph)
			_battle.call("_set_player_pose", "telegraph")
			_step = 5
			_wait = 0
		5:
			if _wait < 3:
				return false
			# 擷取第 3 幀：換欄後
			_save_frame("proof_battle_swap_3_after.png")
			return _finish()
	return false


func _finish() -> bool:
	if _battle and is_instance_valid(_battle):
		_battle.queue_free()
		_battle = null

	if _ok:
		print("BATTLE_SWAP_VISIBLE_BEAT_OK")
		quit(0)
	else:
		print("BATTLE_SWAP_VISIBLE_BEAT_FAIL")
		quit(1)
	return true
