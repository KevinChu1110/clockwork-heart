extends SceneTree
## 戰鬥頂欄鎖定提示與 HUD 水平排版多語系驗收測試 (test_battle_hud_overflow_i18n.gd)
##
## 驗證：
## 1. 英文 (en) 及長譯代表語系 (es, ja, ko) 與繁中 (zh_TW) 進入戰鬥 (Boss Leo)
## 2. 頂欄 SideBars 在 1280 橫屏內不溢出畫面：
##    - SideBars.global_position.x >= 0
##    - SideBars.global_position.x + SideBars.size.x <= 1280
## 3. 左側玩家 HUD (角色名、HP 標籤、HP 條) 完整可見，不被左邊界裁切 (x >= 0)
## 4. 右側 Boss HUD (名稱、HP 標籤、HP 條、部位面板) 完整可見，不被右邊界裁切 (right_edge <= 1280)
## 5. 部位破壞與鎖定提示功能正常，提示字串無系統 emoji

const LOCALES_TO_TEST := ["en", "es", "ja", "ko", "zh_TW"]
const SCREEN_WIDTH := 1280.0

var _ok := true
var _frame := 0

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win != null:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		return false
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_battle_hud_overflow_i18n 測試 ===")

	var root_node = root
	if not root_node.has_node("GameFont"):
		var gf_cls = load("res://scripts/autoload/game_font.gd")
		if gf_cls:
			var gf = gf_cls.new()
			gf.name = "GameFont"
			root_node.add_child(gf)

	var loc_node: Node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	var gs: Node = root_node.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root_node.add_child(gs)

	var battle_scene = load("res://scenes/battle/battle.tscn")
	if battle_scene == null:
		_fail("找不到 res://scenes/battle/battle.tscn")
		return

	for loc in LOCALES_TO_TEST:
		print("\n--- 驗證語系: %s ---" % loc)
		loc_node.call("set_locale", loc)
		gs.call("reset_new_game")
		gs.set("player_race", "rabbit")
		gs.set("player_name", "小白")
		gs.set("chapter", "c1")
		gs.set("level", 10)
		gs.set("gold", 1000)

		var battle = battle_scene.instantiate()
		root_node.add_child(battle)
		battle.call("setup", "leo")

		var sim = battle.get("sim")
		if sim == null:
			_fail("[%s] battle sim 為 null" % loc)
			battle.queue_free()
			continue

		var boss = sim.call("_primary_boss_unit")
		if boss and boss.parts.size() >= 2:
			boss.parts[0]["broken"] = false
			boss.parts[0]["hp"] = boss.parts[0]["max_hp"]
			boss.parts[1]["broken"] = true
			boss.parts[1]["hp"] = 0
			sim.parts_break_unlocked = true
			sim.parts_break_stage = 1
			sim.focus_part_id = boss.parts[0].get("id", "helm")
			if battle.has_method("_refresh_part_bars"):
				battle.call("_refresh_part_bars", boss)
			if battle.has_method("_refresh_part_focus_hint"):
				battle.call("_refresh_part_focus_hint")
			if battle.has_method("_refresh_hud"):
				battle.call("_refresh_hud")

		# 等待 2 幀讓 Viewport / Container 排版計算完成
		for _i in range(2):
			await process_frame

		var sb = battle.get_node("SideBars") as Control
		var ps = battle.get_node("SideBars/PlayerSide") as Control
		var ch = battle.get_node("SideBars/CenterHint") as Control
		var es = battle.get_node("SideBars/EnemySide") as Control
		var ph = battle.get_node("%ParryHint") as Label
		var pn = battle.get_node("%PlayerName") as Label
		var php = battle.get_node("%PlayerHP") as Control
		var en = battle.get_node("%EnemyName") as Label
		var ehp = battle.get_node("%EnemyHP") as Control

		# 1. 檢驗 SideBars 水平邊界
		var sb_x: float = sb.global_position.x
		var sb_right: float = sb_x + sb.size.x
		print("  SideBars: pos=(%.1f, %.1f), size=(%.1f, %.1f), right=%.1f" % [sb_x, sb.global_position.y, sb.size.x, sb.size.y, sb_right])

		if sb_x < 0.0:
			_fail("[%s] SideBars 向左溢出 (x=%.1f < 0)" % [loc, sb_x])
		elif sb_x < 16.0:
			_fail("[%s] SideBars 左邊距過小 (x=%.1f < 16)" % [loc, sb_x])
		else:
			print("  [PASS] SideBars 左邊距安全 (x=%.1f >= 16)" % sb_x)

		if sb_right > SCREEN_WIDTH:
			_fail("[%s] SideBars 向右溢出 (right=%.1f > %.1f)" % [loc, sb_right, SCREEN_WIDTH])
		elif sb_right > SCREEN_WIDTH - 16.0:
			_fail("[%s] SideBars 右邊距過小 (right=%.1f > %.1f)" % [loc, sb_right, SCREEN_WIDTH - 16.0])
		else:
			print("  [PASS] SideBars 右邊距安全 (right=%.1f <= %.1f)" % [sb_right, SCREEN_WIDTH - 16.0])

		# 2. 檢驗左側 PlayerSide 完整可見
		var ps_x: float = ps.global_position.x
		var pn_x: float = pn.global_position.x
		var php_x: float = php.global_position.x
		if ps_x < 0.0 or pn_x < 0.0 or php_x < 0.0:
			_fail("[%s] 玩家 HUD 被左邊界截斷 (ps_x=%.1f, pn_x=%.1f, php_x=%.1f)" % [loc, ps_x, pn_x, php_x])
		else:
			print("  [PASS] 玩家 HUD 完整在畫面內 (x=%.1f)" % ps_x)

		# 3. 檢驗右側 EnemySide 完整可見
		var es_right: float = es.global_position.x + es.size.x
		var en_right: float = en.global_position.x + en.size.x
		var ehp_right: float = ehp.global_position.x + ehp.size.x
		if es_right > SCREEN_WIDTH or en_right > SCREEN_WIDTH or ehp_right > SCREEN_WIDTH:
			_fail("[%s] 敵方 HUD 被右邊界截斷 (es_right=%.1f, en_right=%.1f, ehp_right=%.1f)" % [loc, es_right, en_right, ehp_right])
		else:
			print("  [PASS] 敵方 HUD 完整在畫面內 (right=%.1f)" % es_right)

		# 4. 檢驗鎖定提示無 emoji
		if _has_emoji(ph.text):
			_fail("[%s] ParryHint 含有系統 emoji: %s" % [loc, ph.text])
		else:
			print("  [PASS] 鎖定提示零 emoji: '%s'" % ph.text)

		battle.queue_free()

	if _ok:
		print("\n=======================================================")
		print("TEST_BATTLE_HUD_OVERFLOW_I18N_OK")
		quit(0)
	else:
		push_error("TEST_BATTLE_HUD_OVERFLOW_I18N_FAIL")
		print("TEST_BATTLE_HUD_OVERFLOW_I18N_FAIL")
		quit(1)
