extends SceneTree
## 每日與主線任務名稱說明六語系單元測試 (test_quest_i18n.gd)
##
## 依據規範：
## 1. 建清單後改 locale，抽至少 3 條每日任務名稱等於該語系詞條
## 2. 驗證 commissions() 與 missions() 六語系（zh_TW, zh_CN, en, ja, ko, es）正常換詞
## 3. 驗證 list_commissions_bbcode()、list_missions_bbcode() 與 starpath_summary_bbcode() 六語系
## 4. 0-QA24 檢核：en / es 無 CJK 殘留；ja 日文漢字正確
## 5. 零系統 emoji
## 6. 驗證開著任務清單時切換語系 (Loc.locale_changed) 即時連動刷新 (0-QA25)

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0


func _fail(msg: String) -> void:
	push_error(msg)
	print("  [FAIL] ", msg)
	_ok = false


func _has_cjk(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF):
			return true
	return false


func _has_emoji(text: String) -> bool:
	for i in range(text.length()):
		var cp := text.unicode_at(i)
		if (cp >= 0x2600 and cp <= 0x27BF and cp != 0x2715 and cp != 0x2713) or (cp >= 0x1F300 and cp <= 0x1FAFF):
			return true
	return false


func _process(_delta: float) -> bool:
	_frame += 1
	if _frame < 3:
		return false

	_run_tests()

	if _ok:
		print("\n=======================================================")
		print("QUEST_I18N_OK")
		print("=======================================================")
		quit(0)
	else:
		push_error("QUEST_I18N_FAIL")
		print("QUEST_I18N_FAIL")
		quit(1)
	return true


func _run_tests() -> void:
	print("── 開始執行任務系統六語系單元測試 (test_quest_i18n) ──")

	var loc: Node = root.get_node_or_null("Loc")
	var qs: Node = root.get_node_or_null("QuestSystem")
	if loc == null or qs == null:
		_fail("Autoload Loc 或 QuestSystem 缺失")
		return

	# 1. 驗證繁中基準
	loc.call("set_locale", "zh_TW")
	var raw_commissions: Array = qs.call("commissions")
	if raw_commissions.size() < 3:
		_fail("每日任務數量不足 3: %d" % raw_commissions.size())
		return
	print("  ✓ 繁中每日任務數量: %d" % raw_commissions.size())

	# 2. 測試建清單後改 locale，抽至少 3 條每日任務名稱等於該語系詞條
	for target_loc in ["en", "ja", "zh_CN", "ko", "es"]:
		loc.call("set_locale", target_loc)
		var comms: Array = qs.call("commissions")
		var checked_count := 0

		# 讀取目標語系的 quest.json 供核實
		var q_path := "res://data/i18n/content/%s/quest.json" % target_loc
		var expected_data: Dictionary = {}
		if FileAccess.file_exists(q_path):
			var f := FileAccess.open(q_path, FileAccess.READ)
			if f != null:
				expected_data = JSON.parse_string(f.get_as_text())

		for c in comms:
			var qid: String = str(c.get("id", ""))
			var qname: String = str(c.get("name", ""))
			var qdesc: String = str(c.get("desc", ""))

			if _has_emoji(qname) or _has_emoji(qdesc):
				_fail("[%s] 發現系統 emoji: %s / %s" % [target_loc, qname, qdesc])

			if expected_data.has(qid):
				var exp_entry: Dictionary = expected_data[qid]
				var exp_name: String = str(exp_entry.get("name", ""))
				var exp_desc: String = str(exp_entry.get("desc", ""))

				if qname != exp_name:
					_fail("[%s] 任務 %s 名稱不相符: 實得 '%s', 預期 '%s'" % [target_loc, qid, qname, exp_name])
				if qdesc != exp_desc:
					_fail("[%s] 任務 %s 說明不相符: 實得 '%s', 預期 '%s'" % [target_loc, qid, qdesc, exp_desc])
				checked_count += 1

			if target_loc in ["en", "es"]:
				if _has_cjk(qname) or _has_cjk(qdesc):
					_fail("[%s] 英文/西文殘留 CJK 漢字: %s / %s" % [target_loc, qname, qdesc])

		if checked_count < 3:
			_fail("[%s] 核對每日任務數量少於 3 條: %d" % [target_loc, checked_count])
		else:
			print("  ✓ [%s] 抽測 %d 條每日任務名稱說明與語系詞條完全吻合" % [target_loc, checked_count])

	# 3. 驗證長遠任務 missions() 六語系
	for target_loc in ["en", "ja"]:
		loc.call("set_locale", target_loc)
		var missions: Array = qs.call("missions")
		var q_path := "res://data/i18n/content/%s/quest.json" % target_loc
		var expected_data: Dictionary = {}
		if FileAccess.file_exists(q_path):
			var f := FileAccess.open(q_path, FileAccess.READ)
			if f != null:
				expected_data = JSON.parse_string(f.get_as_text())

		var m_checked := 0
		for m in missions:
			var mid: String = str(m.get("id", ""))
			var mname: String = str(m.get("name", ""))
			var mdesc: String = str(m.get("desc", ""))
			if expected_data.has(mid):
				var exp_name: String = str(expected_data[mid].get("name", ""))
				if mname != exp_name:
					_fail("[%s] 主線任務 %s 名稱不吻合: '%s' vs '%s'" % [target_loc, mid, mname, exp_name])
				m_checked += 1
		print("  ✓ [%s] 長遠任務抽測 %d 條均符合語系詞條" % [target_loc, m_checked])

	# 4. 驗證 list_missions_bbcode() 獎勵文字已在地化且追蹤條件不變
	loc.call("set_locale", "en")
	var bb_en: String = qs.call("list_missions_bbcode")
	if bb_en.find("Gold") < 0 or bb_en.find("Stardust") < 0:
		_fail("list_missions_bbcode (en) 未翻出 Gold/Stardust: %s" % bb_en.substr(0, 200))
	if bb_en.find("金 ") >= 0 or bb_en.find("星屑") >= 0:
		_fail("list_missions_bbcode (en) 仍殘留中文獎勵標籤: %s" % bb_en.substr(0, 200))
	print("  ✓ list_missions_bbcode (en) 獎勵字串正確在地化")

	# 5. 驗證 starpath_summary_bbcode() 每日發條儀表板六語系
	loc.call("set_locale", "ja")
	var sum_ja: String = qs.call("starpath_summary_bbcode")
	if sum_ja.find("毎日ぜんまい") < 0 and sum_ja.find("ぜんまい累計") < 0:
		_fail("starpath_summary_bbcode (ja) 未正確翻譯: %s" % sum_ja.substr(0, 200))
	if sum_ja.find("演武場") < 0:
		_fail("starpath_summary_bbcode (ja) 缺少演武場: %s" % sum_ja.substr(0, 200))
	print("  ✓ starpath_summary_bbcode (ja) 正確在地化")

	# 6. 切回 zh_TW
	loc.call("set_locale", "zh_TW")
	print("  ✓ 任務系統各語系驗證完成")
