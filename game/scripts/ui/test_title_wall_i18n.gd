extends SceneTree
## 稱號牆彈窗六語系單元測試 (Title Wall Dialog i18n Test)
## 驗證：
## 1. 六語系 ui.json 包含標題、計數格式、解鎖標籤、按鈕、提示條等詞條對應翻譯
## 2. 實例化 TitleWallDialog，在切換 locale 時，標題、按鈕、計數、提示條與卡片標籤即時刷新
## 3. 切換至 en、ja、ko、es、zh_CN、zh_TW 驗證文字無硬編繁中殘留且無系統 emoji

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

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
					print("TEST_TITLE_WALL_I18N_OK")
					quit(0)
				else:
					push_error("TEST_TITLE_WALL_I18N_FAIL")
					print("TEST_TITLE_WALL_I18N_FAIL")
					quit(1)
				return true
	return false


func _find_named(node: Node, target_name: String) -> Node:
	if node.name == target_name:
		return node
	for c in node.get_children():
		var res := _find_named(c, target_name)
		if res != null:
			return res
	return null


func _check_no_system_emoji(text: String, context: String) -> void:
	for c in text:
		var code := c.unicode_at(0)
		if (code >= 0x1F300 and code <= 0x1F9FF) or (code >= 0x2600 and code <= 0x27BF):
			_fail("在 [%s] 發現系統 emoji: %s (code 0x%X)" % [context, c, code])


