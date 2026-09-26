extends SceneTree
## 停擺巨偶蓄力必殺與發條格擋單元測試 (test_colossus_windup_parry.gd)
## 依據任務 t_efaa460d 驗收規範：
## 1. colossus 模式蓄力時格擋窗為開（前搖 1.85s，格擋窗 0.85s，時間模型鎖定）
## 2. 成功格擋後走既有完美格擋，鎖定部位 hp 下降或已破壞（掉落鐵屑，不准新道具）
## 3. 右下按鈕文案在巨偶蓄力時顯示「發條格擋」，按鈕高度 >= 50px
## 4. 普通關卡雜魚戰不出現「發條格擋」四字
## 5. 六語系 ui.json 包含「發條格擋」（英 Windup Parry、日 ぜんまいパリィ等），零系統 emoji
## 6. 遵守 0-QA27：第三隻巨偶中文名對齊「黑鏽蒸氣巨象」，enemy.json 與 ui.json 六語系同名

const BattleSimClass = preload("res://scripts/battle/battle_sim.gd")
const ContentLocClass = preload("res://scripts/systems/content_loc.gd")
const WorldContentClass = preload("res://scripts/world/world_content.gd")

var _ok := true
var _step := 0
var _wait := 0
var _battle_view: Control = null
var _normal_view: Control = null

func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false

func _has_emoji(s: String) -> bool:
	for ch in s:
		var code := ch.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
			return true
	return false

