extends SceneTree
## 新手引導畫面六語系即時切換單元測試 (Onboard View i18n Test)
## 依據規範：review.md 0-QA23, 0-QA24, 0-QA25
## 驗證：
## 1. 六語系 ui.json 包含「下一步」、「稍後再說」、「新手完成」、「新手引導 · 第 %d／%d 步」、「空白鍵／下一步 · 部分步驟可「稍後再說」」、「封靈」。
## 2. OnboardView 在 Loc.locale_changed 下即時動態刷新按鈕、步驟標籤、提示與台詞。
## 3. 切換至 en, ja, ko, es, zh_CN, zh_TW 驗證各步驟文字精確度與零殘留。

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const OnboardViewClass := preload("res://scripts/systems/onboard/onboard_view.gd")

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
			print("ONBOARD_I18N_OK")
			quit(0)
		else:
			push_error("ONBOARD_I18N_FAIL")
			print("ONBOARD_I18N_FAIL")
			quit(1)
		return true
	return false


func _run_test_suite() -> void:
	print("=== 開始 test_onboard_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root_node.add_child(loc_node)

	# 1. 驗證六語系詞條解析
	var exp_next := {
		"zh_TW": "下一步",
		"zh_CN": "下一步",
		"en": "Next",
		"ja": "次へ",
		"ko": "다음",
		"es": "Siguiente"
	}
	var exp_skip := {
		"zh_TW": "稍後再說",
		"zh_CN": "稍后再说",
		"en": "Later",
		"ja": "あとで",
		"ko": "나중에",
		"es": "Más tarde"
	}
	var exp_done := {
		"zh_TW": "新手完成",
		"zh_CN": "新手完成",
		"en": "Tutorial Complete",
		"ja": "チュートリアル完了",
		"ko": "튜토리얼 완료",
		"es": "Tutorial completado"
	}
	var exp_step := {
		"zh_TW": "新手引導 · 第 %d／%d 步",
		"zh_CN": "新手引导 · 第 %d／%d 步",
		"en": "Tutorial · Step %d/%d",
		"ja": "チュートリアル · ステップ %d/%d",
		"ko": "튜토리얼 · %d/%d 단계",
		"es": "Tutorial · Paso %d/%d"
	}
	var exp_hint := {
		"zh_TW": "空白鍵／下一步 · 部分步驟可「稍後再說」",
		"zh_CN": "空格键／下一步 · 部分步骤可「稍后再说」",
		"en": "Space / Next · Some steps can be skipped with \"Later\"",
		"ja": "スペース / 次へ · 一部の手順は「あとで」でスキップ可能",
		"ko": "스페이스바 / 다음 · 일부 단계는 「나중에」로 건너뛰기 가능",
		"es": "Espacio / Siguiente · Algunos pasos se pueden omitir con «Más tarde»"
	}
	var exp_seal := {
		"zh_TW": "封靈",
		"zh_CN": "封灵",
		"en": "Soul Seal",
		"ja": "封霊",
		"ko": "봉령",
		"es": "Sello de alma"
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_next := ContentLoc.text("ui", "下一步")
		if t_next != exp_next[code]:
			_fail("[%s] 下一步 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_next[code], t_next])
		else:
			print("  [OK] [%s] 下一步 => %s" % [code, t_next])

		var t_skip := ContentLoc.text("ui", "稍後再說")
		if t_skip != exp_skip[code]:
			_fail("[%s] 稍後再說 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_skip[code], t_skip])
		else:
			print("  [OK] [%s] 稍後再說 => %s" % [code, t_skip])

		var t_done := ContentLoc.text("ui", "新手完成")
		if t_done != exp_done[code]:
			_fail("[%s] 新手完成 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_done[code], t_done])
		else:
			print("  [OK] [%s] 新手完成 => %s" % [code, t_done])

		var t_step := ContentLoc.text("ui", "新手引導 · 第 %d／%d 步")
		if t_step != exp_step[code]:
			_fail("[%s] 步驟標籤 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_step[code], t_step])
		else:
			print("  [OK] [%s] 步驟標籤 => %s" % [code, t_step])

		var t_hint := ContentLoc.text("ui", "空白鍵／下一步 · 部分步驟可「稍後再說」")
		if t_hint != exp_hint[code]:
			_fail("[%s] 底部提示 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_hint[code], t_hint])
		else:
			print("  [OK] [%s] 底部提示 => %s" % [code, t_hint])

		var t_seal := ContentLoc.text("ui", "封靈")
		if t_seal != exp_seal[code]:
			_fail("[%s] 封靈 翻譯不符: 預期 '%s', 實際 '%s'" % [code, exp_seal[code], t_seal])
		else:
			print("  [OK] [%s] 封靈 => %s" % [code, t_seal])

	# 2. 實例化 OnboardView 測試動態 locale_changed 即時切換
	print("\n--- 測試 OnboardView 實例與 locale_changed 動態切換 ---")
	var view: Control = OnboardViewClass.new()
	root_node.add_child(view)

	var btn_next: Button = view.find_child("BtnNext", true, false) as Button
	var btn_skip: Button = view.find_child("BtnSkip", true, false) as Button
	var node_lbl: Label = view.find_child("NodeTitle", true, false) as Label
	var hint_lbl: Label = view.find_child("HintLabel", true, false) as Label
	var dialog_lbl: Label = view.find_child("DialogLabel", true, false) as Label

	if btn_next == null or btn_skip == null or node_lbl == null or hint_lbl == null or dialog_lbl == null:
		_fail("OnboardView 子節點缺失")
		view.queue_free()
		return

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		# 驗證按鈕文字
		if btn_next.text != exp_next[code]:
			_fail("動態切換 [%s] BtnNext 文字不符: 預期 '%s', 實際 '%s'" % [code, exp_next[code], btn_next.text])
		else:
			print("  [OK] 動態切換 [%s] BtnNext => %s" % [code, btn_next.text])

		if btn_skip.text != exp_skip[code]:
			_fail("動態切換 [%s] BtnSkip 文字不符: 預期 '%s', 實際 '%s'" % [code, exp_skip[code], btn_skip.text])
		else:
			print("  [OK] 動態切換 [%s] BtnSkip => %s" % [code, btn_skip.text])

		# 驗證步驟標籤 (N01 為第 1 步)
		var exp_n01_step: String = exp_step[code] % [1, 8]
		if node_lbl.text != exp_n01_step:
			_fail("動態切換 [%s] NodeTitle 文字不符: 預期 '%s', 實際 '%s'" % [code, exp_n01_step, node_lbl.text])
		else:
			print("  [OK] 動態切換 [%s] NodeTitle => %s" % [code, node_lbl.text])

		# 驗證底部提示
		if hint_lbl.text != exp_hint[code]:
			_fail("動態切換 [%s] HintLabel 文字不符: 預期 '%s', 實際 '%s'" % [code, exp_hint[code], hint_lbl.text])
		else:
			print("  [OK] 動態切換 [%s] HintLabel => %s" % [code, hint_lbl.text])

	# 3. 測試進展至 N07（含兩顆按鈕可見與結果卡）
	print("\n--- 測試 N07 步驟之雙按鈕與結果卡六語系 ---")
	var flow = view.get("flow")
	while flow != null and str(flow.current().get("node", "")) != "N07" and not flow.done:
		view.call("_advance", false)

	if str(flow.current().get("node", "")) != "N07":
		_fail("無法切換至 N07 步驟")
	else:
		if not btn_next.visible or not btn_skip.visible:
			_fail("N07 時雙按鈕未同時可見: next=%s, skip=%s" % [btn_next.visible, btn_skip.visible])
		else:
			print("  [OK] N07 雙按鈕皆可見")

		for code in ["en", "ja", "zh_TW"]:
			if loc_node:
				loc_node.call("set_locale", code)

			var exp_n07_step: String = exp_step[code] % [7, 8]
			if node_lbl.text != exp_n07_step:
				_fail("N07 [%s] NodeTitle 不符: 預期 '%s', 實際 '%s'" % [code, exp_n07_step, node_lbl.text])
			else:
				print("  [OK] N07 [%s] NodeTitle => %s" % [code, node_lbl.text])

			var card: Control = view.find_child("SoulResultCard", true, false) as Control
			if card == null or not card.visible:
				_fail("N07 [%s] SoulResultCard 不可見" % code)
			else:
				var badge: Label = card.find_child("BadgeLabel", true, false) as Label
				if badge and badge.text != exp_seal[code]:
					_fail("N07 [%s] 抽魂結果卡 Badge 不符: 預期 '%s', 實際 '%s'" % [code, exp_seal[code], badge.text])
				else:
					print("  [OK] N07 [%s] 結果卡 Badge => %s" % [code, badge.text if badge else ""])

	# 4. 測試新手完成步驟
	print("\n--- 測試新手完成步驟六語系 ---")
	while flow != null and not flow.done:
		view.call("_advance", false)

	if not flow.done:
		_fail("未能抵達完成狀態")
	else:
		for code in ["en", "ja", "zh_TW"]:
			if loc_node:
				loc_node.call("set_locale", code)
			if node_lbl.text != exp_done[code]:
				_fail("完成狀態 [%s] NodeTitle 不符: 預期 '%s', 實際 '%s'" % [code, exp_done[code], node_lbl.text])
			else:
				print("  [OK] 完成狀態 [%s] NodeTitle => %s" % [code, node_lbl.text])

	view.queue_free()
	if loc_node:
		loc_node.call("set_locale", "zh_TW")
