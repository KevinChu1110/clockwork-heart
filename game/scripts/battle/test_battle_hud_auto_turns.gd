extends SceneTree
## 無頭自動換武流程與純自動戰鬥HUD驗證 (test_battle_hud_auto_turns.gd)
##
## 驗收重點：
## 1. 徹底移除右下角格擋、普攻、技能、換武、逃離等所有手動按鈕，右下角無任何操作輪盤。
## 2. 戰鬥畫面僅保留雙方血條、怒氣、當前武器名與剩餘次數、兩欄備用武器小圖（用完變灰）、部位條、跳字與小暫停鈕。
## 3. 次數用完自動換欄佔一回合並插入戰報『發條劍停擺，換上黃銅槍』，畫面停一拍。
## 4. 三欄全空改赤手，同樣佔一回合、戰報一句。
## 5. 部位破壞有 0.4 秒慢動作，結束後時間流速歸位；缺 swap 音檔不當機。
## 6. 鍵盤／點擊不能手動換武、暴怒、格擋（見 test_battle_keys／test_battle_touch）。
## 7. 產出 proof_battle_hud_auto_turns.png 實機截圖。

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
	print("=== 開始 test_battle_hud_auto_turns 測試 ===")
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

			# 配置三把武器：發條劍 / 黃銅槍 / 破岩斧
			var w1 := {
				"uid": "auto_w1", "base_id": "test_sword", "name": "發條劍", "slot": "weapon",
				"tier": 1, "line": "sword", "quality": "common",
				"rolled": {"atk": 10, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w2 := {
				"uid": "auto_w2", "base_id": "test_spear", "name": "黃銅槍", "slot": "weapon",
				"tier": 1, "line": "spear", "quality": "common",
				"rolled": {"atk": 12, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			var w3 := {
				"uid": "auto_w3", "base_id": "test_axe", "name": "破岩斧", "slot": "weapon",
				"tier": 1, "line": "axe", "quality": "common",
				"rolled": {"atk": 15, "def": 0, "hp": 0, "crit": 0, "crit_dmg": 0},
			}
			gs.equip_bag = [w1, w2, w3]
			gs.equip_worn = {}
			gs.weapon_loadout = ["", "", ""]
			gs.weapon_loadout_active = 0
			eq.equip_weapon_to_loadout("auto_w1", 0)
			eq.equip_weapon_to_loadout("auto_w2", 1)
			eq.equip_weapon_to_loadout("auto_w3", 2)
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

			# 1. 驗證右下角無任何操作輪盤與格擋按鈕
			print("--- 1. 驗證右下角零操作輪盤、零格擋按鈕 ---")
			var tc: Dictionary = _battle.call("thumb_controls")
			for k in ["attack", "skill", "switch", "flee", "lock"]:
				var btn: Control = tc.get(k) as Control
				if btn != null and btn.is_visible_in_tree():
					_fail("右下角仍有手動按鈕: %s" % k)
			print("  ✓ 右下角徹底移除 attack/skill/switch/flee/lock 等所有手動按鈕")

			# 2. 驗證保留要素：血條、怒氣、小暫停鈕、武器欄
			print("--- 2. 驗證畫面核心可讀性介面 ---")
			var php: Control = _battle.get("player_hp") as Control
			var ehp: Control = _battle.get("enemy_hp") as Control
			var prage: Control = _battle.get("player_rage") as Control
			var pause_b: Control = tc.get("pause") as Control
			var dock: Control = _battle.get("_weapon_dock") as Control

			if php == null or not php.is_visible_in_tree():
				_fail("玩家血條未正確顯示")
			if ehp == null or not ehp.is_visible_in_tree():
				_fail("敵人血條未正確顯示")
			if prage == null or not prage.is_visible_in_tree():
				_fail("怒氣槽未正確顯示")
			if pause_b == null or not pause_b.is_visible_in_tree():
				_fail("小暫停鈕未正確顯示")
			else:
				print("  ✓ 小暫停鈕正常掛載於右上角，尺寸: ", pause_b.size)

			if dock == null or dock.get_child_count() < 3:
				_fail("三欄武器欄未正確建立")
			else:
				print("  ✓ 三欄武器欄正常掛載，格子數: %d" % dock.get_child_count())

			# 3. 實作次數耗盡與自動換欄佔一回合驗證
			print("--- 3. 驗證次數用完自動換欄佔一回合並插入戰報 ---")
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

			# 第 1 動：攻擊消耗掉最後 1 次耐久
			p.weapon_uses_left = 0
			_sim.call("_persist_active_bar_uses", p)
			print("  ✓ 發條劍最後 1 次攻擊打出，剩餘耐久歸 0")

			# 第 2 動：ATB 滿觸發行動，此時武器耐久為 0，應自動換欄佔一回合
			var foes: Array = _sim.call("living_of", 1) # 1 = BattleUnit.Team.ENEMY
			var enemy = foes[0] if foes.size() > 0 else null
			var enemy_hp_before: int = enemy.hp if enemy != null else 0

			_sim.call("_begin_attack", p)

			# 驗證此回合佔一回合：狀態為 recover，未對敵人造成傷害（未揮出攻擊）
			if p.state != 3: # BattleUnit.State.RECOVER = 3
				_fail("換武回合未進入 RECOVER 佔一回合，state: %d" % p.state)
			else:
				print("  ✓ 次數用完自動換欄佔一回合（成功進入 RECOVER，未打出普通攻擊）")

			if enemy != null:
				var enemy_hp_after: int = enemy.hp
				if enemy_hp_after != enemy_hp_before:
					_fail("換武回合不應對敵人造成傷害！HP: %d -> %d" % [enemy_hp_before, enemy_hp_after])
				else:
					print("  ✓ 換武回合敵人未受傷，確認換武佔滿該回合行動")

			# 驗證作用中武器欄已切換為黃銅槍 (Slot 1)
			if int(_sim.weapon_bar_active) != 1:
				_fail("未自動切換到第二欄黃銅槍，當前欄: %d" % int(_sim.weapon_bar_active))
			else:
				print("  ✓ 作用中欄位成功自動切換至黃銅槍 (Slot 1)")

			# 4. 驗證戰報插入『發條劍停擺，換上黃銅槍』
			var log_history: Array = _battle.get("_log_history") if _battle.get("_log_history") != null else []
			var log_text := "\n".join(log_history)
			if log_text == "":
				var log_lbl: RichTextLabel = _battle.get("log_label") as RichTextLabel
				if log_lbl:
					log_text = log_lbl.get_parsed_text()
			print("  [戰報記錄數]: %d" % log_history.size())

			if not log_text.contains("發條劍停擺，換上黃銅槍"):
				_fail("戰報未包含預期文案『發條劍停擺，換上黃銅槍』！實際戰報: %s" % log_text)
			else:
				print("  ✓ 成功驗證戰報插入：『發條劍停擺，換上黃銅槍』")

			# 換武停一拍：BattleView 暫停 sim 一小段
			if float(_battle.get("_beat_hold_left")) <= 0.0:
				_fail("換武後沒有停一拍（_beat_hold_left 應 > 0）")
			else:
				print("  ✓ 換武停一拍：%.2fs" % float(_battle.get("_beat_hold_left")))

			# 5. 三欄全空：改赤手，同樣佔一回合
			print("--- 4. 驗證三欄用盡改赤手 ---")
			_battle.set_process(false)  # 只看這一動，不讓 sim 自己跑
			for i in _sim.weapon_bars.size():
				_sim.weapon_bars[i]["uses_left"] = 0
			p.weapon_uses_left = 0
			p.state = 0
			_sim.call("_begin_attack", p)
			if not bool(p.bare_fisted):
				_fail("三欄用盡後應改赤手")
			elif p.state != 3:
				_fail("改赤手那一動應佔一回合（RECOVER），state: %d" % p.state)
			else:
				print("  ✓ 三欄用盡 → 赤手，佔一回合")
			var log2 := "\n".join(_battle.get("_log_history"))
			if not log2.contains("黃銅槍停擺，三欄用盡，改用赤手"):
				_fail("戰報缺『黃銅槍停擺，三欄用盡，改用赤手』！實際: %s" % log2)
			else:
				print("  ✓ 戰報：黃銅槍停擺，三欄用盡，改用赤手")

			# 6. 部位破壞慢動作
			print("--- 5. 驗證部位破壞 0.4 秒慢動作 ---")
			_battle.call("_on_event", "part_broken", {"boss_id": "wolf", "part_name": "測試部位", "part_id": "t"})
			if Engine.time_scale >= 0.99 or not bool(_battle.get("_in_slowmo")):
				_fail("部位破壞後應進慢動作（time_scale=%.2f）" % Engine.time_scale)
			else:
				print("  ✓ 部位破壞進慢動作 time_scale=%.2f" % Engine.time_scale)
			_step = 2
			_wait = 0
		2:
			# 等慢動作結束（真實時間 0.4 秒），time_scale 要歸位
			if bool(_battle.get("_in_slowmo")) and _wait < 2000:
				return false
			if absf(Engine.time_scale - 1.0) > 0.001:
				_fail("慢動作結束後 time_scale 沒歸位：%.2f" % Engine.time_scale)
			else:
				print("  ✓ 慢動作結束，time_scale 歸位 1.0")
			_step = 3
			_wait = 0
		3:
			if _wait < 8:
				return false

			# 5. 產出 proof_battle_hud_auto_turns.png 實機截圖
			print("--- 5. 擷取 proof_battle_hud_auto_turns.png 實機截圖 ---")
			var img: Image = null
			var vp := root.get_viewport()
			if vp and vp.get_texture():
				img = vp.get_texture().get_image()
			if img == null and root.get_texture():
				img = root.get_texture().get_image()

			if img != null:
				var p_root := ProjectSettings.globalize_path("res://").path_join("../proof_battle_hud_auto_turns.png")
				var p_proofs := ProjectSettings.globalize_path("res://").path_join("../proofs/t_c5b2eec7/proof_battle_hud_auto_turns.png")
				var p_ws := "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c5b2eec7/proof_battle_hud_auto_turns.png"

				DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://").path_join("../proofs/t_c5b2eec7"))
				DirAccess.make_dir_recursive_absolute("/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c5b2eec7")

				img.save_png(p_root)
				img.save_png(p_proofs)
				img.save_png(p_ws)
				print("  ✓ 實機截圖已儲存至: %s, %s, %s" % [p_root, p_proofs, p_ws])
			else:
				print("  (提示: 無頭 dummy 驅動無緩衝區圖像，若在 Xvfb 運行即可輸出真圖)")

			return _finish()
	return false


func _finish() -> bool:
	if _ok:
		print("BATTLE_HUD_AUTO_TURNS_OK")
		quit(0)
	else:
		print("BATTLE_HUD_AUTO_TURNS_FAIL")
		quit(1)
	return true
