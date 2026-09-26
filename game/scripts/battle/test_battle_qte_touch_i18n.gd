extends SceneTree
## 單元測試：戰鬥時機窗與互動窗鍵盤用語改觸控＋六語系驗收 (test_battle_qte_touch_i18n.gd)
## 依據規範：AGENTS.md, review.md 0-QA23, 0-QA24, 0-QA25
## 驗證項目：
## 1. 字典完整性：六語系（zh_TW, zh_CN, en, ja, ko, es）時機窗/互動窗/格擋/閃避提示字典無漏翻、無系統 emoji。
## 2. 觸控模式（force_touch_mode = true）：
##    - 雷歐王者斬蓄力與格擋時機窗：無「按 J」「滑鼠左鍵」，顯示觸控用語（現在點閃避！、準備：倒數到「格擋」再點閃避）。
##    - 落石/火圈危險互動窗：無「按 J」「滑鼠」，顯示觸控用語（互動窗：點閃避、現在點閃避）。
## 3. 開著戰鬥即時切換語系 (locale_changed)：
##    - 時機窗與互動窗提示隨語系切換立即更新為 en / ja，無繁中殘留，無鍵盤用語。
##    - 切回繁中完整還原。
## 4. 桌面模式（force_touch_mode = false）：保留原鍵盤鍵名「按 J」「滑鼠」。

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
	return "按 J" in text or "滑鼠" in text or "Tab" in text or "【Tab】" in text or "【J】" in text or "（J）" in text or "靠 J" in text or "press J" in text.to_lower() or "left-click" in text.to_lower() or "clic izquierdo" in text.to_lower() or "左クリック" in text or "좌클릭" in text


func _initialize() -> void:
	print("=== 開始執行 test_battle_qte_touch_i18n ===")
	_loc = root.get_node_or_null("Loc")
	if _loc == null:
		printerr("FATAL: 找不到 Loc autoload")
		print("TEST_BATTLE_QTE_TOUCH_I18N_FAIL")
		quit(1)
		return

	# 1. 六語系字典檢驗
	print("\n--- 1. 六語系時機窗/互動窗字典完整性與零 emoji 檢驗 ---")
	var check_keys := [
		"現在點閃避！",
		"現在按 J 或滑鼠左鍵！",
		"互動窗：點閃避",
		"互動窗：按 J",
		"時機窗：點閃避",
		"時機窗：按 J 或點畫面",
		"準備：倒數到「格擋」再點閃避",
		"準備：倒數到「格擋」再按",
		"%s！現在點閃避  %.1fs",
		"%s！現在按 J 或滑鼠  %.1fs",
		"準備：黃色「閃」出現時點閃避",
		"準備：黃色「閃」出現時按 J",
		"輸出本體 · 落岩仍要點閃避",
		"輸出本體 · 落岩仍要 J"
	]
	var locales := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]
	for lc in locales:
		_loc.call("set_locale", lc)
		for k in check_keys:
			var translated: String = ContentLoc.text("ui", k)
			_assert(translated != "", "[%s] key '%s' 翻譯不可為空" % [lc, k])
			if lc in ["en", "es"]:
				_assert(not ("點閃避" in translated) and not ("按 J" in translated) and not ("滑鼠" in translated), "[%s] 譯文不應殘留繁體中文: %s" % [lc, translated])
			# 零 emoji
			for ch in translated:
				var cp: int = ch.unicode_at(0)
				_assert(not (cp >= 0x1F300 and cp <= 0x1F9FF), "[%s] 不准包含系統 emoji: %s" % [lc, translated])
	_loc.call("set_locale", "zh_TW")

	_step = 1
	_wait = 0


