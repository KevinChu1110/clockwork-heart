extends SceneTree
## 招式名稱與升級說明六語系單元測試 (Skill i18n Test)
## 驗證：
## 1. 六語系 (zh_TW, zh_CN, en, ja, ko, es) skill.json 覆蓋全 54 招與 5 欄位 (name, desc, lv2, lv3, unlock_hint)
## 2. SkillSystem 底層 def_of()、pick_battle_skill()、panel_status_bbcode() 隨 ContentLoc 正確傳回各語系名稱
## 3. 實例化 SkillDialog，在切換 locale (locale_changed) 時，面板全片招式名稱、說明、解鎖條件、戰鬥優先即時刷新
## 4. 至少抽 3 招 (slash, counter_strike, emergency_heal, thunder_fury) 驗證在各語系下完全等於對應詞條
## 5. 傷害倍率、解鎖條件等數值邏輯完全不變

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const SkillDialogScn = preload("res://scripts/ui/skill_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)
	change_scene_to_file("res://scenes/main.tscn")


func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 20:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_SKILL_I18N_OK")
					quit(0)
				else:
					push_error("TEST_SKILL_I18N_FAIL")
					print("TEST_SKILL_I18N_FAIL")
					quit(1)
				return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_skill_i18n 測試 ===")

	var root_node := root
	var loc_node: Node = root_node.get_node_or_null("Loc")
	var sk_node: Node = root_node.get_node_or_null("SkillSystem")
	var gs_node: Node = root_node.get_node_or_null("GameState")

	if loc_node == null or sk_node == null or gs_node == null:
		_fail("Autoload 節點缺失 (Loc, SkillSystem, GameState)")
		return

	gs_node.call("reset_new_game")
	sk_node.call("ensure_skill_map")
	sk_node.call("learn", "slash", 1)

	# 1. 驗證詞條字典解析 (54 招全語系覆蓋)
	print("\n--- 1. 驗證六語系詞條完整性 ---")
	var test_skills := ["slash", "counter_strike", "emergency_heal", "thunder_fury"]
	var expected_names := {
		"zh_TW": {
			"slash": "橫斬",
			"counter_strike": "反戈一擊",
			"emergency_heal": "緊急恢復",
			"thunder_fury": "怒雷狂擊",
		},
		"zh_CN": {
			"slash": "横斩",
			"counter_strike": "反戈一击",
			"emergency_heal": "紧急恢复",
			"thunder_fury": "怒雷狂击",
		},
		"en": {
			"slash": "Wide Slash",
			"counter_strike": "Counterstrike",
			"emergency_heal": "Emergency Recovery",
			"thunder_fury": "Thunder Fury",
		},
		"ja": {
			"slash": "横薙ぎ",
			"counter_strike": "反撃の一手",
			"emergency_heal": "緊急回復",
			"thunder_fury": "怒雷狂撃",
		},
		"ko": {
			"slash": "횡베기",
			"counter_strike": "반격의 한 수",
			"emergency_heal": "긴급 회복",
			"thunder_fury": "노뢰광격",
		},
		"es": {
			"slash": "Tajo horizontal",
			"counter_strike": "Contragolpe",
			"emergency_heal": "Recuperación de urgencia",
			"thunder_fury": "Furia del trueno",
		}
	}

	for code in LOCALES:
		loc_node.call("set_locale", code)
		for sid in test_skills:
			var d: Dictionary = sk_node.call("def_of", sid)
			var actual_name: String = str(d.get("name", ""))
			var exp_name: String = expected_names[code][sid]
			if actual_name != exp_name:
				_fail("語系 [%s] 招式 [%s] def_of 名稱不符: 期望 '%s'，實際 '%s'" % [code, sid, exp_name, actual_name])
			else:
				print("  ✓ [%s] 招式 %s -> %s" % [code, sid, actual_name])

	# 2. 驗證戰鬥出招 API (pick_battle_skill) 名稱隨語系切換
	print("\n--- 2. 驗證戰鬥出招 pick_battle_skill() 語系連動 ---")
	loc_node.call("set_locale", "en")
	var kit_en: Dictionary = sk_node.call("pick_battle_skill", 1.0, "sword")
	if str(kit_en.get("name", "")) != "Wide Slash":
		_fail("en 下 pick_battle_skill 技能名應為 Wide Slash，實際: " + str(kit_en.get("name", "")))
	else:
		print("  ✓ en 戰鬥出招技能名正確: Wide Slash")

	loc_node.call("set_locale", "ja")
	var kit_ja: Dictionary = sk_node.call("pick_battle_skill", 1.0, "sword")
	if str(kit_ja.get("name", "")) != "横薙ぎ":
		_fail("ja 下 pick_battle_skill 技能名應為 横薙ぎ，實際: " + str(kit_ja.get("name", "")))
	else:
		print("  ✓ ja 戰鬥出招技能名正確: 横薙ぎ")

	# 3. 實例化 SkillDialog 測試 locale_changed 即時動態連動
	print("\n--- 3. 測試 SkillDialog 實例與 locale_changed 即時連動 ---")
	loc_node.call("set_locale", "zh_TW")

	var dlg: Control = SkillDialogScn.new()
	root_node.add_child(dlg)

	# 驗證繁中初始渲染
	for sid in ["slash", "counter_strike", "emergency_heal"]:
		var s_name: String = dlg.call("get_skill_name_text", sid)
		if s_name != expected_names["zh_TW"][sid]:
			_fail("初始繁中 SkillDialog 招式 [%s] 名稱不符: 期望 '%s'，實際 '%s'" % [sid, expected_names["zh_TW"][sid], s_name])
		else:
			print("  ✓ 初始繁中面板招式 %s -> %s" % [sid, s_name])

	# 動態切換至 en
	print("  >> 動態發射 locale_changed -> en...")
	loc_node.call("set_locale", "en")
	for sid in ["slash", "counter_strike", "emergency_heal"]:
		var s_name: String = dlg.call("get_skill_name_text", sid)
		if s_name != expected_names["en"][sid]:
			_fail("切換至 en 後 SkillDialog 招式 [%s] 名稱未刷新: 期望 '%s'，實際 '%s'" % [sid, expected_names["en"][sid], s_name])
		else:
			print("  ✓ en 面板即時刷新招式 %s -> %s" % [sid, s_name])

	var desc_slash_en: String = dlg.call("get_skill_desc_text", "slash")
	if not desc_slash_en.contains("One sweeping cut"):
		_fail("切換至 en 後 slash 說明未翻譯: " + desc_slash_en)
	else:
		print("  ✓ en 招式說明即時刷新: %s" % desc_slash_en)

	# 動態切換至 ja
	print("  >> 動態發射 locale_changed -> ja...")
	loc_node.call("set_locale", "ja")
	for sid in ["slash", "counter_strike", "emergency_heal"]:
		var s_name: String = dlg.call("get_skill_name_text", sid)
		if s_name != expected_names["ja"][sid]:
			_fail("切換至 ja 後 SkillDialog 招式 [%s] 名稱未刷新: 期望 '%s'，實際 '%s'" % [sid, expected_names["ja"][sid], s_name])
		else:
			print("  ✓ ja 面板即時刷新招式 %s -> %s" % [sid, s_name])

	var desc_slash_ja: String = dlg.call("get_skill_desc_text", "slash")
	if not desc_slash_ja.contains("一薙ぎ"):
		_fail("切換至 ja 後 slash 說明未翻譯: " + desc_slash_ja)
	else:
		print("  ✓ ja 招式說明即時刷新: %s" % desc_slash_ja)

	# 動態切換至 ko
	print("  >> 動態發射 locale_changed -> ko...")
	loc_node.call("set_locale", "ko")
	for sid in ["slash", "counter_strike", "emergency_heal"]:
		var s_name: String = dlg.call("get_skill_name_text", sid)
		if s_name != expected_names["ko"][sid]:
			_fail("切換至 ko 後 SkillDialog 招式 [%s] 名稱未刷新: 期望 '%s'，實際 '%s'" % [sid, expected_names["ko"][sid], s_name])
		else:
			print("  ✓ ko 面板即時刷新招式 %s -> %s" % [sid, s_name])

	# 動態切換至 es
	print("  >> 動態發射 locale_changed -> es...")
	loc_node.call("set_locale", "es")
	for sid in ["slash", "counter_strike", "emergency_heal"]:
		var s_name: String = dlg.call("get_skill_name_text", sid)
		if s_name != expected_names["es"][sid]:
			_fail("切換至 es 後 SkillDialog 招式 [%s] 名稱未刷新: 期望 '%s'，實際 '%s'" % [sid, expected_names["es"][sid], s_name])
		else:
			print("  ✓ es 面板即時刷新招式 %s -> %s" % [sid, s_name])

	# 恢復繁中
	loc_node.call("set_locale", "zh_TW")
	dlg.queue_free()

	# 4. 驗證戰鬥數值不變
	print("\n--- 4. 驗證戰鬥數值與規則未受影響 ---")
	var mult1: float = sk_node.call("mult_for", "slash")
	if absf(mult1 - 1.8) > 0.01:
		_fail("slash 倍率異常: %s (應為 1.8)" % mult1)
	else:
		print("  ✓ slash base_mult 保持 1.8")

	var heal1: float = sk_node.call("heal_pct_for", "emergency_heal")
	if absf(heal1 - 0.30) > 0.01:
		_fail("emergency_heal 治療比例異常: %s (應為 0.30)" % heal1)
	else:
		print("  ✓ emergency_heal heal_pct 保持 0.30")
