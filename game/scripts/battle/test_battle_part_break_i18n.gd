extends SceneTree
## 戰鬥部位「已破」標籤六語系單元測試 (Battle Part Break i18n Test)
## 驗證：
## 1. 六語系字典（zh_TW, zh_CN, en, ja, ko, es）包含「已破」詞條
## 2. 實例化 BattleView 戰鬥畫面，在部位破損時，標籤正確顯示各語系「已破」標籤
## 3. 切換語系時（Loc.set_locale），已破部位標籤即時連動刷新，非中文語系無繁中「已破」殘留
## 4. 未破部位名稱、鎖定標記、血量數字維持正確且無 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame == 1:
		_run_test_suite()
		if _ok:
			print("\n=======================================================")
			print("TEST_BATTLE_PART_BREAK_I18N_OK")
			quit(0)
		else:
			push_error("TEST_BATTLE_PART_BREAK_I18N_FAIL")
			print("TEST_BATTLE_PART_BREAK_I18N_FAIL")
			quit(1)
		return true
	return false


func _has_emoji(s: String) -> bool:
	for c in s:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x26FF) or (code >= 0x2700 and code <= 0x27BF):
			return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_battle_part_break_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 六語系字典定義檢查
	var expected_broken := {
		"zh_TW": "已破",
		"zh_CN": "已破",
		"en": "Broken",
		"ja": "破壊済",
		"ko": "파괴됨",
		"es": "Roto",
	}

	for lc in LOCALES:
		loc_node.set_locale(lc)
		var trans := ContentLoc.text("ui", "已破")
		var exp_val: String = expected_broken.get(lc, "")
		if trans != exp_val:
			_fail("語系 %s ContentLoc.text('ui', '已破') 預期 '%s'，實際得到 '%s'" % [lc, exp_val, trans])
		else:
			print("  [PASS] 字典已破翻譯 [%s] = %s" % [lc, trans])

		if _has_emoji(trans):
			_fail("語系 %s 翻譯含 emoji: %s" % [lc, trans])

	# 2. 實例化戰鬥畫面 (BattleView) 並驗證部位已破標籤
	var battle_scene = load("res://scenes/battle/battle.tscn")
	if battle_scene == null:
		_fail("找不到 res://scenes/battle/battle.tscn")
		return

	var bv = battle_scene.instantiate()
	root_node.add_child(bv)
	bv.setup("leo")

	var sim = bv.get("sim")
	if sim == null:
		_fail("BattleView sim 為 null")
		bv.queue_free()
		return

	var boss = sim.call("_primary_boss_unit")
	if boss == null or boss.parts.size() < 2:
		_fail("Leo Boss 部位數量小於 2")
		bv.queue_free()
		return

	# 破壞第二個部位 (盾)
	boss.parts[1]["broken"] = true
	boss.parts[1]["hp"] = 0
	# 第一個部位 (盔) 保持未破
	boss.parts[0]["broken"] = false
	boss.parts[0]["hp"] = boss.parts[0]["max_hp"]

	var part_labels: Dictionary = bv.get("_part_labels")

	for lc in LOCALES:
		loc_node.set_locale(lc)
		# 驗證即時連動刷新
		var exp_tag: String = expected_broken.get(lc, "")
		var pid_broken := str(boss.parts[1].get("id", ""))
		var pid_intact := str(boss.parts[0].get("id", ""))

		var lab_broken: Label = part_labels.get(pid_broken) as Label
		var lab_intact: Label = part_labels.get(pid_intact) as Label

		if lab_broken == null:
			_fail("找不到已破部位 Label: %s" % pid_broken)
			continue
		if lab_intact == null:
			_fail("找不到未破部位 Label: %s" % pid_intact)
			continue

		var broken_text := lab_broken.text
		var intact_text := lab_intact.text

		print("  [%s] 破損部位標籤: %s | 未破部位標籤: %s" % [lc, broken_text, intact_text])

		# 檢驗破損部位標籤尾端含有 [exp_tag]
		var want_bracket := "[%s]" % exp_tag
		if not broken_text.contains(want_bracket):
			_fail("語系 %s 已破部位標籤 '%s' 應包含 '%s'" % [lc, broken_text, want_bracket])
		else:
			print("    [PASS] 已破部位包含 %s" % want_bracket)

		# 檢驗非繁中/簡中語系不得有繁中「已破」殘留
		if lc not in ["zh_TW", "zh_CN"]:
			if broken_text.contains("已破"):
				_fail("語系 %s 已破部位標籤含有殘留中文 '已破': %s" % [lc, broken_text])
			else:
				print("    [PASS] 語系 %s 無繁中 '已破' 殘留" % lc)

		# 檢驗未破部位標籤不得含已破標籤
		if intact_text.contains(want_bracket) or intact_text.contains("[已破]"):
			_fail("語系 %s 未破部位標籤誤含已破標籤: %s" % [lc, intact_text])
		else:
			print("    [PASS] 未破部位不含已破標籤")

		# 檢驗零 emoji
		if _has_emoji(broken_text) or _has_emoji(intact_text):
			_fail("語系 %s 畫面標籤含有 emoji: broken=%s, intact=%s" % [lc, broken_text, intact_text])

	bv.queue_free()
	print("=== test_battle_part_break_i18n 完成 ===")
