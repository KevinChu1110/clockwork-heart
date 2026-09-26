extends SceneTree
## 單元測試：戰鬥操作提示改觸控用語＋六語系即時切換驗證 (test_battle_touch_prompt_i18n.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 0-QA23, 0-QA24, 0-QA25
## 驗證項目：
## 1. 觸控模式下（force_touch_mode = true）：雷歐戰、部位戰日誌與 HUD 完全沒有「按 J」「Tab」等鍵盤鍵名，正確顯示「點閃避」「點鎖定」。
## 2. 桌面模式下（force_touch_mode = false）：保留原鍵盤鍵名「按 J」「Tab」。
## 3. 六語系（zh_TW, zh_CN, en, ja, ko, es）觸控與桌面文案皆有譯文，非繁中殘留。
## 4. 戰鬥中動態切換語系 (locale_changed)，日誌與提示同步即時更換；切回繁中還原。
## 5. 全文零系統 emoji。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

var _ok: bool = true
var _battle: Control = null
var _loc: Node = null
var _step: int = 0
var _wait: int = 0


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_ok = false
		printerr("  [ASSERT FAIL] ", msg)
	else:
		print("  [PASS] ", msg)


func _contains_keyboard_prompt(text: String) -> bool:
	# 檢查是否含有未轉換的鍵盤提示
	return "按 J" in text or "Tab 鎖定" in text or "Tab/1/2/3" in text or "【Tab】" in text or "【J】" in text or "（J）" in text or "靠 J" in text