func _process(_delta: float) -> bool:
	_wait += 1
	match _step:
		1:
			# 2. 觸控模式 (force_touch_mode = true) 啟動雷歐戰鬥
			print("\n--- 2. 觸控模式下啟動雷歐戰鬥，驗證時機窗/互動窗提示 ---")
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
			var sim = _battle.get("sim")
			var pe = _battle.call("_primary_enemy")
			_assert(pe != null, "雷歐敵方單位存在")
			if pe == null:
				quit(1)
				return true

			# (A) 模擬王者斬蓄力階段 (telegraph_active = true, state_timer = 2.0)
			pe.telegraph_active = true
			pe.state_timer = 2.0
			_battle.call("_update_parry_countdown", pe)

			var sub_lbl: Label = _battle.get("countdown_sub")
			var hint_lbl: Label = _battle.get("parry_hint")
			var cd_lbl: Label = _battle.get("countdown")
			var sub_t: String = sub_lbl.text if sub_lbl else ""
			var hint_t: String = hint_lbl.text if hint_lbl else ""
			print("  [王者斬蓄力中] sub: ", sub_t)
			print("  [王者斬蓄力中] hint: ", hint_t)
			_assert(not _contains_keyboard_prompt(sub_t), "觸控王者斬蓄力 sub 不得含鍵盤鍵名")
			_assert(not _contains_keyboard_prompt(hint_t), "觸控王者斬蓄力 hint 不得含鍵盤鍵名")
			_assert("點閃避" in hint_t, "觸控王者斬蓄力 hint 應為觸控用語（點閃避）")

			# (B) 模擬進入王者斬格擋時機窗 (state_timer = 0.5 <= PARRY_WINDOW 0.85)
			pe.state_timer = 0.5
			_battle.call("_update_parry_countdown", pe)
			sub_t = sub_lbl.text if sub_lbl else ""
			hint_t = hint_lbl.text if hint_lbl else ""
			print("  [王者斬時機窗] countdown: ", cd_lbl.text if cd_lbl else "")
			print("  [王者斬時機窗] sub: ", sub_t)
			print("  [王者斬時機窗] hint: ", hint_t)
			_assert(not _contains_keyboard_prompt(sub_t), "觸控王者斬時機窗 sub 不得含鍵盤鍵名（按 J／滑鼠左鍵）")
			_assert("現在點閃避！" in sub_t, "觸控王者斬時機窗 sub 應為「現在點閃避！」")
			_assert(not _contains_keyboard_prompt(hint_t), "觸控王者斬時機窗 hint 不得含鍵盤鍵名")
			_assert("格擋時機！" in hint_t, "觸控王者斬時機窗 hint 應為「格擋時機！」")

			# (C) 模擬落石危害互動窗 (rockfall window)
			sim.hazard_kind = "rockfall"
			sim.hazard_phase = "window"
			sim.hazard_timer = 0.8
			_battle.call("_update_hazard_hud")
			sub_t = sub_lbl.text if sub_lbl else ""
			hint_t = hint_lbl.text if hint_lbl else ""
			print("  [落石互動窗] countdown: ", cd_lbl.text if cd_lbl else "")
			print("  [落石互動窗] sub: ", sub_t)
			print("  [落石互動窗] hint: ", hint_t)
			_assert(not _contains_keyboard_prompt(sub_t), "觸控落石互動窗 sub 不得含鍵盤鍵名")
			_assert("現在點閃避" in sub_t, "觸控落石互動窗 sub 應為「現在點閃避」")
			_assert(not _contains_keyboard_prompt(hint_t), "觸控落石互動窗 hint 不得含鍵盤鍵名")
			_assert("互動窗：點閃避" in hint_t, "觸控落石互動窗 hint 應為「互動窗：點閃避」")

			_step = 3
			_wait = 0

		3:
			# 3. 開著戰鬥中動態切換語系至 EN
			print("\n--- 3. 開著戰鬥動態切換語系至 EN ---")
			_loc.call("set_locale", "en")
			_step = 4
			_wait = 0

		4:
			if _wait < 3:
				return false
			var sub_lbl: Label = _battle.get("countdown_sub")
			var hint_lbl: Label = _battle.get("parry_hint")
			var cd_lbl: Label = _battle.get("countdown")
			var sub_t: String = sub_lbl.text if sub_lbl else ""
			var hint_t: String = hint_lbl.text if hint_lbl else ""
			print("  [EN 落石互動窗] countdown: ", cd_lbl.text if cd_lbl else "")
			print("  [EN 落石互動窗] sub: ", sub_t)
			print("  [EN 落石互動窗] hint: ", hint_t)
			_assert(not _contains_keyboard_prompt(sub_t), "EN 落石互動窗 sub 不得含鍵盤鍵名")
			_assert(not ("落岩" in sub_t) and not ("點閃避" in sub_t), "EN 落石互動窗 sub 不應殘留繁中")
			_assert("Tap Dodge" in sub_t, "EN 落石互動窗 sub 應為英文 Tap Dodge")
			_assert(not _contains_keyboard_prompt(hint_t), "EN 落石互動窗 hint 不得含鍵盤鍵名")
			_assert(not ("互動窗" in hint_t), "EN 落石互動窗 hint 不應殘留繁中")
			_assert("Tap Dodge" in hint_t or "Dodge" in hint_t, "EN 落石互動窗 hint 應為英文譯文")

			# 切換至王者斬時機窗驗證 EN
			var pe = _battle.call("_primary_enemy")
			var sim = _battle.get("sim")
			sim.hazard_phase = "idle"
			pe.telegraph_active = true
			pe.state_timer = 0.5
			_battle.call("_update_parry_countdown", pe)
			sub_t = sub_lbl.text if sub_lbl else ""
			hint_t = hint_lbl.text if hint_lbl else ""
			print("  [EN 王者斬時機窗] sub: ", sub_t)
			print("  [EN 王者斬時機窗] hint: ", hint_t)
			_assert("Tap Dodge now!" in sub_t, "EN 王者斬時機窗 sub 應為 'Tap Dodge now!'")
			_assert("Parry window!" in hint_t, "EN 王者斬時機窗 hint 應為 'Parry window!'")

			_step = 5
			_wait = 0

		5:
			# 4. 開著戰鬥中動態切換語系至 JA
			print("\n--- 4. 開著戰鬥動態切換語系至 JA ---")
			_loc.call("set_locale", "ja")
			_step = 6
			_wait = 0

		6:
			if _wait < 3:
				return false
			var sub_lbl: Label = _battle.get("countdown_sub")
			var hint_lbl: Label = _battle.get("parry_hint")
			var sub_t: String = sub_lbl.text if sub_lbl else ""
			var hint_t: String = hint_lbl.text if hint_lbl else ""
			print("  [JA 王者斬時機窗] sub: ", sub_t)
			print("  [JA 王者斬時機窗] hint: ", hint_t)
			_assert(not _contains_keyboard_prompt(sub_t), "JA 王者斬時機窗 sub 不得含鍵盤鍵名")
			_assert("今すぐ回避をタップ！" in sub_t, "JA 王者斬時機窗 sub 應為日文 '今すぐ回避をタップ！'")
			_assert("パリィのタイミング！" in hint_t, "JA 王者斬時機窗 hint 應為日文 'パリィのタイミング！'")

			# 測試 JA 落石互動窗
			var sim = _battle.get("sim")
			var pe = _battle.call("_primary_enemy")
			pe.telegraph_active = false
			sim.hazard_kind = "rockfall"
			sim.hazard_phase = "window"
			sim.hazard_timer = 0.8
			_battle.call("_update_hazard_hud")
			sub_t = sub_lbl.text if sub_lbl else ""
			hint_t = hint_lbl.text if hint_lbl else ""
			print("  [JA 落石互動窗] sub: ", sub_t)
			print("  [JA 落石互動窗] hint: ", hint_t)
			_assert("今すぐ回避をタップ" in sub_t, "JA 落石互動窗 sub 應為日文 '今すぐ回避をタップ'")
			_assert("連携窓：回避をタップ" in hint_t, "JA 落石互動窗 hint 應為日文 '連携窓：回避をタップ'")

			_step = 7
			_wait = 0

		7:
			# 5. 切回繁中還原
			print("\n--- 5. 切回繁中還原 ---")
			_loc.call("set_locale", "zh_TW")
			_step = 8
			_wait = 0

		8:
			if _wait < 3:
				return false
			var sub_lbl: Label = _battle.get("countdown_sub")
			var hint_lbl: Label = _battle.get("parry_hint")
			var sub_t: String = sub_lbl.text if sub_lbl else ""
			var hint_t: String = hint_lbl.text if hint_lbl else ""
			print("  [還原繁中 落石互動窗] sub: ", sub_t)
			print("  [還原繁中 落石互動窗] hint: ", hint_t)
			_assert("現在點閃避" in sub_t, "還原繁中後落石互動窗 sub 為繁中觸控用語")
			_assert("互動窗：點閃避" in hint_t, "還原繁中後落石互動窗 hint 為繁中觸控用語")

			# 清除觸控場景，驗證桌面模式
			root.remove_child(_battle)
			_battle.queue_free()
			_battle = null

			print("\n--- 6. 桌面鍵盤模式 (force_touch_mode = false) 保留鍵盤鍵名 ---")
			var b_scn_desk: PackedScene = load("res://scenes/battle/battle.tscn")
			_battle = b_scn_desk.instantiate()
			_battle.set("force_touch_mode", false)
			root.add_child(_battle)
			_battle.call("setup", "leo")
			_step = 9
			_wait = 0

		9:
			if _wait < 3:
				return false
			var pe = _battle.call("_primary_enemy")
			var sim = _battle.get("sim")
			var sub_lbl: Label = _battle.get("countdown_sub")
			var hint_lbl: Label = _battle.get("parry_hint")

			# 桌面王者斬時機窗
			pe.telegraph_active = true
			pe.state_timer = 0.5
			_battle.call("_update_parry_countdown", pe)
			var sub_t: String = sub_lbl.text if sub_lbl else ""
			print("  [桌面模式 王者斬時機窗] sub: ", sub_t)
			_assert("按 J 或滑鼠左鍵" in sub_t, "桌面模式王者斬時機窗 sub 應保留 '按 J 或滑鼠左鍵'")

			# 桌面落石互動窗
			pe.telegraph_active = false
			sim.hazard_kind = "rockfall"
			sim.hazard_phase = "window"
			sim.hazard_timer = 0.8
			_battle.call("_update_hazard_hud")
			sub_t = sub_lbl.text if sub_lbl else ""
			var hint_t: String = hint_lbl.text if hint_lbl else ""
			print("  [桌面模式 落石互動窗] sub: ", sub_t)
			print("  [桌面模式 落石互動窗] hint: ", hint_t)
			_assert("按 J 或滑鼠" in sub_t, "桌面模式落石互動窗 sub 應保留 '按 J 或滑鼠'")
			_assert("互動窗：按 J" in hint_t, "桌面模式落石互動窗 hint 應保留 '互動窗：按 J'")

			# 清理
			root.remove_child(_battle)
			_battle.queue_free()
			_battle = null

			print("\n=======================================================")
			if _ok:
				print("TEST_BATTLE_QTE_TOUCH_I18N_OK")
				quit(0)
			else:
				printerr("TEST_BATTLE_QTE_TOUCH_I18N_FAIL")
				quit(1)
			return true
	return false