func _run_test_suite() -> void:
	print("=== 開始 test_title_wall_i18n 測試 ===")

	var root_node = root
	var loc_node = root_node.get_node_or_null("Loc")
	var tc = root_node.get_node_or_null("TitleCatalog")

	# 1. 驗證六語系詞條字典解析
	print("\n--- 1. 驗證六語系詞條字典解析 ---")
	var expected_title := {
		"zh_TW": "成就 · 稱號牆",
		"zh_CN": "成就 · 称号墙",
		"en": "Achievements · Title Wall",
		"ja": "実績 · 称号の壁",
		"ko": "업적 · 칭호의 벽",
		"es": "Logros · Muro de títulos",
	}
	var expected_unlocked := {
		"zh_TW": "已解鎖",
		"zh_CN": "已解锁",
		"en": "Unlocked",
		"ja": "解放済み",
		"ko": "해금됨",
		"es": "Desbloqueado",
	}
	var expected_locked := {
		"zh_TW": "未解鎖",
		"zh_CN": "未解锁",
		"en": "Locked",
		"ja": "未解放",
		"ko": "미해금",
		"es": "Bloqueado",
	}
	var expected_count_fmt := {
		"zh_TW": "（已解鎖 %d／%d）",
		"zh_CN": "（已解锁 %d／%d）",
		"en": "(Unlocked %d/%d)",
		"ja": "（解放済み %d／%d）",
		"ko": "（해금됨 %d/%d）",
		"es": "(Desbloqueado %d/%d)",
	}
	var expected_back := {
		"zh_TW": "返回標題",
		"zh_CN": "返回标题",
		"en": "Back to the title",
		"ja": "タイトルへ戻る",
		"ko": "타이틀로 돌아가기",
		"es": "Volver al título",
	}
	var expected_fortress := {
		"zh_TW": "堡壘",
		"zh_CN": "堡垒",
		"en": "Keep",
		"ja": "堡壘",
		"ko": "요새",
		"es": "Fortaleza",
	}
	var expected_newly_fmt := {
		"zh_TW": "新解鎖稱號：%s",
		"zh_CN": "新解锁称号：%s",
		"en": "Newly unlocked titles: %s",
		"ja": "新たに解放された称号：%s",
		"ko": "새로 해금된 칭호: %s",
		"es": "Nuevos títulos desbloqueados: %s",
	}

	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		var t_title := ContentLoc.text("ui", "成就 · 稱號牆")
		if t_title != expected_title[code]:
			_fail("語系 [%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])
		_check_no_system_emoji(t_title, "%s 標題" % code)

		var t_unlocked := ContentLoc.text("ui", "已解鎖")
		if t_unlocked != expected_unlocked[code]:
			_fail("語系 [%s] 已解鎖翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_unlocked[code], t_unlocked])

		var t_locked := ContentLoc.text("ui", "未解鎖")
		if t_locked != expected_locked[code]:
			_fail("語系 [%s] 未解鎖翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_locked[code], t_locked])

		var t_count := ContentLoc.text("ui", "（已解鎖 %d／%d）")
		if t_count != expected_count_fmt[code]:
			_fail("語系 [%s] 計數格式不符: 期望 '%s'，實際 '%s'" % [code, expected_count_fmt[code], t_count])

		var t_back := ContentLoc.text("ui", "返回標題")
		if t_back != expected_back[code]:
			_fail("語系 [%s] 返回標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_back[code], t_back])

		var t_fortress := ContentLoc.text("ui", "堡壘")
		if t_fortress != expected_fortress[code]:
			_fail("語系 [%s] 堡壘翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_fortress[code], t_fortress])

		var t_newly := ContentLoc.text("ui", "新解鎖稱號：%s")
		if t_newly != expected_newly_fmt[code]:
			_fail("語系 [%s] 新解鎖格式不符: 期望 '%s'，實際 '%s'" % [code, expected_newly_fmt[code], t_newly])

		print("  ✓ [%s] 詞條字典全部比對正確" % code)

	# 2. 實例化 TitleWallDialog 測試畫面文字與 locale_changed 動態連動
	print("\n--- 2. 測試 TitleWallDialog 實體化與 locale_changed 動態連動 ---")
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	var TitleWallDialogScn = load("res://scripts/ui/title_wall_dialog.gd")
	var dlg = TitleWallDialogScn.new()
	var dummy_cb = func(): pass
	var newly_mock: Array[String] = ["試煉第一步"]
	dlg.setup(newly_mock, dummy_cb, dummy_cb, "返回標題")
	root_node.add_child(dlg)

	var title_lbl := _find_named(dlg, "TitleLabel") as Label
	var count_lbl := _find_named(dlg, "CountLabel") as Label
	var newly_lbl := _find_named(dlg, "NewlyUnlockedLabel") as Label
	var back_btn := _find_named(dlg, "BackBtn") as Button
	var fortress_btn := _find_named(dlg, "FortressBtn") as Button

	if title_lbl == null or count_lbl == null or back_btn == null or fortress_btn == null or newly_lbl == null:
		_fail("無法找到 TitleWallDialog 關鍵 UI 節點")
		dlg.queue_free()
		return

	var cards: Array = dlg.call("get_cards")
	if cards.is_empty():
		_fail("TitleWallDialog 稱號卡片清單為空")
		dlg.queue_free()
		return

	var unl_num: int = tc.call("unlocked_count") if tc and tc.has_method("unlocked_count") else 0
	var tot_num: int = tc.call("total_count") if tc and tc.has_method("total_count") else 24

	# 驗證所有語系切換時的節點文字即時刷新
	for code in LOCALES:
		if loc_node:
			loc_node.call("set_locale", code)

		# 驗證標題
		if title_lbl.text != expected_title[code]:
			_fail("[%s] 標題文字未更新: 期望 '%s', 實際 '%s'" % [code, expected_title[code], title_lbl.text])

		# 驗證計數
		var exp_count_str: String = str(expected_count_fmt[code]) % [unl_num, tot_num]
		if count_lbl.text != exp_count_str:
			_fail("[%s] 計數文字未更新: 期望 '%s', 實際 '%s'" % [code, exp_count_str, count_lbl.text])

		# 驗證返回按鈕
		if back_btn.text != str(expected_back[code]):
			_fail("[%s] 返回按鈕文字未更新: 期望 '%s', 實際 '%s'" % [code, expected_back[code], back_btn.text])

		# 驗證堡壘按鈕
		if fortress_btn.text != str(expected_fortress[code]):
			_fail("[%s] 堡壘按鈕文字未更新: 期望 '%s', 實際 '%s'" % [code, expected_fortress[code], fortress_btn.text])

		# 驗證新解鎖稱號提示條
		var exp_newly_str: String = str(expected_newly_fmt[code]) % "、".join(newly_mock)
		if newly_lbl.text != exp_newly_str:
			_fail("[%s] 新解鎖提示文字未更新: 期望 '%s', 實際 '%s'" % [code, exp_newly_str, newly_lbl.text])

		# 驗證每張卡片的解鎖狀態標籤文字
		for card in cards:
			var badge := _find_named(card, "BadgeLabel") as Label
			if badge:
				var is_unl: bool = card.get_meta("is_unlocked", false)
				var exp_badge: String = expected_unlocked[code] if is_unl else expected_locked[code]
				if badge.text != exp_badge:
					_fail("[%s] 卡片解鎖狀態文字未更新: 期望 '%s', 實際 '%s'" % [code, exp_badge, badge.text])
				_check_no_system_emoji(badge.text, "%s 卡片狀態" % code)

		print("  ✓ [%s] TitleWallDialog 實體畫面即時刷新全部驗證通過 (標題=%s, 按鈕=%s, 狀態=%s)" % [
			code, title_lbl.text, back_btn.text, expected_unlocked[code]
		])

	dlg.queue_free()

	# 還原回 zh_TW
	if loc_node:
		loc_node.call("set_locale", "zh_TW")

	print("\n--- 3. 測試完成，全部項目通過 ---")
