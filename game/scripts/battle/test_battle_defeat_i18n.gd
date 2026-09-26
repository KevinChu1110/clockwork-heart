extends SceneTree
## 戰鬥失敗復活彈窗六語系即時刷新單元測試 (test_battle_defeat_i18n.gd)
##
## 驗證：
## 1. 六語系 ui.json 包含標題、動能耗盡、二次機會說明、看廣告立即復活、結束戰鬥、今日上限、免廣告直接領取等詞條
## 2. 實例化 BattleDefeatDialog，開著彈窗時切換語系 (Loc.locale_changed)，整窗文字即時刷新
## 3. 移除廣告模式下 (has_removed_ads = true) 的說明與按鈕六語系即時切換
## 4. 廣告次數耗盡模式下 (can_claim = false) 的按鈕六語系即時切換
## 5. 0-QA24 檢核：en, es 語系下完全無 CJK 中文字元殘留；ja 日文漢字正確
## 6. 零系統 emoji、橫屏尺寸 740~760、按鈕高 >= 50px、關閉鈕 >= 50px

const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const BattleDefeatDialogClass = preload("res://scripts/battle/battle_defeat_dialog.gd")

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

var _ok := true
var _frame := 0
var _step := 0

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

func _initialize() -> void:
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

func _process(_delta: float) -> bool:
	_frame += 1
	match _step:
		0:
			if _frame >= 5:
				_step = 1
				_run_test_suite()
				if _ok:
					print("\n=======================================================")
					print("TEST_BATTLE_DEFEAT_I18N_OK")
					quit(0)
				else:
					push_error("TEST_BATTLE_DEFEAT_I18N_FAIL")
					print("TEST_BATTLE_DEFEAT_I18N_FAIL")
					quit(1)
				return true
	return false