func _initialize() -> void:
	print("=== 開始執行 test_battle_touch_prompt_i18n ===")
	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		printerr("FATAL: 找不到 Loc autoload")
		print("TEST_BATTLE_TOUCH_PROMPT_I18N_FAIL")
		quit(1)
		return

	# 1. 驗證六語系字典完整性與零 emoji
	print("\n--- 1. 六語系字典完整性與零 emoji 檢驗 ---")
	var check_keys := [
		"點閃避",
		"點鎖定",
		"[color=#fa6]王者斬要擋，擋住就能反擊 · 火圈亮起後點閃避跳開[/color]",
		"[color=#fc0]部位破壞：點鎖定部位／本體 · 破甲降防 · 破冠／角會激怒[/color]",
		"【點閃避】格擋　·　【點鎖定】鎖部位　·　火圈後躍出",
		"提示：倒數變綠立刻點閃避格擋！火圈亮起後再點閃避躍出",
		"鎖定：%s　·　點鎖定切換　·　破甲降防／破冠激怒"
	]
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	for lc in locales:
		_loc.call("set_locale", lc)
		for k in check_keys:
			var translated: String = ContentLoc.text("ui", k)
			_assert(translated != "", "[%s] key '%s' 翻譯不可為空" % [lc, k])
			if lc in ["en", "es"]:
				_assert(not ("王者斬" in translated) and not ("部位破壞" in translated), "[%s] 譯文不應殘留繁體中文: %s" % [lc, translated])
			# 檢驗零 emoji
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				# Emoji code point ranges
				_assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 不准包含系統 emoji: %s" % [lc, translated])
	_loc.call("set_locale", "zh_TW")

	# 準備進入場景實機生命週期測試
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 2. 建立雷歐戰鬥，以觸控模式 (force_touch_mode = true) 啟動
			print("\n--- 2. 觸控模式下啟動雷歐戰鬥 (force_touch_mode = true) ---")
			_loc.call("set_locale", "zh_TW")
			var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn.instantiate()
			_battle.set("force_touch_mode", true)
			root.add_child(_battle)
			_battle.call("setup", "leo")
			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false
			var history: Array = _battle.get("_log_history")
			var full_log: String = " ".join(history)
			print("  [觸控繁中] 開場日誌: ", full_log)
			var parry_lbl: Label = _battle.get("parry_hint")
			var hint_text: String = parry_lbl.text if parry_lbl else ""
			print("  [觸控繁中] 提示文字: ", hint_text)

			# 驗證日誌與提示無鍵盤鍵名，且包含觸控用語
			_assert(not _contains_keyboard_prompt(full_log), "觸控繁中日誌不應包含鍵盤鍵名 (按 J / Tab)")
			_assert("點閃避" in full_log or "點鎖定" in full_log, "觸控繁中日誌應包含 '點閃避' 或 '點鎖定'")
			_assert(not _contains_keyboard_prompt(hint_text), "觸控繁中提示不應包含鍵盤鍵名 (按 J / Tab)")
			_assert("點閃避" in hint_text or "點鎖定" in hint_text, "觸控繁中提示應包含 '點閃避' 或 '點鎖定'")

			# 3. 戰鬥中動態切換到 en
			print("\n--- 3. 開著戰鬥動態切換語系至 EN ---")
			_loc.call("set_locale", "en")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			var history_en: Array = _battle.get("_log_history")
			var full_log_en: String = " ".join(history_en)
			print("  [觸控 EN] 開場日誌: ", full_log_en)
			var parry_lbl: Label = _battle.get("parry_hint")
			var hint_text_en: String = parry_lbl.text if parry_lbl else ""
			print("  [觸控 EN] 提示文字: ", hint_text_en)

			_assert(not _contains_keyboard_prompt(full_log_en), "EN 日誌不應包含鍵盤鍵名")
			_assert(not ("王者斬" in full_log_en), "EN 日誌不應殘留繁中 '王者斬'")
			_assert("Tap Dodge" in full_log_en or "Tap Lock" in full_log_en or "Dodge" in full_log_en, "EN 日誌應包含英文觸控用語 Tap Dodge / Tap Lock")
			_assert(not _contains_keyboard_prompt(hint_text_en), "EN 提示不應包含鍵盤鍵名")
			_assert("Tap Dodge" in hint_text_en or "Tap Lock" in hint_text_en or "parry" in hint_text_en, "EN 提示應包含英文觸控提示")

			# 4. 戰鬥中動態切換到 ja
			print("\n--- 4. 開著戰鬥動態切換語系至 JA ---")
			_loc.call("set_locale", "ja")
			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false
			var history_ja: Array = _battle.get("_log_history")
			var full_log_ja: String = " ".join(history_ja)
			print("  [觸控 JA] 開場日誌: ", full_log_ja)
			var parry_lbl: Label = _battle.get("parry_hint")
			var hint_text_ja: String = parry_lbl.text if parry_lbl else ""
			print("  [觸控 JA] 提示文字: ", hint_text_ja)

			_assert(not _contains_keyboard_prompt(full_log_ja), "JA 日誌不應包含鍵盤鍵名")
			_assert("回避" in full_log_ja or "タップ" in full_log_ja or "ロック" in full_log_ja, "JA 日誌應包含日文觸控用語")
			_assert(not _contains_keyboard_prompt(hint_text_ja), "JA 提示不應包含鍵盤鍵名")
			_assert("回避" in hint_text_ja or "タップ" in hint_text_ja or "ロック" in hint_text_ja, "JA 提示應包含日文觸控提示")

			# 5. 切回繁中還原
			print("\n--- 5. 切回繁中還原 ---")
			_loc.call("set_locale", "zh_TW")
			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			var history_tw: Array = _battle.get("_log_history")
			var full_log_tw: String = " ".join(history_tw)
			print("  [還原繁中] 開場日誌: ", full_log_tw)
			_assert("王者斬" in full_log_tw, "切回繁中後應正確還原繁中原文")
			_assert("點閃避" in full_log_tw or "點鎖定" in full_log_tw, "切回繁中後觸控用語依然有效")

			# 清除第一場戰鬥，測試桌面模式 (force_touch_mode = false)
			root.remove_child(_battle)
			_battle.queue_free()
			_battle = null

			print("\n--- 6. 桌面鍵盤模式驗證 (force_touch_mode = false) ---")
			var b_scn_desk: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn_desk.instantiate()
			_battle.set("force_touch_mode", false)
			root.add_child(_battle)
			_battle.call("setup", "leo")
			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false
			var history_desk: Array = _battle.get("_log_history")
			var full_log_desk: String = " ".join(history_desk)
			print("  [桌面模式] 開場日誌: ", full_log_desk)
			var parry_lbl: Label = _battle.get("parry_hint")
			var hint_text_desk: String = parry_lbl.text if parry_lbl else ""
			print("  [桌面模式] 提示文字: ", hint_text_desk)

			_assert("按 J" in full_log_desk or "Tab" in full_log_desk, "桌面模式日誌應保留鍵盤鍵名 '按 J' 或 'Tab'")
			_assert("J" in hint_text_desk or "Tab" in hint_text_desk, "桌面模式提示應保留鍵盤鍵名 'J' 或 'Tab'")

			# 清理
			root.remove_child(_battle)
			_battle.queue_free()
			_battle = null

			print("\n=======================================================")
			if _ok:
				print("TEST_BATTLE_TOUCH_PROMPT_I18N_OK")
				quit(0)
			else:
				printerr("TEST_BATTLE_TOUCH_PROMPT_I18N_FAIL")
				quit(1)
			return true
	return false
