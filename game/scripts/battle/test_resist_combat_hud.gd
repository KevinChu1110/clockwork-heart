extends SceneTree
## 抗性吃力／過載戰鬥場上顯示受傷加深 單元測試 (test_resist_combat_hud.gd)

const ContentLocClass = preload("res://scripts/systems/content_loc.gd")
const FormulasClass = preload("res://scripts/battle/formulas.gd")

var _loc_node: Node = null
var _gs: Node = null
var _battle: Control = null
var _step := 0
var _wait := 0

func _initialize() -> void:
	print("=== 開始驗證抗性吃力/過載戰鬥場上受傷加深 HUD ===")
	root.size = Vector2i(1280, 720)

	_loc_node = root.get_node_or_null("Loc")
	if _loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			_loc_node = LocClass.new()
			_loc_node.name = "Loc"
			root.add_child(_loc_node)

	_gs = root.get_node_or_null("GameState")
	if _gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			_gs = GsClass.new()
			_gs.name = "GameState"
			root.add_child(_gs)

	if _gs:
		_gs.call("reset_new_game", "rabbit")
		_gs.set("player_name", "小白")
		_gs.set("level", 10)

	_test_damage_mult_and_format_logic()
	_test_six_locales()
	_test_timings_and_formulas_untouched()

	_step = 1
	_wait = 0

func _test_damage_mult_and_format_logic() -> void:
	print("--- 1. 驗證倍率與提示對應邏輯 ---")
	var BattleViewClass = load("res://scripts/battle/battle_view.gd")

	# 達標 / 安全檔
	var m_safe1: float = FormulasClass.underlevel_damage_multiplier(10, 10)
	var m_safe2: float = FormulasClass.underlevel_damage_multiplier(15, 10)
	var m_safe3: float = FormulasClass.underlevel_damage_multiplier(5, 0)
	assert(abs(m_safe1 - 1.0) < 0.001, "達標倍率應為 1.0")
	assert(abs(m_safe2 - 1.0) < 0.001, "超標倍率應為 1.0")
	assert(abs(m_safe3 - 1.0) < 0.001, "未設建議等級倍率應為 1.0")

	# 繁中環境下
	if _loc_node: _loc_node.call("set_locale", "zh_TW")
	ContentLocClass.reload()
	assert(BattleViewClass.call("format_underlevel_vulnerability", m_safe1) == "", "安全檔應無提示 (回傳空字串)")
	assert(BattleViewClass.call("format_underlevel_vulnerability", 1.0) == "", "1.0 應無提示")

	# 吃力檔：差 1–4 級
	for diff in [1, 2, 3, 4]:
		var m: float = FormulasClass.underlevel_damage_multiplier(10, 10 + diff)
		assert(abs(m - 1.2) < 0.001, "差 %d 級倍率應為 1.2" % diff)
		var txt: String = BattleViewClass.call("format_underlevel_vulnerability", m)
		assert(txt == "吃力 · 受傷 ×1.2", "差 %d 級提示應為 '吃力 · 受傷 ×1.2', got '%s'" % [diff, txt])
	print("  ✓ 差 1–4 級 (×1.2) 提示正確: 吃力 · 受傷 ×1.2")

	# 過載檔：差 >= 5 級
	for diff in [5, 6, 10]:
		var m: float = FormulasClass.underlevel_damage_multiplier(10, 10 + diff)
		assert(abs(m - 1.5) < 0.001, "差 %d 級倍率應為 1.5" % diff)
		var txt: String = BattleViewClass.call("format_underlevel_vulnerability", m)
		assert(txt == "過載 · 受傷 ×1.5", "差 %d 級提示應為 '過載 · 受傷 ×1.5', got '%s'" % [diff, txt])
	print("  ✓ 差 >= 5 級 (×1.5) 提示正確: 過載 · 受傷 ×1.5")
	print("  ✓ 達標 ×1.0 安全檔無提示 (避免多餘字)")

func _test_six_locales() -> void:
	print("--- 2. 驗證六語系沿用既有譯名與切語系即時刷新 ---")
	var BattleViewClass = load("res://scripts/battle/battle_view.gd")

	var expected := {
		"zh_TW": { "strain": "吃力 · 受傷 ×1.2", "overload": "過載 · 受傷 ×1.5" },
		"en": { "strain": "Strained · Dmg ×1.2", "overload": "Overload · Dmg ×1.5" },
		"zh_CN": { "strain": "吃力 · 受伤 ×1.2", "overload": "过载 · 受伤 ×1.5" },
		"ja": { "strain": "苦戦 · 被ダメ ×1.2", "overload": "過負荷 · 被ダメ ×1.5" },
		"ko": { "strain": "버거움 · 받는 피해 ×1.2", "overload": "과부하 · 받는 피해 ×1.5" },
		"es": { "strain": "Difícil · Daño ×1.2", "overload": "Sobrecarga · Daño ×1.5" },
	}

	for loc in expected.keys():
		if _loc_node: _loc_node.call("set_locale", loc)
		ContentLocClass.reload()
		var s_txt: String = BattleViewClass.call("format_underlevel_vulnerability", 1.2)
		var o_txt: String = BattleViewClass.call("format_underlevel_vulnerability", 1.5)
		var safe_txt: String = BattleViewClass.call("format_underlevel_vulnerability", 1.0)
		assert(s_txt == expected[loc]["strain"], "[%s] 吃力提示應為 '%s', 實測得 '%s'" % [loc, expected[loc]["strain"], s_txt])
		assert(o_txt == expected[loc]["overload"], "[%s] 過載提示應為 '%s', 實測得 '%s'" % [loc, expected[loc]["overload"], o_txt])
		assert(safe_txt == "", "[%s] 安全檔應為空字串, 實測得 '%s'" % [loc, safe_txt])
		# 檢查無 emoji
		for txt in [s_txt, o_txt]:
			for i in range(txt.length()):
				var code: int = txt.unicode_at(i)
				assert(code < 0x1F300 or code > 0x1FAFF, "[%s] 提示禁止包含 emoji: %s" % [loc, txt])
		print("  ✓ [%s] 易傷提示合規: '%s' / '%s' (安全檔無文字, 零 emoji)" % [loc, s_txt, o_txt])

	# 恢復繁中
	if _loc_node: _loc_node.call("set_locale", "zh_TW")
	ContentLocClass.reload()

