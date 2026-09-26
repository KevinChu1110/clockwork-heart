extends SceneTree
## 單元測試：章節教學對白改觸控用語＋六語系驗證 (test_chapter_touch_prompt_i18n.gd)
## 依據規範：AGENTS.md, CLAUDE.md, review.md 0-QA15, 0-QA23, 0-QA24, 0-QA25
## 驗證項目：
## 1. 六語系（zh_TW, zh_CN, en, ja, ko, es）字典完整性：5 句觸控與 5 句桌面文案皆有譯文，非空、無系統 emoji、非繁中殘留。
## 2. 觸控模式下（force_touch_mode = true）：章節教學對白與 DialogueBox 完全無「按 J」「Press J」「Space」等鍵盤鍵名，正確顯示「點閃避」等觸控用語。
## 3. 桌面模式下（force_touch_mode = false）：保留原鍵盤鍵名「按 J」「Press J」等，底部提示保留「Space」。
## 4. 動態切換語系（locale_changed）：切換語系後重開對話，即時呈現新語言譯文。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const DialogueBoxScn = preload("res://scenes/ui/dialogue_box.tscn")

var _ok: bool = true
var _loc: Node = null
var _box: DialogueBox = null
var _step: int = 0
var _wait: int = 0

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

const DESKTOP_KEYS := [
	"王者斬必擋。火圈先亮再落，亮了按 J。",
	"風切前會先響。響了按 J。",
	"牠停下來的那一拍才吃滿傷害。風聲響起就按 J。",
	"衝來時按 J 硬碰，岩甲會裂。落石也按 J。",
	"地先亮，再落石。亮了按 J。"
]

const TOUCH_KEYS := [
	"王者斬必擋。火圈先亮再落，亮了點閃避。",
	"風切前會先響。響了點閃避。",
	"牠停下來的那一拍才吃滿傷害。風聲響起就點閃避。",
	"衝來時點閃避硬碰，岩甲會裂。落石也點閃避。",
	"地先亮，再落石。亮了點閃避。"
]


func _assert(cond: bool, msg: String) -> void:
	if not cond:
		_ok = false
		printerr("  [ASSERT FAIL] ", msg)
	else:
		print("  [PASS] ", msg)


func _contains_keyboard_prompt(text: String) -> bool:
	# 檢查是否含有未轉換的鍵盤提示（包含各語言鍵盤詞）
	var keywords := [
		"按 J", "按J", "【J】", "（J）", "靠 J",
		"Press J", "press J", "Pulsa J", "pulsa J",
		"光ったら J", "落石は J", "落石も J",
		"J로", "J 로", "낙석도 J", "낙석은 J",
		"Space", "Espacio", "스페이스", "空白鍵"
	]
	for kw in keywords:
		if kw in text:
			return true
	return false


