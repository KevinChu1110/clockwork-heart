extends SceneTree
## 戰鬥畫面不教按鍵：godot --headless -s res://scripts/battle/test_battle_touch_prompt_i18n.gd
##
## 自動回合（任務書 §0、§2）之後，戰報、教學小字、中央倒數都不能再出現
## 「按 J」「Tab」「點閃避」「點鎖定」這類操作提示 —— 觸控與桌面模式都一樣。
## 驗證項目：
## 1. 新增的戰報／提示字串六語系都有譯文、英西文不殘留中文、零系統 emoji。
## 2. 雷歐戰（觸控、桌面兩種模式）開場戰報與教學小字沒有任何操作提示。
## 3. 開著戰鬥切 EN，戰報跟著換、仍沒有 Tap Dodge／Tap Lock／press J；切回繁中還原。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

const NEW_KEYS := [
	"[color=#8ff]%s停擺，換上%s[/color]",
	"[color=#fc8]%s停擺，三欄用盡，改用空手[/color]",
	"彈開",
	"[color=#ffd700]自動彈開 · %s[/color]",
	"[color=#f66]%s蓄力中[/color]",
	"%s蓄力中",
	"[color=#fc0]本體血量壓到七成、四成時，部位會自動破[/color]",
	"王者斬蓄力時會自動彈開 · 看部位條",
	"自動戰鬥 · 次數用完會自動換武",
	"[color=#e88]沒彈開 · %s[/color]",
	"離開練習",
]

const PROMPTS_ZH := ["按 J", "【J】", "（J）", "靠 J", "Tab", "點閃避", "點鎖定", "右側拇指", "格擋窗"]
const PROMPTS_EN := ["Tap Dodge", "Tap Lock", "press J", "Press J", "[J]", "Tab"]

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


func _has_cjk(t: String) -> bool:
	for ch in t:
		var cp: int = ch.unicode_at(0)
		if cp >= 0x4E00 and cp <= 0x9FFF:
			return true
	return false


func _visible_text() -> String:
	## 玩家看得到的字：戰報、教學小字、中央倒數
	var parts: PackedStringArray = []
	var history: Array = _battle.get("_log_history")
	for r in history:
		parts.append(str(r))
	var lbl: RichTextLabel = _battle.get("log_label") as RichTextLabel
	if lbl:
		parts.append(lbl.get_parsed_text())
	var coach: Label = _battle.get("_coach") as Label
	if coach:
		parts.append(coach.text)
	for n in ["countdown", "countdown_sub"]:
		var l: Label = _battle.get(n) as Label
		if l and l.visible:
			parts.append(l.text)
	return " ".join(parts)


func _first_hit(text: String, needles: Array) -> String:
	for n in needles:
		if str(n) in text:
			return str(n)
	return ""


func _initialize() -> void:
	print("=== 開始執行 test_battle_touch_prompt_i18n（自動回合版）===")
	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		printerr("FATAL: 找不到 Loc autoload")
		print("TEST_BATTLE_TOUCH_PROMPT_I18N_FAIL")
		quit(1)
		return

	print("\n--- 1. 新字串六語系譯文與零 emoji ---")
	for lc in ["zh_CN", "en", "ja", "ko", "es"]:
		_loc.call("set_locale", lc)
		for k in NEW_KEYS:
			var tr: String = ContentLoc.text("ui", k)
			## 簡中有些字跟繁中同形（例：蓄力中），只要求不為空
			_assert(tr != "" and (lc == "zh_CN" or tr != k), "[%s] '%s' 有譯文" % [lc, k])
			if lc in ["en", "es"]:
				_assert(not _has_cjk(tr), "[%s] 譯文不殘留中文: %s" % [lc, tr])
			for ch in tr:
				var cp: int = ch.unicode_at(0)
				_assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 不含系統 emoji: %s" % [lc, tr])
	_loc.call("set_locale", "zh_TW")
	_step = 1
	_wait = 0


func _start(touch: bool) -> void:
	var b_scn: PackedScene = load("res://scenes/battle/battle.tscn")
	_battle = b_scn.instantiate()
	_battle.set("force_touch_mode", touch)
	root.add_child(_battle)
	_battle.call("setup", "leo")


func _close() -> void:
	if _battle:
		root.remove_child(_battle)
		_battle.queue_free()
		_battle = null


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			print("\n--- 2a. 觸控模式雷歐戰 ---")
			_loc.call("set_locale", "zh_TW")
			_start(true)
			_step = 2
			_wait = 0
		2:
			if _wait < 3:
				return false
			var txt := _visible_text()
			var hit := _first_hit(txt, PROMPTS_ZH)
			_assert(hit == "", "觸控繁中沒有操作提示（命中：%s）" % hit)
			_assert("部位會自動破" in txt, "開場戰報說明部位自動破")
			print("\n--- 3. 開著戰鬥切 EN ---")
			_loc.call("set_locale", "en")
			_step = 3
			_wait = 0
		3:
			if _wait < 3:
				return false
			var txt_en := _visible_text()
			var hit_en := _first_hit(txt_en, PROMPTS_EN)
			_assert(hit_en == "", "EN 沒有操作提示（命中：%s）" % hit_en)
			_assert("Parts break on their own" in txt_en, "EN 戰報跟著換語系")
			_loc.call("set_locale", "zh_TW")
			_step = 4
			_wait = 0
		4:
			if _wait < 3:
				return false
			_assert("部位會自動破" in _visible_text(), "切回繁中還原")
			_close()
			print("\n--- 2b. 桌面模式雷歐戰 ---")
			_start(false)
			_step = 5
			_wait = 0
		5:
			if _wait < 3:
				return false
			var txt_d := _visible_text()
			var hit_d := _first_hit(txt_d, PROMPTS_ZH)
			_assert(hit_d == "", "桌面繁中也沒有操作提示（命中：%s）" % hit_d)
			_close()
			print("\n=======================================================")
			if _ok:
				print("TEST_BATTLE_TOUCH_PROMPT_I18N_OK")
				quit(0)
			else:
				printerr("TEST_BATTLE_TOUCH_PROMPT_I18N_FAIL")
				quit(1)
			return true
	return false
