extends SceneTree
## 每日發條彈窗六語系單元測試 (Windup Daily Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含「冒險委託 · 今天誰需要上發條」、「離開委託」、「前往出征」、「今日委託已完成（當日不可再領）」等對應翻譯。
## 2. 每日發條彈窗在六語系切換下，標題、按鈕、獎勵句與個案提示即時連動刷新。
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字精確度。

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const WindupDailyDialogClass = preload("res://scripts/ui/windup_daily_dialog.gd")

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
			print("WINDUP_DAILY_I18N_OK")
			quit(0)
		else:
			push_error("WINDUP_DAILY_I18N_FAIL")
			print("WINDUP_DAILY_I18N_FAIL")
			quit(1)
		return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_windup_daily_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證詞條字典解析
	var expected_title := {
		"zh_TW": "冒險委託 · 今天誰需要上發條",
		"zh_CN": "冒险委托 · 今天谁需要上发条",
		"en": "Adventure Commission · Who Needs Winding Today?",
		"ja": "冒険依頼 · 今日ゼンマイを巻くのは誰？",
		"ko": "모험 의뢰 · 오늘 태엽을 감아야 할 자는 누구인가",
		"es": "Comisión de Aventura · ¿A quién hay que darle cuerda hoy?"
	}
	var expected_leave := {
		"zh_TW": "離開委託",
		"zh_CN": "离开委托",
		"en": "Leave Commission",
		"ja": "依頼を離れる",
		"ko": "의뢰 떠나기",
		"es": "Salir de la Comisión"
	}
	var expected_sortie := {
		"zh_TW": "前往出征",
		"zh_CN": "前往出征",
		"en": "Set Out to Battle",
		"ja": "出征する",
		"ko": "출정하기",
		"es": "Partir a la Batalla"
	}
	var expected_done := {
		"zh_TW": "今日委託已完成（當日不可再領）",
		"zh_CN": "今日委托已完成（当日不可再领）",
		"en": "Today's Commission Completed (Cannot claim again today)",
		"ja": "本日の依頼達成済（当日再受取不可）",
		"ko": "오늘 의뢰 완료됨 (당일 재수령 불가)",
		"es": "Comisión de hoy completada (No disponible de nuevo hoy)"
	}
	var expected_reward := {
		"zh_TW": "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1",
		"zh_CN": "完成委托奖励：金币 +25、星尘 +1、发条碎片 +1",
		"en": "Commission Reward: Gold +25, Stardust +1, Windup Fragment +1",
		"ja": "依頼達成報酬：ゴールド +25、星屑 +1、ゼンマイの破片 +1",
		"ko": "의뢰 완료 보상: 골드 +25, 스타더스트 +1, 태엽 파편 +1",
		"es": "Recompensa de Comisión: Oro +25, Polvo Estelar +1, Fragmento de Cuerda +1"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "冒險委託 · 今天誰需要上發條")
		if t_title != expected_title[code]:
			_fail("語系 [%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])
		else:
			print("  ✓ [%s] 標題 -> %s" % [code, t_title])

		var t_leave := ContentLoc.text("ui", "離開委託")
		if t_leave != expected_leave[code]:
			_fail("語系 [%s] 離開委託翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_leave[code], t_leave])
		else:
			print("  ✓ [%s] 離開委託 -> %s" % [code, t_leave])

		var t_sortie := ContentLoc.text("ui", "前往出征")
		if t_sortie != expected_sortie[code]:
			_fail("語系 [%s] 前往出征翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_sortie[code], t_sortie])
		else:
			print("  ✓ [%s] 前往出征 -> %s" % [code, t_sortie])

		var t_done := ContentLoc.text("ui", "今日委託已完成（當日不可再領）")
		if t_done != expected_done[code]:
			_fail("語系 [%s] 今日委託已完成翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_done[code], t_done])
		else:
			print("  ✓ [%s] 今日委託已完成 -> %s" % [code, t_done])

		var t_reward := ContentLoc.text("ui", "完成委託獎勵：金幣 +25、星塵 +1、發條碎片 +1")
		if t_reward != expected_reward[code]:
			_fail("語系 [%s] 完成委託獎勵翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_reward[code], t_reward])
		else:
			print("  ✓ [%s] 完成委託獎勵 -> %s" % [code, t_reward])

	# 2. 驗證 WindupDailyDialog 節點即時連動切換
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var dialog = WindupDailyDialogClass.new()
	root_node.add_child(dialog)

	# 驗證 zh_TW 初始
	var title_lbl: Label = dialog.find_child("TitleLabel", true, false)
	var btn_leave: Button = dialog.find_child("BtnCloseWindup", true, false)
	var msg_lbl: Label = dialog.find_child("MsgLabel", true, false)

	if not title_lbl or title_lbl.text != expected_title["zh_TW"]:
		_fail("zh_TW 初始標題不符: %s" % (title_lbl.text if title_lbl else "null"))
	if not btn_leave or btn_leave.text != expected_leave["zh_TW"]:
		_fail("zh_TW 初始離開鈕不符: %s" % (btn_leave.text if btn_leave else "null"))
	if not msg_lbl or msg_lbl.text != expected_reward["zh_TW"]:
		_fail("zh_TW 初始獎勵句不符: %s" % (msg_lbl.text if msg_lbl else "null"))

	# 即時切換至 en
	if loc_node:
		loc_node.call("set_locale", "en")
	if title_lbl.text != expected_title["en"]:
		_fail("切換 en 後標題未連動: %s" % title_lbl.text)
	else:
		print("  ✓ 切換 en 後標題動態變更 -> ", title_lbl.text)

	if btn_leave.text != expected_leave["en"]:
		_fail("切換 en 後離開鈕未連動: %s" % btn_leave.text)
	else:
		print("  ✓ 切換 en 後離開鈕動態變更 -> ", btn_leave.text)

	if msg_lbl.text != expected_reward["en"]:
		_fail("切換 en 後獎勵句未連動: %s" % msg_lbl.text)
	else:
		print("  ✓ 切換 en 後獎勵句動態變更 -> ", msg_lbl.text)

	# 即時切換至 ja
	if loc_node:
		loc_node.call("set_locale", "ja")
	if title_lbl.text != expected_title["ja"]:
		_fail("切換 ja 後標題未連動: %s" % title_lbl.text)
	else:
		print("  ✓ 切換 ja 後標題動態變更 -> ", title_lbl.text)

	if btn_leave.text != expected_leave["ja"]:
		_fail("切換 ja 後離開鈕未連動: %s" % btn_leave.text)
	else:
		print("  ✓ 切換 ja 後離開鈕動態變更 -> ", btn_leave.text)

	if msg_lbl.text != expected_reward["ja"]:
		_fail("切換 ja 後獎勵句未連動: %s" % msg_lbl.text)
	else:
		print("  ✓ 切換 ja 後獎勵句動態變更 -> ", msg_lbl.text)

	# 驗證已完成狀態 (done)
	var ws = root_node.get_node_or_null("WindupDailySystem")
	var gs = root_node.get_node_or_null("GameState")
	if gs:
		gs.call("set_flag", "windup.done", true)
	if ws:
		ws.call("refresh")
	dialog.call("_refresh_display")

	var btn_sortie: Button = dialog.find_child("BtnGoSortie", true, false)
	var btn_done: Button = dialog.find_child("BtnDoneStatus", true, false)

	if not btn_sortie or btn_sortie.text != expected_sortie["ja"]:
		_fail("ja 已完成狀態下出征鈕文字不符: %s" % (btn_sortie.text if btn_sortie else "null"))
	else:
		print("  ✓ [ja] 出征鈕 -> ", btn_sortie.text)

	if not btn_done or btn_done.text != expected_done["ja"]:
		_fail("ja 已完成狀態下已完成鈕文字不符: %s" % (btn_done.text if btn_done else "null"))
	else:
		print("  ✓ [ja] 今日已完成鈕 -> ", btn_done.text)

	# 切換回 en 驗證已完成按鈕連動
	if loc_node:
		loc_node.call("set_locale", "en")
	if btn_sortie.text != expected_sortie["en"]:
		_fail("en 已完成狀態下出征鈕文字不符: %s" % btn_sortie.text)
	else:
		print("  ✓ [en] 出征鈕動態變更 -> ", btn_sortie.text)

	if btn_done.text != expected_done["en"]:
		_fail("en 已完成狀態下已完成鈕文字不符: %s" % btn_done.text)
	else:
		print("  ✓ [en] 今日已完成鈕動態變更 -> ", btn_done.text)

	# 還原狀態
	if gs:
		gs.call("set_flag", "windup.done", false)
	dialog.queue_free()
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