func _initialize() -> void:
	print("=== 開始 test_colossus_windup_parry 測試 ===")
	root.size = Vector2i(1280, 720)

	var player_stats := {
		"name": "小白",
		"max_hp": 150,
		"hp": 150,
		"atk": 25,
		"def": 12,
		"speed": 11.0,
	}

	var boss_modes := ["colossus_lion", "colossus_puppet", "colossus_elephant"]

	# 1. 驗證三隻巨偶蓄力必殺與既有格擋窗開啟 (1.85s / 0.85s)
	print("--- 1. 驗證三隻停擺巨偶蓄力必殺與格擋窗 (1.85s / 0.85s) ---")
	for bk in boss_modes:
		var sim = BattleSimClass.make_world_fight(player_stats, bk)
		if sim == null:
			_fail("無法建立巨偶戰鬥實例: %s" % bk)
			continue
		var boss = sim.get_unit(bk)
		if boss == null:
			_fail("戰鬥缺少敵方 Boss 單位: %s" % bk)
			continue

		# 初始狀態：未蓄力，格擋窗為關
		if sim.parry_window_open():
			_fail("[%s] 戰鬥剛開始未蓄力時格擋窗不應為開" % bk)

		# 觸發蓄力必殺
		var triggered = sim.trigger_colossus_windup()
		if not triggered or not boss.telegraph_active:
			_fail("[%s] 巨偶蓄力必殺未能成功啟動" % bk)

		# 剛進入前搖（1.85s），在 0.85s 前，格擋窗應為關
		if absf(boss.state_timer - 1.85) > 0.05:
			_fail("[%s] 巨偶蓄力前搖時間應為 1.85s，實際: %.2f" % [bk, boss.state_timer])

		if sim.parry_window_open():
			_fail("[%s] 前搖前段 (1.85s) 格擋窗應關閉" % bk)

		# 步進時間進入格擋窗（<= 0.85s）
		boss.state_timer = 0.80
		if not sim.parry_window_open():
			_fail("[%s] 進入 0.85s 格擋窗後 parry_window_open 應為 true" % bk)

		print("  ✓ [%s] 巨偶蓄力與格擋窗運作正常 (前搖: %.2fs, 格擋窗開啟: %s)" % [
			bk, 1.85, str(sim.parry_window_open())
		])

	# 2. 驗證完美格擋與部位破壞 (掉落鐵屑，不准新道具)
	print("--- 2. 驗證成功格擋走完美格擋與部位破壞 ---")
	for bk in boss_modes:
		var sim = BattleSimClass.make_world_fight(player_stats, bk)
		var boss = sim.get_unit(bk)

		# 確保有鎖定部位
		sim.focus_part_id = "core"
		var initial_part_hp := 0
		for p in boss.parts:
			if str(p.get("id")) == "core":
				initial_part_hp = int(p.get("hp", 0))
				break

		# 巨偶蓄力並進入格擋窗
		sim.trigger_colossus_windup()
		boss.state_timer = 0.50 # 在 0.85s 窗內

		# 執行反應格擋
		var parried = sim.try_react()
		if not parried:
			_fail("[%s] 在格擋窗內按下格擋應成功" % bk)

		# 檢查鎖定部位 hp 下降或已破
		var post_part_hp := 0
		var part_broken := false
		for p in boss.parts:
			if str(p.get("id")) == "core":
				post_part_hp = int(p.get("hp", 0))
				part_broken = bool(p.get("broken", false))
				break

		if post_part_hp >= initial_part_hp and not part_broken:
			_fail("[%s] 成功格擋後鎖定部位 hp 應下降或已破壞 (初始: %d, 結算: %d)" % [
				bk, initial_part_hp, post_part_hp
			])

		# 檢查掉落物：只准 iron_scrap
		for mat in sim.pending_part_materials:
			if mat != "iron_scrap":
				_fail("[%s] 部位掉落物應為 iron_scrap，發現非法道具: %s" % [bk, mat])

		print("  ✓ [%s] 完美格擋成功，部位受到傷害 (HP: %d -> %d, broken: %s)" % [
			bk, initial_part_hp, post_part_hp, str(part_broken)
		])

	# 5. 驗證六語系詞條與零系統 emoji
	print("--- 5. 驗證六語系詞條 (ui.json) 與零系統 emoji ---")
	var expected_parry_i18n := {
		"zh_TW": "發條格擋",
		"zh_CN": "发条格挡",
		"en": "Windup Parry",
		"ja": "ぜんまいパリィ",
		"ko": "태엽 패링",
		"es": "Parada de Cuerda",
	}

	var loc_node = root.get_node_or_null("Loc")
	for loc_code in expected_parry_i18n.keys():
		if loc_node:
			loc_node.set("locale", loc_code)
		ContentLocClass.reload()
		var txt = ContentLocClass.text("ui", "發條格擋")
		var exp = expected_parry_i18n[loc_code]
		if txt != exp:
			_fail("[%s] 發條格擋譯名不符: 預期 '%s'，實際 '%s'" % [loc_code, exp, txt])
		if _has_emoji(txt):
			_fail("[%s] 詞條含有系統 emoji: %s" % [loc_code, txt])
		print("  ✓ [%s] 發條格擋譯名合規: '%s' (零 emoji)" % [loc_code, txt])

	# 6. 驗證 0-QA27 對齊（第三隻中文名黑鏽蒸氣巨象，enemy.json 與 ui.json 六語系同名）
	print("--- 6. 驗證 0-QA27 對齊（黑鏽蒸氣巨象，六語系同名）---")
	var expected_elephant_i18n := {
		"zh_TW": "黑鏽蒸氣巨象",
		"zh_CN": "黑锈蒸气巨象",
		"en": "Black-Rust Steam Colossus",
		"ja": "黒錆の蒸気巨象",
		"ko": "검은녹 증기 거상",
		"es": "Coloso de Vapor de Óxido Negro",
	}

	for loc_code in expected_elephant_i18n.keys():
		if loc_node:
			loc_node.set("locale", loc_code)
		ContentLocClass.reload()
		var ui_name = ContentLocClass.text("ui", "黑鏽蒸氣巨象")
		var enemy_name = ContentLocClass.t("enemy", "colossus_elephant", "name", "黑鏽蒸氣巨象")
		var exp_name = expected_elephant_i18n[loc_code]
		if ui_name != exp_name:
			_fail("[%s] 0-QA27 ui.json 巨象名稱不符: 預期 '%s'，實際 '%s'" % [loc_code, exp_name, ui_name])
		if enemy_name != exp_name:
			_fail("[%s] 0-QA27 enemy.json 巨象名稱不符: 預期 '%s'，實際 '%s'" % [loc_code, exp_name, enemy_name])
		if ui_name != enemy_name:
			_fail("[%s] 0-QA27 ui.json 與 enemy.json 名稱未同名！ui='%s', enemy='%s'" % [loc_code, ui_name, enemy_name])
		print("  ✓ [%s] 0-QA27 巨象六語系同名完全一致: '%s'" % [loc_code, ui_name])

	# 恢復繁中
	if loc_node:
		loc_node.set("locale", "zh_TW")
	ContentLocClass.reload()

	_step = 1
	_wait = 0

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 3. 驗證 BattleView 巨偶蓄力時格擋按鈕文案「發條格擋」且高度 >= 50px
			print("--- 3. 驗證 BattleView 巨偶蓄力按鈕文案與高度 ---")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			if b_scn == null:
				_fail("無法載入 res://scenes/battle/battle.tscn")
				_step = 99
				return false
			_battle_view = b_scn.instantiate()
			root.add_child(_battle_view)
			_battle_view.call("setup", "colossus_lion")
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			var thumb_controls: Dictionary = _battle_view.call("thumb_controls")
			var attack_btn: Button = thumb_controls.get("attack") as Button
			if attack_btn == null:
				_fail("BattleView 未找到 attack 按鈕")
			else:
				if attack_btn.custom_minimum_size.y < 50.0:
					_fail("格擋按鈕高度小於 50px: %.1f" % attack_btn.custom_minimum_size.y)
				print("  ✓ 格擋按鈕高度符合規範: %.1fpx >= 50px" % attack_btn.custom_minimum_size.y)

				# 平常狀態應為「攻擊」
				if attack_btn.text != "攻擊":
					_fail("平常狀態按鈕文案應為『攻擊』，實際: %s" % attack_btn.text)

				# 巨偶蓄力狀態
				var b_sim: Object = _battle_view.get("sim")
				var lion = b_sim.call("get_unit", "colossus_lion")
				b_sim.call("trigger_colossus_windup")
				_battle_view.call("_update_parry_countdown", lion)

				if attack_btn.text != "發條格擋":
					_fail("巨偶蓄力時按鈕文案應改為『發條格擋』，實際: %s" % attack_btn.text)
				print("  ✓ 巨偶蓄力時橫屏按鈕文案正確顯示『%s』" % attack_btn.text)

			_battle_view.queue_free()
			_battle_view = null

			# 4. 驗證普通關卡雜魚戰不出現「發條格擋」
			print("--- 4. 驗證普通關卡雜魚戰不出現『發條格擋』 ---")
			var b_scn2: PackedScene = load("res://scenes/battle/battle.tscn")
			_normal_view = b_scn2.instantiate()
			root.add_child(_normal_view)
			_normal_view.call("setup", "black_ronin")
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			var normal_attack_btn: Button = _normal_view.call("thumb_controls").get("attack") as Button
			if normal_attack_btn.text == "發條格擋":
				_fail("普通關卡雜魚戰不應出現『發條格擋』按鈕！")
			if normal_attack_btn.text != "攻擊":
				_fail("普通關卡雜魚戰按鈕應為『攻擊』，實際: %s" % normal_attack_btn.text)
			print("  ✓ 普通關卡雜魚戰按鈕為『%s』，零『發條格擋』" % normal_attack_btn.text)
			_normal_view.queue_free()
			_normal_view = null
			_step = 4
		4:
			if _ok:
				print("TEST_COLOSSUS_WINDUP_PARRY_OK")
				quit(0)
			else:
				print("TEST_COLOSSUS_WINDUP_PARRY_FAIL")
				quit(1)
	return false
