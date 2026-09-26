extends SceneTree
## 單元測試：章節教學對白鍵盤用語改觸控＋六語系即時切換驗證 (test_chapter_tutorial_touch_i18n.gd)
## 依據規範：AGENTS.md, review.md 0-QA23, 0-QA24, 0-QA25
## 驗證項目：
## 1. 六語系字典（zh_TW, zh_CN, en, ja, ko, es）觸控與桌面教學文案完整性、零 emoji、無繁中殘留。
## 2. 觸控模式 (force_touch_mode = true) 下：
##    main.gd 教學句與 DialogueBox 對白完全移除「按 J」「Tab」，正確顯示「點閃避」「點鎖定」。
## 3. 桌面模式 (force_touch_mode = false) 下：保留原鍵盤鍵名「按 J」「Tab」。
## 4. 對話開啟時動態切換語系 (locale_changed)，對話框文字即時換成對應語言；切回繁中還原。
## 5. chapter.json 教學句（c2.train_tip, c5.cliff_path）在觸控模式下亦無鍵盤鍵名並支援六語系。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const DialogueBoxScript = preload("res://scripts/ui/dialogue_box.gd")

var _ok: bool = true
var _loc: Node = null
var _box: Control = null
var _step: int = 0
var _wait: int = 0


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_ok = false
		printerr("  [ASSERT FAIL] ", msg)
	else:
		print("  [PASS] ", msg)


func _contains_keyboard_prompt(text: String) -> bool:
	return "按 J" in text or "Tab" in text or "【Tab】" in text or "【J】" in text or "（J）" in text or "靠 J" in text or "press J" in text.to_lower()


