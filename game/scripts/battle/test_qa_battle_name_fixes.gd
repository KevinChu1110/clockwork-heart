extends SceneTree
## 單元測試：QA #9 & #10 戰鬥日誌顯示名、敵方 HUD 名稱與角色名樣式驗證
## godot --headless -s res://scripts/battle/test_qa_battle_name_fixes.gd

const BattleSim = preload("res://scripts/battle/battle_sim.gd")
const WorldContent = preload("res://scripts/world/world_content.gd")

var _ok := true
var _step := 0
var _wait := 0
var _main: Node = null
var _battle: Node = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  FAIL: ", msg)
	_ok = false

func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_fail(msg)
	else:
		print("  [OK] ", msg)

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	print("=== 開始 QA #9 & #10 驗證測試 ===")

	# 1. 靜態資料檢驗
	var bandit_def := WorldContent.enemy_def("road_bandit")
	_assert(str(bandit_def.get("name")) == "荒路匪徒", "road_bandit enemy_def name 應為 '荒路匪徒'，實際為: %s" % bandit_def.get("name"))

	var ronin_def := WorldContent.enemy_def("black_ronin")
	_assert(str(ronin_def.get("name")) == "黑鏽浪人", "black_ronin enemy_def name 應為 '黑鏽浪人'，實際為: %s" % ronin_def.get("name"))

	var dummy_stats := {"name": "測試小白", "max_hp": 100, "hp": 100, "atk": 20, "def": 5, "speed": 10.0}
	var sim_bandit := BattleSim.make_world_fight(dummy_stats, "road_bandit")
	var u_bandit = sim_bandit.get_unit("road_bandit")
	_assert(u_bandit != null and u_bandit.display_name == "荒路匪徒", "road_bandit BattleUnit.display_name 應為 '荒路匪徒'")

	var sim_ronin := BattleSim.make_world_fight(dummy_stats, "black_ronin")
	var u_ronin = sim_ronin.get_unit("black_ronin")
	_assert(u_ronin != null and u_ronin.display_name == "黑鏽浪人", "black_ronin BattleUnit.display_name 應為 '黑鏽浪人'")

	change_scene_to_file("res://scenes/main.tscn")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		0:
			if _wait < 20:
				return false
			_main = current_scene
			var gs: Node = root.get_node_or_null("GameState")
			if _main == null or gs == null:
				_fail("main 或 GameState 未載入")
				quit(1)
				return true
			gs.call("reset_new_game", "rabbit")
			_main.call("proof_show_battle", "road_bandit")
			_step = 1
			_wait = 0

		1:
			if _wait < 25:
				return false
			var host: Control = _main.get("host") as Control
			if host == null or host.get_child_count() == 0:
				_fail("找不到 host 或 battle 節點")
				quit(1)
				return true
			_battle = host.get_child(0)

			# 2. 驗證 PlayerName 與 EnemyName 樣式
			var pn: Label = _battle.get_node_or_null("%PlayerName")
			var en: Label = _battle.get_node_or_null("%EnemyName")
			_assert(pn != null, "PlayerName 節點存在")
			_assert(en != null, "EnemyName 節點存在")

			if pn:
				var sz = pn.get_theme_font_size("font_size")
				var out_sz = pn.get_theme_constant("outline_size")
				var sh_x = pn.get_theme_constant("shadow_offset_x")
				var sh_y = pn.get_theme_constant("shadow_offset_y")
				_assert(sz >= 18, "PlayerName 字級應 >= 18px，實際為: %d" % sz)
				_assert(out_sz >= 2, "PlayerName 描邊應 >= 2px，實際為: %d" % out_sz)
				_assert(sh_x == 0 and sh_y == 0, "PlayerName 陰影位移應為 0 防止雙層重疊，實際為: (%d, %d)" % [sh_x, sh_y])
				_assert(pn.text == "小白", "兔族 PlayerName 應為 '小白'，實際為: '%s'" % pn.text)

			if en:
				var sz = en.get_theme_font_size("font_size")
				var out_sz = en.get_theme_constant("outline_size")
				var sh_x = en.get_theme_constant("shadow_offset_x")
				var sh_y = en.get_theme_constant("shadow_offset_y")
				_assert(sz >= 18, "EnemyName 字級應 >= 18px，實際為: %d" % sz)
				_assert(out_sz >= 2, "EnemyName 描邊應 >= 2px，實際為: %d" % out_sz)
				_assert(sh_x == 0 and sh_y == 0, "EnemyName 陰影位移應為 0 防止雙層重疊，實際為: (%d, %d)" % [sh_x, sh_y])
				_assert(en.text == "荒路匪徒", "敵方 EnemyName 應為 '荒路匪徒'，實際為: '%s'" % en.text)

			var e_bandit_name = _battle.call("_unit_display_name", "road_bandit")
			_assert(e_bandit_name == "荒路匪徒", "_unit_display_name('road_bandit') 應為 '荒路匪徒'，實際為: '%s'" % e_bandit_name)

			# 3. 切換獅族戰鬥驗證
			var gs: Node = root.get_node_or_null("GameState")
			gs.call("reset_new_game", "lion")
			_main.call("proof_show_battle", "black_ronin")
			_step = 2
			_wait = 0

		2:
			if _wait < 25:
				return false
			var host: Control = _main.get("host") as Control
			_battle = host.get_child(0)
			var pn: Label = _battle.get_node_or_null("%PlayerName")
			var en: Label = _battle.get_node_or_null("%EnemyName")

			if pn:
				_assert(pn.text == "烈鬃獅", "獅族 PlayerName 應為 '烈鬃獅'，實際為: '%s'" % pn.text)
			if en:
				_assert(en.text == "黑鏽浪人", "black_ronin EnemyName 應為 '黑鏽浪人'，實際為: '%s'" % en.text)

			var p_lion = _battle.call("_unit_display_name", "player")
			_assert(p_lion == "烈鬃獅", "_unit_display_name('player') 獅族應為 '烈鬃獅'，實際為: '%s'" % p_lion)
			var e_ronin_name = _battle.call("_unit_display_name", "black_ronin")
			_assert(e_ronin_name == "黑鏽浪人", "_unit_display_name('black_ronin') 應為 '黑鏽浪人'，實際為: '%s'" % e_ronin_name)

			# 4. 驗證其餘各族開局名稱正確性
			var gs: Node = root.get_node_or_null("GameState")
			var other_races := {
				"fox": "靈尾狐",
				"boar": "鋼牙豕",
				"macaque": "靈爪猴",
				"tiger": "烈焰虎",
				"crane": "雲嵐鶴",
				"bear": "玄軸熊",
				"penguin": "蒸氣企鵝",
				"tortoise": "玄機龜",
				"elephant": "鋼岳象",
				"frog": "碧簧蛙"
			}
			for r in other_races.keys():
				gs.call("reset_new_game", r)
				var stats = BattleSim.gather_player_stats()
				_assert(str(stats.get("name")) == other_races[r], "各族 [%s] gather_player_stats 名稱應為 '%s'，實際為: '%s'" % [r, other_races[r], stats.get("name")])
				# 驗證 _unit_display_name 在 sim 為空且 player_name 為空時 fallback 各族中文名
				gs.player_name = ""
				var saved_sim = _battle.get("sim")
				_battle.set("sim", null)
				var fallback_name = _battle.call("_unit_display_name", "player")
				_assert(fallback_name == other_races[r], "各族 [%s] _unit_display_name 備援名稱應為 '%s'，實際為: '%s'" % [r, other_races[r], fallback_name])
				_battle.set("sim", saved_sim)

			# 5. 驗證 hit 事件日誌不洩漏 id
			_battle.call("_on_event", "hit", {
				"attacker": "player",
				"defender": "black_ronin",
				"damage": 40,
				"crit": false,
				"hp": 40,
				"max_hp": 75
			})
			_battle.call("_on_event", "hit", {
				"attacker": "black_ronin",
				"defender": "player",
				"damage": 11,
				"crit": false,
				"hp": 43,
				"max_hp": 50
			})
			_battle.call("_on_event", "hit", {
				"attacker": "road_bandit",
				"defender": "player",
				"damage": 7,
				"crit": false,
				"hp": 36,
				"max_hp": 50
			})

			var history: Array = _battle.get("_log_history")
			var full_log_text := " ".join(history)
			print("  全域戰鬥日誌內容: ", full_log_text)
			_assert(not ("player 造成" in full_log_text), "日誌不應包含洩漏的 'player 造成'")
			_assert(not ("road_bandit 造成" in full_log_text), "日誌不應包含洩漏的 'road_bandit 造成'")
			_assert(not ("black_ronin 造成" in full_log_text), "日誌不應包含洩漏的 'black_ronin 造成'")
			_assert("造成 40 傷害" in full_log_text, "日誌應包含造成 40 傷害")
			_assert("造成 11 傷害" in full_log_text, "日誌應包含造成 11 傷害")
			_assert("造成 7 傷害" in full_log_text, "日誌應包含造成 7 傷害")
			_assert("烈鬃獅 造成 40 傷害" in full_log_text, "日誌應包含 '烈鬃獅 造成 40 傷害'")
			_assert("黑鏽浪人 造成 11 傷害" in full_log_text, "日誌應包含 '黑鏽浪人 造成 11 傷害'")
			_assert("荒路匪徒 造成 7 傷害" in full_log_text, "日誌應包含 '荒路匪徒 造成 7 傷害'")

			if _ok:
				print("TEST_QA_BATTLE_NAME_FIXES_OK")
				quit(0)
			else:
				print("TEST_QA_BATTLE_NAME_FIXES_FAIL")
				quit(1)
			return true
	return false