func _run_test_suite() -> void:
	print("=== 開始 test_battle_defeat_i18n 測試 ===")

	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		var LocClass = load("res://scripts/autoload/loc.gd")
		if LocClass:
			loc_node = LocClass.new()
			loc_node.name = "Loc"
			root.add_child(loc_node)

	var gs = root.get_node_or_null("GameState")
	if gs == null:
		var GsClass = load("res://scripts/autoload/game_state.gd")
		if GsClass:
			gs = GsClass.new()
			gs.name = "GameState"
			root.add_child(gs)

	var es = root.get_node_or_null("EnergySystem")
	if es == null:
		var EsClass = load("res://scripts/systems/energy_system.gd")
		if EsClass:
			es = EsClass.new()
			es.name = "EnergySystem"
			root.add_child(es)

	if loc_node == null or gs == null or es == null:
		_fail("Autoload 節點初始化失敗")
		return

	# 1. 預期六語系對照表
	var expected_title := {
		"zh_TW": "戰鬥失敗",
		"zh_CN": "战斗失败",
		"en": "Defeat",
		"ja": "敗北",
		"ko": "전투 패배",
		"es": "Derrota",
	}

	var expected_sub := {
		"zh_TW": "發條動能耗盡，齒輪暫時停擺！",
		"zh_CN": "发条动能耗尽，齿轮暂时停摆！",
		"en": "Clockwork kinetic energy depleted, gears brought to a halt!",
		"ja": "ぜんまい動力が尽き、歯車が一時停止した！",
		"ko": "태엽 동력이 다하여, 톱니가 잠시 멈췄습니다!",
		"es": "¡La energía de la cuerda se ha agotado y los engranajes se han detenido!",
	}

	var expected_hint_normal := {
		"zh_TW": "二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！",
		"zh_CN": "二次机会：观看赞助广告即可重新上链，立即以 50% 生命值重返战场！",
		"en": "Second Chance: Watch a sponsor ad to rewind, returning to battle with 50% HP!",
		"ja": "セカンドチャンス：広告を視聴してぜんまいを巻き直し、HP 50% で即座に戦場へ復帰！",
		"ko": "두 번째 기회: 스폰서 광고를 시청하여 태엽을 다시 감고, 즉시 HP 50%로 전장에 복귀합니다!",
		"es": "Segunda oportunidad: ¡mira un anuncio para recargar la cuerda y vuelve al combate con 50% de PS!",
	}

	var expected_hint_no_ads := {
		"zh_TW": "二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！",
		"zh_CN": "二次机会：已移除广告，可直接重新上链，立即以 50% 生命值重返战场！",
		"en": "Second Chance: Ads removed, rewind directly and return to battle with 50% HP immediately!",
		"ja": "セカンドチャンス：広告削除済み、直接ぜんまいを巻き直して HP 50% で即座に戦場へ復帰！",
		"ko": "두 번째 기회: 광고가 제거되어 바로 태엽을 다시 감고, 즉시 HP 50%로 전장에 복귀합니다!",
		"es": "Segunda oportunidad: ¡anuncios eliminados, puedes recargar la cuerda directamente y volver al combate con 50% de PS!",
	}

	var expected_tip := {
		"zh_TW": "若是選擇承認敗北，將返回城鎮整頓裝備與招式。",
		"zh_CN": "若是选择承认败北，将返回城镇整顿装备与招式。",
		"en": "Accepting defeat will return you to town to reorganize equipment and skills.",
		"ja": "敗北を認める場合、町に戻って装備と技を整えます。",
		"ko": "패배를 인정하면 마을로 돌아가 장비와 기술을 정비합니다.",
		"es": "Si aceptas la derrota, volverás a la aldea a organizar tu equipo y técnicas.",
	}

	var expected_revive_btn_normal_fmt := {
		"zh_TW": "觀看廣告立即復活  (%d/%d)",
		"zh_CN": "观看广告立即复活  (%d/%d)",
		"en": "Watch Ad to Revive Instantly  (%d/%d)",
		"ja": "広告を見て即座に復活  (%d/%d)",
		"ko": "광고 보고 즉시 부활  (%d/%d)",
		"es": "Ver anuncio y revivir al instante  (%d/%d)",
	}

	var expected_revive_btn_no_ads_fmt := {
		"zh_TW": "已移除廣告，直接領取  (%d/%d)",
		"zh_CN": "已移除广告，直接领取  (%d/%d)",
		"en": "Ads Removed, Claim Directly  (%d/%d)",
		"ja": "広告削除済み、直接受取  (%d/%d)",
		"ko": "광고 제거됨, 즉시 수령  (%d/%d)",
		"es": "Anuncios eliminados, reclamar directamente  (%d/%d)",
	}

	var expected_revive_btn_limit_fmt := {
		"zh_TW": "今日復活次數已達上限 (0/%d)",
		"zh_CN": "今日复活次数已达上限 (0/%d)",
		"en": "Daily revives limit reached (0/%d)",
		"ja": "本日の復活上限に達しました (0/%d)",
		"ko": "오늘 부활 횟수 상한 도달 (0/%d)",
		"es": "Límite de resurrecciones diario alcanzado (0/%d)",
	}

	var expected_give_up := {
		"zh_TW": "結束戰鬥",
		"zh_CN": "结束战斗",
		"en": "End Battle",
		"ja": "戦闘終了",
		"ko": "전투 종료",
		"es": "Terminar combate",
	}

	print("\n--- 1. 驗證六語系字典靜態映射與 ContentLoc.text ---")
	for code in LOCALES:
		loc_node.call("set_locale", code)
		ContentLoc.reload()

		var t_title := ContentLoc.text("ui", "戰鬥失敗")
		if t_title != expected_title[code]:
			_fail("[%s] 標題翻譯不符: 期望 '%s'，實際 '%s'" % [code, expected_title[code], t_title])

		var t_sub := ContentLoc.text("ui", "發條動能耗盡，齒輪暫時停擺！")
		if t_sub != expected_sub[code]:
			_fail("[%s] 動能耗盡說明不符: 期望 '%s'，實際 '%s'" % [code, expected_sub[code], t_sub])

		var t_hint := ContentLoc.text("ui", "二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！")
		if t_hint != expected_hint_normal[code]:
			_fail("[%s] 二次機會說明不符: 期望 '%s'，實際 '%s'" % [code, expected_hint_normal[code], t_hint])

		var t_revive := ContentLoc.text("ui", "觀看廣告立即復活  (%d/%d)")
		if t_revive != expected_revive_btn_normal_fmt[code]:
			_fail("[%s] 復活按鈕不符: 期望 '%s'，實際 '%s'" % [code, expected_revive_btn_normal_fmt[code], t_revive])

		var t_give_up := ContentLoc.text("ui", "結束戰鬥")
		if t_give_up != expected_give_up[code]:
			_fail("[%s] 結束戰鬥按鈕不符: 期望 '%s'，實際 '%s'" % [code, expected_give_up[code], t_give_up])

		if code in ["en", "es"]:
			if _has_cjk(t_title) or _has_cjk(t_sub) or _has_cjk(t_hint) or _has_cjk(t_revive) or _has_cjk(t_give_up):
				_fail("[%s] 詞條存在 CJK 中文字元殘留！" % code)

		if _has_emoji(t_title) or _has_emoji(t_sub) or _has_emoji(t_hint) or _has_emoji(t_revive) or _has_emoji(t_give_up):
			_fail("[%s] 詞條存在 Emoji！" % code)

		print("  ✓ [%s] 字典詞條檢核通過 (標題: '%s', 復活鈕: '%s', 放棄鈕: '%s')" % [
			code, t_title, t_revive % [3, 3], t_give_up
		])

	print("\n--- 2. 驗證 BattleDefeatDialog 實例與 locale_changed 即時動態連動 ---")
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	gs.reset_new_game()
	gs.has_removed_ads = false
	es.refresh()
	es.refresh_ad_daily()

	var dlg: Control = BattleDefeatDialogClass.new()
	root.add_child(dlg)

	var title_node: Label = dlg.find_child("TitleLbl", true, false) as Label
	var sub_node: Label = dlg.find_child("SubLbl", true, false) as Label
	var hint_node: Label = dlg.find_child("HintLbl", true, false) as Label
	var tip_node: Label = dlg.find_child("TipLbl", true, false) as Label
	var revive_btn_node: Button = dlg.find_child("ReviveAdBtn", true, false) as Button
	var give_up_btn_node: Button = dlg.find_child("GiveUpBtn", true, false) as Button
	var card_node: PanelContainer = dlg.find_child("DefeatCard", true, false) as PanelContainer
	var close_node: Button = dlg.find_child("CloseBtn", true, false) as Button

	if title_node == null or sub_node == null or hint_node == null or tip_node == null or revive_btn_node == null or give_up_btn_node == null:
		_fail("BattleDefeatDialog 子節點查找失敗")
		dlg.queue_free()
		return

	# 尺寸規範驗證 (橫屏 740~760，按鈕高 >= 50px，關閉鈕 >= 50px)
	if card_node.custom_minimum_size.x < 740 or card_node.custom_minimum_size.x > 760:
		_fail("卡片寬度不符規範 (740~760): %f" % card_node.custom_minimum_size.x)
	else:
		print("  ✓ 卡片寬度符合規範: %f" % card_node.custom_minimum_size.x)

	if revive_btn_node.custom_minimum_size.y < 50:
		_fail("復活按鈕高度小於 50px: %f" % revive_btn_node.custom_minimum_size.y)
	else:
		print("  ✓ 復活按鈕高度符合規範: %f" % revive_btn_node.custom_minimum_size.y)

	if give_up_btn_node.custom_minimum_size.y < 50:
		_fail("結束按鈕高度小於 50px: %f" % give_up_btn_node.custom_minimum_size.y)
	else:
		print("  ✓ 結束按鈕高度符合規範: %f" % give_up_btn_node.custom_minimum_size.y)

	if close_node == null or close_node.custom_minimum_size.x < 50 or close_node.custom_minimum_size.y < 50:
		_fail("關閉按鈕尺寸小於 50px: %s" % (close_node.custom_minimum_size if close_node else "null"))
	else:
		print("  ✓ 右上關閉按鈕尺寸符合規範: %s" % str(close_node.custom_minimum_size))

	# 初始繁中檢查
	if title_node.text != expected_title["zh_TW"]:
		_fail("初始繁中標題不符: %s" % title_node.text)
	if give_up_btn_node.text != expected_give_up["zh_TW"]:
		_fail("初始繁中結束按鈕不符: %s" % give_up_btn_node.text)
	if not revive_btn_node.text.contains("觀看廣告立即復活"):
		_fail("初始繁中看廣告按鈕不符: %s" % revive_btn_node.text)
	print("  ✓ 初始繁中內容驗證正確")

	# 動態切換六語系測試 (彈窗保持開啟狀態)
	for code in LOCALES:
		loc_node.call("set_locale", code)

		var exp_title: String = expected_title[code]
		var exp_sub: String = expected_sub[code]
		var exp_hint: String = expected_hint_normal[code]
		var exp_revive: String = expected_revive_btn_normal_fmt[code] % [3, 3]
		var exp_give_up: String = expected_give_up[code]

		if title_node.text != exp_title:
			_fail("[%s] 標題未即時更新: 實際 '%s'，期望 '%s'" % [code, title_node.text, exp_title])
		if sub_node.text != exp_sub:
			_fail("[%s] 動能耗盡說明未即時更新: 實際 '%s'，期望 '%s'" % [code, sub_node.text, exp_sub])
		if hint_node.text != exp_hint:
			_fail("[%s] 二次機會說明未即時更新: 實際 '%s'，期望 '%s'" % [code, hint_node.text, exp_hint])
		if revive_btn_node.text != exp_revive:
			_fail("[%s] 復活按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, revive_btn_node.text, exp_revive])
		if give_up_btn_node.text != exp_give_up:
			_fail("[%s] 結束按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, give_up_btn_node.text, exp_give_up])

		if code in ["en", "es"]:
			if _has_cjk(title_node.text) or _has_cjk(sub_node.text) or _has_cjk(hint_node.text) or _has_cjk(revive_btn_node.text) or _has_cjk(give_up_btn_node.text):
				_fail("[%s] 畫面文字存在 CJK 中文字元殘留！" % code)

		if _has_emoji(title_node.text) or _has_emoji(sub_node.text) or _has_emoji(hint_node.text) or _has_emoji(revive_btn_node.text) or _has_emoji(give_up_btn_node.text):
			_fail("[%s] 畫面文字存在 Emoji！" % code)

		print("  ✓ [%s] 開窗即時切換連動驗證成功: 標題='%s' | 復活鈕='%s' | 結束鈕='%s'" % [
			code, title_node.text, revive_btn_node.text, give_up_btn_node.text
		])

	print("\n--- 3. 驗證已移除廣告模式 (has_removed_ads = true) 下的六語系即時切換 ---")
	gs.has_removed_ads = true
	dlg.call("_refresh_display")

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var exp_hint_no: String = expected_hint_no_ads[code]
		var exp_btn_no: String = expected_revive_btn_no_ads_fmt[code] % [3, 3]

		if hint_node.text != exp_hint_no:
			_fail("[%s] 免廣告二次機會說明未即時更新: 實際 '%s'，期望 '%s'" % [code, hint_node.text, exp_hint_no])
		if revive_btn_node.text != exp_btn_no:
			_fail("[%s] 免廣告復活按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, revive_btn_node.text, exp_btn_no])

		if code in ["en", "es"]:
			if _has_cjk(hint_node.text) or _has_cjk(revive_btn_node.text):
				_fail("[%s] 免廣告畫面文字存在 CJK 殘留！" % code)

		print("  ✓ [%s] 免廣告即時切換連動驗證成功: 復活鈕='%s'" % [code, revive_btn_node.text])

	print("\n--- 4. 驗證次數上限耗盡模式下的六語系即時切換 ---")
	# 設為次數已用盡 (3/3)
	gs.has_removed_ads = false
	gs.set_flag("battle.ad_revive_count", 3)
	dlg.call("_refresh_display")

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var exp_btn_limit: String = expected_revive_btn_limit_fmt[code] % 3
		if revive_btn_node.text != exp_btn_limit:
			_fail("[%s] 次數用盡按鈕未即時更新: 實際 '%s'，期望 '%s'" % [code, revive_btn_node.text, exp_btn_limit])
		if not revive_btn_node.disabled:
			_fail("[%s] 次數用盡按鈕應為 disabled" % code)

		print("  ✓ [%s] 次數用盡按鈕即時切換連動驗證成功: 按鈕='%s'" % [code, revive_btn_node.text])

	# 測試完畢清理
	dlg.queue_free()
	loc_node.call("set_locale", "zh_TW")
	ContentLoc.reload()
	gs.reset_new_game()
	print("  ✓ 測試清理與語系復原完成")