func _test_timings_and_formulas_untouched() -> void:
	print("--- 4. 驗證戰鬥秒數、公式零更動 ---")
	var BattleSimClass = load("res://scripts/battle/battle_sim.gd")
	assert(abs(BattleSimClass.KING_SLASH_WINDUP - 1.85) < 0.001, "前搖時間必須維持 1.85s")
	assert(abs(BattleSimClass.PARRY_WINDOW - 0.85) < 0.001, "格擋窗口必須維持 0.85s")
	assert(abs(FormulasClass.boss_telegraph_sec() - 1.85) < 0.001, "Formulas 前搖時間必須為 1.85s")
	assert(abs(FormulasClass.boss_parry_window_sec() - 0.85) < 0.001, "Formulas 格擋窗口必須為 0.85s")

	# 驗證傷害計算公式
	var d_safe: int = FormulasClass.apply_underlevel_damage(20, 1.0)
	var d_strain: int = FormulasClass.apply_underlevel_damage(20, 1.2)
	var d_over: int = FormulasClass.apply_underlevel_damage(20, 1.5)
	assert(d_safe == 20, "20 x 1.0 應為 20")
	assert(d_strain == 24, "20 x 1.2 應為 24")
	assert(d_over == 30, "20 x 1.5 應為 30")
	print("  ✓ 戰鬥秒數 (1.85s / 0.85s) 與傷害計算完全無改動")

func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 實例化戰鬥畫面
			if _wait == 2:
				print("--- 3. 驗證戰鬥視圖節點狀態與安全邊距 ---")
				var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
				assert(b_scn != null, "battle.tscn 必須存在")
				_battle = b_scn.instantiate()
				root.add_child(_battle)
				_battle.call("setup", "wolf")
			elif _wait == 6:
				var notice: Label = _battle.get_node_or_null("%ResistNotice") as Label
				assert(notice != null, "%ResistNotice 必須存在")
				var sim: Object = _battle.get("sim")
				assert(sim != null, "sim 必須建立")
				var player_unit: BattleUnit = sim.call("get_unit", "player")
				assert(player_unit != null, "player unit 必須存在")

				# 1. 達標 / 安全檔 (mult = 1.0)
				player_unit.underlevel_damage_mult = 1.0
				_battle.call("_refresh_hud")
				assert(not notice.visible, "安全檔時 notice.visible 必須為 false")
				assert(notice.text == "", "安全檔時 notice.text 必須為空")
				print("  ✓ 安全檔時 ResistNotice 隱藏且不佔空間 (visible=false, text='')")

				# 2. 吃力檔 (mult = 1.2)
				player_unit.underlevel_damage_mult = 1.2
				_battle.call("_refresh_hud")
				assert(notice.visible, "吃力檔時 notice.visible 必須為 true")
				assert(notice.text == "吃力 · 受傷 ×1.2", "吃力檔文字必須為 '吃力 · 受傷 ×1.2', got '%s'" % notice.text)
				print("  ✓ 吃力檔時 ResistNotice 顯示: '吃力 · 受傷 ×1.2'")

				# 3. 過載檔 (mult = 1.5)
				player_unit.underlevel_damage_mult = 1.5
				_battle.call("_refresh_hud")
				assert(notice.visible, "過載檔時 notice.visible 必須為 true")
				assert(notice.text == "過載 · 受傷 ×1.5", "過載檔文字必須為 '過載 · 受傷 ×1.5', got '%s'" % notice.text)
				print("  ✓ 過載檔時 ResistNotice 顯示: '過載 · 受傷 ×1.5'")

				# 4. 切語系即時刷新
				if _loc_node: _loc_node.call("set_locale", "en")
				ContentLocClass.reload()
				_battle.call("_on_locale_changed", "en")
				assert(notice.visible, "切語系後過載檔 notice 仍為 visible")
				assert(notice.text == "Overload · Dmg ×1.5", "切語系至 en 時 notice 應即時更新為 'Overload · Dmg ×1.5', got '%s'" % notice.text)
				print("  ✓ 切換至 en 時 ResistNotice 即時更新為: 'Overload · Dmg ×1.5'")

				# 5. 英文下切回安全檔
				player_unit.underlevel_damage_mult = 1.0
				_battle.call("_refresh_hud")
				assert(not notice.visible, "英文安全檔時 notice.visible 必須為 false")
				assert(notice.text == "", "英文安全檔時 notice.text 必須為空")
				print("  ✓ 英文安全檔時 ResistNotice 隱藏且不佔空間")

				# 恢復繁中
				if _loc_node: _loc_node.call("set_locale", "zh_TW")
				ContentLocClass.reload()

				_battle.queue_free()
				_battle = null

				print("=== 全部測試通過 TEST_RESIST_COMBAT_HUD_OK ===")
				quit(0)
				return true
	return false