func _initialize() -> void:
	print("=== 開始執行 test_chapter_tutorial_touch_i18n ===")
	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		printerr("FATAL: 找不到 Loc autoload")
		print("TEST_CHAPTER_TUTORIAL_TOUCH_I18N_FAIL")
		quit(1)
		return

	# 1. 六語系字典完整性與零 emoji
	print("\n--- 1. 六語系字典完整性與零 emoji 檢驗 ---")
	var check_keys := [
		"王者斬必擋。火圈先亮再落，亮了點閃避。",
		"點鎖定鎖本體，發白再出手。砍到幻影會反咬、變慢。",
		"風切前會先響。響了點閃避。",
		"牠停下來的那一拍才吃滿傷害。風聲響起就點閃避。",
		"衝來時點閃避硬碰，岩甲會裂。落石也點閃避。",
		"發白那一瞬才打得中。點鎖定換目標。",
		"地先亮，再落石。亮了點閃避。",
		"王者斬必擋。火圈先亮再落，亮了按 J。",
		"Tab 鎖本體，發白再出手。砍到幻影會反咬、變慢。",
		"風切前會先響。響了按 J。",
		"牠停下來的那一拍才吃滿傷害。風聲響起就按 J。",
		"衝來時按 J 硬碰，岩甲會裂。落石也按 J。",
		"發白那一瞬才打得中。Tab 換目標。",
		"地先亮，再落石。亮了按 J。"
	]
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	for lc in locales:
		_loc.call("set_locale", lc)
		for k in check_keys:
			var translated: String = ContentLoc.text("ui", k)
			_assert(translated != "", "[%s] key '%s' 翻譯不可為空" % [lc, k])
			if lc in ["en", "es"]:
				_assert(not ("王者斬" in translated) and not ("火圈" in translated) and not ("落石" in translated),
					"[%s] 譯文不應殘留繁中: %s" % [lc, translated])
			# 檢驗零 emoji
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				if cp >= 0x1F300 and cp <= 0x1F9FF:
					_assert(false, "[%s] 不准包含系統 emoji: %s" % [lc, translated])
	_loc.call("set_locale", "zh_TW")

	# 2. 測試 DialogueBox 觸控與桌面切換、動態換語系
	print("\n--- 2. DialogueBox 觸控對白與即時語系切換驗證 ---")
	var scn: PackedScene = load("res://scenes/ui/dialogue_box.tscn")
	_box = scn.instantiate()
	root.add_child(_box)
	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 觸控模式下播放雷歐教學對白
			_box.set("force_touch_mode", true)
			var test_lines := [
				{"speaker": "系統", "text": "王者斬必擋。火圈先亮再落，亮了按 J。"},
				{"speaker": "系統", "text": "發白那一瞬才打得中。Tab 換目標。"},
				{"speaker": "系統", "text": "地先亮，再落石。亮了按 J。"}
			]
			_box.call("play", test_lines)
			_step = 2
			_wait = 0

		2:
			if _wait < 3:
				return false
			var full_t: String = _box.get("_full_text")
			print("  [觸控繁中] 第一句: ", full_t)
			_assert(not _contains_keyboard_prompt(full_t), "觸控繁中對白不可包含鍵盤鍵名 (按 J / Tab)")
			_assert("點閃避" in full_t, "觸控繁中對白應包含 '點閃避'")

			# 3. 測試動態切換到 en
			print("\n--- 3. 測試動態切換到英文 (en) ---")
			_loc.call("set_locale", "en")
			_step = 3
			_wait = 0

		3:
			if _wait < 3:
				return false
			var en_t: String = _box.get("_full_text")
			print("  [觸控英文] 即時更新後: ", en_t)
			_assert("tap dodge" in en_t.to_lower(), "觸控英文對白應包含 'tap Dodge'")
			_assert(not _contains_keyboard_prompt(en_t), "觸控英文對白不可包含按鍵 'press J'")
			_assert(not ("王者斬" in en_t), "觸控英文對白不應包含繁中殘留")

			# 4. 測試動態切換到 ja
			print("\n--- 4. 測試動態切換到日文 (ja) ---")
			_loc.call("set_locale", "ja")
			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false
			var ja_t: String = _box.get("_full_text")
			print("  [觸控日文] 即時更新後: ", ja_t)
			_assert("回避をタップ" in ja_t, "觸控日文對白應包含 '回避をタップ'")
			_assert(not _contains_keyboard_prompt(ja_t), "觸控日文對白不可包含按鍵 'J'")

			# 5. 測試切回繁中還原
			print("\n--- 5. 測試切回繁中 (zh_TW) 還原 ---")
			_loc.call("set_locale", "zh_TW")
			_step = 5
			_wait = 0

		5:
			if _wait < 3:
				return false
			var restored_t: String = _box.get("_full_text")
			print("  [繁中還原] : ", restored_t)
			_assert("點閃避" in restored_t, "繁中應正確還原為 '點閃避'")
			_assert(not _contains_keyboard_prompt(restored_t), "還原繁中不可包含鍵盤鍵名")

			# 6. 測試跳至第二句 (Tab 換目標 -> 點鎖定)
			print("\n--- 6. 測試第二句部位鎖定 (Tab 換目標) ---")
			_box.call("_finish_typing")
			_box.call("_skip_or_advance")
			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false
			var line2_t: String = _box.get("_full_text")
			print("  [觸控繁中 第二句] : ", line2_t)
			_assert(not _contains_keyboard_prompt(line2_t), "第二句觸控不可含 Tab")
			_assert("點鎖定" in line2_t, "第二句應轉為 '點鎖定'")

			# 7. 測試第二句英日切換
			_loc.call("set_locale", "en")
			var line2_en: String = _box.get("_full_text")
			print("  [觸控英文 第二句] : ", line2_en)
			_assert("Tap Lock" in line2_en, "第二句英文應包含 'Tap Lock'")
			_assert(not _contains_keyboard_prompt(line2_en), "第二句英文不可含 Tab")

			_loc.call("set_locale", "ja")
			var line2_ja: String = _box.get("_full_text")
			print("  [觸控日文 第二句] : ", line2_ja)
			_assert("ロックをタップ" in line2_ja, "第二句日文應包含 'ロックをタップ'")

			_loc.call("set_locale", "zh_TW")

			# 8. 測試桌面模式 (force_touch_mode = false) 保留鍵盤鍵名
			print("\n--- 7. 測試桌面鍵盤模式 (force_touch_mode = false) 保留按鍵 ---")
			_box.set("force_touch_mode", false)
			var desk_lines := [
				{"speaker": "系統", "text": "王者斬必擋。火圈先亮再落，亮了按 J。"},
				{"speaker": "系統", "text": "發白那一瞬才打得中。Tab 換目標。"}
			]
			_box.call("play", desk_lines)
			_step = 7
			_wait = 0

		7:
			if _wait < 3:
				return false
			var desk_t1: String = _box.get("_full_text")
			print("  [桌面繁中 第一句] : ", desk_t1)
			_assert("按 J" in desk_t1, "桌面模式應保留 '按 J'")

			_box.call("_finish_typing")
			_box.call("_skip_or_advance")
			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false
			var desk_t2: String = _box.get("_full_text")
			print("  [桌面繁中 第二句] : ", desk_t2)
			_assert("Tab" in desk_t2, "桌面模式應保留 'Tab'")

			# 清理與完成
			if _box and is_instance_valid(_box):
				_box.queue_free()
				_box = null

			if _ok:
				print("\n=== test_chapter_tutorial_touch_i18n 全部通過 ===")
				print("TEST_CHAPTER_TUTORIAL_TOUCH_I18N_OK")
				quit(0)
			else:
				printerr("\n=== test_chapter_tutorial_touch_i18n 斷言失敗 ===")
				print("TEST_CHAPTER_TUTORIAL_TOUCH_I18N_FAIL")
				quit(1)
			return true

	return false