func _initialize() -> void:
	print("=== 開始執行 test_chapter_touch_prompt_i18n ===")
	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		printerr("FATAL: 找不到 Loc autoload")
		print("TEST_CHAPTER_TOUCH_PROMPT_I18N_FAIL")
		quit(1)
		return

	# 1. 檢驗六語系字典完整性、無 emoji、無繁中殘留
	print("\n--- 1. 六語系字典完整性與規範檢驗 ---")
	for lc in LOCALES:
		_loc.call("set_locale", lc)
		for k in TOUCH_KEYS:
			var translated: String = ContentLoc.text("ui", k)
			_assert(translated != "", "[%s] 觸控 key '%s' 翻譯不可為空" % [lc, k])
			_assert(not _contains_keyboard_prompt(translated), "[%s] 觸控譯文不應包含鍵盤關鍵詞: %s" % [lc, translated])
			if lc in ["en", "es"]:
				_assert(not ("王者斬" in translated) and not ("點閃避" in translated), "[%s] 譯文不應殘留繁體中文: %s" % [lc, translated])
			# 檢驗零 emoji
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				_assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 觸控譯文不准包含系統 emoji: %s" % [lc, translated])

		for k in DESKTOP_KEYS:
			var translated_desk: String = ContentLoc.text("ui", k)
			_assert(translated_desk != "", "[%s] 桌面 key '%s' 翻譯不可為空" % [lc, k])

	_loc.call("set_locale", "zh_TW")

	# 2. 檢驗 DialogueBox 在觸控模式與桌面模式下的文字與提示表現
	print("\n--- 2. DialogueBox 實體運算與模式切換檢驗 ---")
	_box = DialogueBoxScn.instantiate() as DialogueBox
	root.add_child(_box)

	# (A) 觸控模式 (force_touch_mode = true)
	_box.force_touch_mode = true
	for i in DESKTOP_KEYS.size():
		var desk_k: String = DESKTOP_KEYS[i]
		var touch_k: String = TOUCH_KEYS[i]
		_box.play([{"speaker": "系統", "text": ContentLoc.text("ui", desk_k)}])
		var displayed: String = _box._full_text
		_assert(not _contains_keyboard_prompt(displayed), "觸控模式下輸入桌面句 '%s'，輸出應自動適配且無鍵名: %s" % [desk_k, displayed])
		_assert(displayed == ContentLoc.text("ui", touch_k), "觸控模式輸出應等於觸控 key '%s' 譯文: %s" % [touch_k, displayed])

	var hint_touch: String = DialogueBox._hint_text(true)
	_assert(not _contains_keyboard_prompt(hint_touch), "觸控 continue hint 不應包含鍵盤鍵名 (Space等): %s" % hint_touch)
	_assert("點一下繼續" in hint_touch, "觸控 continue hint 應包含 '點一下繼續'")

	# (B) 桌面模式 (force_touch_mode = false)
	_box.force_touch_mode = false
	for i in DESKTOP_KEYS.size():
		var desk_k: String = DESKTOP_KEYS[i]
		_box.play([{"speaker": "系統", "text": ContentLoc.text("ui", desk_k)}])
		var displayed_desk: String = _box._full_text
		_assert("按 J" in displayed_desk, "桌面模式下應保留鍵名 '按 J': %s" % displayed_desk)

	var hint_desk: String = DialogueBox._hint_text(false)
	_assert("Space" in hint_desk, "桌面 continue hint 應包含 'Space': %s" % hint_desk)

	# 3. 檢驗動態語言切換 (locale_changed)
	print("\n--- 3. 動態切換語系 (locale_changed) 檢驗 ---")
	_box.force_touch_mode = true
	_loc.call("set_locale", "en")
	_box.play([{"speaker": "系統", "text": ContentLoc.text("ui", DESKTOP_KEYS[0])}])
	var en_text: String = _box._full_text
	_assert("Always parry the King's Cut" in en_text and "tap Dodge" in en_text, "英文觸控對白應正確顯示 tap Dodge: %s" % en_text)
	_assert(not _contains_keyboard_prompt(en_text), "英文觸控對白絕不含 J / Space: %s" % en_text)

	_loc.call("set_locale", "es")
	_box.play([{"speaker": "系統", "text": ContentLoc.text("ui", DESKTOP_KEYS[0])}])
	var es_text: String = _box._full_text
	_assert("toca Esquivar" in es_text, "西語觸控對白應正確顯示 toca Esquivar: %s" % es_text)
	_assert(not _contains_keyboard_prompt(es_text), "西語觸控對白絕不含 J / Espacio: %s" % es_text)

	_loc.call("set_locale", "ja")
	_box.play([{"speaker": "系統", "text": ContentLoc.text("ui", DESKTOP_KEYS[0])}])
	var ja_text: String = _box._full_text
	_assert("回避をタップ" in ja_text, "日語觸控對白應正確顯示 回避をタップ: %s" % ja_text)
	_assert(not _contains_keyboard_prompt(ja_text), "日語觸控對白絕不含 J / Space: %s" % ja_text)

	_loc.call("set_locale", "zh_TW")

	# 清理
	_box.queue_free()

	print("\n=== test_chapter_touch_prompt_i18n 測試結束 ===")
	if _ok:
		print("TEST_CHAPTER_TOUCH_PROMPT_I18N_OK")
		quit(0)
	else:
		printerr("TEST_CHAPTER_TOUCH_PROMPT_I18N_FAIL")
		quit(1)
